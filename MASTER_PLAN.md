IPTV-Auto-Next MASTER_PLAN.md

版本：1.17-G3 完整恢复修订版
文件性质：项目总施工规范
适用范围：整个项目的架构设计、开发实施、测试验收和正式发布

本版本以原始 1.17 为基础，保留已经确定的项目目标、架构、技术参数和发布保护规则，合并全球频道库升级及已确认的修正。本文档是项目唯一总施工依据；实施进度单独记录在 "PROGRESS.md"。

---

1. 项目目标

1.1 核心目标

建设一个高效率、自动化运行的 IPv4 IPTV 直播源仓库。

系统自动收集直播源，识别全球频道身份，筛选符合首版技术支持范围的 IPv4 直播线路，持续生成可用订阅，并如实记录国内网络验证状态。

系统必须实现：

1. 自动收集登记的公开或授权直播源。
2. 使用全球频道库识别频道身份。
3. 根据用户频道清单筛选目标频道。
4. 检测 IPv4 地址及网络连接安全。
5. 验证直播媒体是否符合首版支持的技术要求。
6. 每个频道最多保留三条有效线路。
7. 自动生成 M3U 和 TXT 订阅。
8. 按计划持续更新订阅文件。
9. 正式发布失败时保护上一份成功订阅。
10. 保留运行报告、文件 SHA 和发布记录，保证结果可追溯。

1.2 基本原则

1. 以实际播放所需的媒体结构和网络能力为核心，不以地址数量为目标。
2. 基础直播功能优先完成。
3. 所有来源采用统一的数据结构和验证流程。
4. 不允许单一 HTTP 成功状态代表线路可播放。
5. 全球频道库只负责频道身份识别，不代表频道已经拥有可用线路。
6. 不依赖收费云服务器、备案域名或长期运行的个人电脑。
7. 不使用收费云拨测服务。
8. 不使用线路评分系统。
9. 不增加复杂的持久化线路数据库或自动黑名单。
10. 未经实际验证的功能不得标记为已完成。
11. 严格区分程序技术探测、国内订阅下载、国内媒体可达性和实际设备播放。
12. 国内真实网络验证不是首版开发、首发或日常自动更新的前置条件。
13. 暂时没有真实国内验证证据时，必须标记为 "unverified"，不得虚构验证结论，也不得因此阻断正常开发和发布。
14. 本项目不绑定任何特定播放器，输出订阅必须保持通用标准格式。

1.3 固定核心参数

项目| 固定值
有效来源名额| 40
单来源有效候选上限| 100
总候选上限| 1000
全局网络验证并发| 20
单主机网络验证并发| 5
内部等待队列| 60
单候选验证预算| 8秒绝对预算
入队等待上限| 60秒
来源订阅下载上限| 解压后8MB
HLS 清单上限| 解压后1MB
TS 探测上限| 64KB
重定向上限| 5跳
每频道线路上限| 3
线路骤降保护| 50%
每日更新时间| 北京时间06:17

除非有实际证据、明确的风险分析和用户确认，不得擅自修改以上参数。

1.4 验收层次与责任边界

第一层：程序技术探测

发生在 GitHub Runner 内部。验证来源和频道格式、全球可路由 IPv4、安全连接、TS/HLS 结构等。

该层是系统必须负责并通过自动化测试保障的强制门槛，但不代表中国大陆网络能够访问媒体内容，也不代表播放器能够正常播放。

第二层：国内网络订阅分发

验证中国大陆真实网络能否成功拉取正式 GitHub Raw 订阅文件，并检查格式、频道身份和线路对应关系。

首版默认 "unverified"，只有真实证据才能标记 "passed" 或 "failed"。此层不属于首发或日常更新强制门槛。

第三层：国内媒体网络可达性

验证媒体地址及必要的 HLS 分片能否在中国大陆真实网络中成功请求。

首版默认 "unverified"，没有真实媒体请求证据不得标记 "passed"。此层不属于首发或日常更新强制门槛。

第四层：实际设备播放反馈

发生在真实设备和真实播放器，作为外部使用反馈，不纳入项目强制自动验收。

---

2. 项目实施阶段与绝对顺序

项目分为六个阶段，必须依次实施和验收：

1. 立项与技术规范冻结。
2. 仓库与基础框架。
3. 核心直播系统。
4. 订阅生成与首发。
5. 自动化与稳定性。
6. 扩展能力。

不得跳过阶段验收。后续阶段发现前序阶段缺陷时，先修复并重新验收，不得以临时绕过代替修复。

2.1 绝对前置序列

必须严格按以下顺序执行，不得跳跃：

1. 完成第一阶段规范冻结。
2. 完成第二阶段第0步：全球频道库启动前核验（第5.4节）。
3. 完成上游频道 ID 对齐核验（第5.5节）。
4. 完成上游 Feed/Streams 实测（第5.6节）。
5. 冻结模块接口契约（第6.3节）。
6. 更新并验证相关 JSON Schema（第6.4节）。
7. 将以上核验结果和证据记入 "PROGRESS.md"。
8. 完成以上步骤后，方可编写 "catalog.py" 及其他依赖全球频道库结构的业务代码。

第二阶段允许开展仓库结构检查、依赖环境验证、Schema 现状检查和测试框架准备，但不得提前编写依赖全球频道库结构的业务实现。

第三阶段不得重复安排已经完成的前置核验。

2.2 阶段完成条件

每个阶段必须有实际文件、测试结果或核验记录作为完成依据。

仅有计划、代码草稿或未经执行的测试，不得标记为完成。

---

3. 技术环境与依赖

3.1 运行环境

- 运行平台：GitHub-hosted Runner。
- 操作系统：Ubuntu 24.04。
- 开发语言：Python。
- 首选版本：Python 3.14 最新补丁版。
- Python 精确版本写入 ".python-version"。
- GitHub Actions 安装的 Python 版本必须与 ".python-version" 完全一致。
- 依赖版本必须通过 "uv.lock" 锁定。

必须在 GitHub-hosted Ubuntu 环境实际验证：

- Python 版本与 ".python-version" 一致。
- aiohttp、pytest 安装和导入成功。
- asyncio 基础功能和取消行为正常。
- Ruff、uv 正常。
- 依赖锁文件存在且有效。
- "uv lock --check" 通过。
- "uv sync --locked" 通过。
- Ruff 检查通过。
- pytest 全部通过。

如果 Python 3.14 安装或运行失败，必须记录完整报错并排查。确认短期无法解决后，才允许评估 Python 3.13 最新补丁版。回退必须附带排查证据并记录在 "PROGRESS.md"。

不得仅凭本地电脑运行成功就认定 GitHub Runner 环境验证通过。

3.2 核心技术

- Python / asyncio / aiohttp
- dataclasses
- JSON Schema Draft 2020-12
- pytest
- Ruff
- uv
- GitHub Actions

3.3 依赖管理

使用：

- "pyproject.toml"
- "uv.lock"
- ".python-version"

依赖版本必须锁定。第三方 GitHub Actions 必须固定到完整 commit SHA，不得仅使用可变版本标签。

3.4 数据校验边界

- JSON Schema 用于配置文件和持久化 JSON 校验。
- 运行时内存数据使用 dataclasses。
- Schema 版本统一采用 JSON Schema Draft 2020-12。
- Schema 校验失败不得静默忽略或自动修补后继续运行。

全球频道库的唯一校验标准为：

- "data/global_channels/channels.schema.json"
- "data/global_channels/channel_filter.schema.json"

旧的 "schemas/channels.schema.json" 正式废弃，必须删除，不得保留第二套频道库 Schema。

---

4. 项目目录结构

IPTV-Auto-Next/
├── MASTER_PLAN.md
├── PROGRESS.md
├── README.md
├── manual.txt
├── .python-version
├── pyproject.toml
├── uv.lock
├── .github/
│   └── workflows/
├── data/
│   └── global_channels/
│       ├── channels.json
│       ├── channels.schema.json
│       ├── channel_filter.json
│       ├── channel_filter.schema.json
│       └── validation_summary.json
├── config/
│   ├── sources.json
│   └── channels.txt
├── schemas/
│   ├── sources.schema.json
│   ├── run_report.schema.json
│   ├── publish_manifest.schema.json
│   ├── candidate_manifest.schema.json
│   └── subscription_info.schema.json
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

目录职责：

- "data/global_channels/"：全球频道身份库、筛选配置、Schema 和数据核验摘要。
- "config/sources.json"：直播源入口配置。
- "config/channels.txt"：用户频道选择清单。
- 根目录 "manual.txt"：人工订阅来源入口。
- "schemas/"：来源、运行报告、发布清单、Candidate 和订阅信息 Schema。
- "src/iptv_auto_next/catalog.py"：全球频道库读取、校验、选择和身份查询。
- "output/candidate/"：待人工审阅的 Candidate，不是正式订阅。
- "output/" 根目录：正式发布的订阅成品和清单。

特别约束：

1. 全球频道库唯一数据路径为 "data/global_channels/"。
2. 不再读取旧的 "config/channels.json"。
3. "config/channels.txt" 是用户频道选择清单。
4. 根目录 "manual.txt" 是人工订阅来源入口。
5. 不得为了拆分模块而增加没有必要的文件。
6. Candidate 文件不得被正式订阅地址引用。

---

5. 配置管理、解析与全球频道库核验

5.1 来源配置与解析

5.1.1 sources.json 结构

"config/sources.json" 必须存在三个数组：

- "manual_single"
- "carriers"
- "discovery"

允许数组为空。

每个来源必须具有全局唯一 "id"。URL 不得包含 userinfo、CR、LF 或其他控制字符。"enabled=false" 的来源不下载、不占名额。

每个 "manual_single" 对象必须包含唯一 id、有效 "tvg_id" 和 URL。

每个 "carriers"、"discovery" 对象必须包含唯一 id、URL 和布尔值 "enabled"。

三个数组必须保留，不能用 null 或省略字段代替空数组。来源配置必须通过 "sources.schema.json" 校验，禁止未知字段静默进入运行配置。

5.1.2 来源优先级

来源优先级严格如下：

1. 人工单条 "manual_single"。
2. 人工订阅 "manual.txt"。
3. 运营商来源 "carriers"。
4. 自动发现 "discovery"。

同一类别内部保持配置原始顺序，不得擅自重排。

5.1.3 候选上限与名额分配

首版限制：

- 总来源名额：40。
- 单个订阅来源最多接收100条有效候选。
- 总候选池：1000条。
- 人工单条不占40个来源名额，也不受单来源100条限制，但计入总候选1000条。

规则：

1. "manual_single" 优先解析并进入候选池，不占40个来源名额。
2. "manual.txt" 按一个人工订阅来源处理。
3. 人工订阅、运营商来源和自动发现来源共用40个有效来源名额。
4. 来源只有在至少产生一条通过频道身份识别、频道范围过滤、URL 校验和去重的有效候选后，才占用来源名额。
5. 下载失败、格式不支持、解析失败、没有匹配频道、候选全部被去重或全部被范围过滤的来源，不占来源名额。
6. 按来源优先级串行处理，或采用能保证严格相同结果的分阶段实现。
7. 不得先全量并行下载所有来源，再事后计算名额。
8. 达到40个有效来源、单来源100条或总候选1000条时，立即停止后续处理。
9. 频道选择过滤必须在来源名额和候选数量截断之前执行。
10. 每次停止必须记录停止原因、已接收数量及能够确定的未处理数量。

