import json, glob, os, re, sys, collections
d = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/r/res")
rows = []
for p in sorted(glob.glob(d + "/*/result.json")):
    r = json.load(open(p)); t = "\n".join(r["tail"])
    m = re.search(r'"code": "([A-Z_]+)"', t)
    msg = re.search(r'"message": "([^"]{0,110})', t)
    rows.append((" ".join(r["ids"]), r["status"], m.group(1) if m else "-", msg.group(1) if msg else ""))
for i, s, c, msg in rows:
    print(f"{i[:30]:31} {s:8} {c}")
    if s != "ok" and msg: print("     ", msg)
print(dict(collections.Counter(s if s == "ok" else c for _, s, c, _ in rows)))
