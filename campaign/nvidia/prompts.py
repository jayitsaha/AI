"""
Prompts for the NVIDIA harness. Two generations per topic:
  1. NOTION page content  -> strict JSON block spec (blocks_spec.py converts it)
  2. HTML explainer        -> one self-contained file

The full pipeline spec (SKILL.md, ~1200 lines) and gold-standard HTML (~800 lines)
are distilled here ONCE so we don't pay to re-read them per topic. That distillation
is the main cost saving vs the Claude workers.
"""

DESIGN_TOKENS = r""":root{
  --bg:#f9f8f5; --bg2:#f0efe9; --surface:#fff;
  --border:rgba(0,0,0,.12); --border2:rgba(0,0,0,.22);
  --text:#1a1a18; --text2:#6b6b65; --text3:#9c9a92;
  --mono:'JetBrains Mono','Fira Code',monospace; --sans:'DM Sans',system-ui,sans-serif;
  --blue-bg:#E6F1FB;--blue-border:#85B7EB;--blue-text:#042C53;--blue-mid:#185FA5;
  --green-bg:#EAF3DE;--green-border:#97C459;--green-text:#173404;--green-mid:#3B6D11;
  --amber-bg:#FAEEDA;--amber-border:#EF9F27;--amber-text:#412402;--amber-mid:#854F0B;
  --red-bg:#FCEBEB;--red-border:#F09595;--red-text:#501313;--red-mid:#A32D2D;
  --purple-bg:#EEEDFE;--purple-border:#AFA9EC;--purple-text:#26215C;--purple-mid:#534AB7;
  --cyan-bg:#E0F7FA;--cyan-border:#4DD0E1;--cyan-text:#006064;--cyan-mid:#00ACC1;
  --radius:10px;--radius-lg:14px;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#18181a;--bg2:#222224;--surface:#2a2a2d;
  --border:rgba(255,255,255,.1);--border2:rgba(255,255,255,.2);
  --text:#e8e6de;--text2:#9c9a92;--text3:#666460;
  --blue-bg:#0c2a45;--blue-border:#378ADD;--blue-text:#B5D4F4;--blue-mid:#85B7EB;
  --green-bg:#172a0a;--green-border:#639922;--green-text:#C0DD97;--green-mid:#97C459;
  --amber-bg:#2e1c05;--amber-border:#BA7517;--amber-text:#FAC775;--amber-mid:#EF9F27;
  --red-bg:#3a0a0a;--red-border:#E24B4A;--red-text:#F7C1C1;--red-mid:#A32D2D;
  --purple-bg:#1e1a45;--purple-border:#7F77DD;--purple-text:#CECBF6;--purple-mid:#AFA9EC;
  --cyan-bg:#004D54;--cyan-border:#26C6DA;--cyan-text:#B2EBF2;--cyan-mid:#4DD0E1;
}}"""

# ── NOTION PAGE ─────────────────────────────────────────────────────────────────

SYSTEM_NOTION = """You are a PhD-level AI/ML educator writing an authoritative Notion knowledge-vault page for one topic. You output ONLY the line-based markup described — no prose, no JSON, no markdown fences, no commentary before or after."""

NOTION_SCHEMA = r"""
OUTPUT FORMAT — a line-based markup (NOT JSON). One block per line, tag at line start.
Because this is NOT JSON, write LaTeX with NORMAL single backslashes (e.g. \hat, \frac, \top). Do NOT double them.

Tags:
  @meta depth=<Foundational|Intermediate|Advanced|Expert> priority=<Must Know|Important|Good to Know|Bonus>
  @h2 <section heading — use the 10 titles below verbatim, incl. emoji>
  @h3 <sub-heading>
  @p <paragraph; wrap INLINE math in single $...$, e.g. the loss $\mathcal{L}=\|y-X\beta\|^2$>
  @eq <a standalone DISPLAY equation in raw LaTeX, NO surrounding $, e.g. \hat\beta = (X^\top X)^{-1}X^\top y>
  @callout <emoji> | <text>
  @bullet <text>
  @num <text>
  @code <language>
  ...raw code lines (real newlines, backslashes literal)...
  @end
  @table
  Header1 | Header2 | Header3
  cell | cell | cell
  @end
  @toggle <question text>
  @p <answer paragraph, may contain $math$>
  @end
  @divider
  @embed <EXPLAINER_URL>

MATH RULES:
- Inline math: $...$ inside @p/@bullet/@callout text. Display math: an @eq line (no $).
- Use \top (transpose), \hat, \frac, \sum_{i=1}^n, \mathbb{E}, \partial, Greek (\alpha,\beta,\Omega). Single backslashes.
- NEVER write math as plain text and NEVER put math inside @code.

THE 10 MANDATORY SECTIONS (each an @h2, in order, exact titles) — from the AI-pipeline spec.
Every listed element is REQUIRED, not optional:
1. 🎯 The 30-Second Version  — layman what-is-this, an everyday analogy, a one-line summary, and a 💡 "if you remember one thing" @callout.
2. 📜 Why This Exists — Historical Context  — the problem it solves, what came before, the breakthrough + key paper(s) (title/authors/year/venue), and a before/after @table (≥3 dimensions).
3. 🧩 Core Concepts & Theory  — precise definitions (with $inline$ math), the defining property/invariant, a 🔑 blue key-concept @callout, and a prerequisites list.
4. 🏗️ Architecture & Internal Workings  — the PhD deep-dive. For EACH sub-component give WHAT / HOW / WHY. REQUIRED: a NUMERICAL TRACE — walk real numbers through every stage as @eq lines or a @table showing intermediate values. Add edge cases + a design-decision @callout.
5. 📐 The Math Behind It  — REQUIRED: at least 6 display @eq lines forming a FULL step-by-step derivation (no skipped steps), each preceded by an @p explaining that step. Include the loss/objective and gradient as @eq. Add a ⚠️ misconception @callout and a proof sketch.
6. 💻 Code Implementation  — a from-scratch @code (NumPy/PyTorch, line comments) AND a production-usage @code (real framework), plus a gotcha @callout.
7. 🎤 Interview Deep-Dive  — 6-8 Q&A as @toggle blocks (title=question, children=@p answers), Easy→Hard, each with a follow-up trap.
8. ⚖️ Comparison & Trade-offs  — a comparison @table vs ALL real alternatives (≥3 dims), when-to-use / when-NOT-to-use, and a 🎯 decision @callout.
9. 🎯 Interactive Visual Explainer  — one @embed <EXPLAINER_URL> then a short italic-intent @p.
10. 🔗 Related Topics & Further Reading  — prerequisites, what-to-learn-next, 3-5 key papers (title/authors/year), best resources.

HARD MINIMUMS (a page that misses these is a failure):
- Section 5 has ≥6 @eq display equations; the page overall has ≥10 @eq lines across sections 3-5.
- Section 4 contains an explicit numerical trace with concrete numbers.
- Every derivation step is shown — never "it can be shown that".

Put an @divider between sections. Depth/correctness like a top graduate textbook + real FAANG interview prep. Aim for 120-170 blocks. Output ONLY the markup."""

