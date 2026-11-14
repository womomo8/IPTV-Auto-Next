IPTV-Auto-Next

一个基于 Python 的自动化 IPv4 IPTV 直播源收集、验证与订阅生成项目。

项目目标

自动收集公开或授权的直播源，识别频道身份，执行网络安全检查和媒体结构验证，按频道筛选线路，生成 M3U 和 TXT 订阅。

每个频道最多保留 3 条通过项目技术验证的线路。

订阅地址

以下为项目正式输出文件的固定地址。只有在订阅生成和发布工作流完成、文件实际生成后才能使用。

- M3U： https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.m3u
- TXT： https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.txt

验证边界

1. 程序技术验证通过，不代表线路一定能在中国大陆网络访问或正常播放。
2. 国内网络可达性和实际设备播放情况，必须经过对应环境实测；未实测时标记为 "unverified"。
3. 支持 MPEG-TS 直播流，以及符合项目验证规则的 HLS 播放列表（仅支持未加密 MPEG-TS 分片），不绕过 DRM 或付费限制。
4. 全球频道库用于识别频道身份，不代表频道一定存在可用直播线路。

项目状态

当前已具备基础 CI 检查工作流。自动收集、线路验证、订阅生成及正式发布功能，按 "MASTER_PLAN.md" (./MASTER_PLAN.md) 逐步实施。

开发规范

项目架构、实施顺序、技术参数、测试要求和发布保护规则，统一以 "MASTER_PLAN.md" (./MASTER_PLAN.md) 为准。

免责声明

本项目仅供技术交流与学习。使用者应遵守直播源所在地及使用地的法律法规，并自行承担使用风险。
