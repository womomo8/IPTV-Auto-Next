IPTV-Auto-Next 项目进度

对应总施工依据："MASTER_PLAN.md"

当前规范版本："1.17-G3"

仓库："womomo8/IPTV-Auto-Next"

分支："main"

本次核对基准提交："71a0ff1cb2a834e1966935c6cc7955e371940d1c"

«本文件只记录实际状态、核验依据、测试结果和下一步工作，不替代 "MASTER_PLAN.md" 定义技术规则。计划、草稿和未经执行的测试不得记为已完成。»

1. 项目目标与验证边界

项目目标：自动收集公开或授权的 IPTV 来源，使用全球频道库识别频道身份，根据 "config/channels.txt" 选择频道，筛选符合项目技术要求的 IPv4 直播线路，持续生成并安全发布 M3U/TXT 订阅。

验证分为不同层次：

1. GitHub Runner 内部的程序技术探测。
2. 中国大陆网络下载正式订阅文件。
3. 中国大陆网络请求媒体地址及必要的 HLS 分片。
4. 实际设备和播放器播放反馈。

Runner 内部检查不能证明中国大陆网络可达或设备能够播放。没有真实国内网络证据时，第二、第三层必须保持 "unverified"；这不阻断正常开发。

2. 仓库核对基准

- 仓库："womomo8/IPTV-Auto-Next"
- 分支："main"
- 核对基准提交："71a0ff1cb2a834e1966935c6cc7955e371940d1c"

本次核对记录来自该基准下的仓库文件及既有检查结果。历史上游数据核验结果单独标记，不冒充本次重新下载核验。

3. 核心文档

- "MASTER_PLAN.md"：唯一总施工依据。
- "PROGRESS.md"：实际进度、测试证据和遗留问题。
- "README.md"：项目简介和使用说明。

"README.md" 曾被旧版进度内容覆盖，需用本次提供的 README 完整替换内容恢复项目介绍。

4. 基础环境与 CI

已确认存在的基础文件：

- ".python-version"
- "pyproject.toml"
- "uv.lock"
- ".github/workflows/ci.yml"

最新已核对的 CI 记录：

- Run："43569927246"
- 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43569927246
- 事件："push"
- 结果："success"

该工作流包含 Python 环境设置、uv 锁定依赖检查与安装、Ruff 格式检查、Ruff 代码检查、pytest、"iptv-auto-next --mode test"，以及检查测试是否意外修改仓库文件。

该次 CI 成功只证明当时基础框架检查通过，不代表完整 IPTV 业务功能通过验收。

5. 全球频道库

仓库内全球频道库验证摘要记录：

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

已确认的全球频道库文件：

1. "data/global_channels/channels.json"
2. "data/global_channels/channels.schema.json"
3. "data/global_channels/channel_filter.json"
4. "data/global_channels/channel_filter.schema.json"
5. "data/global_channels/validation_summary.json"

以上统计来自仓库内的验证摘要，不等于本次重新遍历并重新验证完整频道数据。

5.1 频道身份规则

"MASTER_PLAN.md" 已明确以下规则：

- "tvg_id" 必须非空且全局唯一。
- 不同频道的名称或别名允许冲突；名称冲突不代表频道 ID 重复或频道库损坏。
- 用户按名称选择时若匹配多个频道，必须明确报告歧义。
- 精确 "tvg_id" 可以区分同名频道。
- "频道ID@FeedID" 必须拆分，FeedID 不得作为频道 ID。
- 不允许模糊匹配、拼音猜测或自动推断频道身份。
- "selected_country_name_conflict_keys" 是诊断统计，允许非零，不是启动阻断条件。

5.2 上游历史核验记录

以下为既有历史核验记录，并非本次重新下载上游数据复核：

频道数据库：

- 上游仓库："iptv-org/database"
- 锁定 Commit："53b0fa6605dac7c65a0fa151fef4877b10e82151"
- 历史记录显示本地频道 ID、名称和国家字段与该锁定版本对齐。

Feed：

- 历史记录文件："data/feeds.csv"
- 历史记录：45,462 条，覆盖 31,805 个频道 ID。

