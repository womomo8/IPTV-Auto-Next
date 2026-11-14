IPTV-Auto-Next 项目进度

对应总施工依据："MASTER_PLAN.md"
当前规范版本：1.17-G3
仓库："womomo8/IPTV-Auto-Next"
分支："main"

本文件只记录实际状态、核验依据、测试结果和下一步工作，不替代 "MASTER_PLAN.md" 定义技术规则。计划、草稿和未经执行的测试不得记为已完成。

---

1. 项目目标与验证边界

项目目标：自动收集公开或授权的 IPTV 来源，使用全球频道库识别频道身份，根据用户频道清单选择频道，筛选符合项目技术要求的 IPv4 直播线路，持续生成并安全发布 M3U/TXT 订阅。

验证分为不同层次：

1. GitHub Runner 内部的程序技术探测。
2. 中国大陆网络下载正式订阅文件。
3. 中国大陆网络请求媒体地址及必要的 HLS 分片。
4. 实际设备和播放器播放反馈。

Runner 内部检查不能证明中国大陆网络可达或设备能够播放。没有真实国内网络证据时，相关状态保持 "unverified"，不阻断正常开发。

2. 最新仓库与 CI 核验

本次实际检查时间：2026-11-14。

- 仓库："womomo8/IPTV-Auto-Next"
- 分支："main"
- 最新提交："1e90f2055a6cf29927efae6dff09b7ef0ccb33c5"
- 提交信息："Delete .github/workflows/upstream-audit.yml"
- CI Run："43578050011"
- CI 编号：第88次
- CI 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43578050011
- CI 结果："success"

本次实际确认：

- 独立工作流 ".github/workflows/upstream-audit.yml" 已从 "main" 分支删除。
- 当前 ".github/workflows/" 目录只保留 "ci.yml"。
- 删除提交触发的 CI Run #88 已完成，结果为 "success"。

当前 "ci.yml" 包含以下检查：

- 依赖锁检查与依赖安装。
- Ruff 格式检查和代码检查。
- pytest 单元测试。
- test 模式入口执行。
- 测试模式执行后仓库无文件变更。
- 依赖锁文件上传步骤。

Run #88 整体结果为成功，说明本次删除后现有基础 CI 正常通过。

本次 CI 不代表上游频道数据、Feed/Streams 关联已经完成核验，也不代表完整 IPTV 采集、网络验证、订阅生成或正式发布功能已经完成。

3. 核心文档

- "MASTER_PLAN.md"：项目唯一总施工依据。
- "PROGRESS.md"：实际进度、测试证据和遗留问题。
- "README.md"：项目简介和使用说明。

三份文件职责保持分离，不以 "PROGRESS.md" 替代技术规范。

4. 全球频道库

仓库内全球频道库文件：

1. "data/global_channels/channels.json"
2. "data/global_channels/channels.schema.json"
3. "data/global_channels/channel_filter.json"
4. "data/global_channels/channel_filter.schema.json"
5. "data/global_channels/validation_summary.json"

当前仓库记录的频道库统计：

- 频道记录：31,805 条。
- 唯一 "tvg_id"：31,805 个。
- 国家和地区：231 个。
- CN：749 条。
- HK：147 条。
- MO：15 条。
- TW：154 条。
- 类别种类：30。
- 空类别记录：5,376 条。
- "channels.json"：5,977,691 bytes。

现有 CI 已通过全球频道库相关静态检查。此前测试覆盖了频道数、唯一 ID 数、国家数、类别数、四个选定地区的频道数、空类别数、文件字节数及 "selected_country_name_conflict_keys" 等静态数据检查。

现有测试还覆盖全球频道库 Schema、频道数据 Schema、"tvg_id" 非空且全局唯一，以及频道名称和别名不得含双引号、CR、LF 等要求。

以上表示当前仓库数据通过现有静态检查，不表示运行时频道身份解析、用户频道选择和名称歧义处理已经实现。

5. 上游数据核验记录

上游核验必须以固定 Commit 为准。历史记录、结构检查和完整自动对照必须明确区分，不能把历史记录写成本次重新核验。

5.1 全球频道库启动前核验（MASTER_PLAN.md 第5.4节）

