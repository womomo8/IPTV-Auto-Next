IPTV-Auto-Next MASTER_PLAN.md

版本：1.18
文件性质：项目总施工规范
适用范围：整个项目的架构设计、开发实施、测试验收和正式发布

本版本在 1.17 基础上，调整频道字典范围、频道搜索模式、上游 Feed 关联和候选分配规则。除本次明确调整的频道搜索相关内容及其必要的数据模型、报告、测试和验收要求外，原有项目目标、技术参数、安全边界、发布保护和阶段顺序均保持不变。

---

1. 项目目标

1.1 核心目标

建设一个高效率、自动化运行的 IPv4 IPTV 直播源仓库。

系统持续收集直播源，执行统一的程序技术探测，筛选并发布符合首版技术支持范围的 IPv4 直播线路，同时如实记录国内网络验证状态。

系统必须实现：

1. 自动收集公开或明确授权的直播源。
2. 识别和整理频道信息。
3. 根据频道所属国家或地区，获取对应的公开频道 Feed。
4. 检测 IPv4 地址及网络连接。
5. 验证直播媒体是否符合首版支持的技术要求。
6. 每个频道最多保留三条线路。
7. 自动生成 M3U 和 TXT 订阅。
8. 按计划持续更新订阅文件。
9. 正式发布失败时保护上一份成功订阅。
10. 保留运行报告、文件 SHA 和发布记录，保证结果可追溯。

1.2 基本原则

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
13. 暂时没有真实国内验证证据时，必须标记为 unverified，不得虚构验证结论，也不得因此阻断项目开发和正常发布。
14. 本项目不绑定任何特定播放器。输出订阅必须保持通用标准格式。
15. 频道搜索范围由 "channels.txt" 的内容决定。空清单使用固定的 CN、HK、MO、TW 默认搜索范围；非空清单只搜索用户指定频道。
16. 默认搜索范围不是全球扫描。用户指定全球任意频道时，也只获取这些频道所属国家的 Feed，不扫描无关国家。

1.3 验收层次与责任边界

1. 第一层：程序技术探测
   
   - 发生在 GitHub Runner 内部。
   - 验证内容：来源和频道格式正确、目标为全球可路由 IPv4、网络安全检查通过、TS/HLS 结构符合首版支持范围。
   - 结论含义：程序完成了规定的技术探测。
   - 此层是系统必须负责并通过自动化测试保障的强制门槛。
   - 此层结果不代表中国大陆网络能够访问媒体内容，也不代表播放器能够正常播放。

2. 第二层：国内网络订阅分发
   
   - 验证对象：正式 GitHub Raw 订阅地址。
   - 验证内容：国内真实网络能否成功拉取订阅文件、格式是否正确、频道身份和线路对应关系是否正常。
   - 结论含义：国内订阅分发链路正常。
   - 此层不代表订阅中的媒体线路在国内网络可达。
   - 首版默认状态为 unverified；只有存在真实国内网络测试证据时，才允许记录为 passed 或 failed。
   - 此层不属于首发或日常自动更新的强制门槛。

3. 第三层：国内媒体网络可达性验证
   
   - 验证对象：媒体地址及必要的 HLS 媒体分片。
   - 验证内容：这些媒体请求能否在中国大陆真实网络中成功取得。
   - 结论含义：国内网络媒体可达性，不等同于完整播放器播放成功。
   - 首版默认状态为 unverified；没有国内真实请求证据时不得填写 passed。
   - 此层不属于首发或日常自动更新的强制门槛。

4. 第四层：用户实际设备播放反馈
   
   - 发生在真实设备和真实播放器。
   - 结论含义：实际设备播放情况。
   - 此层作为外部使用反馈，不将任何具体播放器纳入项目强制验收。
   - 不得因为某个播放器的兼容性问题，擅自改变标准订阅格式或绑定特定播放器。

---

2. 项目实施阶段

项目分为六个阶段，必须依次实施和验收。

第一阶段：立项与技术规范冻结
第二阶段：仓库与基础框架
第三阶段：核心直播系统
第四阶段：订阅生成与首发
第五阶段：自动化与稳定性
第六阶段：扩展能力

不得跳过阶段验收。后续阶段发现前序阶段缺陷时，先修复并重新验收，不得以临时绕过代替修复。

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

Python 版本与依赖验证规则：

1. Python 库验证：验证 aiohttp、pytest 能够成功安装和导入，并能运行基础异步单元测试。
2. 命令行工具验证：验证 Ruff 和 uv 能够成功安装，且命令行执行正常。
3. 全部通过：保留 Python 3.14。
4. 如果安装或运行失败：记录完整报错并排查。确认短期无法解决后，才允许评估 Python 3.13 最新补丁版。回退必须附带排查证据并记录在 "PROGRESS.md"。
5. 必须在 GitHub-hosted Ubuntu 环境实际验证：
   - Python 版本与 ".python-version" 一致；
   - aiohttp、pytest 安装和导入成功；
   - asyncio 基础功能正常；
   - Ruff、uv 正常；
   - 依赖锁文件存在且有效；
   - "uv lock --check" 通过；
   - "uv sync --locked" 通过；
   - Ruff 检查通过；
   - pytest 全部通过。
6. 不得仅凭本地电脑运行成功就认定 GitHub Runner 环境验证通过。

3.2 核心技术

- Python / asyncio / aiohttp
- dataclasses / JSON Schema 2020-12
- pytest / Ruff / uv / GitHub Actions

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
- Schema 校验失败不得静默忽略。

---

4. 项目目录结构

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
├── schemas/
│   ├── sources.schema.json
│   ├── channels.schema.json
│   ├── run_report.schema.json
│   ├── publish_manifest.schema.json
│   ├── candidate_manifest.schema.json
│   └── subscription_info.schema.json
├── config/
│   ├── sources.json
│   ├── channels.txt
│   └── channels.json
├── src/
│   └── iptv_auto_next/
│       ├── main.py
│       ├── config.py
│       ├── models.py
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

目录职责说明：

- "output/candidate/"：存放待人工审阅的 Candidate 文件。它不是正式订阅，不得覆盖正式文件。Candidate 的用途是让用户审阅内容并确认准确 SHA 后，再手动触发正式发布；不要求进行国内网络实测。
- "output/" 根目录：仅存放正式发布的成品和清单。
- "tests/unit/"：不联网的单元测试。
- "tests/integration/"：使用本地受控 Fixture 的集成测试。
- "tests/acceptance/"：程序技术探测和发布流程验收测试。

不得为了拆分模块而增加没有必要的文件。

---

5. 配置管理

5.1 来源配置、来源入口和候选截断规则

5.1.1 sources.json 结构

"config/sources.json" 必须采用以下固定结构：

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
      "id": "public-index-iptv-org",
      "url": "https://example.com/discovery.m3u",
      "enabled": true
    }
  ]
}

以上是字段结构示例。"example.com" 只用于说明格式，不得作为实际来源启用。实际公开频道 Feed 按 5.1.8 的规则获取，不再将 "countries/cn.m3u" 当作频道所属国家的 raw Feed 使用。

配置结构约束：

- "manual_single"、"carriers"、"discovery" 三个数组必须存在；允许为空数组。
- 每个 "manual_single" 对象必须包含唯一 id、有效 "tvg_id" 和 URL。
- 每个 "carriers"、"discovery" 对象必须包含唯一 id、URL 和布尔值 "enabled"。
- 三类来源的 id 在整个 "sources.json" 中必须全局唯一。
- URL 必须是绝对 HTTP/HTTPS URL，不得包含 userinfo，不得含 CR、LF 或控制字符。
- "enabled=false" 的来源不下载、不占来源名额。
- 三个数组即使没有内容也必须保留，不能用 null 或省略字段代替空数组。
- "sources.schema.json" 必须严格校验上述结构，禁止未知字段静默进入运行配置。

"channels.json" 的目标结构：

{
  "source_revision": {
    "repository": "iptv-org/database",
    "commit": "固定的上游提交版本",
    "content_hash": "固定的数据内容哈希"
  },
  "channels": [
    {
      "tvg_id": "CCTV5.cn",
      "canonical_name": "CCTV-5",
      "aliases": ["CCTV5", "中央五套"],
      "country": "CN",
      "feeds": [
        {
          "feed_id": "示例 Feed ID",
          "broadcast_area": ["c/CN"]
        }
      ]
    }
  ]
}

以上为目标数据结构示意，不是要求用户手工编辑的配置语法。实际字段必须由项目维护，并在实施阶段落实 Schema。

约束：

1. "channels" 必须为非空数组。
2. 每个频道必须包含非空 "tvg_id"、非空 "canonical_name"、"aliases" 数组和有效 "country"。
3. "feeds" 保存与该频道关联的上游 Feed 标识及必要的广播区域信息。
4. "source_revision" 用于记录频道和 Feed 数据所依据的上游固定版本。
5. "channels.schema.json" 必须在对应实施阶段更新，以支持 "country"、"feeds" 和 "source_revision"。
6. 当前旧 Schema 不支持上述字段，因此在 Schema 更新前，不得声称新频道字典已经完成 Schema 验证。
7. "channels.json" 是项目维护的标准频道字典，不由用户逐条编辑，也不得在每次运行时自动覆盖。

5.1.2 来源定义和优先级

来源类型：

- "manual_single"：人工指定的单条线路。必须填写 "tvg_id" 和完整 URL。
- "manual.txt"：人工订阅来源。每一行是一个独立订阅来源。
- "carriers"：运营商或其他明确来源的订阅目录。
- "discovery"：预先登记的公开或授权目录源。
- "regional_feed"：根据目标频道所属国家，从 iptv-org raw 国家 Feed 获取的候选来源。该来源由频道字典和搜索模式决定，不要求用户在 "channels.txt" 中填写 Feed URL。

来源优先级严格如下：

1. 人工单条：按 "sources.json" 中数组顺序。
2. 人工订阅：按 "manual.txt" 有效 URL 的行顺序。
3. 运营商来源：按 "sources.json" 中 "carriers" 数组顺序。
4. 自动发现及地区 raw Feed：按确定的来源顺序处理；同类内部不得按名称、URL 或网络速度擅自重排。

地区 raw Feed 属于自动发现来源类别，但具有独立的采集和候选上限规则，见 5.1.8 和 5.1.9。

5.1.3 来源名额和候选上限

首版限制保持不变：

- 总来源名额：40。
- 普通订阅来源最多接收：100 条有效候选。
- 总候选池：1000 条。
- 人工单条不占用40个来源名额，也不受单来源100条限制，但受总候选1000条限制。

名额计算规则：

1. 人工单条优先解析并进入候选池，不占40个来源名额。
2. "manual.txt" 每个有效 URL 视为一个独立来源。
3. 人工订阅、运营商来源、自动发现来源及地区 raw Feed 共用40个来源名额。
4. 一个来源只有在至少产生一条通过频道身份识别、目标频道过滤和 URL 去重的有效候选后，才占用一个来源名额。
5. 来源下载失败、格式不支持、解析失败、没有匹配频道或所有条目均被去重的来源，不占来源名额。
6. 来源名额按5.1.2规定的优先级顺序分配；累计达到40个有效来源后，停止接收后续订阅来源。
7. 普通订阅来源最多接收前100条有效且未重复的候选。达到100条后，该来源后续条目不再进入候选池。
8. 地区 raw Feed 不受普通来源单源100条限制，但仍受总来源40和总候选1000条限制。
9. 候选池达到1000条后，立即停止接收后续候选和来源。
10. 所有名额和截断行为必须写入 RunReport，包括来源总数、成功来源数、来源失败数、单来源截断数、地区 Feed 统计和候选池截断数。

