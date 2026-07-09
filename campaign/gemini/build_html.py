#!/usr/bin/env python3
"""Build an HTML explainer with Gemini (Sonnet alternative), feeding EXAMPLE HTML files
as design references so it matches the house style.

Usage:
  python3 campaign/gemini/build_html.py --model gemini-3.1-pro-preview \
      --slug relu_x --topic "ReLU activation" --context "max(0,x)..."
"""
import argparse, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(AI, "campaign", "nvidia"))
from gemini_client import GeminiClient
import prompts  # reuse the NVIDIA html prompt spec

EXPLAINERS = os.path.join(AI, "AI", "explainers")
# diverse, high-quality references so Gemini learns the design system + varied viz types
# Ample, diverse references so Gemini nails the house style across viz types.
# (Daily quota is per-REQUEST not per-token, so more examples don't cost quota.)
EXAMPLES = [
    "generalized_least_squares_gls_explainer.html",  # gold standard — regression/scatter
    "dropout_explainer.html",                        # network diagram + slider
    "softmax_explainer.html",                        # bar-chart parameter exploration
    "mixed_precision_training_explainer.html",       # bit-layout + histogram (architecture/data)
    "perceptron_learning_rule_convergence_theorem_explainer.html",  # animated decision boundary
]

SYSTEM = ("You are a senior front-end engineer and ML educator. You produce ONE complete, "
          "self-contained, production-grade interactive HTML explainer. Output ONLY raw HTML "
          "starting at <!DOCTYPE html>. No markdown fences, no commentary.")


def build_examples_block():
    blocks = []
    for fn in EXAMPLES:
        p = os.path.join(EXPLAINERS, fn)
        if os.path.exists(p):
            html = open(p).read()
            blocks.append(f"===== EXAMPLE: {fn} (match this quality, design tokens, "
                          f"card structure, KaTeX usage, and interactivity) =====\n{html}")
    return "\n\n".join(blocks)


def strip_fences(t):
    t = t.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t); t = re.sub(r"\n?```\s*$", "", t)
    return t.strip()


_EXAMPLES_CACHE = None

def build(model, slug, topic, context, max_tokens=48000, client=None):
    global _EXAMPLES_CACHE
    if _EXAMPLES_CACHE is None:
        _EXAMPLES_CACHE = build_examples_block()
    examples = _EXAMPLES_CACHE
    spec = prompts.html_user_prompt(topic, slug, context)
    user = (f"Study these {len(EXAMPLES)} example explainers from our vault. They define the "
            f"EXACT house style you must match — the :root light/dark design tokens, the "
            f"collapsible card layout, KaTeX math, the step-synced interactive visualization, "
            f"progress dots, and keyboard nav.\n\n{examples}\n\n"
            f"========================================\n"
            f"NOW BUILD A NEW ONE for this topic, matching that quality and style exactly "
            f"(but with a DIFFERENT, topic-appropriate visualization):\n\n{spec}")
    c = client or GeminiClient()
    t0 = time.time()
    text, finish = c.generate(model, SYSTEM, user, max_tokens=max_tokens, temperature=0.6)
    html = strip_fences(text)
    if "<!doctype" not in html.lower():
        raise ValueError(f"no doctype (finish={finish}, {len(html)} chars)")
    path = os.path.join(EXPLAINERS, f"{slug}_explainer.html")
    open(path, "w").write(html)
    return path, len(html), int(time.time() - t0), finish


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--context", default="")
    ap.add_argument("--max-tokens", type=int, default=48000)
    a = ap.parse_args()
    try:
        path, n, dt, finish = build(a.model, a.slug, a.topic, a.context, a.max_tokens)
        print(f"{a.slug} | HTML:y | {n//1024}KB | {dt}s | finish={finish} | {a.model}")
    except Exception as e:
        print(f"{a.slug} | HTML:n | ERROR: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
