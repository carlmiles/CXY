# Germany — 电力储能 / 工业自动化 试跑（2026-07-24）

技能：`global-sheet-metal-export-leads` V3
范围：Germany，第一优先级行业（电力与新能源 / 工业自动化）

## 方法论限制说明

本轮在 Claude Code Remote 的云端沙盒环境中执行，该环境的出网策略拦截了 WebFetch（直接访问任意外部网站返回 403，含 example.com，确认是策略性拒绝而非网站反爬或证书问题），只有 WebSearch 可用。这意味着本轮**无法直接打开企业官网/产品页核实图片和联系人**，只能依据搜索引擎摘要和第三方数据库交叉验证。

按 V3 技能规则，A 级（≥85 分）要求"至少看过企业官网、Product 页面、About/Manufacturing 页面"，本轮不具备这个条件，因此**所有评分都不打 A/A+，如实反映证据链的局限**，而不是为了演示效果虚报。后续切到本地（有完整联网权限）运行同一技能，可以把这些候选做到官网级别核实，评分可能上修。

## 客户台账

| Company | Country | Website | Discovery Date | Last Checked | Status | 客户等级 |
|---|---|---|---|---|---|---|
| TESVOLT AG | Germany | tesvolt.com | 2026-07-24 | 2026-07-24 | Researching | C (62/100) |
| Bicker Elektronik GmbH | Germany | bicker.de | 2026-07-24 | 2026-07-24 | Researching | D (45/100) |
| REFU Elektronik GmbH | Germany | refu.com | 2026-07-24 | 2026-07-24 | Rejected | D (41/100) |
| SMA Solar Technology AG | Germany | sma.de | 2026-07-24 | 2026-07-24 | Rejected | Exclude（规模超上限） |
| MENNEKES | Germany | mennekes.de | 2026-07-24 | 2026-07-24 | Rejected | Exclude（规模超上限） |
| Compleo Charging Solutions | Germany | compleo-cs.com | 2026-07-24 | 2026-07-24 | Rejected | Exclude（破产后并入 Kostal 集团） |
| AEG Power Solutions | Germany | aegps.com | 2026-07-24 | 2026-07-24 | Rejected | Exclude（规模超上限+刚被并购） |
| GVA Leistungselektronik GmbH | Germany | gva-power.de | 2026-07-24 | 2026-07-24 | Rejected | Exclude（产品非钣金机箱导向） |
| ABL GmbH (Wallbox) | Germany | abl.de | 2026-07-24 | 2026-07-24 | Rejected | Exclude（曾破产+现被西班牙集团收购） |

---

## TESVOLT AG — 62/100，客户等级 C（可以开发）

- **官网**：tesvolt.com
- **城市**：Lutherstadt Wittenberg, Germany
- **公司类型**：B类（自有品牌储能设备制造商，兼具部分自产组装能力）
- **主要产品**：商用/工业储能电池柜（30kWh–1MWh 级），户外集装箱式储能系统
- **员工规模**：Estimated Employees: 160–170（Confirmed，多来源交叉一致）
- **营收**：暂未找到可信数据。第三方数据库给出的数字（如 $7M）与其"年产 8 万套储能系统的 Gigafactory"规模明显矛盾，不采用。Revenue Confidence: Low
- **Sheet Metal Intensity**: Very High（Confirmed）——核心产品 PowerCore G2 / TAYTAN 系列本身就是 IP55/IP65 金属机柜、集装箱式系统，钣金外壳是产品主体
- **可能需要的钣金产品**：Enclosure / Cabinet / Base Frame / Front Panel / Internal Mounting Plate / Wall-mount bracket
- **匹配杭州倍力产品**：机箱/箱体、底板、面板、支架
- **为什么匹配**：产品就是电池储能柜和集装箱系统，钣金结构是产品本体，用量大、定制程度高
- **Sheet Metal Outsourcing Probability**: Medium（Inferred）——"Gigafactory"描述看是电芯/模组组装线，未找到自建激光切割/折弯/焊接车间的证据；同时在招"Operativer Einkäufer"（操作层采购岗），说明有活跃外部采购职能
- **China Sourcing Probability**: Low–Unknown（Inferred）——电芯来自三星 SDI（韩国），未发现中国办公室/亚洲采购团队/Made-in-China 部件的公开证据
- **Procurement Signal**: Medium（Confirmed，多来源交叉：pv-magazine、VDI-Nachrichten、TESVOLT 官方新闻稿）——2024年动工、2025年底投产第一期的新 Gigafactory，产能扩大10倍（年产4GWh/约8万套储能系统），投资约3000万欧元，新增400+岗位
- **Why Contact Now**：产能十倍扩张意味着电池柜/外壳类结构件采购量大概率同步放大，新工厂投产窗口（2025年底–2026年）是切入供应链评估的好时机
- **Primary Contact**：暂未找到公开信息
- **Secondary Contact**：暂未找到公开信息
- **Technical Contact**：Philipp Schreiber，Technical Project Manager（LinkedIn 可查，职责偏工程侧大型项目管理而非采购，仅供参考）
- **Company Phone**：+49 (0)3491 8797-100（Confirmed）
- **General Email**：info@tesvolt.com（Confirmed）
- **Contact Form**：tesvolt.com/en/company/contact.html
- **Supplier Registration**：暂未找到公开信息
- **Recommended Entry Product**：Battery cabinet outer enclosure / internal mounting plate
- **Recommended Entry Angle**：借新 Gigafactory 投产、产能十倍扩张窗口，以"能否为新增产能提供电池柜外壳/内部安装板备选加工产能"为切入点，而非泛泛推销钣金加工能力
- **风险点**：暂未找到具体采购联系人；China Sourcing 证据不足；营收数据不可靠
- **证据来源**：
  1. tesvolt.com/en/powercore.html, /en/batterycabinets.html, /en/containersysteme.html
  2. pv-magazine.de "Tesvolt investiert 60 Millionen Euro in neue Gigafactory" / "Spatenstich für die Verzehnfachung der Produktion"
  3. tesvolt.com 官方新闻稿 "Ground-breaking ceremony for the new TESVOLT Gigafactory"
  4. tesvolt-gmbh.jobs.personio.com 招聘页（Operativer Einkäufer 职位）
  5. tesvolt.com/en/company/contact.html

