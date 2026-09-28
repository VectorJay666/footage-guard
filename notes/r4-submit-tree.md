# R4 提交包目录核对（仓库内）

根：`footage-guard/`

与 Crea 对齐用：下列为当前仓内文件（已排除 `__pycache__`/`out`）。

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

必交面（对照比赛红线）：
- SKILL.md / skill-card.md / evals/evals.json / BENCHMARK.md / scripts/ / references/
- README（含评委 10min + 5090/spark.env 口径）
- notes/r2-judge-10min.md（评委入口）
- **禁止**把 stub 数字写进 BENCHMARK 五维真值
