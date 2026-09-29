# narration (v4) — voiceover lines with final-video timestamps

- TTS: edge-tts 7.2.8 (https://github.com/rany2/edge-tts; code LGPLv3, MIT for srt_composer.py), voice **zh-CN-XiaoxiaoNeural**, rate +5%. It is an unofficial client of Microsoft Edge's online Read Aloud service; terms: Microsoft Services Agreement https://www.microsoft.com/servicesagreement , Azure TTS transparency note https://learn.microsoft.com/legal/cognitive-services/speech-service/text-to-speech/transparency-note . Commercial-use rights for the audio are not explicitly granted.
- Processing: leading/trailing silence trimmed (ffmpeg silenceremove −45 dB); voice gain +3.3 dB to −16 LUFS.
- The untested sentence comes from build-v4/config.json (`untested`); edit it and re-run build_v4.py + assemble_v4.py to swap subtitle+voice (other TTS clips are cached).
- Each line starts after its page's incoming crossfade ends and ends before the outgoing crossfade starts (asserted in assemble_v4.py). Subtitle column = on-screen bottom subtitle shown during that line.

| # | start | end | page | subtitle | voiceover |
|---|---|---|---|---|---|
| 1 | 0.90s | 6.30s | p01_title | 离线模式，未接入真模型 | 这是 FootageGuard 的使用演示。本次为离线模式，没有接入真模型。 |
| 2 | 8.40s | 12.76s | p02_pain | 想知道发生了什么，却没空看完 | 监控录了一整段，想知道发生了什么，却没空从头看完。 |
| 3 | 14.27s | 17.23s | p03_cloud | 也不想把录像传给云端模型 | 也不想把录像上传给云端的模型处理。 |
| 4 | 18.77s | 25.05s | p04_what | 每隔几秒取一帧，拼图，写报告 | 它会每隔几秒从录像里取一帧画面，拼成一张总览图，再写一份简短报告。 |
| 5 | 25.40s | 28.20s | p04_what | 全程离线，在你自己的电脑上 | 全程离线，在你自己的电脑上完成。 |
| 6 | 29.70s | 33.27s | p05_clip | 先看素材：一段 56.6 秒的路口录像 | 先看素材：这是一段56.6秒的路口录像。 |
| 7 | 34.60s | 38.01s | p06_term | 先把工具下载到本机 | 先把工具下载到本机，下面是实时录屏。 |
| 8 | 38.18s | 39.06s | p06_term | 下载完成 | 下载完成。 |
| 9 | 42.40s | 44.62s | p06_term | 检查这台电脑的运行环境 | 检查一下这台电脑的运行环境。 |
| 10 | 45.23s | 46.24s | p06_term | 只要一条命令 | 只要一条命令。 |
| 11 | 46.48s | 48.42s | p06_term | 全程在这台电脑上运行 | 全程在这台电脑上运行。 |
| 12 | 48.85s | 50.72s | p06_term | 完成，结果已生成 | 完成，结果已经生成。 |
| 13 | 52.43s | 55.00s | p07_montage | 11 张画面，拼成一张总览图 | 11张画面，拼成一张总览图。 |
| 14 | 55.35s | 57.91s | p07_montage | 每 5 秒一张，每张都标着时间 | 每5秒取一张，每张都标着时间。 |
| 15 | 61.93s | 66.25s | p08_report | 写明时长和看过的时间段 | 报告写明了录像时长，以及看过的时间段：零到五十秒。 |
| 16 | 66.60s | 70.86s | p08_report | 离线模式下，人和车标为未知 | 离线模式下不分析画面内容，人和车都标为未知。 |
| 17 | 72.37s | 75.30s | p09_local | 整个过程，录像都不用上传 | 整个过程，录像都不用上传到云端。 |
| 18 | 75.65s | 78.08s | p09_local | 也不会去识别画面里的人是谁 | 也不会去识别画面里的人是谁。 |
| 19 | 79.60s | 84.82s | p10_untested | 手头没有 DGX Spark，也没有相应算力的机器，暂时无法实测。 | 手头没有 DGX Spark，也没有相应算力的机器，暂时无法实测。 |
| 20 | 86.33s | 89.95s | p11_end | 一张图，快速浏览长录像 | 一张图，快速浏览长录像。欢迎试用。 |
