# IPTV-Auto-Next MASTER_PLAN.md

版本：1.17-G3（基于 1.17 的全球频道库升级最终定稿完整版）  
文件性质：项目总施工规范，本项目唯一指导方针  
适用范围：整个项目的架构设计、开发实施、测试验收和正式发布  
本版本原则：以 MASTER_PLAN.md 1.17 为唯一母版，完整保留 1.17 所有稳定参数、安全约束和底层细节，仅进行全球频道库升级所必需的改造。本文件为唯一指导方针，所有开发者必须以本文件为准。

母版基准：
- 母版版本：MASTER_PLAN.md 1.17
- 母版 Commit：`c62b4c0e8a3c41ee2b50acdd9d00d55a2e7f3a75`
- 母版 SHA：`cae8fbf11bf90c1a125cadd3dc588518a929025d`
- 母版原文件：1,778 行，42,537 字符
- 不得使用 1.18、1.19 或此前压缩遗漏内容的 1.20 版本作为施工依据。

本版升级摘要：
1. `data/global_channels/channels.json` 是唯一全球频道身份库，不再维护另一套重复的频道主字典。
2. `config/channels.txt` 是用户频道选择入口：有有效内容按人工选择；空文件按默认四地区（CN, HK, MO, TW）。
3. 全球频道库仅负责身份识别，线路通过上游 Feed / Streams 发现。
4. 保留 1.17 全部稳定参数与安全约束（40源、100条/源、1000候选、8秒/60秒、DNS Rebinding防范等）。
5. 本修订版内化了全球频道库启动前核验、tvg_id 对齐、Feed/Streams 数据源接入规范、模块接口契约、冲突处理判定矩阵及统计口径等实施前必须确定的事项。
6. 本修订版不改变 1.17 任何稳定参数、安全约束、发布机制或验收边界。

---

## 1. 项目目标

### 1.1 核心目标

建设一个高效率、自动化运行的 IPv4 IPTV 直播源仓库。

系统持续收集直播源，执行统一的程序技术探测，筛选并发布符合首版技术支持范围的 IPv4 直播线路，同时如实记录国内网络验证状态。

系统必须实现：
1. 自动收集直播源。
2. 读取并校验全球频道身份库，按用户频道选择入口确定本次搜索范围。
3. 识别和整理频道信息。
4. 检测 IPv4 地址及网络连接。
5. 验证直播媒体是否符合首版支持的技术要求。
6. 每个频道最多保留三条线路。
7. 自动生成 M3U 和 TXT 订阅。
8. 按计划持续更新订阅文件。
9. 正式发布失败时保护上一份成功订阅。
10. 保留运行报告、文件 SHA 和发布记录，保证结果可追溯。

### 1.2 基本原则

1. 以实际播放所需的媒体结构和网络能力为核心，不以地址数量为目标。
2. 基础直播功能优先完成。
3. 所有来源采用统一的数据结构和验证流程。
4. 不允许单一 HTTP 成功状态代表线路可播放。
5. 扩展功能不得影响基础直播。
6. 不依赖收费云服务器、备案域名或长期运行的个人电脑。
7. 所有正式发布必须经过程序测试、文件检查和发布保护。
8. 未经实际验证的功能不得标记为已完成。
9. 严格区分程序技术探测、国内订阅下载、国内媒体可达性和实际设备播放。
10. 不得将 GitHub Runner 内部验证结果直接认定为中国大陆网络可播放。
11. 不得将国内订阅文件下载成功直接认定为媒体线路可播放。
12. 不使用收费云拨测服务；国内网络验证不是首版开发、首发或日常自动更新的前置条件。
13. 暂时没有真实国内验证证据时，必须标记为 `unverified`，不得虚构验证结论，也不得因此阻断项目开发和正常发布。
14. 本项目不绑定任何特定播放器。输出订阅必须保持通用标准格式。
15. 全球频道库只负责频道身份识别和筛选，不得把“频道存在”推断为“线路存在”或“线路可播放”。
16. 用户频道选择范围必须优先于候选名额限制执行；不匹配选择范围的条目不得占用单来源 100 条或总候选 1000 条名额。
17. 全球频道库规模扩大不得改变既有安全、并发、验证、发布和质量保护参数。
18. 本文件为唯一指导方针。任何未在本文件正文中明确的实施前提，必须通过本文件第 5.3、5.4、5.6、6.3 节规定的核验、接入规范或接口契约纳入阶段交付物；不得以“记录在未定义的外部文件”代替规范。
19. 实施前核验失败时，不得通过跳过校验、放宽匹配、隐式转义或降低安全约束绕过；必须按本文件第 5.3.1 节规定的判定矩阵处理。
20. 1.17 稳定参数（来源名额 40、单来源 100、总候选 1000、全局并发 20、单主机并发 5、等待队列 60、单候选 8 秒、队列等待 60 秒、订阅 8MB、HLS 清单 1MB、TS 分片 64KB、重定向 5 跳、每频道 3 条、50% 骤降保护、北京时间 06:17 等）在本版本中零变更。

### 1.3 验收层次与责任边界

1. 第一层：程序技术探测
   - 发生在 GitHub Runner 内部。
   - 验证内容：来源和频道格式正确、频道身份匹配正确、目标为全球可路由 IPv4、网络安全检查通过、TS/HLS 结构符合首版支持范围。
   - 结论含义：程序完成了规定的技术探测。
   - 此层是系统必须负责并通过自动化测试保障的强制门槛。
   - 此层结果不代表中国大陆网络能够访问媒体内容，也不代表播放器能够正常播放。

2. 第二层：国内网络订阅分发
   - 验证对象：正式 GitHub Raw 订阅地址。
   - 验证内容：国内真实网络能否成功拉取订阅文件、格式是否正确、频道身份和线路对应关系是否正常。
   - 结论含义：国内订阅分发链路正常。
   - 此层不代表订阅中的媒体线路在国内网络可达。
   - 首版默认状态为 `unverified`；只有存在真实国内网络测试证据时，才允许记录为 `passed` 或 `failed`。
   - 此层不属于首发或日常自动更新的强制门槛。

3. 第三层：国内媒体网络可达性验证
   - 验证对象：媒体地址及必要的 HLS 媒体分片。
   - 验证内容：这些媒体请求能否在中国大陆真实网络中成功取得。
   - 结论含义：国内网络媒体可达性，不等同于完整播放器播放成功。
   - 首版默认状态为 `unverified`；没有国内真实请求证据时不得填写 `passed`。
   - 此层不属于首发或日常自动更新的强制门槛。

