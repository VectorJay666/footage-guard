#!/usr/bin/env python3
"""footage-guard · 端到端编排：probe → 抽帧 → VLM 描述 → 事件时间线 → 复盘报告。

用法:
    python3 footage_guard.py VIDEO [--out DIR] [--interval 5] [--start 0] [--end S]
                                   [--max-frames 240] [--model auto] [--concurrency 4]
                                   [--no-vlm] [--focus "车辆,人"] [--limit N] [--no-montage]

产物（--out 目录，默认 <视频名>.footage-guard/）:
    meta.json · frames.json · frames/ · montage.jpg · events.json ·
    event_timeline.md · describe_report.json · report.md

输出通道契约：stdout 最后一行（非空行）为未格式化的纯文本
    MEDIA:<绝对路径>
见 references/output-contract.md。
"""
import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_timeline  # noqa: E402
import extract_frames  # noqa: E402
import probe as _probe  # noqa: E402
import vlm_describe  # noqa: E402


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def write_report(out_dir, meta, manifest, vlm_report, events, structural, focus, montage_path, resolved_model):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    att = [e for e in events if e.get("attention")]
    lines = []
    lines.append("# 视频事件复盘报告")
    lines.append("")
    lines.append(f"- 生成时间: {now} · 工具: footage-guard 1.0.0")
    lines.append(f"- 视频: `{meta['video']}`")
    lines.append(
        f"- 时长 {meta['duration_s']:.1f}s · {meta['width']}x{meta['height']} · "
        f"{meta['fps']} fps · {meta['codec']} · {(meta['size_bytes'] / 1e6):.1f} MB"
    )
    lines.append(
        f"- 分析范围: {manifest['start']:.1f}s 起 · 取帧间隔 {manifest['interval']:g}s · "
        f"共 {len(manifest['frames'])} 帧"
    )
    if vlm_report:
        lines.append(
            f"- VLM: 模型 {resolved_model or vlm_report.get('model')} · "
            f"新描述 {vlm_report.get('described', 0)} 帧 · 命中缓存 {vlm_report.get('cached', 0)} 帧 · "
            f"失败 {vlm_report.get('failed', 0)} 帧"
        )
    else:
        lines.append("- VLM: 未启用（--no-vlm 结构模式）")
    if focus:
        lines.append(f"- 关注对象: {focus}")
    lines.append("")

    lines.append("## 事件时间线")
    lines.append("")
    lines.append("| # | 起 | 止 | 人数 | 车辆 | 显著物体 | 关注 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for e in events:
        st = e["state"]
        objs = "、".join(st["top_objects"]) if st["top_objects"] else "-"
        flag = "⚠ " + "、".join(e["attention_reasons"][:3]) if e.get("attention") else ""
        lines.append(
            f"| {e['idx']} | {build_timeline.fmt_ts(e['start_ts'])} | {build_timeline.fmt_ts(e['end_ts'])} "
            f"| {st['people']} | {st['vehicles']} | {objs} | {flag} |"
        )
    lines.append("")

    lines.append("## 关注事件")
    if att:
        for e in att:
            lines.append(
                f"- 事件 {e['idx']}（{build_timeline.fmt_ts(e['start_ts'])}–"
                f"{build_timeline.fmt_ts(e['end_ts'])}）: 命中「{'、'.join(e['attention_reasons'])}」，"
                f"代表帧 `frames/{e['sample_frame']}`"
            )
    else:
        lines.append("- 未命中关注关键词。")
    lines.append("")

    lines.append("## 产物清单")
    lines.append("")
    lines.append("| 文件 | 说明 |")
    lines.append("| --- | --- |")
    lines.append("| `report.md` | 本报告 |")
    lines.append("| `events.json` | 事件结构化数据（供下游 Agent/工具消费） |")
    lines.append("| `event_timeline.md` | 事件时间线（含逐事件说明） |")
    lines.append("| `frames.json` / `frames/` | 抽帧清单与关键帧 |")
    if montage_path:
        lines.append(f"| `montage.jpg` | 关键帧拼图（时间戳标注）: `{os.path.basename(montage_path)}` |")
    lines.append("| `frames/frame_XXXX.json` | 逐帧 VLM 结构化描述缓存 |")
    lines.append("")

    lines.append("## 安全与免责")
    lines.append("")
    lines.append("- 事件结果为**启发式聚合**（人数/车辆状态切分 + 关键词提示），不是行为识别结果，需人工复核。")
    lines.append("- 本流程**不推断个人身份、年龄、国籍、关系或意图**。")
    lines.append("- 分析全程只读原视频、只写本目录；如端点非 127.0.0.1，画面会发送到对应远端服务。")
    lines.append("")
    media = montage_path or os.path.join(out_dir, "report.md")
    lines.append(f"输出通道契约（Agent 最终回复的最后一行）: `MEDIA:{os.path.abspath(media)}`")

    path = os.path.join(out_dir, "report.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="footage-guard 端到端视频事件复盘")
    ap.add_argument("video", help="本地视频文件路径")
    ap.add_argument("--out", default=None, help="输出目录（默认 <视频名>.footage-guard/）")
    ap.add_argument("--interval", type=float, default=5.0, help="取帧间隔秒（默认 5）")
    ap.add_argument("--start", type=float, default=0.0, help="起始秒（默认 0）")
    ap.add_argument("--end", type=float, default=None, help="结束秒（默认全片）")
    ap.add_argument("--max-frames", type=int, default=240, help="帧数上限（默认 240）")
    ap.add_argument("--model", default="auto", help="VLM 模型名或 auto（默认 auto）")
    ap.add_argument("--concurrency", type=int, default=4, help="VLM 并发（默认 4）")
    ap.add_argument("--no-vlm", action="store_true", help="结构模式：只抽帧+时间覆盖，不调 VLM")
    ap.add_argument("--focus", default="", help="关注对象，逗号分隔，写入提示词")
    ap.add_argument("--limit", type=int, default=None, help="只描述前 N 帧（低成本冒烟）")
    ap.add_argument("--no-montage", action="store_true", help="不生成关键帧拼图")
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out or (args.video + ".footage-guard"))
    os.makedirs(out_dir, exist_ok=True)

    # STEP 1/5 探测
    log("STEP 1/5 probe …")
    meta = _probe.probe(args.video)
    log(f"  {meta['duration_s']:.1f}s {meta['width']}x{meta['height']} @ {meta['fps']}fps {meta['codec']}")
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)

    # STEP 2/5 抽帧 + 拼图
    log("STEP 2/5 extract_frames …")
    manifest, montage_path = extract_frames.extract(
        args.video, out_dir, args.interval, args.start, args.end,
        args.max_frames, montage=not args.no_montage,
    )

    # STEP 3/5 VLM 描述（失败降级为结构模式，不中断）
    vlm_report, resolved_model = None, args.model
    if args.no_vlm:
        log("STEP 3/5 VLM: 跳过（--no-vlm 结构模式）")
    else:
        log("STEP 3/5 vlm_describe …")
        try:
            vlm_report, resolved_model = vlm_describe.run(
                out_dir, model=args.model, concurrency=args.concurrency,
                focus=args.focus, limit=args.limit,
            )
        except Exception as exc:
            log(f"STEP 3/5 WARN: VLM 不可用（{exc}），降级为结构模式继续。")
            vlm_report = None

    # STEP 4/5 事件时间线
    log("STEP 4/5 build_timeline …")
    events = build_timeline.build(out_dir)

    # STEP 5/5 复盘报告
    log("STEP 5/5 report …")
    report_path = write_report(
        out_dir, meta, manifest, vlm_report, events,
        structural=vlm_report is None, focus=args.focus,
        montage_path=montage_path, resolved_model=resolved_model,
    )
    log(f"  报告 -> {report_path}")

    media = montage_path or report_path
    print(f"MEDIA:{os.path.abspath(media)}")  # 输出通道契约：stdout 最后一行
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"[footage-guard] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
