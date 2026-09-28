# 完整工作流（五步）

> 什么时候读这份：用户说"复盘 / 分析 / 摘要这段视频"，参数已经问全，准备开跑。
> 全程只读原视频、只写 `--out` 目录；不改、不转码、不删输入。

## 第 0 步：前置确认（缺了先问，不许猜）

| 要确认什么 | 不给时的默认 | 备注 |
| --- | --- | --- |
| 视频路径 | 没有默认 | 文件不存在就停下告诉用户，别猜路径 |
| 时间范围 | 全片 | `--start/--end`，单位秒 |
| 取帧间隔 | 5s | `--interval`；片子长就放大到 10–15s |
| 关注对象 | 无 | `--focus "车辆,人"`，进 VLM 提示词 |
| VLM 端点 | `http://127.0.0.1:8000/v1` | 不可用就跟用户确认改 `--no-vlm` |

先算笔账：帧数 ≈ 时长 ÷ 间隔，硬上限 `--max-frames`（默认 240）。超了脚本会自动放大间隔并打 WARN，不会偷偷烧钱。

## 第 1 步：探测

```bash
python3 scripts/probe.py /abs/path/video.mp4 /abs/path/out/meta.json
```

报错处理见 `troubleshooting.md`。

## 第 2 步：抽帧 + 拼图

```bash
python3 scripts/extract_frames.py /abs/path/video.mp4 \
  --out /abs/path/out --interval 5 --start 0 --max-frames 240
```

产物：`frames/frame_XXXX.jpg`（宽 ≤1280）、`frames.json`（帧清单 + 时间戳）、`montage.jpg`。
重复执行会先清掉旧帧再重抽；`frames/*.json` 里的描述缓存保留，参数没变就能接着用。

## 第 3 步：VLM 逐帧描述

```bash
python3 scripts/vlm_describe.py --out /abs/path/out --model auto --concurrency 4 --focus "车辆,人"
# 只描述前 3 帧冒烟：加 --limit 3
# 只检查端点和缓存、不发请求：加 --dry-run
```

- 端点和 key 走环境变量：`FOOTAGE_GUARD_BASE_URL`、`FOOTAGE_GUARD_API_KEY`（默认 EMPTY）；模型名走 `--model`。
- `--model auto`：请求 `/v1/models`，优先挑名字里带 `vl`/`vision`/`video` 的。
- 缓存按 `model + focus` 匹配，两个都不变才复用；换关注对象等于换提示词，会重新描述。
- 端点不是本机地址会打 WARN（数据要出网），这种情况先征得用户同意。

## 第 4 步：事件时间线

```bash
python3 scripts/build_timeline.py --out /abs/path/out
```

- 状态 = (人数档位, 车辆档位)：无人 / 1–3 人 / ≥4 人，无车 / 1–3 辆 / ≥4 辆。
- 状态不变的连续帧算一个事件；只有 1 帧的段并进相邻段，避免切碎。
- 段内任何一帧的描述命中关注关键词（默认：摔倒/奔跑/聚集/开门/翻越/逆行/烟雾/火焰/闯入…），事件打上 `attention`。自定义：`FOOTAGE_GUARD_KEYWORDS="开门,翻墙,聚集"`。
- 没有 VLM 数据时生成一个覆盖全片的占位事件，文件里注明 VLM 未启用。

## 第 5 步：一键跑完（平时用这个）

```bash
scripts/run.sh /abs/path/video.mp4 --interval 5 --out /abs/path/out
# 指定范围和关注对象：
scripts/run.sh /abs/path/video.mp4 --start 30 --end 60 --focus "车辆"
# VLM 没起来先出结构：
scripts/run.sh /abs/path/video.mp4 --no-vlm
```

跑完 stdout 最后一行是 `MEDIA:<绝对路径>`（有拼图指拼图，没有就指 report.md）。
Agent 最终回复的最后一行必须原样带上这行——详见 `output-contract.md`。

## 一键还是分步

- 平时用一键。VLM 挂了会自动降级成结构模式，不中断。
- 排查问题时用分步，每步单独重跑，看卡在哪。
- 复跑几乎免费：命中缓存的帧不会再调端点，只有失败和新帧才发请求。
