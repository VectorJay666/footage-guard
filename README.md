# footage-guard

把一段本地监控/现场录像，变成「事件时间线 + 带时间戳的关键帧拼图 + 复盘报告」。

一句话定位：隐私本地复盘 Skill——双 RTX 5090（x86，相近算力）上拿真跑证据；DGX Spark / GX10 用 spark.env 一键迁移，不冒充已在 GB10 跑过。stub 只做开发回退，不算 M5。

## 评委 10 分钟

- 命令与期望产物（四轨 A/B/C/D）：[`notes/r2-judge-10min.md`](notes/r2-judge-10min.md)
- 管线开发机证据（9/9）：[`TEST-REPORT.md`](TEST-REPORT.md)
- 盘点：[`notes/r1-inventory.md`](notes/r1-inventory.md)
- Windows 入口：`scripts/run.ps1`（参数同 `footage_guard.py` / `run.sh`）

默认演示走 **轨 A**（只读证据）；有 ffmpeg 再跑轨 B/C；5090 真数走轨 D（`notes/m0-vllm-smoke.md`）。**stub / --no-vlm 不算 M5。**

## 提交现实（9/29 缩范围）

**可交证据**：M3 Skill 目录 + 开发机 `TEST-REPORT`（含 `--no-vlm`）+ 离线 report/montage Demo + `BENCHMARK` 第一部分 PASS。  
**诚实 BLOCKED**：无工作站入口前，不做 M0 冒烟日志、不填 M5 五维真数；硬件若日后真跑，标注双 RTX 5090（x86，相近算力），不冒充 DGX Spark/GB10。  
**开发优先命令**（无需 GPU）：

```bash
scripts/run.sh assets/sample_footage.mp4 --interval 5 --no-vlm
```

有 OpenAI 兼容本地端点时再去掉 `--no-vlm`，并设置 `FOOTAGE_GUARD_BASE_URL`。

## 要解决什么

安防、园区、门店、活动现场，录像的复盘方式是"打开播放器慢慢拖进度条"。一段 30 分钟的监控里真正有用的可能就两分钟，但人是得全程看的。丢给云端视频分析又踩隐私红线；官方 VSS（Video Search and Summarization）能做，但那是一套 Docker + Kafka + Elasticsearch 的重型部署，在单卡边缘机上不现实。

我们要的是中间那档：**单机本地（开发机 / 双 5090 相近算力 / 将来 Spark），视频进 → 报告出，中间几步是分钟级的**——没卡也能 `--no-vlm` 交管线证据。

## 怎么工作

```
视频文件
   │
   ├─ 1 探测      ffprobe 拿时长/分辨率/fps/码率
   ├─ 2 抽帧      ffmpeg 按间隔取关键帧（宽 ≤1280），同时生成时间戳拼图
   ├─ 3 理解      本地 VLM（OpenAI 兼容端点）逐帧输出 人数/车辆/物体/动作
   ├─ 4 聚合      按「人数档位 × 车辆档位」状态切段成事件，关键词命中打 attention
   └─ 5 交付      report.md + events.json + montage.jpg（末行 MEDIA 通道输出）
```

每一步都是独立可重跑的脚本，一键入口是 `scripts/run.sh`。

## 项目优势

每条都标了实测用例编号，证据在 `TEST-REPORT.md`。

1. **画面不出本机，而且是代码保证的，不是文档保证的**。默认端点 `127.0.0.1:8000/v1`；`vlm_describe.py` 启动时检查端点地址，非本机直接打 WARN；SKILL.md 规定 Agent 用远端端点前必须先征得用户同意。隐私在这条链路里是一等公民，不是文档里的客套话。

2. **没有模型也出活**。监控运维里"端点没起"是常态不是意外。VLM 调用失败或传 `--no-vlm` 时管线降级为结构模式：抽帧、拼图、时间覆盖照出，报告里明确写"无语义信息"。实测 T8：6/6 帧调用失败，管线 exit=0，7 个产物齐全。

