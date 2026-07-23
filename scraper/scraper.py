#!/usr/bin/env python3
"""Lead-gen scraper for Europages public company-search pages.

Usage:
    python scraper.py                # full crawl, writes output/leads.xlsx
    python scraper.py --selftest      # fetch one page and report which
                                       # selector strategy matched, without
                                       # writing any output

IMPORTANT: This script has NOT been tested against the live site from this
machine (the dev sandbox that generated it has no outbound network access).
Europages' markup changes over time, so run --selftest first. If it reports
zero matches for every strategy, open output/debug_html/*.html in a browser,
inspect a listing card's selector, and add it to CARD_SELECTOR_CANDIDATES
below.

Also review europages.com's Terms of Service and robots.txt before running
a full crawl - this script checks robots.txt and refuses disallowed paths,
but that is not a substitute for reading the ToS yourself.
"""
import argparse
import csv
import random
import sys
import time
import urllib.robotparser
from pathlib import Path
from urllib.parse import quote

import requests
import yaml
from bs4 import BeautifulSoup

# Candidate CSS selectors for the element wrapping a single company listing.
# Tried in order; the first one that matches >0 elements on a page is used
# for that page. Add/replace entries here if --selftest reports 0 matches.
CARD_SELECTOR_CANDIDATES = [
    "div[data-testid='company-card']",
    "article.company-card",
    "div.company-card",
    "li.company-result",
    "div.card-content",
]

FIELD_SELECTORS = {
    "company_name": ["h2", "h3", "[data-testid='company-name']", "a.company-name"],
    "country": ["[data-testid='company-country']", ".country", "span.country"],
    "category": ["[data-testid='company-activity']", ".activity", ".category"],
    "link": ["a"],
}


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def robots_allows(base_url: str, robots_txt_url: str, path: str, user_agent: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_txt_url)
    try:
        rp.read()
    except Exception as exc:
        print(f"[warn] could not read robots.txt ({exc}); proceeding cautiously", file=sys.stderr)
        return True
    return rp.can_fetch(user_agent, base_url + path)


def fetch(session: requests.Session, url: str, config: dict) -> str | None:
    headers = {"User-Agent": config["user_agent"]}
    for attempt in range(3):
        try:
            resp = session.get(url, headers=headers, timeout=config["timeout_seconds"])
        except requests.RequestException as exc:
            print(f"[warn] request failed ({exc}), retrying...", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
            continue
        if resp.status_code == 200:
            return resp.text
        if resp.status_code in (429, 503):
            wait = 10 * (attempt + 1)
            print(f"[warn] got {resp.status_code}, backing off {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        print(f"[error] {url} -> HTTP {resp.status_code}", file=sys.stderr)
        return None
    return None


def _first_text(el, selectors: list[str]) -> str:
    for sel in selectors:
        found = el.select_one(sel)
        if found and found.get_text(strip=True):
            return found.get_text(strip=True)
    return ""


def parse_listings(html: str, base_url: str) -> tuple[list[dict], str | None]:
    """Returns (rows, selector_used). selector_used is None if nothing matched."""
    soup = BeautifulSoup(html, "lxml")
    for selector in CARD_SELECTOR_CANDIDATES:
        cards = soup.select(selector)
        if not cards:
            continue
        rows = []
        for card in cards:
            link_el = card.select_one("a[href]")
            href = link_el["href"] if link_el else ""
            if href.startswith("/"):
                href = base_url + href
            rows.append(
                {
                    "company_name": _first_text(card, FIELD_SELECTORS["company_name"]),
                    "country": _first_text(card, FIELD_SELECTORS["country"]),
                    "category": _first_text(card, FIELD_SELECTORS["category"]),
                    "source_url": href,
                }
            )
        rows = [r for r in rows if r["company_name"]]
        if rows:
            return rows, selector
    return [], None


def dump_debug_html(html: str, dump_dir: str, tag: str) -> None:
    Path(dump_dir).mkdir(parents=True, exist_ok=True)
    out = Path(dump_dir) / f"{tag}.html"
    out.write_text(html, encoding="utf-8")
    print(f"[debug] saved raw HTML to {out} for selector inspection", file=sys.stderr)


def write_output(rows: list[dict], config: dict) -> None:
    dedupe_keys = config["output"]["dedupe_on"]
    seen = set()
    unique_rows = []
    for row in rows:
        key = tuple(row.get(k, "") for k in dedupe_keys)
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)

    out_path = Path(config["output"]["path"])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = "leads"
        columns = ["company_name", "country", "category", "source_url", "search_keyword"]
        ws.append(columns)
        for row in unique_rows:
            ws.append([row.get(c, "") for c in columns])
        wb.save(out_path)
        print(f"[ok] wrote {len(unique_rows)} unique leads to {out_path}")
    except ImportError:
        csv_path = out_path.with_suffix(".csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["company_name", "country", "category", "source_url", "search_keyword"])
            writer.writeheader()
            writer.writerows(unique_rows)
        print(f"[ok] openpyxl not installed; wrote {len(unique_rows)} unique leads to {csv_path}")


def crawl(config: dict, selftest: bool = False) -> list[dict]:
    session = requests.Session()
    all_rows: list[dict] = []
    keywords = config["keywords"][:1] if selftest else config["keywords"]
    max_pages = 1 if selftest else config["max_pages_per_keyword"]

    for keyword in keywords:
        slug = quote(keyword)
        for page in range(1, max_pages + 1):
            url = config["site"]["search_url_template"].format(keyword=slug, page=page)
            path = url.replace(config["site"]["base_url"], "")
            if not robots_allows(
                config["site"]["base_url"], config["site"]["robots_txt_url"], path, config["user_agent"]
            ):
                print(f"[stop] robots.txt disallows {path}", file=sys.stderr)
                return all_rows

            print(f"[fetch] {url}")
            html = fetch(session, url, config)
            if html is None:
                break

            rows, selector_used = parse_listings(html, config["site"]["base_url"])
            if selftest:
                print(f"[selftest] selector candidates tried: {CARD_SELECTOR_CANDIDATES}")
                print(f"[selftest] matched selector: {selector_used!r}, rows found: {len(rows)}")
                if not rows:
                    dump_debug_html(html, config["debug_dump_dir"], f"selftest_{keyword.replace(' ', '_')}")
                return rows

            if not rows:
                dump_debug_html(html, config["debug_dump_dir"], f"{keyword.replace(' ', '_')}_p{page}")
                print(f"[warn] no listings parsed for '{keyword}' page {page}; stopping this keyword", file=sys.stderr)
                break

            for r in rows:
                r["search_keyword"] = keyword
            all_rows.extend(rows)

            delay = config["request_delay_seconds"] + random.uniform(0, config["request_delay_jitter"])
            time.sleep(delay)

    return all_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--selftest", action="store_true", help="fetch one page, report selector match, no output file")
    args = parser.parse_args()

    config = load_config(args.config)
    rows = crawl(config, selftest=args.selftest)

    if args.selftest:
        return

    if not rows:
        print("[error] no leads collected - check output/debug_html for the raw pages and update selectors", file=sys.stderr)
        sys.exit(1)

    write_output(rows, config)


if __name__ == "__main__":
    main()
