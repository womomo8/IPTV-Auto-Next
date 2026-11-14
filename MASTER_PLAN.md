# IPTV-Auto-Next MASTER_PLAN.md

版本：1.17-G3 最终定稿版（完整合并修订版）
文件性质：项目总施工规范，唯一指导方针
适用范围：整个项目架构、开发实施、测试验收和正式发布
优先级：本文档为最高指导规范，替代以往所有版本及补充条款。

1. 项目目标

1.1 核心目标

建设自动化运行的 IPv4 IPTV 直播源仓库。系统持续收集来源，执行技术探测，筛选并发布 IPv4 线路，如实记录国内网络验证状态。

必须实现：

自动收集直播源。

读取、校验全球频道库。

精确识别频道身份。

检测网络和媒体结构。

每个频道最多保留 3 条有效线路。

生成 M3U、TXT 订阅。

按计划自动更新。

保护上一份成功订阅。

保留运行报告、发布清单和 SHA 记录。

1.2 基本原则

基础直播优先，扩展不得影响基础。

严格区分程序技术探测、国内订阅分发、国内媒体可达性、实际设备播放四层。

不得将 Runner 结果视为国内可播；不得将订阅下载成功视为媒体可播。

无国内证据必须标记 unverified，不阻断正常开发发布；不使用收费云拨测。

全球频道库只负责频道身份识别，不推断线路存在。

用户选择范围优先于候选名额限制。

不采用线路评分机制，不建立复杂的持久化线路数据库或自动黑名单。

稳定参数不得擅自修改。

稳定参数：

项目固定值有效来源上限40单来源候选上限100总候选上限1000全局网络并发20单主机网络并发5内部等待队列60单候选验证预算8 秒绝对预算入队等待上限60 秒订阅下载上限8 MBHLS 清单上限1 MBTS 探测上限64 KB重定向上限5 跳每频道线路上限3线路骤降保护50%每日更新时间北京时间 06:17 

1.3 验收层次与责任边界

第一层：程序技术探测。Runner 内部保障格式、IPv4 安全、TS/HLS 结构，不代表国内可播。

第二层：国内网络订阅分发。真实拉取订阅文件，默认 unverified。

第三层：国内媒体网络可达性。真实请求媒体或分片，默认 unverified。

第四层：用户实际设备播放反馈。属于外部反馈，不纳入强制自动验收。

2. 实施阶段与绝对顺序

项目依次分为：规范冻结、基础框架、核心系统、生成首发、自动化、扩展。

2.1 绝对前置序列

必须严格按以下顺序执行，不得跳跃：

完成第一阶段规范冻结。

完成第二阶段第 0 步：全球频道库启动前核验（第 5.4 节）。

完成上游频道 ID 对齐核验（第 5.5 节）。

完成上游 Feed/Streams 实测（第 5.6 节）。

冻结模块接口契约（第 6.3 节）。

更新并验证相关 JSON Schema（第 12.3 节）。

将以上核验结果记入 PROGRESS.md。

完成以上步骤后，方可编写 catalog.py 及其他依赖全球频道库结构的业务代码。

第二阶段允许开展仓库结构检查、依赖环境验证、Schema 现状检查和测试框架准备，但不得提前编写依赖全球频道库结构的业务实现。

第三阶段不得重复安排已经完成的前置核验。

2.2 阶段完成条件

每个阶段必须有实际文件、测试结果或核验记录作为完成依据。仅有计划、代码草稿或未经执行的测试，不得标记为完成。

3. 运行环境与依赖

平台：GitHub-hosted Runner，Ubuntu 24.04。

语言：Python 3.14 最新补丁版，写入 .python-version，Actions 安装版本必须一致。

依赖：使用 uv.lock 锁定。

第三方 GitHub Actions 固定完整 Commit SHA，禁止使用浮动版本标签作为正式依赖。

Runner 必须实际验证： 

uv lock --check

uv sync --locked

Ruff

pytest

aiohttp 基础异步请求及取消行为

数据校验统一使用 JSON Schema Draft 2020-12。

Schema 校验失败不得静默忽略或自动修补后继续运行。

data/global_channels/channels.schema.json 和 data/global_channels/channel_filter.schema.json 是全球频道库唯一校验标准。

schemas/channels.schema.json 正式废弃，必须删除，不得保留第二套频道库 Schema。

4. 项目目录结构

IPTV-Auto-Next/ ├── data/ │ └── global_channels/ │ ├── channels.json │ ├── channels.schema.json │ ├── channel_filter.json │ ├── channel_filter.schema.json │ └── validation_summary.json ├── schemas/ │ ├── sources.schema.json │ ├── run_report.schema.json │ ├── publish_manifest.schema.json │ ├── candidate_manifest.schema.json │ └── subscription_info.schema.json ├── config/ │ ├── sources.json │ └── channels.txt ├── manual.txt ├── src/ │ └── iptv_auto_next/ │ ├── main.py │ ├── config.py │ ├── models.py │ ├── catalog.py │ ├── source.py │ ├── network.py │ ├── parser.py │ ├── validator.py │ ├── channel.py │ ├── selector.py │ ├── playlist.py │ ├── publisher.py │ └── reporter.py ├── tests/ │ ├── unit/ │ ├── integration/ │ └── acceptance/ └── output/ ├── candidate/ │ ├── iptv.m3u │ ├── iptv.txt │ └── candidate_manifest.json ├── iptv.m3u ├── iptv.txt ├── subscription_info.json └── publish_manifest.json 

