#!/usr/bin/env bash
# 生成演示用样片（无需真实监控素材）：
#   - 前段：testsrc2 测试图（静态"场景"）
#   - 中段：移动方块 + 颜色块变化（模拟"有物体移动"）
#   - 尾段：灰场（模拟"无人场景"）
# 合计 ~30s，足够跑通 5s 间隔的事件时间线演示。
set -euo pipefail
OUT="${1:-assets/sample_footage.mp4}"
mkdir -p "$(dirname "$OUT")"

A=/tmp/fg_a.mp4
B=/tmp/fg_b.mp4
C=/tmp/fg_c.mp4

# A: 10s testsrc2（画面内容稳定，模拟静态场景）
ffmpeg -hide_banner -loglevel error -f lavfi -i "testsrc2=duration=10:size=1280x720:rate=15" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 "$A"

# B: 10s 移动方块（drawbox 随 t 移动，模拟物体移动/场景变化）
ffmpeg -hide_banner -loglevel error -f lavfi -i "color=c=0x223344:duration=10:size=1280x720:rate=15" -vf "drawbox=x='100+mod(t*120,1000)':y=300:w=180:h=120:color=yellow:t=fill,drawbox=x=500:y='400-mod(t*60,300)':w=120:h=120:color=red:t=fill" -c:v libx264 -pix_fmt yuv420p -crf 23 "$B"

# C: 10s 灰场（模拟无人/空旷场景）
ffmpeg -hide_banner -loglevel error -f lavfi -i "color=c=0x808080:duration=10:size=1280x720:rate=15" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 "$C"

# 拼接
ffmpeg -hide_banner -loglevel error -i "$A" -i "$B" -i "$C" \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart "$OUT"

rm -f "$A" "$B" "$C"
echo "样片已生成: $OUT（约 30s：静态场景 → 移动物体 → 空旷场景）"
