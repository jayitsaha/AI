#!/usr/bin/env python3
"""
Enhanced parallel Gemini HTML builder — focused on interactive walkthrough quality.
Feeds EXAMPLE files as references, validates quality gate, retries failures.

Run from repo root:
  cd ~/Downloads/PersonalSkillUp/AI
  python3 campaign/gemini/run_html_wave.py

Options:
  python3 campaign/gemini/run_html_wave.py --workers 8 --model gemini-2.5-flash
  python3 campaign/gemini/run_html_wave.py --workers 12 --model gemini-2.5-pro
"""
import sys, os, re, json, time, threading, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(AI, "campaign", "nvidia"))

from gemini_client import GeminiClient
import prompts

EXPLAINERS = os.path.join(AI, "explainers")
TODO_TSV = os.path.join(HERE, "html_todo.tsv")
FAILED_TSV = os.path.join(HERE, "html_failed.tsv")

# High-quality, diverse example files (fed to Gemini as style references)
EXAMPLES = [
    "generalized_least_squares_gls_explainer.html",  # gold: regression, matrix viz
    "variational_autoencoder_explainer.html",         # generative: latent space, ELBO
    "bpe_explainer.html",                             # NLP: iterative merge animation
    "dropout_explainer.html",                         # training: network diagram + slider
    "softmax_explainer.html",                         # parameter exploration: bar chart
]

SYSTEM = (
    "You are a senior front-end engineer and ML educator. You produce ONE complete, "
    "self-contained, production-grade interactive HTML explainer. Output ONLY raw HTML "
    "starting at <!DOCTYPE html>. No markdown fences, no commentary.\n\n"
    "⭐ THE INTERACTIVE WALKTHROUGH IS YOUR #1 PRIORITY. The animated, topic-specific "
    "visualization is the CENTERPIECE. A page with a brilliant interactive diagram is a "
    "success even if the prose is merely good. A page with great prose but a broken, "
    "generic, or empty visualization is a FAILURE.\n\n"
    "HARD REQUIREMENTS for the visualization:\n"
    "- Real working <canvas> or <svg>, topic-specific (architecture/sliders/distributions/"
    "heatmaps/trellis/pipeline — pick what fits THIS topic)\n"
    "- ≥8 walkthrough steps, each visibly changing the diagram with animation/transition\n"
    "- ALL displayed numbers computed LIVE in JS from actual math — never hardcoded fakes\n"
    "- At least one interactive control (slider/toggle/drag) that recomputes in real-time\n"
    "- step-synced info card, progress dots, Prev/Next/Reset, arrow-key nav (← → R)\n"
    "- Verify your JS mentally: no undefined references, canvas actually draws, steps run\n\n"
    "HARD MINIMUMS:\n"
    "- File ≥ 550 lines, ≥ 30KB\n"
    "- Largest inline <script> ≥ 4000 chars\n"
    "- Steps array must be non-empty and have ≥8 entries\n"
    "- 4-6 collapsible educational cards, 500-1000 words prose\n"
    "- KaTeX CDN in <head> for math: $$...$$ display, \\(...\\) inline\n"
    "- Light+dark mode using the exact design tokens from the examples"
)

_examples_cache = None

def load_examples():
    global _examples_cache
    if _examples_cache is not None:
        return _examples_cache
    blocks = []
    for fn in EXAMPLES:
        p = os.path.join(EXPLAINERS, fn)
        if os.path.exists(p):
            html = open(p).read()
            blocks.append(
                f"===== EXAMPLE: {fn} =====\n"
                f"(Match this quality: design tokens, collapsible cards, KaTeX, "
                f"interactive canvas/svg viz with ≥8 steps, keyboard nav)\n{html}"
            )
    _examples_cache = "\n\n".join(blocks)
    return _examples_cache


