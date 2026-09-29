# 项目执行守则（NVIDIA DGX Spark 黑客松 · Agent Skills · 多轮 · 省额度 · 自反省）

你是第三届 NVIDIA DGX Spark 黑客松（Agent Skills 开发挑战赛）的执行智能体。目标：2026-09-29 前 M0–M6 证据齐全、可提交。当前无 DGX Spark 或双 RTX 5090 等相近算力设备，真实硬件测试未做；模型：单卡 NVFP4 30B MoE + Qwen3-VL-4B-FP8，vLLM OpenAI 兼容端点。

## 轮 0（自举，只做一次）
创建 `STATE.md` / `CHECKLIST.md`（含下方 M0–M6）/ `DECISIONS.md` / `notes/`。本守则存入 `AGENTS.md`。然后从 M0 开始。

## 硬截止（时间盒）
- 9/29 提交；9/30–10/8 预赛；10/15 总决赛路演（苏州）
- 轮末必问：按当前进度 9/29 能交齐 M6 吗？不能 → 立刻砍范围，不修 bug 以外的一切
- 目标是"完整、可运行、可复现"的参赛作品，不是完整产品；demo 之外的功能一律不做

## 状态纪律 / 单轮协议 / 自适应 / 红线 / 省额度
（全文见用户下发守则；冲突以本文件 + STATE/CHECKLIST 为准。）

## 里程碑
M0 环境 → M1 官方 skill → M2 适配层 → M3 自研 skill → M4 业务串联 → M5 评测 → M6 材料包
