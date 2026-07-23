#!/usr/bin/env python3
"""Buying-lead radar for Tradewheel's public /buyers/ category pages.

Usage:
    python scraper.py                # full run, updates master log + new_leads file
    python scraper.py --selftest      # fetch one page, report selector match, no output

IMPORTANT: This script has NOT been tested against the live site from this
machine (the dev sandbox that generated it has no outbound network access).
Run --selftest first. If it reports zero matches for every strategy, open
output/debug_html/*.html in a browser, inspect a lead card's actual selector,
and add it to CARD_SELECTOR_CANDIDATES below.

What this does NOT do: buyer contact details on trade-lead marketplaces are
normally gated behind a paid supplier account, and that's intentional - it's
the platform's business model, not a bug to work around. This script only
tracks publicly visible lead titles/summaries/dates and flags which ones are
NEW since your last run, so you know when to log into Tradewheel yourself
and respond to a fresh lead through their normal quote flow.

Review Tradewheel's Terms of Service and robots.txt before running a full
scan - the robots.txt check here is a basic courtesy check, not legal advice.
"""
import argparse
import json
import random
import sys
import time
import urllib.robotparser
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

# Candidate CSS selectors for the element wrapping a single buying lead.
# Tried in order; the first one that matches >0 elements on a page is used.
# Add/replace entries here if --selftest reports 0 matches.
CARD_SELECTOR_CANDIDATES = [
    "div[data-testid='lead-card']",
    "div.lead-card",
    "div.buying-lead",
    "li.lead-item",
    "div.post-item",
]

FIELD_SELECTORS = {
    "lead_title": ["h2", "h3", "a.lead-title", "[data-testid='lead-title']"],
    "country": ["[data-testid='lead-country']", ".country", "span.country"],
    "posted_date": ["[data-testid='lead-date']", ".date", "time"],
}


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_seen_store(path: str) -> set:
    p = Path(path)
    if not p.exists():
        return set()
    return set(json.loads(p.read_text(encoding="utf-8")))


def save_seen_store(path: str, seen: set) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(sorted(seen)), encoding="utf-8")


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
        if resp.status_code == 404:
            print(f"[warn] 404 at {url} - category slug is probably wrong", file=sys.stderr)
            return None
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
                    "lead_title": _first_text(card, FIELD_SELECTORS["lead_title"]),
                    "country": _first_text(card, FIELD_SELECTORS["country"]),
                    "posted_date": _first_text(card, FIELD_SELECTORS["posted_date"]),
                    "source_url": href,
                }
            )
        rows = [r for r in rows if r["lead_title"]]
        if rows:
            return rows, selector
    return [], None


def dump_debug_html(html: str, dump_dir: str, tag: str) -> None:
    Path(dump_dir).mkdir(parents=True, exist_ok=True)
    out = Path(dump_dir) / f"{tag}.html"
    out.write_text(html, encoding="utf-8")
    print(f"[debug] saved raw HTML to {out} for selector inspection", file=sys.stderr)


def write_xlsx(rows: list[dict], path: Path, columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "leads"
    ws.append(columns)
    for row in rows:
        ws.append([row.get(c, "") for c in columns])
    wb.save(path)


def crawl(config: dict, selftest: bool = False) -> list[dict]:
    session = requests.Session()
    all_rows: list[dict] = []
    categories = config["categories"][:1] if selftest else config["categories"]
    max_pages = 1 if selftest else config["max_pages_per_category"]

    for category in categories:
        for page in range(1, max_pages + 1):
            url = config["site"]["search_url_template"].format(category=category, page=page)
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
                    dump_debug_html(html, config["debug_dump_dir"], f"selftest_{category}")
                return rows

            if not rows:
                dump_debug_html(html, config["debug_dump_dir"], f"{category}_p{page}")
                print(f"[warn] no leads parsed for '{category}' page {page}; stopping this category", file=sys.stderr)
                break

            for r in rows:
                r["category"] = category
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

    # Dedupe within this run's results
    dedupe_keys = config["output"]["dedupe_on"]
    seen_this_run = set()
    unique_rows = []
    for row in rows:
        key = tuple(row.get(k, "") for k in dedupe_keys)
        if key in seen_this_run:
            continue
        seen_this_run.add(key)
        unique_rows.append(row)

    # Compare against leads seen in previous runs
    seen_store_path = config["seen_store_path"]
    previously_seen = load_seen_store(seen_store_path)
    new_rows = [r for r in unique_rows if r["source_url"] not in previously_seen]

    columns = ["lead_title", "country", "posted_date", "category", "source_url"]
    write_xlsx(unique_rows, Path(config["output"]["path"]), columns)
    print(f"[ok] wrote {len(unique_rows)} total leads to {config['output']['path']}")

    if new_rows:
        write_xlsx(new_rows, Path(config["output"]["new_leads_path"]), columns)
        print(f"[ok] {len(new_rows)} NEW leads since last run -> {config['output']['new_leads_path']}")
    else:
        print("[ok] no new leads since last run")

    previously_seen.update(r["source_url"] for r in unique_rows)
    save_seen_store(seen_store_path, previously_seen)


if __name__ == "__main__":
    main()