5.1.4 解析、过滤和去重顺序

统一执行以下顺序：

1. 根据 "channels.txt" 判定搜索模式和目标频道集合。
2. 按来源优先级及目标国家确定需要获取的来源。
3. 下载来源内容。
4. 解析 M3U 或 TXT 条目。
5. 校验条目 URL 的基本格式和协议。
6. 识别频道身份，并验证必要的 Feed 关联。
7. 执行目标频道过滤。所有来源都必须经过该过滤，包括人工单条、人工订阅、运营商、普通自动发现和地区 raw Feed。
8. 生成规范化 URL。
9. 对规范化 URL 做全局去重，保留优先级最高、原始顺序最靠前的第一条。
10. 普通订阅来源应用单来源100条限制；地区 raw Feed 不应用该单源限制。
11. 对地区 raw Feed 候选执行按频道公平分配。
12. 应用总候选1000条限制。
13. 将唯一候选提交验证调度器。

同一 URL 在不同来源重复出现时，只验证一次，并保留优先级最高的第一条来源身份。若同一 URL 被不同频道身份声明，按优先级保留第一条并记录 "cross_channel_url_conflict"，后续冲突条目丢弃，不得把同一 URL 同时输出为多个频道。

最终线路选择阶段不得再次改变 URL 去重归属；只能执行唯一性断言，发现重复属于程序错误。

5.1.5 人工订阅入口 manual.txt

- 仓库根目录使用 "manual.txt"。
- UTF-8 纯文本，每行一个完整 HTTP/HTTPS 订阅地址。
- 空行忽略，首尾空白去除。
- 不修改 URL 的路径和查询参数内容。
- 每行作为一个独立人工订阅来源。
- 下载内容按实际内容自动识别 M3U 或 TXT，不依赖 URL 后缀。
- 下载内容必须先经过网络安全检查、超时和大小限制，再解析。
- M3U：以 "#EXTM3U" 或有效 "#EXTINF" 记录识别；每个 "#EXTINF" 对应其后第一个非空、非注释 URL 行；缺少 URL 的条目记为解析失败。
- TXT：按 RFC 4180 CSV 规则逐行解析，每条有效记录必须恰好包含两个字段：频道名称、URL；字段数量不为2的记录记为解析失败。
- 来源文件允许 UTF-8 BOM 和 CRLF 输入；解析时统一处理，但正式输出仍必须无 BOM、LF。
- 如果内容既不能识别为 M3U，也不能按上述规则解析为 TXT，则判定格式不支持。
- 不得把完整 M3U/TXT 订阅文件当作单条媒体线路。
- 单个来源失败或无法解析时，记录原因并跳过，不得中断其他来源。
- 人工订阅中的频道仍必须通过标准频道字典识别，并接受当前搜索模式的目标频道过滤，不得绕过频道范围限制。

5.1.6 来源下载边界

来源订阅下载与候选媒体验证使用不同的超时预算：

- 单个来源下载总超时：20秒，包含 DNS、连接、重定向和内容读取。
- 单个来源下载内容上限：解压后8MB。
- 重定向最多5跳。
- HTTP 状态必须为200；其他状态记录失败原因并跳过。
- 必须流式读取并累计解压后字节数，不得只依赖 Content-Length。
- 超过8MB立即中止。
- 不进行额外重试。
- 所有来源下载必须通过 "network.py"。
- 四个默认地区 Feed 必须分别获取、分别记录结果。一个地区获取失败，不得中止其他地区 Feed 的获取。
- 多个目标频道属于同一国家时，该国家 raw Feed 在一次运行中只下载一次。

5.1.7 频道字典和上游数据维护

"config/channels.json" 是项目自己的标准频道字典，不在每次运行时动态改变。

频道字典以 "iptv-org/database" 的频道和 Feed 数据为基础，采用受控版本更新：

- 上游频道 "id" 映射为本项目标准 "tvg_id"。
- 上游频道 "name" 映射为 "canonical_name"。
- 上游频道 "alt_names" 映射为 "aliases"。
- 上游频道 "country" 映射为频道所属国家代码。
- 上游 Feed 表中的 "channel" 和 "id" 用于建立频道与 Feed 的精确关联。
- Feed 的 "broadcast_area" 作为 Feed 属性保留，但不得用它替代频道 "country" 决定默认频道搜索范围。
- 频道和 Feed 数据必须记录固定上游 commit 或等效版本标识及内容哈希。
- 上游数据更新必须经过项目变更、冲突检查、Schema 检查和测试，不得在运行时自动覆盖。
- 不新增独立 Feed 数据文件作为必要依赖；频道与 Feed 的关联数据保存在项目维护的频道字典中。
- 用户只需要编辑 "config/channels.txt"。频道字典、国家字段和 Feed 关联由项目维护。

频道字典必须支持全球频道，而不是只包含 CN。用户指定全球频道时，必须能够从字典查到频道的国家代码和必要 Feed 关联。

5.1.8 频道搜索模式和地区 Feed

系统根据 "config/channels.txt" 的有效内容，确定唯一搜索模式。

模式一：默认地区搜索（default_regions）

满足以下任一条件时进入：

- "channels.txt" 文件为空；
- 文件只有空白字符；
- 文件只有空行；
- 文件只有注释行。

默认目标地区固定为：

- CN：中国大陆
- HK：中国香港
- MO：中国澳门
- TW：中国台湾

此模式不是停止搜索，也不是全球扫描。系统必须搜索上述四个地区的标准频道字典条目，并获取对应地区的 raw Feed。

默认地区 Feed URL：

- CN："https://iptv-org.github.io/iptv/raw/cn.m3u"
- HK："https://iptv-org.github.io/iptv/raw/hk.m3u"
- MO："https://iptv-org.github.io/iptv/raw/mo.m3u"
- TW："https://iptv-org.github.io/iptv/raw/tw.m3u"

四个 Feed 必须独立获取和处理：

1. 一个地区 Feed 下载失败、超时、格式错误或暂时不可用，不得导致其他地区停止。
2. 每个地区分别记录下载状态、解析数量、频道匹配数量、候选数量和失败原因。
3. 某个地区失败时，其余成功地区继续处理。
4. 四个地区均没有产生可用线路时，必须明确记录结果，并触发空订阅保护；不得生成或发布空订阅，不得覆盖旧正式订阅。
5. 默认模式下，目标频道集合为频道字典中 "country" 精确等于 CN、HK、MO 或 TW 的频道。
6. 频道是否属于默认搜索范围，以频道自身 "country" 为准，不以 Feed 的 "broadcast_area" 判断。

模式二：用户指定频道搜索（user_watchlist）

当 "channels.txt" 存在至少一条有效频道内容时进入。

规则：

1. 每一条有效内容必须按既有清单语法解析为一个标准频道。
2. 支持标准 "tvg_id"、"canonical_name" 或 "alias" 的精确匹配。
3. 不额外附加 CN、HK、MO、TW 的其他频道。
4. 只搜索用户指定的频道。
5. 根据每个目标频道在 "channels.json" 中的 "country"，确定需要获取的国家 raw Feed。
6. 多个目标频道属于同一国家时，该国家 Feed 只获取一次。
7. 用户指定全球任意国家的频道时，只获取这些目标频道所属国家的 raw Feed，不得因此扫描全球所有国家。
8. 频道 country 缺失、国家代码不支持或无法确定对应 Feed 时，记录为 "unsupported" 或 "unresolved"，不得猜测国家，也不得擅自扩大搜索范围。
9. 用户指定频道的国家 Feed 获取失败时，隔离该国家的失败结果，其他国家继续处理。
10. 用户指定清单中的有效目标频道顺序不作为最终输出排序依据；最终输出仍按标准频道字典的原始数组顺序保持稳定。

地区 raw Feed 采用 "raw/{country_code}.m3u"，其含义是按频道自身 country 字段分组。

不得把 "countries/{country_code}.m3u" 当作上述 raw Feed 使用。该类列表按 Feed 的 "broadcast_area" 分组，与频道自身 country 不是同一个字段，不能混用。

地区 Feed 的获取范围必须由已经识别的目标频道集合决定。禁止因为一个频道属于某个国家，就顺带扫描其他国家。

5.1.9 地区 Feed 候选公平分配

地区 raw Feed 不应用普通单来源100条截断，否则可能使频道候选在进入总候选池前被不合理丢弃。

地区 Feed 候选必须先完成频道身份识别和目标频道过滤，再按频道进行确定性公平分配：

1. 先将候选按标准 "tvg_id" 分组。
2. 每个频道组内保留来源优先级和来源内原始顺序。
3. 第一轮每个目标频道最多取一个候选。
4. 第二轮再次按频道顺序，每个频道最多取一个候选。
5. 持续轮询，直到总候选池达到1000条，或所有频道均没有剩余候选。
6. 不得为每个频道预先设置固定配额。
7. 不得让候选数量较多的单个频道独占总候选池。
8. 轮询顺序必须确定性，不能由网络响应完成顺序决定。
9. 人工单条、人工订阅、运营商和普通 discovery 候选仍遵循既有来源优先级；整体候选处理不得破坏来源优先级和 URL 首次归属规则。
10. 公平分配后的候选统一进入原有 IPv4 和媒体验证流程。

若目标国家数量超过总来源40的上限，只能按确定性目标顺序处理可容纳的来源，并对未能获取的国家和目标频道明确记录 "source_limit_reached"。不得静默跳过，也不得突破40来源限制。

5.1.10 特殊 M3U 选项和不支持协议

- 不支持的 URL 协议必须明确标记为 "unsupported" 或 "rejected"，不得作为普通线路继续处理。
- RTMP 等首版不支持的协议直接拒绝。
- 如果某个 M3U 条目带有 "#EXTVLCOPT" 等需要播放器额外处理的特殊请求头或选项，首版不得静默忽略该选项后继续把 URL 当作普通线路。
- 该条目必须记录为不支持或格式拒绝，并隔离该条目。
- 特殊选项导致某条目失败，不得中断同一来源中的其他独立条目。
- 不得将不支持的协议或特殊请求头线路用于补足每频道三线路数量。

5.2 频道配置与精确匹配原则

采用确定性映射，严禁使用模糊匹配或子串包含匹配。CCTV-5 和 CCTV-5+ 必须保持完全独立。

5.2.1 标准频道身份

1. "config/channels.json" 是 Canonical 标准频道字典。
2. 每个标准频道必须有唯一 "tvg_id"。
3. 标准频道至少保存 "tvg_id"、"canonical_name"、"aliases"、"country" 和 Feed 关联信息。
4. 上游频道 ID 是标准身份来源，不得因名称相似而合并不同频道。
5. "country" 表示频道自身所属国家或地区，不代表线路在中国大陆可播放。

5.2.2 来源条目身份匹配

身份与匹配逻辑严格按以下规则执行：

1. 来源条目存在非空 "tvg-id" 属性时，优先按上游频道 ID 规则精确识别。
2. 如果 "tvg-id" 为 "channelID@feedID" 形式，必须拆分为频道 ID 和 Feed ID，并同时确认：
   - 频道 ID 与标准频道 "tvg_id" 完全一致；
   - 上游 Feed 表中存在对应记录；
   - 该 Feed 记录的 "channel" 必须与频道 ID 完全一致；
   - Feed 的 "id" 必须与 "@" 后缀完全一致。
