# 杭州倍力钣金产品清单 — 判断"产品匹配"分数与 Sheet Metal Intensity 时查阅

判断一家候选企业时，逐条对照其产品照片/说明书/Datasheet/Exploded View 是否出现以下任一类别。命中类别越多、且这些零件明显是设备的结构性组成部分（不是偶尔用到的小配件），"产品匹配"分和 Sheet Metal Intensity 都应打得越高。

## 7.1 盖板 / 罩

Cover / Top Cover / Metal Cover / Sheet Metal Cover / Protective Cover / Equipment Cover

## 7.2 支架 / 支撑 / 托架

Bracket / Mounting Bracket / Support Bracket / Metal Bracket / Tray / Mount / Holder

## 7.3 安装板

Mounting Plate / Mounting Panel / Backplate / Terminal Mounting Plate / Fan Mounting Plate / Equipment Mounting Plate

## 7.4 底板 / 底框 / 底座

Base Plate / Base Frame / Bottom Plate / Bottom Cover / Metal Base / Chassis Base

## 7.5 壁挂结构

Wall Mount / Wall Mounting Plate / Wall Bracket / Back Mounting Bracket / Wall Plate

## 7.6 机箱 / 箱体 / 壳体

Enclosure / Sheet Metal Enclosure / Metal Enclosure / Chassis / Metal Chassis / Cabinet / Housing / Rack / Cage / Equipment Enclosure / Electrical Enclosure

## 7.7 内部结构件

Divider / Partition Plate / Back Plate / Side Panel / Adapter Plate / Connection Plate / Internal Panel

## 7.8 面板

Front Panel / Rear Panel / Control Panel / Equipment Panel / Sheet Metal Panel

## 7.9 挡板 / 防护

Baffle / Shield / Guard Plate / Safety Guard / Protective Plate

## 7.10 导轨

DIN Rail / Mounting Rail / Steel Rail / Equipment Rail

## 使用方式

不要只搜产品词本身（那样会大量命中钣金同行/贸易公司）。把这些词和行业词（见 `industry-targets.md`）、采购行为词组合，例如：

- `sheet metal enclosure` + `power supply manufacturer` + 国家名
- `mounting bracket` + `industrial automation` + 国家名
- `metal chassis` + `EV charger manufacturer` + 国家名

## 与 Sheet Metal Intensity 的对应关系

- 产品主体本身就是本清单里的箱体/机柜/机架（7.6）→ 通常是 **Very High**。
- 产品明显包含外壳、安装板、支架、底座、前后面板、内部隔板（7.1–7.5, 7.7–7.8）中的多类 → 通常是 **High**。
- 只命中其中一两类，且体积/占比不大 → **Medium**。
- 仅作为附件、装饰件或极少量辅助结构出现 → **Low**。