说明：

manual.txt 固定在仓库根目录。

config/channels.txt 是用户频道选择清单。

不再读取旧的 config/channels.json。

正式订阅固定发布在仓库 output/ 目录，不使用 GitHub Pages。

output/candidate/ 只存放候选发布文件，不得被订阅正式地址引用。

5. 配置管理、解析与全球频道库核验

5.1 来源配置与解析

5.1.1 sources.json 结构

必须存在三个数组：

manual_single

carriers

discovery

允许数组为空。

每个来源必须具有全局唯一 id。URL 不得包含 userinfo 或控制字符。enabled=false 的来源不下载、不占名额。

来源配置必须通过 sources.schema.json 校验。

5.1.2 来源优先级

固定顺序：

人工单条 manual_single

人工订阅 manual.txt

运营商来源 carriers

自动发现 discovery

同一类别内部保持配置原始顺序，不得擅自重排。

5.1.3 候选上限与名额分配

最多接收 40 个有效来源。

每个来源最多接收 100 条候选。

总候选最多 1000 条。

人工单条不占 40 个来源名额，但计入总候选 1000 条。

manual.txt 按一个人工订阅来源处理。如果 manual.txt 为空或全为注释，不产生任何有效候选，不占用有效来源名额。

不占有效来源名额：

下载失败。

格式不支持。

解析失败。

没有匹配频道的有效候选。

候选全部被去重。

候选全部被频道范围过滤。

占有效来源名额：

至少产生一条同时通过身份识别、频道范围过滤、URL 校验和去重的有效候选。

截断规则：

按来源优先级串行处理，或采用能够保证相同优先级结果的严格分阶段实现。

不得先全量并行下载所有来源，再事后计算名额。

达到 40 个有效来源、单来源 100 条或总候选 1000 条时，立即停止后续处理。

频道选择过滤必须在来源名额和候选数量截断之前执行。

每次停止必须记录停止原因、已接收数量及能够确定的未处理数量。

失败来源不得占用有效来源名额。

同一来源内部保持原始条目顺序。

5.1.4 解析与去重顺序

必须依次执行：

获取来源。

解析内容。

校验 URL。

识别频道身份。

执行用户频道范围过滤。

URL 规范化。

全局去重。

应用单来源 100 条限制。

应用总候选 1000 条限制。

提交网络验证调度。

不得把频道范围过滤移动到候选截断之后。

5.1.5 manual.txt 解析

M3U：

允许 UTF-8 BOM 和 CRLF。

识别 #EXTM3U、#EXTINF。

每个 #EXTINF 只关联其后第一个有效 URL。

空行和注释不作为 URL。

到下一个 #EXTINF 仍无 URL，当前条目记录解析失败。

一个 URL 不得关联多个频道。

不完整条目单独记录，不得导致其他有效条目全部丢弃。

TXT：

使用 RFC 4180 规则解析。

每条记录必须恰好两个字段：频道名称、URL。

字段数量错误、名称为空或 URL 为空，当前记录失败。

单条错误不得导致整份文件丢弃。

不支持的格式必须记录并跳过，不得影响其他来源。

5.1.6 来源下载边界

单次下载超时：20 秒。

解压后实际读取上限：8 MB。

最多重定向：5 跳。

每次响应必须为 HTTP 200。

使用流式读取并统计真实解压字节。

超限立即终止。

缺少 Content-Length 时仍必须执行流式字节计数。

下载失败不得静默视为成功。

5.2 全球频道库结构与统计

5.2.1 唯一身份库

data/global_channels/channels.json 是唯一全球频道身份库。

它负责识别频道，不负责证明频道有可播放线路。

核心字段至少包括：

tvg_id

canonical_name

aliases

country

categories

如上游数据提供，还应保留并校验：

feeds

feed_id

broadcast_area

不得因为某频道没有 Feed 或 Stream 就将其从身份库中删除。

5.2.2 上游版本锁定

必须记录上游数据来源、仓库地址、固定 Commit SHA 或等效不可变版本标识、获取时间。

禁止正式运行时无记录地跟随上游最新数据。

上游更新必须重新执行频道 ID 对齐、Feed/Streams 核验、Schema 校验和统计复算。

5.2.3 validation_summary.json 统计口径

必须包含：

字段计算方式channels频道数组元素总数unique_tvg_ids非空 tvg_id 去重数量countries非空国家代码去重数量country_counts按稳定国家代码统计的频道数量category_values非空分类展开后的去重数量empty_categories没有有效分类的频道数量selected_country_name_conflict_keys本次选择范围内名称/别名冲突键数量json_byteschannels.json 原始文件字节数 

统计必须从实际原始文件计算，不能使用序列化后重新计算的长度替代 json_bytes。

5.2.4 统计一致性

启动时重新计算全部统计字段，与 validation_summary.json 逐项比较。

任何字段缺失、类型错误或数值不一致，均启动失败，退出码 1。

5.2.5 默认地区

channel_filter.json 必须定义默认地区：

["CN", "HK", "MO", "TW"]

用户人工模式优先，人工模式不受默认地区限制。

5.3 频道选择与身份匹配

5.3.1 channels.txt 解析

UTF-8。

允许 BOM 和 CRLF。

忽略空行。

忽略以 # 开头的注释。

清理每行首尾空白。

空文件、只有空行或只有注释时，进入默认地区模式。