3. **成本有上限**。帧数 = 时长 ÷ 间隔，硬上限 240 帧，超了自动放大间隔并告警（实测 T5：30s 片 + 1s 间隔 → 自动变 3.0s，正好 10 帧）。描述过的帧写本地缓存，同参数复跑零调用（实测 T7：cached=6，todo=0）。

4. **零必装 pip 包**。核心链路只有 Python 标准库 + ffmpeg。机器上 `apt install ffmpeg`、起一个本地 vLLM，就能用。Pillow 可选（拼图加时间戳标注）；端点可换成任意 OpenAI 兼容服务。

5. **治理产物齐**。SKILL.md（窄触发 + 前置提问 + 安全边界）、references 渐进披露、evals（4 正向 + 3 负向）、skill-card（风险与缓解）、BENCHMARK（实测模板）。负向用例包括"识别视频里某人是谁"，正确答案是拒答——边界行为写进测试集了。

6. **输出契约是机器可读的**。stdout 末行是裸的 `MEDIA:/绝对路径/montage.jpg`，Agent 把拼图直接递给用户，不用再用文字描述一张图。`events.json` 给下游工具消费，`report.md` 给人看。

## 快速开始（开发机优先；有本地 VLM 再接）

```bash
cd footage-guard
bash scripts/install.sh                        # 依赖 + 端点检查
bash assets/make_sample.sh assets/sample_footage.mp4   # 没有真实素材就生成 30s 样片
scripts/run.sh assets/sample_footage.mp4 --interval 5
# 产物在 assets/sample_footage.mp4.footage-guard/
# stdout 最后一行: MEDIA:/abs/path/.../montage.jpg
```

有真实录像时：

```bash
scripts/run.sh /path/to/cctv.mp4 --start 600 --end 900 --focus "车辆,人"
# VLM 没起来先出结构：
scripts/run.sh /path/to/cctv.mp4 --no-vlm
```

## 配置

环境变量：

| 变量 | 默认 | 用途 |
| --- | --- | --- |
| `FOOTAGE_GUARD_BASE_URL` | `http://127.0.0.1:8000/v1` | OpenAI 兼容端点 |
| `FOOTAGE_GUARD_API_KEY` | `EMPTY` | 只走环境变量，不落盘不打印 |
| `FOOTAGE_GUARD_TIMEOUT_S` | `120` | 单请求超时 |
| `FOOTAGE_GUARD_KEYWORDS` | 内置中文关注词表 | attention 关键词，逗号分隔 |

常用参数：`--interval`（取帧间隔，默认 5s）· `--start/--end`（秒）· `--focus "车辆,人"`（写进提示词）· `--model auto`（自动挑 vl/vision/video 命名的模型）· `--max-frames 240` · `--concurrency 4` · `--no-vlm`（结构模式）· `--limit N`（只描述前 N 帧，冒烟用）。

## 测试与验证

2026-09-23 在开发机（Windows + Python 3.13.5 + ffmpeg 7.1）完成自测：管线 9 个用例 + 合成数据 4 个用例，全部通过，含"端点不通降级""范围过短""帧数上限"等边界。过程里抓出来一个 guard 条件 bug（1 秒范围 + 5 秒间隔会抽 0 帧，导致 ffmpeg 报看不懂的编码错）并已修复。详见 `TEST-REPORT.md`。

还没测的两块：VLM 真实推理质量、Agent 触发行为（evals 7 条）。**当前无工作站入口 → BENCHMARK 第二部分 BLOCKED**；命令在 `notes/m0-vllm-smoke.md` / `BENCHMARK.md`，有入口再填真数。

## 技术细节

### 处理流程（五步，全程本机）

| 步 | 脚本 | 做什么 | 产物 |
| --- | --- | --- | --- |
| 1 探测 | `scripts/probe.py` | 用 ffprobe 读时长、分辨率、帧率、编码 | `meta.json` |
| 2 抽帧 | `scripts/extract_frames.py` | 用 ffmpeg 按固定间隔（默认 5 秒）截帧，拼成带时间戳的拼图 | `frames/`、`frames.json`、`montage.jpg` |
| 3 看图 | `scripts/vlm_describe.py` | 把每帧发给本地多模态模型（OpenAI 兼容接口），拿回人数、车辆、物体、动作 | `frames/frame_XXXX.json`（逐帧缓存） |
| 4 聚合 | `scripts/build_timeline.py` | 把"人数档位 + 车辆档位"不变的连续帧合成一个事件，命中关注词的打标 | `events.json`、`event_timeline.md` |
| 5 报告 | `scripts/footage_guard.py` | 汇总成复盘报告，stdout 最后一行打印 `MEDIA:<拼图绝对路径>` | `report.md` |

