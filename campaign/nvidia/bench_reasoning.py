#!/usr/bin/env python3
"""Benchmark high-end NVIDIA REASONING models for Notion page generation.
Real generation call per model (bounded), reports blocks parsed + latency + key used.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nvidia_client import NvidiaClient, load_keys
import prompts, blocks_spec

MODELS = [
    "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "nvidia/nemotron-3-ultra-550b-a55b",
    "nvidia/nemotron-3-super-120b-a12b",
    "deepseek-ai/deepseek-v4-pro",
    "deepseek-ai/deepseek-v4-flash",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2.6",
]
TOPIC = "ReLU activation function"
CTX = "max(0,x); solves vanishing gradients, sparsity, cheap; dying-ReLU problem"
URL = "https://jayitsaha.github.io/AI/explainers/relu_x_explainer.html"

def run():
    keys = load_keys()
    msgs = [{"role": "system", "content": prompts.SYSTEM_NOTION},
            {"role": "user", "content": prompts.notion_user_prompt(TOPIC, CTX, URL)}]
    print(f"{len(keys)} keys | topic: {TOPIC}\n")
    for m in MODELS:
        # try each key until one returns, so we also learn which keys work
        best = None
        for ki, key in enumerate(keys):
            c = NvidiaClient(keys=[key])
            t = time.time()
            try:
                raw = c.chat_long(m, msgs, max_tokens=8000, temperature=0.3, max_rounds=1)
                meta, blocks = blocks_spec.blocks_from_dsl(raw)
                dt = time.time() - t
                best = f"{m:48s} key{ki+1}  {len(blocks):3d} blocks  {dt:5.0f}s  depth={meta.get('depth','?')}"
                if len(blocks) >= 25:
                    break  # good enough, stop trying keys
            except Exception as e:
                dt = time.time() - t
                best = f"{m:48s} key{ki+1}  FAIL {dt:5.0f}s  {str(e)[:60]}"
        print(best, flush=True)

if __name__ == "__main__":
    run()
