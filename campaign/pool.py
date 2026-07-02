#!/usr/bin/env python3
"""
Tracks the rolling pool of in-flight builder agents so we can:
  - keep a constant number of agents running (refill on completion),
  - enforce a per-agent time cap (stop + requeue anything too slow).

inflight.json: { agent_id: {slug, page_id, topic, start_epoch} }

Usage:
  pool.py add <agent_id> <page_id> <slug> <topic...>   # register a launched agent
  pool.py done <agent_id> [<agent_id> ...]             # deregister finished agents
  pool.py overdue <minutes>                            # list agents older than N min (agent_id|page_id|slug|topic|age)
  pool.py count                                        # number in flight
  pool.py list                                         # all in flight with ages
"""
import json, os, sys, time

CDIR = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(CDIR, "inflight.json")


def load():
    return json.load(open(F)) if os.path.exists(F) else {}


def save(d):
    json.dump(d, open(F, "w"), indent=2)


def main():
    if len(sys.argv) < 2:
        print("usage: pool.py add|done|overdue|count|list ...")
        return
    cmd = sys.argv[1]
    d = load()
    now = time.time()

    if cmd == "add":
        aid, pid, slug = sys.argv[2], sys.argv[3], sys.argv[4]
        topic = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else slug
        d[aid] = {"slug": slug, "page_id": pid, "topic": topic, "start": now}
        save(d)
        print(f"added {aid} [{slug}] — inflight={len(d)}")
    elif cmd == "done":
        for aid in sys.argv[2:]:
            d.pop(aid, None)
        save(d)
        print(f"inflight={len(d)}")
    elif cmd == "overdue":
        mins = float(sys.argv[2]) if len(sys.argv) > 2 else 16
        for aid, v in d.items():
            age = (now - v["start"]) / 60
            if age >= mins:
                print(f"{aid}|{v['page_id']}|{v['slug']}|{v['topic']}|{age:.1f}")
    elif cmd == "count":
        print(len(d))
    elif cmd == "list":
        for aid, v in d.items():
            print(f"{aid} [{v['slug']}] {(now - v['start'])/60:.1f}min")


if __name__ == "__main__":
    main()
