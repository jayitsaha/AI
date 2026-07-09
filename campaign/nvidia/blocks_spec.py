"""
Convert a compact JSON block spec (what the NVIDIA model emits) into real Notion
blocks using the proven notion_template helpers.

Why a JSON spec instead of letting the model call the Notion API? Because the
mechanical/fragile parts (KaTeX escaping, block batching, property setting) then
run in OUR deterministic code, not the LLM's — which is exactly where open models
are least reliable. The model only produces content.

Spec format (a list of block dicts):
  {"t":"h2","text":"..."}   {"t":"h3","text":"..."}
  {"t":"p","text":"...$x_i$..."}                 # $...$ = inline equation
  {"t":"eq","latex":"\\hat\\beta=(X^\\top X)^{-1}X^\\top y"}   # display equation
  {"t":"callout","emoji":"💡","text":"..."}
  {"t":"bullet","text":"..."}   {"t":"num","text":"..."}
  {"t":"code","lang":"python","text":"..."}
  {"t":"table","rows":[["h1","h2"],["a","b"]]}   # first row = header
  {"t":"toggle","title":"Q1: ...","children":[{...}]}
  {"t":"divider"}   {"t":"embed","url":"https://..."}
"""
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from notion_template import (
    rt, eq, heading2, heading3, para, equation_block, callout,
    bullet, numbered, code_block, divider, toggle, table, table_row, embed,
)

_SENT = ""                      # unicode private-use char; never in real text
_INLINE = re.compile(r"\$([^$]+?)\$")  # single-$ inline math


_MD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__|\*(.+?)\*|(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])")


def _fmt_runs(s):
    """Plain text (no math) -> rt() runs honoring **bold** and *italic* markdown."""
    s = s.replace(_SENT, "$")
    out, last = [], 0
    for m in _MD.finditer(s):
        if m.start() > last:
            out.append(rt(s[last:m.start()]))
        b, b2, i, i2 = m.groups()
        if b is not None or b2 is not None:
            out.append(rt(b if b is not None else b2, bold=True))
        else:
            out.append(rt(i if i is not None else i2, italic=True))
        last = m.end()
    if last < len(s):
        out.append(rt(s[last:]))
    return out


def parse_inline(text):
    r"""'a $x^2$ **b**' -> [rt('a '), eq('x^2'), rt(' '), rt('b',bold)]. \$ = literal $."""
    if text is None:
        text = ""
    text = text.replace("\\$", _SENT)  # hide escaped dollars from the splitter
    parts, last = [], 0
    for m in _INLINE.finditer(text):
        if m.start() > last:
            parts += _fmt_runs(text[last:m.start()])
        parts.append(eq(m.group(1).replace(_SENT, "$")))
        last = m.end()
    if last < len(text):
        parts += _fmt_runs(text[last:])
    return parts or [rt("")]


_LANGS = {"python", "javascript", "typescript", "c", "c++", "c#", "java", "go",
          "rust", "ruby", "php", "bash", "shell", "sql", "json", "yaml", "html",
          "css", "markdown", "r", "matlab", "scala", "kotlin", "swift", "julia",
          "latex", "haskell", "lua", "perl", "plain text"}
_LANG_ALIAS = {"py": "python", "python3": "python", "pytorch": "python",
               "numpy": "python", "pandas": "python", "sklearn": "python",
               "tensorflow": "python", "jax": "python", "ipython": "python",
               "js": "javascript", "node": "javascript", "ts": "typescript",
               "sh": "bash", "zsh": "bash", "console": "bash", "shell session": "bash",
               "cpp": "c++", "cxx": "c++", "text": "plain text", "txt": "plain text",
               "": "plain text", "none": "plain text", "pseudocode": "plain text"}


def clean_lang(lang):
    """Map the model's code language to one Notion accepts; default 'python'."""
    l = (lang or "").strip().lower()
    if l in _LANGS:
        return l
    if l in _LANG_ALIAS:
        return _LANG_ALIAS[l]
    return "python"


def clean_emoji(e, default="💡"):
    """Notion callouts require a SINGLE emoji. Open models emit emoji+text or 2 emojis.
    Return the first emoji char (+ optional variation selector), else a safe default."""
    e = (e or "").strip()
    for i, ch in enumerate(e):
        if ord(ch) >= 0x2190:  # arrows/symbols/emoji territory
            nxt = e[i + 1] if i + 1 < len(e) else ""
            return ch + (nxt if nxt == "️" else "")
    return default


