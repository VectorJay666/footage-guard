# 测试报告

> 评委 10 分钟复现命令（含期望产物）：[`notes/r2-judge-10min.md`](notes/r2-judge-10min.md)。本报告是轨 A/B 的管线证据；M5 真数待真实硬件测试，禁止 stub 冒充。

项目：footage-guard（本地视频事件复盘 Skill）
日期：2026-09-23
测试性质：开发环境实测（提交前自测），DGX Spark + 本地 VLM 的实测结果见 `BENCHMARK.md`，后续回填。

## 测试环境

| 项 | 值 |
| --- | --- |
| 操作系统 | Windows 11（10.0.26100，x64） |
| Python | 3.13.5（仅标准库） |
| Pillow | 11.3.0（拼图带时间戳） |
| ffmpeg | 7.1（gyan essentials build，libx264） |
| ffprobe | 4.0.2 |
| VLM 端点 | 无（本机未部署 vLLM，测的是降级路径） |

说明：抽帧、拼图、时间线聚合、报告生成、缓存、边界处理这些环节都不依赖模型，在本环境里是真实跑通的。VLM 逐帧描述那一环需要多模态端点，本环境测的是"端点不通时怎么办"，模型推理质量留到 Spark 上实测（`BENCHMARK.md` 有复现命令）。

## 测试对象

30 秒演示样片（`assets/sample_footage.mp4`，1280x720@15fps，h264，约 2.4MB），由 `assets/make_sample.sh` 的命令生成，三段内容：0–10s 测试图（静态场景）、10–20s 两个移动方块（物体移动）、20–30s 灰场（空旷场景）。

## 用例与结果

| # | 用例 | 命令要点 | 预期 | 结果 |
| --- | --- | --- | --- | --- |
| T1 | 主流程（结构模式） | `footage_guard.py 样片.mp4 --no-vlm --interval 5` | 6 帧、拼图、占位事件、report、末行 MEDIA | 通过。stderr 五步日志完整，stdout 末行 `MEDIA:...\montage.jpg`，montage 33KB（4 列 2 行、带时间戳） |
| T2 | 幂等重跑 | 同 T1 再跑一次 | 不报错，产物一致 | 通过 |
| T3 | 范围过短 | `--start 29 --end 30`（默认 5s 间隔） | 干净报错，exit=1 | 通过。报"范围 1.0s 按 5s 间隔抽不出任何帧"。见下方"修复记录" |
| T3b | 短范围合法 | `--start 28 --end 30 --interval 1` | 抽 2 帧 | 通过 |
| T4 | 文件不存在 | 指向不存在的 mp4 | 干净报错，exit=1 | 通过。报"视频文件不存在" |
| T5 | 帧数上限 | `--interval 1 --max-frames 10`（30s 片） | 自动放大间隔到 3.0s，恰好 10 帧，打 WARN | 通过 |
| T6 | VLM dry-run（离线） | `vlm_describe.py --dry-run` | 不发请求，输出帧数/缓存统计 | 通过。`total=6, todo=6, cached=0` |
| T7 | 缓存命中判定 | 预置 6 个帧缓存（model/focus 一致）后 dry-run | 全部判为已缓存 | 通过。`todo=0, cached=6`，复跑不会再调端点 |
| T8 | 端点不通降级 | 去掉 `--no-vlm` 全链路跑（本地无服务） | 每帧重试 3 次后记失败，管线继续，降级为结构模式 | 通过。6/6 帧记 FAIL，`events.json` 为占位事件（带 note），`report.md` 标注"VLM: 未启用"，exit=0，7 个产物齐全 |
| S1 | 事件聚合（合成数据） | 8 帧 fixture：推门/奔跑/烟雾描述 | 单帧段并入相邻段；关键词命中 attention | 通过。2 个事件（0–20s、25–35s），事件 1 命中"推门/开门/奔跑"，事件 2 命中"烟雾" |
| S2 | 结构模式占位事件 | 只有 frames.json、无帧缓存 | 生成 1 个占位事件且注明 VLM 未启用 | 通过 |
| S3 | VLM 脏输出解析 | 带 ```json 围栏、objects 为字符串、损坏 JSON | 围栏剥离、字符串转列表、坏 JSON 降级为 summary | 通过 |
| S4 | probe 错误路径 | 不存在的文件 | exit=1 + 中文报错 | 通过 |

## 修复记录（测试中发现并修掉的）

1. **范围保护条件不够严**：原来只挡 `span < 1s`，但 `fps=1/5` 对 1s 窗口产出 0 帧（首个采样点在 2.5s），ffmpeg 会以一个看不懂的 mjpeg 编码错误退出。改成 `span < interval/2` 即报错，提示语直接告诉用户要扩大范围还是调小间隔。T3 回归通过。

2. **事件状态标签取错位置**：事件合并后标签原来取"段创建时"的状态，合并段里状态以另一种居多时会标错。改成取段内出现次数最多的档位。S1 回归通过。

3. **make_sample.sh 的 -vf 跨行**：双引号里反斜杠续行会把空格带进滤镜参数，改为单行写法。

## 关键产物证据（T1 输出摘录）

`events.json`（结构模式）：

```json
[
  {
    "idx": 1,
    "start_ts": 0.0,
    "end_ts": 25.0,
    "state": {"people": "未知", "vehicles": "未知", "top_objects": []},
    "attention": false,
    "attention_reasons": [],
    "n_frames": 6,
    "sample_frame": "frame_0003.jpg",
    "note": "VLM 未启用（结构模式），仅覆盖信息。"
  }
]
```

`report.md` 末行（输出通道契约）：

```
输出通道契约（Agent 最终回复的最后一行）: `MEDIA:\D:\...\out_main\montage.jpg`
```

stdout 末行实测：

```
MEDIA:D:\DGX Spark黑客松比赛\.test\out_main\montage.jpg
```

## 没测到的部分（如实说明）

- **VLM 真实推理质量**：本机没有多模态端点，"逐帧描述准不准"要在 Spark 上起 vLLM 后验。样片是合成画面（测试图、色块），真实素材语义信息密度更高，切分质量以 Spark 实测为准；路演建议用真实片段。
- **bash 脚本语法**：本机没装 bash，`run.sh`/`install.sh`/`make_sample.sh` 只做了人工走查，没上 `bash -n`。Spark 上先跑 `bash scripts/install.sh --offline` 兜底。
- **ffprobe 4.0.2 偏旧**：本机凑的是 4.0.2，Spark 上 `apt install ffmpeg` 给的是新版，不影响用法。
- **Agent 触发行为**（evals 的 7 条用例）：属于"装进 Agent 后"的测试，需要在比赛现场或自己的 Agent 环境里跑，方法写在 `BENCHMARK.md` 的复现命令里。

## 结论

开发环境内能测的全部通过，管线在"没有模型"的极端条件下也不会崩（这是刻意的：监控运维场景里端点没起是常态，先出抽帧和覆盖信息比报错强）。剩下的 VLM 实测和 Agent 级评测，命令都已备好，到 Spark 上照 `BENCHMARK.md` 执行即可。
