# 外贸获客线索雷达（钣金加工行业 / Tradewheel 求购信息）

## 思路（和第一版不一样，先看这个）

第一版对着 Europages 抓的是"钣金加工服务供应商"目录——那里面躺的基本是同行，不是客户。

这一版换成 Tradewheel 的 `/buyers/` 求购信息页：这类页面是采购商主动发布的"我要买XX"
需求帖，是真实的采购信号，方向对了。但有个现实限制：**这类求购平台的买家联系方式通常
锁在付费供应商账号后面**，这是平台的商业模式，不是漏洞，这份工具不会去绕过它。

所以这个工具的定位是"线索雷达"：定期抓一遍公开可见的求购帖标题/国家/发布日期，
和上一次抓到的结果比对，**标出这次新出现的求购帖**，提醒你去 Tradewheel 上用供应商
账号登录、按平台正常流程去报价联系——新发布的求购帖越早响应，回复率越高，这个工具
省的是你每天手动刷页面的时间，不是帮你绕开付费墙。

## 重要说明：先读这个

代码是在一个**无法访问外网**的沙盒环境里写的，从未在真实页面上跑过。选择器
（`CARD_SELECTOR_CANDIDATES` / `FIELD_SELECTORS`）以及 `config.yaml` 里的分类 slug
（除了 `sheet-metal-parts` 是搜索确认过真实存在的，其余都是猜的）都需要你自己验证。

**第一次使用必须先跑 selftest**：

```bash
pip install -r requirements.txt
python scraper.py --selftest
```

- `rows found: 0`：脚本会把页面存到 `output/debug_html/`，浏览器打开看实际结构，
  把正确的 selector 加进 `CARD_SELECTOR_CANDIDATES` / `FIELD_SELECTORS` 最前面。
- 看到 `[warn] 404 ... 分类 slug 可能不对`：去 `config.yaml` 的 `categories` 里删掉/
  改正这个 slug（可以先手动在浏览器里试一下 `https://www.tradewheel.com/buyers/<slug>/`
  是否存在）。

调整好之后把新的 HTML 样例或报错发给我，我可以帮你把选择器改对。

## 法律/合规提醒

- 运行前自己看一遍 Tradewheel 的服务条款和 `robots.txt`；脚本里的 `robots_allows()`
  只是基本检查，不代表法律上一定合规。
- 只抓公开可见的求购帖标题/国家/日期，**不尝试获取被付费墙保护的联系方式**——那部分
  应该老老实实注册供应商账号去拿，这是平台合理的商业模式。
- 限速默认 3~5 秒/请求，别调太激进。

## 使用方法

1. `config.yaml` 里核对/调整 `categories`（钣金相关分类 slug）
2. `pip install -r requirements.txt`
3. `python scraper.py --selftest` 确认选择器可用
4. `python scraper.py` 跑全量
5. 看结果：
   - `output/buying_leads.xlsx`：历史全部线索（越滚越多）
   - `output/new_leads.xlsx`：**只看这个文件就行**，是这次新出现的求购帖
   - `output/seen_leads.json`：内部状态文件，记录哪些帖子已经见过，不用管

## 建议用法

定时跑（比如 cron 每天一次），每次看 `new_leads.xlsx` 有没有新东西，有就登录
Tradewheel 供应商账号去回复。这比每天手动刷网页效率高，但拿不到联系方式这件事
改变不了——这本来就是平台该收的钱。

## 后续可以扩展

- 同样的"雷达"模式可以套到 EC21、TradeKey、Global Sources 的求购版块
- 展会方向：EuroBLECH / FABTECH 每年的参展商目录里能找到很多做钣金上游设备/
  可能外发钣金件的下游制造商，值得单独做一份抓取配置
