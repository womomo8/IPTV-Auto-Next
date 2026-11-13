# PROGRESS.md

# IPTV-Auto-Next 开发进度记录

本文件记录真实开发进度、测试结果和阶段验收情况。未实际执行的测试不得标记为通过。

---

## 当前阶段：第二阶段——仓库与基础框架

状态：进行中。

### 已完成的基础工作

- [x] MASTER_PLAN.md 1.17 已冻结。
- [x] README.md 和 PROGRESS.md 已建立。
- [x] Python 包和命令行入口已建立。
- [x] 基础 RunReport dataclass 已建立。
- [x] Python 版本固定为 3.14.10。
- [x] pyproject.toml 已建立。
- [x] GitHub Actions CI 工作流已建立。
- [x] uv.lock 已提交至仓库根目录。
- [x] GitHub Runner 曾成功执行 uv lock --check。
- [x] GitHub Runner 曾成功执行 uv sync --locked --extra dev。
- [x] 基础 Ruff 检查曾通过。
- [x] 基础 pytest 曾通过：2 passed。
- [x] CLI --mode test 曾通过。

以上基础工作以 CI #21 的成功记录为验收依据，不代表后续 Schema 批次已经通过。

### 基础 CI 成功记录

- 工作流：CI #21
- Run ID：43382908152
- Commit：bf3f3ab808d4437d05f990fab2740a82211a9608
- 结果：success
- 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43382908152

### Schema 批次提交记录

- 最新提交：77621e15c9b02875ede29b4294d01081ffff9465
- 提交内容：六份 JSON Schema、Schema 单元测试及进度记录。
- 当前状态：已提交，尚未通过 CI 验收。

### 最近 CI 运行记录

CI #28：
- Run ID：43384964575
- Commit：77621e15c9b02875ede29b4294d01081ffff9465
- 结果：failure
- 失败位置：Ruff format 检查。
- pytest 和后续步骤未执行。

CI #29：
- Run ID：43385092613
- Commit：77621e15c9b02875ede29b4294d01081ffff9465
- 结果：failure
- 失败位置：tests/unit/test_schemas.py 格式检查。
- pytest 和后续步骤未执行。
- 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43385092613

失败原因已经定位：test_schemas.py 中有一处格式不符合 Ruff 要求。由于格式检查失败，不能将这两次运行视为 Schema 测试通过。

### 本批待验收

- [ ] 六份 Draft 2020-12 JSON Schema 均通过结构检查。
- [ ] 来源配置 Schema 正向和反向测试通过。
- [ ] 频道配置 Schema 正向和反向测试通过。
- [ ] Candidate 四个正式文件基准全有或全无的约束通过测试。
- [ ] subscription_info 状态与证据对应关系通过测试。
- [ ] publish_manifest 文件路径及字段约束通过测试。
- [ ] RunReport Schema 测试通过。
- [ ] Ruff format 检查通过。
- [ ] Ruff lint 检查通过。
- [ ] GitHub Runner 上 pytest 全部通过。
- [ ] CLI --mode test 通过。
- [ ] 第二阶段整体验收完成。

---

## 阶段验收记录

### 第一阶段：立项与技术规范冻结

- [x] MASTER_PLAN.md 1.17 已冻结。
- [x] 项目目标、技术边界和阶段划分已确定。

### 第二阶段：仓库与基础框架

- [x] Python 3.14.10 在 GitHub Runner 安装并使用。
- [x] 依赖锁文件已提交并通过检查。
- [x] 基础 CI 曾经完整通过。
- [ ] 所有配置及持久化数据 Schema 完成并通过测试。
- [ ] 测试工作流不修改正式文件的验收完成。
- [ ] 第二阶段整体验收完成。

### 第三阶段：核心直播系统

尚未开始。

### 第四阶段：订阅生成与首发

尚未开始。

### 第五阶段：自动化与稳定性

尚未开始。

### 第六阶段：扩展能力

尚未开始。

---

## 已确认的实施边界

1. 国内第二层和第三层验证没有真实证据时记录为 unverified。
2. 不使用收费云拨测服务。
3. 每日定时运行时间为北京时间 06:17，UTC cron 为 17 22 * * *。
4. 不采用线路评分系统。
5. 不建立复杂的持久化线路数据库或复杂黑名单。
6. manual.txt 是独立人工订阅入口。
7. 所有 Schema 使用 JSON Schema Draft 2020-12。
8. 运行时对象使用 dataclasses。
9. 未实际执行的验收项目保持未完成状态。
10. Schema 负责结构和可表达的字段关系校验；跨文件 SHA 一致性、跨数组 ID 唯一性等规则必须由运行时逻辑负责。

---

## 下一步

完成本批 Schema 和测试修正，提交后重新运行 GitHub Actions。

必须确认 Ruff、pytest 和 CLI 检查全部通过，并复核 Schema 语义约束后，才能记录本批验收完成。

第二阶段尚未完成前，不进入第三阶段核心直播系统开发。
