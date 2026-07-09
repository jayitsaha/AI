"""Groq (OpenAI-compatible) client with multi-key rotation for HTML generation.
Skips restricted/invalid keys automatically. Pure stdlib.
"""
import json, os, ssl, time, urllib.request, urllib.error, itertools

BASE = "https://api.groq.com/openai/v1"
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
            if line.startswith("GROQ_API_KEYS") and "=" in line:
                keys = [k.strip() for k in line.split("=", 1)[1].split(",") if k.strip()]
    if os.environ.get("GROQ_API_KEY"):
        keys.insert(0, os.environ["GROQ_API_KEY"])
    if not keys:
        raise RuntimeError("No GROQ keys (campaign/groq/.env)")
    return keys


class GroqClient:
    def __init__(self, keys=None):
        self.keys = keys or load_keys()
        self._cycle = itertools.cycle(range(len(self.keys)))

    def chat(self, model, messages, temperature=0.5, max_tokens=32768, tries=8,
             timeout=180):
        payload = {"model": model, "messages": messages, "temperature": temperature,
                   "max_tokens": max_tokens, "stream": False}
        data = json.dumps(payload).encode()
        err = None
        for attempt in range(tries):
            ki = next(self._cycle)
            try:
                req = urllib.request.Request(f"{BASE}/chat/completions", data=data,
                    headers={"Authorization": f"Bearer {self.keys[ki]}",
                             "Content-Type": "application/json",
                             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                                           "Chrome/125.0 Safari/537.36"},
                    method="POST")
                with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
                    resp = json.loads(r.read().decode())
                ch = resp["choices"][0]
                return ch["message"].get("content") or "", ch.get("finish_reason", "stop")
            except urllib.error.HTTPError as e:
                body = ""
                try: body = e.read().decode()[:200]
                except Exception: pass
                err = f"HTTP {e.code}: {body}"
                if e.code in (429, 400, 401, 403):
                    time.sleep(1.0)      # skip to next key quickly
                elif e.code >= 500:
                    time.sleep(min(20, 2 ** attempt))
                else:
                    time.sleep(1.0)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                time.sleep(min(15, 2 ** attempt))
        raise RuntimeError(f"groq failed after {tries}: {err}")

    def chat_long(self, model, messages, max_tokens=32768, temperature=0.5,
                  max_rounds=4, stop_marker=None):
        out = ""; convo = list(messages)
        for _ in range(max_rounds):
            text, reason = self.chat(model, convo, temperature=temperature,
                                     max_tokens=max_tokens)
            out += text
            if stop_marker and stop_marker in out:
                break
            if reason != "length":
                break
            convo = convo + [{"role": "assistant", "content": text},
                             {"role": "user", "content": "Continue exactly where you left "
                              "off; output only the continuation, no repetition."}]
        return out


if __name__ == "__main__":
    c = GroqClient()
    print(f"{len(c.keys)} keys")
    t, r = c.chat("qwen/qwen3-32b", [{"role": "user", "content": "Say OK only"}], max_tokens=20)
    print(repr(t[:40]), r)
