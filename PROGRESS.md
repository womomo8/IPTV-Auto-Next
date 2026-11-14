IPTV-Auto-Next 项目进度

对应总施工依据：MASTER_PLAN.md
当前规范版本：1.17-G3
仓库：womomo8/IPTV-Auto-Next
分支：main

本文件只记录实际状态、核验依据、测试结果和下一步工作，不替代 MASTER_PLAN.md 定义技术规则。计划、草稿和未经执行的测试不得记为已完成。

---

## 1. 项目目标与验证边界

项目目标：自动收集公开或授权的 IPTV 来源，使用全球频道库识别频道身份，根据 config/channels.txt 选择频道，筛选符合项目技术要求的 IPv4 直播线路，持续生成并安全发布 M3U/TXT 订阅。

验证分为不同层次：

1. GitHub Runner 内部的程序技术探测。
2. 中国大陆网络下载正式订阅文件。
3. 中国大陆网络请求媒体地址及必要的 HLS 分片。
4. 实际设备和播放器播放反馈。

Runner 内部检查不能证明中国大陆网络可达或设备能够播放。没有真实国内网络证据时，第二、第三层必须保持 unverified；这不阻断正常开发。

## 2. 最新仓库与 CI 核验

- 仓库：womomo8/IPTV-Auto-Next
- 分支：main
- 本次核验提交：4f449784cea7d751793a7b27fe963dd21250bc18
- 提交信息：Add files via upload
- CI Run：43575941026
- CI 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43575941026
- CI 结果：success

本次 GitHub-hosted Runner 实际环境：

- Ubuntu 24.04
- CPython 3.14.10
- pytest 9.2.0

本次 CI 全部步骤通过：

- 依赖锁检查与依赖安装。
- Ruff 格式检查。
- Ruff 代码检查。
- pytest：43 passed。
- iptv-auto-next --mode test。
- 测试模式执行后仓库无文件变更。

Ruff 格式检查使用仓库锁定依赖中的 Ruff 0.17.5。此前临时添加的格式化导出步骤已从正式 .github/workflows/ci.yml 恢复移除；当前工作流保留正式检查流程。

本次 CI 只证明当前基础框架、Schema 测试和 test 模式检查通过，不代表完整 IPTV 采集、网络验证、订阅生成或发布功能已经完成。

## 3. 核心文档

- MASTER_PLAN.md：项目唯一总施工依据。
- PROGRESS.md：实际进度、测试证据和遗留问题。
- README.md：项目简介和使用说明。

三份文件的职责保持分离，不以 PROGRESS.md 替代技术规范。

## 4. 全球频道库

仓库内全球频道库文件：

1. data/global_channels/channels.json
2. data/global_channels/channels.schema.json
3. data/global_channels/channel_filter.json
4. data/global_channels/channel_filter.schema.json
5. data/global_channels/validation_summary.json

仓库记录的频道库统计：

- 频道记录：31,805 条。
- 唯一 tvg_id：31,805 个。
- 国家和地区：231 个。
- CN：749 条。
- HK：147 条。
- MO：15 条。
- TW：154 条。
- 类别种类：30。
- 空类别记录：5,376 条。
- channels.json：5,977,691 bytes。

本次 CI 中的 test_validation_summary_matches_actual_global_channel_data 测试已实际比较频道数、唯一 ID 数、国家数、类别数、四个选定地区的频道数、空类别数、文件字节数及 selected_country_name_conflict_keys，测试通过。

本次 CI 还通过了全球频道库 Schema 校验、频道数据 Schema 校验、tvg_id 非空且全局唯一检查，以及频道名称和别名不得含双引号、CR、LF 的检查。

以上证明当前仓库数据通过已实现的静态数据测试；名称歧义索引、运行时频道身份解析和用户频道选择仍需在 catalog 模块中实现并测试。

## 5. 上游数据核验记录

以下为 MASTER_PLAN.md 和既有记录中的固定版本核验结果。本次没有重新下载上游仓库，因此不把它们描述为本次重新核验。

### 5.1 频道数据库与 ID 对齐

- 上游仓库：iptv-org/database
- 锁定 Commit：53b0fa6605dac7c65a0fa151fef4877b10e82151
- 上游文件：data/channels.csv
- 上游频道记录：31,805 条。
- 本地频道记录：31,805 条。
- 历史核验记录：本地与上游频道 ID 双向对齐，频道名称和国家代码一致。
- 历史核验记录：1 条别名重复、1 条类别重复在本地去重；未发现频道 ID 缺失或错误映射。

### 5.2 Feed 与 Streams

Feed：

- 上游仓库：iptv-org/database
- 锁定 Commit：53b0fa6605dac7c65a0fa151fef4877b10e82151
- 文件：data/feeds.csv
- 历史记录：45,462 条 Feed，覆盖 31,805 个频道 ID；频道 ID 与 Feed ID 组合未发现重复。

Streams：

