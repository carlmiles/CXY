# 外贸获客线索工具（钣金加工行业 / Europages）

从 Europages 公开企业搜索页抓取潜在客户线索（公司名、国家、行业分类、来源链接），
按关键词分页采集，去重后导出为 Excel。

## 重要说明：先读这个

这份代码是在一个**无法访问外网**的沙盒环境里写的（当前会话的网络策略直接拒绝了对
europages.com 的连接），所以**从未在真实页面上跑过**。选择器（`scraper.py` 里的
`CARD_SELECTOR_CANDIDATES` / `FIELD_SELECTORS`）是基于对该类站点常见结构的合理猜测，
不保证和当前真实页面完全匹配。

**第一次使用必须先跑 selftest**，不要直接上全量抓取：

```bash
pip install -r requirements.txt
python scraper.py --selftest
```

- 如果输出 `rows found: 0` for 所有 selector：脚本会把原始 HTML 存到
  `output/debug_html/`，用浏览器打开这个文件，找到一个公司卡片的实际 CSS class，
  把它加进 `CARD_SELECTOR_CANDIDATES` 列表最前面，再跑一次 selftest。
- 如果匹配上了但字段（公司名/国家）是空的，同理去调整 `FIELD_SELECTORS`。

把调整好的 HTML 样例或者报错发给我，我可以帮你把选择器改对。

## 法律/合规提醒

- 运行前请自己看一遍 europages.com 的服务条款（ToS）和 `robots.txt`，确认允许自动化抓取；
  脚本里的 `robots_allows()` 只是按 robots.txt 做了个基本检查，**不代表法律上一定合规**。
- 默认加了限速（`request_delay_seconds` + 随机抖动），请不要调得太激进，避免对目标站点
  造成压力或触发封锁。
- 抓到的是网上公开展示的企业名录信息，用于 B2B 获客调研；如果计划批量发送营销邮件，
  还需要留意目标国家的反垃圾邮件法规（如欧盟 GDPR、美国 CAN-SPAM）。

## 使用方法

1. 修改 `config.yaml` 里的 `keywords`（默认是钣金加工相关的英文关键词，Europages 上
   英文关键词效果最好，不分具体地区）、`max_pages_per_keyword`。
2. `pip install -r requirements.txt`
3. `python scraper.py --selftest` 确认选择器可用
4. 确认没问题后跑全量：`python scraper.py`
5. 结果在 `output/leads.xlsx`，列：`company_name, country, category, source_url, search_keyword`

## 后续可以扩展

- 加一列联系状态/备注，当成简易 CRM 用（谈下来了再做也不迟，先把线索抓稳）
- 支持 Kompass 等其他目录站点：复制 `config.yaml` 里的 `site` 段配一份新的，
  Kompass 有更强的反爬（Cloudflare），大概率需要换成 Playwright 渲染 JS 才能拿到内容。