存在有效内容时，进入人工选择模式。

5.3.2 用户目标匹配

channels.txt 每行目标：

优先按完整 tvg_id 精确匹配。

未匹配时，才按规范化名称精确匹配。

不允许模糊匹配、部分匹配、拼音猜测或自动推断。

重复目标仅保留首次，记录重复数量。

目标无法匹配或匹配到多个频道，启动失败，退出码 1。只要有一个目标无法匹配或产生歧义，整个启动过程直接报错退出（退 1），不允许静默跳过，防止用户误以为填写的频道已经生效。

5.3.3 来源条目匹配

来源中的 Candidate 与用户目标匹配规则不同：

只要来源条目存在 tvg-id 属性，就必须按 ID 精确匹配。

tvg-id 存在但为空，直接拒绝。

tvg-id 存在但不匹配，直接拒绝。

以上两种情况绝不回退名称匹配。

只有完全不存在 tvg-id 属性时，才允许按名称匹配。

5.3.4 名称规范化

统一执行：

Unicode NFKC → 去首尾空白 → 转小写。

不删除内部空格，不删除标点，不转换拼音，不自动转换繁简体。

名称规范化仅用于比较，不修改频道库原始名称和别名。

5.4 全球库启动前核验（第二阶段第 0 步）

5.4.1 全局身份命名空间检查

启动前检查整个频道库，而不只是本次选择范围：

tvg_id 必须非空。

tvg_id 必须全局唯一。

不同频道之间，任何会导致同一输入指向不同频道的规范化名称或别名键均属全局冲突。

频道名称和别名不得包含双引号、CR 或 LF。

Schema、字段类型和必填字段必须通过校验。

任何全局冲突均启动失败，退出码 1。

不得因为冲突频道不在本次选择范围内而忽略。

5.4.2 selected_country_name_conflict_keys

全局命名空间检查通过后，计算本次选择范围：

人工模式：只统计用户选择的频道。

默认模式：只统计 CN、HK、MO、TW 频道。

将范围内全部名称和别名规范化，建立“名称键 → 频道集合”映射。

同一个键关联两个或以上不同频道，计为一个冲突键；涉及更多频道仍只计一次。

由于全局冲突检查（5.4.1）已经保证全库无冲突，此字段仅用于防御性校验和记录风险，正常情况下该值绝对为 0。如果发现非零，代表代码内部状态错乱或全局库被并发篡改，必须直接抛出 panic 级异常中断启动，不得继续正常运行。

5.5 上游频道 ID 对齐核验

必须验证上游频道身份与本地全球频道库之间的对应关系。

检查内容：

上游 ID 是否稳定、唯一。

上游频道 ID 是否正确映射到本地 tvg_id。

名称、别名是否存在错误映射。

国家代码是否一致。

上游字段变化是否影响本地 Schema。

无法确定身份的记录不得自动猜测归属。

核验结果记录到 PROGRESS.md。未完成不得进入依赖该结果的业务实现。

5.6 上游 Feed/Streams 实测

必须对上游 Feed/Streams 数据进行实际结构检查：

数据能否正常读取。

Feed/Stream ID 是否有效。

Feed 与频道身份的对应关系是否可靠。

是否存在重复、失效或结构异常。

上游数据是否提供实际媒体地址。

不得把上游存在频道记录等同于存在可播放线路。

实测失败必须记录具体原因。不得伪造成功结果。

6. 核心数据模型与接口契约

6.1 数据模型

Source

必填字段：

id, source_type, url, priority, enabled, original_index

Candidate

必填字段：

source_id, source_type, raw_url, normalized_url, raw_tvg_id, raw_name, channel_id, original_index, discovered_at

另须保留 tvg-id 属性是否存在的信息，避免把“属性不存在”和“属性存在但为空”混为一谈。

VerifiedLine

必填字段：

channel_id, url, source_id, source_priority, stability, verified_at, ts_probe_status, error_code

Channel

必填字段：

tvg_id, canonical_name, aliases, country, categories, original_index

ValidationResult

必填字段：

status, attempt_count, passed_count, failure_count, started_at, finished_at, error_code, reason

结构化错误对象

必填字段：

error_type, error_code, identifier, stage, reason, retryable, affects_publish, occurred_at

不得在结构化错误中包含密码、Token、Cookie 或完整敏感 URL。

6.2 验证等级

两次短验证必须串行，共用单候选 8 秒绝对预算。

第一次第二次状态是否有效通过通过stable是通过失败unstable是失败通过unstable是通过预算耗尽single_pass是失败预算耗尽invalid否失败失败invalid否 

规则：

至少一次完整通过才算有效线路。

queue_wait_timeout 是调度超时，不是验证等级。

queue_wait_timeout 不得计为 invalid 或 unstable。

queue_wait_timeout 不进入有效线路集合。

pending 仅为内部状态，不得进入正式输出。

TS 结构探测与国内网络可达性必须分开记录。

6.3 模块接口契约（冻结）