Streams：

- 上游仓库："iptv-org/iptv"
- 锁定 Commit："f1191d1b8d8d5e76314cfd5690ceec904d26e1a9"
- 历史检查文件："streams/cn.m3u"、"streams/hk.m3u"、"streams/mo.m3u"、"streams/tw.m3u"
- 历史记录总条目：610 条。
- 非空 "tvg-id"：346 条。
- 空 "tvg-id"：264 条。

这些记录只涉及历史数据结构和身份关联核验，不代表媒体线路在线、可播放或中国大陆网络可达。

6. 当前代码与业务功能

此前仓库检查确认，"src/iptv_auto_next/" 仅包含基础入口和数据模型文件：

- "__init__.py"
- "main.py"
- "models.py"

尚未确认实现完整的以下业务能力：

- 全球频道库读取与校验。
- 来源采集与解析。
- IPv4 网络安全访问。
- TS/HLS 媒体验证。
- 频道身份匹配与线路筛选。
- M3U/TXT 订阅生成。
- Candidate 与正式发布保护。
- 完整运行报告生成。

因此，当前不能把项目描述为已经具备完整自动采集、验证和发布能力。

7. Schema 状态与遗留工作

规范要求使用 JSON Schema Draft 2020-12，并分别管理全球频道库 Schema 与运行配置 Schema。

全球频道库 Schema：

- "data/global_channels/channels.schema.json"
- "data/global_channels/channel_filter.schema.json"

其他项目 Schema：

- "schemas/sources.schema.json"
- "schemas/run_report.schema.json"
- "schemas/publish_manifest.schema.json"
- "schemas/candidate_manifest.schema.json"
- "schemas/subscription_info.schema.json"

此前检查发现的遗留事项：

- "schemas/channels.schema.json" 仍需按总规范清理。
- "tests/unit/test_schemas.py" 仍有旧路径引用，需要迁移测试入口。
- 全球频道库的两个 Schema 需要纳入测试。
- 不得只删除旧 Schema 而不迁移相应测试。

8. 输出与发布状态

正式输出路径规划为：

- "output/iptv.m3u"
- "output/iptv.txt"
- "output/subscription_info.json"
- "output/publish_manifest.json"

此前检查未确认这些正式输出文件已经生成，也未确认正式订阅生成和发布工作流已经完成。

预定订阅地址：

- M3U：https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.m3u
- TXT：https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.txt

在对应文件实际生成并发布前，以上地址不能视为可用订阅。

9. 当前实施状态

工作项| 状态
项目总规范| 已有 "MASTER_PLAN.md"
全球频道库文件入库| 已完成
全球频道库统计摘要| 仓库内已有记录
上游频道 ID 对齐| 有历史核验记录
Feed/Streams 结构核验| 有历史核验记录
频道身份规则| 已在 "MASTER_PLAN.md" 明确
Schema 完整校验| 待完成
旧频道 Schema 清理| 待完成
Schema 测试迁移| 待完成
第二阶段整体验收| 未完成
全球频道库读取模块| 未实施
来源采集与解析| 未实施
IPv4 网络安全层| 未实施
TS/HLS 媒体验证| 未实施
线路筛选| 未实施
M3U/TXT 生成| 未实施
Candidate 与正式发布| 未实施
自动更新工作流| 未完成
国内网络订阅及媒体可达性| "unverified"

10. 下一步施工顺序

严格按照 "MASTER_PLAN.md" 的阶段顺序执行：

1. 完成全球频道库及项目其他 Schema 的 Draft 2020-12 校验。
2. 将全球频道库 Schema 纳入测试入口。
3. 迁移旧频道 Schema 测试路径。
4. 删除废弃的 "schemas/channels.schema.json"。
5. 执行完整基础测试并记录实际结果。
6. 第二阶段验收通过后，再开始全球频道库读取模块及后续业务代码。

不得提前标记未完成的业务功能。

11. 进度记录规则

每批实际施工完成后记录：

- 日期及完成事项。
- 涉及文件。
- 实际测试结果。
- GitHub Commit。
- 未解决问题。

不得把计划、草稿或未经执行的测试记为已完成。