4. 第四层：用户实际设备播放反馈
   - 发生在真实设备和真实播放器。
   - 结论含义：实际设备播放情况。
   - 此层作为外部使用反馈，不将任何具体播放器纳入项目强制验收。
   - 不得因为某个播放器的兼容性问题，擅自改变标准订阅格式或绑定特定播放器。

---

## 2. 项目实施阶段

项目分为六个阶段，必须依次实施和验收。

第一阶段：立项与技术规范冻结  
第二阶段：仓库与基础框架  
第三阶段：核心直播系统  
第四阶段：订阅生成与首发  
第五阶段：自动化与稳定性  
第六阶段：扩展能力

不得跳过阶段验收。后续阶段发现前序阶段缺陷时，先修复并重新验收，不得以临时绕过代替修复。

**绝对前置序列（不可跳过）**：
在进入任何代码实现（特别是 `catalog.py`）前，必须依次完成：
1. **第一阶段完成**：规范冻结。
2. **第二阶段第 0 步核验**：完成第 5.3 节全球频道库启动前核验，并确定第 5.3.1 节错误处理矩阵的落地方式。
3. **第三阶段第 0 步核验**：完成第 5.4 节 tvg_id 对齐核验准备，以及第 5.6 节上游源实测。
4. **接口冻结**：完成第 6.3 节模块接口契约冻结。
5. **Schema 更新**：完成第 15.1 节规定的 Schema 更新。
6. **实现**：开始编写 `catalog.py`。

---

## 3. 技术环境与依赖

### 3.1 运行环境

- 运行平台：GitHub-hosted Runner。
- 操作系统：Ubuntu 24.04。
- 开发语言：Python。
- 首选版本：Python 3.14 最新补丁版。
- Python 精确版本写入 `.python-version`。
- GitHub Actions 安装的 Python 版本必须与 `.python-version` 完全一致。
- 依赖版本必须通过 `uv.lock` 锁定。

Python 版本与依赖验证规则：
1. Python 库验证：验证 `aiohttp`、`pytest` 能够成功安装和导入，并能运行基础异步单元测试。
2. 命令行工具验证：验证 Ruff 和 uv 能够成功安装，且命令行执行正常。
3. 全部通过：保留 Python 3.14。
4. 如果安装或运行失败：记录完整报错并排查。确认短期无法解决后，才允许评估 Python 3.13 最新补丁版。回退必须附带排查证据并记录在 `PROGRESS.md`。
5. 必须在 GitHub-hosted Ubuntu 环境实际验证：
   - Python 版本与 `.python-version` 一致；
   - `aiohttp`、`pytest` 安装和导入成功；
   - asyncio 基础功能正常；
   - Ruff、uv 正常；
   - 依赖锁文件存在且有效；
   - `uv lock --check` 通过；
   - `uv sync --locked` 通过；
   - Ruff 检查通过；
   - pytest 全部通过。
6. 不得仅凭本地电脑运行成功就认定 GitHub Runner 环境验证通过。

### 3.2 核心技术

- Python / asyncio / aiohttp
- dataclasses / JSON Schema 2020-12
- pytest / Ruff / uv / GitHub Actions

### 3.3 依赖管理

使用：
- `pyproject.toml`
- `uv.lock`
- `.python-version`

依赖版本必须锁定。第三方 GitHub Actions 必须固定到完整 commit SHA，不得仅使用可变版本标签。

### 3.4 数据校验边界

- JSON Schema 用于配置文件和持久化 JSON 校验。
- 运行时内存数据使用 dataclasses。
- Schema 版本统一采用 JSON Schema Draft 2020-12。
- Schema 校验失败不得静默忽略。
- 全球频道身份库的唯一 Schema 为 `data/global_channels/channels.schema.json`。
- 默认地区范围和频道筛选配置的唯一 Schema 为 `data/global_channels/channel_filter.schema.json`。
- `data/global_channels/validation_summary.json` 用于记录全球频道库数据完整性和统计校验结果；正式实施时必须重新执行校验。
- **废弃声明**：`schemas/channels.schema.json` 正式废弃，不得用于校验任何频道数据。开发者在第二阶段必须删除或清空该文件，防止误用。
- 不得在运行时用未经 Schema 校验的全球频道数据覆盖本地已提交的身份库。

---

## 4. 项目目录结构

```text
IPTV-Auto-Next/
├── MASTER_PLAN.md
├── PROGRESS.md
├── README.md
├── manual.txt
├── .github/
│   └── workflows/
├── .python-version
├── pyproject.toml
├── uv.lock
├── data/
│   └── global_channels/
│       ├── channels.json
│       ├── channels.schema.json
│       ├── channel_filter.json
│       ├── channel_filter.schema.json
│       └── validation_summary.json
├── schemas/
│   ├── sources.schema.json
│   ├── run_report.schema.json
│   ├── publish_manifest.schema.json
│   ├── candidate_manifest.schema.json
│   └── subscription_info.schema.json
├── config/
│   ├── sources.json
│   ├── channels.txt
│   └── channels.json (仅作兼容占位，不读取)
├── src/
│   └── iptv_auto_next/
│       ├── main.py
│       ├── config.py
│       ├── models.py
│       ├── catalog.py
│       ├── source.py
│       ├── network.py
│       ├── parser.py
│       ├── validator.py
│       ├── channel.py
│       ├── selector.py
│       ├── playlist.py
│       ├── publisher.py
│       └── reporter.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/
└── output/
    ├── candidate/
    │   ├── iptv.m3u
    │   ├── iptv.txt
    │   └── candidate_manifest.json
    ├── iptv.m3u
    ├── iptv.txt
    ├── subscription_info.json
    └── publish_manifest.json
```

目录职责说明：
- `data/global_channels/`：存放唯一频道身份库及筛选配置。`channels.json` 不得被重复维护。
- `config/`：保留来源配置和用户频道选择入口。`config/channels.txt` 是用户频道选择入口。`config/channels.json` 运行时不读取、不校验；若文件存在，仅作兼容占位，删除不影响运行。
- `output/candidate/`：存放待人工审阅的 Candidate 文件。不是正式订阅，不得覆盖正式文件。用途是让用户审阅内容并确认准确 SHA 后，再手动触发正式发布；不要求进行国内网络实测。
- `output/` 根目录：仅存放正式发布的成品和清单。
- `tests/unit/`：不联网的单元测试。
- `tests/integration/`：使用本地受控 Fixture 的集成测试。
- `tests/acceptance/`：程序技术探测和发布流程验收测试。

不得为了拆分模块而增加没有必要的文件。`catalog.py` 为全球频道库读取、Schema 校验、统计校验和频道筛选的必要模块，不属于无必要拆分。

---

## 5. 配置管理与核验规则

### 5.1 来源配置、来源入口和候选截断规则