# catalog.py def load_catalog( channels_path: str, filter_path: str ) -> Catalog: ... def validate(self) -> None: """ 校验 Schema、字段、统计、tvg_id 唯一性、 全局名称命名空间和非法字符。 失败抛出 ConfigError。 """ def resolve_selection( self, channels_txt_path: str ) -> SelectionMode: """ 解析用户目标或默认地区。 无法匹配、歧义、格式错误抛出 ConfigError。 """ def is_in_scope(self, tvg_id: str) -> bool: ... def ordered_channels(self) -> List[Channel]: """ 按 channels.json 原始数组顺序返回选择范围内频道。 不得按名称或字母重新排序。 """ # channel.py def match_identity( raw_tvg_id: Optional[str], raw_name: str ) -> ChannelIdentity: """ 有 tvg-id 属性时必须精确匹配。 ID 存在但为空或不匹配，抛 InvalidIdentityError。 无 ID 属性时按规范化名称匹配。 名称歧义抛 AmbiguousIdentityError。 """ 

接口冻结后，未经规范修订不得随意更改函数签名、返回类型、异常语义和排序契约。

7. 网络访问、调度与媒体验证

7.1 网络统一出口

所有外部网络请求必须通过 network.py：

订阅下载。

Feed 下载。

Streams 下载。

TS 探测。

HLS 主清单、子清单和分片。

Raw 正式文件检查。

其他模块不得自行建立绕过统一安全规则的网络连接。

7.2 IPv4 与 DNS 安全

只查询 DNS A 记录。

每个解析出的 IPv4 地址必须单独检查。

使用 ipaddress 的公网属性判断，拒绝私网、环回、链路本地、保留、组播及其他非全球可路由地址。

多个 A 记录必须逐个验证，不得因其中一个地址安全就放行全部地址。

实际连接只能使用本次已验证的 IP。

自定义 resolver 必须避免连接时再次进行不受控 DNS 解析。

禁用 DNS 缓存或确保每次请求使用本次验证结果。

TCP 建立后读取 Socket peer IP，必须与本次选用的已验证 IP 一致。

不一致立即终止请求并记录安全错误。

7.3 TLS、请求与重定向安全

使用系统 CA 证书验证。

禁止 ssl=False。

TLS 握手必须使用原始域名 SNI。

HTTP Host 必须保留原始域名，不能替换成连接 IP。

设置 trust_env=False，禁止继承环境代理。

不复用未经本次验证的旧连接。

禁止自动重定向，必须逐跳处理。

最多允许 5 跳重定向。

每一跳重新检查协议、域名、DNS A 记录、IPv4 地址和安全属性。

HTTPS 降级到 HTTP 必须拒绝。

HLS 子清单和分片请求必须重新执行完整安全检查。

安全校验失败严禁降级放行。

7.4 程序内部并发调度

内部网络调度与 GitHub Actions 工作流队列完全独立。

固定参数：

全局网络并发：20。

单主机并发：5。

内部等待队列：60。

执行规则：

使用中央调度器统一管理全局和单主机资源。

单主机并发已满时，跳过该主机候选，调度其他可运行主机。

不得因为某一主机满载而让全局可用并发长期闲置。

被跳过的候选继续计算其已入队等待时间。

必须同时取得全局和单主机资源后，才开始单候选 8 秒验证预算。

释放资源必须在成功、失败、超时、取消等所有路径执行。

内部等待队列最多 60 个任务。

超出队列容量的任务保留在待调度列表，不算入队，不开始 60 秒等待计时。

队列容量恢复后，按调度规则继续入队。

队列超时：

只有成功进入内部等待队列的任务才开始计算 60 秒。

入队后等待超过 60 秒，记录 queue_wait_timeout。

超时任务从队列移除。

不占网络并发。

不计为线路验证失败。

不计入 invalid、unstable 或有效线路数量。

报告必须区分未入队数量、队列超时数量和实际验证数量。

7.5 单候选 8 秒绝对预算

单一绝对 deadline 覆盖：

DNS → TCP → TLS → 重定向 → 主清单 → 子清单 → 分片 → 两次短验证。

规则：

取得全部调度资源后才启动 deadline。

所有阶段共用同一个 deadline。

不得在重定向、子清单或第二次验证时重置预算。

达到 deadline 后立即取消该候选剩余网络任务。

超时后必须释放所有调度资源。

两次短验证必须串行执行。

7.6 读取边界

内容最大读取量订阅文件8 MBHLS 清单1 MBTS 媒体64 KB 

全部使用流式读取并统计真实解压字节。

缺少 Content-Length 时仍然必须计数。

超过上限立即终止。

TS 找到连续 5 个 0x47，且相邻同步字节间隔均为 188 字节，即可停止继续读取。

7.7 直接媒体验证

不依赖 URL 后缀判断媒体类型。

必须 HTTP 200。

拒绝 HTTP 206。

最多读取 64 KB。

必须找到符合要求的 TS 同步结构。

不是 TS 或无法确认 TS 同步，判定失败。

请求超时、安全失败、状态码错误均判定失败。

7.8 HLS 验证

按内容识别 HLS，不依赖后缀。

Variant 按原始顺序检查前两个。

第一条通过即停止，不再检查第二条。

第一条失败且预算允许时，才检查第二条。

最多允许一层子清单，不允许递归继续解析。

每个媒体列表最多读取一个分片。

分片必须 HTTP 200，拒绝 206。

分片必须满足 TS 同步要求。

拒绝规则：

EXT-X-KEY 仅允许 METHOD=NONE。

其他加密方式拒绝。

EXT-X-SESSION-KEY 拒绝。

EXT-X-MAP 拒绝，记录 fMP4_not_supported。

EXT-X-BYTERANGE 拒绝，记录 byterange_not_supported。

外部音轨、字幕 Rendition 不支持。

不得绕过上述限制继续放行。

HLS 失败条件：