当前仓库已有全球频道库数据、Schema 和 "validation_summary.json"。

当前已具备的检查依据：

- 频道记录数及唯一 "tvg_id" 数量。
- 国家和地区数量及选定地区记录数。
- 类别数量和空类别数量。
- "channels.json" 文件字节数。
- "selected_country_name_conflict_keys" 统计。
- Schema 和频道数据静态约束。

状态：现有静态数据检查通过。运行时名称歧义索引和频道身份解析仍未实现。

5.2 上游频道 ID 对齐（MASTER_PLAN.md 第5.5节）

上游仓库："iptv-org/database"

锁定 Commit：

"53b0fa6605dac7c65a0fa151fef4877b10e82151"

上游文件："data/channels.csv"

历史记录中曾记录：

- 上游频道记录：31,805 条。
- 本地频道记录：31,805 条。
- 历史核验结果为本地与上游频道 ID 双向对齐。
- 历史核验结果为频道名称和国家代码一致。
- 历史记录提及 1 条重复别名和 1 条重复类别在本地去重。

重要状态说明：

本次没有成功重新读取并自动对照锁定版本的完整 "channels.csv"。上述对齐结果目前作为历史核验记录保留，不记为本次重新执行并验收通过。

尚待下载锁定版本的 "channels.csv"，重新执行自动对照并保存报告。

状态：待本次自动核验确认。

5.3 上游 Feed/Streams（MASTER_PLAN.md 第5.6节）

Feed 上游仓库："iptv-org/database"

锁定 Commit：

"53b0fa6605dac7c65a0fa151fef4877b10e82151"

文件："data/feeds.csv"

历史记录中曾记录：

- Feed 记录：45,462 条。
- 覆盖频道 ID：31,805 个。
- 历史核验记录称频道 ID 与 Feed ID 组合未发现重复。

重要状态说明：

本次尚未重新下载并核验完整 "feeds.csv"，因此上述数量和对应关系仍属于历史记录，不能标记为本次重新验收通过。

Streams 上游仓库："iptv-org/iptv"

锁定 Commit：

"f1191d1b8d8d5e76314cfd5690ceec904d26e1a9"

已检查文件：

- "streams/cn.m3u"
- "streams/hk.m3u"
- "streams/mo.m3u"
- "streams/tw.m3u"

已完成的 Streams 结构统计：

地区| Streams 数量| 非空 tvg-id| 空 tvg-id
CN| 518| 284| 234
HK| 26| 25| 1
MO| 10| 8| 2
TW| 56| 29| 27
合计| 610| 346| 264

已确认：

- 四个地区共 610 条 Streams。
- 346 条具有非空 "tvg-id"。
- 264 条 "tvg-id" 为空。
- 346 条非空 "tvg-id" 均采用 "频道ID@FeedID" 格式。
- 未发现非空 ID 缺少 "@" 或包含多个 "@" 的情况。

尚未完成：

- 将全部 346 条 "频道ID@FeedID" 与锁定版本的 "channels.csv"、"feeds.csv" 进行自动逐条对照。
- 确认所有频道 ID 和 Feed ID 组合均真实存在。

空 "tvg-id" 不得通过名称猜测补齐身份。

状态：Streams 数量和 ID 格式检查已完成；Feed/频道身份关联的完整自动核验待完成。

以上检查只证明数据结构和格式，不代表任何媒体线路可播放，也不代表中国大陆网络可达。

6. Schema 与测试状态

当前仓库存在并纳入测试的七个 Schema：

- "data/global_channels/channels.schema.json"
- "data/global_channels/channel_filter.schema.json"
- "schemas/sources.schema.json"
- "schemas/run_report.schema.json"
- "schemas/publish_manifest.schema.json"
- "schemas/candidate_manifest.schema.json"
- "schemas/subscription_info.schema.json"

现有 CI 的 Schema 相关测试步骤已通过。

旧文件 "schemas/channels.schema.json" 已不在当前 main 分支文件树中；全球频道库 Schema 使用 "data/global_channels/" 下的路径。

重要状态说明：

