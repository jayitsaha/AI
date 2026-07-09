"""
Notion page updater template for the AI/ML Knowledge Pipeline.

Usage from a topic script:

    from notion_template import *

    PAGE_ID = "..."   # from topic_page_ids.json
    PROPERTIES = {    # page properties to set
        "Status": {"select": {"name": "Completed"}},
        "Interview Priority": {"select": {"name": "Important"}},
        "Has Explainer": {"checkbox": True},
        "Explainer URL": {"url": "https://jayitsaha.github.io/..."},
    }
    ICON = "🟢"  # depth icon

    blocks = [
        heading2("🎯 The 30-Second Version"),
        para(rt("Explanation..."), eq("x^2 + y^2 = r^2"), rt(" is the circle equation.")),
        equation_block(r"\\hat{\\beta} = (X^T \\Omega^{-1} X)^{-1} X^T \\Omega^{-1} y"),
        ...
    ]

    update_page(PAGE_ID, ICON, PROPERTIES, blocks)
"""

import json
import os
import urllib.request
import urllib.error
import time
import ssl

# ── SSL Fix (macOS Python) ─────────────────────────────────────────────────────
_ssl_ctx = ssl.create_default_context()
try:
    import certifi
    _ssl_ctx.load_verify_locations(certifi.where())
except ImportError:
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE

# ── Config ──────────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("NOTION_API_TOKEN", "")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "33c93418-809c-81f7-a93d-df0ac011aa09")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


# ══════════════════════════════════════════════════════════════════════════════
#  API LAYER
# ══════════════════════════════════════════════════════════════════════════════

def api(method, url, payload=None, retries=5):
    """Make a Notion API request with retries and exponential backoff."""
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After", 2)))
            elif e.code == 404 and method == "DELETE":
                return None
            else:
                print(f"  HTTP {e.code}: {body[:300]}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
        except Exception as ex:
            print(f"  Error: {ex}")
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


# ══════════════════════════════════════════════════════════════════════════════
#  RICH TEXT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def rt(content, bold=False, italic=False, code=False, color="default", link=None):
    """Plain text rich_text element."""
    t = {"type": "text", "text": {"content": content}}
    if link:
        t["text"]["link"] = {"url": link}
    ann = {}
    if bold:
        ann["bold"] = True
    if italic:
        ann["italic"] = True
    if code:
        ann["code"] = True
    if color != "default":
        ann["color"] = color
    if ann:
        t["annotations"] = ann
    return t


def eq(expression):
    """Inline equation rich_text element (KaTeX).

    Use inside para(), callout(), bullet() etc. alongside rt() elements:
        para(rt("The formula is "), eq(r"E = mc^2"), rt("."))
    """
    return {"type": "equation", "equation": {"expression": expression}}


# ══════════════════════════════════════════════════════════════════════════════
#  BLOCK HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def heading2(text):
    """Heading 2 block."""
    return {"type": "heading_2", "heading_2": {"rich_text": [rt(text)]}}


def heading3(text):
    """Heading 3 block."""
    return {"type": "heading_3", "heading_3": {"rich_text": [rt(text)]}}


def para(*texts):
    """Paragraph block. Pass rt() and eq() elements."""
    return {"type": "paragraph", "paragraph": {"rich_text": list(texts)}}


def equation_block(expression):
    """Standalone equation block (centered, display math). Uses KaTeX.

    Example:
        equation_block(r"\\hat{\\beta}_{GLS} = (X^\\top \\Omega^{-1} X)^{-1} X^\\top \\Omega^{-1} y")
    """
    return {"type": "equation", "equation": {"expression": expression}}


def callout(emoji, *texts):
    """Callout block with emoji icon."""
    return {
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "rich_text": list(texts),
        },
    }


def bullet(*texts):
    """Bulleted list item."""
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": list(texts)}}


def numbered(*texts):
    """Numbered list item."""
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": list(texts)}}


def code_block(language, content):
    """Code block. Auto-splits content into 2000-char segments (Notion limit)."""
    segments = []
    while content:
        segments.append(rt(content[:2000]))
        content = content[2000:]
    return {"type": "code", "code": {"language": language, "rich_text": segments}}


def divider():
    """Horizontal divider."""
    return {"type": "divider", "divider": {}}


def toggle(title_texts, children):
    """Toggle block with nested children.

    title_texts: list of rt()/eq() elements, or a plain string.
    children: list of blocks inside the toggle.
    """
    if isinstance(title_texts, str):
        title_texts = [rt(title_texts)]
    return {"type": "toggle", "toggle": {"rich_text": title_texts, "children": children}}


def table_row(cells):
    """Table row. cells = list of strings (for simple text) or list of rich_text lists."""
    row_cells = []
    for c in cells:
        if isinstance(c, str):
            row_cells.append([rt(c)])
        elif isinstance(c, list):
            row_cells.append(c)
        else:
            row_cells.append([c])
    return {"type": "table_row", "table_row": {"cells": row_cells}}


def table(width, header_row, *data_rows):
    """Table block. Pass table_row() elements. First row is header."""
    return {
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": [header_row] + list(data_rows),
        },
    }


def embed(url):
    """Embed block (for explainer iframes)."""
    return {"type": "embed", "embed": {"url": url}}


def bookmark(url):
    """Bookmark block."""
    return {"type": "bookmark", "bookmark": {"url": url}}


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

def clear_page(page_id):
    """Delete all existing blocks from a page (to avoid duplicates on re-run)."""
    print("Clearing existing page content...")
    all_blocks = []
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"

    # Paginate through all blocks
    while url:
        result = api("GET", url, None)
        if result and result.get("results"):
            all_blocks.extend(result["results"])
        if result and result.get("has_more"):
            url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100&start_cursor={result['next_cursor']}"
        else:
            url = None

    if all_blocks:
        for block in all_blocks:
            try:
                api("DELETE", f"https://api.notion.com/v1/blocks/{block['id']}", None)
                time.sleep(0.12)
            except Exception:
                pass
        print(f"  Cleared {len(all_blocks)} blocks.")
    else:
        print("  No existing blocks to clear.")


def send_blocks(page_id, blocks, batch_size=95):
    """Append blocks to a page in batches (Notion 100-block limit)."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    total = len(blocks)
    print(f"Sending {total} blocks...")

    for i in range(0, total, batch_size):
        chunk = blocks[i : i + batch_size]
        batch_num = i // batch_size + 1
        print(f"  Batch {batch_num} ({len(chunk)} blocks)...", end=" ", flush=True)
        try:
            api("PATCH", url, {"children": chunk})
            print("OK")
        except Exception as e:
            print(f"FAILED: {e}")
        time.sleep(0.4)


def update_page(page_id, icon, properties, blocks):
    """Full page update: set properties, clear old content, add new blocks.

    Args:
        page_id: Notion page UUID
        icon: emoji string (e.g. "🟢")
        properties: dict of Notion property updates
        blocks: list of block dicts (from heading2, para, equation_block, etc.)
    """
    # 1. Update properties
    print(f"Updating page {page_id}...")
    api("PATCH", f"https://api.notion.com/v1/pages/{page_id}", {
        "icon": {"type": "emoji", "emoji": icon},
        "properties": properties,
    })
    print("  Properties updated.")
    time.sleep(0.3)

    # 2. Clear existing content
    clear_page(page_id)
    time.sleep(0.3)

    # 3. Add new blocks
    send_blocks(page_id, blocks)

    print(f"\nDone! https://www.notion.so/{page_id.replace('-', '')}")