没有有效 Variant。

没有媒体分片。

子清单层级超限。

分片请求失败。

TS 分片无法找到同步。

加密或不支持格式。

HTTP 状态码不符合要求。

DNS、连接、TLS、重定向或其他安全检查失败。

8 秒绝对预算耗尽且没有一次完整通过。

8. 频道整理与 URL 规范化

8.1 URL 规范化

严格按以下规则：

scheme 转小写。

hostname 转小写并进行 IDNA 规范化。

只删除默认端口：HTTP 80、HTTPS 443。

非默认端口必须保留。

Path 原样保留。

Query 完整保留，不删除、不修改、不重排。

删除 Fragment。

拒绝包含 userinfo 的 URL。

全局去重统一使用规范化后的 URL。

重复线路保留来源优先级最高者；同优先级保持原始顺序。

8.2 线路排序与截断

排序优先级：

stable

single_pass

unstable

来源优先级。

验证时间，新到旧。

来源内原始顺序。

每频道最多保留 3 条。

invalid、pending、queue_wait_timeout 和其他未通过线路不得进入有效线路集合或正式输出。

9. Candidate 与正式发布保护

9.1 Candidate 生成

Candidate 固定由三个文件组成：

output/candidate/iptv.m3u

output/candidate/iptv.txt

output/candidate/candidate_manifest.json

三个文件必须在同一个 Candidate Commit 中。

Candidate Manifest 必须记录：

schema_version

generated_at

source_commit_sha

Candidate M3U SHA-256

Candidate TXT SHA-256

第一层状态

频道数量

线路数量

正式四文件基准 SHA-256

正式四文件是：

output/iptv.m3u

output/iptv.txt

output/subscription_info.json

output/publish_manifest.json

首发规则：

四个正式文件全部不存在时，四个基准 SHA 均为 null。

四个正式文件全部存在时，必须记录各自实际 SHA。

部分存在、部分缺失时，阻断 Candidate 生成。

不得把缺失文件伪装成 SHA 为零或空字符串。

9.2 dry-run 执行规则

获取写任务锁。

拉取最新远端 main。

记录当前 main HEAD。

检查发布门禁。

检查正式四文件基准。

执行完整采集和验证。

生成三个 Candidate 文件。

通过对应 Schema 和格式校验。

重新计算 M3U/TXT SHA。

与 Candidate Manifest 记录值核对。

确认本次提交只包含三个 Candidate 文件。

推送 Candidate Commit。

获取并记录精确 Candidate Commit SHA。

dry-run 不得修改正式四文件。

9.3 candidate-publish 输入

必须提供：

expected_m3u_sha256

expected_txt_sha256

expected_candidate_commit_sha

格式要求：

两个 SHA-256 必须为 64 位十六进制字符串。

Commit SHA 必须为 40 位十六进制字符串。

任一缺失或格式错误，退出码 1。

9.4 candidate-publish 严格校验

必须逐项执行：

获取写任务锁。

拉取完整 Git 历史。

确认指定 Candidate Commit 存在。

确认 Candidate Commit 是当前 main 的祖先。

确认 Candidate Commit 的父提交等于 Manifest 中的 source_commit_sha。

确认 Candidate Commit 的文件差异仅限三个 Candidate 文件。

必须使用 git show <commit>:<path> 精确提取文件。

严禁通过 git checkout 切换到历史 Candidate 来提取文件。

核对提取文件 SHA、Manifest SHA 和用户输入 SHA。

核对 Candidate Manifest Schema。

核对正式四文件基准与当前 main 一致。

核对核心代码、配置、Schema 等关键路径没有变化。核心路径明确包括 src/、config/、data/、schemas/、.github/、manual.txt、.python-version 及依赖锁文件。除上述路径外（如 README、PROGRESS）的变更，不阻断 Candidate 发布。

检查第一层状态必须为 passed。

检查 M3U/TXT 格式和内容一致性。

检查正式发布质量门槛。

任何一项失败，Candidate 失效，必须重新执行 dry-run。

正式发布的 M3U 和 TXT 必须与 Candidate 对应文件字节级完全一致，不得重新生成或修改内容。

9.5 正式发布提交边界

正式发布必须同时更新四个文件：

output/iptv.m3u

output/iptv.txt

output/subscription_info.json

output/publish_manifest.json

四个文件必须在同一个 Git Commit 中。

禁止：

force push。

覆盖无关文件。

只更新部分正式文件。

将未经 Candidate 校验的内容直接发布。

将旧代码运行结果直接 rebase 后推送。

推送必须基于最新 main 快进完成。

推送响应丢失时，必须查询远端确认提交是否成功；无法确认，退出码 4。

9.6 空订阅与质量骤降保护

频道数量为 0，阻断发布，退出码 3。

与上次成功发布相比，线路数量下降超过 50%，阻断发布，退出码 3。

恰好下降 50% 时允许通过。

有明确配置变更且符合豁免规则时，可以豁免骤降检查，但必须记录原因。

--force 只能绕过 50% 骤降保护。

--force 不得绕过空订阅、安全检查、Schema 检查、状态不明、Candidate 校验或发布阻断。

10. Raw 检查与双重持久化阻断

10.1 Raw 检查分类

Runner 对正式 Raw 文件执行检查，最多 3 次，间隔 5 秒。

Raw 检查只代表 program_connectivity，不代表国内网络可达或实际设备播放。

结果分为：

