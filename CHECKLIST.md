# CHECKLIST · M0–M6（footage-guard）

硬件口径：**双 RTX 5090（x86，相近算力）** — 不冒充 GB10/Spark。  
stub 栏与真跑栏分列；未跑不填数。

## M0 环境（Backend 认领）
- [ ] vLLM 起 NVFP4 30B MoE（单卡）冒烟 — 证据：
- [ ] vLLM 起 Qwen3-VL-4B-FP8 冒烟 — 证据：
- [ ] OpenAI 兼容 `GET /v1/models` + 小输入 `POST /v1/chat/completions` — 证据：
- 命令模板：`notes/m0-vllm-smoke.md`（待真机执行后写 `notes/m0-smoke-*.log`）

## M1 官方 skill
- [ ] `npx skills add nvidia/skills` ≥2 — 证据：
- [ ] `model_signing verify` PASS — 证据：
- [ ] skill-card 风险/许可记录 — 证据：

## M2 适配层
- [ ] `env.sh` + `run-official-skill.sh` — 证据：
- [ ] 官方 skill 本机端到端 — 证据：

## M3 自研 skill（footage-guard 已有骨架）
- [x] SKILL.md + references/ + scripts/ + evals + skill-card — 仓库内已有（开发机管线）
- [ ] 5090 真跑复核 — 证据：（待）

## M4 业务串联 / MEDIA
- [ ] 官方+自研衔接 + 末行 `MEDIA:/绝对路径` — 证据：（待；本机缺 ffmpeg BLOCKED）

## M5 评测
- [ ] BENCHMARK 五维真数（禁止 stub 冒充）— 证据：
- [ ] 三帧：造/换/验 — 证据：
- stub 分栏见：`notes/accept-matrix-5090-vs-stub.md`（Test）

## M6 材料
- [x] 叙事/电梯稿/提交清单 — 证据：`NARRATIVE.md` rev4 · `DEMO-SCRIPT.md` · `SUBMIT-PACKAGE.md` · `notes/r1-gap-inventory.md`
- [ ] README 迁移脚本实体 + 视频 + PPT — 证据：（spark.env / 视频待补）

## 旁路（非 M5）
- [x] 开发 stub `/v1` — `scripts/vlm_stub_server.py`（不算 Spark/5090 分）
- [x] 管线 9/9 开发机 `--no-vlm` — `TEST-REPORT.md`
- [ ] ffmpeg PATH — **BLOCKED**（环境）

- [x] R1 验收骨架：`FINAL_ACCEPTANCE.md` + `notes/r1-runnable-blocked-owners.md`；stub 双轮日志 `notes/r1-stub-dual-round.log`（pipeline BLOCKED）