3. 不得仅删除 "@" 后缀后就认定频道匹配成功。
4. 不得根据 Feed 名称、显示名称或相似字符串猜测 Feed 归属。
5. 如果来源条目存在非空 "tvg-id"，但频道 ID 或 Feed 关联不匹配，必须拒绝该条目，不得退回名称匹配。
6. 如果来源条目完全没有 "tvg-id" 属性，才允许使用显示名称进行精确匹配。
7. 如果 "tvg-id" 属性存在但为空，视为存在但无效，不得退回名称匹配。
8. 对于上游没有 "@feedID" 的普通频道 ID，只有在该 ID 与标准频道 ID 完全匹配时才可识别；不得自行补造 Feed ID。

5.2.3 名称匹配规则

只有来源条目完全缺少 "tvg-id" 时，才允许使用名称匹配。

规范化规则：

- Unicode NFKC；
- 去除首尾空白；
- 统一小写；
- 不删除内部字符；
- 不删除连字符、加号、斜杠或其他有区分意义的字符；
- 不做拼音转换；
- 不做模糊匹配；
- 不做子串包含匹配。

名称匹配必须在标准频道的 "canonical_name" 和 "aliases" 中进行完全相等匹配。

如果同一个规范化名称对应多个标准频道：

- 标记为 "ambiguous"；
- 不得任选一个频道；
- 不得把该条目作为任何一个频道的有效候选；
- 其他无歧义频道继续处理；
- 用户需要通过标准 "tvg_id" 明确指定有歧义的频道。

空或缺失 "tvg-id" 时才允许名称匹配；非空 "tvg-id" 匹配失败时绝不允许名称回退。

5.2.4 channels.txt 清单规则

用户只编辑 "config/channels.txt"。

- 每行一个频道搜索目标。
- 空行和以 "#" 开头的注释行忽略。
- 不新增 URL、国家代码、Feed ID、通配符或其他清单语法。
- 每行必须对应 "channels.json" 中一个 "tvg_id"、"canonical_name" 或 alias。
- 优先按精确 "tvg_id" 匹配；否则按规范化名称完全相等匹配。
- 同一标准频道重复出现时只保留一个目标，并记录重复项。
- 一个条目无法识别或存在歧义时，记录该条目为 "unresolved" 或 "ambiguous"，不得猜测归属。
- 清单存在语法错误、编码错误或无法解析的结构性错误时，启动时报错退出，退出码1。
- 个别频道无法识别时隔离该目标，不得因此中断其他已识别目标。
- 如果清单中所有目标均无法识别，必须阻止生成和发布。
- 有至少一个有效目标时，按 "user_watchlist" 模式执行，只搜索已识别目标，不额外附加默认四地区频道。
- 文件为空、全空白或只有注释时，按 "default_regions" 模式执行，默认搜索 CN、HK、MO、TW。

两种模式后续共用统一验证、筛选、生成及发布流程。

5.2.5 频道配置完整性

1. "tvg_id" 必须唯一且非空。
2. alias 不得产生重复或冲突映射。
3. 不同标准频道不得通过规范化规则映射为同一个身份。
4. "tvg_id"、"canonical_name" 和 alias 的查找命名空间不得产生跨频道歧义。
5. 全球频道允许存在相同名称或别名；重名时必须建立多频道映射并标记 ambiguous，不得因重复别名导致整个全球字典无法启动。
6. 有歧义的名称不得用于名称匹配；用户可以使用标准 "tvg_id" 明确区分。
7. 频道 country 必须符合标准国家代码格式。
8. Feed 关联必须能通过上游频道 ID 和 Feed ID 精确验证。
9. 配置出现重复身份、非法国家代码、错误 Feed 关联或无法确定归属的数据时，启动检查必须按错误类型处理，不得静默选择。
10. 配置检查必须有对应单元测试。

---

6. 核心数据模型

6.1 统一数据对象

系统使用以下运行时 dataclass：

- Source
- Candidate
- VerifiedLine
- Channel
- Feed
- ValidationResult
- RunReport
- PublishManifest

关键字段定义：

- Source：来源 ID、来源类型、优先级、原始顺序、来源 URL、所属国家（适用于地区 Feed）、来源获取结果。
- Candidate：候选 ID、来源 ID、频道 "tvg_id"、必要的 Feed ID、原始 URL、规范化 URL、来源内顺序。
- Channel："tvg_id"、"canonical_name"、"aliases"、"country"、Feed 关联。
- Feed：Feed ID、所属频道 ID、broadcast_area 等上游关联信息。
- ValidationResult：候选 ID、验证等级、两次验证结果、阶段耗时、错误类型和验证时间。
- VerifiedLine：候选信息、验证等级、验证时间及验证结果。
- RunReport：单次运行的完整过程和结果。
- PublishManifest：当前正式发布文件、SHA、统计数据、发布来源和状态。

频道字典的上游版本信息必须能够追溯到固定的 "source_revision"。

来源身份、线路身份、频道身份必须分开管理：

- 来源身份：线路从哪个来源取得。
- 线路身份：规范化后的媒体 URL。
- 频道身份：标准频道字典中的 "tvg_id"。
- Feed 身份：上游 Feed 表中与频道 ID 精确关联的 Feed ID。

6.2 验证等级与稳定性判定

- stable：两次短验证均通过。
- unstable：一次通过、一次失败。
- single_pass：至少一次通过，另一次因总预算耗尽而未完成。
- pending：尚未进入或完成验证的内部调度状态，不得作为最终有效线路状态。
- invalid：两次均未通过，或没有任何一次完整通过。

短验证判定：

- TS 流必须找到连续5个 "0x47" 同步字节，间隔严格为188字节。
- 禁止用单一 "valid=true" 替代实际结构检查。

两次验证执行规则：

1. 两次验证串行执行，不增加固定等待。
2. 两次完整验证共用一个8秒总预算，不是每次8秒。
3. 每次短验证均执行完整的媒体验证流程。
4. 第一次验证完整结束为通过或失败后，只要8秒总预算仍有剩余，就执行第二次。
5. 如果总预算已经耗尽，立即停止，不再启动第二次。
6. 不增加第三次验证或额外重试。

判定表：

第一次| 第二次| 最终状态| 是否有效
通过| 通过| stable| 是
通过| 失败| unstable| 是
失败| 通过| unstable| 是
通过| 未完成（总预算耗尽）| single_pass| 是
失败| 未完成（总预算耗尽）| invalid| 否
失败| 失败| invalid| 否
未完成| 未执行| invalid| 否

只有至少一次完整通过，才可进入有效线路集合。

"queue_wait_timeout" 是调度排队超时，不属于媒体验证失败，不得记为 unstable。排队超时的候选不进入有效线路集合。

验证结论边界：

1. 连续5个 "0x47"、间隔188字节，只能证明数据具有 MPEG-TS 结构特征。
2. 不代表节目表、音视频轨道、解码或画面已经验证成功。
3. stable 只代表两次规定的程序技术探测均通过，不代表中国大陆网络播放稳定。
4. 所有验证等级均属于第一层程序技术探测等级。
5. TS 结构探测结果必须与国内媒体可达性验证结果分开记录。

---

7. 网络访问与媒体验证

7.1 网络统一出口

所有网络访问必须通过 "network.py"，包括：

- 来源订阅下载；
- 地区 raw Feed 下载；
- 直接 TS 媒体请求；
- HLS 主清单、子清单和媒体分片请求；
- 重定向请求；
- 发布后的 GitHub Raw 程序侧检查。

其他模块不得自行创建绕过 "network.py" 安全检查的 HTTP 客户端。

7.2 IPv4 验证与安全

7.2.1 协议和目标地址

- 只允许 HTTP 和 HTTPS。
- file、ftp、rtsp、rtmp、WebSocket 等其他协议直接拒绝。
- 只允许连接全球可路由的公网 IPv4 地址。
- IPv6 URL 直接拒绝。
- 域名只查询 IPv4 A 记录。
- 使用 Python ipaddress 对每个解析结果执行 "is_global" 检查；非全球可路由地址一律拒绝。
- 必须拒绝私有、环回、链路本地、共享地址空间、保留、组播及其他非全球可路由地址。
- DNS 没有合法公网 IPv4 结果时拒绝。

7.2.2 DNS Rebinding 防范

1. DNS 返回多个 IPv4 地址时，逐个检查。
2. 实际连接只能使用已经检查通过的公网 IPv4。
3. 必须使用自定义 resolver 或等效机制，将已校验 IP 直接提供给实际连接器。
4. 禁止连接阶段再次使用系统 DNS 对原域名进行未校验解析。
5. 关闭 DNS 缓存，避免使用过期或未经本次检查的解析结果。
6. 实际 TCP 连接建立后，必须检查 socket peer IP 与本次已校验 IP 一致；不一致立即关闭连接并拒绝。
7. HTTP 请求必须保留原域名 Host。
8. HTTPS 必须使用原域名进行 TLS SNI 和证书主机名校验；不得把 URL 域名替换成 IP 来绕过证书校验。
9. 禁止通过系统代理绕过上述 IP 校验。
10. 显式设置 "trust_env=False"，不读取 HTTP_PROXY、HTTPS_PROXY 等系统代理环境变量；请求不得指定代理。

7.2.3 TLS 和请求客户端

- HTTPS 必须启用系统可信 CA 证书校验。
- 禁止使用 "ssl=False" 或关闭证书校验。
- 禁止接受域名不匹配证书。
- 禁止接受无效或过期证书。
- 不跨候选共享 Cookie。
- 不从环境变量读取代理。
- 禁止自动重定向。
- 使用流式读取和解压后字节计数。
- 候选验证连接不得复用未经本次目标校验的旧连接；首版采用关闭连接复用或经过等效证明的实现，确保每次新连接均经过已校验 resolver 和 peer IP 检查。
- 实际连接器的 DNS、socket peer IP、Host、SNI 和证书行为必须有集成测试。

7.2.4 重定向与子请求

- "allow_redirects=False"，手动处理重定向。
- 每个请求最多跟随5跳；初始请求不计为重定向。
- Location 相对地址必须以当前请求 URL 为基准，按标准 URL reference resolution 解析。
- 覆盖相对路径、根路径、跨主机路径和绝对 URL。
- 每次解析完成后，重新检查协议、主机、端口、DNS 和 IPv4 安全性。
- 未完成安全检查前不得连接。
- HTTPS 重定向到 HTTP 属于协议降级，直接拒绝。
- HLS 子清单和分片 URI 同样必须重新经过完整安全检查。
- 重定向超过5跳立即失败。

7.2.5 安全测试要求

必须测试：

- 实际 socket 连接 IP 是否等于已校验 IP；
- DNS 解析后是否存在未经校验的二次解析；
- HTTP Host 是否保留原域名；
- HTTPS SNI 是否使用原域名；
- 正确证书是否通过；
- 错误证书和域名不匹配证书是否被拒绝；
- 系统代理环境变量是否无法绕过 IP 校验；
- 每次重定向是否重新执行完整安全检查；
- HLS 子清单和分片是否重新执行安全检查。

不能只测试 DNS 解析函数返回正确 IP，还必须测试实际网络连接器行为。测试未通过，不得宣称安全验证通过。

