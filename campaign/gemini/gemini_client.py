"""Minimal Gemini (generativelanguage API) client — API key as query param.
Used to build HTML explainers as a Sonnet alternative. Pure stdlib.
"""
import json, os, ssl, time, urllib.request, urllib.error

BASE = "https://generativelanguage.googleapis.com/v1beta"
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
            if line.startswith("GEMINI_API_KEYS") and "=" in line:
                keys = [k.strip() for k in line.split("=", 1)[1].split(",") if k.strip()]
            elif line.startswith("GEMINI_API_KEY") and "=" in line and not keys:
                keys = [line.split("=", 1)[1].strip()]
    if os.environ.get("GEMINI_API_KEY"):
        keys.insert(0, os.environ["GEMINI_API_KEY"])
    if not keys:
        raise RuntimeError("No GEMINI keys (campaign/gemini/.env)")
    return keys


# back-compat
def load_key(env_path=None):
    return load_keys(env_path)[0]


class GeminiClient:
    def __init__(self, key=None, keys=None):
        import threading
        self.keys = keys or ([key] if key else load_keys())
        self._i = 0
        self._lock = threading.Lock()

    def _next_key(self):
        with self._lock:
            k = self.keys[self._i % len(self.keys)]
            self._i += 1
            return k

    def generate(self, model, system, user, max_tokens=32768, temperature=0.6,
                 tries=None, timeout=300):
        models = model if isinstance(model, list) else [model]
        tries = tries or 6   # fail fast on 429 (quota is project-pooled; don't burn it on retries)
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature,
                                 "maxOutputTokens": max_tokens},
        }
        data = json.dumps(payload).encode()
        err = None
        for attempt in range(tries):
            # rotate BOTH key and model each attempt — model rotation taps the
            # separate per-model daily quota buckets when one model is exhausted.
            k = self._next_key()
            m = models[attempt % len(models)]
            url = f"{BASE}/models/{m}:generateContent?key={k}"
            try:
                req = urllib.request.Request(url, data=data,
                                             headers={"Content-Type": "application/json"},
                                             method="POST")
                with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
                    resp = json.loads(r.read().decode())
                cand = (resp.get("candidates") or [{}])[0]
                parts = cand.get("content", {}).get("parts", [])
                text = "".join(p.get("text", "") for p in parts)
                finish = cand.get("finishReason", "")
                return text, finish
            except urllib.error.HTTPError as e:
                body = ""
                try: body = e.read().decode()[:300]
                except Exception: pass
                err = f"HTTP {e.code}: {body}"
                if e.code in (429, 400, 401, 403):
                    time.sleep(min(8, 2 ** attempt))    # bad/limited key -> next key
                elif e.code >= 500:
                    time.sleep(min(30, 2 ** attempt))
                else:
                    time.sleep(2)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                time.sleep(min(20, 2 ** attempt))
        raise RuntimeError(f"gemini failed after {tries}: {err}")


if __name__ == "__main__":
    c = GeminiClient()
    t, f = c.generate("gemini-3.1-pro-preview", "You are terse.",
                      "Reply with exactly: OK", max_tokens=32)
    print(repr(t), f)