#### 5.1.1 sources.json 结构

`config/sources.json` 必须采用以下固定结构（示例说明，实际使用需替换域名或使用经核对的公开来源）：

```json
{
  "manual_single": [
    {
      "id": "manual-single-0001",
      "tvg_id": "CCTV5.cn",
      "url": "https://example.com/live.ts"
    }
  ],
  "carriers": [
    {
      "id": "carrier-source-0001",
      "url": "https://example.com/carrier.m3u",
      "enabled": false
    }
  ],
  "discovery": [
    {
      "id": "public-index-iptv-org-cn",
      "url": "https://iptv-org.github.io/iptv/countries/cn.m3u",
      "enabled": true
    }
  ]
}
```

以上是字段结构示例。`example.com` 只用于说明格式，不得作为实际来源启用。初始公开目录来源可使用 iptv-org 中国频道公开播放列表、iptv-org 全球 Feed / Streams 公开数据或经核对的公开授权目录；其内容仍须经过本项目自己的解析、频道身份匹配、频道选择过滤、IPv4 安全检查和媒体验证。

全球频道库升级后，初始来源策略：
1. `data/global_channels/channels.json` 只提供频道身份，不直接提供候选线路。
2. 频道对应线路必须来自 `sources.json` 登记的 `manual_single`、`manual.txt`、`carriers` 或 `discovery` 来源。
3. 允许 `discovery` 登记 iptv-org 的 Feed / Streams 公开数据源，但必须遵守第 5.6 节规定的接入规范。
4. 全球频道库规模不得成为绕过来源名额、单来源候选上限、总候选上限或安全验证的理由。
5. 不进行无边界网页爬虫，不使用搜索引擎批量抓取，不依赖 GitHub 搜索 API 动态搜索仓库。

配置结构约束：
- `manual_single`、`carriers`、`discovery` 三个数组必须存在；允许为空数组。
- 每个 `manual_single` 对象必须包含唯一 `id`、有效 `tvg_id` 和 URL。
- 每个 `carriers`、`discovery` 对象必须包含唯一 `id`、URL 和布尔值 `enabled`。
- 三类来源的 `id` 在整个 `sources.json` 中必须全局唯一。
- URL 必须是绝对 HTTP/HTTPS URL，不得包含 userinfo，不得含 CR、LF 或控制字符。
- `enabled=false` 的来源不下载、不占来源名额。
- 三个数组即使没有内容也必须保留，不能用 `null` 或省略字段代替空数组。
- `sources.schema.json` 必须严格校验上述结构，禁止未知字段静默进入运行配置。

`data/global_channels/channels.json` 的字段以 `data/global_channels/channels.schema.json` 为准。用于本项目匹配和筛选的必备信息至少包括：非空 `tvg_id`、非空 `canonical_name`、`aliases` 数组、国家/地区字段（如 `country`）。全球频道库 Schema 校验字段类型和基本格式；跨频道唯一性、alias 冲突、规范化歧义和默认地区字段有效性由第 5.3 节启动前核验进一步校验。

来源定义：
- `manual_single`：人工指定的单条线路。必须填写 `tvg_id` 和完整 URL。
- `manual.txt`：人工订阅来源。每一行是一个独立订阅来源。
- `carriers`：运营商或其他明确来源的订阅目录。
- `discovery`：预先登记的公开或授权目录源。每次运行自动获取其最新列表，再提取候选线路。

首版自动发现边界：
1. 自动发现采用 `sources.json` 中登记的公开或授权目录源。
2. 每次运行自动下载这些目录并解析其中的线路或上游 Feed / Streams 数据。
3. 首版不进行无边界网页爬虫，不使用搜索引擎批量抓取，不依赖 GitHub 搜索 API 动态搜索仓库。
4. 新增目录源必须先核对其公开来源、授权或公开发布依据、格式和可获取性，再写入 `sources.json`。
5. 未实际获取和解析成功的来源不得标记为已接入。
6. 不得为增加数量而加入来源不明、未经授权或仅有名称没有真实获取地址的来源。
7. 全球频道库不得自动生成线路候选；线路候选必须来自上述来源。

#### 5.1.2 来源优先级和顺序

来源优先级严格如下：
1. 人工单条：按 `sources.json` 中数组顺序。
2. 人工订阅：按 `manual.txt` 有效 URL 的行顺序。
3. 运营商来源：按 `sources.json` 中 `carriers` 数组顺序。
4. 自动发现来源：按 `sources.json` 中 `discovery` 数组顺序。

同一类别内部不得自行按名称、URL 或网络速度重新排序。

#### 5.1.3 来源名额和候选上限

首版限制：
- 总来源名额：40。
- 单个订阅来源最多接收：100 条有效候选。
- 总候选池：1000 条。
- 人工单条不占用 40 个来源名额，也不受单来源 100 条限制，但受总候选 1000 条限制。

名额计算规则：
1. 人工单条优先解析并进入候选池，不占 40 个来源名额。
2. `manual.txt` 每个有效 URL 视为一个独立来源。
3. 人工订阅、运营商来源和自动发现来源共用 40 个来源名额。
4. 一个来源只有在至少产生一条通过频道身份识别、频道选择过滤、名单过滤和 URL 去重的有效候选后，才占用一个来源名额。
5. 来源下载失败、格式不支持、解析失败、没有匹配频道、没有匹配用户选择范围或所有条目均被去重的来源，不占来源名额。
6. 来源名额按 5.1.2 规定的优先级顺序分配；累计达到 40 个有效来源后，停止接收后续订阅来源。
7. 单个来源最多接收前 100 条有效且未重复的候选。达到 100 条后，该来源后续条目不再进入候选池。
8. 候选池达到 1000 条后，立即停止接收后续候选和来源。
9. 所有名额和截断行为必须写入 RunReport，包括来源总数、成功来源数、来源失败数、单来源截断数、候选池截断数、频道选择过滤丢弃数和默认地区过滤丢弃数。

**推进方式**：来源处理必须按 5.1.2 优先级顺序串行推进，或采用可等效证明“在第 40 个有效来源处准确截断、在第 1000 条候选处准确停止”的分阶段实现。不得采用“全量并行下载全部来源后再统一计算名额”的实现，因为该实现无法在名额边界准确停止后续来源。

#### 5.1.4 解析、过滤和去重顺序

统一执行以下顺序：
1. 按来源优先级获取来源内容。
2. 解析 M3U、TXT 或经核对的 iptv-org Feed / Streams 数据条目。
3. 校验条目 URL 的基本格式和协议。
4. 识别频道身份。
5. 执行频道选择过滤：
   - `config/channels.txt` 有有效内容时，只保留用户填写的频道目标；
   - `config/channels.txt` 为空或只有注释时，只保留默认地区 CN、HK、MO、TW 的频道。
