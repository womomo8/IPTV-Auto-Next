
# PROGRESS.md

# IPTV-Auto-Next 开发进度记录

本文件记录仓库真实状态、已执行测试和阶段验收结果。未实际执行的项目不得标记为通过。

---

## 当前阶段

- 阶段：第二阶段——仓库与基础框架
- 状态：进行中，尚未完成整体验收
- 当前分支：main
- 当前最新提交：`b10a9cbf043fd28913868db9216e29dfa02dca06`
- 最新 CI：#37，结果 success

## 第二阶段已完成工作

### 仓库与环境

- [x] Python 包目录和命令行入口已建立。
- [x] Python 版本固定为 3.14.10。
- [x] `pyproject.toml` 已建立。
- [x] `uv.lock` 已提交。
- [x] GitHub Actions 基础 CI 已建立。
- [x] 第三方 GitHub Actions 均固定到完整 commit SHA。
- [x] CI 使用 Ubuntu 24.04 和 `.python-version` 指定的 Python 版本。

### Schema 与测试

- [x] 六份 JSON Schema 已提交。
- [x] 六份 Schema 的 Draft 2020-12 结构检查通过。
- [x] 当前 Schema 单元测试已通过。
- [x] 来源和频道配置的基础正反向测试已建立。
- [x] Candidate 四个正式文件基准全空或全有的约束已有测试。
- [x] 订阅信息验证状态与证据关系已有测试。
- [x] PublishManifest 正式文件路径及历史统计约束已有测试。
- [x] RunReport Schema 不完整数据拒绝测试已建立。

说明：Schema 结构检查和当前单元测试通过，不代表运行时规则已经全部实现。来源 ID 跨数组全局唯一、频道别名冲突、证据 SHA 与正式文件 SHA 一致等规则，仍须由后续运行时配置检查或发布逻辑实现并测试。RunReport 当前仅有基础 dataclass，完整报告字段将在对应实现阶段补齐；不得把基础模型描述为完整报告系统。

### 基础运行

- [x] `uv lock --check` 在 GitHub Runner 通过。
- [x] `uv sync --locked --extra dev` 在 GitHub Runner 通过。
- [x] Ruff format 检查通过。
- [x] Ruff lint 检查通过。
- [x] pytest 全部通过：30 passed。
- [x] `iptv-auto-next --mode test` 在 GitHub Runner 通过。
- [x] 最小 RunReport dataclass 和 JSON 输出入口已建立。

## GitHub Actions 验收记录

### 最新成功记录

- 工作流：CI #37
- Run ID：43386714124
- Commit：`b10a9cbf043fd28913868db9216e29dfa02dca06`
- 结果：success
- pytest：30 passed
- 运行记录：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43386714124

CI #37 的以下步骤均成功：

1. Check out repository
2. Set up Python
3. Set up uv
4. Check or bootstrap dependency lock
5. Install locked dependencies
6. Check formatting and lint
7. Run unit tests
8. Verify test-mode entry point
9. Upload dependency lock file

### 历史失败记录

此前 Schema 文件和测试分批提交时出现过 Ruff 格式检查失败。相关失败提交已由后续提交修正。不得将这些旧失败记录误认为当前 main 分支仍然失败；当前最新结果以 CI #37 为准。

## 第二阶段剩余验收

- [ ] 在 CI 中增加工作区完整性检查，确认单元测试和 `--mode test` 不修改或生成仓库文件。
- [ ] 在 GitHub Runner 上验证新增工作区完整性检查通过。
- [ ] 复核第二阶段目录结构与交付范围，确认没有遗漏必要目录，也不创建无用途的空模块。
- [ ] 完成第二阶段整体验收后，才进入第三阶段核心直播系统。

## 后续实施边界

1. 国内第二层和第三层没有真实证据时必须记录为 `unverified`。
2. 不使用收费云拨测服务。
3. 每日定时更新为北京时间 06:17，UTC cron 为 `17 22 * * *`。
4. 不采用线路评分系统。
5. 不建立复杂的持久化线路数据库或复杂黑名单。
6. `manual.txt` 是独立人工订阅入口。
7. 所有 Schema 使用 JSON Schema Draft 2020-12。
8. 运行时对象使用 dataclasses。
9. Schema 负责结构校验；跨数组唯一性、跨文件 SHA 一致性等规则由运行时逻辑负责。
10. 未实际执行的验收项目保持未完成状态。
11. 正式文件不得由 test 模式或只读 CI 工作流修改。
12. 所有阶段严格按 `MASTER_PLAN.md` 的交付和验收顺序推进。

## 下一步

先完成 CI 工作区完整性检查并通过 GitHub Runner 验收。确认第二阶段交付范围和目录结构无遗漏后，完成第二阶段验收，再启动第三阶段。不得提前把未实现的网络访问、来源采集或媒体验证能力标记为已完成。
