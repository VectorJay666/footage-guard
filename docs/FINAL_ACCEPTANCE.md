# docs/FINAL_ACCEPTANCE.md · 与权威正文同口径

> **权威正文**：[`../notes/FINAL_ACCEPTANCE.md`](../notes/FINAL_ACCEPTANCE.md)（R3 · Test · 2026-09-28）  
> **入口指针**：[`../FINAL_ACCEPTANCE.md`](../FINAL_ACCEPTANCE.md)  
> 本文件不另起叙事；仅做提交包可读入口 + box 冒烟附注。

## 三轨速览（用户机评委口径 · 勿改）

| 轨 | 含义 | 用户机结果 | 证据 |
| --- | --- | --- | --- |
| **A** | 只读文档 / 不要求本机 MEDIA | **PASS**（10/10） | TEST-REPORT · evals · skill-card · NARRATIVE · accept-matrix · … |
| **B** | `--no-vlm` → MEDIA | **BLOCKED** | PATH 无 ffmpeg/ffprobe（laptop） |
| **C 端点** | stub `/v1/models` + chat | **PASS**（双轮，已标 stub） | `notes/r1-stub-dual-round.log` · `notes/r3-round-log.txt` |
| **C 全链路 MEDIA** | stub + 管线 | **BLOCKED** | 同 B，无 ffmpeg |
| **M0 / 真 VLM / BENCHMARK 五维** | 5090 真跑 | **BLOCKED** | 无工作站入口；空栏不填假数 |

## box 副本冒烟附注（2026-09-28 · Asia/Shanghai）

box 环境有 ffmpeg，额外可跑项（**不覆盖**用户机 Verdict；**不算 M5**）：

| 项 | 结果 | 证据 |
| --- | --- | --- |
| B `--no-vlm` → MEDIA | **PASS** | `out/judge-novlm/` + `notes/box-smoke-2026-09-28.log`；末行 `MEDIA:.../montage.jpg` |
| C stub 端点 | **PASS** | 同日志；`footage-guard-vlm-stub` / `stub:true` |
| M0 / Spark / 5090 五维 | **仍 BLOCKED** | 未连机；无假分 |

## 禁止

- 用 box B-PASS 改写用户机 B-BLOCKED 总表  
- 把 stub / `--no-vlm` 写入 BENCHMARK 五维真分  
- 声称已在 DGX Spark / GB10 跑通
