# IPTV-Auto-Next 开发进度记录

本文件记录仓库实际状态、测试结果和阶段验收情况。
未实际执行的项目不得标记为通过。

---

## 一、当前阶段

- 阶段：第二阶段——仓库与基础框架
- 状态：进行中，尚未完成整体验收
- 分支：main
- 最近一次 CI：#39
- 最近一次 CI 结果：success
- 最近一次 CI 验证提交：`8d995cd5a8b4f7296e25f4c9131b4d44892460f6`

## 二、已完成工作

### 2.1 Python 环境与仓库基础

- [x] Python 包目录和命令行入口已建立。
- [x] Python 版本固定为 3.14.10。
- [x] pyproject.toml 已建立。
- [x] uv.lock 已提交。
- [x] GitHub Actions 基础 CI 已建立。
- [x] 第三方 GitHub Actions 均固定到完整 commit SHA。
- [x] CI 使用 Ubuntu 24.04。
- [x] Python 版本由 .python-version 统一指定。

### 2.2 JSON Schema

- [x] sources.schema.json 已建立。
- [x] channels.schema.json 已建立。
- [x] run_report.schema.json 已建立。
- [x] publish_manifest.schema.json 已建立。
- [x] candidate_manifest.schema.json 已建立。
- [x] subscription_info.schema.json 已建立。
- [x] 六份 Schema 的 Draft 2020-12 结构检查通过。
- [x] 当前 Schema 正反向基础测试通过。

说明：

Schema 通过不代表运行时规则全部完成。

来源 ID 跨数组全局唯一、频道别名冲突、跨文件 SHA 一致性等规则，仍须在对应运行时实现阶段完成。

RunReport 当前只有基础 dataclass，完整字段和统计结构尚未实现。

### 2.3 基础运行与测试

- [x] uv lock --check 通过。
- [x] uv sync --locked --extra dev 通过。
- [x] Ruff format 检查通过。
- [x] Ruff lint 检查通过。
- [x] pytest 测试通过。
- [x] iptv-auto-next --mode test 运行通过。
- [x] test 模式能够输出 JSON 运行报告。
- [x] CI 已增加工作区完整性检查。
- [x] 工作区完整性检查通过，未发现测试运行产生的仓库文件变更。

## 三、GitHub Actions 验收记录

### 最新成功记录

- 工作流：CI #39
- Run ID：43387422099
- Commit：`8d995cd5a8b4f7296e25f4c9131b4d44892460f6`
- 结果：success

运行记录：

https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43387422099

以下步骤全部通过：

1. Check out repository
2. Set up Python
3. Set up uv
4. Check or bootstrap dependency lock
5. Install locked dependencies
6. Check formatting and lint
7. Run unit tests
8. Verify test-mode entry point
9. Verify test mode leaves the repository unchanged
10. Upload dependency lock file

### 历史测试记录

CI #37：

- Run ID：43386714124
- 结果：success
- pytest：30 passed

https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43386714124

此前出现过的 Ruff 格式检查失败，已由后续提交修正，不属于当前 main 分支的最新状态。

## 四、第二阶段尚未完成的工作

### 4.1 配置和输入文件

- [ ] 建立 config/sources.json。
- [ ] 建立 config/channels.json。
- [ ] 建立 config/channels.txt。
- [ ] 建立仓库根目录 manual.txt。
- [ ] 对实际配置文件执行 Schema 校验。
- [ ] 核对初始频道字典的来源、字段映射和数据完整性。

### 4.2 目录结构

- [x] schemas/
- [x] src/iptv_auto_next/
- [x] tests/unit/
- [ ] tests/integration/
- [ ] tests/acceptance/
- [ ] config/

说明：

不得为了让目录树看起来完整而创建没有用途的空模块。
后续目录应随实际测试和功能实现建立。

正式 output 文件和 Candidate 文件属于后续阶段交付，不得提前伪造正式成品。

### 4.3 基础框架

- [x] 最小 RunReport dataclass。
- [x] test 模式入口。
- [ ] 对照 MASTER_PLAN 完成基础配置加载和校验准备。
- [ ] 完成第二阶段目录结构和配置文件验收。

## 五、实施边界

1. 国内第二层和第三层没有真实证据时保持 `unverified`。
2. 不使用收费云拨测服务。
3. 每日定时更新为北京时间 06:17，UTC cron 为 `17 22 * * *`。
4. 不采用线路评分系统。
5. 不建立复杂持久化线路数据库或复杂黑名单。
6. manual.txt 是独立人工订阅入口。
7. 所有 Schema 使用 JSON Schema Draft 2020-12。
8. 运行时对象使用 dataclasses。
9. Schema 负责结构校验，跨字段和跨文件规则由运行时逻辑负责。
10. 未实际执行的验收项目保持未完成状态。
11. test 模式不得修改正式文件。
12. 所有阶段严格按照 MASTER_PLAN.md 顺序推进。
13. 不得将计划或理论可行性描述成已经实现。

## 六、下一步

先完成第二阶段缺失的配置文件和目录结构。

初始频道字典必须依据指定数据源生成，并执行完整性、重复身份和别名冲突检查，不得使用猜测数据代替。

配置文件建立后，补齐对应的单元测试和必要 Fixture 测试。

完成第二阶段全部交付与验收后，才能进入第三阶段核心直播系统。