def _block(b):
    t = (b.get("t") or "").lower()
    if t in ("h2", "heading2"):
        return heading2(b.get("text", ""))
    if t in ("h3", "heading3"):
        return heading3(b.get("text", ""))
    if t in ("p", "para", "paragraph"):
        return para(*parse_inline(b.get("text", "")))
    if t in ("eq", "equation", "display"):
        return equation_block(b.get("latex") or b.get("text", ""))
    if t == "callout":
        return callout(clean_emoji(b.get("emoji", "💡")), *parse_inline(b.get("text", "")))
    if t in ("bullet", "li"):
        return bullet(*parse_inline(b.get("text", "")))
    if t in ("num", "numbered", "ol"):
        return numbered(*parse_inline(b.get("text", "")))
    if t == "code":
        return code_block(clean_lang(b.get("lang", "python")), b.get("text", ""))
    if t == "divider":
        return divider()
    if t == "embed":
        return embed(b.get("url", ""))
    if t == "table":
        rows = b.get("rows") or []
        if not rows:
            return None
        width = max(len(r) for r in rows)
        rows = [[str(c) for c in r] + [""] * (width - len(r)) for r in rows]
        return table(width, table_row(rows[0]), *[table_row(r) for r in rows[1:]])
    if t == "toggle":
        children = [c for c in (_block(x) for x in b.get("children", [])) if c]
        return toggle(parse_inline(b.get("title", "")), children or [para(rt(""))])
    if b.get("text"):
        return para(*parse_inline(b["text"]))
    return None


def blocks_from_spec(spec):
    out = []
    for b in spec:
        blk = _block(b)
        if blk:
            out.append(blk)
    return out


# ── Line-based DSL (backslash-safe transport for LaTeX-heavy content) ─────────────
# JSON + LaTeX + open models = broken escapes. A line DSL keeps backslashes literal.
#
#   @meta depth=Intermediate priority=Must Know
#   @h2 🎯 The 30-Second Version
#   @p The estimator $\hat\beta$ minimizes the loss.
#   @eq \hat\beta = (X^\top X)^{-1}X^\top y
#   @callout 💡 | If you remember one thing: ...
#   @bullet a point with $x_i$
#   @num a numbered step
#   @code python
#   ...raw code lines...
#   @end
#   @table
#   H1 | H2
#   a | b
#   @end
#   @toggle Q1: what is X?
#   @p the answer, can include $math$
#   @end
#   @divider
#   @embed https://...

_KNOWN = {"meta", "h2", "h3", "p", "eq", "callout", "bullet", "num",
          "code", "table", "toggle", "divider", "embed", "end"}
_SECTION = {"meta", "h2", "h3", "divider", "toggle", "end"}


def _tag_of(line):
    s = line.strip()
    if not s.startswith("@"):
        return None
    return s[1:].split(None, 1)[0].lower() if len(s) > 1 else ""


def parse_dsl(text):
    """Parse the line DSL into (meta_dict, spec_list). Robust to raw LaTeX backslashes,
    to MISSING @end (open models forget it), inline table headers, and markdown."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    lines = text.replace("\r\n", "\n").split("\n")
    meta, spec, i, n = {}, [], 0, len(lines)

    def read_body(j, stop_tags):
        """Read lines until @end (consumed) or a line whose tag is in stop_tags (left)."""
        buf = []
        while j < n:
            s = lines[j].strip()
            if s == "@end":
                return buf, j + 1
            t = _tag_of(lines[j])
            if t is not None and t in stop_tags:
                return buf, j
            buf.append(lines[j])
            j += 1
        return buf, j

    while i < n:
        s = lines[i].strip()
        if not s or not s.startswith("@"):
            i += 1
            continue
        parts = s.split(None, 1)
        tag = parts[0][1:].lower()
        rest = parts[1].rstrip() if len(parts) > 1 else ""
        if tag == "meta":
            md = re.search(r"depth\s*=\s*(Foundational|Intermediate|Advanced|Expert)", rest, re.I)
            mp = re.search(r"priority\s*=\s*(Must Know|Important|Good to Know|Bonus)", rest, re.I)
            if md:
                meta["depth"] = md.group(1).title()
            if mp:
                meta["priority"] = mp.group(1).title().replace("To", "to")
            i += 1
        elif tag in ("h2", "h3", "p", "bullet", "num", "eq", "divider", "embed"):
            b = {"t": tag}
            if tag == "eq":
                b["latex"] = rest
            elif tag == "embed":
                b["url"] = rest
            elif tag != "divider":
                b["text"] = rest
            spec.append(b)
            i += 1
        elif tag == "callout":
            if "|" in rest:
                emoji, _, txt = rest.partition("|")
            else:  # model often forgets the '|': "@callout 💡 text..."
                emoji, _, txt = rest.partition(" ")
            spec.append({"t": "callout", "emoji": emoji.strip() or "💡", "text": txt.strip()})
            i += 1
        elif tag == "code":
            body, i = read_body(i + 1, _KNOWN)  # stop at any known tag if @end missing
            spec.append({"t": "code", "lang": rest.strip() or "python", "text": "\n".join(body)})
        elif tag == "table":
            body, i = read_body(i + 1, _KNOWN)
            rows = []
            if rest:  # header placed on the @table line
                rows.append([c.strip() for c in rest.split("|")])
            rows += [[c.strip() for c in ln.split("|")] for ln in body if ln.strip()]
            if rows:
                spec.append({"t": "table", "rows": rows})
        elif tag == "toggle":
            body, i = read_body(i + 1, _SECTION)  # children are @p etc; stop at section boundary
            _, child_spec = parse_dsl("\n".join(body))
            spec.append({"t": "toggle", "title": rest, "children": child_spec})
        else:
            i += 1
    return meta, spec


def blocks_from_dsl(text):
    meta, spec = parse_dsl(text)
    return meta, blocks_from_spec(spec)