6. 生成规范化 URL。
7. 对规范化 URL 做全局去重，保留优先级最高、原始顺序最靠前的第一条。
8. 应用单来源 100 条限制。
9. 应用总候选 1000 条限制。
10. 将唯一候选提交验证调度器。

第 5 步“频道选择过滤”在人工选择模式下与“人工名单过滤”是同一件事，必须合并实现为一个过滤函数，不得拆成两步重复放宽范围。

频道选择过滤必须在单来源 100 条和总候选 1000 条之前执行。未匹配用户频道选择范围或默认地区范围的条目不得占用候选名额。

同一 URL 在不同来源重复出现时，只验证一次，并保留优先级最高的第一条来源身份。若同一 URL 被不同频道身份声明，按优先级保留第一条并记录 `cross_channel_url_conflict`，后续冲突条目丢弃，不得把同一 URL 同时输出为多个频道。

最终线路选择阶段不得再次改变 URL 去重归属；只能执行唯一性断言，发现重复属于程序错误。

#### 5.1.5 人工订阅入口 manual.txt

- 仓库根目录使用 `manual.txt`。
- UTF-8 纯文本，每行一个完整 HTTP/HTTPS 订阅地址。
- 空行忽略，首尾空白去除。
- 不修改 URL 的路径和查询参数内容。
- 每行作为一个独立人工订阅来源。
- 下载内容按实际内容自动识别 M3U、TXT 或经核对的 Feed / Streams 数据格式，不依赖 URL 后缀。
- 下载内容必须先经过网络安全检查、超时和大小限制，再解析。
- M3U：以 `#EXTM3U` 或有效 `#EXTINF` 记录识别；每个 `#EXTINF` 对应其后第一个非空、非注释 URL 行；缺少 URL 的条目记为解析失败。
- TXT：按 RFC 4180 CSV 规则逐行解析，每条有效记录必须恰好包含两个字段：频道名称、URL；字段数量不为 2 的记录记为解析失败。
- 来源文件允许 UTF-8 BOM 和 CRLF 输入；解析时统一处理，但正式输出仍必须无 BOM、LF。
- 如果内容既不能识别为 M3U，也不能按上述规则解析为 TXT，也不能识别为已登记支持的上游 Feed / Streams 数据格式，则判定格式不支持。
- 不得把完整 M3U/TXT 订阅文件当作单条媒体线路。
- 单个来源失败或无法解析时，记录原因并跳过，不得中断其他来源。

#### 5.1.6 来源下载边界

来源订阅下载与候选媒体验证使用不同的超时预算：
- 单个来源下载总超时：20 秒，包含 DNS、连接、重定向和内容读取。
- 单个来源下载内容上限：解压后 8MB。
- 重定向最多 5 跳。
- HTTP 状态必须为 200；其他状态记录失败原因并跳过。
- 必须流式读取并累计解压后字节数，不得只依赖 `Content-Length`。
- 超过 8MB 立即中止。
- 不进行额外重试。
- 所有来源下载必须通过 `network.py`。

#### 5.1.7 全球频道身份库与统计口径

`data/global_channels/channels.json` 是项目唯一全球频道身份库，不再维护另一套重复的频道主字典。

1. 全球频道库只负责频道身份识别，不代表其中包含可直接播放的线路。
2. 全球频道库不在每次运行时动态改变；运行时只读取本地已提交文件。
3. 全球频道库必须通过 `data/global_channels/channels.schema.json` 校验。
4. 必须执行数据完整性和统计一致性验证。统计一致性校验口径为：`channels.json` 实际统计结果 == `validation_summary.json` 中记录的统计结果。不得以历史数字作为运行时硬编码比对目标。
5. 当前数据基准统计（仅作说明）：
   - 频道数量：31,805；唯一 tvg_id：31,805；国家和地区：231；
   - CN：749；HK：147；MO：15；TW：154。
6. 初始数据来源可为 iptv-org/database 等已提交的全球频道数据；数据写入本项目后，运行时只读取本地文件。
7. 后续新增或修改频道必须通过本项目配置变更、Schema 检查和统计校验，不得在运行时自动覆盖全球频道身份库。
8. 该字典定义项目当前支持识别的频道范围。未纳入全球频道库的频道不会被输出，不得通过模糊匹配擅自加入。
9. `data/global_channels/channel_filter.json` 定义默认地区范围，首版必须为 CN、HK、MO、TW，并通过 `channel_filter.schema.json` 校验。
10. `config/channels.txt` 有有效内容时，人工选择模式优先，不受默认地区限制；可以混合填写不同国家和地区的频道。
11. `config/channels.txt` 为空或只有注释时，进入默认地区模式，只搜索 `channel_filter.json` 定义的 CN、HK、MO、TW 频道。
12. `config/channels.json` 不再作为频道主字典；运行时不读取、不校验；若保留，仅作兼容占位，删除不影响运行。

**统计字段计算规则（必须严格执行）**：
1. `channels`: `channels.json` 中频道数组的元素总数。
2. `unique_tvg_ids`: 提取所有非空 `tvg_id`，去重后的唯一值数量。
3. `countries`: 提取所有非空国家/地区字段（如 `country`），去重后的唯一值数量。
4. `country_counts`: 按国家/地区字段分组计数的字典，例如 `{"CN": 749, "HK": 147, ...}`。
5. `category_values`: 提取所有非空分类字段（如 `categories` 展开），去重后的唯一值数量。
6. `empty_categories`: 分类字段为空或缺失的频道数量。
7. **一致性校验**：`channels.json` 的实际计算结果必须与 `validation_summary.json` 中记录的上述字段完全一致，否则启动报错退出 1。

### 5.2 频道配置与精确匹配原则

采用确定性映射，严禁使用模糊匹配或子串包含匹配。CCTV-5 和 CCTV-5+ 必须保持完全独立。

身份与匹配逻辑严格按以下优先级执行：
1. 以 `data/global_channels/channels.json` 作为 Canonical 标准频道字典，包含 `tvg_id`、`canonical_name`、`aliases`，以及国家/地区字段。
2. 来源条目存在 `tvg-id` 属性时，直接与全球频道库的 `tvg_id` 完全相等匹配。匹配不到即判定为无效条目，严禁退回使用名称进行 alias 匹配。
3. 只有来源条目完全没有 `tvg-id` 属性时，才提取来源显示名称，与 `canonical_name` 和 `aliases` 完全相等匹配。
4. 名称规范化规则：来源名称、`canonical_name` 和 `aliases` 执行相同的 Unicode NFKC、去首尾空白、统一小写处理。
5. 严禁删除内部字符、连字符、加号、斜杠或其他有区分意义的字符来强行合并匹配。
6. `tvg-id` 使用原值完全匹配，不进行名称规范化。
7. `tvg-id` 属性存在但为空或不匹配时，均视为存在但无效，不得回退名称匹配。