现有 Schema 测试通过，不等于 MASTER_PLAN.md 第6.3节接口契约已经正式冻结，也不等于第6.4节已经完成基于冻结接口的最终更新与验收。

必须先完成第5.5节和第5.6节的完整上游核验，再按顺序冻结接口契约、检查并更新相关 Schema，最后记录验收证据。

7. 当前代码与业务功能

当前 "src/iptv_auto_next/" 已确认包含：

- "__init__.py"
- "main.py"
- "models.py"

当前 "models.py" 只有基础 RunReport 数据模型。

尚未实现或尚未验收的业务能力：

- 全球频道库运行时加载和完整性检查。
- 名称及别名歧义索引。
- 用户频道清单解析与目标匹配。
- 来源采集与 M3U/TXT 解析。
- IPv4 网络安全访问。
- TS/HLS 媒体验证。
- 候选调度与线路筛选。
- M3U/TXT 订阅生成。
- Candidate、SHA 校验与正式发布保护。
- 完整运行报告和发布记录。

8. 实施阶段状态

工作项| 当前状态
第一阶段规范冻结| 已有 MASTER_PLAN.md、PROGRESS.md、README.md
全球频道库文件入库| 已完成
全球频道库静态数据检查| 现有 CI 通过
第5.4节全球库启动前核验| 现有静态检查通过，运行时功能未实现
第5.5节上游频道 ID 对齐| 有历史核验记录，本次完整自动复核待完成
第5.6节 Feed/Streams 实测| Streams 数量及 ID 格式已检查，Feed 对应关系待自动复核
第6.3节接口契约冻结| 待完成
第6.4节 Schema 更新与最终验收| 待完成
PROGRESS.md 前置核验记录| 待补充后续实际核验报告
Ruff 格式和代码检查| CI Run #88 通过
pytest| CI Run #88 通过
test 模式入口及仓库无变更检查| CI Run #88 通过
独立 upstream-audit 工作流| 已删除，当前只保留 ci.yml
第二阶段整体验收| 未完成
catalog 模块及身份匹配| 未开始
来源采集与解析| 未开始
IPv4 网络安全层| 未开始
TS/HLS 媒体验证| 未开始
线路筛选| 未开始
M3U/TXT 生成| 未开始
Candidate 与正式发布| 未开始
国内网络订阅及媒体可达性| "unverified"

9. 下一步施工顺序

严格按照 "MASTER_PLAN.md" 第2.1节绝对前置序列执行，不得跳步。

当前下一步不是编写 "catalog.py"，也不是重新建立独立工作流。

按以下顺序继续：

1. 完成本次 "PROGRESS.md" 更新并提交，使进度记录与当前真实仓库状态一致。
2. 完成锁定版本 "channels.csv" 的本地频道库与上游频道 ID 双向对照，以及名称、国家代码对照。
3. 完成锁定版本 "feeds.csv" 的频道 ID、Feed ID 和组合重复检查。
4. 将四个地区 Streams 中的非空 "频道ID@FeedID" 与上游频道和 Feed 数据逐条对照。
5. 保存实际核验报告和上游 Commit SHA；核验失败时明确报告差异，不得自动猜测或掩盖。
6. 完成上述核验后，按 MASTER_PLAN.md 第6.3节冻结模块接口契约。
7. 按第6.4节检查、更新并验证相关 JSON Schema。
8. 将第5.4、5.5、5.6、6.3、6.4节的实际结果和证据写入本文件。
9. 以上全部完成并验收后，才开始 "catalog.py" 及依赖全球频道库结构的业务代码。

核验实施方式必须遵守现有仓库结构和项目规范，优先使用现有 CI，不为同一任务额外建立重复工作流或增加无必要文件。具体实施前先检查现有文件和能力，不得未经检查就改动现有 CI。

10. 进度记录规则

每批实际施工完成后记录：

- 实际完成日期。
- 涉及文件。
- 上游数据版本或 Commit SHA（如适用）。
- 实际测试和核验结果。
- GitHub Commit。
- GitHub Actions Run 和结果。
- 尚未解决的问题。

不得把计划、草稿、历史数据或未经执行的测试记为本次已完成。

不得仅凭 CI 成功就宣称尚未实现的业务功能已经完成。
