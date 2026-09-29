# 验收矩阵 · 5090 真跑 / stub 分栏（Test）
日期: 2026-09-28
硬件口径: 相近算力设备—当前未连机，真实硬件测试未做；真跑栏一律空白
标记: PASS / FAIL / SILENT_FAIL / BLOCKED / （空=未跑，禁止填数）
规则: M5 数字只许进「5090 真跑」栏；stub 栏只证编排，不算 Spark/5090 分

## Agent 用例（evals 4+3）

| ID | 5090 真跑 | stub | 备注 |
| --- | --- | --- | --- |
| pos-1-full-pipeline |  | BLOCKED | 本机缺 ffmpeg/ffprobe，管线未接 stub |
| pos-2-range-and-focus |  |  | 未跑 |
| pos-3-no-vlm-fallback |  |  | 未跑（开发机 TEST-REPORT 有 --no-vlm，非本栏） |
| pos-4-cache-reuse |  |  | 未跑 |
| neg-1-identity |  |  | 未跑（需 Agent 运行时） |
| neg-2-transcode |  |  | 未跑 |
| neg-3-realtime |  |  | 未跑 |

## 端点冒烟（编排层）

| ID | 5090 真跑 | stub | 证据 |
| --- | --- | --- | --- |
| E-models GET /v1/models |  | PASS | 2026-09-28 本机 stub:8000 |
| E-chat POST /v1/chat/completions |  | PASS | 固定 JSON，`stub:true` |
| E-pipeline footage_guard→VLM |  | BLOCKED | PATH 无 ffprobe |

## 五维（BENCHMARK 第二部分）

| 维 | 5090 baseline | 5090 with-skill | stub |
| --- | --- | --- | --- |
| Security |  |  | 不算分 |
| Correctness |  |  | 不算分 |
| Discoverability |  |  | 不算分 |
| Effectiveness |  |  | 不算分 |
| Efficiency |  |  | 不算分 |

Verdict: **5090 栏全部未填**；stub 仅端点 2/2 PASS，全链路/Agent/五维未跑。
下一轮: 相近算力设备入口 + ffmpeg 回 PATH 后复跑，只往真跑栏写真数。
