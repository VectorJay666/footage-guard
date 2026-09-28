#!/usr/bin/env python3
"""footage-guard local OpenAI-compatible VLM STUB (NOT Spark / NOT real VLM).

Purpose: let Agent/orchestration call FOOTAGE_GUARD_BASE_URL without a GPU.
Returns fixed JSON descriptions. Never claim this is a Spark or vLLM result.

Usage:
  python3 scripts/vlm_stub_server.py [--port 8000]
  export FOOTAGE_GUARD_BASE_URL=http://127.0.0.1:8000/v1
  curl http://127.0.0.1:8000/v1/models
"""
from __future__ import annotations

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STUB_MODEL = "footage-guard-vlm-stub"
FIXED_DESC = {
    "people": 1,
    "vehicles": 0,
    "objects": ["door", "bag"],
    "actions": ["walk", "open"],
    "summary": "STUB: one person near a door with a bag (not real VLM).",
}


def _models_body():
    return {
        "object": "list",
        "data": [
            {
                "id": STUB_MODEL,
                "object": "model",
                "owned_by": "footage-guard-stub",
                "note": "LOCAL STUB — not Spark, not vLLM",
            }
        ],
    }


def _chat_body(req_model: str | None):
    content = json.dumps(FIXED_DESC, ensure_ascii=False)
    model = req_model if req_model and req_model != "auto" else STUB_MODEL
    return {
        "id": "chatcmpl-stub",
        "object": "chat.completion",
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "stub": True,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "footage-guard-vlm-stub/1.0"

    def log_message(self, fmt, *args):
        print(f"[vlm-stub] {self.address_string()} {fmt % args}", flush=True)

    def _send(self, code: int, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/v1/models", "/models", "/health"):
            if path == "/health":
                self._send(200, {"ok": True, "stub": True, "model": STUB_MODEL})
            else:
                self._send(200, _models_body())
            return
        self._send(404, {"error": {"message": f"stub unknown path: {path}", "type": "stub"}})

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send(400, {"error": {"message": "invalid json", "type": "stub"}})
            return
        if path in ("/v1/chat/completions", "/chat/completions"):
            self._send(200, _chat_body(payload.get("model")))
            return
        self._send(404, {"error": {"message": f"stub unknown path: {path}", "type": "stub"}})


def main() -> int:
    ap = argparse.ArgumentParser(description="Local VLM stub (NOT Spark)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"[vlm-stub] listening http://{args.host}:{args.port}/v1 "
        f"(STUB only — set FOOTAGE_GUARD_BASE_URL=http://{args.host}:{args.port}/v1)",
        flush=True,
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[vlm-stub] stopped", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
