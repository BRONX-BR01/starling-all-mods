import json, os, pathlib, re, shutil, subprocess, sys

name, ids = sys.argv[1], sys.argv[2:]
full = os.environ.get("FULL_APK") == "true"
dropped, status = [], "failed"
pathlib.Path("out").mkdir(exist_ok=True)

def pick(text, ids):
    if not re.search(r'"code": "E_', text):
        return None
    comp = re.search(r"competing injections: ([^\"]+)", text)
    if comp:
        mods = [x.strip().split("/")[0] for x in comp.group(1).split(",")]
        mods = [x for x in mods if x in ids]
        if len(mods) > 1:
            return mods[-1]
    mid = re.search(r'"mod_id": "([^"]+)"', text)
    if mid and mid.group(1) in ids:
        return mid.group(1)
    return None

for _ in range(60):
    shutil.rmtree("native-mods", ignore_errors=True)
    p = subprocess.run(["python3", "tools/scripts/prepare.py", *ids], capture_output=True, text=True)
    if p.returncode:
        status = "prepare_failed"
        pathlib.Path("build.log").write_text(p.stderr)
        break
    env = dict(os.environ)
    if not full:
        env["NATIVE_LIBRARY_ONLY"] = "1"
    with open("build.log", "w") as log:
        b = subprocess.run(["bash", "source/packaging/android/native_build.sh", "source", "out", *p.stdout.split()],
                           stdout=log, stderr=subprocess.STDOUT, env=env)
    if b.returncode == 0:
        status = "ok"
        break
    victim = pick(pathlib.Path("build.log").read_text(errors="replace"), ids)
    if not victim:
        break
    dropped.append(victim)
    ids = [i for i in ids if i != victim]

if status == "ok":
    out = pathlib.Path("out")
    (out / "libhorizon_android.so").rename(out / f"{name}.so")
    (out / "build.json").rename(out / f"{name}.json")
tail = pathlib.Path("build.log").read_text(errors="replace").splitlines()[-40:]
json.dump({"batch": name, "status": status, "ids": ids, "dropped": dropped, "tail": tail},
          open("result.json", "w"), indent=1)