5.1.4 解析与去重顺序

必须依次执行：

1. 按来源优先级获取来源内容。
2. 解析 M3U 或 TXT 条目。
3. 校验条目 URL 基本格式和协议。
4. 识别频道身份。
5. 执行用户频道范围过滤。
6. 生成规范化 URL。
7. 对规范化 URL 做全局去重。
8. 应用单来源100条限制。
9. 应用总候选1000条限制。
10. 提交网络验证调度器。

同一 URL 在不同来源重复出现时，只验证一次，保留优先级最高且原始顺序最靠前的第一条。

若同一 URL 被不同频道身份声明，保留优先级最高的第一条并记录 "cross_channel_url_conflict"，后续冲突条目丢弃，不得把同一 URL 同时输出为多个频道。

最终线路选择阶段不得再次改变 URL 去重归属；只能执行唯一性断言，发现重复属于程序错误。

5.1.5 manual.txt 解析

- 固定路径：仓库根目录 "manual.txt"。
- UTF-8 纯文本，每行一个完整 HTTP/HTTPS 订阅地址。
- 空行忽略，首尾空白去除。
- 不修改 URL 路径和查询参数。
- 每行作为一个独立人工订阅来源。
- 文件为空或全为注释时，不产生有效候选，不占有效来源名额。
- 下载内容按实际内容自动识别 M3U 或 TXT，不依赖 URL 后缀。
- 下载内容必须先经过网络安全检查、超时和大小限制，再解析。

M3U 规则：

- 以 "#EXTM3U" 或有效 "#EXTINF" 记录识别。
- 每个 "#EXTINF" 对应其后第一个非空、非注释 URL 行。
- 缺少 URL 的条目记为解析失败。
- 下一个 "#EXTINF" 到来前仍没有 URL，前一条记为失败。
- 一个 URL 不得被关联到多个频道。
- 允许 UTF-8 BOM 和 CRLF 输入，解析时统一处理。

TXT 规则：

- 按 RFC 4180 CSV 字段规则逐行解析。
- 每条有效记录必须恰好包含两个字段：频道名称、URL。
- 字段数量不为2的记录记为解析失败，不废弃整个文件。
- 不得把完整 M3U/TXT 订阅文件当作单条媒体线路。

如果内容既不能识别为 M3U，也不能按上述规则解析为 TXT，则判定格式不支持。

单个来源失败或无法解析时，记录原因并跳过，不得中断其他来源。

5.1.6 来源下载边界

来源订阅下载与候选媒体验证使用不同超时预算：

- 单个来源下载总超时：20秒，包含 DNS、连接、重定向和内容读取。
- 单个来源下载内容上限：解压后8MB。
- 重定向最多5跳。
- HTTP 状态必须为200，其他状态记录失败原因并跳过。
- 必须流式读取并累计解压后字节数，不得只依赖 Content-Length。
- 超过8MB立即中止。
- 不进行额外重试。
- 所有来源下载必须通过 "network.py"。

5.1.7 初始全球频道数据来源

全球频道库以公开的上游频道数据库为基础，具体上游仓库和数据版本必须固定记录。

上游版本必须锁定 commit SHA，不能只记录浮动的 "master" 或 "main" 分支名称。

初始数据处理原则：

- 上游频道 ID 映射为本项目 "tvg_id"。
- 上游频道名称映射为 "canonical_name"。
- 上游别名映射为 "aliases"。
- 国家、类别等字段按上游数据结构保留并核验。
- 必要的人工修正必须经过冲突检查。
- 全球频道库写入本项目仓库后，运行时只读取本地锁定数据，不得每次运行自动覆盖。
- 上游版本升级必须作为明确的数据变更重新核验。

全球频道库定义项目能够识别的频道身份范围。未纳入频道库的频道不得通过模糊匹配擅自加入。

全球频道库存在某个频道，不代表存在该频道的实际播放线路。

5.2 全球频道库与筛选配置

5.2.1 数据文件

全球频道库固定由以下文件组成：

- "data/global_channels/channels.json"
- "data/global_channels/channels.schema.json"
- "data/global_channels/channel_filter.json"
- "data/global_channels/channel_filter.schema.json"
- "data/global_channels/validation_summary.json"

不得另建第二套并行频道库。

5.2.2 频道身份

每个频道必须有：

- 唯一且非空的 "tvg_id"。
- 非空的 "canonical_name"。
- "aliases" 数组。
- 国家代码。
- 类别信息及上游规定的必要字段。

具体字段以当前锁定的全球频道库 Schema 为准。

"channels.json" 是频道身份数据；"channel_filter.json" 是筛选范围配置。二者职责不得混用。

5.2.3 频道筛选模式

"config/channels.txt" 有有效内容时，进入人工选择模式：

- 每行一个目标频道。
- 可以选择不同国家和地区的频道。
- 只输出用户明确选择的频道。
- 不得因频道属于非中国地区而排除。

"config/channels.txt" 为空或只有注释时，进入默认模式：

- 默认范围为 CN、HK、MO、TW。
- 具体范围以 "channel_filter.json" 中锁定的筛选配置为准。
- 不得把全球频道库全部频道默认输出。

两种模式后续共用统一的来源采集、身份识别、网络验证、筛选、订阅生成和发布流程。

5.2.4 用户目标匹配

"channels.txt" 每行目标：

1. 优先按完整 "tvg_id" 精确匹配。
2. 未匹配时，才按规范化名称精确匹配。
3. 不允许模糊匹配、部分匹配、拼音猜测或自动推断。
4. 重复目标仅保留首次，记录重复数量。
5. 目标无法匹配或匹配到多个频道，启动失败，退出码1。
6. 只要有一个目标无法匹配或产生歧义，整个启动过程直接报错退出，不允许静默跳过。

5.2.5 来源条目匹配

来源中的 Candidate 与用户目标匹配规则不同：

- 只要来源条目存在 "tvg-id" 属性，就必须按 ID 精确匹配。
- "tvg-id" 存在但为空，直接拒绝。
- "tvg-id" 存在但不匹配，直接拒绝。
- 以上两种情况绝不回退名称匹配。
- 只有完全不存在 "tvg-id" 属性时，才允许按名称匹配。

5.2.6 名称规范化

统一执行：

"Unicode NFKC → 去首尾空白 → 转小写"

不删除内部空格，不删除标点，不转换拼音，不自动转换繁简体。

名称规范化仅用于比较，不修改频道库原始名称和别名。

5.3 全局身份完整性与匹配规则

5.3.1 全局命名空间检查

启动前检查整个全球频道库，而不只是本次选择范围：

- "tvg_id" 必须非空。
- "tvg_id" 必须全局唯一。
- 不同频道之间，任何会导致同一输入指向不同频道的规范化名称或别名键均属全局冲突。
- 频道名称和别名不得包含双引号、CR 或 LF。
- Schema、字段类型和必填字段必须通过校验。
- 国家、类别和上游字段必须符合锁定的数据规范。

任何全局冲突均启动失败，退出码1。

不得因为冲突频道不在本次选择范围内而忽略。

5.3.2 身份命名空间

"tvg_id"、"canonical_name" 和 "aliases" 的查找命名空间不得产生跨频道歧义。

频道身份必须确定性匹配。禁止通过子串包含、模糊相似度或自动猜测选择频道。

5.3.3 冲突检测测试

必须覆盖：

- 重复 tvg_id。
- 重复 canonical_name。
- 跨频道 alias 冲突。
- 规范化后冲突。
- 名称与另一频道 alias 冲突。
- CCTV-5 与 CCTV-5+ 不得误判。
- 不同国家频道使用相同显示名时的身份隔离。

5.4 全球库启动前核验（第二阶段第0步）

5.4.1 全局身份命名空间检查

启动前检查整个频道库：

- tvg_id 非空且全局唯一。
- 所有规范化名称和别名键不存在跨频道冲突。
- 字段类型、必填字段和 Schema 全部通过。
- 频道名称和别名不得包含双引号、CR 或 LF。
- 国家代码、类别值和空类别情况必须可统计。
- 不得仅检查用户选择范围而忽略全球库其他频道。

任何全局冲突均阻断启动，退出码1。

5.4.2 selected_country_name_conflict_keys

全局命名空间检查通过后，计算本次选择范围：

- 人工模式：统计用户选择的频道。
- 默认模式：统计 CN、HK、MO、TW 频道。

将范围内全部名称和别名规范化，建立“名称键 → 频道集合”映射。

同一个键关联两个或以上不同频道，计为一个冲突键；涉及更多频道仍只计一次。

由于5.4.1已经保证全库无冲突，此字段仅用于防御性校验和记录风险，正常情况下该值必须为0。

如果发现非零，代表代码内部状态错乱或全球库被并发篡改，必须：

1. 抛出专用致命异常 "GlobalIdentityInvariantError"。
2. 记录错误代码 "GLOBAL_IDENTITY_INVARIANT_VIOLATION"。
3. 记录冲突键和涉及频道。
4. 立即停止采集、验证和发布。
5. 以退出码1结束。

不得仅使用可能被 Python 优化模式移除的普通 "assert" 作为唯一保护。

5.4.3 validation_summary.json

必须核验并记录：

- "channels"
- "unique_tvg_ids"
- "countries"
- "country_counts"
- "category_values"
- "empty_categories"
- "selected_country_name_conflict_keys"
- "json_bytes"

统计结果必须与实际全球频道库一致。

"selected_country_name_conflict_keys" 非0属于致命不变量错误，不是普通警告。

5.5 上游频道 ID 对齐核验

必须验证上游频道身份与本地全球频道库之间的对应关系。

检查内容：

- 上游 ID 是否稳定、唯一。
- 上游频道 ID 是否正确映射到本地 tvg_id。
- 名称、别名是否存在错误映射。
- 国家代码是否一致。
- 上游字段变化是否影响本地 Schema。
- 是否存在同名但身份不同的频道。
- 是否存在上游记录缺失或重复。

无法确定身份的记录不得自动猜测归属。

核验结果和上游版本 SHA 记录到 "PROGRESS.md"。未完成不得进入依赖该结果的业务实现。

5.6 上游 Feed/Streams 实测

必须对上游 Feed/Streams 数据进行实际结构检查：

- 数据能否正常读取。
- Feed/Stream ID 是否有效。
- Feed 与频道身份的对应关系是否可靠。
- 是否存在重复、失效或结构异常。
- 上游数据是否提供实际媒体地址。
- Feed 与频道身份是否存在一对多、多对一或无法确认的关系。

不得把上游存在频道记录等同于存在可播放线路。

不得把上游公开频道目录中的播放地址直接认定为有效线路。

实测失败必须记录具体原因，不得伪造成功结果。

---

6. 核心数据模型与接口契约

6.1 统一数据对象

系统使用以下运行时 dataclass：

- Source
- Candidate
- VerifiedLine
- Channel
- ValidationResult
- RunReport
- PublishManifest

