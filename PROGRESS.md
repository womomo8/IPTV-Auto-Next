
# PROGRESS.md

# IPTV-Auto-Next 开发进度记录

本文件记录真实开发进度、测试结果和阶段验收情况。未实际执行的测试不得标记为通过。

---

## 当前阶段：第二阶段——仓库与基础框架

状态：进行中。

### 已完成

- [x] MASTER_PLAN.md 1.17 已冻结。
- [x] README.md 和 PROGRESS.md 已建立。
- [x] Python 包和命令行入口已建立。
- [x] 基础 RunReport dataclass 已建立。
- [x] Python 版本固定为 3.14.10。
- [x] pyproject.toml 已建立。
- [x] GitHub Actions CI 工作流已建立。
- [x] uv.lock 已提交至仓库根目录。
- [x] GitHub Runner 成功执行 uv lock --check。
- [x] GitHub Runner 成功执行 uv sync --locked --extra dev。
- [x] Ruff format 检查通过。
- [x] Ruff lint 检查通过。
- [x] pytest 通过：2 passed。
- [x] CLI --mode test 通过。

### 最新 CI 验收证据

- 工作流：CI #21
- Run ID：43382908152
- Commit：bf3f3ab808d4437d05f990fab2740a82211a9608
- 结果：success
- 地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43382908152

CI #19 和 #20 曾因 main.py 中 finished_at 的格式问题失败。随后修正，并在 CI #21 完整通过。

### 本批待验收

- [ ] 六份 Draft 2020-12 JSON Schema。
- [ ] Schema 单元测试。
- [ ] GitHub Runner 上 Schema 测试通过。
- [ ] 第二阶段整体验收。

---

## 阶段验收记录

### 第二阶段：仓库与基础框架

- [x] Python 3.14.10 在 GitHub Runner 安装并使用。
- [x] 依赖锁文件已提交并通过检查。
- [x] CI 基础测试流通过。
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

---

## 下一步

完成 Schema 对应的配置加载和校验实现，并通过 GitHub Actions 验收。
