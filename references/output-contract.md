# 输出契约

> 什么时候读这份：用户问"输出什么""报告怎么交付""events.json 什么结构""图怎么给到用户"。

## 产物清单（全部只写 `--out` 目录）

| 文件 | 内容 | 给谁用 |
| --- | --- | --- |
| `meta.json` | 时长/分辨率/fps/编码/码率 | 报告引用 |
| `frames.json` | 抽帧清单 `{video, start, interval, frames:[{file, ts}]}` | 拼图、时间线 |
| `frames/frame_XXXX.jpg` | 关键帧（宽 ≤1280） | 拼图、人工复核 |
| `frames/frame_XXXX.json` | 逐帧 VLM 描述缓存 `{model, focus, ts, desc}` | 时间线、复跑省钱 |
| `montage.jpg` | 关键帧拼图，带时间戳标注，最多 32 帧 | MEDIA 通道的目标 |
| `events.json` | 事件结构化数据 | 下游工具 / Agent |
| `event_timeline.md` | 事件表 + 关注事件 + 说明 | 人读 |
| `describe_report.json` | VLM 运行统计（新描述/命中缓存/失败） | 排障 |
| `report.md` | 复盘总报告 | 人读、交付 |

## MEDIA 通道（最重要的一条）

脚本跑完，stdout 最后一行（非空行）输出一行裸文本：

```
MEDIA:/abs/path/out/montage.jpg
```

没有拼图时退化成 `MEDIA:/abs/path/out/report.md`。

Agent 最终回复的最后一个非空行，必须原样是这行。生成了文件不等于用户看到了图——输出通道也是契约。别给它加引号或包成 markdown 链接，也不要在后面补说明。

## events.json 结构

```json
[
  {
    "idx": 1,
    "start_ts": 0.0,
    "end_ts": 14.0,
    "state": {
      "people": "1人",
      "vehicles": "无车辆",
      "top_objects": ["行人", "自行车"]
    },
    "attention": false,
    "attention_reasons": [],
    "n_frames": 3,
    "sample_frame": "frame_0002.jpg"
  }
]
```

- `state.people` / `state.vehicles` 是档位字符串（无人/1人/…/4人及以上），不是精确计数。
- `attention=true` 表示段内有帧命中关注关键词，`attention_reasons` 是命中词 top5。
- 结构模式下只有一个覆盖全片的占位事件，带 `"note": "VLM 未启用…"`。

## 逐帧缓存的 desc 结构

```json
{
  "people": 2,
  "vehicles": 0,
  "objects": ["行人", "自行车"],
  "actions": ["有人推开门"],
  "summary": "两人经过入口，一人推门"
}
```

模型可能漏字段或写错类型：`people/vehicles` 可能是 `null`；解析彻底失败时只剩 `summary` 加一个 `"parse_failed": true`。消费端记得做空值兜底。

## 不变量（和 SKILL.md 一致）

- 不推断个人身份、年龄、国籍、关系、情绪、意图。
- 默认只连 127.0.0.1；换远端端点必须用户知情。
- 不改、不转码、不删原视频；只写 `--out`。
- 不打印明文 API key。