`config/channels.txt`：
- 每行一个频道搜索目标。空行和以 `#` 开头的注释行忽略。
- 每行必须对应全球库中一个 `tvg_id`、`canonical_name` 或 alias。
- 优先按精确 `tvg_id` 匹配；否则按规范化名称完全相等匹配。
- 匹配不到任何标准频道，启动时报错退出 1。
- 有有效内容时进入人工选择模式：不限制国家和地区，可以混合填写。
- 文件为空或只有注释时进入默认地区模式：只搜索 CN、HK、MO、TW。

频道选择与候选限制关系：
1. 人工选择模式下，只有被用户填写并精确匹配到的频道进入后续候选处理。
2. 默认地区模式下，只有国家/地区属于 CN、HK、MO、TW 的频道进入后续候选处理。
3. 频道选择过滤必须在单来源 100 条和总候选 1000 条之前执行。
4. 不匹配频道选择范围的条目不得占用来源名额、单来源候选名额或总候选名额。
5. 默认地区模式下，`manual_single` 中非四地区条目同样会被丢弃。用户需搜索非四地区频道必须写入 `channels.txt`。

频道配置完整性：
1. `tvg_id` 必须唯一且非空。2. `alias` 不得产生重复或冲突映射。3. 不同标准频道不得通过规范化规则映射为同一个身份。
4. 查找命名空间不得产生跨频道歧义。5. 冲突时报错不得静默选择。6. 默认地区字段缺失时报错。7. 必须有对应单元测试。

### 5.3 全球频道库启动前核验（第二阶段第 0 步）

在实现 `catalog.py` 前，必须执行以下核验，结果写入 `PROGRESS.md`。
1. **alias 全局重复**：提取全库所有名称及别名，计算规范化后跨频道的碰撞次数。
2. **M3U 字符约束**：统计包含双引号、CR、LF 的条目数。
3. **默认地区字段**：确认 `country` 字段在 CN/HK/MO/TW 均有值。
4. **统计一致性**：按 5.1.7 口径计算，与 `validation_summary.json` 比对。

#### 5.3.1 错误处理矩阵（强制裁定）
为了避免各模块处理方式不一，严格按以下矩阵执行：

| 错误场景 | 判定范围 | 处理动作 | 退出码 | 后续影响 |
| :--- | :--- | :--- | :--- | :--- |
| 统计口径不一致 | 全局 | 立即中止启动 | 1 | 禁止进入任何流程 |
| `tvg_id` 重复 | 全局 | 立即中止启动 | 1 | 禁止进入任何流程 |
| 名称含双引号/CR/LF | 单条目 | 拒绝该条目加载 | 1 | 若为全局数据错误则整库失败；若清理后则为对应条目报错 |
| 名称规范化后跨频道碰撞 | 单条目 | 标记歧义 | - | 匹配时若命中歧义则丢弃该候选并记录 `channel_selection_ambiguous` |
| 来源中 `tvg-id` 存在但不匹配 | 单条目 | 丢弃该候选 | - | 记录 `channel_identity_mismatch`，不影响库和其他来源 |
| 来源无 `tvg-id` 且名称歧义 | 单条目 | 丢弃该候选 | - | 记录 `channel_selection_ambiguous`，不影响库和其他来源 |

*说明：凡是导致“库自身不完整或不可信”的问题直接阻断启动；凡是“来源匹配不到”的问题，仅丢弃单条，不得影响全局运行。*

### 5.4 tvg_id 与上游 channel id 对齐规则（第三阶段前置）
1. 必须明确 `tvg_id` 与 Feed/Streams 中 channel 字段的对齐关系。
2. 若直接对齐，需记录证据；若存在改写，必须提供映射函数并覆盖单测。
3. 无法对齐的条目按无效处理。

### 5.5 频道名称字符约束处理
1. 包含双引号、CR、LF 的 `canonical_name` 或 `aliases` 必须被 catalog 校验拒绝并报 `ConfigError`。
2. 不得在 M3U/TXT 生成阶段隐式转义，也不得静默跳过而不报错。

### 5.6 上游 Feed / Streams 数据源接入实测
在接入任何 `discovery` 源前，必须**实际获取**并测量：数据实际大小（解压后，超8MB必须拆分）、字段结构、是否支持分片、授权依据。实测记录必须写入 `PROGRESS.md`，未实测不得在 `sources.json` 中标记启用。

---

## 6. 核心数据模型与接口契约

### 6.1 统一数据对象
系统使用以下运行时 dataclass：Source, Candidate, VerifiedLine, Channel, ValidationResult, RunReport, PublishManifest。
- Source：来源 ID、类型、优先级、原始顺序、URL。
- Candidate：候选 ID、来源 ID、频道 `tvg_id`、原始/规范化 URL、来源内顺序。
- Channel：`tvg_id`、`canonical_name`、`aliases`、国家/地区字段。
- ValidationResult：候选 ID、验证等级、两次结果、耗时、错误、时间。
- VerifiedLine：候选信息、验证等级、时间、结果。
- RunReport：单次运行完整过程。
- PublishManifest：当前正式发布文件、SHA、统计、发布来源和状态。
*关键原则：来源身份、线路身份（URL）、频道身份（tvg_id）必须分开管理。*

### 6.2 验证等级与稳定性判定
- `stable`：两次短验证均通过。
- `unstable`：一次通过、一次失败。
- `single_pass`：至少一次通过，另一次因预算耗尽未完成。
- `pending`：内部调度状态，不得输出。
- `invalid`：两次均未通过。

**短验证规则**：TS 流必须找到连续 5 个 `0x47` 同步字节，间隔严格为 188 字节。
**两次验证执行规则**：
1. 两次验证串行执行，不增加固定等待。
2. 两次完整验证共用一个 8 秒总预算，不是每次 8 秒。
3. 第一次结束（通过或失败）后，只要 8 秒总预算有剩余，就执行第二次。
4. 如果预算耗尽，立即停止。不增加第三次或额外重试。

**判定表**：
| 第一次 | 第二次 | 最终状态 | 是否有效 |
|---|---|---|---|
| 通过 | 通过 | stable | 是 |
| 通过 | 失败 | unstable | 是 |
| 失败 | 通过 | unstable | 是 |
| 通过 | 未完成（耗尽） | single_pass | 是 |
| 失败 | 未完成（耗尽） | invalid | 否 |
| 失败 | 失败 | invalid | 否 |
| 未完成 | 未执行 | invalid | 否 |

