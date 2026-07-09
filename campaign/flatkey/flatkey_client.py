"""flatkey.ai LLM gateway client (OpenAI-compatible) with round-robin keys + STREAMING.
Streaming is required — the Cloudflare-fronted gateway 524-times-out on long non-stream calls.
"""
import json, os, ssl, time, threading, itertools, urllib.request, urllib.error

BASE = "https://console.flatkey.ai/v1"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
_ctx = ssl.create_default_context()
try:
    import certifi
    _ctx.load_verify_locations(certifi.where())
except Exception:
    _ctx.check_hostname = False
    _ctx.verify_mode = ssl.CERT_NONE


def load_keys(env_path=None):
    env_path = env_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    keys = []
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith("FLATKEY_API_KEYS") and "=" in line:
                keys = [k.strip() for k in line.split("=", 1)[1].split(",") if k.strip()]
    if os.environ.get("FLATKEY_API_KEY"):
        keys.insert(0, os.environ["FLATKEY_API_KEY"])
    if not keys:
        raise RuntimeError("No FLATKEY keys (campaign/flatkey/.env)")
    return keys


class FlatkeyClient:
    def __init__(self, keys=None):
        self.keys = keys or load_keys()
        self._i = 0
        self._lock = threading.Lock()

    def _next_key(self):
        with self._lock:
            k = self.keys[self._i % len(self.keys)]
            self._i += 1
            return k

    def chat(self, model, messages, max_tokens=32000, temperature=0.5, tries=None,
             timeout=600):
        """Streaming chat -> accumulated text. Rotates keys on each attempt."""
        tries = tries or max(6, len(self.keys))
        payload = json.dumps({
            "model": model, "messages": messages, "temperature": temperature,
            "max_tokens": max_tokens, "stream": True,
        }).encode()
        err = None
        for attempt in range(tries):
            k = self._next_key()
            req = urllib.request.Request(f"{BASE}/chat/completions", data=payload,
                headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json",
                         "User-Agent": UA, "Accept": "text/event-stream"}, method="POST")
            try:
                out = []
                with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
                    for raw in r:
                        line = raw.decode("utf-8", "ignore").strip()
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0].get("delta", {})
                            if delta.get("content"):
                                out.append(delta["content"])
                        except Exception:
                            continue
                text = "".join(out)
                if text:
                    return text
                err = "empty stream"
            except urllib.error.HTTPError as e:
                body = ""
                try: body = e.read().decode()[:200]
                except Exception: pass
                err = f"HTTP {e.code}: {body}"
                if e.code in (429, 402, 403):   # rate/credit/blocked -> next key
                    time.sleep(min(10, 2 ** attempt))
                elif e.code >= 500:             # 524 timeout etc -> retry
                    time.sleep(min(15, 2 ** attempt))
                else:
                    time.sleep(2)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                time.sleep(min(15, 2 ** attempt))
        raise RuntimeError(f"flatkey failed after {tries}: {err}")


if __name__ == "__main__":
    c = FlatkeyClient()
    print(f"{len(c.keys)} keys")
    t = c.chat("gemini-2.5-flash", [{"role": "user", "content": "Reply with exactly: OK"}], max_tokens=20)
    print(repr(t[:40]))