状态处理passed正常记录unavailable记录警告，不回滚，不单独阻断test_error记录测试错误，不回滚，不单独阻断content_mismatch立即启动双重持久化阻断 

unavailable 和 test_error 不得误判为 content_mismatch。

10.2 content_mismatch 双重阻断

发现 content_mismatch 时，必须执行：

第一步：建立专用 Issue

创建或更新专用 Issue：

[IPTV-Auto-Next] PUBLISH_BLOCKED

记录：

发生时间。

不一致文件路径。

预期 SHA。

实际 SHA。

对应 Commit SHA。

本次运行 ID。

阻断原因。

Issue 创建或更新失败，立即停止发布，退出码 4。

第二步：写入 PublishManifest

Issue 成功后，才允许将 Manifest 的：

publish_blocked

publish_block_reason

更新为阻断状态。

Manifest 推送冲突最多重试 4 次。

每次重试必须重新拉取远端 main 并检查阻断状态：

远端已经存在阻断标记，视为成功。

远端尚无阻断标记，重新尝试写入。

四次均失败，退出码 4。

Issue 保留作为第二道持久化门禁。

10.3 正式任务启动门禁

任何正式写任务开始前：

获取写任务锁。

拉取最新 main。

检查 publish_manifest.json 的阻断标记。

检查是否存在未关闭的专用阻断 Issue。

任意一个存在，立即 fail-closed，退出码 4。

检查正式 Raw 文件 SHA。

Raw SHA 与 Manifest 不一致，退出码 3。

无法确定远端状态，退出码 4。

不得在状态不明时继续发布。

10.4 人工解除阻断

阻断只能人工解除，程序严禁自动清除。

人工解除必须依次完成：

查明并修复问题。

核对本地正式文件 SHA。

核对远端 Raw SHA。

人工修改 Manifest 阻断标记。

将修复后的 Manifest 推送到 main。

将处理原因和核验结果写入 PROGRESS.md。

确认正式文件和 Manifest 一致。

最后关闭专用 Issue。

不得仅关闭 Issue 而不修复 Manifest，也不得仅清除 Manifest 而保留未解决的 Issue。

11. GitHub Actions 自动化与远端保护

11.1 定时任务

每日北京时间 06:17 执行。

对应 UTC Cron：

17 22 * * * 

工作流必须明确使用 UTC 调度，并在报告中记录目标时段和实际运行时间。

11.2 手动运行模式

必须支持：

test

dry-run

candidate-publish

daily-update

各模式职责：

模式职责test测试配置、Schema、基础流程和网络能力，不发布正式文件dry-run完整采集验证，生成 Candidatecandidate-publish校验指定 Candidate 并执行正式发布daily-update按正式自动更新流程执行采集、验证、发布 

11.3 工作流并发

所有写任务使用统一 concurrency group。

固定要求：

cancel-in-progress: false

使用平台支持的最大排队配置。

目标为 1 个运行任务、最多 100 个等待任务。

队列按平台支持的 FIFO 行为处理。

队列满时新任务不得并行绕过锁执行。

取消或排队失败必须在可记录的情况下写入报告。

工作流队列与程序内部验证队列完全独立。

平台不支持的排队行为不得由程序假定为已实现，必须通过实际 Actions 配置和运行验证确认。

11.4 远端 main 保护

写任务获取锁后重新拉取最新 main。

记录本次运行使用的 main HEAD。

推送前重新读取远端 main HEAD。

如果 HEAD 变化，当前 dry-run 或 daily-update 结果作废。

必须基于最新代码重新运行。

严禁将旧代码运行结果直接 rebase 后推送。

candidate-publish 必须重新核对祖先关系、核心路径和正式四文件基准。

任何无法确认的远端状态均停止发布。

11.5 漏跑补偿

每日任务必须记录目标时段 target_slot。

下一次日常运行时：

检查上一次成功更新时间。

判断是否存在未完成的目标时段。

按既定规则执行漏跑补偿。

补偿必须使用当前最新 main，不得复用过期运行结果。

补偿成功或失败均写入 RunReport 和 PROGRESS.md。

不得因补偿重复覆盖已经成功发布的更新。

12. 运行报告、发布清单与 Schema

12.1 RunReport

每次运行必须生成结构化 RunReport。

至少包含：

运行信息

run_id

mode

started_at

finished_at

run_commit_sha

source_commit_sha

candidate_commit_sha

candidate_source_commit_sha

target_slot

频道选择与预检

selection_mode

default_regions

preflight_result

dropped_by_scope_count

全球库统计结果

上游核验状态

来源和候选统计

来源总数、成功数、失败数。

有效来源数量。

候选总数、解析失败数、过滤数、去重数。

单来源截断数、总候选截断数。

未处理来源及停止原因。

验证与调度统计

stable

single_pass

unstable

invalid

queue_wait_timeout

未入队数量。

实际验证数量。

全局并发峰值。

单主机并发峰值。

等待队列峰值。

超时和取消数量。

错误和发布状态

结构化错误列表。

test_error

force_used

force_bypass_reason

漏跑补偿状态。

各层验证状态。

program_connectivity

publish_blocked

publish_block_reason

发布前后 SHA 核验结果。

时间统一使用 ISO 8601，明确时区或使用 UTC。

报告必须通过 run_report.schema.json 校验。

12.2 PublishManifest

至少包含：

基本信息

schema_version

generated_at

source_commit_sha

candidate_commit_sha，日常直接更新时为 null