7.3 请求限制、并发与读取策略

首版限制：

- 总候选：1000。
- 普通单来源候选：100。
- 有效订阅来源：40。
- 全局媒体验证并发：20。
- 同一主机媒体验证并发：5。
- 等待队列：最多60个等待任务。
- 单候选媒体验证总预算：8秒。
- 单候选队列等待上限：60秒。

7.3.1 候选调度规则

1. 候选池最多1000条。
2. 调度器最多允许20条正在验证，另有最多60条处于等待队列。
3. 超出60条等待容量的候选保留在尚未入队的待调度列表中，不丢弃。
4. 候选只有进入60条等待队列后，才开始计算60秒队列等待时间。
5. 尚未进入等待队列的候选属于待调度列表，不计入队列等待时间。
6. 等待队列中的候选超过60秒仍未获得验证资源，记录 "queue_wait_timeout" 并从队列移除。
7. 全局20个并发和同一主机5个并发必须由中央调度器统一管理。
8. 不允许工作任务先占用执行工作位，再阻塞等待单主机并发名额。
9. 调度器按等待顺序选择最早且当前主机有可用名额的候选；某主机已达到5个并发时，可以先调度其他主机的候选，不能让空闲全局并发位闲置。
10. 被跳过等待主机名额的候选继续计算其队列等待时间。
11. 取得全局和主机资源、即将开始网络验证时，才启动8秒媒体验证总预算。
12. "queue_wait_timeout" 不得占用网络验证并发名额。

7.3.2 8秒总预算

单候选8秒总预算包含：

- DNS 解析；
- TCP 连接；
- TLS 握手；
- 每次重定向；
- HLS 主清单；
- HLS 子清单；
- HLS 媒体分片；
- 两次短验证。

必须使用单个绝对截止时间控制整个候选验证过程。每个 HTTP 请求只能使用该候选剩余时间，不得在每个请求开始时重新获得8秒。

必须使用整体 deadline 控制所有异步请求；不能只依赖 aiohttp 单次请求的 "ClientTimeout(total=8)"，因为它会在多个请求之间重新计时。

达到绝对截止时间，立即终止该候选验证。

7.3.3 读取限制

1. 订阅文件：解压后最多8MB。
2. HLS ".m3u8" 清单：解压后最多1MB。
3. TS 媒体流：最多读取64KB。
4. 必须流式分块读取，例如使用 aiohttp "iter_chunked"。
5. 不得一次性读取不受限制的响应体。
6. 必须累计解压后的真实字节数；不能只依赖 Content-Length。
7. HLS 清单超过1MB立即失败，不允许截断后继续解析。
8. TS 流累计读取64KB仍未找到同步结构，立即中止并判定失败。
9. 找到连续5个 "0x47" 且间隔188字节后，可以立即停止读取本次 TS 数据。

7.3.4 压力测试

必须在 GitHub-hosted Ubuntu Runner 上执行1000候选受控压力测试。

压力测试使用本地受控 Fixture 服务器，不得对不受项目控制的第三方直播服务器发起1000条压力请求。

必须覆盖：

1. 1000候选集中访问同一主机；
2. 1000候选分散访问多个主机；
3. 多主机与热点主机混合访问；
4. 慢响应、连接失败、超时和队列等待；
5. 队列容量达到60；
6. 单主机并发达到5；
7. 全局并发达到20；
8. "queue_wait_timeout" 的触发与记录；
9. 候选是否丢失、重复验证或重复进入结果。

必须记录：

- 并发峰值；
- 单主机并发峰值；
- 等待队列峰值；
- 排队超时数量；
- 完成数量；
- 有效线路数量；
- 总耗时；
- CPU 和内存峰值；
- 是否出现调度阻塞。

不得只用理论估算代替实际压力测试。压力测试失败时，先定位调度器或实现缺陷；不得未经证据擅自更改8秒、60秒、20、5、60队列容量等既定参数。

7.4 媒体验证完整流程

首版只支持未加密 MPEG-TS。所有请求（包括主清单、子清单和分片）均计入单候选8秒总预算，并受每个请求最多5跳重定向限制。

7.4.1 直接媒体地址

- 不依赖 URL 后缀。
- 根据响应内容识别媒体类型。
- 最终媒体响应必须为 HTTP 200。
- 不发送 Range 请求；非200状态（包括206）不得作为首版直接 TS 或 HLS 分片验证通过。
- 只有通过 TS 同步结构检测，才算一次完整通过。
- HTML、JSON、普通文本或其他不支持内容均失败。

7.4.2 HLS 识别

- 如果响应内容为 HLS 播放列表，按内容识别，不依赖 ".m3u8" 后缀。
- 媒体播放列表包含 "#EXTINF" 和媒体分片 URI 时，直接进入分片验证。
- 主清单包含 "#EXT-X-STREAM-INF" 时，按 Variant 规则处理。
- 不支持的格式必须明确记录原因。

7.4.3 Variant 处理

1. 多码率主清单按原始出现顺序处理。
2. 最多尝试前2个 "EXT-X-STREAM-INF" Variant。
3. 每次验证先尝试第一个 Variant。
4. 第一个 Variant 完整验证通过后，停止本次 Variant 尝试。
5. 第一个 Variant 失败时，在8秒剩余预算允许的情况下继续尝试第二个。
6. 第二个 Variant 通过即可视为本次验证通过。
7. 不按带宽、分辨率或名称重新排序 Variant。
8. 不递归解析超过一层的子清单。主清单指向媒体播放列表属于一层；子清单再次指向主清单或更深层级，直接判定不支持。

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
2. "#EXT-X-SESSION-KEY"：
   - 首版一律拒绝。该标签用于在主清单声明媒体播放列表的加密密钥，不属于首版未加密支持范围。
3. "#EXT-X-MAP"：
   - 直接拒绝并记录 "FormatError: fMP4_not_supported"。
4. "#EXT-X-BYTERANGE"：
   - 首版直接拒绝并记录 "FormatError: byterange_not_supported"。
   - 不允许把资源整文件当成分片，也不允许忽略 Range 偏移。
5. 主清单声明带 URI 的外部音频或字幕 Rendition 时，首版判定为不支持，避免只验证视频分片却误判整个组合流可用。
6. 其他无法明确支持的加密或媒体格式，均不得判定通过。

7.4.6 失败判定

以下情况均判定验证失败：

- 没有有效 Variant；
- 没有可用媒体分片；
- HLS 子清单层级超过限制；
- 加密或不支持的格式；
- TS 分片无法满足连续5个 "0x47"、间隔188字节；
- 直接媒体内容无法识别为支持的 MPEG-TS；
- 请求状态、网络安全检查或总预算失败。

本节只定义首版支持边界，不代表已经完成全部 HLS 兼容性验证。

---

8. 频道整理与三线路选择

8.1 来源优先级

人工单条 > 人工订阅 > 运营商 > 自动发现。

来源优先级主要用于采集阶段去重和相同验证等级下的排序，不得覆盖验证等级排序。

地区 raw Feed 属于自动发现来源。其国家获取顺序、同国家只下载一次及候选公平分配规则按第5章执行。

8.2 线路去重规则

首版 URL 规范化规则：

1. scheme 转为小写；
2. host 转为小写并使用统一 IDNA 主机名表示；
3. 去除默认端口（HTTP 80、HTTPS 443）；
4. 去除 fragment；
5. Query 参数完整保留，不删除任何参数、不重排参数；
6. Path 保持原样，不擅自删除路径字符或改变路径大小写；
7. 不做额外的 tracking 参数删除或推测性 URL 改写；
8. URL 中包含用户名或密码的 userinfo 时拒绝该条目，避免把访问凭据写入公开订阅；
9. 输出使用规范化后的 URL，保留完整 Query 值。

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

- 已知存在一次失败的 unstable，不得排在只完成一次成功验证、尚未确认失败的 single_pass 前面。
- invalid、pending 和 queue_wait_timeout 不得进入正式订阅。
- 不引入线路评分系统、持久化线路数据库或复杂历史记录。
- 每次运行均基于本次采集和验证结果重新生成，不依赖上次运行的线路状态。
- 地区 raw Feed 的公平分配只控制进入候选池的机会，不是线路评分，也不改变验证等级和最终排序规则。

8.4 频道输出顺序

- 频道顺序按照 "channels.json" 中标准频道数组的原始顺序。
- 默认地区模式只输出 CN、HK、MO、TW 目标频道中有有效线路的频道。
- 用户指定模式只输出已识别的指定频道中有有效线路的频道。
- 用户清单顺序不得改变标准频道字典的固定输出顺序。
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
- "tvg-id" 使用标准频道字典原值，不输出未经确认的 Feed 复合 ID。
- "tvg-name" 和显示名使用 "canonical_name"。
- 频道配置中的 M3U 属性值不得含双引号、CR 或 LF，避免破坏 M3U 结构。
- URL 不得含 CR、LF 或其他控制字符。
- UTF-8 无 BOM，LF 换行，末尾保留一个换行。

9.2 TXT 格式

独立逻辑，UTF-8，LF 换行。

单行格式：

频道名称,线路URL

- 频道名称和 URL 两个字段都执行 RFC 4180 字段转义规则。
- 字段包含逗号、双引号、CR 或 LF 时，正确引用。
- 字段内部双引号必须双写。
- 准确表述为采用 RFC 4180 字段转义规则，不宣称完整字节级 RFC 4180 兼容。
- 同频道多线路直接并列输出多行，不允许使用未知分组。
- 末尾保留换行。

9.3 双格式一致性

生成正式文件前，必须重新解析 M3U 和 TXT 并核对：

- 频道集合完全一致；
- 每个频道线路数量一致；
- 每条线路 URL 完全一致；
- 频道顺序一致；
- 线路顺序一致。

任何不一致均阻断发布。

9.4 订阅信息

"subscription_info.json" 记录元数据，必须通过 "schemas/subscription_info.schema.json" 校验。

必须包含：

- 生成时间；
- 订阅版本或 Schema 版本；
- 频道数量；
- 线路数量；
- M3U 和 TXT 的 SHA-256；
- 搜索模式："default_regions" 或 "user_watchlist"；
- 本次目标国家或地区代码；
- 目标频道数量；
- 成功识别、未识别及有歧义的频道数量；
- 统一的验证状态对象：
  - "layer1_status"
  - "layer2_status"
  - "layer3_status"
  - "layer2_evidence"
  - "layer3_evidence"

"layer2_evidence"：没有真实证据时为 null；有证据时必须包含结果、M3U SHA、TXT SHA、验收时间、网络环境、验收方法和证据位置。

"layer3_evidence"：没有真实证据时为 null；有证据时必须包含结果、M3U SHA、TXT SHA、实际请求的媒体 URL、必要的 HLS 媒体分片请求结果、验收时间、网络环境和证据位置。

状态规则：

- 状态枚举统一为 passed、failed、unverified。
- 正式文件通过第一层程序技术探测后，"layer1_status" 为 passed。
- 没有国内真实订阅分发证据时，"layer2_status" 为 unverified。
- 没有国内真实媒体请求证据时，"layer3_status" 为 unverified。
- 不得把 Runner 内部 Raw 检查结果写成国内第二层或第三层通过。
- passed 或 failed 状态必须有对应的真实验收证据对象；证据中的 M3U/TXT SHA 必须与当前正式订阅 SHA 一致；不得只修改状态文字。
- "layer2_evidence" 和 "layer3_evidence" 的字段必须由 "subscription_info.schema.json" 校验。
- "layer2_status=unverified" 时 "layer2_evidence" 必须为 null；"layer3_status=unverified" 时 "layer3_evidence" 必须为 null。
- "layer3_status=passed" 的证据必须包含真实媒体 URL 请求结果；如果是 HLS，还必须包含被请求分片的结果。

