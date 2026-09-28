#!/usr/bin/env bash
# footage-guard 安装检查：依赖 + 本地端点连通性
# 用法:
#   scripts/install.sh            # 全量检查（含端点）
#   scripts/install.sh --offline  # 只查本地依赖，不连端点
set -euo pipefail
OFFLINE=0
if [ "${1:-}" = "--offline" ]; then OFFLINE=1; fi

echo "== footage-guard install check =="
fail=0

if command -v python3 >/dev/null 2>&1; then
  echo "[ok] python3 $(python3 -V 2>&1)"
else
  echo "[x]  缺少 python3"; fail=1
fi
for b in ffmpeg ffprobe; do
  if command -v "$b" >/dev/null 2>&1; then
    echo "[ok] $b"
  else
    echo "[x]  缺少 $b（Ubuntu/Debian: apt install ffmpeg；macOS: brew install ffmpeg）"; fail=1
  fi
done
if python3 -c "import PIL" 2>/dev/null; then
  echo "[ok] Pillow（可选）：关键帧拼图带时间戳标注"
else
  echo "[!]  无 Pillow（可选）：拼图退化为无标注网格；pip install Pillow 可启用"
fi
if [ "$fail" -ne 0 ]; then
  echo "== 依赖不完整，先补齐再运行 =="
  exit 1
fi

if [ "$OFFLINE" -eq 0 ]; then
  BASE="${FOOTAGE_GUARD_BASE_URL:-http://127.0.0.1:8000/v1}"
  KEY="${FOOTAGE_GUARD_API_KEY:-EMPTY}"
  echo "== 端点检查: ${BASE} =="
  if python3 - "$BASE" "$KEY" <<'PY'
import json, sys, urllib.request
base, key = sys.argv[1], sys.argv[2]
req = urllib.request.Request(base.rstrip("/") + "/models")
if key and key != "EMPTY":
    req.add_header("Authorization", "Bearer " + key)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
    ids = [m.get("id") for m in data.get("data", []) if m.get("id")]
    print("[ok] 端点可达，可用模型: " + (", ".join(ids) if ids else "(空)"))
except Exception as e:
    print(f"[x]  端点不可达: {e}")
    sys.exit(1)
PY
  then
    :
  else
    echo "提示: 端点不通时可先启动 vLLM（参考 references/troubleshooting.md），或用 --no-vlm 结构模式。"
  fi
fi
echo "== install check done =="