正式文件信息

对以下三个业务文件记录路径、大小和 SHA-256：

output/iptv.m3u

output/iptv.txt

output/subscription_info.json

Manifest 不记录自身 SHA。

发布统计

本次频道数量。

本次线路数量。

上次成功频道数量。

上次成功线路数量。

首发时上次统计值为 null，不得伪造为 0。

成功时间

last_successful_daily_update_at：UTC 时间。

last_successful_daily_target_slot：北京时间目标时段。

保护状态

publish_blocked

publish_block_reason

第一层状态。

第二层状态。

第三层状态。

program_connectivity

Raw 检查分类及结果。

Manifest 必须通过 publish_manifest.schema.json 校验。

12.3 CandidateManifest 与 SubscriptionInfo

CandidateManifest 必须包含：

Schema 版本。

生成时间。

source_commit_sha。

Candidate M3U/TXT SHA-256。

正式四文件基准 SHA-256。

第一层状态。

频道数量。

线路数量。

SubscriptionInfo 必须包含正式订阅的生成时间、频道数量、线路数量、线路状态和必要的订阅说明。

两者分别通过：

candidate_manifest.schema.json

subscription_info.schema.json

校验。

12.4 Schema 原则

所有正式数据结构必须通过对应 JSON Schema。

必填字段、类型、枚举、时间格式、SHA 格式、空值规则均必须写入 Schema。

不得只依赖 Python 代码隐式约定。

Schema 校验失败不得继续发布。

12.5 报告保留

运行报告至少保留 30 天。

报告上传必须设置为工作流结束时仍执行的步骤，避免前序任务失败后丢失报告。

报告上传失败必须在可用日志中明确记录，不得伪称报告已保存。

13. 退出码与错误类型

13.1 退出码

退出码含义0成功1输入、配置、Schema、全球库核验错误2阶段不可恢复错误3发布保护或发布拒绝4状态不明、阻断写入失败或无法确认远端状态 

13.2 错误类型

统一使用：

ConfigError

SourceError

NetworkError

ValidationError

FormatError

PublishError

退出码和错误类型是两个不同概念，不得混为一谈。

13.3 错误记录

错误必须记录：

错误类型。

错误代码。

所属阶段。

对应来源或频道标识。

简要原因。

是否可重试。

是否影响发布。

发生时间。

不得将敏感 URL、密码、Token 或 Cookie 写入错误报告。

14. 日志、安全与 URL 边界

14.1 日志脱敏

URL 中的 userinfo 整体脱敏。

Query 参数只保留键名，隐藏参数值。

不记录密码、Token、Cookie 或其他敏感凭证。

异常信息不得间接输出完整敏感 URL。

14.2 正式订阅 URL

日志脱敏规则不得应用到正式订阅内容。

正式 M3U/TXT 必须保留完整播放 URL 和完整 Query，不得删除或修改可能影响播放的参数。

14.3 网络安全边界

禁止访问：

私有内网地址。

环回地址。

链路本地地址。

云平台元数据地址。

其他非全球可路由地址。

所有外部网络访问必须遵守第 7 章统一安全规则。

15. 测试清单与验收

15.1 全球库与频道身份

必须测试：

JSON Schema。

全球库统计复算。

validation_summary.json 一致性。

tvg_id 非空和唯一性。

跨频道名称、别名冲突。

非法字符。

默认地区配置。

人工模式和默认模式切换。

用户目标 ID/名称精确匹配。

来源 tvg-id 存在但为空时拒绝。

来源 tvg-id 不匹配时不回退名称。

无 ID 时名称匹配。

名称歧义处理。

重复目标处理。

原始频道顺序保持。

15.2 来源与候选

必须测试：

来源优先级。

同类别原始顺序。

单来源 100 条限制。

有效来源 40 个限制。

总候选 1000 条限制。

人工单条不占来源名额。

失败来源不占有效来源名额。

全部去重来源不占名额。

频道过滤先于截断。

来源停止条件和停止原因记录。

manual.txt M3U/TXT 解析。

单条解析错误不影响其他有效条目。

URL 规范化和全局去重。

15.3 网络安全

必须测试：

DNS A 记录检查。

多 A 记录逐个验证。

DNS Rebinding。

实际连接 IP 与已验证 IP 一致。

Socket peer IP 一致性。

原始 Host。

TLS SNI。

系统 CA 证书验证。

trust_env=False 代理绕过。

不复用旧连接。

重定向每一跳重新检查。

HTTPS 降级拒绝。

内网和云元数据访问拒绝。

HLS 子清单和分片重新执行安全检查。

15.4 调度与资源限制

必须测试：

全局并发 20。

单主机并发 5。

内部等待队列 60。

队列满时未入队任务不计时。

入队后 60 秒等待超时。

单主机满载时跳选其他主机。

资源释放。

取消任务资源回收。

8 秒绝对 deadline。

两次验证共用同一预算。

大量慢响应。

大量超时。

全局并发满载。

单主机并发满载。

15.5 媒体与读取边界

必须测试：

订阅 8 MB 上限。

HLS 清单 1 MB 上限。

TS 64 KB 上限。

缺少 Content-Length 时的流式计数。

HTTP 200 要求。

HTTP 206 拒绝。

TS 连续 5 个同步字节。

HLS 前两个 Variant 顺序。

第一条通过即停止。

子清单最多一层。

每个媒体列表最多一个分片。

无 Variant。

无分片。

不支持加密。