---

10. 订阅发布与验收

10.1 正式发布路径

正式文件固定为：

- "output/iptv.m3u"
- "output/iptv.txt"
- "output/subscription_info.json"
- "output/publish_manifest.json"

这四个文件为正式发布组。

首版唯一正式发布渠道为 GitHub Raw。仓库必须为公开仓库，默认分支固定为 main，以保证普通播放器可以直接访问订阅文件。

正式 URL 形式：

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
   - "candidate_layer2_status = unverified"
   - "layer2_status = unverified"
   - "layer3_status = unverified"
5. GitHub Runner 内部的 Raw 检查只能记录为 "program_connectivity"，不得冒充国内第二层或第三层。
6. 如果未来实际取得国内网络验证证据，可以单独更新 JSON 元数据；必须记录验收对象、M3U SHA、TXT SHA、验收层级、时间、结论和证据位置。
7. M3U 或 TXT 内容变化，旧的第二层和第三层验收结果自动失效，必须重新取得对应证据后才能恢复为 passed。
8. 仅 metadata 变化、M3U 和 TXT 内容不变，不自动使订阅内容验收失效。
9. 推送前再次确认被测订阅内容没有变化。
10. 不得把第二层订阅文件拉取成功推断为第三层媒体可达。

10.4 国内验收证据标准（仅在实际执行时适用）

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

"candidate_manifest.json" 必须记录：

- Schema 版本；
- Candidate 生成时间；
- 生成 Candidate 所使用的源代码和配置提交 SHA："source_commit_sha"；
- Candidate 的 M3U SHA-256；
- Candidate 的 TXT SHA-256；
- 第一层程序技术探测状态；
- Candidate 频道数量和线路数量；
- 搜索模式和目标范围摘要；
- 生成时四个正式文件的 SHA-256 基准。

四个正式文件基准为：

- "output/iptv.m3u"
- "output/iptv.txt"
- "output/subscription_info.json"
- "output/publish_manifest.json"

首次正式发布前，四个正式文件必须全部不存在，四个基准值统一为 null。

四个正式文件必须全部存在或全部不存在。部分存在、部分缺失时，必须阻断 Candidate 生成。

Candidate Manifest 不记录自身 SHA，也不在自身内容中记录 Candidate commit SHA，避免自引用。Candidate commit SHA 在推送后由 Git 返回，写入 RunReport。

10.5.3 dry-run 生成和推送

"mode=dry-run" 必须：

1. 获取并确认 main 最新提交。
2. 检查正式四文件全部存在或全部不存在。
3. 记录正式四文件 SHA 基准。
4. 执行来源采集、解析、频道识别、Feed 关联验证、目标频道过滤、IPv4 安全检查和第一层媒体验证。
5. 生成 Candidate M3U、TXT 和 Manifest。
6. 重新计算 M3U、TXT SHA，并校验 Candidate Manifest。
7. 只提交 "output/candidate/" 三个文件。
8. 不修改正式四文件。
9. 以非强制快进方式推送到 main。
10. 推送成功后取得准确 Candidate commit SHA，并写入 RunReport 和 Actions Summary。
11. Actions Summary 必须同时展示：
    - Candidate commit SHA；
    - Candidate M3U SHA-256；
    - Candidate TXT SHA-256；
    - Candidate 频道数量；
    - Candidate 线路数量；
    - 第一层状态；
    - 搜索模式和目标国家或地区范围。

不得仅凭远端分支最新 HEAD 推断 Candidate commit SHA。

10.5.4 candidate-publish 输入参数

"mode=candidate-publish" 必须提供：

- "expected_m3u_sha256"
- "expected_txt_sha256"
- "expected_candidate_commit_sha"

输入格式：

- M3U/TXT SHA-256：64位十六进制字符。
- Git commit SHA：40位十六进制字符。

参数缺失、格式错误或比对不一致，统一阻断，退出码1。

10.5.5 指定提交提取与校验

"candidate-publish" 必须：

1. 获取 main 完整历史，不能依赖默认浅克隆。
2. 检查目标 commit 存在且属于当前仓库。
3. 检查目标 commit 是当前 main 历史中的祖先提交。
4. 检查 Candidate commit 的直接父提交必须等于 Manifest 中的 "source_commit_sha"。
5. 检查该 Candidate commit 的文件差异严格只有以下三个文件：
   - "output/candidate/iptv.m3u"
   - "output/candidate/iptv.txt"
   - "output/candidate/candidate_manifest.json"
6. 检查三个 Candidate 文件在该提交中真实存在。
7. 必须通过 "git show <commit>:<path>" 从指定提交读取文件，保存到独立临时目录。
8. 禁止使用 "git checkout <commit> -- <path>" 修改工作区。
9. 对 "candidate_manifest.json" 执行 Schema 校验。
10. 重新计算 M3U 和 TXT SHA-256。
11. 分别与 Manifest 内记录的 SHA 比对。
12. 再与用户传入的两个预期 SHA 比对。
13. 检查 Manifest 的四个正式文件基准与当前 main 正式四文件完全一致。
14. 检查 Candidate 的 "source_commit_sha" 与当前 main 相比，核心代码、配置、Schema、测试和工作流文件没有发生变化。
15. 如果核心文件已变化，Candidate 失效，必须重新执行 dry-run。
16. README、MASTER_PLAN、PROGRESS 等非核心文档变化，不单独导致 Candidate 失效。
17. 任一 SHA、文件、Schema 或提交归属检查失败，均不得发布。

10.5.6 正式文件生成

- 正式发布的 M3U/TXT 必须与指定 Candidate 文件字节级一致。
- 不得重新生成或重新排序 Candidate 的 M3U/TXT。
- "subscription_info.json" 和 "publish_manifest.json" 根据正式文件重新生成。
- 正式四文件必须在同一个 Git 提交中更新。
- 正式发布时 "layer2_status" 和 "layer3_status" 默认保持 unverified。
- Candidate 文件保留在 "output/candidate/"，不属于正式订阅。

10.5.7 Candidate 失效条件

出现以下任一情况，Candidate 不得发布：

- 当前正式四文件 SHA 基准与 Candidate Manifest 不一致；
- 正式四文件从全无变成部分存在或从完整变成部分缺失；
- Candidate 文件 SHA 不一致；
- Candidate commit 不存在或不属于当前 main 历史；
- 核心代码、配置、Schema、测试或工作流在 Candidate 生成后发生变化；
- Candidate Manifest Schema 不通过；
- Candidate 第一层状态不是 passed。

Candidate 失效时必须重新执行 dry-run，不得人工绕过。

10.6 关键变更与日常自动更新边界

以下文件变化属于关键变更：

- "src/"
- "tests/"
- ".github/workflows/"
- "config/"
- "schemas/"
- "manual.txt"
- ".python-version"
- "pyproject.toml"
- "uv.lock"

首次正式发布和上述关键变更后，必须先 dry-run，再由用户手动触发 candidate-publish。

日常自动更新必须比较当前 main 与上一次正式发布所记录的 "source_commit_sha"：

- 如果上述关键路径发生变化，自动 daily-update 阻断，要求先生成 Candidate 并人工确认。
- 如果只有 README、MASTER_PLAN、PROGRESS 等非关键文档变化，不阻断日常自动更新。
- 如果没有正式发布记录，daily-update 不得执行首发，必须走 Candidate 首发流程。

10.7 空订阅与质量骤降保护

10.7.1 非空门槛

- "iptv.m3u" 与 "iptv.txt" 必须非空。
- 至少1个有效频道。
- 每个输出频道至少1条线路。
- M3U 和 TXT 必须通过9.3双格式一致性检查。
- 用户指定模式下，若清单存在有效目标，但所有目标均无法识别或均无有效线路，禁止发布。
- 默认地区模式下，若 CN、HK、MO、TW 均无可用线路，禁止发布。
- 部分目标频道或部分地区失败，不得自动扩大范围搜索其他国家或其他频道。
- 所有空订阅阻断均不得覆盖上一份成功正式订阅。

以上门槛不受 "--force" 或其他豁免条件影响。

10.7.2 质量骤降保护

以最近一次成功正式发布的 Manifest 统计为比较基准。

- 本次频道数低于上次频道数的50%，默认阻断。
- 本次线路数低于上次线路数的50%，默认阻断。
- 恰好等于50%不属于“低于50%”，允许通过该项检查。
- 任一项低于50%即阻断，退出码3。
- 首次发布且无 previous manifest 时，跳过骤降检查。

豁免条件：

- 如果 "config/channels.txt" 或 "config/channels.json" 相对于上一次正式发布的 "source_commit_sha" 发生变化，则跳过本次50%骤降检查。
- 该豁免只影响50%骤降检查，不影响非空门槛、格式校验、Schema、安全检查、SHA 检查和发布阻断状态。
- 配置变化必须能够通过 Git 历史准确比较；无法读取基准提交时不得自动豁免。

"--force" 规则：

- 仅允许人工触发的 candidate-publish 或 daily-update 使用。
- 只允许绕过50%频道数/线路数骤降门槛。
- 不得绕过空订阅、名单保护、Schema、格式、安全、SHA、Candidate 基准、核心变更确认、并发保护、远端状态核对或 publish_blocked。
- 定时自动任务不得自动启用 "--force"。
- 使用 "--force" 必须在 RunReport 中记录操作者输入、触发方式和绕过的具体门槛。

本条50%保护规则保留。后续如有实际运行数据证明误拦截或漏拦截，必须先提供证据，再提出修改方案，不得无替代保护直接删除。

10.8 发布提交、失败恢复和 Raw 检查

10.8.1 Git 提交边界

- 首次正式发布及每次正式内容更新，四个正式文件必须在同一个 Git 提交中更新。
- Candidate 三个文件必须在同一个 Candidate 提交中更新。
- 生成或推送失败时，不得留下半组正式文件。
- 正式发布只能使用非强制快进方式。
- 绝不使用 force push。
- 正式提交必须基于当前最新 main。
- 提交前再次读取远端 main，若运行期间远端已变化，不得将旧状态直接推送；dry-run 和 daily-update 必须中止并从最新状态重新运行。
- candidate-publish 可以基于最新 main 创建正式提交，但必须重新完整核对 Candidate 祖先关系、核心路径一致性和正式四文件基准。
- Candidate 提交的文件差异必须严格只有三个 Candidate 文件；正式发布提交的文件差异必须严格只有四个正式文件。
- README 等无关文件不得被发布程序覆盖。

10.8.2 推送结果核对

- 推送明确被拒绝且确认远端未接受提交：退出码3。
- 推送响应丢失或结果不明确：读取远端分支、commit 和正式文件内容进行核对。
- 如果确认目标提交已进入远端历史，且远端正式文件内容与预期一致，视为推送成功。
- 如果无法确认远端是否接受提交，退出码4。
- 不得在状态不明时盲目重复覆盖或 force push。

10.8.3 Runner 内部 Raw 检查

正式提交成功后，可以在 GitHub Runner 内部检查正式 GitHub Raw 地址：