关键字段：

Source

来源 ID、来源类型、优先级、原始顺序、来源 URL、启用状态。

Candidate

候选 ID、来源 ID、频道 tvg_id、原始 URL、规范化 URL、来源内顺序。

Channel

tvg_id、canonical_name、aliases、国家、类别及必要的上游身份信息。

ValidationResult

候选 ID、验证等级、两次验证结果、阶段耗时、错误类型和验证时间。

VerifiedLine

候选信息、验证等级、验证时间及验证结果。

RunReport

单次运行的完整过程和结果。

PublishManifest

当前正式发布文件、SHA、统计数据、发布来源和状态。

来源身份、线路身份、频道身份必须分开管理：

- 来源身份：线路从哪个来源取得。
- 线路身份：规范化后的媒体 URL。
- 频道身份：全球频道库中的 tvg_id。

6.2 验证等级与稳定性判定

- "stable"：两次短验证均通过。
- "unstable"：一次通过、一次失败。
- "single_pass"：至少一次通过，另一次因总预算耗尽而未完成。
- "pending"：尚未进入或完成验证的内部调度状态，不得作为最终有效线路状态。
- "invalid"：两次均未通过，或没有任何一次完整通过。

TS 流必须找到连续5个 "0x47" 同步字节，间隔严格为188字节。

两次验证规则：

1. 两次验证串行执行，不增加固定等待。
2. 两次完整验证共用一个8秒总预算，不是每次8秒。
3. 每次短验证均执行完整媒体验证流程。
4. 第一次完整结束后，只要总预算仍有剩余，就执行第二次。
5. 总预算耗尽，立即停止，不再启动第二次。
6. 不增加第三次验证或额外重试。

第一次| 第二次| 最终状态| 是否有效
通过| 通过| stable| 是
通过| 失败| unstable| 是
失败| 通过| unstable| 是
通过| 未完成（预算耗尽）| single_pass| 是
失败| 未完成（预算耗尽）| invalid| 否
失败| 失败| invalid| 否
未完成| 未执行| invalid| 否

只有至少一次完整通过，才可进入有效线路集合。

"queue_wait_timeout" 是调度排队超时，不属于媒体验证失败，不得记为 unstable。排队超时的候选不进入有效线路集合。

验证结论边界：

1. 连续5个 "0x47"、间隔188字节，只能证明数据具有 MPEG-TS 结构特征。
2. 不代表节目表、音视频轨道、解码或画面已经验证成功。
3. stable 只代表两次规定的程序技术探测均通过。
4. 所有验证等级均属于第一层程序技术探测等级。
5. TS 结构探测结果必须与国内媒体可达性验证结果分开记录。

6.3 模块接口契约冻结

接口必须在全球频道库启动前核验、上游 ID 对齐核验和 Feed/Streams 实测完成后冻结。

全球频道库接口至少包括：

- "load_catalog(channels_path, filter_path)"
- "validate_catalog(...)"
- "resolve_selection(channels_txt_path)"
- "is_in_scope(tvg_id)"
- "ordered_channels"
- "channel.match_identity(raw_tvg_id, raw_name)"

约束：

1. "ordered_channels" 必须保持 "channels.json" 原始数组顺序。
2. "resolve_selection" 必须返回明确的人工模式或默认模式。
3. 任一用户目标无法匹配或产生歧义，必须抛出明确异常并退出，不得静默跳过。
4. 来源条目存在 tvg-id 时必须按 ID 精确匹配。
5. ID 不匹配抛出 "InvalidIdentityError"。
6. 名称歧义抛出 "AmbiguousIdentityError"。
7. 全局身份不变量异常使用 "GlobalIdentityInvariantError"。
8. 其他模块不得自行复制一套频道匹配规则。

接口冻结后如需变更，必须先更新本文档、Schema、测试和 PROGRESS 记录。

6.4 Schema 更新与校验

在6.3接口契约冻结后，更新并验证相关 JSON Schema。

必须覆盖：

- "data/global_channels/channels.schema.json"
- "data/global_channels/channel_filter.schema.json"
- "schemas/sources.schema.json"
- "schemas/run_report.schema.json"
- "schemas/publish_manifest.schema.json"
- "schemas/candidate_manifest.schema.json"
- "schemas/subscription_info.schema.json"

全球频道库 Schema 与其他运行配置 Schema 分开管理，不得重复定义第二套频道库标准。

所有 Schema 必须通过 Draft 2020-12 校验。

Schema 更新、实际校验结果和文件状态必须记录到 "PROGRESS.md"。

完成本节后，才能开始依赖全球频道库结构的业务代码。

---

7. 网络访问与媒体验证

7.1 网络统一出口

所有网络访问必须通过 "network.py"，包括：

- 来源订阅下载。
- 直接 TS 媒体请求。
- HLS 主清单、子清单和媒体分片请求。
- 重定向请求。
- 发布后的 GitHub Raw 程序侧检查。

其他模块不得自行创建绕过 "network.py" 安全检查的 HTTP 客户端。

7.2 IPv4 验证与安全

7.2.1 协议和目标地址

- 只允许 HTTP 和 HTTPS。
- file、ftp、rtsp、rtmp、WebSocket 等其他协议直接拒绝。
- 只允许连接全球可路由的公网 IPv4 地址。
- IPv6 URL 直接拒绝。
- 域名只查询 IPv4 A 记录。
- 对每个解析结果执行 "ipaddress.is_global" 检查。
- 私有、环回、链路本地、共享地址空间、保留、组播及其他非全球可路由地址一律拒绝。
- DNS 没有合法公网 IPv4 结果时拒绝。

7.2.2 DNS Rebinding 防范

1. DNS 返回多个 IPv4 地址时，逐个检查。
2. 实际连接只能使用已经检查通过的公网 IPv4。
3. 必须使用自定义 resolver 或等效机制，将已校验 IP 直接提供给实际连接器。
4. 禁止连接阶段再次使用系统 DNS 对原域名进行未校验解析。
5. 关闭 DNS 缓存，避免使用过期或未经本次检查的解析结果。
6. 实际 TCP 连接建立后，必须检查 socket peer IP 与本次已校验 IP 一致；不一致立即关闭连接并拒绝。
7. HTTP 请求必须保留原域名 Host。
8. HTTPS 必须使用原域名进行 TLS SNI 和证书主机名校验。
9. 禁止通过系统代理绕过上述 IP 校验。
10. 显式设置 "trust_env=False"，不读取 HTTP_PROXY、HTTPS_PROXY 等系统代理环境变量；请求不得指定代理。

7.2.3 TLS 和请求客户端

- HTTPS 必须启用系统可信 CA 证书校验。
- 禁止使用 "ssl=False" 或关闭证书校验。
- 禁止接受域名不匹配、无效或过期证书。
- 不跨候选共享 Cookie。
- 不从环境变量读取代理。
- 禁止自动重定向。
- 使用流式读取和解压后字节计数。
- 候选验证连接不得复用未经本次目标校验的旧连接。
- 首版采用关闭连接复用或经过等效证明的实现，确保每次新连接均经过已校验 resolver 和 peer IP 检查。
- 实际连接器的 DNS、socket peer IP、Host、SNI 和证书行为必须有集成测试。

7.2.4 重定向与子请求

- "allow_redirects=False"，手动处理重定向。
- 每个请求最多跟随5跳，初始请求不计为重定向。
- Location 相对地址必须以当前请求 URL 为基准解析。
- 覆盖相对路径、根路径、跨主机路径和绝对 URL。
- 每次解析完成后，重新检查协议、主机、端口、DNS 和 IPv4 安全性。
- 未完成安全检查前不得连接。
- HTTPS 重定向到 HTTP 属于协议降级，直接拒绝。
- HLS 子清单和分片 URI 同样必须重新经过完整安全检查。
- 重定向超过5跳立即失败。

7.2.5 安全测试要求

必须测试：

- 实际 socket 连接 IP 是否等于已校验 IP。
- DNS 解析后是否存在未经校验的二次解析。
- HTTP Host 是否保留原域名。
- HTTPS SNI 是否使用原域名。
- 正确证书是否通过。
- 错误证书和域名不匹配证书是否被拒绝。
- 系统代理环境变量是否无法绕过 IP 校验。
- 每次重定向是否重新执行完整安全检查。
- HLS 子清单和分片是否重新执行安全检查。

不能只测试 DNS 解析函数返回正确 IP，还必须测试实际网络连接器行为。

7.2.6 网络错误处理

所有网络失败必须有明确错误类型和错误代码。

安全检查失败不得降级为普通网络失败后继续访问。

7.3 请求限制、并发与读取策略

首版限制：

- 总候选1000。
- 单来源候选100。
- 有效订阅来源40。
- 全局媒体验证并发20。
- 同一主机媒体验证并发5。
- 等待队列最多60个等待任务。
- 单候选媒体验证总预算8秒。
- 单候选队列等待上限60秒。

7.3.1 候选调度规则

1. 候选池最多1000条。
2. 调度器最多允许20条正在验证，另有最多60条处于等待队列。
3. 超出60条等待容量的候选保留在尚未入队的待调度列表中，不丢弃。
4. 候选只有进入等待队列后，才开始计算60秒队列等待时间。
5. 尚未进入等待队列的候选不计入队列等待时间。
6. 等待队列中的候选超过60秒仍未获得验证资源，记录 "queue_wait_timeout" 并从队列移除。
7. 全局20个并发和同一主机5个并发必须由中央调度器统一管理。
8. 不允许工作任务先占用执行工作位，再阻塞等待单主机并发名额。
9. 调度器按等待顺序选择最早且当前主机有可用名额的候选。
10. 某主机已达到5个并发时，可以先调度其他主机候选，不能让空闲全局并发位闲置。
11. 被跳过等待主机名额的候选继续计算队列等待时间。
12. 取得全局和主机资源、即将开始网络验证时，才启动8秒总预算。
13. "queue_wait_timeout" 不得占用网络验证并发名额。

7.3.2 8秒总预算

单候选8秒总预算包含：

- DNS 解析。
- TCP 连接。
- TLS 握手。
- 每次重定向。
- HLS 主清单。
- HLS 子清单。
- HLS 媒体分片。
- 两次短验证。

必须使用单个绝对截止时间控制整个候选验证过程。每个 HTTP 请求只能使用该候选剩余时间，不得在每个请求开始时重新获得8秒。

必须使用整体 deadline 控制所有异步请求，不能只依赖单次请求的 "ClientTimeout(total=8)"。

达到绝对截止时间，立即终止该候选验证。

7.3.3 读取限制

1. 订阅文件：解压后最多8MB。
2. HLS ".m3u8" 清单：解压后最多1MB。
3. TS 媒体流：最多读取64KB。
4. 必须流式分块读取。
5. 不得一次性读取不受限制的响应体。
6. 必须累计解压后的真实字节数，不能只依赖 Content-Length。
7. HLS 清单超过1MB立即失败，不允许截断后继续解析。
8. TS 流累计读取64KB仍未找到同步结构，立即中止并判定失败。
9. 找到连续5个 "0x47" 且间隔188字节后，可以立即停止读取本次 TS 数据。

7.3.4 压力测试

