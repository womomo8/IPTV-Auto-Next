IPTV-Auto-Next PROGRESS.md

«本文件只记录实际进度、核验结果、测试结果和下一步工作。
唯一总施工依据："MASTER_PLAN.md"
当前规范版本："1.17-G3"
仓库："womomo8/IPTV-Auto-Next"
分支："main"
本次核对基准提交："473544ed1b49ba226a645e7a2705f8d45802a724"»

1. 当前项目阶段

当前处于第二阶段：仓库与基础框架。

第一阶段规范冻结已完成。

第二阶段前置数据核验已完成，6.3 模块接口契约已在 MASTER_PLAN 中明确；6.4 Schema 更新与完整校验尚未完成。

目前只有基础框架和 CI，不具备完整的直播源自动采集、验证、订阅生成及发布能力。

2. 已完成的前置核验

2.1 全球频道库

- 数据路径："data/global_channels/"
- 频道记录：31,805 条。
- 唯一 "tvg_id"：31,805 个。
- 覆盖国家和地区：231 个。
- CN：749 条；HK：147 条；MO：15 条；TW：154 条。
- 类别种类：30。
- 空类别记录：5,376 条。
- 数据文件大小：5,977,691 bytes。
- 上游仓库："iptv-org/database"
- 锁定 Commit："53b0fa6605dac7c65a0fa151fef4877b10e82151"

频道 ID、名称、国家字段与锁定上游版本逐条对齐。重复别名和类别记录已去重。

2.2 Feed / Streams

Feed：

- 上游文件："data/feeds.csv"
- 记录：45,462 条。
- 覆盖频道：31,805 个。
- 频道 ID 均能对应本地全球频道库。
- 未发现重复的频道与 Feed 组合。

Streams：

- 上游仓库："iptv-org/iptv"
- 锁定 Commit："f1191d1b8d8d5e76314cfd5690ceec904d26e1a9"
- 检查文件："streams/cn.m3u"、"streams/hk.m3u"、"streams/mo.m3u"、"streams/tw.m3u"
- 总条目：610 条。
- 非空 "tvg-id"：346 条，身份关联核验通过。
- 空 "tvg-id"：264 条，按规范拒绝，不允许通过名称猜测补齐。

以上是数据结构和身份关联核验，不代表媒体线路可播放。

3. 当前仓库实际状态

3.1 基础环境与 CI

- Python："3.14.10"
- "pyproject.toml"：已存在。
- "uv.lock"：已存在。
- ".python-version"：已存在。
- GitHub Actions：".github/workflows/ci.yml" 已存在。

最新 CI：

- Run："43569079046"
- 对应提交："473544ed1b49ba226a645e7a2705f8d45802a724"
- 结果：success。

实际通过：

- Python 环境设置。
- uv 和锁定依赖安装。
- Ruff 格式检查及代码检查。
- pytest 单元测试。
- "iptv-auto-next --mode test"。
- 测试后仓库无意外文件修改。

这只证明基础 CI 通过，不代表完整业务系统通过验收。

3.2 当前代码

"src/iptv_auto_next/" 目前只有：

- "__init__.py"
- "main.py"
- "models.py"

全球频道读取、来源采集、网络安全、媒体验证、线路筛选、订阅生成、发布保护等业务模块尚未实现。

3.3 当前配置和数据

- "config/sources.json"：目前只有一个 CN 公开发现源。
- "config/channels.txt"：当前为空，按规范进入默认频道范围模式。
- "manual.txt"：当前为空。
- 全球频道库五个文件均已入库。

HK、MO、TW 来源尚未补齐。

3.4 Schema 遗留问题

- 全球频道库两个 Schema 已存在于 "data/global_channels/"。
- 其他项目 Schema 已存在于 "schemas/"。
- "tests/unit/test_schemas.py" 仍从旧 "schemas/" 路径读取频道 Schema。
- 全球频道库两个 Schema 尚未完整纳入测试入口。
- 已废弃的 "schemas/channels.schema.json" 仍然存在。

因此，Schema 完整迁移和验收尚未完成。

3.5 输出和发布

目前仓库尚无：

- "output/iptv.m3u"
- "output/iptv.txt"
- "output/subscription_info.json"
- "output/publish_manifest.json"
- 完整 Candidate 文件组。

当前只有基础 CI，没有正式订阅生成和发布工作流。

4. 当前实施状态

工作项| 状态
第一阶段规范冻结| 已完成
全球频道库数据核验| 已完成
上游频道 ID 对齐| 已完成
Feed/Streams 核验| 已完成
6.3 接口契约规范| 已在 MASTER_PLAN 明确
6.4 Schema 完整校验| 待完成
旧频道 Schema 清理| 待完成
全球频道库 Schema 测试迁移| 待完成
第二阶段整体验收| 未完成
全球频道库读取业务模块| 未实施
来源采集与解析| 未实施
IPv4 安全网络层| 未实施
TS/HLS 媒体验证| 未实施
线路筛选| 未实施
M3U/TXT 生成| 未实施
Candidate 和正式发布| 未实施
每日自动更新| 未实施
国内网络订阅及媒体验证| "unverified"

5. 下一步施工顺序

严格按照 MASTER_PLAN 执行：

1. 核对并落实 6.3 模块接口契约，确保接口、异常和数据结构一致。
2. 完成 6.4 所有指定 Schema 的 Draft 2020-12 校验。
3. 将全球频道库 Schema 纳入测试，迁移旧测试入口。
4. 删除废弃的 "schemas/channels.schema.json"。
5. 执行完整测试，确认第二阶段基础框架验收条件。
6. 第二阶段通过后，再开始全球频道库读取及后续业务模块。

不得提前把未完成的业务模块标记为完成。

6. 后续记录规则

每批实际施工完成后，只追加：

- 日期及完成事项。
- 涉及文件。
- 实际测试结果。
- GitHub Commit。
- 未解决问题。

不重复抄写 MASTER_PLAN 的技术规范，不记录未经执行的测试结果，不把计划当作完成记录。

7. 文件职责

- "MASTER_PLAN.md"：唯一总施工规范。
- "README.md"：项目简介、订阅地址和使用说明。
- "PROGRESS.md"：真实进度、核验依据、测试结果和下一步工作。

每次施工前核对仓库实际状态，每批施工完成后更新本文件。
