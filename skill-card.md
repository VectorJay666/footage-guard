# Skill Card — footage-guard

信任记录。扫描报告回答"机器查到了什么"，签名回答"文件变没变"；这张卡回答"人到底接受了什么"。

## Description / Use Case

> 提交口径：M3+离线 Demo+诚实 BLOCKED（见 `NARRATIVE.md` rev4）。真跑硬件标注双 RTX 5090（x86，相近算力）；Spark/GX10 仅迁移目标。stub ≠ M5。

> 部署现实：默认本机处理；DGX Spark / 真 VLM **可插拔、非必达**。无算力时用 --no-vlm 或本地 stub 验编排，不算 Spark 实测分。

把一段已落地的本地监控/现场录像，变成事件时间线、带时间戳的关键帧拼图和复盘报告。
给安防、园区、零售、活动现场这类需要在本地（数据不出内网）复盘录像、快速定位"发生了什么、什么时候"的团队用。
Agent 触发后的动作：视频探测 → 关键帧抽取 → 本地多模态端点（OpenAI 兼容）逐帧理解 → 事件聚合 → 报告 + 结构化 `events.json`。

## Owner

- 参赛团队 / 个人：**永祺 郑 / 黑客松项目组（footage-guard）**
- 归属：本目录（自研 Skill，随项目分发）

## License / Deployment Geography

- License：Apache-2.0
- 适用地域：全球。数据默认只在本机处理；用户显式指定远端端点时，按该端点所在地域的数据合规要求执行（脚本会打印出网 WARN，SKILL.md 要求先征得用户同意）。

## Requirements / Dependencies

| 依赖 | 必需 | 说明 |
| --- | --- | --- |
| Python ≥ 3.8 | 是 | 只用标准库，没有必装 pip 包 |
| ffmpeg / ffprobe | 是 | 抽帧与元信息（`apt install ffmpeg` / `brew install ffmpeg`） |
| OpenAI 兼容多模态端点 | 是（可降级） | 默认 `http://127.0.0.1:8000/v1`（OpenAI 兼容本地端点：5090/Spark/stub 可插）；`--no-vlm` 走结构模式 |
| Pillow | 否 | 拼图带时间戳标注；没有它拼图退化为无标注网格 |
| 凭据 | 视端点 | `FOOTAGE_GUARD_API_KEY`，本地端点默认 EMPTY；只走环境变量，不落盘、不打印 |

环境变量：`FOOTAGE_GUARD_BASE_URL`、`FOOTAGE_GUARD_API_KEY`、`FOOTAGE_GUARD_TIMEOUT_S`、`FOOTAGE_GUARD_KEYWORDS`。

## Risks & Mitigations

| 风险 | 缓解 |
| --- | --- |
| 误触发（被当成转码/识别/实时工具） | frontmatter 写明 `Not for: 实时告警、身份识别、转码剪辑、单图问答`，触发词窄 |
| 画面被发到远端 | 默认 127.0.0.1；端点非本机时 `vlm_describe.py` 打 WARN，SKILL.md 要求先征得用户同意 |
| 改动输入文件 | 只读原视频、只写 `--out`；不转码、不删除 |
| 身份/属性推断越界 | 系统提示词 + SKILL.md 双层禁止推断身份/年龄/国籍/关系/意图；evals 有对应负向用例 |
| 成本失控（长视频逐帧烧钱） | 帧数上限 `--max-frames`（默认 240，超限自动放大间隔）；帧级缓存，同参数复跑不调端点 |
| 模型选错（选中纯文本模型） | `--model auto` 优先挑 vl/vision/video 命名的模型；可显式指定 |
| 事件切分/关键词误报 | 结果恒标注"需人工复核"，是启发式聚合，不做行为识别承诺 |

## References / Version / Ethical

- References：`README.md` · `TEST-REPORT.md` · `references/workflow.md` · `references/troubleshooting.md` · `references/output-contract.md` · `evals/evals.json` · `BENCHMARK.md`
- Version：1.0.0
- Ethical：不推断个人身份、年龄、国籍、关系、情绪或意图，只输出可观察事实；事件结果强制标注需人工复核；逐帧缓存只存结构化摘要，不落地任何可还原到个人的身份信息。

---
说明：这是自研 Skill 的治理产物。若后续要进官方目录，还需补 SkillSpector 扫描报告、Tier-3 实测和 OMS 签名（见 `BENCHMARK.md`）。