- M3U、TXT、subscription_info 必须返回200且 SHA 与 Manifest 对应；
- publish_manifest 必须返回200并通过 Schema；
- 最多执行3次检查，单次间隔5秒；
- 检查结果只记录为 "program_connectivity"；
- 不得标记国内第二层或第三层通过。

结果分类：

- passed：文件状态和 SHA 均符合预期；
- unavailable：超时、连接失败或非200，无法判断内容是否损坏；
- content_mismatch：连续3次均返回200，但内容 SHA 与预期不一致；
- test_error：检查程序自身异常。

处理规则：

1. passed：正常记录。
2. unavailable：记录警告，不回滚正式文件，不单独阻断下一次更新。
3. test_error：记录程序错误，不回滚正式文件，不单独阻断下一次更新。
4. content_mismatch：正式提交不自动回滚；立即停止本次运行的后续发布动作，并执行本节规定的持久化阻断流程。必须将 "publish_blocked=true" 和对应原因写入 "publish_manifest.json"，阻断后续 candidate-publish 和 daily-update，直到人工检查并清除阻断状态。
5. 清除 "publish_blocked" 必须由人工修改并提交 "publish_manifest.json"，同时在 PROGRESS.md 记录原因和处理证据。

阻断状态的双重持久化机制：

为防止 "publish_manifest.json" 因 Git 并发冲突无法写入，导致后续自动发布任务漏过阻断，必须同时使用 Manifest 阻断标记和专用 GitHub Issue 作为两层持久化记录。

1. 专用 GitHub Issue 使用固定且唯一的标题标识："[IPTV-Auto-Next] PUBLISH_BLOCKED"。
2. 检测到 content_mismatch 后，必须先检查是否存在相同标题的未关闭 Issue：
   - 已存在：更新该 Issue，追加本次故障记录；
   - 不存在：创建新的专用 Issue。
3. Issue 正文必须记录：GitHub Actions run_id、故障发现时间、正式发布 commit SHA、出现不匹配的文件名、Manifest 中的预期 SHA、Raw 实际 SHA、content_mismatch 原因、对应 Actions 运行链接。
4. 不得在 Issue 中写入凭据、Token 或未经脱敏的敏感地址。
5. 必须确认 Issue 创建或更新成功后，才能继续尝试写入 Manifest 阻断标记。
6. 对应 GitHub Actions Job 必须显式授予 "issues: write" 权限，并保留该 Job 实际需要的其他最小权限，例如 "contents: write"。
7. 如果 Issue 创建、更新或成功状态确认失败，必须立即停止后续发布动作，以退出码4结束，并记录具体失败原因。必须明确报警，要求人工暂停 candidate-publish 和 daily-update 工作流，直到确认持久化阻断已经建立。
8. 不得在 Issue 建立失败时，仅依赖本次 Runner 的临时日志或退出码，声称后续任务已经受到可靠阻断。

阻断状态提交的 Git 并发冲突处理：

1. 写入阻断标记前，必须先获取远端最新 main，并基于最新提交准备状态变更。
2. 只允许修改 "publish_manifest.json" 中的 "publish_blocked" 状态及对应原因；必须保留远端最新版本中的其他字段和变更，不得用旧工作区文件覆盖远端新内容。
3. 必须使用普通非强制推送，禁止使用 force push。
4. 如果推送因远端分支已更新而发生冲突，必须重新获取远端最新 main，在最新版本上重新应用阻断状态变更，再尝试推送；首次推送失败后，最多额外重试3次，总计最多4次推送尝试。
5. 每轮重试前，必须检查远端 "publish_manifest.json"。如果相同的 "publish_blocked=true" 及对应阻断原因已经存在，视为阻断状态写入成功，不得重复提交。
6. 经过总计4次推送尝试仍无法成功写入，或无法确认远端是否已接受阻断提交，统一按退出码4结束，并在运行日志、RunReport 及专用 Issue 中记录 content_mismatch、阻断写入失败及具体原因；不得报告阻断写入成功。
7. 即使 Manifest 阻断标记写入失败，只要专用未关闭 Issue 已成功建立，后续正式发布任务仍必须通过 Issue 门禁阻断发布。

后续正式发布任务的强制启动门禁：

任何 candidate-publish 和 daily-update 正式发布任务，必须在执行任何采集、正式文件修改或发布写入之前完成以下检查：

1. 获取远端最新 main 中的 "publish_manifest.json"，不得使用旧工作区缓存或上一次运行的本地文件代替。
2. 检查 "publish_manifest.json" 是否存在 "publish_blocked=true"。
3. 查询 GitHub 仓库中是否存在标题为 "[IPTV-Auto-Next] PUBLISH_BLOCKED" 的未关闭 Issue。
4. 只要 Manifest 为 "publish_blocked=true"，或者存在该专用未关闭 Issue，就必须立即停止任务，禁止采集后的正式发布、Manifest 正常更新及其他正式文件写入。
5. 如果 Manifest 无法获取、Schema 校验失败、Issue 查询失败或远端阻断状态无法确认，必须按退出码4结束，执行 fail-closed，不得继续发布。
6. 上述检查必须在获得正式写入并发锁之后、任何发布操作之前完成；等待并发锁期间不得提前执行正式写入。
7. "--force" 只能用于其原本允许的操作范围，不得绕过 Manifest 阻断、专用 Issue 阻断或启动门禁。

启动阶段 Raw 内容核验兜底：

除上述双重持久化阻断外，正式发布任务还必须执行线上正式文件核验，作为独立的内容完整性检查。

1. 在完成并发锁获取和持久化阻断门禁后、开始采集或写入前，强制获取线上 GitHub Raw 的当前正式文件，包括 M3U、TXT、subscription_info 和 publish_manifest。
2. 对 M3U、TXT、subscription_info 计算实时 SHA-256，并分别与远端 Manifest 中记录的对应 SHA 比对；对 publish_manifest 执行 Schema 校验。
3. 如果 M3U、TXT 或 subscription_info 的实时 SHA 与 Manifest 记录不一致，必须立即中止发布，按退出码3结束，并在 RunReport 中明确记录 "raw_content_mismatch_detected_on_startup"、文件名、预期 SHA 和实际 SHA。
4. 如果 publish_manifest 无法获取或 Schema 校验失败，必须按退出码4结束。
5. Raw 文件无法获取或返回非200时，不能将其视为内容一致；必须中止正式发布并按退出码4结束，记录具体原因。
6. 本项 Raw 核验只能发现当前文件完整性问题，不能替代 Manifest 和专用 Issue 的持久化阻断，也不能因为后续 Raw 内容恢复一致就自动解除已经存在的阻断记录。

人工解除阻断的唯一流程：

1. 人工检查并修复 content_mismatch 对应的问题。
2. 人工核实正式 Raw 文件及 SHA 与 Manifest 一致，确认正式内容已经恢复正常。
3. 人工修改 "publish_manifest.json"，清除 "publish_blocked" 状态及对应原因，并通过正常 Git 提交推送至远端 main。
4. 必须确认远端 Manifest 已成功更新，且阻断标记确实清除。
5. 在 PROGRESS.md 中记录故障原因、修复措施、验证结果和对应证据。
6. 最后由人工关闭专用 GitHub Issue。
7. 如果 Manifest 清除提交失败，或者远端状态无法确认，禁止关闭 Issue，继续保持阻断。
8. 禁止仅关闭 Issue、仅恢复 Raw 文件或仅修改本地 Manifest 就解除阻断。
9. 所有解除操作必须由人工明确执行，自动任务不得自行清除阻断状态。

退出码优先级：

本节特殊退出码规则优先于10.8.2和第13章的一般推送失败分类：

- 退出码3：启动阶段发现 M3U、TXT 或 subscription_info 的实时 SHA 与 Manifest 不一致，立即禁止发布。
- 退出码4：阻断 Issue 建立或更新失败、阻断状态提交失败、远端状态无法确认、Manifest 或 Issue 门禁检查失败、必要的 Raw 文件无法获取或 Manifest Schema 校验失败。
- 任何退出码3或退出码4的情况，都不得继续执行后续正式发布动作。

GitHub 服务整体不可用，导致 Manifest 推送和 Issue API 同时无法建立持久化阻断时，系统无法保证跨运行自动阻断。此时必须明确报警并要求人工暂停 candidate-publish 和 daily-update 工作流，直到人工确认阻断状态已经建立。不得宣称系统已经成功建立持久化阻断。

"publish_blocked" 不得被 "--force" 绕过。

10.8.4 状态元数据独立提交

在 M3U 和 TXT 内容 SHA 不变时，允许单独提交以下 JSON 状态变化：

- 有真实证据的第二层/第三层验收状态；
- publish_blocked 安全状态；
- 与订阅内容无关的必要发布状态字段。

不得在状态元数据提交中改变 M3U/TXT 内容。修改后必须通过 Schema，并保留原订阅 SHA。

---

11. 自动化运行

11.1 定时运行

每天北京时间06:17运行。

GitHub Actions 使用 UTC cron：

17 22 * * *

定时工作流必须位于仓库默认分支。不得改成06:00。

GitHub Actions 定时任务可能延迟或漏触发，系统不得宣称能够保证准时运行。

11.1.1 定时任务漏运行识别与补偿

时间统一使用：

- 北京时间：Asia/Shanghai；
- 持久化时间戳：UTC ISO 8601；
- target_slot：北京时间 YYYY-MM-DD 06:17。

Manifest 必须记录：

- "last_successful_daily_update_at"：最近一次成功 daily-update 的实际完成时间，UTC；
- "last_successful_daily_target_slot"：最近一次成功覆盖的定时目标槽，北京时间字符串；普通手动更新未传 target_slot 时不改变该字段。

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
- workflow_dispatch 中的 Candidate SHA、target_slot 和 force_quality_drop 输入按模式使用；不适用的输入不得被静默解释。

通过 workflow_dispatch 明确区分以下模式。所有会写入 Candidate 或正式文件的模式，在执行网络采集或发布前，必须先完成依赖锁检查、Ruff、单元测试、集成测试和安全测试；测试失败立即阻断写入。candidate-publish 不重新探测媒体线路，但必须重新执行发布前静态检查和测试。

"mode=test"：

仅测试：

- 单元测试；
- 本地 Fixture 集成测试；
- 配置和 Schema 测试；
- 网络安全测试；
- 1000候选受控压力测试；
- M3U/TXT 格式和发布逻辑测试。

明确禁止：

- 访问外部真实媒体地址；
- 下载真实外部订阅；
- 生成或推送 Candidate；
- 生成或修改正式订阅；
- 提交或推送 Git；
- 执行国内真实验收。

RunReport 必须记录实际执行、跳过和失败的测试项目。

"mode=dry-run"：

- 执行完整来源采集和第一层技术验证；
- 根据 "channels.txt" 确定搜索模式；
- 完成频道身份和 Feed 关联检查；
- 生成 Candidate 三文件；
- 推送 Candidate；
- 获取准确 Candidate commit SHA；
- 不修改正式四文件；
- 不执行国内实测。

"mode=candidate-publish"：

- 必须输入三个预期 SHA；
- 精确提取指定 Candidate commit；
- 完成文件、Schema、SHA、基准和核心代码版本检查；
- 完成发布保护；
- 发布 Candidate 对应的正式四文件。

"mode=daily-update"：

