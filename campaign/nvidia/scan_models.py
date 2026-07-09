#!/usr/bin/env python3
"""Scan many NVIDIA models for Notion-page generation quality/latency.
Bounded call per model (small output to reduce hang risk); reports blocks + time.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nvidia_client import NvidiaClient
import prompts, blocks_spec

CANDIDATES = [
    "nvidia/llama-3.3-nemotron-super-49b-v1.5",   # baseline
    "nvidia/nemotron-3-super-120b-a12b",
    "nvidia/nemotron-3-ultra-550b-a55b",
    "nvidia/nemotron-4-340b-instruct",
    "meta/llama-3.3-70b-instruct",
    "mistralai/mistral-large-3-675b-instruct-2512",
    "mistralai/mistral-large-2-instruct",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2.6",
    "deepseek-ai/deepseek-v4-flash",
    "deepseek-ai/deepseek-v4-pro",
]
TOPIC = "ReLU activation function"
CTX = "max(0,x); vanishing gradients, sparsity, dying ReLU; vs sigmoid/tanh"
URL = "https://jayitsaha.github.io/AI/explainers/relu_x_explainer.html"


def main():
    c = NvidiaClient()
    msgs = [{"role": "system", "content": prompts.SYSTEM_NOTION},
            {"role": "user", "content": prompts.notion_user_prompt(TOPIC, CTX, URL)}]
    for m in CANDIDATES:
        t = time.time()
        try:
            raw = c.chat_long(m, msgs, max_tokens=9000, temperature=0.3,
                              max_rounds=1)
            meta, blocks = blocks_spec.blocks_from_dsl(raw)
            neq = sum(1 for b in blocks if b["type"] == "equation")
            print(f"{m:46s} {len(blocks):3d} blk {neq:2d} eq  {int(time.time()-t):4d}s "
                  f"{meta.get('depth','?')}", flush=True)
        except Exception as e:
            print(f"{m:46s} FAIL {int(time.time()-t):4d}s  {str(e)[:55]}", flush=True)


if __name__ == "__main__":
    main()