必须在 GitHub-hosted Ubuntu Runner 上执行1000候选受控压力测试。

使用本地受控 Fixture 服务器，不得对不受项目控制的第三方直播服务器发起1000条压力请求。

必须覆盖：

1. 1000候选集中访问同一主机。
2. 1000候选分散访问多个主机。
3. 多主机与热点主机混合访问。
4. 慢响应、连接失败、超时和队列等待。
5. 队列容量达到60。
6. 单主机并发达到5。
7. 全局并发达到20。
8. "queue_wait_timeout" 触发与记录。
9. 候选是否丢失、重复验证或重复进入结果。

必须记录并发峰值、单主机并发峰值、等待队列峰值、排队超时数量、完成数量、有效线路数量、总耗时、CPU和内存峰值及调度阻塞情况。

不得只用理论估算代替实际压力测试。测试失败时先定位实现缺陷，不得未经证据擅自更改固定参数。

7.4 媒体验证完整流程

首版只支持未加密 MPEG-TS。所有请求均计入单候选8秒总预算，并受每个请求最多5跳重定向限制。

7.4.1 直接媒体地址

- 不依赖 URL 后缀。
- 根据响应内容识别媒体类型。
- 最终媒体响应必须为 HTTP 200。
- 不发送 Range 请求。
- 非200状态，包括206，不得作为首版直接 TS 或 HLS 分片验证通过。
- 只有通过 TS 同步结构检测，才算一次完整通过。
- HTML、JSON、普通文本或其他不支持内容均失败。

7.4.2 HLS 识别

- 根据内容识别 HLS 播放列表，不依赖 ".m3u8" 后缀。
- 媒体播放列表包含 "#EXTINF" 和媒体分片 URI 时，直接进入分片验证。
- 主清单包含 "#EXT-X-STREAM-INF" 时，按 Variant 规则处理。
- 不支持的格式必须明确记录原因。

7.4.3 Variant 处理

1. 多码率主清单按原始出现顺序处理。
2. 最多尝试前2个 "EXT-X-STREAM-INF" Variant。
3. 先尝试第一个 Variant。
4. 第一个 Variant 完整验证通过后，停止本次 Variant 尝试。
5. 第一个 Variant 失败时，在8秒剩余预算允许的情况下继续尝试第二个。
6. 第二个 Variant 通过即可视为本次验证通过。
7. 不按带宽、分辨率或名称重新排序 Variant。
8. 不递归解析超过一层的子清单。

7.4.4 分片请求

- 每个媒体播放列表最多请求1个媒体分片。
- 分片必须通过 "network.py"，最终响应必须为 HTTP 200。
- 分片 URI 按该媒体播放列表的实际 URL 使用标准相对 URI 解析。
- 分片最多读取64KB。
- 必须通过 TS 同步结构检测。
- 分片不能识别为未加密 MPEG-TS 时，本次 Variant 失败。

7.4.5 HLS 加密和格式边界

1. "#EXT-X-KEY"：
   - "METHOD=NONE" 表示未加密，可继续处理。
   - 其他 METHOD 一律判定为不支持。
   - 缺失或无法解析 METHOD，判定为格式错误。
2. "#EXT-X-SESSION-KEY"：首版一律拒绝。
3. "#EXT-X-MAP"：直接拒绝并记录 "fMP4_not_supported"。
4. "#EXT-X-BYTERANGE"：首版直接拒绝并记录 "byterange_not_supported"。
5. 主清单声明带 URI 的外部音频或字幕 Rendition 时，首版判定为不支持。
6. 其他无法明确支持的加密或媒体格式，均不得判定通过。

7.4.6 失败判定

以下情况均判定验证失败：

- 没有有效 Variant。
- 没有可用媒体分片。
- HLS 子清单层级超过限制。
- 加密或不支持的格式。
- TS 分片无法满足连续5个 "0x47"、间隔188字节。
- 直接媒体内容无法识别为支持的 MPEG-TS。
- 请求状态、网络安全检查或总预算失败。

本节只定义首版支持边界，不代表已经完成全部 HLS 兼容性验证。

---

8. 频道整理与三线路选择

8.1 来源优先级

人工单条 > 人工订阅 > 运营商 > 自动发现。

来源优先级主要用于采集阶段去重和相同验证等级下的排序，不得覆盖验证等级排序。

8.2 URL 规范化与线路去重

首版 URL 规范化规则：

1. scheme 转为小写。
2. hostname 转为小写并进行 IDNA 规范化。
3. 只删除默认端口：HTTP 80、HTTPS 443。
4. 非默认端口必须保留。
5. Path 原样保留。
6. Query 参数完整保留，不删除、不修改、不重排。
7. 删除 fragment。
8. 不做 tracking 参数删除或推测性 URL 改写。
9. URL 包含用户名或密码的 userinfo 时拒绝。
10. 输出使用规范化后的 URL。

全局去重在媒体验证之前执行，保留来源优先级最高且原始顺序最靠前的第一条。重复条目只验证一次。

8.3 线路排序和截断

只对通过至少一次短验证的唯一线路进行排序。

严格按以下步骤执行：

1. 验证等级：stable > single_pass > unstable。
2. 来源优先级：人工单条 > 人工订阅 > 运营商 > 自动发现。
3. 最近验证时间：从新到旧。
4. 来源内原始顺序：从前到后。
5. 每个频道最多保留前三条线路。

说明：

- unstable 不得排在 single_pass 前面。
- invalid、pending 和 queue_wait_timeout 不得进入正式订阅。
- 不引入线路评分系统、持久化线路数据库或复杂历史记录。
- 每次运行均基于本次采集和验证结果重新生成，不依赖上次运行的线路状态。

8.4 频道输出顺序

- 频道顺序按照全球频道库 "channels.json" 中标准频道数组的原始顺序。
- 人工模式只输出用户选择的频道，但仍保持频道库原始顺序。
- 每个频道内部按8.3规则排列线路。
- 同一频道的多条线路必须连续输出。
- 不得因网络验证完成先后改变频道整体顺序。

---

9. 订阅格式

9.1 M3U 标准与多线路输出

- 首行 "#EXTM3U"。
- 每条线路连续输出：
  - "#EXTINF:-1 tvg-id="..." tvg-name="...",显示名"
  - 下一行是对应 URL。
- 逗号后不得添加空格。
- 同一频道多线路连续输出。
- 不添加私有标签。
- tvg-id 使用标准频道字典原值。
- tvg-name 和显示名使用 canonical_name。
- 频道配置中的 M3U 属性值不得含双引号、CR 或 LF。
- URL 不得含 CR、LF 或其他控制字符。
- UTF-8 无 BOM。
- LF 换行。
- 文件末尾保留一个换行。

9.2 TXT 格式

独立逻辑，UTF-8，LF 换行。

单行格式：

"频道名称,线路URL"

- 频道名称和 URL 两个字段都执行 RFC 4180 字段转义规则。
- 字段包含逗号、双引号、CR 或 LF 时，正确引用。
- 字段内部双引号必须双写。
- 准确表述为采用 RFC 4180 字段转义规则，不宣称完整字节级 RFC 4180 兼容。
- 同频道多线路直接并列输出多行，不允许使用未知分组。
- 末尾保留换行。

9.3 双格式一致性

生成正式文件前，必须重新解析 M3U 和 TXT 并核对：

- 频道集合完全一致。
- 每个频道线路数量一致。
- 每条线路 URL 完全一致。
- 频道顺序一致。
- 线路顺序一致。

任何不一致均阻断发布。

9.4 订阅信息

"subscription_info.json" 记录元数据，必须通过 "schemas/subscription_info.schema.json" 校验。

必须包含：

- 生成时间。
- 订阅版本或 Schema 版本。
- 频道数量。
- 线路数量。
- M3U 和 TXT 的 SHA-256。
- 统一的验证状态对象：
  - "layer1_status"
  - "layer2_status"
  - "layer3_status"
  - "layer2_evidence"
  - "layer3_evidence"

证据规则：

- 没有真实证据时，对应 evidence 为 null。
- 第二层证据必须包含结果、M3U SHA、TXT SHA、验收时间、网络环境、验收方法和证据位置。
- 第三层证据必须包含结果、M3U SHA、TXT SHA、实际请求的媒体 URL、必要的 HLS 分片请求结果、验收时间、网络环境和证据位置。

状态规则：

- 状态枚举统一为 "passed"、"failed"、"unverified"。
- 正式文件通过第一层程序技术探测后，layer1_status 为 passed。
- 没有国内真实订阅分发证据时，layer2_status 为 unverified。
- 没有国内真实媒体请求证据时，layer3_status 为 unverified。
- 不得把 Runner 内部 Raw 检查结果写成国内第二层或第三层通过。
- passed 或 failed 状态必须有对应真实验收证据对象。
- 证据中的 M3U/TXT SHA 必须与当前正式订阅 SHA 一致。
- 不得只修改状态文字。
- layer2_status=unverified 时 layer2_evidence 必须为 null。
- layer3_status=unverified 时 layer3_evidence 必须为 null。
- layer3_status=passed 的证据必须包含真实媒体 URL 请求结果；如果是 HLS，还必须包含被请求分片的结果。

---

10. 订阅发布与验收

10.1 正式发布路径

正式文件固定为：

- "output/iptv.m3u"
- "output/iptv.txt"
- "output/subscription_info.json"
- "output/publish_manifest.json"

这四个文件为正式发布组。

首版唯一正式发布渠道为 GitHub Raw。仓库必须为公开仓库，默认分支固定为 main。

正式 URL：

- "https://raw.githubusercontent.com/<owner>/<repo>/main/output/iptv.m3u"
- "https://raw.githubusercontent.com/<owner>/<repo>/main/output/iptv.txt"

GitHub Pages 不作为正式发布渠道。

10.2 镜像边界

- Gitee、GitCode、jsDelivr 不属于首版正式发布路径。
- 镜像同步不属于基础直播系统的必要依赖。
- 镜像能力仅在第六阶段作为独立扩展评估，不得影响 GitHub Raw 主发布。

10.3 国内验证状态和首发规则

1. 首版不把国内真实网络订阅实测或国内媒体实测作为首发、关键变更或日常自动更新的强制门槛。
2. 首次正式发布和关键变更仍必须经过 Candidate 生成、文件审阅、SHA 校验和人工触发正式发布。
3. Candidate 人工确认是发布审批，不等同于国内网络实测。
4. Candidate 和正式订阅默认：
   - candidate_layer2_status = unverified
   - layer2_status = unverified
   - layer3_status = unverified
5. GitHub Runner 内部 Raw 检查只能记录为 "program_connectivity"。
6. 如果未来实际取得国内网络验证证据，可以单独更新 JSON 元数据。
7. M3U 或 TXT 内容变化，旧的第二层和第三层验收结果自动失效。
8. 仅 metadata 变化、M3U 和 TXT 内容不变，不自动使订阅内容验收失效。
9. 推送前再次确认被测订阅内容没有变化。
10. 不得把第二层订阅文件拉取成功推断为第三层媒体可达。

10.4 国内验收证据标准

第二层订阅分发验收：

