# docs/DEMO_10MIN.md · 评委 10 分钟路径

> **权威复制块**：[`../notes/r2-judge-10min.md`](../notes/r2-judge-10min.md)  
> **路演话术**：[`../DEMO-SCRIPT.md`](../DEMO-SCRIPT.md)  
> 三轨与 Backend 终稿一致：**默认轨 A**；B=`--no-vlm`；C=stub。

## 建议评委路径（默认）

### 轨 A（默认 · ~3 min · 无 ffmpeg / 无 GPU）

只读核对，不跑管线：

1. `TEST-REPORT.md` — 开发机管线 9/9 PASS（含 `--no-vlm`）
2. `evals/evals.json` — 4 pos + 3 neg
3. `skill-card.md` / `NARRATIVE.md` — 相近算力设备（当前未测）+ spark.env 迁移口径
4. `notes/accept-matrix-5090-vs-stub.md` — 分栏；stub 不算 M5
5. 已有产物：`out/judge-novlm/montage.jpg` + `report.md`（或开发机 `*.footage-guard/`）

口播：「证据在 TEST-REPORT；真 VLM/Agent 分在真实硬件轨，今日 BLOCKED。」

### 轨 B（有 ffmpeg · ~2 min）

```bash
cd footage-guard
python3 scripts/footage_guard.py assets/sample_footage.mp4 --interval 5 --no-vlm --out out/judge-novlm
# Windows:
# .\scripts\run.ps1 assets\sample_footage.mp4 --interval 5 --no-vlm --out "$PWD\out\judge-novlm"
```

期望：`report.md` / `events.json` / `montage.jpg`；stdout 末行 `MEDIA:<abs>/montage.jpg`。

### 轨 C（stub 编排自检 · ≠ M5）

```bash
# 终端 1
python3 scripts/vlm_stub_server.py --port 8000
# 终端 2
export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
curl -s http://127.0.0.1:8000/v1/models
# 有 ffmpeg 时再跑全链路；无则只验端点
```

期望：JSON 含 `footage-guard-vlm-stub` 或 `stub: true`。

### 轨 D（入口到期后 · 今日跳过）

见 `notes/m0-vllm-smoke.md`；数字进 `BENCHMARK.md` 真跑栏。

## box 已验证命令（2026-09-28）

```bash
python3 scripts/footage_guard.py assets/sample_footage.mp4 --interval 5 --no-vlm --out out/judge-novlm
# → EXIT=0 MEDIA:/workspace/footage-guard/out/judge-novlm/montage.jpg
```
