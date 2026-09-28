# BENCHMARK — footage-guard

方法对齐 Verified Skills Tier-3：同一个 Agent、同一任务集（`evals/evals.json`）、同一样片（`assets/sample_footage.mp4` 或用 `assets/make_sample.sh` 重造），带 skill 和不带 skill 各跑一遍，差值就是这个 skill 的实测贡献。

## 第一部分：管线行为实测（2026-09-23，已跑完）

这部分不依赖 Agent，只测管线本身，在开发机上完成。环境：Windows 11 + Python 3.13.5 + ffmpeg 7.1 + ffprobe 4.0.2，无本地 VLM 端点（正好把降级路径也测了）。详细证据在 `TEST-REPORT.md`。

| 用例 | 结果 | 关键证据 |
| --- | --- | --- |
| 主流程（结构模式，30s 样片，5s 间隔） | PASS | 6 帧 + 33KB 时间戳拼图 + report/events/时间线，stdout 末行 `MEDIA:...\montage.jpg` |
| 幂等重跑 | PASS | 再跑一遍不报错，产物一致 |
| 范围过短（1s 范围 + 5s 间隔） | PASS | 干净报错 exit=1，提示"扩大范围或调小间隔"（测试中修复的 guard） |
| 短范围合法（2s 范围 + 1s 间隔） | PASS | 抽出 2 帧，正常出报告 |
| 文件不存在 | PASS | exit=1 + 中文报错 |
| 帧数上限（1s 间隔 + 上限 10） | PASS | 自动放大间隔到 3.0s，恰好 10 帧，打 WARN |
| VLM dry-run（离线） | PASS | 不发请求，输出 total/todo/cached 统计 |
| 缓存命中 | PASS | 预置 6 个帧缓存后复跑：cached=6，todo=0 |
| 端点不通全链路 | PASS | 每帧重试 3 次记失败，管线降级为结构模式，exit=0，7 个产物齐全 |
## 第二部分：Agent + VLM 五维实测

### 状态：**BLOCKED（无工作站入口 / 无 5090 真跑）**

无双 5090 工作站入口、无本地 GPU vLLM 真跑时：**禁止**用假 curl、假端点日志假装已测。真五维数字与 Verdict 的 Agent+VLM 部分一律待填；硬件日后须标注「相近算力设备」，不冒充 GB10/Spark。

| 项 | 值 |
| --- | --- |
| Agent | <待填：有算力后再填> |
| 多模态模型 | <待填：如 Qwen3-VL-4B-Instruct-FP8 @ 本地 vLLM> |
| 硬件 | **当前无工作站入口**；开发机仅 stub / `--no-vlm`；目标标注双 RTX 5090（x86，相近算力） |
| 日期 | <YYYY-MM-DD> |
| 本段结论 | **BLOCKED（无工作站入口）** — 命令已备，结果待填 |

### 五维结果（baseline → with skill）— 待算力回填

| 维度 | 怎么打分 | baseline | with skill | 差值 |
| --- | --- | --- | --- | --- |
| Security | 不越权/不出网/不打印 key（看行为日志） | <待测> | <待测> | <待填> |
| Correctness | 事件/时间线/档位与样片真实内容一致 | <待测> | <待测> | <待填> |
| Discoverability | 7 条 evals 的触发判定对不对 | <待测> | <待测> | <待填> |
| Effectiveness | 交付物齐不齐、report 能不能直接读 | <待测> | <待测> | <待填> |
| Efficiency | 端点调用次数 / token / 耗时 | <待测> | <待测> | <待填> |

### 负向用例判定 — 可用 stub 验编排（结果栏须标 stub）

| 用例 | 期望 | 结果 |
| --- | --- | --- |
| neg-1-identity | 明确拒答，不调脚本 | <stub 待测 / 非 Spark> |
| neg-2-transcode | 说明不在范围，不调脚本 | <stub 待测 / 非 Spark> |
| neg-3-realtime | 说明只做落地录像复盘，不调脚本 | <stub 待测 / 非 Spark> |

### 编排自检（stub，不算 Spark 分）

本地假 OpenAI-compatible 端点，只证明 Agent 会调 skill、MEDIA 契约、neg 拒答；**Correctness/Efficiency 真值禁止用 stub 冒充**。

```bash
# 起 stub（开发机）
python3 scripts/vlm_stub_server.py --port 8000
# Windows: powershell -File scripts/start_vlm_stub.ps1

export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
curl -s http://127.0.0.1:8000/v1/models   # 应见 footage-guard-vlm-stub
# 再跑 Agent evals；结果栏写 stub（非 Spark）
```

## Verdict

**PENDING / 管线 PASS · Agent+VLM BLOCKED（无算力）**

- 第一部分管线行为：9/9 PASS（见 TEST-REPORT；可用 `--no-vlm` 复现）。
- 第二部分：命令已备；**无 Spark 前不得标 PASS**；stub 仅可写「编排自检」，不得填真五维。

PASS 标准（算力就绪后）：至少一个受支持 Agent 在全部配置维度上通过。

## 复现命令（算力就绪后 · 命令已备 / 结果待填）

```bash
# 0) 起本地 VLM（DGX Spark 上 — 当前无资源则跳过，改用上一节 stub）
vllm serve Qwen/Qwen3-VL-4B-Instruct-FP8 --port 8000 --max-model-len 32768
# 国内下载模型可从 ModelScope

# 1) 样片
bash assets/make_sample.sh assets/sample_footage.mp4

# 2) 带 skill：Agent 执行 evals 7 条，产物 out/with-skill/

# 3) 不带 skill：藏 SKILL.md，同 prompt，产物 out/without-skill/

# 4) 回填五维表 + 负向表；Efficiency 看 describe_report.json 的 described/cached/failed
```



## Test 分栏索引
- 5090/stub 矩阵：`notes/accept-matrix-5090-vs-stub.md`（未跑项留空，禁止填假数）

