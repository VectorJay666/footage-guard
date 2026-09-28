# Demo 脚本 · footage-guard（可贴仓库）

## 30 秒电梯稿（背这版）
「监控复盘别再全程拖进度条，也别为了两分钟片段把画面送上云。  
footage-guard 是本地 Skill：视频进，事件时间线、关键帧拼图、复盘报告出；默认数据不出网。  
今天没有工作站入口，我们不装已上卡——交的是可跑 Skill、离线 Demo，和一张诚实的 BLOCKED 评测表。  
有 5090 或 Spark，只换 OpenAI 兼容端点，Skill 不用重写。」

## 评委 Demo 步骤（约 3–4 分钟）

### 0. 开场定调（15s）
- 一句话：隐私本地复盘 Skill。  
- 主动声明：BENCHMARK 第二部分 **BLOCKED（无工作站入口）**；数字不造假。

### 1. 离线产物（90s）— 主路径
1. 打开仓库已有产物目录（样片跑出的 `*.footage-guard/` 或 Frontend Demo 页）。  
2. 展示 `montage.jpg`（时间戳拼图）。  
3. 展示 `report.md` / `events.json` / timeline。  
4. 指出 stdout 契约形态：末行 `MEDIA:/绝对路径/montage.jpg`（可用 `references/output-contract.md` 对照）。

### 2. 治理与边界（60s）— 差异化
1. 打开 `SKILL.md`：`Use when` / `Not for`。  
2. 打开 `evals/evals.json`：指 neg-1/2/3（身份、转码、实时）。  
3. 打开 `skill-card.md`：Owner + 风险表。  
4. 一句话：边界写进测试集，不是 PPT 口号。

### 3. 诚实证据板（45s）
1. `TEST-REPORT.md`：开发机管线 9+4 PASS（含 `--no-vlm` 降级）。  
2. `BENCHMARK.md`：第一部分 PASS；第二部分 BLOCKED。  
3. `notes/accept-matrix-5090-vs-stub.md`：分栏，5090 空、stub 不算分。

### 4. 收束（15s）
「入口一到，按 `notes/m0-vllm-smoke.md` 冒烟，空栏变真数——今天先交不丢人的完整骨架。」

## 禁止话术
- 「我们已经在 Spark/GB10 上跑通五维」  
- 「stub 分数可以当正式 BENCHMARK」  
- 「建议动作已自动下发到生产」