只有至少一次完整通过，才可进入有效线路集合。`queue_wait_timeout` 不记为 unstable，不进入有效集合。
*结论边界*：连续 `0x47` 仅证明结构特征，不代表国内网络可播放。所有验证等级均属第一层。

### 6.3 模块接口契约（强制冻结）
在进入第二阶段代码实现前，必须冻结以下契约：
**catalog.py 职责**：读取库与过滤配置，执行 Schema 与统计校验，构建精确/规范名称索引，解析 channels.txt 确定模式，提供 `is_in_scope`。
**channel.py 职责**：单条身份匹配（tvg-id 精确 / 名称规范化），失败绝不回退名称，名称歧义报错。
**契约签名参考**：
- `load_catalog(paths...) -> Catalog`
- `Catalog.validate() -> None`
- `Catalog.resolve_selection(txt_path) -> SelectionMode`
- `Catalog.is_in_scope(tvg_id) -> bool`
- `Catalog.ordered_channels() -> list[Channel]`
任何接口修改必须在 `PROGRESS.md` 留痕。

---

## 7. 网络访问与媒体验证

### 7.1 网络统一出口
所有网络访问必须通过 `network.py`，包括来源下载、Feed 接入、直接 TS、HLS 分片、重定向和发布后检查。不得绕过。

### 7.2 IPv4 验证与安全

#### 7.2.1 协议和目标地址
- 只允许 HTTP/HTTPS，拒绝 file/ftp/rtsp 等。
- 只允许全球可路由公网 IPv4，直接拒绝 IPv6 URL。
- 域名只查 A 记录。使用 `ipaddress` 的 `is_global` 检查。拒绝私网、环回、链路本地等。

#### 7.2.2 DNS Rebinding 防范
1. 多个 IP 逐个检查，实际连接只能使用通过检查的 IP。
2. 必须使用自定义 resolver 将校验 IP 提供给连接器。禁止二次解析。
3. 关闭 DNS 缓存。TCP 建立后必须检查 socket peer IP 是否等于已校验 IP。
4. HTTP 保留原域名 Host。HTTPS 使用原域名 SNI 和证书校验。
5. 禁止代理绕过。显式设置 `trust_env=False`，不读取代理环境变量。

#### 7.2.3 TLS 和请求客户端
- 必须启用系统可信 CA 证书校验。禁止 `ssl=False`。
- 不跨候选共享 Cookie。禁止自动重定向。流式读取计数。
- 候选验证不得复用旧连接（或等效证明），每次必须经过 resolver 和 peer IP 检查。

#### 7.2.4 重定向与子请求
- `allow_redirects=False`。最多跟随 5 跳，初始请求不计。
- 相对地址按标准解析。每次重查协议、主机、DNS 和 IPv4 安全。未查不得连接。
- HTTPS 降级到 HTTP 直接拒绝。HLS 子清单和分片必须重查。

#### 7.2.5 安全测试要求
必须测试 peer IP 校验、无二次解析、Host 保留、SNI 正确、拒绝错证书、代理无法绕过、每跳重查。不能只测 DNS 返回。

### 7.3 请求限制、并发与读取策略

首版限制：
- 总候选 1000，单来源 100，有效来源 40。
- 全局媒体验证并发 20，同一主机并发 5。
- 等待队列最多 60 个。单候选验证总预算 8 秒，队列等待上限 60 秒。

#### 7.3.1 候选调度规则
1. 调度器最多允许 20 条正在验证，另有最多 60 条等待。
2. 超出 60 条等待容量的候选保留在待调度列表中，不丢弃。
3. 只有进入 60 条等待队列后，才开始计算 60 秒等待时间。超时记录 `queue_wait_timeout` 并移除。
4. 等待队列中的候选超过 60 秒未获资源，记录并移除。
5. 全局 20 和主机 5 必须由中央调度器统一管理。
6. 不允许先占执行工作位再阻塞等待主机名额。
7. 按等待顺序选最早且当前主机有可用名额的候选；主机满可跳选其他主机，不让全局位置闲置。
8. 被跳过等待主机名额的候选继续计算队列等待时间。
9. 取得全局和主机资源、即将开始网络验证时，才启动 8 秒总预算。
10. `queue_wait_timeout` 不得占用并发名额。

#### 7.3.2 8 秒总预算
单候选 8 秒包含 DNS、TCP、TLS、每次重定向、HLS 主/子清单及分片、两次短验证。必须使用单个绝对截止时间控制整个验证过程。每个 HTTP 请求只能使用剩余时间。不能依赖单次请求超时。

#### 7.3.3 读取限制
1. 订阅文件解压后最多 8MB。HLS `.m3u8` 最多 1MB。TS 媒体流最多读取 64KB。
2. 必须流式分块读取。累计解压后真实字节数。
3. HLS 超过 1MB 立即失败，不允许截断。TS 读取 64KB 未找到同步结构立即中止。找到连续 5 个 `0x47` 可停止。

#### 7.3.4 压力测试
在 GitHub-hosted Ubuntu 上执行 1000 候选受控压测（本地 Fixture）。覆盖集中同主机、分散多主机、混合、慢响应、队列满、单主机并发满、全局并发满、排队超时等。必须记录并发峰值、等待峰值、完成数量、资源峰值等。不得理论估算代替。

### 7.4 媒体验证完整流程
首版只支持未加密 MPEG-TS。所有请求均计入单候选 8 秒总预算。

#### 7.4.1 直接媒体地址
不依赖后缀。最终 HTTP 状态必须为 200。不发送 Range（206 不接受）。必须通过 TS 同步结构才算完整通过。不支持内容均失败。

#### 7.4.2 HLS 识别
按内容识别。包含 `#EXTINF` 和分片 URI 为媒体播放列表。包含 `#EXT-X-STREAM-INF` 为主清单。不支持格式明确记录原因。

#### 7.4.3 Variant 处理
1. 按原始顺序，最多尝试前 2 个 Variant。
2. 先试第一个，完整通过即停止。失败且预算允许再试第二个。第二个通过也算通过。
3. 不按带宽重排。子清单不递归超过一层。

#### 7.4.4 分片请求
每媒体列表最多请求 1 个分片。必须走 `network.py`，响应为 200。分片读取最多 64KB。必须通过 TS 同步结构。不支持则 Variant 失败。

#### 7.4.5 HLS 加密和格式边界
1. `#EXT-X-KEY`：仅允许 `METHOD=NONE`。其他拒绝。
2. `#EXT-X-SESSION-KEY`：一律拒绝。
3. `#EXT-X-MAP`：拒绝并记录 `fMP4_not_supported`。
4. `#EXT-X-BYTERANGE`：拒绝并记录 `byterange_not_supported`。
5. 带 URI 的外部音频/字幕 Rendition：判定不支持。
6. 其他不明确格式不得判定通过。