- 上游仓库：iptv-org/iptv
- 锁定 Commit：f1191d1b8d8d5e76314cfd5690ceec904d26e1a9
- 已检查文件：streams/cn.m3u、streams/hk.m3u、streams/mo.m3u、streams/tw.m3u
- 历史记录：610 条；346 条具有非空 tvg-id，264 条 tvg-id 为空。
- 历史记录：346 条非空 ID 均能对应本地频道 ID 和 Feed ID；264 条空 ID 不得通过名称猜测补齐身份。

这些记录只证明固定上游版本的数据结构和身份关联，不证明任何媒体线路可播放或中国大陆网络可达。

## 6. Schema 与测试状态

当前仓库存在并纳入测试的七个 Schema：

- data/global_channels/channels.schema.json
- data/global_channels/channel_filter.schema.json
- schemas/sources.schema.json
- schemas/run_report.schema.json
- schemas/publish_manifest.schema.json
- schemas/candidate_manifest.schema.json
- schemas/subscription_info.schema.json

本次 tests/unit/test_schemas.py 已使用上述七个实际路径，并通过 Draft 2020-12 Schema 自身校验及对应配置/数据校验测试。

旧文件 schemas/channels.schema.json 已不在当前 main 分支文件树中；测试不再引用旧路径。全球频道库唯一 Schema 路径为 data/global_channels/。

本次 pytest 共 43 项通过。Schema 与静态频道数据检查已通过当前测试覆盖；运行时目录加载、身份解析、选择模式和名称歧义行为尚未实现，不得标记为完成。

## 7. 当前代码与业务功能

当前 src/iptv_auto_next/ 已确认包含：

- __init__.py
- main.py
- models.py

models.py 当前只有基础 RunReport 数据模型；尚未实现完整业务数据模型。

尚未实现或尚未验收的业务能力：

- 全球频道库读取、运行时完整性检查和名称歧义索引。
- 用户频道清单解析与目标匹配。
- 来源采集与 M3U/TXT 解析。
- IPv4 网络安全访问。
- TS/HLS 媒体验证。
- 候选调度与线路筛选。
- M3U/TXT 订阅生成。
- Candidate、SHA 校验与正式发布保护。
- 完整运行报告和发布记录。

## 8. 实施阶段状态

| 工作项 | 状态 |
|---|---|
| 项目总规范与三份核心文档 | 已存在，仍需持续保持一致 |
| 全球频道库文件入库 | 已完成 |
| 全球频道库统计摘要与静态数据测试 | 本次 CI 通过 |
| 上游频道 ID 对齐 | 有固定 Commit 的历史核验记录，未在本次重跑 |
| Feed/Streams 结构核验 | 有固定 Commit 的历史核验记录，未在本次重跑 |
| 七个 JSON Schema Draft 2020-12 校验 | 本次 CI 通过 |
| Schema 测试路径迁移 | 已完成，本次 CI 通过 |
| 废弃 schemas/channels.schema.json 清理 | 当前 main 分支已不存在 |
| Ruff 格式和代码检查 | 本次 CI 通过 |
| pytest | 本次 43 项通过 |
| test 模式入口及仓库无变更检查 | 本次 CI 通过 |
| 第二阶段整体验收 | 未完成 |
| catalog 模块及身份匹配 | 未实施 |
| 来源采集与解析 | 未实施 |
| IPv4 网络安全层 | 未实施 |
| TS/HLS 媒体验证 | 未实施 |
| 线路筛选 | 未实施 |
| M3U/TXT 生成 | 未实施 |
| Candidate 与正式发布 | 未实施 |
| 自动更新工作流 | 未完成 |
| 国内网络订阅及媒体可达性 | unverified |

## 9. 下一步施工顺序

按照 MASTER_PLAN.md 的绝对前置序列，静态频道数据核验、上游历史核验记录、接口规范定义和七个 Schema 测试已经具备记录依据。下一步进入全球频道库读取与身份处理模块，但必须先按 MASTER_PLAN.md 第6.3节实现并测试接口，不得扩展成来源采集或网络验证功能。

下一项工作：

1. 新建 src/iptv_auto_next/catalog.py，实现全球频道库加载和运行时完整性校验。
2. 建立规范化名称/别名索引，保留名称歧义，不因歧义导致整个频道库加载失败。
3. 实现用户频道清单的人工模式与默认模式解析。
4. 实现 tvg_id 精确匹配、名称精确匹配、歧义报错，以及频道ID@FeedID 拆分。
5. 为上述行为编写单元测试，覆盖 MASTER_PLAN.md 第5.3节列出的冲突和边界案例。
6. 运行 GitHub Actions，全部通过后再记录 catalog 阶段结果。

在 catalog 接口和测试通过前，不开始来源采集、网络访问、媒体验证或订阅生成模块。

## 10. 进度记录规则

每批实际施工完成后记录日期、涉及文件、实际测试结果、GitHub Commit 和未解决问题。不得把计划、草稿、历史数据或未经执行的测试记为本次已完成。