- 等同日常定时更新；
- 重新采集、验证并生成最新订阅；
- 按 "channels.txt" 当前内容决定默认地区或用户指定模式；
- 仅当不存在未确认的关键变更、发布阻断和质量保护问题时，才允许更新正式文件；
- 手动触发时可选传入 target_slot；
- 可选 force_quality_drop，只用于人工绕过50%质量骤降门槛；
- 定时触发不得自动启用强制发布。

首版不设置 verify-release 工作模式。国内第二层和第三层状态没有真实证据时保持 unverified；Runner 不得冒充国内测试环境。

11.3 运行保护与 GitHub Actions 并发

11.3.1 写入任务范围

以下任务会修改 main，必须使用同一个正式写入并发组：

- dry-run：写入 Candidate；
- candidate-publish：写入正式文件；
- daily-update：写入正式文件；
- 必要的发布阻断或验证状态元数据提交。

test 不修改 Git，不需要加入写入并发组。

11.3.2 并发参数

所有写入任务使用完全相同的 concurrency group 名称，并配置：

- "cancel-in-progress: false"
- "queue: max"

GitHub Actions 当前语义：

- 同一并发组最多1个运行任务；
- "queue: max" 最多允许100个等待任务；
- 队列满后，新任务会被取消；
- "queue: max" 不得与 "cancel-in-progress: true" 组合；
- FIFO 按任务开始等待并发组的时间排序，不是按事件触发时间排序。

不得为不同写入工作流使用不同并发组，否则可能同时修改同一分支。

未进入运行状态、在队列满时被取消的任务，不能保证生成自己的 RunReport 或 Artifact。

11.3.3 远端分支保护

- 所有正式写入任务获得并发锁后，必须重新获取远端 main 最新提交。
- 写入任务必须基于锁内读取的最新分支状态执行。
- 推送前再次确认远端状态未被外部提交改变。
- dry-run 或 daily-update 运行期间如果 main HEAD 发生变化，本次生成结果基于旧代码/配置，必须中止本次写入并重新运行，不得直接 rebase 后沿用旧结果。
- candidate-publish 可以基于最新 main 创建正式提交，但必须重新完整核对 Candidate 祖先关系、核心路径一致性和正式四文件基准。
- 如果远端变化导致当前提交过期，不得强制覆盖；应重新核对或安全终止。
- 所有推送均为非强制快进推送。
- Candidate 提交的文件差异必须严格只有三个 Candidate 文件；正式发布提交的文件差异必须严格只有四个正式文件。

11.3.4 GitHub 权限

- 只读测试任务使用 "contents: read"。
- dry-run、candidate-publish、daily-update 和元数据写入任务必须显式声明 "permissions: contents: write"。
- 由于阻断持久化机制依赖专用 GitHub Issue，所有具备写入权限的工作流（至少 daily-update 和 candidate-publish）必须同时声明 "issues: write"。
- 仓库 Settings → Actions → General 中必须允许工作流使用所需写权限。
- 默认分支 main 必须允许受控的 GitHub Actions 提交；如果分支保护规则禁止该自动提交，必须先调整规则，否则不得宣称发布流程已验证。
- 需要读取历史 Candidate commit 和比较历史配置时，actions/checkout 必须使用 "fetch-depth: 0"，不得使用默认浅克隆后假设旧 commit 已存在。
- 第三方 Actions 固定完整 commit SHA。

---

12. 测试与质量控制

12.1 测试分层

- "tests/unit/"：单元测试。
- "tests/integration/"：Fixture 集成测试。
- "tests/acceptance/"：真实 GitHub Runner 程序技术探测和发布流程验收。
- 国内第二层和第三层若未实际执行，必须保持 unverified，不得伪装成验收通过。

12.2 单元测试

不联网。必须覆盖：

- manual.txt 读取、空行忽略、异常容错；
- M3U/TXT 来源格式自动识别和记录解析规则；
- sources.json、channels.json Schema 和字段校验；
- 来源优先级和来源名额分配；
- 人工单条不占40个来源名额，但受1000候选限制；
- 普通单来源100条、总候选1000条截断；
- 地区 raw Feed 不受单来源100条限制；
- 来源无有效候选时不占来源名额；
- 默认地区模式判定；
- 空文件、全空白、只有注释时默认 CN、HK、MO、TW；
- 非空清单只搜索用户指定频道；
- 用户指定全球频道时只获取目标频道所属国家 Feed；
- 多个目标频道同一国家只获取一次 Feed；
- 四个默认地区 Feed 独立处理；
- 单个地区 Feed 失败不影响其他地区；
- "channel.country" 与 "feed.broadcast_area" 不得混用；
- "tvg-id" 中频道 ID 和 Feed ID 精确匹配；
- Feed.channel 与频道 ID 不一致时拒绝；
- Feed.id 与 tvg-id 后缀不一致时拒绝；
- 非空 tvg-id 匹配失败不得退回别名匹配；
- 只有 tvg-id 缺失时才允许名称精确匹配；
- 空 tvg-id 不得回退名称匹配；
- 名称别名歧义处理；
- CCTV-5 与 CCTV-5+ 不得误判；
- alias 冲突、重复身份和频道字典完整性；
- "channels.txt" 未识别单项隔离及全部未识别阻断；
- 目标频道过滤适用于所有来源；
- 地区 Feed 候选按频道轮询公平分配；
- 候选公平分配的确定性和总候选1000上限；
- 不支持协议和 "#EXTVLCOPT" 条目隔离；
- URL 规范化、Query 完整保留、默认端口和 fragment 处理；
- URL 全局去重和跨频道冲突处理；
- stable、single_pass、unstable、invalid 状态组合；
- 验证等级排序；
- 队列超时和验证超时区别；
- M3U/TXT RFC 4180 字段转义；
- M3U/TXT 双格式一致性；
- 空订阅阻断；
- 50%骤降保护、恰好50%边界、配置变更豁免和 "--force" 边界；
- Candidate 三 SHA 参数校验；
- Candidate 四文件基准校验；
- Candidate source commit 核心路径比较；
- publish_blocked 不得被 "--force" 绕过；
- RunReport 和 PublishManifest 字段空值处理；
- 日志中的 URL userinfo 和 Query 值脱敏；
- TS 技术探测不得被标记为国内播放成功。

12.3 集成测试

使用本地 Fixture。必须覆盖：

- DNS、IPv4 白名单和非全球地址拒绝；
- DNS Rebinding 防范；
- 实际网络连接器 peer IP；
- HTTP Host；
- HTTPS SNI；
- 正确证书、错误证书和域名不匹配证书；
- 系统代理环境变量不能绕过安全检查；
- 每次重定向重新执行完整安全检查；
- HTTPS 降级到 HTTP 被拒绝；
- 来源下载20秒超时和8MB解压后大小限制；
- 地区 Feed 独立获取和失败隔离；
- 缺少 Content-Length 时的分块读取限制；
- gzip 解压后的真实字节计数；
- HLS 主清单、子清单和分片请求；
- 最多2个 Variant；
- 每个媒体播放列表最多1个分片；
- HLS 子清单最多一层；
- EXT-X-SESSION-KEY 拒绝；
- EXT-X-KEY METHOD 判定；
- EXT-X-MAP 拒绝；
- EXT-X-BYTERANGE 拒绝；
- 相对 URI 正确解析；
- HLS 子请求安全校验；
- 8秒候选绝对 deadline；
- 两次短验证共用8秒；
- 60秒队列等待上限；
- 全局20、单主机5、等待队列60；
- 调度器不因单主机并发阻塞全局空闲工作位；
- queue_wait_timeout 正确触发和记录；
- 1000候选三种压力场景；
- Candidate 精确 commit 提取；
- git show 读取旧提交且不改变工作区；
- Candidate 基准变化时阻断；
- dry-run 与正式发布提交边界；
- 并发互斥和重复任务去重；
- 推送状态不明确时的远端核对；
- 定时任务漏运行识别和补偿；
- 普通手动更新不受 target_slot 重复判断影响；
- Raw 检查状态分类；
- verify-release 不属于首版模式。

必须全绿，阻断发布。

12.4 验收测试

真实联网测试允许外部来源失败，但必须记录原因写入 RunReport。

验收结果必须区分：

1. GitHub Runner 第一层程序技术探测；
2. Runner 内部 GitHub Raw 程序侧连通性检查；
3. 国内订阅文件分发；
4. 国内媒体网络可达性；
5. 实际设备播放反馈。

没有实际执行的层次必须标记 unverified。

频道搜索验收还必须检查：

- 空清单确实进入 CN、HK、MO、TW 默认模式；
- 非空清单只处理指定频道；
- 指定全球频道不会触发全球扫描；
- 所有来源都执行目标频道过滤；
- Feed 关联严格匹配；
- 单个地区 Feed 失败不会中止其他地区；
- 所有目标均无有效线路时不发布空订阅、不覆盖旧正式订阅。

12.5 正式发布门槛

必须满足：

- 单元、集成、安全测试全绿；
- 配置及 Schema 校验通过；
- 第一层程序技术探测通过；
- M3U/TXT 双格式一致；
- Candidate 或 daily-update 的发布保护全部通过；
- 空订阅和质量骤降保护通过；
- Candidate 首发或关键变更时，三个预期 SHA 分别校验一致；
- 正式四文件在同一个提交中更新；
- 统一并发保护和远端状态核对通过；
- 不存在 "publish_blocked=true"。

国内第二层和第三层没有真实验证证据时保持 unverified，不阻断首发或日常更新。

---

13. 统一退出码

- 0：成功。
- 1：配置或输入错误，包括配置 Schema 错误、频道字典错误、频道清单语法错误、Candidate SHA 参数缺失或格式错误、Candidate SHA 比对不一致。
- 2：阶段不可恢复错误，包括依赖环境失败、程序内部不可恢复错误、来源获取阶段完全无法形成候选等。
- 3：正式发布保护或发布失败，包括空订阅阻断、质量骤降阻断、关键变更未走 Candidate、Candidate 基准过期、发布被明确拒绝、publish_blocked 阻断。
- 4：发布状态无法确认，包括推送响应不明确且无法通过远端核对确定是否成功。

优先规则：

1. 输入或配置无效，返回1。
2. 处理阶段不可恢复且尚未进入发布状态，返回2。
3. 发布门槛明确不通过或推送明确失败，返回3。
4. 远端是否接受提交无法确认，返回4。
5. 不得将远端状态不明误报为普通成功或普通失败。

单个频道未识别、单个 Feed 失败或单个来源失败，原则上作为可观察的隔离结果记录；只有配置本身结构错误、全部目标无法识别或整体处理无法继续时，才按对应退出码阻断。

---

14. 统一错误类型

错误类别：

- ConfigError
- SourceError
- NetworkError
- ValidationError
- FormatError
- PublishError

错误记录必须包含：

- error_type
- error_code
- identifier
- stage
- reason
- retryable
- affects_publish
- 发生时间

必要错误代码包括：

- source_fetch_timeout
- source_size_limit
- source_parse_error
- channel_identity_mismatch
- channel_unresolved
- channel_ambiguous
- channel_country_unsupported
- feed_fetch_failed
- feed_channel_mismatch
- feed_id_mismatch
- feed_relation_unresolved
- regional_feed_partial_failure
- regional_feed_all_failed
- source_limit_reached
- candidate_fair_allocation
- unsupported_protocol
- unsupported_m3u_option
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

来源或候选失败可以跳过，但必须记录原因，不得静默跳过。