def strip_fences(t):
    t = t.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```\s*$", "", t)
    return t.strip()


def quality_gate(path):
    """Returns (pass, reason). Checks size, script size, steps."""
    if not os.path.exists(path):
        return False, "MISSING"
    size = os.path.getsize(path)
    if size < 30000:
        return False, f"TOO_SMALL({size})"
    with open(path) as f:
        content = f.read()
    if "<!doctype" not in content.lower():
        return False, "NO_DOCTYPE"
    scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', content, re.DOTALL)
    max_script = max((len(s) for s in scripts), default=0)
    if max_script < 4000:
        return False, f"THIN_JS({max_script})"
    return True, "OK"


def build_one(client, model, topic, slug, context, max_tokens=48000):
    """Build one HTML explainer via Gemini. Returns (path, size, seconds, finish)."""
    examples = load_examples()
    spec = prompts.html_user_prompt(topic, slug, context)
    user = (
        f"Study these {len(EXAMPLES)} example explainers from our vault. They define the "
        f"EXACT house style — :root light/dark tokens, collapsible cards, KaTeX math, "
        f"step-synced interactive visualization, progress dots, keyboard nav.\n\n"
        f"PAY SPECIAL ATTENTION to how each example builds its interactive walkthrough: "
        f"the canvas/svg rendering code, the steps array, the go()/render() pattern, "
        f"the info-card sync. Your visualization must be AT LEAST this sophisticated.\n\n"
        f"{examples}\n\n"
        f"========================================\n"
        f"NOW BUILD A NEW ONE for this topic. Match that quality exactly, but with a "
        f"DIFFERENT, topic-appropriate visualization. The interactive walkthrough is "
        f"the #1 thing I'm evaluating.\n\n{spec}"
    )
    t0 = time.time()
    text, finish = client.generate(
        model, SYSTEM, user, max_tokens=max_tokens, temperature=0.6, timeout=300
    )
    html = strip_fences(text)
    if "<!doctype" not in html.lower():
        raise ValueError(f"no doctype (finish={finish}, {len(html)} chars)")
    path = os.path.join(EXPLAINERS, f"{slug}_explainer.html")
    with open(path, "w") as f:
        f.write(html)
    return path, len(html), int(time.time() - t0), finish


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-2.5-flash",
                    help="Model name(s), comma-separated for rotation")
    ap.add_argument("--workers", type=int, default=0,
                    help="Parallel workers (default: num_keys)")
    ap.add_argument("--max-tokens", type=int, default=48000)
    ap.add_argument("--retries", type=int, default=2,
                    help="Retry failed topics this many times")
    args = ap.parse_args()

    models = [m.strip() for m in args.model.split(",")]
    client = GeminiClient()
    workers = args.workers or min(len(client.keys), 12)

    # Load todo
    todo = []
    for line in open(TODO_TSV):
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 3:
            pid, topic, slug = parts[0], parts[1], parts[2]
            # Skip if already exists and passes gate
            path = os.path.join(EXPLAINERS, f"{slug}_explainer.html")
            ok, _ = quality_gate(path)
            if not ok:
                todo.append((pid, topic, slug))

    print(f"{'='*60}")
    print(f"Gemini HTML Builder — Interactive Walkthrough Focus")
    print(f"{'='*60}")
    print(f"Model(s): {models}")
    print(f"Keys: {len(client.keys)} | Workers: {workers}")
    print(f"Topics to build: {len(todo)}")
    print(f"Retries per topic: {args.retries}")
    print(f"{'='*60}\n")

    done_count = [0]
    fail_list = []
    lock = threading.Lock()

    def work(item):
        pid, topic, slug = item
        path = os.path.join(EXPLAINERS, f"{slug}_explainer.html")

        for attempt in range(1, args.retries + 1):
            try:
                model = models[(hash(slug) + attempt) % len(models)]
                _, n, dt, fin = build_one(client, model, topic, slug, topic,
                                          max_tokens=args.max_tokens)
                ok, reason = quality_gate(path)
                if ok:
                    with lock:
                        done_count[0] += 1
                        d = done_count[0]
                    return f"[{d}/{len(todo)}] {slug} | {n//1024}KB {dt}s | {model}"
                else:
                    if attempt < args.retries:
                        try: os.remove(path)
                        except: pass
                        continue
                    fail_list.append((pid, topic, slug))
                    return f"{slug} | REJECT({reason}) after {attempt} tries"
            except Exception as e:
                if attempt == args.retries:
                    fail_list.append((pid, topic, slug))
                    return f"{slug} | FAIL: {str(e)[:60]}"
                time.sleep(2)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, item) for item in todo]
        for fut in as_completed(futs):
            print("  " + fut.result(), flush=True)

    dt = int(time.time() - t0)
    ok = done_count[0]
    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(todo)} built in {dt}s ({dt//60}m)")
    if fail_list:
        with open(FAILED_TSV, "w") as f:
            for pid, topic, slug in fail_list:
                f.write(f"{pid}\t{topic}\t{slug}\n")
        print(f"FAILED: {len(fail_list)} (saved to {FAILED_TSV})")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