1. 在中国大陆真实网络中拉取正式订阅 URL。
2. HTTP 状态必须为200。
3. 检查订阅文件格式。
4. 至少抽查五个频道的频道身份、线路数量及 URL 对应关系；有效频道少于五个时检查全部频道。
5. 记录验收对象、commit SHA、M3U SHA、TXT SHA、验收人、验收时间、结果和证据位置。
6. 严禁请求或验证媒体线路来替代第二层订阅文件验收。

第三层媒体可达性验收：

1. 必须在中国大陆真实网络请求媒体地址。
2. 对 HLS 必须验证必要的媒体分片。
3. 记录媒体 URL、请求结果、时间、网络环境、对应订阅 SHA 和证据位置。
4. 只有真实媒体请求证据才能将第三层状态标记为 passed。
5. 不得由第二层结果推断第三层通过。

以上两层为状态记录标准，不是首版发布门槛。

10.5 Candidate 发布（防测 A 发 B）

10.5.1 Candidate 文件

Candidate 必须包含：

- "output/candidate/iptv.m3u"
- "output/candidate/iptv.txt"
- "output/candidate/candidate_manifest.json"

三个文件必须在同一个 Candidate Git 提交中。

10.5.2 Candidate Manifest

必须记录：

- Schema 版本。
- Candidate 生成时间。
- 生成 Candidate 所使用的源代码和配置提交 SHA："source_commit_sha"。
- Candidate 的 M3U SHA-256。
- Candidate 的 TXT SHA-256。
- 第一层程序技术探测状态。
- Candidate 频道数量和线路数量。
- 生成时四个正式文件的 SHA-256 基准。

四个正式文件基准：

- output/iptv.m3u
- output/iptv.txt
- output/subscription_info.json
- output/publish_manifest.json

首次正式发布前，四个正式文件必须全部不存在，四个基准值统一为 null。

四个正式文件必须全部存在或全部不存在。部分存在、部分缺失时，必须阻断 Candidate 生成。

Candidate Manifest 不记录自身 SHA，也不在自身内容中记录 Candidate commit SHA，避免自引用。

10.5.3 dry-run 生成和推送

mode=dry-run 必须：

1. 获取并确认 main 最新提交。
2. 检查正式四文件全部存在或全部不存在。
3. 记录正式四文件 SHA 基准。
4. 执行来源采集、解析、频道识别、IPv4 安全检查和第一层媒体验证。
5. 生成 Candidate M3U、TXT 和 Manifest。
6. 重新计算 M3U、TXT SHA，并校验 Candidate Manifest。
7. 只提交 output/candidate/ 三个文件。
8. 不修改正式四文件。
9. 以非强制快进方式推送到 main。
10. 推送成功后取得准确 Candidate commit SHA，并写入 RunReport 和 Actions Summary。

Actions Summary 必须展示：

- Candidate commit SHA。
- Candidate M3U SHA-256。
- Candidate TXT SHA-256。
- Candidate 频道数量。
- Candidate 线路数量。
- 第一层状态。

不得仅凭远端分支最新 HEAD 推断 Candidate commit SHA。

10.5.4 candidate-publish 输入参数

必须提供：

- "expected_m3u_sha256"
- "expected_txt_sha256"
- "expected_candidate_commit_sha"

输入格式：

- M3U/TXT SHA-256：64位十六进制字符。
- Git commit SHA：40位十六进制字符。

参数缺失或格式错误，退出码1。

10.5.5 指定提交提取与校验

candidate-publish 必须：

1. 获取 main 完整历史，不能依赖默认浅克隆。
2. 检查目标 commit 存在且属于当前仓库。
3. 检查目标 commit 是当前 main 历史中的祖先提交。
4. 检查 Candidate commit 的直接父提交必须等于 Manifest 中的 source_commit_sha。
5. 检查该 Candidate commit 的文件差异严格只有三个 Candidate 文件。
6. 检查三个 Candidate 文件在该提交中真实存在。
7. 必须通过 "git show <commit>:<path>" 从指定提交读取文件，保存到独立临时目录。
8. 禁止使用 "git checkout <commit>" 修改工作区。
9. 对 candidate_manifest.json 执行 Schema 校验。
10. 重新计算 M3U 和 TXT SHA-256。
11. 分别与 Manifest 内记录的 SHA 比对。
12. 再与用户传入的两个预期 SHA 比对。
13. 检查 Manifest 的四个正式文件基准与当前 main 正式四文件完全一致。
14. 检查 Candidate 生成后核心路径没有发生变化。

核心路径明确包括：

- "src/"
- "config/"
- "data/"
- "schemas/"
- ".github/"
- "manual.txt"
- ".python-version"
- 依赖锁文件，例如 "uv.lock" 及其等效锁定文件。

上述核心路径任何变化均阻断 Candidate 发布。

上述路径之外的文档变化，例如 README.md、MASTER_PLAN.md、PROGRESS.md，不单独阻断 Candidate 发布。

15. 检查 Candidate 第一层状态必须为 passed。
16. 检查 M3U/TXT 格式和内容一致性。
17. 检查正式发布质量门槛。

任一 SHA、文件、Schema、提交归属、核心路径或质量门禁检查失败，均不得发布。Candidate 失效后必须重新执行 dry-run，不得人工绕过。

10.5.6 正式文件生成

- 正式发布的 M3U/TXT 必须与指定 Candidate 文件字节级一致。
- 不得重新生成或重新排序 Candidate 的 M3U/TXT。
- subscription_info.json 和 publish_manifest.json 根据正式文件重新生成。
- 正式四文件必须在同一个 Git 提交中更新。
- 正式发布时 layer2_status 和 layer3_status 默认保持 unverified。
- Candidate 文件保留在 output/candidate/，不属于正式订阅。

10.5.7 Candidate 失效条件

出现以下任一情况，Candidate 不得发布：

- 当前正式四文件 SHA 基准与 Candidate Manifest 不一致。
- 正式四文件从全无变成部分存在或从完整变成部分缺失。
- Candidate 文件 SHA 不一致。
- Candidate commit 不存在或不属于当前 main 历史。
- Candidate commit 父提交与 Manifest 的 source_commit_sha 不一致。
- Candidate commit 文件差异超出三个 Candidate 文件。
- 核心路径发生变化。
- Candidate Manifest Schema 不通过。
- Candidate 第一层状态不是 passed。

Candidate 失效时必须重新执行 dry-run，不得人工绕过。

10.6 关键变更与日常自动更新边界

以下变化属于关键变更：

- "src/"
- "tests/"
- ".github/workflows/"
- "config/"
- "data/"
- "schemas/"
- "manual.txt"
- ".python-version"
- "pyproject.toml"
- "uv.lock"

首次正式发布和关键变更后，必须先 dry-run，再由用户手动触发 candidate-publish。

日常自动更新必须比较当前 main 与上一次正式发布所记录的 source_commit_sha：

- 如果上述关键路径发生变化，自动 daily-update 阻断，要求先生成 Candidate 并人工确认。
- 如果只有 README、MASTER_PLAN、PROGRESS 等非关键文档变化，不阻断日常自动更新。
- 如果没有正式发布记录，daily-update 不得执行首发，必须走 Candidate 首发流程。

10.7 空订阅与质量骤降保护

10.7.1 非空门槛

- iptv.m3u 与 iptv.txt 必须非空。
- 至少1个有效频道。
- 每个输出频道至少1条线路。
- M3U 和 TXT 必须通过9.3双格式一致性检查。

若 channels.txt 有有效频道名单，但最终0频道，禁止发布，退出码3。

以上门槛不受 --force 或其他豁免条件影响。

10.7.2 质量骤降保护

以最近一次成功正式发布的 Manifest 统计为比较基准：

- 本次频道数低于上次频道数的50%，默认阻断。
- 本次线路数低于上次线路数的50%，默认阻断。
- 恰好等于50%不属于“低于50%”，允许通过该项检查。
- 任一项低于50%即阻断，退出码3。
- 首次发布且无 previous manifest 时，跳过骤降检查。

豁免条件：

- 如果 config/channels.txt 或全球频道筛选配置相对于上一次正式发布的 source_commit_sha 发生变化，可以跳过本次50%骤降检查。
- 该豁免只影响50%骤降检查，不影响非空门槛、格式校验、Schema、安全检查、SHA 检查和发布阻断状态。
- 配置变化必须能够通过 Git 历史准确比较；无法读取基准提交时不得自动豁免。

--force 规则：

- 仅允许人工触发的 candidate-publish 或 daily-update 使用。
- 只允许绕过50%频道数/线路数骤降门槛。
- 不得绕过空订阅、名单保护、Schema、格式、安全、SHA、Candidate 基准、核心变更确认、并发保护、远端状态核对或 publish_blocked。
- 定时自动任务不得自动启用 --force。
- 使用 --force 必须在 RunReport 中记录操作者输入、触发方式和绕过的具体门槛。

本条50%保护规则保留。后续如有实际运行数据证明误拦截或漏拦截，必须先提供证据，再提出修改方案，不得无替代保护直接删除。

10.8 发布提交、失败恢复和 Raw 检查

10.8.1 Git 提交边界

- 首次正式发布及每次正式内容更新，四个正式文件必须在同一个 Git 提交中更新。
- Candidate 三个文件必须在同一个 Candidate 提交中更新。
- 生成或推送失败时，不得留下半组正式文件。
- 正式发布只能使用非强制快进方式。
- 绝不使用 force push。
- 正式提交必须基于当前最新 main。
- 提交前再次读取远端 main，若运行期间远端已变化，不得将旧状态直接推送。
- dry-run 和 daily-update 必须中止并从最新状态重新运行。
- candidate-publish 可以基于最新 main 创建正式提交，但必须重新完整核对 Candidate 祖先关系、核心路径一致性和正式四文件基准。
- Candidate 提交的文件差异必须严格只有三个 Candidate 文件。
- 正式发布提交的文件差异必须严格只有四个正式文件。
- README 等无关文件不得被发布程序覆盖。

10.8.2 推送结果核对

- 推送明确被拒绝且确认远端未接受提交：退出码3。
- 推送响应丢失或结果不明确：读取远端分支、commit 和正式文件内容进行核对。
- 如果确认目标提交已进入远端历史，且远端正式文件内容与预期一致，视为推送成功。
- 如果无法确认远端是否接受提交，退出码4。
- 不得在状态不明时盲目重复覆盖或 force push。

10.8.3 Runner 内部 Raw 检查

正式提交成功后，在 GitHub Runner 内部检查正式 GitHub Raw 地址：

- M3U、TXT、subscription_info 必须返回200且 SHA 与 Manifest 对应。
- publish_manifest 必须返回200并通过 Schema。
- 最多执行3次检查，单次间隔5秒。
- 检查结果只记录为 "program_connectivity"。
- 不得标记国内第二层或第三层通过。

结果分类：

- "passed"：文件状态和 SHA 均符合预期。
- "unavailable"：超时、连接失败或非200，无法判断内容是否损坏。
- "content_mismatch"：连续3次均返回200，但内容 SHA 与预期不一致。
- "test_error"：检查程序自身异常。

处理规则：

