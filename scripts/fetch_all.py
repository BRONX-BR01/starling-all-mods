import json, hashlib, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
REPO = "horizon-rust/horizon-mods"
mods = json.loads(pathlib.Path("manifest.json").read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def get(e):
    d = pathlib.Path("files") / e["kind"]; d.mkdir(parents=True, exist_ok=True)
    f = d / e["file"]
    if f.exists() and sha(f) == e["sha256"]:
        return e["id"], "ok (ja baixado)"
    r = subprocess.run(["gh", "release", "download", f'{e["id"]}-{e["version"]}',
                        "-R", REPO, "--pattern", e["file"], "--dir", str(d), "--clobber"],
                       capture_output=True, text=True)
    if r.returncode or not f.exists():
        return e["id"], "FALHOU download: " + r.stderr.strip()[:120]
    if sha(f) != e["sha256"]:
        f.unlink()
        return e["id"], "FALHOU sha256"
    return e["id"], "ok"
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(get, mods))
bad = [r for r in res if r[1].startswith("FALHOU")]
for i, s in bad: print(i, s)
print(len(res) - len(bad), "ok,", len(bad), "falhas")
