#!/usr/bin/env python3
"""Benchmark Groq models for HTML explainer generation (examples fed in as design refs).
Writes test files to campaign/groq/ (does NOT touch real explainers). Reports size+structure."""
import sys, os, re, time
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(AI, "campaign", "nvidia"))
from groq_client import GroqClient
import prompts

EXPL = os.path.join(AI, "explainers")
EXAMPLES = ["generalized_least_squares_gls_explainer.html", "dropout_explainer.html",
            "softmax_explainer.html"]
MODELS = ["openai/gpt-oss-120b", "qwen/qwen3-32b", "qwen/qwen3.6-27b",
          "llama-3.3-70b-versatile"]
TOPIC = "Exploding gradient problem"
SLUG = "exploding_gradient_problem"
CTX = ("Gradients grow exponentially through layers/timesteps when weight/Jacobian norms "
       ">1; NaN loss, unstable training; RNNs/deep nets; fixes: clipping, init, norm, residuals.")

SYSTEM = ("You are a senior front-end engineer and ML educator. Output ONE complete "
          "self-contained interactive HTML explainer starting at <!DOCTYPE html>. "
          "No markdown fences, no commentary, no <think> text in the output.")


def extract_html(t):
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S)
    i = t.lower().find("<!doctype")
    return t[i:] if i >= 0 else t.strip()


def examples_block():
    out = []
    for fn in EXAMPLES:
        p = os.path.join(EXPL, fn)
        if os.path.exists(p):
            out.append(f"===== EXAMPLE {fn} (match this quality/design/interactivity) =====\n"
                       + open(p).read())
    return "\n\n".join(out)


def main():
    c = GroqClient()
    print(f"{len(c.keys)} keys | topic: {TOPIC}\n")
    ex = examples_block()
    user = (f"Study these {len(EXAMPLES)} example explainers — they define the EXACT house "
            f"style (the :root light/dark tokens, collapsible cards, KaTeX, step-synced "
            f"interactive viz, progress dots, keyboard nav).\n\n{ex}\n\n"
            f"====================\nNOW BUILD A NEW ONE, same quality/style but a DIFFERENT "
            f"topic-appropriate visualization:\n\n{prompts.html_user_prompt(TOPIC, SLUG, CTX)}")
    for m in MODELS:
        t = time.time()
        try:
            raw = c.chat_long(m, [{"role": "system", "content": SYSTEM},
                                  {"role": "user", "content": user}],
                              max_tokens=32000, temperature=0.5, stop_marker="</html>")
            html = extract_html(raw)
            fn = os.path.join(HERE, f"test_{m.replace('/','_')}.html")
            open(fn, "w").write(html)
            kb = len(html) // 1024
            lines = html.count("\n") + 1
            katex = html.count("katex"); viz = len(re.findall(r"<canvas|<svg", html))
            cards = html.count('class="card"'); kbd = "ArrowRight" in html
            dark = "prefers-color-scheme" in html; eq = html.count("$$") // 2
            ok = "<!doctype" in html.lower() and "</html>" in html.lower()
            print(f"{m:34s} {kb:3d}KB {lines:4d}ln  katex={katex} viz={viz} cards={cards} "
                  f"eq={eq} kbd={int(kbd)} dark={int(dark)} complete={int(ok)}  {int(time.time()-t)}s",
                  flush=True)
        except Exception as e:
            print(f"{m:34s} FAIL {int(time.time()-t)}s  {str(e)[:60]}", flush=True)


if __name__ == "__main__":
    main()
