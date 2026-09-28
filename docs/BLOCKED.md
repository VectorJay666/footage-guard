# docs/BLOCKED.md · 诚实阻塞清单（缩范围）

> 与 `notes/FINAL_ACCEPTANCE.md` / `CHECKLIST.md` / `NARRATIVE.md` rev4 同口径。  
> **禁止**用 stub 或口头「差不多」填假 PASS。

## 强制 BLOCKED（9/29 提交时保持）

| ID | 阻塞 | Owner | 说明 |
| --- | --- | --- | --- |
| M0 | 无工作站入口 | 用户 / Infra | 无 SSH/真机；零伪造冒烟日志 |
| M1 | 官方 skill 链未装 | Backend | `npx skills add nvidia/skills` 等未做 |
| M2 | 适配层未落地 | Backend / Infra | `env.sh` / `run-official-skill.sh` / `spark.env` 待落 |
| M5 五维 | 须 5090 真跑 | Test | stub / `--no-vlm` **不算分**；BENCHMARK 第二部分空栏 |
| 真 VLM | 无本地 vLLM 端点 | Backend | 默认 127.0.0.1:8000 未起真模型 |
| 用户机 ffmpeg | PATH 无 ffprobe | Ops | 用户机轨 B/C 全链路 BLOCKED |

## 降级（非 BLOCKED · 可交）

| 能力 | 状态 | 证据 |
| --- | --- | --- |
| M3 自研 Skill 目录 | 可交 | SKILL / scripts / evals / skill-card |
| 轨 A 文档演示 | PASS | notes/FINAL_ACCEPTANCE |
| 离线 Demo 产物 | 可交 | report / events / montage（开发机或 box `out/judge-novlm/`） |
| stub 端点编排自检 | PASS（标 stub） | r1/r3 stub 日志；≠ M5 |
| box `--no-vlm` MEDIA | PASS（环境有 ffmpeg） | `notes/box-smoke-2026-09-28.log`；不改写用户机 B-BLOCKED |

## 评委一句话

「今日交的是可跑 Skill + 离线 Demo + 诚实 BLOCKED 表；有 5090/Spark 只换 OpenAI 兼容端点，不重写 Skill。」
