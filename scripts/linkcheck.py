#!/usr/bin/env python3
"""linkcheck.py: HEAD-check every source_url in researcher JSON files.

Usage: python3 scripts/linkcheck.py research/runs/<run>/researchers/*.json

For each claim: OK (2xx/3xx), MISSING (404/410), or ERROR (anything else).
MISSING and ERROR claims get "link": "<status>" added and their claim text is
appended to the file's "unverified" list, so no skeptic or synthesizer can
treat them as sourced. Writes <run>/linkcheck.json with the full table.
Stdlib only. Local paths (archive files) are checked with os.path.exists.
"""
import json, os, sys, urllib.request, urllib.error, concurrent.futures, datetime

def head(url, timeout=15):
    if not url.startswith("http"):
        return "OK" if os.path.exists(url) else "MISSING"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (linkcheck)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return "OK" if r.status < 400 else f"ERROR:{r.status}"
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return "MISSING"
        if e.code in (403, 405, 429):   # HEAD refused; try GET without body
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (linkcheck)"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return "OK" if r.status < 400 else f"ERROR:{r.status}"
            except urllib.error.HTTPError as e2:
                return "MISSING" if e2.code in (404, 410) else f"ERROR:{e2.code}"
            except Exception as e2:
                return f"ERROR:{type(e2).__name__}"
        return f"ERROR:{e.code}"
    except Exception as e:
        return f"ERROR:{type(e).__name__}"

def main(paths):
    table = []
    for p in paths:
        d = json.load(open(p))
        urls = [(i, c.get("source_url", "")) for i, c in enumerate(d.get("claims", []))]
        with concurrent.futures.ThreadPoolExecutor(8) as ex:
            results = list(ex.map(lambda t: head(t[1]) if t[1] else "MISSING", urls))
        for (i, url), status in zip(urls, results):
            c = d["claims"][i]
            c["link"] = status
            if status != "OK":
                d.setdefault("unverified", []).append(f"[link {status}] {c.get('claim','')[:160]} :: {url}")
            table.append({"file": os.path.basename(p), "claim_index": i + 1, "url": url, "status": status})
        json.dump(d, open(p, "w"), indent=2)
    out = os.path.join(os.path.dirname(os.path.dirname(paths[0])), "linkcheck.json")
    json.dump({"checked_at": datetime.datetime.now().isoformat(timespec="seconds"), "results": table}, open(out, "w"), indent=2)
    bad = [r for r in table if r["status"] != "OK"]
    print(f"{len(table)} sources checked, {len(bad)} not OK -> {out}")
    for r in bad:
        print(f"  {r['file']} #{r['claim_index']} {r['status']} {r['url']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
