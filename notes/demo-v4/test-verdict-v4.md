# Test verdict — demo v4 (baseline 72d7018)
Date: 2026-09-29 ~15:40 Asia/Shanghai. Verdict: **PASS**

| Rule | Result | Evidence |
|---|---|---|
| 1 Terminal uncut clone→MEDIA:, commit = main HEAD | PASS | run.log:6–39; git log shows 72d7018 = ls-remote origin HEAD; take 00:35.90–00:48.75 (12.85s) vs run.cast elapsed 12.8s → real-time, labeled 未加速未剪辑 |
| 2 montage in MEDIA: = file shown | PASS | montage.jpg sha256 a39b5edd… = v2; events.json adc84067… = v2; montage page at 00:51.53 |
| 3 Opening disclaimer | PASS | 00:00 subtitle 离线模式，未接入真模型 |
| Voiceover ⊆ subtitles | PASS | faster-whisper small transcript (<test-root>/asr.txt) matches narration.srt 20 lines; no extra claims |
| Numbers from this run | PASS | 56.6s / 11帧 / 每5秒 / 0–50秒 / 未知 = run.log:30–32, report.md |
| No 5090 / no perf numbers / untested line = user wording | PASS | srt+claims grep; 01:19.60 |
| Music CC0 | PASS | Softly, sha256 6fea22d3…, FMA + Commons CC0 |
| Transitions only between pages | PASS | PSNR min 48.2 dB over terminal segment (Vector); frame samples 36.2/42/48.9/51 clean |
| Repo consistency @72d7018 | PASS (minor) | leftover label FINAL_ACCEPTANCE.md:17 “5090+spark.env” — fix in final push |

Open risk (non-blocking): edge-tts is an unofficial client; commercial-use terms for its audio unclear. Repo has no LICENSE file.
Rule 4 (notes/ push) pending: will verify push only adds notes/ v4 material + FINAL_ACCEPTANCE.md:17 label change.
