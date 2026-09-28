#!/usr/bin/env python3
"""footage-guard · vlm_describe：调用本地 OpenAI 兼容多模态端点，逐帧生成结构化描述。

用法:
    python3 vlm_describe.py --out OUT_DIR [--model auto] [--concurrency 4]
                            [--limit N] [--focus "车辆,人"] [--dry-run]

环境变量:
    FOOTAGE_GUARD_BASE_URL   端点，默认 http://127.0.0.1:8000/v1
    FOOTAGE_GUARD_API_KEY    默认 EMPTY（不打印明文）
    FOOTAGE_GUARD_TIMEOUT_S  单请求超时秒，默认 120

产物: OUT_DIR/frames/frame_XXXX.json（帧级缓存，model+focus 不变时复跑直接复用）
      OUT_DIR/describe_report.json（本次运行统计）
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_BASE_URL = "http://127.0.0.1:8000/v1"
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", "0.0.0.0"}

SYSTEM_PROMPT = (
    "你是本地视频事件分析器，运行在用户本机。"
    "只描述画面中可观察的事实：人数、车辆数、显著物体、正在发生的动作、镜头视角。"
    "禁止推断或指认个人身份、年龄、国籍、关系、情绪或意图。"
)


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def warn_remote(base_url: str) -> None:
    host = (urllib.parse.urlparse(base_url).hostname or "").lower()
    if host not in LOCAL_HOSTS:
        log(f"[vlm] WARN: 端点 {base_url} 不是本机地址，视频帧将发送到远端服务（数据出网风险）。")


def http_json(url, payload=None, api_key=None, timeout=30):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=("POST" if data is not None else "GET"))
    req.add_header("User-Agent", "footage-guard/1.0")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def resolve_model(base_url, api_key, model, timeout=30):
    """model='auto' 时探测 /models，优先挑视觉模型；失败则保持原值。"""
    if model and model != "auto":
        return model
    try:
        data = http_json(base_url.rstrip("/") + "/models", api_key=api_key, timeout=timeout)
        ids = [m.get("id", "") for m in data.get("data", []) if m.get("id")]
    except Exception as exc:
        log(f"[vlm] WARN: 无法列出模型（{exc}），沿用 '{model}'")
        return model
    if not ids:
        return model
    for pref in ("vl", "vision", "video"):
        for i in ids:
            if pref in i.lower():
                return i
    return ids[0]


def coerce(obj: dict) -> dict:
    for k in ("people", "vehicles"):
        try:
            obj[k] = int(obj.get(k))
        except (TypeError, ValueError):
            obj[k] = None
    for k in ("objects", "actions"):
        v = obj.get(k)
        if isinstance(v, str):
            v = [v]
        elif not isinstance(v, list):
            v = []
        obj[k] = [str(x)[:60] for x in v][:10]
    s = obj.get("summary")
    obj["summary"] = str(s)[:200] if s not in (None, "") else ""
    return obj


def parse_desc(content: str) -> dict:
    content = (content or "").strip()
    content = re.sub(r"^```[a-zA-Z]*\s*|\s*```\s*$", "", content).strip()
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if m:
        try:
            return coerce(json.loads(m.group(0)))
        except json.JSONDecodeError:
            pass
    return {
        "people": None, "vehicles": None, "objects": [], "actions": [],
        "summary": content[:200], "parse_failed": True,
    }


def user_text(ts: float, focus: str) -> str:
    t = (
        "这是监控视频第 {ts:.1f} 秒的画面。"
        "只描述可观察内容，用 JSON 回答（people/vehicles 为整数，objects/actions 为字符串数组，summary 不超过 40 字）："
        '{{"people": 0, "vehicles": 0, "objects": [], "actions": [], "summary": ""}}'
    ).format(ts=ts)
    if focus:
        t += f"\n重点关注这些对象：{focus}。"
    return t


def cache_path(frames_dir: str, fname: str) -> str:
    return os.path.join(frames_dir, os.path.splitext(fname)[0] + ".json")


def read_cache(path, model, focus):
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("model") == model and d.get("focus") == (focus or "") and "desc" in d:
            return d
    except (json.JSONDecodeError, OSError):
        pass
    return None


def write_cache(path, model, focus, ts, desc):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"model": model, "focus": focus or "", "ts": ts, "desc": desc},
                  fh, ensure_ascii=False, indent=2)


def describe_one(job):
    base_url, model, api_key, timeout, fr, focus = job
    frames_dir, fname, ts = fr["dir"], fr["file"], fr["ts"]
    with open(os.path.join(frames_dir, fname), "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    body = {
        "model": model,
        "temperature": 0.1,
        "max_tokens": 256,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": user_text(ts, focus)},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ]},
        ],
    }
    last_err = None
    for attempt in range(3):
        try:
            data = http_json(base_url.rstrip("/") + "/chat/completions",
                             payload=body, api_key=api_key, timeout=timeout)
            content = data["choices"][0]["message"]["content"]
            desc = parse_desc(content)
            write_cache(cache_path(frames_dir, fname), model, focus, ts, desc)
            return ("ok", ts, desc.get("summary", "")[:40])
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError, KeyError, OSError) as exc:
            last_err = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    return ("fail", ts, str(last_err)[:200])


def run(out_dir, model="auto", concurrency=4, focus="", limit=None, dry_run=False):
    """执行描述流程，返回 (describe_report dict, resolved_model)。"""
    manifest_p = os.path.join(out_dir, "frames.json")
    if not os.path.isfile(manifest_p):
        raise RuntimeError(f"缺少 {manifest_p}，请先运行 extract_frames.py")
    with open(manifest_p, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    frames = manifest["frames"]
    if limit:
        frames = frames[:limit]
    frames_dir = os.path.join(out_dir, "frames")

    base_url = os.environ.get("FOOTAGE_GUARD_BASE_URL", DEFAULT_BASE_URL)
    api_key = os.environ.get("FOOTAGE_GUARD_API_KEY", "EMPTY")
    timeout = int(os.environ.get("FOOTAGE_GUARD_TIMEOUT_S", "120"))
    warn_remote(base_url)

    resolved = model
    if not dry_run:
        resolved = resolve_model(base_url, api_key, model)

    todo, cached = [], []
    for fr in frames:
        fr = dict(fr, dir=frames_dir)
        c = read_cache(cache_path(frames_dir, fr["file"]), resolved, focus)
        if c:
            cached.append(fr["file"])
        else:
            todo.append(fr)

    log(f"[vlm] 端点={base_url} 模型={resolved} 帧数={len(frames)} 待描述={len(todo)} 命中缓存={len(cached)}")
    if dry_run:
        report = {"model": resolved, "dry_run": True, "total": len(frames),
                  "todo": len(todo), "cached": len(cached), "failed": 0, "failed_frames": []}
        _save_report(out_dir, report)
        return report, resolved

    failed = []
    n_done = 0
    if todo:
        jobs = [(base_url, resolved, api_key, timeout, fr, focus) for fr in todo]
        with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
            futures = {pool.submit(describe_one, j): j[4]["file"] for j in jobs}
            for fut in as_completed(futures):
                status, ts, detail = fut.result()
                n_done += 1
                if status == "ok":
                    log(f"[vlm] {n_done}/{len(todo)} t={ts:.0f}s ok {detail}")
                else:
                    failed.append({"file": futures[fut], "error": detail})
                    log(f"[vlm] {n_done}/{len(todo)} t={ts:.0f}s FAIL {detail}")

    report = {
        "model": resolved, "dry_run": False, "total": len(frames),
        "described": n_done, "cached": len(cached),
        "failed": len(failed), "failed_frames": failed,
    }
    _save_report(out_dir, report)
    if failed:
        log(f"[vlm] WARN: {len(failed)}/{len(todo)} 帧描述失败，事件时间线将基于可用帧。")
    return report, resolved


def _save_report(out_dir, report):
    with open(os.path.join(out_dir, "describe_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)


def main() -> int:
    ap = argparse.ArgumentParser(description="本地 VLM 逐帧描述")
    ap.add_argument("--out", required=True, help="extract_frames 的输出目录")
    ap.add_argument("--model", default="auto", help="模型名或 auto（默认 auto）")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--limit", type=int, default=None, help="只描述前 N 帧（低成本冒烟）")
    ap.add_argument("--focus", default="", help="关注对象，逗号分隔")
    ap.add_argument("--dry-run", action="store_true", help="只检查端点/模型与缓存，不发描述请求")
    args = ap.parse_args()
    try:
        run(args.out, args.model, args.concurrency, args.focus, args.limit, args.dry_run)
    except (RuntimeError, OSError) as exc:
        print(f"[vlm] ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
