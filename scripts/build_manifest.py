import tomllib, json, pathlib, collections
src = pathlib.Path.home() / "ref/horizon-mods/mods"
out = []
for p in sorted(src.glob("*.toml")):
    d = tomllib.loads(p.read_text())
    vs = d.get("versions") or []
    if not vs:
        continue
    v = max(vs, key=lambda v: v.get("published", ""))
    out.append({"id": d["id"], "kind": d["kind"], "name": d.get("name", d["id"]),
                "version": v["version"], "game": v.get("game"),
                "file": v["file"], "sha256": v["sha256"]})
pathlib.Path("manifest.json").write_text(json.dumps(out, indent=1))
print(len(out), "projetos")
for k, n in collections.Counter(e["kind"] for e in out).most_common():
    print(f"  {k}: {n}")
print("game:", dict(collections.Counter(e["game"] for e in out)))
