IPTV-Auto-Next

一个基于 Python 和 GitHub Actions 的 IPv4 IPTV 直播源自动收集、验证与订阅生成项目。

项目目标

自动收集公开或授权的直播源，使用全球频道库识别频道身份，筛选符合项目技术要求的 IPv4 线路，并持续生成 M3U 和 TXT 订阅。

每个频道最多保留 3 条通过项目技术验证的线路。

订阅地址

以下是项目预定的正式订阅地址。只有对应文件实际生成并提交后，地址才可使用。

- M3U：https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.m3u
- TXT：https://raw.githubusercontent.com/womomo8/IPTV-Auto-Next/main/output/iptv.txt

项目状态

目前已有 Python 基础项目框架、全球频道数据库和 GitHub Actions 基础 CI。

自动采集、线路验证、订阅生成和正式发布功能仍在开发中。基础 CI 通过不代表完整 IPTV 功能已经完成。

验证边界

1. 程序技术验证通过，不代表线路一定能在中国大陆网络访问或正常播放。
2. 国内网络可达性和实际设备播放情况，必须有对应环境的真实测试证据；未实测时标记为 "unverified"。
3. 首版支持 MPEG-TS，以及符合项目验证规则的 HLS 播放列表（仅支持未加密 MPEG-TS 分片）。
4. 全球频道库用于识别频道身份，不代表频道一定存在可用直播线路。

开发与进度

- 项目架构、实施顺序、技术参数、测试要求和发布保护规则，以 "MASTER_PLAN.md" (./MASTER_PLAN.md) 为唯一总施工依据。
- 实际进度、测试证据和遗留问题记录在 "PROGRESS.md" (./PROGRESS.md)。

免责声明

本项目仅供技术交流与学习。使用者应遵守直播源所在地及使用地的法律法规，并自行承担使用风险。
