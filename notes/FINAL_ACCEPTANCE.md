# FINAL_ACCEPTANCE · footage-guard（R3 · Test · 2026-09-28 21:35 CST）

依据：`notes/r1-inventory.md`、`notes/r2-judge-10min.md`  
硬件：双 RTX 5090（x86，相近算力）— **未连机**  
标记：PASS / FAIL / SILENT_FAIL / BLOCKED / （空=未跑）  
复测：可跑项至少两轮；FAIL → 打回 Backend → 再测；BLOCKED 写原因，禁止造假

---

## 轨 A（默认 PASS 标准 · 文档可讲 · 不要求本机 MEDIA）

| ID | R1 | R2 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| A-TEST-REPORT | PASS | PASS | PASS | `TEST-REPORT.md` 在库 |
| A-evals 4pos+3neg | PASS | PASS | PASS | `evals/evals.json` |
| A-skill-card | PASS | PASS | PASS | `skill-card.md` |
| A-NARRATIVE 5090+spark.env | PASS | PASS | PASS | `NARRATIVE.md` |
| A-accept-matrix | PASS | PASS | PASS | `notes/accept-matrix-5090-vs-stub.md` |
| A-output-contract | PASS | PASS | PASS | `references/output-contract.md` |
| A-SKILL | PASS | PASS | PASS | `SKILL.md` |
| A-sample | PASS | PASS | PASS | `assets/sample_footage.mp4` |
| A-r1-inventory | PASS | PASS | PASS | `notes/r1-inventory.md` |
| A-r2-judge | PASS | PASS | PASS | `notes/r2-judge-10min.md` |

**轨 A Verdict：PASS（10/10）** — 文件存在性双轮核对一致；未声称本机出 MEDIA。

---

## 轨 B（需 ffmpeg · `--no-vlm` → `out\judge-novlm` + MEDIA）

| ID | R1 | R2 | 结果 | 原因 / 证据 |
| --- | --- | --- | --- | --- |
| B-novlm-MEDIA | BLOCKED | BLOCKED | BLOCKED | PATH 无 `ffprobe`/`ffmpeg`（`where` 空）；未伪造 MEDIA |

责任人：**Ops**（回 PATH）→ Test 复跑双轮。

---

## 轨 C（stub 必须标注 stub · ≠ M5）

| ID | R1 | R2 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| C-models GET /v1/models | PASS | PASS | PASS | `notes/r3-round-log.txt`；模型 id=`footage-guard-vlm-stub` |
| C-chat POST /v1/chat/completions | PASS | PASS | PASS | 同日志；`stub:true` / STUB 文案 |
| C-pipeline→MEDIA | BLOCKED | BLOCKED | BLOCKED | 无 ffmpeg，无法出 MEDIA；**不算 M5** |

---

## M0 / 真 VLM / BENCHMARK（强制 BLOCKED）

| ID | 结果 | 原因 |
| --- | --- | --- |
| M0 vLLM 冒烟 | BLOCKED | 无工作站入口；零伪造日志 |
| 真 VLM 5090 管线 | BLOCKED | 同上 |
| BENCHMARK 五维填数 | BLOCKED | 须 5090 真跑；stub/`--no-vlm` 不算分 |

---

## R3 总 Verdict

| 轨 | 状态 |
| --- | --- |
| A | **PASS** |
| B | **BLOCKED**（无 ffmpeg） |
| C 端点 | **PASS**（双轮，已标 stub） |
| C 全链路 MEDIA | **BLOCKED** |
| M0/M5 | **BLOCKED** |

本轮 **无 FAIL** → 不打回 Backend 修代码。OPEN 打回：**Ops**=ffmpeg；**用户/Infra**=5090 入口。

下一轮：ffmpeg 回 PATH 后立即跑轨 B 双轮；入口到后跑 M0 再填 5090 栏。
