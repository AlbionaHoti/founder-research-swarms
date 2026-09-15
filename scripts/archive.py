#!/usr/bin/env python3
"""archive.py: save fetched pages into knowledge/ so the next run starts local.

Usage: python3 scripts/archive.py <url> [<url> ...]

Each page becomes knowledge/<date>-<slug>.md with frontmatter (url, canonical,
title, fetched, sha256, extractor). The same canonical URL is fetched at most
once per day (tracking parameters stripped first). On a later day, identical
content is not rewritten; changed content becomes a new dated file, so
revisions accumulate. PDFs are saved as extracted text via pdftotext when it is
installed; otherwise the PDF is skipped with a note. Appends to
knowledge/INDEX.md. Stdlib only; HTML is reduced to text by stripping tags.
"""
import sys, re, os, hashlib, datetime, urllib.request, urllib.parse, subprocess, tempfile, html

TRACK = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","fbclid","gclid","dclid","msclkid","mc_cid","mc_eid","_hsenc","_hsmi","mkt_tok","ref","ref_src","igshid","igsh","si","yclid","gbraid","wbraid"}

def canonical(url):
    p = urllib.parse.urlsplit(url.strip())
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if k not in TRACK]
    q.sort()
    path = re.sub(r"/{2,}", "/", p.path).rstrip("/") or "/"
    netloc = p.netloc.lower().replace(":80", "").replace(":443", "")
    return urllib.parse.urlunsplit((p.scheme.lower(), netloc, path, urllib.parse.urlencode(q), ""))

def slug(url, title):
    base = (title or "")[:48] + "-" + urllib.parse.urlsplit(url).netloc + urllib.parse.urlsplit(url).path[:40]
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:90]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (archive)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get("Content-Type", "")

def to_text(data, ctype, url):
    if "pdf" in ctype or url.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(data); path = f.name
        try:
            out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, timeout=120)
            return out.stdout, "pdftotext", ""
        except FileNotFoundError:
            return "", "none", "pdftotext not installed; PDF skipped"
    s = data.decode("utf-8", "replace")
    m = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
    title = html.unescape(m.group(1).strip()) if m else ""
    s = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s); s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip(), "strip-tags", title

def main(urls):
    os.makedirs("knowledge", exist_ok=True)
    index = "knowledge/INDEX.md"
    if not os.path.exists(index):
        open(index, "w").write("# Knowledge index\n\nGrep this folder before searching the web. One file per fetched page.\n\n")
    existing = open(index).read()
    today = datetime.date.today().isoformat()
    for url in urls:
        try:
            data, ctype = fetch(url)
        except Exception as e:
            print(f"FAILED {url}: {e}"); continue
        text, extractor, title_or_note = to_text(data, ctype, url)
        if not text:
            print(f"SKIPPED {url}: {title_or_note}"); continue
        title = title_or_note if extractor == "strip-tags" else os.path.basename(urllib.parse.urlsplit(url).path)
        can = canonical(url)
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        if f" — {can} — fetched {today} — " in existing:
            print(f"ALREADY TODAY {url}"); continue
        if h in existing:
            print(f"UNCHANGED {url}"); continue
        name = f"knowledge/{today}-{slug(url, title)}.md"
        n = 2
        while os.path.exists(name):
            name = f"knowledge/{today}-{slug(url, title)}-{n}.md"; n += 1
        with open(name, "w") as f:
            f.write(f"---\nurl: {url}\ncanonical: {can}\ntitle: {title!r}\nfetched: {today}\nsha256: {h}\nextractor: {extractor}\n---\n\n{text}\n")
        with open(index, "a") as f:
            f.write(f"- [{title or url}]({os.path.basename(name)}) — {can} — fetched {today} — sha256 {h}\n")
        existing += h
        print(f"saved {name} ({len(text)} chars)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
