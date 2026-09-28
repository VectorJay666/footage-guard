#!/usr/bin/env python3
"""footage-guard · probe：用 ffprobe 提取视频元信息。

用法:
    python3 probe.py VIDEO [OUT_JSON]

OUT_JSON 缺省时打印到 stdout。
"""
import json
import os
import shutil
import subprocess
import sys


def probe(video: str) -> dict:
    """提取视频元信息；文件不存在或 ffprobe 失败时抛出异常。"""
    if not os.path.isfile(video):
        raise FileNotFoundError(f"视频文件不存在: {video}")
    if shutil.which("ffprobe") is None:
        raise RuntimeError("未找到 ffprobe，请先安装 ffmpeg（Ubuntu: apt install ffmpeg）")
    cmd = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("ffprobe 失败: " + (proc.stderr or "").strip()[:500])
    data = json.loads(proc.stdout or "{}")
    vstream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    fmt = data.get("format", {})
    try:
        duration = round(float(fmt.get("duration") or 0.0), 3)
    except ValueError:
        duration = 0.0
    fps = 0.0
    if vstream:
        r = vstream.get("avg_frame_rate") or vstream.get("r_frame_rate") or "0/1"
        try:
            num, den = r.split("/")
            if float(den):
                fps = round(float(num) / float(den), 3)
        except (ValueError, ZeroDivisionError):
            fps = 0.0
    return {
        "video": os.path.abspath(video),
        "size_bytes": int(fmt.get("size") or os.path.getsize(video)),
        "duration_s": duration,
        "width": int(vstream.get("width") or 0) if vstream else 0,
        "height": int(vstream.get("height") or 0) if vstream else 0,
        "fps": fps,
        "codec": (vstream or {}).get("codec_name", ""),
        "bit_rate": int(fmt.get("bit_rate") or 0),
        "nb_frames": int((vstream or {}).get("nb_frames") or 0),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    video = sys.argv[1]
    out_json = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        meta = probe(video)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"[probe] ERROR: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(meta, ensure_ascii=False, indent=2)
    if out_json:
        with open(out_json, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"[probe] OK -> {out_json}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
