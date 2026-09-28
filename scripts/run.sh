#!/usr/bin/env bash
# footage-guard 入口：透传参数给 footage_guard.py
# 用法:
#   scripts/run.sh VIDEO [--interval 5] [--start 0] [--end 60] [--focus "车辆,人"]
#                        [--model auto] [--no-vlm] [--out DIR] [--max-frames 240]
# 完整参数: python3 scripts/footage_guard.py --help
set -euo pipefail
SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[run] ERROR: 未找到 python3" >&2
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  echo "[run] ERROR: 未找到 ffmpeg/ffprobe，先执行 scripts/install.sh --offline 查看依赖清单" >&2
  exit 1
fi
exec python3 "${SKILL_ROOT}/scripts/footage_guard.py" "$@"