def notion_user_prompt(topic, context, url):
    return (f"TOPIC: {topic}\n"
            f"CONTEXT / SCOPE: {context}\n"
            f"EXPLAINER_URL to embed in section 9 and there only: {url}\n\n"
            + NOTION_SCHEMA)


# ── HTML EXPLAINER ──────────────────────────────────────────────────────────────

SYSTEM_HTML = """You are a senior front-end engineer + ML educator. You produce ONE complete, self-contained, production-grade interactive HTML explainer for a single ML topic. Output ONLY raw HTML (starting at <!DOCTYPE html>), no markdown fences, no commentary."""

def html_user_prompt(topic, slug, context):
    return f"""Build a single self-contained HTML file: an interactive visual explainer for "{topic}".
CONTEXT: {context}

HARD REQUIREMENTS:
- Start with <!DOCTYPE html>. Everything inline in ONE file. Only external refs allowed: Google Fonts and the KaTeX CDN.
- In <head> include KaTeX and auto-render:
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\(',right:'\\\\)',display:false}}]}})"></script>
- Use EXACTLY these CSS design tokens (paste this :root verbatim into your <style>, light+dark):
{DESIGN_TOKENS}
- Layout: a header (title, one-line subtitle, small tags for depth/category), then EXACTLY 6 COLLAPSIBLE educational cards
  (1 Understanding · 2 How It Works Internally · 3 The Math / Why It Works · 4 Interactive Walkthrough · 5 Key Takeaways · 6 Code Trace),
  then the interactive visualization, an info card synced to the current step, progress dots, Prev/Next/Reset buttons,
  arrow-key navigation (← →, R to reset), and a legend.
### ⭐ THE INTERACTIVE DIAGRAM IS THE #1 DELIVERABLE — spend most of your effort here.
The animated, interactive visualization is the CENTERPIECE and the single most important part of the
file. A page with weak prose but a brilliant diagram is a success; a page with great prose but a broken
or generic diagram is a FAILURE. Requirements for the diagram:
- It MUST be a real, working, TOPIC-SPECIFIC visualization drawn with <canvas> or <svg> — pick the form
  that genuinely illuminates THIS concept (architecture flow / parameter sliders / distribution curves /
  attention heatmap / matrix ops / trellis / generative steps / pipeline / training dynamics / graph).
  NEVER a generic placeholder or a decorative box.
- Every number shown MUST be COMPUTED LIVE in JS from the actual math (real intermediate values), never
  hard-coded fakes. The visual must visibly CHANGE on each Prev/Next step and on every slider/toggle.
- Each of the ≥8 walkthrough steps must advance the diagram to a new, meaningful state with a clear
  visual transition (highlight, motion, redraw) and a synced explanation of what changed and why.
- Include at least one interactive control (slider / toggle / drag) that recomputes and redraws the
  diagram in real time. Verify mentally that the JS has no undefined references and actually renders.
- Before finishing, re-read your visualization code and make sure it RUNS and DRAWS correctly — this is
  the part that must be flawless. Iterate on it until the diagram is genuinely instructive and bug-free.
- All math rendered via KaTeX: display as $$...$$, inline as \\(...\\). Never Unicode-math or ASCII hacks.
- Must be responsive and work offline-of-your-server (single file). No build step.

HARD MINIMUMS (a thin file is a failure — match the depth of a top interactive textbook):
- The file must be SUBSTANTIAL: at least 550 lines of real content (aim 650-800). Do NOT produce a skeleton.
- At least 8 interactive steps in the walkthrough, each with its own synced explanation in the info card.
- The visualization must use <canvas> or <svg> with real per-step computed values, an animation/transition on step
  change, and at least one interactive control (slider/toggle/drag) that recomputes the numbers live.
- Cards 1-3 and 5 together: 500-1000 words of genuine prose (definitions, mechanism, derivation, intuition).
- Card 3 includes at least 3 KaTeX display equations ($$...$$) forming a real derivation.
- Card 6 shows an annotated from-scratch code snippet in a styled <pre> block.

Output ONLY the HTML."""
