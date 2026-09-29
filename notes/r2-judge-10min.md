# R2 · 评委 10 分钟可跑（复制块）

相关入口：[`../README.md`](../README.md) · [`../TEST-REPORT.md`](../TEST-REPORT.md) · [`r1-inventory.md`](r1-inventory.md)

根目录：
```text
D:\DGX Spark黑客松比赛\footage-guard
```
硬件口径：相近算力设备真跑拿分；当前未实测。**stub / --no-vlm 不算 M5**。

---

## 轨 A — 无 ffmpeg / 无 GPU（今晚本机默认）：只验「已有证据」

**不跑管线。** 打开并核对：

1. `TEST-REPORT.md` — 管线 9/9 PASS（开发机 `--no-vlm`）
2. `evals/evals.json` — 4 正 + 3 负
3. `skill-card.md` / `NARRATIVE.md` — 相近算力设备（当前未测）+ spark.env 迁移口径
4. `notes/accept-matrix-5090-vs-stub.md` — stub 与 5090 分栏

期望产物：无新文件。口播：「管线证据在 TEST-REPORT；真 VLM/Agent 分在真实硬件轨。」

---

## 轨 B — 有 ffmpeg、无 GPU：结构模式 demo（~2 min）

**前置：** `ffmpeg`/`ffprobe` 在 PATH（`where ffmpeg` 有输出）。

```powershell
cd "D:\DGX Spark黑客松比赛\footage-guard"
python scripts\footage_guard.py assets\sample_footage.mp4 --interval 5 --no-vlm --out "$PWD\out\judge-novlm"
```

期望产物（目录 `out\judge-novlm\`）：
- `report.md` / `events.json` / 时间线相关文件
- `frames\` + `montage.jpg`（或等价拼图）
- **stdout 最后一行**：`MEDIA:<绝对路径>\montage.jpg`（或约定媒体文件）

FAIL 信号：无 `MEDIA:` 末行；或缺 report/events。

---

## 轨 C — 有 ffmpeg + stub（编排自检，非 M5）

终端 1：
```powershell
cd "D:\DGX Spark黑客松比赛\footage-guard"
python scripts\vlm_stub_server.py --port 8000
```

终端 2：
```powershell
cd "D:\DGX Spark黑客松比赛\footage-guard"
$env:FOOTAGE_GUARD_BASE_URL = "http://127.0.0.1:8000/v1"
curl.exe -s http://127.0.0.1:8000/v1/models
python scripts\footage_guard.py assets\sample_footage.mp4 --interval 5 --out "$PWD\out\judge-stub"
```

期望产物：同轨 B，且 `describe_report.json` 中模型名为 stub 系；**结果栏必须标 stub（非真实硬件）**。

冒烟-only（不跑管线）：
```powershell
curl.exe -s http://127.0.0.1:8000/v1/models
curl.exe -s http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"auto\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":32}"
```
期望：JSON 含 `footage-guard-vlm-stub` 或 `stub: true`。

---

## 轨 D — 真实硬件 VLM（M0/M5，设备到位后）

命令与日志路径：`notes/m0-vllm-smoke.md`  
管线接真端点：
```bash
export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
python3 scripts/footage_guard.py assets/sample_footage.mp4 --interval 5 --out out/judge-5090
```
期望：`MEDIA:` 末行 + `describe_report.json` 非 stub；数字进 `BENCHMARK.md` 真跑栏。

---

## 降级契约（给评委一句）

| 缺失 | 行为 |
| --- | --- |
| 无 ffmpeg | 入口直接 ERROR，不假装 MEDIA |
| 无 VLM / `--no-vlm` | 结构模式：帧+拼图+占位事件，标注未启用 VLM |
| 端点不通 | 帧级失败后降级结构模式，exit=0 产物齐（见 TEST-REPORT） |
| 仅 stub | 可证编排；**禁止**写入 M5 真分 |

### Windows 等价入口

```powershell
# 与 footage_guard.py 参数一致（剩余参数原样转发）
.\scripts\run.ps1 assets\sample_footage.mp4 --interval 5 --no-vlm --out "$PWD\out\judge-novlm"
```

