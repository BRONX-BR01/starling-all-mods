import json, sys, zipfile, hashlib, subprocess, pathlib
REPO = "horizon-rust/horizon-mods"
root = pathlib.Path(__file__).resolve().parents[1]
mods = {m["id"]: m for m in json.loads((root / "manifest.json").read_text())}
def die(msg): print(msg, file=sys.stderr); sys.exit(1)
for mid in sys.argv[1:]:
    m = mods.get(mid) or die(f"{mid}: nao esta no manifest")
    d = pathlib.Path("dl"); d.mkdir(exist_ok=True)
    f = d / m["file"]
    r = subprocess.run(["gh", "release", "download", f'{mid}-{m["version"]}', "-R", REPO,
                        "--pattern", m["file"], "--dir", str(d), "--clobber"],
                       capture_output=True, text=True)
    if r.returncode: die(f"{mid}: download falhou: {r.stderr[:200]}")
    if hashlib.sha256(f.read_bytes()).hexdigest() != m["sha256"]: die(f"{mid}: sha256 diferente")
    z = zipfile.ZipFile(f)
    for n in z.namelist():
        p = pathlib.PurePosixPath(n)
        if p.is_absolute() or ".." in p.parts: die(f"{mid}: caminho suspeito {n}")
    dest = pathlib.Path("native-mods") / mid
    z.extractall(dest)
    found = sorted((dest / "mixins").glob("*/horizon-mixin.toml"))
    if not found: die(f"{mid}: sem horizon-mixin.toml")
    for p in found: print(p.parent.resolve())