频道身份识别错误必须区分：

- 未找到频道；
- 频道 ID 不匹配；
- Feed 不存在；
- Feed 与频道关联不匹配；
- 名称存在歧义；
- 频道国家缺失或不支持。

不得将所有频道识别失败合并成一个无法追踪的通用错误。

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
- 搜索模式
- 目标国家或地区列表
- 目标频道数量
- 已识别频道数量
- 未识别频道数量
- 有歧义频道数量
- Feed 获取总数
- Feed 成功数
- Feed 失败数
- 每个地区 Feed 的独立结果
- Feed 频道关联成功和失败统计
- 来源统计
- 候选统计
- 公平分配统计
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
- 是否使用 "--force"
- "--force" 绕过的具体门槛

SHA 字段定义：

- "run_commit_sha"：本次运行所使用的代码和配置提交。
- "candidate_commit_sha"：包含 Candidate 三文件的 Git 提交；没有 Candidate 时为 null。
- "candidate_source_commit_sha"：生成 Candidate 所使用的代码和配置提交；没有 Candidate 时为 null。
- "formal_m3u_sha256" 和 "formal_txt_sha256"：正式订阅内容 SHA。

RunReport 保存为 GitHub Actions Artifact，保留30天。

Artifact 上传步骤必须尽可能使用 "if: always()"，保证运行开始后即使测试或发布失败，也能保存报告。任务在进入 Runner 前就被并发队列取消时，不保证存在 RunReport。

RunReport 必须通过 Schema 校验。

15.2 PublishManifest

统计口径：

- 频道数：M3U 中不同 tvg-id 的数量。
- 线路数：M3U 中 URL 总行数。

必须记录：

- Schema 版本；
- 生成时间；
- 本次正式发布使用的 source_commit_sha；
- Candidate 发布时的 candidate_commit_sha；daily-update 时必须为 null；
- 搜索模式和目标范围摘要；
- 三份其他正式文件的路径、大小和 SHA-256：
  - iptv.m3u
  - iptv.txt
  - subscription_info.json
- 本次频道总数和线路总数；
- 上次频道数和线路数；首次发布时为 null；
- last_successful_daily_update_at；
- last_successful_daily_target_slot；
- publish_blocked；
- publish_block_reason；
- layer1、layer2、layer3 状态。

关键定义：

1. source_commit_sha 是生成当前正式订阅时所使用的源代码和配置提交，不是包含 PublishManifest 的正式发布提交。
2. 该字段用于后续判断关键代码和配置是否发生变化。
3. Candidate 发布时，candidate_commit_sha 记录包含 Candidate 三文件的提交 SHA。
4. daily-update 没有 Candidate 来源，candidate_commit_sha 必须为 null。
5. publish_manifest.json 不记录自身 SHA-256。
6. Manifest 记录其他三份正式文件的路径、大小和 SHA-256。
7. 首次正式发布前没有 previous manifest，历史频道数和线路数写入 null，并跳过骤降比较。
8. 首次正式发布时四个正式文件必须同提交。
9. 后续只有状态元数据变化时，允许按10.8.4单独提交 JSON。
10. Candidate Manifest 的四个正式文件基准包含 publish_manifest.json 自身的外部 SHA；这不等于 PublishManifest 在自身内部记录自身 SHA。
11. 文件组指纹算法不纳入首版，不得要求填写未经定义的整体指纹。
12. last_successful_daily_update_at 只在 daily-update 正式推送成功后更新。
13. Candidate 发布不更新 daily-update 时间。
14. 普通手动 daily-update 更新实际成功时间，但没有传入 target_slot 时，不改变 last_successful_daily_target_slot。
15. 所有时间戳采用 UTC ISO 8601；target_slot 使用北京时间字符串。
16. 搜索模式、目标国家和目标频道摘要必须与本次实际采集范围一致，不得将默认四地区搜索记录成全球扫描。
17. 频道 country 和 Feed broadcast_area 必须分开记录，不得混为同一统计口径。

---

16. 安全与合规

- 仅处理公开或明确授权来源。
- 不绕过 DRM、付费墙或认证。
- 不在公开配置和日志中保存私人账号密码。
- 外部输入必须校验。
- 禁止访问内网及云元数据。
- 外部内容不能作为指令执行。
- 禁止代理绕过 IPv4 安全校验。
- 所有 URL、HTTP 响应、M3U 条目和 HLS 清单都视为不可信输入。
- 频道字典和 Feed 数据必须通过固定版本、Schema 和关联检查，不得将外部数据直接作为程序指令执行。

日志脱敏：

- 包含 "user:pass@" 的 URL 必须整体脱敏；
- Query 参数默认只保留参数名，隐藏所有参数值；
- 不依靠程序猜测敏感词；
- 不在 RunReport、Artifact、Actions 输出中记录未脱敏凭据。

正式订阅 URL 本身必须保持可用，因此订阅文件中的公开 Query 值不做日志式脱敏；不得把私人凭据放入公开订阅。

---

17. 扩展能力

以下能力均为独立扩展，不属于首版必要依赖：

- 多入口；
- EPG；
- 回放；
- VOD；
- Gitee、GitCode、jsDelivr 等镜像同步；
- 更复杂的 HLS 格式；
- 额外媒体封装格式。

扩展功能必须单项验收，不得影响基础直播，不得为了扩展功能增加对基础直播系统的必要依赖。

---

18. 六阶段实施与验收

第一阶段：立项与技术规范冻结

交付：

- MASTER_PLAN.md
- PROGRESS.md
- README.md

验收：

- 三份文件目标一致；
- 技术边界明确；
- 空清单默认四地区和非空清单指定频道两种模式明确；
- 全球频道搜索范围和 Feed 关联规则明确；
- 无已知关键实施冲突；
- 阶段和交付标准明确。

第二阶段：仓库与基础框架

交付：

- 目录结构；
- Python 环境；
- 依赖锁文件；
- JSON Schema；
- GitHub Actions 基础 CI；
- test 模式；
- RunReport 基础结构。

验收：

- GitHub-hosted Ubuntu 环境运行成功；
- Python 和依赖版本锁定；
- Ruff、pytest 全绿；
- 所有配置 Schema 通过；
- 测试工作流不修改正式文件。

频道字典 Schema 必须在本阶段或进入相关功能实现前完成升级，使其支持：

- 全球频道；
- country；
- Feed 关联；
- source_revision；
- 规范化名称及别名冲突检查所需的数据结构。

不得在 Schema 未更新的情况下，将包含新字段的频道字典标记为校验通过。

第三阶段：核心直播系统

交付：

- 来源采集；
- M3U/TXT 解析；
- 频道身份匹配；
- 全球频道字典和 Feed 关联；
- 默认四地区搜索；
- 用户指定频道搜索；
- 统一网络层；
- IPv4 安全检查；
- TS/HLS 媒体验证；
- 候选调度；
- 地区候选公平分配；
- 线路选择。

验收：

- 空清单进入 CN、HK、MO、TW 默认搜索；
- 非空清单只搜索指定频道；
- 用户指定全球频道只获取目标频道所属国家 Feed；
- Feed 关联精确匹配；
- 四地区 Feed 独立获取和失败隔离；
- 所有来源执行目标频道过滤；
- 网络安全集成测试通过；
- HLS 首版支持边界测试通过；
- 1000候选受控压力测试通过；
- 状态判定和排序符合规范；
- 不产生未验证或虚假标记。

第四阶段：订阅生成与首发

交付：

- M3U/TXT 生成；
- subscription_info；
- Candidate 三文件；
- Candidate SHA 校验；
- Candidate 精确 commit 提取；
- 正式四文件发布；
- GitHub Raw 正式地址。

验收：

- M3U/TXT 内容一致；
- Candidate 与正式文件字节级一致；
- Candidate 三 SHA 校验通过；
- 正式四文件同一个提交；
- 空订阅、骤降和发布保护通过；
- 默认模式与用户指定模式输出范围正确；
- 首发不依赖国内真实网络测试。

第五阶段：自动化与稳定性

交付：

- 北京时间06:17定时更新；
- 手动 test、dry-run、candidate-publish、daily-update；
- 漏运行识别和补偿；
- 并发保护；
- RunReport Artifact；
- 推送失败和远端状态核对；
- Raw 程序侧检查；
- 发布阻断和人工解除流程；
- 双重阻断持久化机制及启动门禁。

验收：

- 定时和手动流程正确；
- 写入任务统一并发组；
- 不覆盖上一份成功订阅；
- 失败和状态不明按退出码处理；
- RunReport 完整。

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
9. 四个正式文件必须在同一个 Git 提交中生成；后续允许按10.8.4单独提交状态元数据。
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
23. 频道搜索范围只能按本文件确定的两种模式执行，不得自行扩大或缩小。
24. 不得将空 "channels.txt" 解释为停止搜索；必须默认搜索 CN、HK、MO、TW。
25. 不得将非空 "channels.txt" 解释为在用户指定频道之外追加默认四地区频道。
26. 不得将频道 country 与 Feed broadcast_area 混用。
27. 不得为了凑够线路数量而绕过频道身份、Feed 关联、IPv4 或媒体验证。
28. 不得用未验证线路补位。
29. 不得因为某个地区或国家 Feed 失败而擅自扩大搜索范围。
30. 频道字典和 Feed 关联由项目维护，用户只编辑 "config/channels.txt"；不得擅自增加用户必须维护的 Feed 清单或新语法。
31. 本次规范调整不代表已经完成相应 Python 代码、配置文件、Schema 或 GitHub Actions 修改。实施状态必须以仓库真实文件和测试证据为准。

---

20. 最终交付标准

最终系统必须能够：

1. 自动获取登记的公开或授权来源；
2. 空 "channels.txt" 时默认搜索 CN、HK、MO、TW 四个地区；
3. 非空 "channels.txt" 时只搜索用户指定频道；
4. 支持用户指定全球频道，但只获取这些频道所属国家的 raw Feed，不进行全球扫描；
5. 通过频道 country 和 Feed 关联确定目标频道，不混淆 broadcast_area；
6. 识别频道并按确定性规则匹配；
7. 对存在 "tvg-id" 的条目执行精确身份匹配，对缺失 "tvg-id" 的条目执行无歧义名称精确匹配；
8. 只连接经过校验的全球可路由公网 IPv4；
9. 按首版 TS/HLS 规则执行媒体技术探测；
10. 对地区 Feed 独立获取、独立记录失败，并对地区候选执行确定性公平分配；
11. 依据验证等级和来源优先级筛选线路；
12. 每个频道最多保留三条线路；
13. 持续生成 M3U 和 TXT；
14. 通过 Candidate、SHA、质量保护和 Git 提交边界安全发布；
15. 按北京时间06:17自动更新；
16. 保留完整运行报告、发布清单和错误记录；
17. 正式发布失败时保护上一份成功订阅；
18. 明确区分第一层程序技术探测、国内订阅分发、国内媒体可达性和实际设备播放反馈。

最终交付的不是一套仅仅能够运行、显示绿色状态的程序，而是一套能够持续采集、验证、筛选、发布和追溯 IPTV 直播源的自动化系统。

任何没有真实证据的国内网络可达性结论，都必须保持 unverified。不得将程序技术探测包装成国内实际播放成功。

任何频道或地区没有可用线路时，必须如实记录；不得通过扩大搜索范围、放宽频道身份匹配或降低线路验证标准制造虚假结果。

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
