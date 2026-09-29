# footage-guard 叙事终稿（Crea&Cons · rev4 · 缩范围可交）

> **9/29 可交口径（砍完美保主干）**  
> 交什么：① M3 自研 Skill 目录（SKILL / scripts / evals / skill-card）② 离线 Demo（已有 report / events / timeline / montage）③ 诚实 BLOCKED（M0/M5 无 DGX Spark 或相近算力设备 = 不填假数）。  
> **不交什么**：冒充 GB10/Spark/5090 已跑的 BENCHMARK 数字；假 curl；「已上卡」话术。  
> 硬件红线：真跑若发生，标注 **双 RTX 5090（x86，相近算力设备）**；Spark/GX10 仅迁移目标。

## 如果大家都这么做，凭什么选我们？
云端 VSS 要整栈；聊天套壳只会复述。  
我们把「本地复盘」做成**可分发 Skill**：窄触发、MEDIA 契约、3 条 neg 写进 evals——评委不用信口头，可以打 SILENT_FAIL。

## 一句话价值
**隐私本地复盘**：监控/现场录像默认不出网 → 事件时间线 + 关键帧拼图 + 复盘报告。端点可插拔；没卡也能 `--no-vlm` 把管线与契约演完。

## 痛点（一击）
30 分钟录像里有用的可能就两分钟——人却得全程拖。上云踩合规。  
痛点不是模型不够大，是**证据链出不了本机、边界行为测不了**。

## Demo 高光（对齐离线可演）
1. 打开已有 `report.md` + `montage.jpg`（不堵 ffmpeg / 不堵入口）。  
2. 指末行契约：`MEDIA:/绝对路径`。  
3. 翻 evals 三条 neg：身份 / 转码 / 实时——该拒却跑 = SILENT_FAIL。  
4. 翻 BENCHMARK：第一部分管线 9/9 PASS；第二部分 **BLOCKED（无入口）**——诚实比满分重要。

## 相对套壳
| 套壳 | 我们 |
| --- | --- |
| 「本地」写在 README | 默认 `127.0.0.1` + 非本机 WARN + 征得同意 |
| 假表刷五维 | stub / 真跑分栏；空栏不填 |
| 锁死一台机器 | 迁移说明待 `spark.env` 进仓后再挂链 |

## 风险（路演主动说）
| 风险 | 怎么说 |
| --- | --- |
| 无相近算力设备入口 | M0/M5 BLOCKED；今日交 M3+离线证据 |
| 本机缺 ffmpeg | 全链路复跑 BLOCKED；Demo 用已生成产物 |
| stub 被误读 | 话术强制：「stub 不算分」 |

## 修订
| 版本 | 说明 |
| --- | --- |
| rev3 | 5090 主口径 + spark.env |
| rev4 | 缩范围终稿：M3+离线 Demo+诚实 BLOCKED |