## Bicker Elektronik GmbH — 45/100，客户等级 D（低优先级，可留意）

- **官网**：bicker.de
- **城市**：Donauwörth, Germany
- **公司类型**：B类（家族自有品牌，工业电源/UPS制造商）
- **主要产品**：工业电源（3–24,000W）、AC/DC 与 DC UPS 系统、DIN 导轨模块
- **员工规模**：Estimated Employees: ~50（Confirmed，低于重点区间 80–500，但技能规则允许"小于80人但产品高度匹配同样可以开发"）
- **营收**：来源冲突（$2.5M vs "up to €10M"），Revenue Confidence: Low
- **Sheet Metal Intensity**: Medium——官网有独立产品分类 "Enclosed – Industrial Power Supplies – Chassis" 和 "Housing – Accessories"，IP65/IP67 铝合金外壳，但材质是铝合金而非确认的折弯钢板，强度打 Medium
- **匹配杭州倍力产品**：机箱、盖板、导轨相关支架
- **为什么匹配**：工业电源和 UPS 产品线里有独立的 Chassis/Housing 类目，说明外壳是标准化可替换零件
- **Sheet Metal Outsourcing Probability**: Medium（Inferred）——50人规模电子公司不太可能自建完整钣金车间，但无直接证据
- **China Sourcing Probability**: Unknown——无相关证据
- **Procurement Signal**: None——本轮未发现 RFQ/新工厂/相关招聘信号
- **Why Contact Now**: No immediate public trigger found.
- **Primary/Secondary/Technical Contact**：暂未找到公开联系人姓名
- **Company Phone**：+49 (0)906 70595-0（Confirmed）
- **General Email**：官网 Kontakt 页显示企业邮箱，本次搜索结果遮蔽了具体地址未能确认——推测邮箱，未验证，建议走 bicker.de/kontakt 联系表单
- **Recommended Entry Product**：Housing / Chassis for enclosed power supplies
- **Recommended Entry Angle**：针对 "Housing – Accessories" 产品线，问是否有外壳类零件的钣金加工产能需求
- **风险点**：规模偏小、无近期采购信号、外壳材质是否为钣金尚未确认
- **证据来源**：bicker.de/en/products/industrial-power-supplies/enclosed；bicker.de/en/products/accessories/housing；bicker.de/kontakt

## 筛掉/降级的候选（Step 1 快速排除）

| 公司 | 排除/降级理由 |
|---|---|
| SMA Solar Technology AG | 上市公司，员工数千人、营收远超 USD 300M 上限 |
| MENNEKES | 员工约1000–1600人，营收约130–300M+ EUR，明显超出目标规模，未发现例外信号 |
| Compleo Charging Solutions | 2022年破产，2023年被 Kostal 集团收购后作为品牌并入其运营体系，已非独立中小企业 |
| AEG Power Solutions | 员工约1519人，且2026年6月刚被 Hammond Power Solutions 收购 |
| GVA Leistungselektronik | 34人，但产品以功率半导体元件/散热器为主，钣金机箱类需求证据不足 |
| ABL GmbH（Wallbox） | 曾破产，现被西班牙 Wallbox N.V. 收购，员工超580人，规模和稳定性存疑 |
| REFU Elektronik GmbH | 隶属 PRETTL Group，该集团明确宣传其内部一体化供应链覆盖 housing（外壳）品类，集团内部很可能优先内部关联企业采购外壳，外部供应商切入难度较高 |

## 下一步建议

1. 切到有完整联网权限的环境（本地 Claude Code CLI）重跑同一技能，对 TESVOLT / Bicker 做官网+产品页级别核实，寻找具体采购/工程联系人，评分有机会上修到 B 级。
2. 路线 A（明确采购信号）本轮没有单独跑，建议下一轮专门搜 `sheet metal RFQ Germany` / `Blechgehäuse Hersteller gesucht` 之类信号词，和路线 B 并行。
3. 如果 TESVOLT 评估通过，建议先从 battery cabinet 外壳或内部安装板的小批量打样切入，而不是整套集装箱系统。