SESSION-KEY 拒绝。

MAP 拒绝。

BYTERANGE 拒绝。

外部音轨和字幕拒绝。

TS 同步失败。

直接媒体非 TS。

15.6 Candidate 与发布

必须测试：

三文件同一 Candidate Commit。

Candidate Manifest SHA 一致。

正式四文件基准记录。

首发四文件全部不存在。

正式文件部分缺失时阻断。

Candidate Commit 祖先关系。

Candidate 父提交一致性。

git show 精确提取。

禁止 checkout 提取。

差异仅限三个 Candidate 文件。

核心代码路径变化阻断。

Candidate SHA 与用户输入一致。

正式 M3U/TXT 字节级一致。

正式四文件同一提交。

推送前远端 HEAD 复核。

推送响应丢失后的远端确认。

15.7 Raw 与双重阻断

必须测试：

passed 正常处理。

unavailable 警告处理。

test_error 警告处理。

content_mismatch 阻断处理。

Issue 建立失败立即退出。

Manifest 写入最多重试 4 次。

每次重试检查远端阻断状态。

Manifest 阻断门禁。

未关闭 Issue 门禁。

Raw SHA 不一致。

人工解除流程。

程序不得自动解除阻断。

15.8 压力测试

必须在 Runner 上执行 1000 候选受控压力测试，覆盖：

候选集中在同一主机。

候选分散在多个主机。

集中与分散混合。

大量慢响应。

等待队列满。

单主机并发满。

全局并发满。

大量超时。

大量连接失败。

任务取消与资源回收。

记录：

候选总量。

成功完成量。

失败量。

队列超时量。

未入队量。

并发峰值。

总耗时。

错误分类。

未实际执行的测试不得标记通过。

15.9 发布门槛

正式发布必须满足：

配置和 Schema 校验通过。

全球频道库核验通过。

核心测试全绿。

Candidate 校验通过。

无发布阻断。

非空订阅。

质量骤降保护通过或有合规豁免。

正式四文件能够同一提交发布。

国内网络状态没有真实证据时标记 unverified，不阻断正常开发和技术层发布。

16. 六阶段实施、开发纪律与最终交付

16.1 六阶段实施

第一阶段：规范冻结

确认 MASTER_PLAN。

冻结目录、参数、接口和安全规则。

确认全球频道库数据结构。

第二阶段：基础框架与前置核验

严格完成：

5.4 → 5.5 → 5.6 → 6.3 → Schema

完成后实现 catalog.py 和基础配置校验。

第三阶段：核心系统

来源采集。

频道身份匹配。

URL 规范化。

网络安全层。

并发调度。

TS/HLS 媒体验证。

线路整理。

第四阶段：生成与首发

M3U/TXT 生成。

Candidate 生成。

Candidate SHA 校验。

正式四文件发布。

首发基准建立。

第五阶段：自动化

每日北京时间 06:17 更新。

手动运行模式。

Actions 并发控制。

Raw 检查。

双重持久化阻断。

RunReport 和 PublishManifest。

漏跑补偿。

第六阶段：扩展

按需评估。任何扩展必须单项验收，不得影响基础直播能力和既有稳定参数。

16.2 开发纪律

本文件是唯一施工依据。

前置核验先于业务实现。

不得跳过已经冻结的接口契约。

不得擅自改变稳定参数。

不得为增加模块数量而拆分不必要文件。

不得引入没有实际必要的持久化数据库。

不得使用评分机制决定线路。

未实际运行的测试不得标绿。

不得把国内未验证状态伪装成已验证。

规范遇到无法实施的条款，必须提供实际证据，经过确认后才能修改。

所有关键核验、方案决定、测试结果和阶段进度必须记录到 PROGRESS.md。

修改规范时必须更新版本或修订记录，不得静默改变规则。

16.3 最终交付标准

最终交付必须具备：

完整全球频道库及其 Schema。

可复算的频道库统计文件。

用户频道选择配置。

来源配置及解析能力。

IPv4 网络安全层。

TS/HLS 验证能力。

中央并发调度器。

每频道最多 3 条线路的订阅生成能力。

Candidate 与正式发布保护。

双重持久化阻断机制。

自动更新和手动运行能力。

结构化报告及 SHA 记录。

完整测试和验收记录。

更新后的 PROGRESS.md。

未达到实际验收条件，不得宣称项目完成。

附录 A：技术参考

HLS：RFC 8216

aiohttp：官方 Client Reference

Python：ipaddress 官方文档

JSON Schema：Draft 2020-12

GitHub Actions：Workflow syntax、Concurrency

全球频道数据：iptv-org 公开列表及数据库

附录 B：正式输出与发布地址约定

正式输出固定为：

output/iptv.m3u

output/iptv.txt

output/subscription_info.json

output/publish_manifest.json

Raw 订阅地址使用 GitHub 仓库对应分支的固定文件路径：

https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.m3u

TXT 地址：

https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.txt

正式订阅地址不得指向 Candidate 目录。

附录 C：修订与进度记录

本文件是唯一规范，不另设长期并行的补充规范。

PROGRESS.md 只记录实施进度、核验结果、测试证据和已完成事项，不得取代本文件。

规范变更必须先说明原因、影响范围和验证方法，经确认后再修改。

任何代码实现必须遵守本文档冻结的参数、接口、安全和发布约束。

文档定稿不代表程序实现完成；每项功能必须以实际代码和测试结果验收。
