# 提交包清单 · footage-guard（R4 冻结）

> **清单已冻结** · 对照源：`notes/r4-submit-tree.md`（40 文件，排除 `__pycache__`/`out`）  
> 评委默认轨 A：离线文档 + 诚实 BLOCKED。禁止暗示 Spark/真 VLM 已出分；stub ≠ M5。

## 故意不交（不是漏文件）

| 路径 / 项 | 原因 |
| --- | --- |
| `spark.env` + Spark/GX10 迁移脚本 | **故意不交**：环境未就绪；入口到了再由 Backend/Infra 补实体 |
| `notes/m0-smoke-*.log` | **BLOCKED**：无工作站 / 双 5090 入口，无真冒烟日志 |
| `BENCHMARK.md` 五维真数 | **BLOCKED**：未真跑；空栏不填假数 |
| `__pycache__/` · `out/` | 构建/运行产物，不进提交包 |

## 必交面（评委入口）

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` · `skill-card.md` · `evals/evals.json` | Skill / 信任卡 / 边界用例 |
| `BENCHMARK.md` · `TEST-REPORT.md` | 管线证据 + 五维空栏诚实 BLOCKED |
| `README.md` | 复现；含评委 10min 与 spark.env「故意不交」口径 |
| `NARRATIVE.md` · `DEMO-SCRIPT.md` | 叙事终稿 + 电梯 / Demo 步骤 |
| `notes/r2-judge-10min.md` | 评委 10 分钟复制块（默认轨 A） |
| `notes/FINAL_ACCEPTANCE.md` | Test 验收权威表（根目录 `FINAL_ACCEPTANCE.md` 仅为入口指针） |
| `scripts/`（含 `run.ps1` / `run.sh` / stub） | 可跑入口；根目录无 `run.ps1`，以 `scripts/run.ps1` 为准 |
| `references/` | workflow / output-contract / troubleshooting |

## 仓内实档（与 r4-submit-tree 一致 · 40）

```
AGENTS.md
assets/make_sample.sh
assets/README.md
assets/sample_footage.mp4
BENCHMARK.md
CHECKLIST.md
DECISIONS.md
DEMO-SCRIPT.md
evals/evals.json
FINAL_ACCEPTANCE.md
NARRATIVE.md
notes/accept-matrix-5090-vs-stub.md
notes/m0-vllm-smoke.md
notes/r1-gap-inventory.md
notes/r1-inventory.md
notes/r1-runnable-blocked-owners.md
notes/r1-stub-dual-round.log
notes/r2-judge-10min.md
notes/r3-round-log.txt
notes/README.md
README.md
references/output-contract.md
references/troubleshooting.md
references/workflow.md
scripts/build_timeline.py
scripts/extract_frames.py
scripts/footage_guard.py
scripts/install.sh
scripts/probe.py
scripts/requirements.txt
scripts/run.ps1
scripts/run.sh
scripts/start_vlm_stub.ps1
scripts/vlm_describe.py
scripts/vlm_stub_server.py
skill-card.md
SKILL.md
STATE.md
SUBMIT-PACKAGE.md
TEST-REPORT.md
```

## 清单增补（仓内有、树未列 · 评委仍要看）

| 路径 | 说明 |
| --- | --- |
| `notes/FINAL_ACCEPTANCE.md` | 验收正文（冻结后请 Backend 下一轮把该行补进 `r4-submit-tree.md`） |
| `docs/SUBMIT_PACK.md` | 本清单指针，方便旧链跳转 |
| `notes/r4-submit-tree.md` | 本轮对账源 |

## 提交前自检
- [x] 无「Spark/真 VLM 已出分」暗示  
- [x] `spark.env` 标为故意不交，非漏交  
- [x] `scripts/run.ps1` 在清单内；根无 `run.ps1` 不算缺  
- [x] FINAL_ACCEPTANCE / DEMO-SCRIPT / NARRATIVE / r2-judge-10min 均可打开  
