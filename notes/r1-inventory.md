# R1 盘点 · footage-guard（Backend · 2026-09-28）

路径根：`D:\DGX Spark黑客松比赛\footage-guard`

| 项 | 就绪 | 缺口 | 今晚可补 |
| --- | --- | --- | --- |
| Skill 入口 | `SKILL.md` + `scripts/run.sh` → `footage_guard.py`；stdout 末行 `MEDIA:/abs` | 无 Windows 一键 `.ps1` 入口（仅 bash `run.sh`） | 写 `scripts/run.ps1` 薄封装 |
| stub VLM | `scripts/vlm_stub_server.py` + `start_vlm_stub.ps1`；`/v1/models`+`chat/completions` smoke 曾 PASS | 默认占 8000；与真 vLLM 端口冲突时需改 `--port` | 在 R2 命令块写清 `FOOTAGE_GUARD_BASE_URL` |
| 样片 | `assets/sample_footage.mp4` 已在仓 | — | — |
| 一键 demo | README/`make_sample.sh`/`run.sh --interval 5` 文档齐 | **无**单一「评委复制即跑」文件；本机 **无 ffmpeg/ffprobe PATH** | **已补** `notes/r2-judge-10min.md` |
| 无 ffmpeg 降级 | `probe.py` 显式报错退出（不装有） | 管线无法抽帧；不能静默出 MEDIA | R2 提供「只读 TEST-REPORT + 离线产物说明」路径 |
| 无真 VLM 降级 | `--no-vlm` 结构模式；端点不通时帧失败降级结构模式（TEST-REPORT T8） | M5 真数不能用 stub/`--no-vlm` 冒充 | R2 分轨：结构 demo vs 真实硬件真跑 |
| 契约/评测文档 | `references/output-contract.md`、`evals/evals.json`、`TEST-REPORT.md`、`BENCHMARK.md`(第二部分 BLOCKED) | 真实硬件冒烟日志空；ffmpeg BLOCKED | 等入口；不造假 |
