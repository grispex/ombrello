"""Costruisce sito/index.html unendo sito/template.html con i dati del database.

Uso: python3 -I strumenti/costruisci_sito.py
"""
import glob
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Nome breve, sigla e colore di ogni partito (colori scelti per distinguerli, non sono quelli ufficiali).
PARTITI = {
    "fdi": ("Fratelli d'Italia", "FdI", "#1b4f8f", "maggioranza"),
    "lega": ("Lega", "Lega", "#2e8b57", "maggioranza"),
    "fi": ("Forza Italia", "FI", "#4aa3df", "maggioranza"),
    "nm": ("Noi Moderati", "NM", "#8e6bbf", "maggioranza"),
    "udc": ("UDC", "UDC", "#6b7fa8", "maggioranza"),
    "maie": ("MAIE", "MAIE", "#9a8c5a", "maggioranza"),
    "fn": ("Futuro Nazionale", "FN", "#7a3b2e", "da definire"),
    "pd": ("Partito Democratico", "PD", "#d6453d", "opposizione"),
    "m5s": ("Movimento 5 Stelle", "M5S", "#e0a526", "opposizione"),
    "ev": ("Europa Verde", "EV", "#3f9f45", "opposizione"),
    "si": ("Sinistra Italiana", "SI", "#a8325e", "opposizione"),
    "azione": ("Azione", "Az", "#1f8fa8", "opposizione"),
    "iv": ("Italia Viva", "IV", "#c46fb4", "opposizione"),
    "piu-europa": ("+Europa", "+E", "#e07b39", "opposizione"),
    "svp": ("SVP", "SVP", "#5c6b73", "altro"),
}


def main():
    aree = json.load(open(os.path.join(BASE, "metodo", "aree.json"), encoding="utf-8"))["aree"]
    fonti = {}
    for p in glob.glob(os.path.join(BASE, "dati", "fonti", "*.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                fonti[r["id"]] = {"t": r["titolo"], "u": r["url"], "k": r["tipo"], "d": r["data"]}
    prop, usate = [], set()
    conta = {}
    for p in sorted(glob.glob(os.path.join(BASE, "dati", "proposte", "*.jsonl"))):
        for l in open(p, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            usate.add(r["fonte"])
            prop.append([r["id"], r["partiti"], r["sintesi"], r["citazione"], r["fonte"], r["aree"],
                         r["sottotema"], r["concretezza"], r["data"], r["stato"], r.get("punto") or ""])
            for pt in r["partiti"]:
                conta[pt] = conta.get(pt, 0) + 1
    # ordine alfabetico per area, sottotema e sintesi
    nomi = {a["id"]: a["nome"] for a in aree}
    prop.sort(key=lambda x: (nomi[x[5][0]].lower(), x[6].lower(), x[2].lower()))
    prova = json.load(open(os.path.join(BASE, "sito", "questioni-prova.json"), encoding="utf-8"))
    dati = {
        "data": "16 ottobre 2026",
        "aree": [{"id": a["id"], "nome": a["nome"]} for a in aree],
        "partiti": [{"id": k, "nome": v[0], "sigla": v[1], "colore": v[2], "schieramento": v[3], "n": conta.get(k, 0)}
                    for k, v in PARTITI.items()],
        "fonti": {k: v for k, v in fonti.items() if k in usate},
        "proposte": prop,
        "prova": prova,
    }
    tpl = open(os.path.join(BASE, "sito", "template.html"), encoding="utf-8").read()
    out = tpl.replace("/*DATI*/null", json.dumps(dati, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(BASE, "sito", "index.html"), "w", encoding="utf-8").write(out)
    print(f"{len(prop)} proposte, {len(dati['fonti'])} fonti, {len(out)//1024} KB")


if __name__ == "__main__":
    main()
