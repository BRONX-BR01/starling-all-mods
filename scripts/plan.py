import json, os
mods = json.load(open("manifest.json"))
sel = os.environ.get("MODS", "").replace(",", " ").split()
size = int(os.environ.get("BATCH", "10"))
nat = [m for m in mods if m["kind"] == "native-mod" and (not sel or m["id"] in sel)]
batches = [{"name": f"b{i//size:03d}", "ids": " ".join(m["id"] for m in nat[i:i+size])}
           for i in range(0, len(nat), size)]
open(os.environ["GITHUB_OUTPUT"], "a").write("batches=" + json.dumps(batches) + "\n")
print(len(nat), "mods em", len(batches), "lotes")