1. passed：正常记录。
2. unavailable：记录警告，不回滚正式文件，不单独阻断下一次更新。
3. test_error：记录程序错误，不回滚正式文件，不单独阻断下一次更新。
4. content_mismatch：正式提交不自动回滚；立即停止本次运行的后续发布动作，并执行双重持久化阻断流程。
5. 清除 publish_blocked 必须由人工修改并提交 publish_manifest.json，同时在 PROGRESS.md 记录原因和处理证据。

10.8.4 双重持久化阻断机制

为防止 publish_manifest.json 因 Git 并发冲突无法写入，必须同时使用 Manifest 阻断标记和专用 GitHub Issue 作为两层持久化记录。

专用 Issue 标题固定为：

"[IPTV-Auto-Next] PUBLISH_BLOCKED"

检测到 content_mismatch 后：

1. 先检查是否存在相同标题的未关闭 Issue。
2. 已存在则更新该 Issue，追加本次故障记录。
3. 不存在则创建新的专用 Issue。
4. Issue 正文必须记录 GitHub Actions run_id、故障发现时间、正式发布 commit SHA、不匹配文件名、预期 SHA、Raw 实际 SHA、故障原因和对应 Actions 运行链接。
5. 不得在 Issue 中写入凭据、Token 或未经脱敏的敏感地址。
6. 必须确认 Issue 创建或更新成功后，才能继续尝试写入 Manifest 阻断标记。
7. 对应 GitHub Actions Job 必须显式授予 "issues: write" 权限。
8. Issue 创建、更新或成功状态确认失败，立即停止后续发布动作，以退出码4结束。
9. Issue 建立失败时，不得声称后续任务已经受到可靠阻断。

Manifest 阻断状态写入：

1. 写入前必须先获取远端最新 main。
2. 只允许修改 publish_manifest.json 中的 publish_blocked 状态及对应原因。
3. 必须保留远端最新版本中的其他字段和变更。
4. 只允许普通非强制推送。
5. 首次推送失败后，最多额外重试3次，总计最多4次。
6. 每轮重试前必须检查远端 publish_manifest.json。
7. 如果相同的 publish_blocked=true 及对应原因已经存在，视为写入成功。
8. 四次均失败或无法确认远端状态，统一按退出码4结束。
9. 即使 Manifest 阻断标记写入失败，只要专用未关闭 Issue 已成功建立，后续正式发布任务仍必须通过 Issue 门禁阻断发布。

10.8.5 正式任务启动门禁

任何 candidate-publish 和 daily-update 正式发布任务，在执行任何采集、正式文件修改或发布写入之前，必须：

1. 获取正式写入并发锁。
2. 获取远端最新 main 中的 publish_manifest.json。
3. 检查 publish_manifest.json 是否存在 publish_blocked=true。
4. 查询 GitHub 仓库是否存在标题为 "[IPTV-Auto-Next] PUBLISH_BLOCKED" 的未关闭 Issue。
5. 只要 Manifest 为 publish_blocked=true，或者存在该专用未关闭 Issue，就立即停止任务。
6. Manifest 无法获取、Schema 校验失败、Issue 查询失败或远端阻断状态无法确认，必须按退出码4结束，执行 fail-closed。
7. --force 不得绕过 Manifest 阻断、专用 Issue 阻断或启动门禁。

10.8.6 启动阶段 Raw 内容核验

完成并发锁获取和持久化阻断门禁后、开始采集或写入前，强制获取线上 GitHub Raw 当前正式文件：

- M3U
- TXT
- subscription_info
- publish_manifest

对 M3U、TXT、subscription_info 计算实时 SHA-256，并分别与远端 Manifest 中记录的对应 SHA 比对；对 publish_manifest 执行 Schema 校验。

处理规则：

1. M3U、TXT 或 subscription_info 的实时 SHA 与 Manifest 记录不一致，立即中止发布，按退出码3结束，并记录 "raw_content_mismatch_detected_on_startup"、文件名、预期 SHA 和实际 SHA。
2. publish_manifest 无法获取或 Schema 校验失败，按退出码4结束。
3. Raw 文件无法获取或返回非200，不能视为内容一致，必须中止正式发布并按退出码4结束。
4. Raw 核验不能替代 Manifest 和专用 Issue 的持久化阻断。
5. Raw 内容恢复一致不得自动解除已经存在的阻断记录。

10.8.7 人工解除阻断的唯一流程

1. 人工检查并修复 content_mismatch 对应的问题。
2. 人工核实正式 Raw 文件及 SHA 与 Manifest 一致。
3. 人工修改 publish_manifest.json，清除 publish_blocked 状态及对应原因。
4. 通过正常 Git 提交推送至远端 main。
5. 确认远端 Manifest 已成功更新，且阻断标记确实清除。
6. 在 PROGRESS.md 中记录故障原因、修复措施、验证结果和对应证据。
7. 最后由人工关闭专用 GitHub Issue。
8. 如果 Manifest 清除提交失败或远端状态无法确认，禁止关闭 Issue。
9. 禁止仅关闭 Issue、仅恢复 Raw 文件或仅修改本地 Manifest 就解除阻断。
10. 自动任务不得自行清除阻断状态。

10.8.8 特殊退出码

本节特殊退出码优先于一般推送失败分类：

- 退出码3：启动阶段发现 M3U、TXT 或 subscription_info 的实时 SHA 与 Manifest 不一致。
- 退出码4：阻断 Issue 建立或更新失败、阻断状态提交失败、远端状态无法确认、Manifest 或 Issue 门禁检查失败、必要 Raw 文件无法获取或 Manifest Schema 校验失败。

GitHub 服务整体不可用，导致 Manifest 推送和 Issue API 同时无法建立持久化阻断时，必须明确报警并要求人工暂停 candidate-publish 和 daily-update 工作流，直到人工确认阻断状态已经建立。

publish_blocked 不得被 --force 绕过。

10.8.9 状态元数据独立提交

在 M3U 和 TXT 内容 SHA 不变时，允许单独提交：

- 有真实证据的第二层/第三层验收状态。
- publish_blocked 安全状态。
- 与订阅内容无关的必要发布状态字段。

不得在状态元数据提交中改变 M3U/TXT 内容。修改后必须通过 Schema，并保留原订阅 SHA。

---

11. 自动化运行

11.1 定时运行

每天北京时间06:17运行。

GitHub Actions 使用 UTC cron：

"17 22 * * *"

定时工作流必须位于仓库默认分支。不得改成06:00。

GitHub Actions 定时任务可能延迟或漏触发，系统不得宣称能够保证准时运行。

11.1.1 定时任务漏运行识别与补偿

时间统一使用：

- 北京时间：Asia/Shanghai。
- 持久化时间戳：UTC ISO 8601。
- target_slot：北京时间 YYYY-MM-DD 06:17。

Manifest 必须记录：

- "last_successful_daily_update_at"：最近一次成功 daily-update 的实际完成时间，UTC。
- "last_successful_daily_target_slot"：最近一次成功覆盖的定时目标槽，北京时间字符串。

普通手动更新未传 target_slot 时不改变该字段。

漏运行判断：

1. 定时任务启动时，计算本次目标槽，即当前北京时间已经到达的最近一个06:17。
2. 如果最近一次成功 daily-update 时间早于昨天北京时间06:17，记录漏运行。
3. 手动触发 daily-update 时，如果当前触发时间距离最近一次成功 daily-update 超过24小时，记录漏运行。
4. 首次运行无历史记录时，视为正常，不记录漏运行。
5. 延迟触发跨过多个日期时，记录从上次成功更新时间到本次目标槽之间遗漏的日期范围。

补偿机制：

1. 定时任务可将本次运行作为补偿运行，重新采集、验证并生成最新订阅，不要求逐日重放所有错过的历史任务。
2. 用户手动触发 daily-update 时，可以传入 target_slot，格式必须严格为北京时间 YYYY-MM-DD 06:17。
3. 手动传入的 target_slot 不得是未来时间，格式不合法立即拒绝。
4. 任务获得并发锁后，必须重新读取线上 publish_manifest.json。
5. 如果 last_successful_daily_target_slot 已经覆盖本次目标槽，则判定为重复补偿任务，跳过正式发布并记录。
6. 普通手动 daily-update 不带 target_slot，不因刚有一次成功更新而被重复任务逻辑跳过。
7. 补偿成功后更新最近一次成功时间；带有目标槽的补偿还更新 last_successful_daily_target_slot。
8. 补偿失败时保留旧订阅和旧成功时间。
9. 必须记录漏运行日期范围、发现时间、是否补偿、目标槽、补偿结果和最终发布结果。

能力边界：

- GitHub Actions 不能在完全没有新事件时自行唤醒。
- 补偿依靠下一次正常定时触发或人工手动触发发现漏运行。
- 不得为补偿机制引入收费外部调度服务或长期运行的个人电脑。

11.2 手动运行和模式定义

工作流触发规则：

- push 和 pull_request：只运行只读 test job。
- schedule：自动执行 daily-update。
- workflow_dispatch：由用户选择 test、dry-run、candidate-publish 或 daily-update。

Candidate SHA、target_slot 和 force_quality_drop 输入按模式使用；不适用的输入不得被静默解释。

所有会写入 Candidate 或正式文件的模式，在执行网络采集或发布前，必须先完成依赖锁检查、Ruff、单元测试、集成测试和安全测试。测试失败立即阻断写入。

candidate-publish 不重新探测媒体线路，但必须重新执行发布前静态检查和测试。

mode=test

仅测试：

- 单元测试。
- 本地 Fixture 集成测试。
- 配置和 Schema 测试。
- 网络安全测试。
- 1000候选受控压力测试。
- M3U/TXT 格式和发布逻辑测试。

明确禁止：

- 访问外部真实媒体地址。
- 下载真实外部订阅。
- 生成或推送 Candidate。
- 生成或修改正式订阅。
- 提交或推送 Git。
- 执行国内真实验收。

RunReport 必须记录实际执行、跳过和失败的测试项目。

mode=dry-run

- 执行完整来源采集和第一层技术验证。
- 生成 Candidate 三文件。
- 推送 Candidate。
- 获取准确 Candidate commit SHA。
- 不修改正式四文件。
- 不执行国内实测。

mode=candidate-publish

- 必须输入三个预期 SHA。
- 精确提取指定 Candidate commit。
- 完成文件、Schema、SHA、基准和核心路径版本检查。
- 完成发布保护。
- 发布 Candidate 对应的正式四文件。

mode=daily-update

- 等同日常定时更新。
- 重新采集、验证并生成最新订阅。
- 仅当不存在未确认的关键变更、发布阻断和质量保护问题时，才允许更新正式文件。
- 手动触发时可选传入 target_slot。
- 可选 force_quality_drop，只用于人工绕过50%质量骤降门槛。
- 定时触发不得自动启用强制发布。

首版不设置 verify-release 工作模式。

国内第二层和第三层状态没有真实证据时保持 unverified；Runner 不得冒充国内测试环境。

11.3 运行保护与 GitHub Actions 并发

11.3.1 写入任务范围

以下任务会修改 main，必须使用同一个正式写入并发组：

- dry-run：写入 Candidate。
- candidate-publish：写入正式文件。
- daily-update：写入正式文件。
- 必要的发布阻断或验证状态元数据提交。

