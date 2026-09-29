# M0 · vLLM 冒烟（真实硬件 · 命令已备 / 当前未测）

> 硬件：当前无 DGX Spark 或相近算力设备，真实硬件测试未做。  
> **禁止**在无 GPU 机上伪造本文件对应的 `.log`。  
> 执行后把 stdout/stderr 落到 `notes/m0-smoke-moe.log` / `notes/m0-smoke-vl.log` / `notes/m0-smoke-openai.json`。

## 0) 前置
```bash
nvidia-smi -L
# 预期：两张 RTX 5090；记 UUID 到 notes/m0-gpus.txt
```

## 1) 单卡 NVFP4 30B MoE（示例端口 8001）
```bash
# 模型路径/镜像以实测设备实际为准；下列为契约形状
CUDA_VISIBLE_DEVICES=0 vllm serve <NVFP4_30B_MoE_MODEL> \
  --port 8001 --max-model-len 8192
curl -s http://127.0.0.1:8001/v1/models | tee notes/m0-smoke-moe-models.json
curl -s http://127.0.0.1:8001/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"auto","messages":[{"role":"user","content":"ping"}],"max_tokens":16}' \
  | tee notes/m0-smoke-moe-chat.json
```

## 2) Qwen3-VL-4B-FP8（footage-guard 默认 8000）
```bash
CUDA_VISIBLE_DEVICES=1 vllm serve Qwen/Qwen3-VL-4B-Instruct-FP8 \
  --port 8000 --max-model-len 32768
curl -s http://127.0.0.1:8000/v1/models | tee notes/m0-smoke-vl-models.json
# 小输入冒烟（勿喂大图）
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"auto","messages":[{"role":"user","content":"ping"}],"max_tokens":16}' \
  | tee notes/m0-smoke-vl-chat.json
```

## 3) 接 footage-guard（仅端点通后再跑管线）
```bash
export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
# 需 ffmpeg 在 PATH；否则管线 BLOCKED（记 STATE，不硬撑）
```

## PASS 标准
- `/v1/models` 返回非空 data
- 小 `chat/completions` HTTP 200 且有 choices[0].message
- 日志路径写入 CHECKLIST M0 三项
