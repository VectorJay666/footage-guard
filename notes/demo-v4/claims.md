# claims.md (v4) — every factual sentence/number (on screen and spoken) in out-v4/demo.mp4 and what backs it

**v4 re-recorded the terminal take and re-ran the pipeline** (2026-09-29 15:31 Asia/Shanghai) from a fresh clone of **72d7018** (72d7018238df85857de701d87006be5e0f484ed0), which equals `git ls-remote origin main` checked just before recording. The same CC0 input file and the same command (`scripts/run.sh … --interval 5 --no-vlm`) were used. Result vs the v2 run (ed4eb34): events.json, frames.json, meta.json, event_timeline.md, montage.jpg and all 11 frame JPEGs are byte-identical (same SHA-256). report.md differs only in line 3 (生成时间 15:02 → 15:31) and the output path. All numbers shown are from the v4 run.

Paths: run.log / run.cast = out-v4/; run output = <demo-root>/v4/run-out/ (montage.jpg, events.json, report.md copied to out-v4/); repo = <demo-root>/v4/footage-guard @ 72d7018 (unmodified). Times = final video mm:ss. Full voiceover/subtitle list with timestamps: narration.md / narration.srt.

## Transitions and terminal integrity
- Crossfade (`xfade=transition=fade`, 0.5 s) between every pair of pages; none inside a page.
- Terminal page 00:33.90–00:52.03: static blank-terminal pre-roll labeled 「录屏即将开始（静止）」 (incoming fade 00:33.90–00:34.40 is inside it) → **uncut 1× take 00:35.90–00:48.75** (`$ git clone` … `MEDIA:` line; 12.8 s = run.cast elapsed; label 「实时录屏 ×1（未加速、未剪辑）」) → last-frame hold to 00:51.35 (2.6 s, label 「已完成（末行定格）」) → static tail; outgoing fade starts 00:51.53. PSNR of final video vs. rendered terminal page over 00:35.90–00:51.35: min 48.2 dB, avg 52.1 dB (re-encode noise only, no blending).
- The v2/v3 keyframe close-up sequence is removed; only montage.jpg is shown (slow 6% zoom).

## Pages
| page (start) | On-screen text / spoken | Backing |
|---|---|---|
| Title 00:00.00 | 「使用演示」「FootageGuard」「长录像 → 一张总览图 + 一份简短报告」, repo URL; icons video→grid→report; subtitle 「离线模式，未接入真模型」; voice 00:00.90–00:06.30「这是 FootageGuard 的使用演示。本次为离线模式，没有接入真模型。」 | README.md:3 (关键帧拼图 + 复盘报告); run.log:28 (`--no-vlm`), run.log:34; report.md:7 |
| Pain 00:07.50 | 「录像太长，看不过来」; 00:08.40–00:12.76「监控录了一整段，想知道发生了什么，却没空从头看完。」 | persona scenario, not a claim about this run; README.md:32 |
| Cloud 00:13.37 | 「也不想交给云端」, cloud-with-slash icon; 00:14.27–00:17.23「也不想把录像上传给云端的模型处理。」 | persona motivation; README.md:32 (云端视频分析踩隐私红线) |
| What it does 00:17.87 | 「FootageGuard 能帮你做什么」 ① 按间隔取关键帧 ② 拼成一张总览图 ③ 写一份简短报告; 00:18.77–00:25.05「它会每隔几秒从录像里取一帧画面，拼成一张总览图，再写一份简短报告。」 00:25.40–00:28.20「全程离线，在你自己的电脑上完成。」 | run.log:32 (`间隔 5s`), :33 (拼图), :39 (report); run is fully local: run.log:29–39, VLM skipped run.log:34, scripts/footage_guard.py:151–152 |
| Source clip 00:28.80 | subtitle 「先看素材：一段 56.6 秒的路口录像」; credit line; 00:29.70–00:33.27「先看素材：这是一段56.6秒的路口录像。」 | run.log:30; report.md:5; input-source.md |
| Terminal 00:33.90 | real take (clone → `git log` shows **72d7018** → install check → run → `MEDIA:`); subtitles/voice 00:34.60–00:38.01「先把工具下载到本机，下面是实时录屏。」 00:38.18–00:39.06「下载完成。」 00:42.40–00:44.62「检查一下这台电脑的运行环境。」 00:45.23–00:46.24「只要一条命令。」 00:46.48–00:48.42「全程在这台电脑上运行。」 00:48.85–00:50.72「完成，结果已经生成。」 | run.cast; run.log:6 (clone), :14–15 (72d7018), :18–25 (environment check), :28 (single command), :29–39 (local steps), :39 (MEDIA) |
| Montage 00:51.53 | pill 「本次生成的总览图」+ montage.jpg; 00:52.43–00:55.00「11张画面，拼成一张总览图。」 00:55.35–00:57.91「每5秒取一张，每张都标着时间。」 | run.log:32 (`11 帧, 间隔 5s`); montage.jpg (tiles labeled t=0s…50s); events.json:13 |
| Report 01:01.03 | 「附一份简短报告」 rows: 录像时长 56.6 秒 / 取帧 每 5 秒一张，共 11 张 / 看过的时间段 00:00 – 00:50 / 人数 / 车辆 未知 / 未知（离线模式未分析画面内容）; 「数据摘自本次生成的 report.md」; 01:01.93–01:06.25「报告写明了录像时长，以及看过的时间段：零到五十秒。」 01:06.60–01:10.86「离线模式下不分析画面内容，人和车都标为未知。」 | report.md:5 (56.6s), :6 (间隔 5s · 共 11 帧), :13 (00:00–00:50, 未知, 未知), :7 (VLM 未启用); event_timeline.md:7 (无事件语义) |
| Local 01:11.47 | 「录像留在自己的电脑上」, laptop+shield icon; 01:12.37–01:15.30「整个过程，录像都不用上传到云端。」 01:15.65–01:18.08「也不会去识别画面里的人是谁。」 | run.log:29–39 all local, :34 no model call; report.md:32 (不推断个人身份) |
| Untested 01:18.70 | 「接入真模型：待实测」, chip icon; subtitle+voice 01:19.60–01:24.82「手头没有 DGX Spark，也没有相应算力的机器，暂时无法实测。」 | wording supplied by the user/parent (final); consistent with repo HEAD commit message run.log:15 ("no DGX Spark or comparable-compute device available; real-hardware testing not done"). No performance numbers anywhere in the video. |
| End 01:25.43 | 「FootageGuard」「长录像 → 一张总览图 + 一份简短报告」, repo URL; credits 「素材：Raysonho / Wikimedia Commons（CC0） 音乐：Loyalty Freak Music《Softly》（CC0）」; subtitle 「一张图，快速浏览长录像」; 01:26.33–01:29.95「一张图，快速浏览长录像。欢迎试用。」 | README.md:3; input-source.md; music-source.md |

Badges: 「离线模式 · 未接真模型」 top-right on source clip and terminal pages (run.log:28, :34).
Not in the video any more (removed per feedback): eval IDs, endpoint/localhost, stub/BLOCKED, licence talk (except credits), 5090, per-frame close-ups.
