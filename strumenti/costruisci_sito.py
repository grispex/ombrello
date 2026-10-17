"""Costruisce sito/index.html unendo sito/template.html con i dati del database.

Uso: python3 -I strumenti/costruisci_sito.py
"""
import glob
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ordine di presentazione: maggioranza, fuori dagli schieramenti, opposizione.
PARTITI = {
    "fdi": ("Fratelli d'Italia", "FdI", "maggioranza"),
    "lega": ("Lega", "Lega", "maggioranza"),
    "fi": ("Forza Italia", "FI", "maggioranza"),
    "nm": ("Noi Moderati", "NM", "maggioranza"),
    "udc": ("UDC", "UDC", "maggioranza"),
    "maie": ("MAIE", "MAIE", "maggioranza"),
    "fn": ("Futuro Nazionale", "FN", "altro"),
    "svp": ("SVP", "SVP", "altro"),
    "azione": ("Azione", "Az", "opposizione"),
    "iv": ("Italia Viva", "IV", "opposizione"),
    "piu-europa": ("+Europa", "+E", "opposizione"),
    "pd": ("Partito Democratico", "PD", "opposizione"),
    "m5s": ("Movimento 5 Stelle", "M5S", "opposizione"),
    "ev": ("Europa Verde", "EV", "opposizione"),
    "si": ("Sinistra Italiana", "SI", "opposizione"),
}
COD = {"favorevole": "S", "favorevole con riserve": "R", "contrario": "N", "ambiguo": "A"}


def main():
    aree = json.load(open(os.path.join(BASE, "metodo", "aree.json"), encoding="utf-8"))["aree"]
    fonti = {}
    for p in glob.glob(os.path.join(BASE, "dati", "fonti", "*.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                fonti[r["id"]] = {"t": r["titolo"], "u": r["url"], "k": r["tipo"], "d": r["data"]}
    prop, usate, conta = [], set(), {}
    for p in sorted(glob.glob(os.path.join(BASE, "dati", "proposte", "*.jsonl"))):
        for l in open(p, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            usate.add(r["fonte"])
            prop.append([r["id"], [x for x in r["partiti"] if x in PARTITI], r["sintesi"], r["citazione"], r["fonte"], r["aree"],
                         r["sottotema"], r["concretezza"], r["data"], r["stato"], r.get("punto") or ""])
            for pt in r["partiti"]:
                conta[pt] = conta.get(pt, 0) + 1
    nomi = {a["id"]: a["nome"] for a in aree}
    prop.sort(key=lambda x: (nomi[x[5][0]].lower(), x[6].lower(), x[2].lower()))
    questioni = []
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "questioni", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for q in d["questioni"]:
            tp = q.get("touchpoint") or {}
            questioni.append({
                "id": q["id"], "a": d["area"], "d": q["domanda"], "s": q.get("spiegazione") or "",
                "p": [[x["partito"], COD[x["posizione"]], x.get("parametri"), x["prove"], x.get("nota")] for x in q["posizioni"]],
                "g": tp.get("grado"), "gn": tp.get("nota"), "f": q.get("forza", {}),
            })
    dati = {
        "data": "16 ottobre 2026",
        "aree": [{"id": a["id"], "nome": a["nome"]} for a in aree],
        "partiti": [{"id": k, "nome": v[0], "sigla": v[1], "schieramento": v[2], "n": conta.get(k, 0)} for k, v in PARTITI.items()],
        "fonti": {k: v for k, v in fonti.items() if k in usate},
        "proposte": prop,
        "questioni": questioni,
        "soglie": json.load(open(os.path.join(BASE, "dati", "seggi.json"), encoding="utf-8"))["soglie"],
    }
    tpl = open(os.path.join(BASE, "sito", "template.html"), encoding="utf-8").read()
    out = tpl.replace("/*DATI*/null", json.dumps(dati, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(BASE, "sito", "index.html"), "w", encoding="utf-8").write(out)
    print(f"{len(prop)} proposte, {len(questioni)} questioni, {len(dati['fonti'])} fonti, {len(out)//1024} KB")


if __name__ == "__main__":
    main()
