# IPTV-Auto-Next

基于 Python 的 IPv4 IPTV 直播源自动收集、技术验证与订阅发布项目。

## 项目目标

自动收集公开或授权的直播源，识别频道，执行网络安全检查和媒体结构验证，筛选有效线路，生成标准 M3U 和 TXT 订阅。

每个频道最多保留三条线路。

## 订阅地址

正式首发完成后使用：

- M3U：<https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.m3u>
- TXT：<https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.txt>

当前仍处于开发阶段，正式订阅尚未发布。

## 验证说明

程序技术探测通过，不代表中国大陆网络一定能够访问媒体地址。

没有真实国内网络验证证据时，国内订阅分发和媒体可达性状态必须保持 `unverified`。

## 开发状态

项目按照 `MASTER_PLAN.md` 规定的六个阶段依次开发和验收。

当前阶段：第二阶段——仓库与基础框架。

## 技术规范

完整架构、技术参数、安全规则、测试要求和发布流程，以 [MASTER_PLAN.md](./MASTER_PLAN.md) 为准。

## 许可与来源

仅处理公开或明确授权的来源，不绕过 DRM、付费墙或认证。
