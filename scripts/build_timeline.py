#!/usr/bin/env python3
"""footage-guard · build_timeline：从帧级描述聚合事件时间线（启发式，非行为识别承诺）。

用法:
    python3 build_timeline.py --out OUT_DIR

产物: OUT_DIR/events.json、OUT_DIR/event_timeline.md
聚合规则: 以（人数档位, 车辆档位）为状态，状态连续段为一个事件；
          段内任一帧命中关注关键词 → 标记 attention；单帧段并入相邻段。
"""
import argparse
import json
import os
import sys
from collections import Counter

DEFAULT_KEYWORDS = [
    "摔倒", "倒地", "奔跑", "快速移动", "聚集", "推门", "开门", "关门",
    "翻越", "攀爬", "逆行", "冲突", "推搡", "烟雾", "火焰", "泄漏",
    "闯入", "静止不动", "蹲下",
]


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def bucket_people(p):
    if p is None:
        return "未知"
    if p == 0:
        return "无人"
    if p <= 3:
        return f"{p}人"
    return "4人及以上"


def bucket_vehicles(v):
    if v is None:
        return "未知"
    if v == 0:
        return "无车辆"
    if v <= 3:
        return f"{v}辆车"
    return "4辆车及以上"


def fmt_ts(s: float) -> str:
    s = max(0, int(round(s)))
    return f"{s // 60:02d}:{s % 60:02d}"


