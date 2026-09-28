# assets/ — 演示素材

## 没有真实监控素材？生成一段样片

```bash
bash assets/make_sample.sh assets/sample_footage.mp4
```

生成约 30 秒的片子，三段内容：测试图（静态）→ 移动色块（物体移动）→ 灰场（空旷）。
`--interval 5` 下能出 6 帧，够跑通演示。依赖 ffmpeg。

仓库里已经有一份生成好的 `sample_footage.mp4`（2026-09-23 生成，30s / 1280x720 / h264，约 2.4MB），可以直接用；要重新生成再跑上面的命令。

## 用真实素材

1. mp4 放本机任意目录，建议给绝对路径。
2. `scripts/run.sh /abs/path/your.mp4 --interval 5`。
3. 隐私提醒：本 skill 只在本机处理。但如果你把 VLM 端点配到了远端（非 127.0.0.1），画面会发到那边——脚本会打 WARN，按 SKILL.md 要先征得用户同意。

## 说明

- 样片是 `testsrc2` / 纯色 / 移动 `drawbox` 合成的，没有真实人物，不碰 PII。
- 做 BENCHMARK 带/不带 skill 对照时，两边固定用同一份样片、同一套参数，别换。