一键入口：`scripts/run.sh <视频> --out <目录>`（Windows 用 `scripts/run.ps1`）。（依据：`references/workflow.md`）

### 依赖

- 必需：Python 3 和 ffmpeg/ffprobe 两个可执行文件。所有脚本只 import 标准库，不需要 pip 安装任何包。（依据：`scripts/*.py` 的 import 行、`scripts/install.sh`）
- 可选：Pillow。装了之后拼图上每张缩略图会带时间戳标注；没装会退化成 ffmpeg 拼的无标注网格。安装命令 `pip install "Pillow>=9.0"`。（依据：`scripts/install.sh`）
- 可选依赖文件：`scripts/requirements.txt`，只列了 Pillow（`Pillow>=9.0`），`pip install -r scripts/requirements.txt` 即可；不装也能跑。
- 环境自检：`scripts/install.sh --offline`。

### 两种运行模式

| | 离线结构模式 `--no-vlm` | 接模型模式 |
| --- | --- | --- |
| 需要什么 | Python 3（只用标准库）+ ffmpeg/ffprobe；Pillow 可选 | 另加一个本地 OpenAI 兼容多模态端点（默认 `http://127.0.0.1:8000/v1`） |
| 跑第 3 步吗 | 跳过 | 跑 |
| 拼图 | 有 | 有 |
| 事件内容 | 只有 1 条覆盖性占位事件，人和车写"未知" | 按画面内容切分事件，写出人数/车辆档位和关注标记 |
| 本次实测 | 样例 30 秒视频 → 6 帧（每 5 秒一帧）+ 1 条事件（0–25 秒）、`EXIT=0`（`notes/box-smoke-2026-09-28.log`，在装了 ffmpeg 的另一台 Linux 开发机上跑） | **未实测**，见下方 BLOCKED |

端点连不上时，一键脚本会自动降级到结构模式，不中断。（依据：`references/workflow.md`"一键还是分步"）

### Skill 输入输出约定

- **输入**：已落地的本地视频路径（必填，不存在就停下问，不猜）、起止秒、取帧间隔、关注对象（可选）。（`SKILL.md`）
- **输出**：全部写进 `--out` 目录，清单见 `references/output-contract.md`。
- **MEDIA 通道**：stdout 最后一个非空行是裸文本 `MEDIA:/abs/path/montage.jpg`，没有拼图时指向 `report.md`；Agent 最终回复最后一行必须原样带上。（`references/output-contract.md`）
- **`events.json` 字段**：`idx`、`start_ts`/`end_ts`（秒）、`state.people`/`state.vehicles`（档位字符串，不是精确计数）、`attention`、`attention_reasons`、`n_frames`、`sample_frame`；结构模式下多一个 `note`。
- **消费端兜底**：模型可能漏字段或给 `null`，解析失败时只剩 `summary` 和 `"parse_failed": true`。

### 安全边界（写在 Skill 里的设计约束）

- 默认只连 `127.0.0.1`；换成非本机端点会打 WARN，必须先告知用户画面将发往远端。
- 只读原视频，不改、不转码、不删；产物只写 `--out`。
- API key 只走环境变量 `FOOTAGE_GUARD_API_KEY`，不打印明文。
- 设计上拒绝四类请求：实时告警、身份/人脸识别、转码剪辑、单图问答。**这一条目前只写在 `SKILL.md` 里，负向用例 neg1–neg3 需要走 Agent 链路，本次没有跑过。**
- 帧数上限 `--max-frames`（默认 240），超了自动放大间隔；同参数复跑命中逐帧缓存，不重复调模型。

### 本地模拟端点（stub，不算模型结果）

