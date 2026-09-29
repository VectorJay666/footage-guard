# R1 缩范围 · 可跑 / BLOCKED / 责任人（Test · 2026-09-28 21:34 CST）

约束：无 ffmpeg、无真 VLM（无相近算力设备入口）。stub 不算 M5 分。

| ID | 无 ffmpeg / 无真 VLM 下 | 责任人 | 说明 |
| --- | --- | --- | --- |
| E-models GET /v1/models（stub） | **能跑** | Backend(stub) / Test(验) | 双轮 PASS → `notes/r1-stub-dual-round.log` |
| E-chat POST /v1/chat/completions（stub） | **能跑** | Backend / Test | 双轮 PASS（固定 JSON + stub:true） |
| E-health GET /health（stub） | **能跑** | Backend / Test | 随 stub |
| E-pipeline `--no-vlm` / 接 stub | **BLOCKED** | Ops(ffmpeg PATH) | `where ffprobe` 空；PROBE 失败 |
| pos-1-full-pipeline | **BLOCKED** | Ops+Backend(Agent) | 需 ffmpeg + Agent |
| pos-2-range-and-focus | **BLOCKED** | Ops+Backend | 同上 |
| pos-3-no-vlm-fallback | **BLOCKED** | Ops | 需 ffmpeg（可不需 VLM） |
| pos-4-cache-reuse | **BLOCKED** | Ops+Backend | 需 ffmpeg + stub/VLM |
| neg-1-identity | **BLOCKED** | Backend(Agent 运行时) | 纯 Agent 行为，无脚本代跑 |
| neg-2-transcode | **BLOCKED** | Backend(Agent) | 同上 |
| neg-3-realtime | **BLOCKED** | Backend(Agent) | 同上 |
| M5 五维 BENCHMARK | **BLOCKED** | Backend+Infra | 须真实硬件真跑；禁止填 stub 数 |
| 开发机 TEST-REPORT 9+4 | 历史证据（非 R1 本机复跑） | — | 仅作管线旁证，不进 M5 |

打回：Ops → 装回 ffmpeg 并回 PATH；Infra/用户 → 相近算力设备入口；Backend → Agent 运行时跑 neg。