---

## 8. 频道整理与三线路选择

### 8.1 优先级
人工单条 > 人工订阅 > 运营商 > 自动发现。不得覆盖验证等级排序。

### 8.2 URL 去重规则
1. scheme 小写；2. host 小写及 IDNA；3. 去默认端口（80/443）；4. 去 fragment；5. Query 参数完整保留，不删不改不重排；6. Path 原样保留；7. 不做 tracking 删除；8. userinfo 拒绝；9. 保留完整 Query 值输出。
全局去重在验证前执行，保留优先级最高、顺序最靠前的第一条。

### 8.3 排序和截断
只对通过至少一次短验证的线路排序：
1. 验证等级：`stable` > `single_pass` > `unstable`。
2. 来源优先级。
3. 验证时间（新到旧）。
4. 来源内原始顺序。
每个频道最多保留前三条。`invalid`、`pending` 和超时不得进入。每次运行重新生成，不依赖历史。

### 8.4 频道输出顺序
按 `global_channels/channels.json` 原始顺序，先按选择范围过滤。同频道多条连续输出，不因验证完成时间改变频道顺序。

---

## 9. 订阅格式

### 9.1 M3U 标准与多线路输出
首行 `#EXTM3U`。连续输出 `#EXTINF:-1 tvg-id="..." tvg-name="...",显示名` 和 URL。逗号后无空格。多线路连续。无私有标签。属性值不得含双引号/CR/LF。URL 不得含控制字符。UTF-8 无 BOM，LF 换行。

### 9.2 TXT 格式
单行格式：`频道名称,线路URL`。按 RFC 4180 字段转义（含逗号/引号需引用，内部引号双写）。LF 换行，末尾保留。

### 9.3 双格式一致性
生成前必须交叉解析核对：频道集合、线路数量、URL、顺序完全一致。不一致阻断发布。

### 9.4 订阅信息
`subscription_info.json` 记录元数据。包含 `layer1/2/3_status` 及证据。无国内证据时保持 `unverified`，`evidence` 为 `null`。通过/失败必须有对应证据且 SHA 匹配。不得伪造国内验证结果。

---

## 10. 订阅发布与验收

### 10.1 正式发布路径
固定四文件：`output/iptv.m3u`, `iptv.txt`, `subscription_info.json`, `publish_manifest.json`。唯一渠道 GitHub Raw。

### 10.2 镜像边界
Gitee 等不属于首版，第六阶段评估。

### 10.3 国内验证与首发规则
1. 首版国内实测不是强制门槛。
2. 首发及关键变更必须经过 Candidate、审阅、SHA 校验和人工触发。
3. 默认状态均为 `unverified`。
4. Runner 内部 Raw 检查仅记录为 `program_connectivity`。
5. 若未来有国内证据，单改 JSON，M3U/TXT 变则证据失效。不得由第二层推断第三层。

### 10.4 国内验收证据标准（仅在实际执行时适用）
第二层需真实网络 200，查格式，抽查 5 个频道。第三层需真实请求媒体/分片。均需记录 SHA 和时间。不得互相代替。

### 10.5 Candidate 发布（防测 A 发 B）

#### 10.5.1 文件与 Manifest
三文件同 Commit：`output/candidate/iptv.m3u`, `iptv.txt`, `candidate_manifest.json`。
Manifest 记录：Schema 版本、时间、`source_commit_sha`、M3U/TXT SHA、第一层状态、统计数、四文件 SHA 基准。首发前四文件全无则基准为 `null`。不记录自身 SHA。

#### 10.5.2 dry-run 生成
拉最新 main，查四文件存在性，记录 SHA 基准。采集验证，生成 Candidate，重算 SHA，只提交 Candidate 三文件。获取准确 Commit SHA。不修改正式文件。

#### 10.5.3 candidate-publish 提取
输入三个 SHA 参数。必须 `fetch-depth: 0`。查目标 Commit 祖先关系，查父提交等于 `source_commit_sha`，查差异仅限三文件。使用 `git show` 提取文件。执行 Schema 校验和 SHA 重算。核对四文件基准和核心代码是否改变（README 等非核心变更不失效）。任一失败阻断。

#### 10.5.4 正式文件生成与失效
正式文件必须与 Candidate 字节级一致。四文件同提交。Candidate 失效条件：基准不一致、SHA 不一致、非 main 祖先、核心代码变更、Schema 失败等。

### 10.6 关键变更与日常自动更新边界
关键变更包括：`src/`, `tests/`, `workflows/`, `config/`, `data/global_channels/`, `schemas/`, `manual.txt`, 依赖文件。
首发或关键变更后必须走 dry-run 和 candidate-publish。日常更新比对 `source_commit_sha`，关键路径变则阻断。

### 10.7 空订阅与质量骤降保护

#### 10.7.1 非空门槛
0 频道禁止发布。名单模式或默认模式 0 频道退 3。不受 `--force` 影响。

#### 10.7.2 质量骤降
对比上次 Manifest：频道数或线路数低于 50% 阻断。恰好 50% 放行。
豁免：`channels.txt`、`channels.json`、`filter.json` 变化时跳过骤降。`--force` 仅人工可用，只绕此限，不可绕空订阅、安全、SHA 和 `publish_blocked`。必须记录绕过情况。

### 10.8 发布提交、失败恢复和 Raw 检查

#### 10.8.1 提交边界
四文件同提交，Candidate 三文件同提交。严禁 force push。基于最新 main。推送前再读远端，变化则中止重跑。差异严格限定。

#### 10.8.2 推送核对
明确拒绝退 3。状态不明查远端，确认成功算成功。无法确认退 4。

#### 10.8.3 Runner 内部 Raw 检查
最多 3 次（间隔 5 秒）。记录 `program_connectivity`。
- `passed`：正常记录。
- `unavailable` / `test_error`：记录警告，不回滚，不阻断下次。
- `content_mismatch`：立即停止后续发布，写入 `publish_blocked=true`。

**阻断双重持久化**：
1. 检查/创建专用未关闭 Issue (`[IPTV-Auto-Next] PUBLISH_BLOCKED`)，写入 run_id、SHA、原因。确认成功后写入 Manifest。
2. 若 Issue 建立失败，退 4 并报警要求人工暂停工作流。
3. Manifest 写入冲突重试最多 3 次（共 4 次推送）。每轮重试前查远端，若已存在相同阻断则视为成功。
4. 若 Issue 建立成功但 Manifest 写入最终失败，仍依靠 Issue 门禁阻断。

