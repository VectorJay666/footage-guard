#!/usr/bin/env python3
"""footage-guard · extract_frames：关键帧抽取 + 帧清单 + 关键帧拼图。

用法:
    python3 extract_frames.py VIDEO --out OUT_DIR [--interval 5] [--start 0]
                                [--end SECONDS] [--max-frames 240] [--no-montage]

产物（OUT_DIR 下）:
    meta.json            视频元信息
    frames.json          帧清单 {"video","start","interval","frames":[{file,ts}]}
    frames/frame_0001.jpg 抽帧（宽度 <=1280 的 JPEG）
    montage.jpg          带时间戳标注的关键帧拼图（可选）
"""
import argparse
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys

try:
    from PIL import Image, ImageDraw
    HAVE_PIL = True
except Exception:  # Pillow 为可选依赖
    HAVE_PIL = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe as _probe  # noqa: E402

MAX_W = 1280
MAX_TILES = 32          # 拼图最多展示 32 帧，超出均匀下采样
CELL_W, CELL_H, CAP_H = 320, 180, 20


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def run_ffmpeg(args, allow_fail: bool = False):
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error"] + args,
        capture_output=True, text=True,
    )
    if proc.returncode != 0 and not allow_fail:
        raise RuntimeError("ffmpeg 失败: " + (proc.stderr or "").strip()[:600])
    return proc


def extract(video, out_dir, interval, start, end, max_frames, montage=True):
    """执行抽帧，返回 (manifest, montage_path_or_None)。"""
    meta = _probe.probe(video)
    duration = meta["duration_s"]
    if duration <= 0:
        raise RuntimeError("无法从 ffprobe 获取视频时长")

    start = max(0.0, float(start))
    end = min(duration, float(end)) if end else duration
    span = end - start
    if span < interval / 2:
        raise RuntimeError(
            f"分析范围过短: 范围 {span:.1f}s 按 {interval:g}s 间隔抽不出任何帧，"
            f"请扩大范围或调小 --interval"
        )

    # 帧数上限：超限时自动放大间隔，保证 VLM 成本可控
    n_expected = max(1, int(math.floor(span / interval)))
    eff_interval = interval
    if n_expected > max_frames:
        eff_interval = span / max_frames
        log(f"[extract] WARN: 按 {interval:g}s 间隔将产生 {n_expected} 帧，超过上限 {max_frames}，"
            f"自动放大间隔为 {eff_interval:.1f}s")
    interval = eff_interval

    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    for old in glob.glob(os.path.join(frames_dir, "frame_*.jpg")):
        os.remove(old)

    cmd = [
        "-ss", f"{start:.3f}", "-t", f"{span:.3f}", "-i", video,
        "-vf", f"fps=1/{interval:g},scale='min({MAX_W},iw)':-2",
        "-q:v", "3",
        os.path.join(frames_dir, "frame_%04d.jpg"),
    ]
    run_ffmpeg(cmd)

    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    if not files:
        raise RuntimeError("抽帧失败：未生成任何帧")
    frames = [{"file": f, "ts": round(start + i * interval, 2)} for i, f in enumerate(files)]
    frames = [f for f in frames if f["ts"] < end - 1e-3] or frames[:1]

    manifest = {"video": meta["video"], "start": start, "interval": interval, "frames": frames}
    with open(os.path.join(out_dir, "frames.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    log(f"[extract] OK: {len(frames)} 帧, 间隔 {interval:g}s, 范围 {start:.1f}s–{end:.1f}s")

    montage_path = None
    if montage:
        montage_path = _build_montage(frames_dir, frames, os.path.join(out_dir, "montage.jpg"))
        if montage_path:
            log(f"[extract] 拼图 -> {montage_path}")
        else:
            log("[extract] WARN: 拼图生成失败（不影响事件时间线）")
    return manifest, montage_path


# ---------------------------------------------------------------- 拼图


def _build_montage(frames_dir, frames, out_path):
    try:
        if len(frames) > MAX_TILES:
            idxs = {int(round(i * (len(frames) - 1) / (MAX_TILES - 1))) for i in range(MAX_TILES)}
            picked = [frames[i] for i in sorted(idxs)]
        else:
            picked = frames

        if HAVE_PIL:
            resample = getattr(Image, "Resampling", Image).LANCZOS
            cols = 4
            rows = math.ceil(len(picked) / cols)
            canvas = Image.new("RGB", (cols * CELL_W, rows * (CELL_H + CAP_H)), (16, 16, 16))
            draw = ImageDraw.Draw(canvas)
            for i, fr in enumerate(picked):
                p = os.path.join(frames_dir, fr["file"])
                img = Image.open(p).convert("RGB").resize((CELL_W, CELL_H), resample)
                r, c = divmod(i, cols)
                x0, y0 = c * CELL_W, r * (CELL_H + CAP_H)
                canvas.paste(img, (x0, y0))
                draw.rectangle([x0, y0 + CELL_H, x0 + CELL_W, y0 + CELL_H + CAP_H], fill=(0, 0, 0))
                draw.text((x0 + 6, y0 + CELL_H + 4), f"t={fr['ts']:.0f}s", fill=(255, 255, 255))
            canvas.save(out_path, quality=88)
            return out_path

        # Pillow 缺失：仅当帧连续且 <=32 时用 ffmpeg tile 兜底（无时间戳标注）
        if len(picked) == len(frames) and len(frames) <= MAX_TILES:
            rows = math.ceil(len(frames) / 4)
            run_ffmpeg([
                "-framerate", "1",
                "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
                "-vf", f"tile=4x{rows}",
                "-frames:v", "1", "-q:v", "3", "-y", out_path,
            ], allow_fail=True)
            if os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
                return out_path
        return None
    except Exception as exc:  # 拼图失败不阻断主流程
        log(f"[extract] 拼图异常: {exc}")
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="关键帧抽取")
    ap.add_argument("video")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--interval", type=float, default=5.0, help="取帧间隔秒（默认 5）")
    ap.add_argument("--start", type=float, default=0.0, help="起始秒（默认 0）")
    ap.add_argument("--end", type=float, default=None, help="结束秒（默认全片）")
    ap.add_argument("--max-frames", type=int, default=240, help="帧数上限（默认 240）")
    ap.add_argument("--no-montage", action="store_true", help="不生成拼图")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    try:
        extract(args.video, args.out, args.interval, args.start, args.end,
                args.max_frames, montage=not args.no_montage)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"[extract] ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