`scripts/vlm_stub_server.py` 起一个 OpenAI 兼容的假服务（模型 id `footage-guard-vlm-stub`），`/v1/models` 和 `/v1/chat/completions` 双轮 PASS（`notes/r3-round-log.txt`）。它只回固定文案、带 `stub:true`，只证明接口调用链路通，不代表识别效果，不计入跑分。

### 当前状态（BLOCKED 清单，照 `notes/FINAL_ACCEPTANCE.md`）

| 项 | 状态 | 原因 |
| --- | --- | --- |
| 文档/Skill/evals 齐全（轨 A） | PASS 10/10 | 双轮核对 |
| stub 端点（轨 C） | PASS | 双轮，已标 stub |
| 提交用笔记本上跑离线流程（轨 B） | BLOCKED | 该机 PATH 里没有 ffmpeg |
| stub 接完整流程出 MEDIA | BLOCKED | 同上 |
| 负向用例 neg1–neg3 实际拒绝 | 未跑 | 需要 Agent 链路 |
| M0 vLLM 冒烟 / 真模型管线 | BLOCKED | 没有工作站（双 RTX 5090）入口 |
| BENCHMARK 五项数字 | BLOCKED | 须真机实跑；stub 和 `--no-vlm` 不算分 |

### 已知小问题（如实记录，本次不改代码）

- 结构模式的占位事件 `end_ts` 是最后一帧的时间戳，不是视频总长：样例 30 秒视频是 0 到 25 秒，演示用的 56.6 秒路口素材是 0 到 50 秒。`output-contract.md` 说它"覆盖全片"，两者有出入，README 里不写"覆盖全片"。

## 目录结构

```
footage-guard/
├── SKILL.md                  # 入口：frontmatter + 路由表 + 前置提问 + 安全边界
├── README.md                 # 本文件
├── TEST-REPORT.md            # 开发环境实测报告（2026-09-23）
├── skill-card.md             # 信任记录（Description/Owner/Risk…）
├── BENCHMARK.md              # Tier-3 实测模板（带/不带 skill 对照）
├── scripts/
│   ├── run.sh                # 一键入口
│   ├── footage_guard.py      # 端到端编排
│   ├── probe.py              # ffprobe 元信息
│   ├── extract_frames.py     # 抽帧 + 帧清单 + 拼图
│   ├── vlm_describe.py       # 端点逐帧描述（缓存/并发/重试/出网告警）
│   ├── build_timeline.py     # 事件聚合
│   ├── install.sh            # 依赖 + 端点检查
│   └── requirements.txt      # 可选依赖说明
├── references/               # 命中才读（渐进披露）
│   ├── workflow.md           # 五步流程与分步命令
│   ├── troubleshooting.md    # 故障排查
│   └── output-contract.md    # 产物与 MEDIA 通道契约
├── evals/
│   └── evals.json            # 4 正向 + 3 负向用例
└── assets/
    ├── make_sample.sh        # 生成 30s 演示样片
    ├── sample_footage.mp4    # 已生成的样片（静态→移动物体→空旷）
    └── README.md
```

## 与训练营要求的对齐

| 要求 | 落点 |
| --- | --- |
| 窄触发、强路由 | SKILL.md frontmatter 写 `Use when / Not for`，正文是路由表不是百科 |
| 前置提问 | SKILL.md「前置提问」：路径/范围/间隔/关注对象/端点，缺了先问 |
| 安全边界内嵌 | 不推断身份；默认本机端点（非本机打 WARN）；只读输入单目录输出；不打印 key；帧缓存省钱 |
| 负向用例 | evals 3 条：身份识别、转码、实时告警，正确答案都是拒答 |
| 治理产物 | SKILL.md + skill-card + evals + BENCHMARK + 安装脚本 |
| 本地化 | 默认 `127.0.0.1:8000/v1`，DGX Spark 本地 vLLM 直接可用 |


## 无 Spark 时（编排自检 stub，不算真 VLM）

`ash
python3 scripts/vlm_stub_server.py --port 8000
export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
# 仅验证会调端点 / MEDIA / neg；BENCHMARK 第二部分仍标 BLOCKED（无算力）
`

## License

Apache-2.0