**启动门禁与 Raw 兜底**：
1. 发布前获取远端 Manifest 和专用 Issue 状态。若存在阻断则 fail-closed 退 4。
2. 获取线上 Raw 四文件，计算 SHA 与 Manifest 比对。不一致退 3。
3. 人工解除唯一流程：人工修问题，核实 Raw 与 Manifest 一致，修改 Manifest 清标记并推送到 main，记录 PROGRESS，最后由人工关闭 Issue。自动任务严禁自行解除。

#### 10.8.4 状态元数据独立提交
仅允许当 M3U/TXT SHA 不变时，单提交 JSON 状态变化（如真实证据状态、`publish_blocked`）。不改变订阅内容，保留原 SHA。

---

## 11. 自动化运行

### 11.1 定时运行
UTC `17 22 * * *`（北京时间 06:17）。不得修改。允许延迟或漏运行。

### 11.1.1 漏运行识别与补偿
Manifest 记录成功时间和 `target_slot`。漏运行记录范围并执行补偿（重新采集验证，不逐日重放）。可手动传 `target_slot`，不得传未来时间。带槽补偿防重复执行。补偿失败保留旧订阅和旧时间。不得引入外部收费调度。

### 11.2 手动运行和模式定义
- `test`：只读测试，严禁联网/写 Git/发布。
- `dry-run`：完整采集生成 Candidate 并推送。
- `candidate-publish`：提供 SHA，校验后发布正式四文件。
- `daily-update`：日常更新，受关键变更和阻断限制。
所有写入模式必须先跑测试。不适用模式的输入直接拒绝或忽略并记录。

### 11.3 运行保护与并发

#### 11.3.1 并发组
写入任务（dry-run, candidate-publish, daily-update, 元数据）必须共用同一 concurrency group：`cancel-in-progress: false`, `queue: max`（最多 100 等待）。不修改 Git 的 test 任务除外。

#### 11.3.2 远端分支保护
拿锁后必须拉最新 main。运行期间变 HEAD 则中止。candidate-publish 基于最新 main 创建但须重核基准。非强制快进推送。

#### 11.3.3 权限与 Checkout
写任务需 `contents: write`，阻断需 `issues: write`。`fetch-depth: 0`。Actions 固定 Commit SHA。

---

## 12. 测试与质量控制

### 12.1 测试分层
- `unit`：不联网，覆盖 Schema、核验、匹配、字符约束、规范化、排序等。
- `integration`：本地 Fixture，覆盖网络层安全、重定向、超时、HLS 边界、调度逻辑、压力测试、Candidate 提取等。
- `acceptance`：真实探测与流程验收。未实测状态保持 `unverified`。

### 12.2 关键测试点补充
- `catalog.py` 接口契约和全局库核验。
- `channels.txt` 模式切换及默认地区隔离。
- `--force` 映射与绕过边界。
- RunReport 新增字段的 Schema 校验（第二阶段必须更新 Schema）。

### 12.3 发布门槛
单测/集成/安全/压力全绿，无 `publish_blocked`。国内未实测不阻断。

---

## 13. 退出码与错误类型

### 退出码
- 0：成功。
- 1：配置/输入错误（含库校验失败、前缀未知、SHA 缺失等）。
- 2：不可恢复错误。
- 3：发布保护/失败（空订阅、骤降、基线过期、Raw 不一致等）。
- 4：状态无法确认（推送不明、阻断 Issue/Manifest 建立失败、门禁查询失败）。

### 错误类型
`ConfigError`, `SourceError`, `NetworkError`, `ValidationError`, `FormatError`, `PublishError`。
关键新增：`channel_catalog_schema_error`, `channel_catalog_stats_mismatch`, `channel_catalog_preflight_failed`, `channel_name_char_constraint_violation`, `channel_selection_unknown`, `channel_selection_ambiguous`, `tvg_id_mapping_unknown`, `feed_stream_size_limit`。

---

## 14. 运行报告与发布清单

### 14.1 RunReport
Artifact 保留 30 天。必须通过 Schema。
**新增必填字段**：`selection_mode`, `default_regions`, `preflight_result`, `dropped_by_scope_count`。
*注：第二阶段必须同步更新 `schemas/run_report.schema.json`。*

### 14.2 PublishManifest
记录 `source_commit_sha`, `candidate_commit_sha` (daily更新时为null), 其他三文件 SHA-256、频道/线路数、`publish_blocked`、每日成功时间（UTC+北京时间）等。自身不记录 SHA。

---

## 15. 六阶段实施与验收

### 第一阶段：立项与技术规范冻结
交付三文件，明确全球升级范围和唯一指导地位。

### 第二阶段：基础与全球库核验
- **前置**：5.3 核验完成，6.3 接口冻结，Schema 更新完成。
- **交付**：`catalog.py` 及测试，基础 CI。
- **验收**：核验无冲突，单测全绿，测试不修改正式文件。

### 第三阶段：核心接入
- **前置**：5.4 对齐核验，5.6 上游源实测。
- **交付**：Feed 接入，安全网络层，媒体验证，调度器，线路选择。
- **验收**：安全集成、1000压力测试、HLS边界全绿。

### 第四阶段：发布与首发
- **交付**：M3U/TXT 生成，Candidate 机制，正式发布。
- **验收**：格式一致，SHA 校验通过。

### 第五阶段：自动化
- **交付**：定时更新，补偿，并发锁，阻断机制。
- **验收**：状态不明处理，RunReport 完整。

### 第六阶段：扩展
暂缓。

---

## 16. 开发与协作纪律
1. **绝对顺序**：5.3 核验 -> 5.4 对齐 -> 6.3 冻结 -> catalog 编写。不可跳跃。
2. 本文档是唯一指导，若冲突以此为准。
3. 未跑过的测试严禁标为通过。
4. 核验结果必须记入 `PROGRESS.md`，但规范由本文件界定。
5. 交付完整文件，不直接修改用户仓库。

---

## 17. 最终交付标准
系统能自动收集、识别、验证、筛选、发布，严格区分四层验收边界，保持未经实测为 `unverified`。

---

## 附录 A：技术参考
- HLS RFC 8216: https://www.rfc-editor.org/rfc/rfc8216.html
- aiohttp Client: https://docs.aiohttp.org/en/stable/client_reference.html
- Python ipaddress: https://docs.python.org/3/library/ipaddress.html

## 附录 B：进度基准
- 母版 Commit: `c62b4c0...`
- 当前状态：方案确定，等待第二阶段前置核验与契约冻结。
- 下一步任务：执行 5.3 节核验并冻结 6.3 节契约，通过后方可开始编写 `catalog.py`。
