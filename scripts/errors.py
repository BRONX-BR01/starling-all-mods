import json, glob, os, re
for p in sorted(glob.glob(os.path.expanduser("~/r/res/*/result.json"))):
    r = json.load(open(p))
    if r["status"] == "ok":
        continue
    d = os.path.dirname(p)
    f = os.path.join(d, "build.log")
    if not os.path.exists(f):
        continue
    log = open(f, errors="replace").read()
    if '"code":' in log:
        continue
    m = re.search(r"^error[^\n]*\n[^\n]*\n", log, re.M)
    print(r["ids"][0], "|", m.group(0).replace("\n", " ")[:150] if m else "?")
