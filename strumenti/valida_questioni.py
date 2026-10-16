"""Controlla un file dati/questioni/<area>.json.

Uso: python3 -I strumenti/valida_questioni.py <area>
Verifica formato, valori ammessi, che ogni prova esista e appartenga a quel partito,
che ogni partito abbia almeno una prova e che nessuna proposta sia usata in due questioni.
"""
import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POS = {"favorevole", "favorevole con riserve", "contrario", "ambiguo"}
GRADI = {"pieno", "parziale", "nominale", None}


def main():
    area = sys.argv[1]
    prop = {}
    for f in glob.glob(os.path.join(BASE, "dati", "proposte", "*.jsonl")):
        for l in open(f, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                prop[r["id"]] = r
    d = json.load(open(os.path.join(BASE, "dati", "questioni", area + ".json"), encoding="utf-8"))
    err, usate, ids = [], {}, set()
    if d.get("area") != area:
        err.append("campo 'area' errato")
    for q in d.get("questioni", []):
        qid = q.get("id", "?")
        if not re.fullmatch(r"q-[a-z0-9-]+", qid or ""):
            err.append(f"{qid}: id non valido")
        if qid in ids:
            err.append(f"{qid}: id duplicato")
        ids.add(qid)
        if not (q.get("domanda") or "").endswith("?"):
            err.append(f"{qid}: la domanda deve finire con '?'")
        if (q.get("touchpoint") or {}).get("grado") not in GRADI:
            err.append(f"{qid}: grado non valido")
        visti = set()
        for p in q.get("posizioni", []):
            pt = p.get("partito")
            if pt in visti:
                err.append(f"{qid}: partito {pt} ripetuto")
            visti.add(pt)
            if p.get("posizione") not in POS:
                err.append(f"{qid}/{pt}: posizione non valida '{p.get('posizione')}'")
            if not p.get("prove"):
                err.append(f"{qid}/{pt}: nessuna prova")
            for pr in p.get("prove", []):
                if pr not in prop:
                    err.append(f"{qid}/{pt}: prova inesistente {pr}")
                    continue
                if pt not in prop[pr]["partiti"]:
                    err.append(f"{qid}/{pt}: la prova {pr} non è di {pt}")
                if area not in prop[pr]["aree"]:
                    err.append(f"{qid}/{pt}: la prova {pr} non è nell'area {area}")
                if pr in usate and usate[pr] != qid:
                    err.append(f"{qid}: la proposta {pr} è già usata in {usate[pr]}")
                usate[pr] = qid
    nq = len(d.get("questioni", []))
    tot = sum(1 for r in prop.values() if area in r["aree"])
    print(f"{area}: {nq} questioni, {len(usate)} proposte collegate su {tot}, errori: {len(err)}")
    for e in err[:60]:
        print("  ", e)
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
