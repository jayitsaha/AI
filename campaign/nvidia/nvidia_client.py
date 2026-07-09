"""
NVIDIA build (integrate.api.nvidia.com) OpenAI-compatible client.

- Rotates across the API keys in .env (round-robin) to spread rate limits.
- Retries on 429 / 5xx with backoff, failing over to the next key.
- chat(): single completion. chat_long(): auto-continues when the model stops
  on `length` (needed for the ~800-line HTML in one logical generation).
- list_models(): GET /v1/models so you can see exactly what your keys can call.

Pure stdlib (urllib) so there's nothing to pip install.
"""
import json, os, ssl, time, urllib.request, urllib.error, itertools

BASE = "https://integrate.api.nvidia.com/v1"

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
            line = line.strip()
            if line.startswith("NVIDIA_API_KEY") and "=" in line:
                keys.append(line.split("=", 1)[1].strip())
    # also honor a plain env var
    if os.environ.get("NVIDIA_API_KEY"):
        keys.insert(0, os.environ["NVIDIA_API_KEY"])
    if not keys:
        raise RuntimeError("No NVIDIA API keys found (campaign/nvidia/.env)")
    return keys


class NvidiaClient:
    def __init__(self, keys=None):
        self.keys = keys or load_keys()
        self._cycle = itertools.cycle(range(len(self.keys)))

    def _request(self, path, payload=None, method="POST", key_idx=0):
        url = f"{BASE}{path}"
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={
                "Authorization": f"Bearer {self.keys[key_idx]}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=120, context=_ctx) as r:
            return json.loads(r.read().decode())

    def list_models(self):
        # try each key until one works
        last = None
        for i in range(len(self.keys)):
            try:
                return self._request("/models", method="GET", key_idx=i)
            except Exception as e:
                last = e
        raise last

    def chat(self, model, messages, temperature=0.35, max_tokens=8192,
             top_p=0.95, tries=6, extra=None):
        """One completion. Returns (text, finish_reason). Fails over across keys."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if extra:
            payload.update(extra)
        err = None
        for attempt in range(tries):
            key_idx = next(self._cycle)
            try:
                resp = self._request("/chat/completions", payload, key_idx=key_idx)
                choice = resp["choices"][0]
                msg = choice["message"]
                text = msg.get("content") or ""
                # some reasoning models put chain-of-thought in reasoning_content;
                # we only want the final content
                return text, choice.get("finish_reason", "stop")
            except urllib.error.HTTPError as e:
                body = ""
                try:
                    body = e.read().decode()[:300]
                except Exception:
                    pass
                err = f"HTTP {e.code}: {body}"
                if e.code in (401, 403):
                    # bad key — try another, but don't sleep long
                    time.sleep(0.5)
                elif e.code == 429:
                    time.sleep(min(30, 2 * (2 ** attempt)))
                elif e.code >= 500:
                    time.sleep(min(30, 2 ** attempt))
                else:
                    time.sleep(1.5)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                time.sleep(min(20, 2 ** attempt))
        raise RuntimeError(f"chat failed after {tries} tries: {err}")

    def chat_long(self, model, messages, max_tokens=8192, temperature=0.3,
                  max_rounds=6, stop_marker=None):
        """Generate a long output, auto-continuing when finish_reason == 'length'.

        Returns the concatenated text. If stop_marker is given, stops once it
        appears in the accumulated output.
        """
        out = ""
        convo = list(messages)
        for _ in range(max_rounds):
            text, reason = self.chat(model, convo, temperature=temperature,
                                     max_tokens=max_tokens)
            out += text
            if stop_marker and stop_marker in out:
                break
            if reason != "length":
                break
            # ask it to continue verbatim from where it stopped
            convo = convo + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": "Continue exactly where you left off. "
                 "Do not repeat anything already written; output only the continuation."},
            ]
        return out


if __name__ == "__main__":
    import sys
    c = NvidiaClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        data = c.list_models()
        ids = sorted(m["id"] for m in data.get("data", []))
        print(f"{len(ids)} models available:")
        for i in ids:
            print(" ", i)
    else:
        txt, reason = c.chat("meta/llama-3.3-70b-instruct",
                             [{"role": "user", "content": "Reply with exactly: OK"}],
                             max_tokens=16)
        print(repr(txt), reason)