def build(out_dir):
    """读取 frames.json + 帧缓存，生成事件；返回 events 列表（可能为空）。"""
    manifest_p = os.path.join(out_dir, "frames.json")
    if not os.path.isfile(manifest_p):
        raise RuntimeError(f"缺少 {manifest_p}")
    with open(manifest_p, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)

    entries = []
    for fr in manifest["frames"]:
        p = os.path.join(out_dir, "frames", os.path.splitext(fr["file"])[0] + ".json")
        desc = None
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    desc = json.load(fh).get("desc")
            except (json.JSONDecodeError, OSError):
                desc = None
        entries.append({"file": fr["file"], "ts": fr["ts"], "desc": desc})

    model = None
    dr = os.path.join(out_dir, "describe_report.json")
    if os.path.isfile(dr):
        try:
            with open(dr, "r", encoding="utf-8") as fh:
                model = json.load(fh).get("model")
        except (json.JSONDecodeError, OSError):
            model = None

    vlm_used = any(e["desc"] for e in entries)
    if not vlm_used:
        # 结构模式：无 VLM 数据，只产出一段"全片"占位事件
        events = [{
            "idx": 1,
            "start_ts": entries[0]["ts"], "end_ts": entries[-1]["ts"],
            "state": {"people": "未知", "vehicles": "未知", "top_objects": []},
            "attention": False, "attention_reasons": [],
            "n_frames": len(entries),
            "sample_frame": entries[0]["file"],
            "note": "VLM 未启用（结构模式），仅覆盖信息。",
        }]
        _write(out_dir, manifest, events, model, structural=True)
        log("[timeline] 结构模式：无 VLM 数据，生成覆盖性占位事件。")
        return events

    # 分段：状态 = (人数档位, 车辆档位)
    segs = []
    for e in entries:
        d = e["desc"] or {}
        key = (bucket_people(d.get("people")), bucket_vehicles(d.get("vehicles")))
        if segs and segs[-1]["key"] == key:
            segs[-1]["frames"].append(e)
        else:
            segs.append({"key": key, "frames": [e]})

    # 单帧段并入相邻段：优先并入前一段；首段为单帧时暂存，遇到多帧段时反向吸收
    merged = []
    for s in segs:
        if len(s["frames"]) < 2:
            if merged:
                merged[-1]["frames"].extend(s["frames"])
            else:
                merged.append(s)
        else:
            if merged and len(merged[-1]["frames"]) < 2:
                s["frames"] = merged[-1]["frames"] + s["frames"]
                merged.pop()
            merged.append(s)

    keywords = _load_keywords()
    events = []
    for i, s in enumerate(merged, start=1):
        frs = s["frames"]
        objects = Counter()
        reasons = Counter()
        state_counts = Counter()
        for e in frs:
            d = e["desc"] or {}
            state_counts[(bucket_people(d.get("people")), bucket_vehicles(d.get("vehicles")))] += 1
            for o in d.get("objects", []):
                objects[o] += 1
            text = " ".join(d.get("actions", [])) + " " + d.get("summary", "")
            for kw in keywords:
                if kw in text:
                    reasons[kw] += 1
        people_label, vehicles_label = state_counts.most_common(1)[0][0]
        events.append({
            "idx": i,
            "start_ts": frs[0]["ts"],
            "end_ts": frs[-1]["ts"],
            "state": {
                "people": people_label,
                "vehicles": vehicles_label,
                "top_objects": [o for o, _ in objects.most_common(3)],
            },
            "attention": bool(reasons),
            "attention_reasons": [k for k, _ in reasons.most_common(5)],
            "n_frames": len(frs),
            "sample_frame": frs[len(frs) // 2]["file"],
        })

    _write(out_dir, manifest, events, model, structural=False)
    log(f"[timeline] OK: {len(events)} 个事件, 其中 {sum(1 for e in events if e['attention'])} 个关注事件。")
    return events


def _load_keywords():
    raw = os.environ.get("FOOTAGE_GUARD_KEYWORDS", "")
    if raw.strip():
        return [k.strip() for k in raw.split(",") if k.strip()]
    return DEFAULT_KEYWORDS


def _write(out_dir, manifest, events, model, structural):
    with open(os.path.join(out_dir, "events.json"), "w", encoding="utf-8") as fh:
        json.dump(events, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 事件时间线（启发式聚合，需人工复核）")
    lines.append("")
    lines.append(f"- 视频: `{manifest['video']}`")
    lines.append(f"- 分析范围: {manifest['start']:.1f}s 起 · 取帧间隔 {manifest['interval']:g}s · 共 {len(manifest['frames'])} 帧")
    if model:
        lines.append(f"- VLM 模型: {model}")
    lines.append("")

    if structural:
        lines.append("## 说明")
        lines.append("- VLM 未启用（结构模式）：本文件仅给出时间覆盖，无事件语义。")
        lines.append("- 启动本地多模态端点后重跑 `scripts/run.sh`（去掉 --no-vlm）即可获得事件时间线。")
    else:
        lines.append("## 事件表")
        lines.append("")
        lines.append("| # | 起 | 止 | 人数 | 车辆 | 显著物体 | 关注 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for e in events:
            st = e["state"]
            objs = "、".join(st["top_objects"]) if st["top_objects"] else "-"
            flag = "⚠ " + "、".join(e["attention_reasons"][:3]) if e["attention"] else ""
            lines.append(
                f"| {e['idx']} | {fmt_ts(e['start_ts'])} | {fmt_ts(e['end_ts'])} "
                f"| {st['people']} | {st['vehicles']} | {objs} | {flag} |"
            )
        lines.append("")
        att = [e for e in events if e["attention"]]
        lines.append("## 关注事件")
        if att:
            for e in att:
                lines.append(
                    f"- 事件 {e['idx']}（{fmt_ts(e['start_ts'])}–{fmt_ts(e['end_ts'])}）："
                    f"命中关键词「{'、'.join(e['attention_reasons'])}」，代表帧 `frames/{e['sample_frame']}`"
                )
        else:
            lines.append("- 未命中关注关键词。")
        lines.append("")
        lines.append("## 说明")
        lines.append("- 事件按「人数/车辆数状态变化」切分，关键词命中仅作提示，**不是行为识别结果**；请结合原视频人工复核。")
        lines.append("- 本 skill 不推断个人身份、年龄、国籍、关系或意图；逐帧明细见 `frames/frame_XXXX.json`。")

    with open(os.path.join(out_dir, "event_timeline.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="事件时间线聚合")
    ap.add_argument("--out", required=True, help="extract_frames 的输出目录")
    args = ap.parse_args()
    try:
        build(args.out)
    except RuntimeError as exc:
        print(f"[timeline] ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