test 不修改 Git，不需要加入写入并发组。

11.3.2 并发参数

所有写入任务使用完全相同的 concurrency group 名称，并配置：

- "cancel-in-progress: false"
- 在平台实际支持时使用 "queue: max"。

GitHub Actions 并发能力必须按实际平台文档和工作流运行结果核验：

- 不得假设所有环境都支持任意队列参数。
- 不得未经核实宣称100个等待任务和严格 FIFO 一定得到平台保证。
- 如果平台不支持指定队列参数，必须记录实际限制。
- 程序正确性不得依赖 FIFO。
- 不得为不同写入工作流使用不同并发组，否则可能同时修改同一分支。
- 队列满时被取消的任务，不能保证生成自己的 RunReport 或 Artifact。

11.3.3 远端分支保护

- 所有正式写入任务获得并发锁后，必须重新获取远端 main 最新提交。
- 写入任务必须基于锁内读取的最新分支状态执行。
- 推送前再次确认远端状态未被外部提交改变。
- dry-run 或 daily-update 运行期间如果 main HEAD 发生变化，本次结果基于旧代码/配置，必须中止并重新运行。
- candidate-publish 可以基于最新 main 创建正式提交，但必须重新完整核对 Candidate 祖先关系、核心路径一致性和正式四文件基准。
- 远端变化导致当前提交过期时，不得强制覆盖。
- 所有推送均为非强制快进推送。
- Candidate 提交的文件差异必须严格只有三个 Candidate 文件。
- 正式发布提交的文件差异必须严格只有四个正式文件。

11.3.4 GitHub 权限

- 只读测试任务使用 "contents: read"。
- dry-run、candidate-publish、daily-update 和元数据写入任务必须显式声明 "permissions: contents: write"。
- 由于阻断持久化机制依赖专用 GitHub Issue，所有具备相应写入职责的工作流必须同时声明 "issues: write"。
- 仓库 Settings → Actions → General 中必须允许工作流使用所需写权限。
- 默认分支 main 必须允许受控的 GitHub Actions 提交；如果分支保护规则禁止该自动提交，必须先调整规则，否则不得宣称发布流程已验证。
- 需要读取历史 Candidate commit 和比较历史配置时，actions/checkout 必须使用 "fetch-depth: 0"。
- 第三方 Actions 固定完整 commit SHA。

---

12. 测试与质量控制

12.1 测试分层

- tests/unit/：单元测试。
- tests/integration/：Fixture 集成测试。
- tests/acceptance/：真实 GitHub Runner 程序技术探测和发布流程验收。
- 国内第二层和第三层若未实际执行，必须保持 unverified，不得伪装成验收通过。

12.2 单元测试

不联网，必须覆盖：

- manual.txt 读取、空行忽略、全注释文件处理和异常容错。
- M3U/TXT 来源格式自动识别和解析。
- sources.json、全球频道库和筛选配置 Schema 校验。
- 来源优先级和来源名额分配。
- 人工单条不占40个来源名额，但受1000候选限制。
- 单来源100条、总候选1000条截断。
- 来源无有效候选时不占来源名额。
- channels.txt 模式切换和精确匹配。
- 人工目标跨国家和地区混合选择。
- 任一目标无法匹配时整体启动失败。
- 重复目标仅保留首次。
- 默认 CN/HK/MO/TW 范围。
- CCTV-5 与 CCTV-5+ 不得误判。
- tvg-id 匹配失败必须直接丢弃，不得退回别名匹配。
- alias 冲突、重复身份和频道字典完整性。
- GlobalIdentityInvariantError 和错误代码。
- selected_country_name_conflict_keys 非0时致命中断。
- URL 规范化、Query 完整保留、默认端口和 fragment 处理。
- URL 全局去重和跨频道冲突处理。
- stable、single_pass、unstable、invalid 状态组合。
- 验证等级排序。
- 队列超时和验证超时区别。
- M3U/TXT RFC 4180 字段转义。
- M3U/TXT 双格式一致性。
- 空订阅阻断。
- 50%骤降保护、恰好50%边界、配置变更豁免和 --force 边界。
- Candidate 三 SHA 参数校验。
- Candidate 四文件基准校验。
- Candidate source commit 核心路径比较。
- publish_blocked 不得被 --force 绕过。
- RunReport 和 PublishManifest 字段空值处理。
- 日志中的 URL userinfo 和 Query 值脱敏。
- TS 技术探测不得被标记为国内播放成功。

12.3 集成测试

使用本地 Fixture，必须覆盖：

- DNS、IPv4 白名单和非全球地址拒绝。
- DNS Rebinding 防范。
- 实际网络连接器 peer IP。
- HTTP Host。
- HTTPS SNI。
- 正确证书、错误证书和域名不匹配证书。
- 系统代理环境变量不能绕过安全检查。
- 每次重定向重新执行完整安全检查。
- HTTPS 降级到 HTTP 被拒绝。
- 来源下载20秒超时和8MB解压后大小限制。
- 缺少 Content-Length 时的分块读取限制。
- gzip 解压后的真实字节计数。
- HLS 主清单、子清单和分片请求。
- 最多2个 Variant。
- 每个媒体播放列表最多1个分片。
- HLS 子清单最多一层。
- EXT-X-SESSION-KEY 拒绝。
- EXT-X-KEY METHOD 判定。
- EXT-X-MAP 拒绝。
- EXT-X-BYTERANGE 拒绝。
- 相对 URI 正确解析。
- HLS 子请求安全校验。
- 8秒候选绝对 deadline。
- 两次短验证共用8秒。
- 60秒队列等待上限。
- 全局20、单主机5、等待队列60。
- 调度器不因单主机并发阻塞全局空闲工作位。
- queue_wait_timeout 正确触发和记录。
- 1000候选压力场景。
- Candidate 精确 commit 提取。
- git show 读取旧提交且不改变工作区。
- Candidate 基准变化时阻断。
- dry-run 与正式发布提交边界。
- 并发互斥和重复任务去重。
- 推送状态不明确时的远端核对。
- 定时任务漏运行识别和补偿。
- 普通手动更新不受 target_slot 重复判断影响。
- Raw 检查状态分类。
- 双重持久化阻断及人工解除。
- verify-release 不属于首版模式。

必须全绿，阻断发布。

12.4 验收测试

真实联网测试允许外部来源失败，但必须记录原因写入 RunReport。

验收结果必须区分：

1. GitHub Runner 第一层程序技术探测。
2. Runner 内部 GitHub Raw 程序侧连通性检查。
3. 国内订阅文件分发。
4. 国内媒体网络可达性。
5. 实际设备播放反馈。

没有实际执行的层次必须标记 unverified。

12.5 正式发布门槛

必须满足：

- 单元、集成、安全测试全绿。
- 配置及 Schema 校验通过。
- 第一层程序技术探测通过。
- M3U/TXT 双格式一致。
- Candidate 或 daily-update 的发布保护全部通过。
- 空订阅和质量骤降保护通过。
- Candidate 首发或关键变更时，三个预期 SHA 分别校验一致。
- 正式四文件在同一个提交中更新。
- 统一并发保护和远端状态核对通过。
- 不存在 publish_blocked=true。

国内第二层和第三层没有真实验证证据时保持 unverified，不阻断首发或日常更新。

---

13. 统一退出码

- 0：成功。
- 1：配置或输入错误，包括配置 Schema 错误、频道字典错误、全局身份不变量错误、Candidate SHA 参数缺失或格式错误、Candidate SHA 比对不一致。
- 2：阶段不可恢复错误，包括依赖环境失败、程序内部不可恢复错误、来源获取阶段完全无法形成候选等。
- 3：正式发布保护或发布失败，包括空订阅阻断、质量骤降阻断、关键变更未走 Candidate、Candidate 基准过期、发布被明确拒绝、publish_blocked 阻断。
- 4：发布状态无法确认，包括推送响应不明确且无法通过远端核对确定是否成功、持久化阻断建立失败或启动门禁状态不明。

优先规则：

1. 输入或配置无效，返回1。
2. 处理阶段不可恢复且尚未进入发布状态，返回2。
3. 发布门槛明确不通过或推送明确失败，返回3。
4. 远端是否接受提交无法确认，返回4。
5. 不得将远端状态不明误报为普通成功或普通失败。
6. 第10.8节特殊退出码规则优先于本章一般规则。

---

14. 统一错误类型

错误类别：

- ConfigError
- SourceError
- NetworkError
- ValidationError
- FormatError
- PublishError
- InvalidIdentityError
- AmbiguousIdentityError
- GlobalIdentityInvariantError

错误记录必须包含：

- error_type
- error_code
- identifier
- stage
- reason
- retryable
- affects_publish
- occurred_at

必要错误代码包括：

- source_fetch_timeout
- source_size_limit
- source_parse_error
- channel_identity_mismatch
- cross_channel_url_conflict
- invalid_ipv4
- dns_rebinding_blocked
- redirect_limit_exceeded
- https_downgrade_blocked
- queue_wait_timeout
- candidate_deadline_exceeded
- hls_encryption_not_supported
- fmp4_not_supported
- byterange_not_supported
- ts_sync_not_found
- candidate_sha_mismatch
- candidate_baseline_stale
- remote_state_unknown
- raw_content_mismatch
- raw_content_mismatch_detected_on_startup
- GLOBAL_IDENTITY_INVARIANT_VIOLATION

来源或候选失败可以跳过，但必须记录原因，不得静默跳过。

结构化错误不得包含凭据、URL 敏感参数值或其他敏感信息。

---

15. 运行报告与发布清单

15.1 RunReport

包含：

- run_id
- 开始和结束时间
- 版本
- 模式
- 当前运行源代码 commit SHA
- Candidate commit SHA
- Candidate source commit SHA
- 正式 M3U/TXT SHA
- 来源统计
- 候选统计
- 各验证等级统计
- queue_wait_timeout 统计
- 并发和队列峰值
- 结构化错误列表
- 发布状态
- program_connectivity
- 验收层次：
  - candidate_layer2_status
  - 正式 layer2_status
  - layer3_status
  - test_error
- 是否发现定时任务漏运行
- 漏运行日期范围
- 是否执行补偿
- 补偿运行结果
- 本次补偿的 target_slot
- 是否使用 --force
- --force 绕过的具体门槛
- selection_mode
- default_regions
- preflight_result
- dropped_by_scope_count
- selected_country_name_conflict_keys
- global_catalog_version_sha
- 来源停止原因
- program_connectivity 状态

SHA 字段定义：

- run_commit_sha：本次运行所使用的代码和配置提交。
- candidate_commit_sha：包含 Candidate 三文件的 Git 提交；没有 Candidate 时为 null。
- candidate_source_commit_sha：生成 Candidate 所使用的代码和配置提交；没有 Candidate 时为 null。
- formal_m3u_sha256 和 formal_txt_sha256：正式订阅内容 SHA。

RunReport 保存为 GitHub Actions Artifact，保留30天。

Artifact 上传步骤必须尽可能使用 "if: always()"，保证运行开始后即使测试或发布失败，也能保存报告。任务在进入 Runner 前就被并发队列取消时，不保证存在 RunReport。

