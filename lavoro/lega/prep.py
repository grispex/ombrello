"""Espande un file compatto {defaults, items} nel formato di aggiungi.py e lo invia."""
import json, sys, subprocess, os
src = sys.argv[1]
d = json.load(open(src, encoding="utf-8"))
defs = {"partiti": ["lega"], "stato": "annunciata", "ambito": "nazionale"}
defs.update(d.get("defaults", {}))
KEYS = {"s": "sintesi", "c": "citazione", "p": "punto", "a": "aree", "t": "sottotema", "k": "concretezza",
        "d": "destinatari", "par": "parametri", "n": "note", "st": "stato", "amb": "ambito", "att": "attuale",
        "cop": "copertura", "f": "fonte", "pt": "partiti"}
out = []
for it in d["items"]:
    r = dict(defs)
    for k, v in it.items():
        kk = KEYS.get(k, k)
        if kk == "parametri":
            v = [{"cosa": x[0], "valore": x[1]} if isinstance(x, list) else x for x in v]
        if kk == "aree" and isinstance(v, str):
            v = v.split(",")
        if kk == "destinatari" and isinstance(v, str):
            v = v.split(",")
        r[kk] = v
    out.append(r)
dst = src.replace(".json", ".exp.json")
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
base = "/home/user/ombrello"
subprocess.run(["python3", "-I", os.path.join(base, "strumenti/aggiungi.py"), "proposte", "lega", dst], cwd=base)
