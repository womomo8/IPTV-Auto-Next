# PROGRESS.md

# IPTV-Auto-Next 开发进度记录

本文件用于记录项目的真实开发进度、测试结果和阶段验收情况。所有开发人员必须严格遵守 `MASTER_PLAN.md` 的规范。未实际执行的测试不得标记为通过。

---

## 当前阶段：第二阶段：仓库与基础框架（进行中）

### 第一阶段交付确认
- [x] `MASTER_PLAN.md` 1.17 终极定稿版冻结完成。
- [x] `PROGRESS.md` 初始化。
- [x] `README.md` 初始化。
- [x] 第一阶段规范冻结验收完成。

### 第二阶段当前进展
- [x] 已建立初始 Python 包、命令行入口、基础 dataclass 和单元测试文件。
- [x] `.python-version` 已写入 Python `3.14.10`。
- [x] `pyproject.toml` 已建立，声明运行依赖和开发依赖。
- [x] GitHub Actions 已建立 Ubuntu 24.04 CI 工作流。
- [x] GitHub Runner 已实际安装并使用 Python 3.14.10。
- [x] GitHub Runner 已成功执行 `uv lock` 并生成 `uv.lock` Artifact。
- [x] GitHub Runner 已成功执行 `uv sync --locked --extra dev`。
- [ ] `uv.lock` 已提交到仓库根目录（Artifact 已生成，待纳入仓库提交）。
- [ ] Ruff 格式和 lint 检查全部通过。
- [ ] GitHub Runner 上 pytest 全部通过。
- [ ] CLI test 模式在 GitHub Runner 上通过。
- [ ] 六份 JSON Schema 及对应测试完成。
- [ ] 第二阶段整体验收完成。

### 当前 CI 证据

- 最新检查：GitHub Actions CI Run #18。
- 运行地址：https://github.com/womomo8/IPTV-Auto-Next/actions/runs/43381840038
- Runner：GitHub-hosted Ubuntu 24.04。
- Python：3.14.10，安装成功。
- uv：0.10.0，安装成功。
- `uv lock`：成功，生成 `uv-lock-bootstrap` Artifact。
- `uv sync --locked --extra dev`：成功。
- Ruff：格式检查失败，定位到 `src/iptv_auto_next/main.py` 的 `finished_at` 字段换行格式。
- pytest：因前置 Ruff 步骤失败而跳过，尚无本轮 Runner 测试结果。
- CLI test：因前置 Ruff 步骤失败而跳过，尚无本轮 Runner 测试结果。
- Artifact：`uv-lock-bootstrap`，Artifact ID `14016503126`，包含由上述 Runner 生成的 `uv.lock`。

本地历史验证记录：
- Python 3.13.5 环境下，基础单元测试曾通过：2 passed。
- Python 3.13.5 的结果不能替代 MASTER_PLAN 要求的 Python 3.14.10 GitHub Runner 验收。

当前阻塞项：修正 `main.py` 格式并将 Runner 生成的 `uv.lock` 纳入仓库后，重新运行 CI，完成 Ruff、pytest 和 CLI 验收。

---

## 阶段验收记录

### [第二阶段] 仓库与基础框架（进行中）
- [ ] 完整目录结构搭建完成。
- [x] Python 3.14.10 在 GitHub Runner 成功安装并实际使用。
- [ ] 依赖锁文件 `uv.lock` 已提交到仓库并通过 `uv lock --check`。
- [ ] 基础 JSON Schema 编写及测试完成。
- [ ] CI 基础测试流（Ruff、pytest、test 模式）全部跑通。
- [ ] 测试工作流不修改正式文件的验收完成。

### [第三阶段] 核心直播系统（未开始）
- [ ] `network.py` 网络安全、IPv4 校验、防 SSRF/DNS Rebinding 逻辑完成。
- [ ] 8 秒总预算绝对 Deadline 调度器完成。
- [ ] 1000 候选受控压力测试通过。
- [ ] HLS 解析边界（拒绝 fMP4、加密、ByteRange 等）完成。
- [ ] 频道精确匹配与去重截断逻辑完成。

### [第四阶段] 订阅生成与首发（未开始）
- [ ] M3U 和 TXT 双格式生成器完成。
- [ ] 双格式一致性校验器完成。
- [ ] Candidate 生成、Manifest 记录及 SHA 防篡改校验完成。
- [ ] 正式发布保护（非空、骤降 50%）完成。
- [ ] 首发流程人工验证通过。

### [第五阶段] 自动化与稳定性（未开始）
- [ ] 06:17 定时任务及漏运行补偿机制完成。
- [ ] GitHub Actions `queue: max` 并发互斥配置完成。
- [ ] 远端状态核对与 Git 冲突重试机制完成。
- [ ] Raw 程序侧检查与 Issue 阻断双重持久化机制完成。

### [第六阶段] 扩展能力（未开始）
- [ ] 按实际需要评估并实施独立扩展。

---

## 关键决策与问题记录

### 已确认的边界与参数
1. **国内实测与首发解耦**：首版首发和日常更新强制依赖第一层程序探测，第二、三层国内验证默认为 `unverified`，不阻断发布。
2. **HLS 格式边界**：遇到 `EXT-X-MAP`、`EXT-X-BYTERANGE`、`EXT-X-SESSION-KEY` 及其他不支持的加密格式，按 `MASTER_PLAN.md` 规定拒绝。
3. **双重验证共享 8 秒**：两次短验证共用 8 秒绝对 deadline，超时不再进行第二次。
4. **Issue 作为阻断锚点**：Git 冲突导致 Manifest 无法写入阻断标记时，必须依靠 GitHub Issue 建立持久化阻断防线。
5. **Python 3.14 验证要求**：必须在 GitHub Runner 实际跑通，失败后记录证据才允许降级到 3.13。
6. **首轮 CI 当前结果**：Python 3.14.10 安装、uv lock 和依赖安装均已成功；当前失败点为 Ruff 格式检查，pytest 和 CLI 检查尚未执行。