RunReport 必须通过 Schema 校验。

15.2 PublishManifest

统计口径：

- 频道数：M3U 中不同 tvg-id 的数量。
- 线路数：M3U 中 URL 总数。

必须记录：

- Schema 版本。
- 生成时间。
- 本次正式发布使用的 source_commit_sha。
- Candidate 发布时的 candidate_commit_sha；daily-update 时必须为 null。
- 三份其他正式文件的路径、大小和 SHA-256：
  - iptv.m3u
  - iptv.txt
  - subscription_info.json
- 本次频道总数和线路总数。
- 上次频道数和线路数；首次发布时为 null。
- last_successful_daily_update_at。
- last_successful_daily_target_slot。
- publish_blocked。
- publish_block_reason。
- layer1、layer2、layer3 状态。
- program_connectivity。

关键定义：

1. source_commit_sha 是生成当前正式订阅时所使用的源代码和配置提交，不是包含 PublishManifest 的正式发布提交。
2. 该字段用于后续判断关键代码和配置是否发生变化。
3. Candidate 发布时，candidate_commit_sha 记录包含 Candidate 三文件的提交 SHA。
4. daily-update 没有 Candidate 来源，candidate_commit_sha 必须为 null。
5. publish_manifest.json 不记录自身 SHA-256。
6. Manifest 记录其他三份正式文件的路径、大小和 SHA-256。
7. 首次正式发布前没有 previous manifest，历史频道数和线路数写入 null，并跳过骤降比较。
8. 首次正式发布时四个正式文件必须同提交。
9. 后续只有状态元数据变化时，允许按10.8.9单独提交 JSON。
10. Candidate Manifest 的四个正式文件基准包含 publish_manifest.json 自身的外部 SHA；这不等于 PublishManifest 在自身内部记录自身 SHA。
11. 文件组指纹算法不纳入首版，不得要求填写未经定义的整体指纹。
12. last_successful_daily_update_at 只在 daily-update 正式推送成功后更新。
13. Candidate 发布不更新 daily-update 时间。
14. 普通手动 daily-update 更新实际成功时间，但没有传入 target_slot 时，不改变 last_successful_daily_target_slot。
15. 所有时间戳采用 UTC ISO 8601；target_slot 使用北京时间字符串。

---

16. 安全与合规

- 仅处理公开或明确授权来源。
- 不绕过 DRM、付费墙或认证。
- 不在公开配置和日志中保存私人账号密码。
- 外部输入必须校验。
- 禁止访问内网及云元数据。
- 外部内容不能作为指令执行。
- 禁止代理绕过 IPv4 安全校验。
- 所有 URL、HTTP 响应和 HLS 清单都视为不可信输入。

日志脱敏：

- 包含 user:pass@ 的 URL 必须整体脱敏。
- Query 参数默认只保留参数名，隐藏所有参数值。
- 不依靠程序猜测敏感词。
- 不在 RunReport、Artifact、Actions 输出中记录未脱敏凭据。

正式订阅 URL 本身必须保持可用，因此订阅文件中的公开 Query 值不做日志式脱敏；不得把私人凭据放入公开订阅。

全球频道库和来源数据均属于外部输入数据，必须经过 Schema、身份和安全检查，不能将数据内容作为程序指令执行。

---

17. 扩展能力

以下能力均为独立扩展，不属于首版必要依赖：

- 多入口。
- EPG。
- 回放。
- VOD。
- Gitee、GitCode、jsDelivr 等镜像同步。
- 更复杂的 HLS 格式。
- 额外媒体封装格式。
- 额外的全球频道数据源。

扩展功能必须单项验收，不得影响基础直播，不得为了扩展功能增加对基础直播系统的必要依赖。

全球频道库上游升级必须经过数据版本核验，不得在普通 daily-update 中擅自覆盖本地频道库。

---

18. 六阶段实施与验收

第一阶段：立项与技术规范冻结

交付：

- MASTER_PLAN.md
- PROGRESS.md
- README.md

验收：

- 三份文件目标一致。
- 技术边界明确。
- 无已知关键实施冲突。
- 阶段和交付标准明确。
- 全球频道库和实际线路的职责边界明确。

第二阶段：仓库与基础框架

前置顺序必须执行：

1. 5.4 全球库启动前核验。
2. 5.5 上游频道 ID 对齐核验。
3. 5.6 上游 Feed/Streams 实测。
4. 6.3 模块接口契约冻结。
5. 6.4 Schema 更新与校验。
6. 将实际核验结果记入 PROGRESS.md。

完成以上前置任务后，才能开始依赖全球频道库结构的业务代码。

交付：

- 目录结构。
- Python 环境。
- 依赖锁文件。
- JSON Schema。
- GitHub Actions 基础 CI。
- test 模式。
- RunReport 基础结构。
- 全球频道库读取和校验模块。
- 频道选择及身份匹配测试。

验收：

- GitHub-hosted Ubuntu 环境运行成功。
- Python 和依赖版本锁定。
- Ruff、pytest 全绿。
- 所有配置 Schema 通过。
- 全球频道库身份检查通过。
- 两种频道选择模式通过测试。
- 测试工作流不修改正式文件。

第三阶段：核心直播系统

交付：

- 来源采集。
- M3U/TXT 解析。
- 频道身份匹配。
- 统一网络层。
- IPv4 安全检查。
- TS/HLS 媒体验证。
- 候选调度。
- 线路选择。

验收：

- 网络安全集成测试通过。
- HLS 首版支持边界测试通过。
- 1000候选受控压力测试通过。
- 状态判定和排序符合规范。
- 不产生未验证或虚假标记。

第四阶段：订阅生成与首发

交付：

- M3U/TXT 生成。
- subscription_info。
- Candidate 三文件。
- Candidate SHA 校验。
- Candidate 精确 commit 提取。
- 正式四文件发布。
- GitHub Raw 正式地址。

验收：

- M3U/TXT 内容一致。
- Candidate 与正式文件字节级一致。
- Candidate 三 SHA 校验通过。
- 正式四文件同一个提交。
- 空订阅、骤降和发布保护通过。
- 首发不依赖国内真实网络测试。

第五阶段：自动化与稳定性

交付：

- 北京时间06:17定时更新。
- 手动 test、dry-run、candidate-publish、daily-update。
- 漏运行识别和补偿。
- 并发保护。
- RunReport Artifact。
- 推送失败和远端状态核对。
- Raw 程序侧检查。
- 发布阻断和人工解除流程。
- 双重阻断持久化机制及启动门禁。

验收：

- 定时和手动流程正确。
- 写入任务统一并发组。
- 不覆盖上一份成功订阅。
- 失败和状态不明按退出码处理。
- RunReport 完整。
- 平台并发能力和实际限制有真实核验记录。

第六阶段：扩展能力

按实际需要逐项评估和验收。不得影响基础直播系统。

---

19. 开发与协作纪律

1. 最高执行令：必须严格遵守 MASTER_PLAN.md 总流程，以 PROGRESS.md 记录为依据推进开发，不得擅自跳过阶段。
2. 以本文档为总施工依据。
3. 修改前检查仓库真实状态。
4. 提供完整文件，不以零散补丁让初学者自行拼接。
5. 标明实现与验证状态，明确处于哪一层。
6. 未跑过的测试不得标为通过。
7. 每阶段完成后更新 PROGRESS.md。
8. 不得绕过阶段验收。
9. 四个正式文件必须在同一个 Git 提交中生成；后续允许按10.8.9单独提交状态元数据。
10. 首发及关键变更时，必须经过 Candidate 和 SHA 校验，不得用未经校验的文件覆盖正式订阅。
11. 对总规范未明确的技术问题，必须先调查、验证并记录依据，不得擅自选择未经验证的方案。
12. 对已经确定的参数和项目边界，未经证据和明确决策，不得随意修改。
13. 修改规范时必须检查 MASTER_PLAN.md、PROGRESS.md 和 README.md 的一致性。
14. 不得将计划、设计或理论可行性描述成已经实现。
15. 发现问题时先判断属于确定错误、缺少定义、待技术验证还是优化建议，再决定是否修改。
16. 不得为了增加模块、文件数量或技术复杂度而拆分功能。
17. README 与 MASTER_PLAN 的目标和验证边界必须保持一致。不得宣传第三层未验证的线路为“国内已可播放”。
18. 不得把国内真实测试环境作为开发启动条件或首发阻断条件。
19. 不得因为 Runner 内部 Raw 检查通过，就宣称国内订阅或媒体可达性通过。
20. 未经用户明确授权，不得声称已经直接修改用户 GitHub 仓库；交付代码时提供完整文件供用户审阅和上传。
21. 修改或提交前先说明拟使用的 commit message，再提供完整文件。
22. 不得为了追求理论上的绝对完美而无限增加首版范围；只处理真实错误、关键缺口和必要边界。
23. 不得要求用户重复上传仓库中已经提交且可以读取的数据文件。
24. 不得重新讨论已经确定的频道选择方案。
25. 不得擅自恢复已废弃的旧频道配置文件或第二套频道库。
26. PROGRESS.md 只记录实际进度、证据、测试结果和下一步，不得代替 MASTER_PLAN.md 定义技术规则。

---

20. 最终交付标准

最终系统必须能够：

1. 自动获取登记的公开或授权来源。
2. 使用全球频道库识别频道身份。
3. 根据 channels.txt 选择用户需要的频道；空文件时按默认范围筛选。
4. 只连接经过校验的全球可路由公网 IPv4。
5. 按首版 TS/HLS 规则执行媒体技术探测。
6. 依据验证等级和来源优先级筛选线路。
7. 每个频道最多保留三条线路。
8. 持续生成 M3U 和 TXT。
9. 通过 Candidate、SHA、质量保护和 Git 提交边界安全发布。
10. 按北京时间06:17自动更新。
11. 保留完整运行报告、发布清单和错误记录。
12. 正式发布失败时保护上一份成功订阅。
13. 明确区分第一层程序技术探测、国内订阅分发、国内媒体可达性和实际设备播放反馈。

最终交付的不是一套仅仅能够运行、显示绿色状态的程序，而是一套能够持续采集、识别、验证、筛选、发布和追溯 IPTV 直播源的自动化系统。

任何没有真实证据的国内网络可达性结论，都必须保持 unverified。不得将程序技术探测包装成国内实际播放成功。

---

附录A：首版技术参考

以下资料用于开发实施时核对协议和平台行为，不代表本项目已经完成相应代码测试：

- HLS RFC 8216：https://www.rfc-editor.org/rfc/rfc8216.html
- aiohttp Client Reference：https://docs.aiohttp.org/en/stable/client_reference.html
- Python ipaddress：https://docs.python.org/3/library/ipaddress.html
- GitHub Actions concurrency：https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
- GitHub Actions workflow syntax：https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- actions/checkout：https://github.com/actions/checkout
- iptv-org 公共频道列表：https://github.com/iptv-org/iptv
- iptv-org 频道数据库：https://github.com/iptv-org/database
- Guovin/iptv-api（多来源聚合和 IPv4 过滤实现参考，不直接复制其架构或代码）：https://github.com/Guovin/iptv-api
