"""Calcola la forza di ogni questione: partiti favorevoli, seggi, schieramenti, maggioranza possibile.

Uso: python3 -I strumenti/calcola_forza.py  (aggiorna i file dati/questioni/*.json aggiungendo il campo "forza")
Un blocco parlamentare conta se almeno uno dei suoi partiti è favorevole (anche con riserve).
"""
import glob
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    S = json.load(open(os.path.join(BASE, "dati", "seggi.json"), encoding="utf-8"))
    blocco_di = {p: b for b in S["blocchi"] for p in b["partiti"]}
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "questioni", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for q in d["questioni"]:
            fav = [p["partito"] for p in q["posizioni"] if p["posizione"] in ("favorevole", "favorevole con riserve")]
            con = [p["partito"] for p in q["posizioni"] if p["posizione"] == "contrario"]
            bf = {blocco_di[p]["id"]: blocco_di[p] for p in fav if p in blocco_di}
            cam = sum(b["camera"] for b in bf.values())
            sen = sum(b["senato"] for b in bf.values())
            sch = sorted({b["schieramento"] for b in bf.values()})
            q["forza"] = {
                "favorevoli": len(fav), "contrari": len(con),
                "seggi_camera": cam, "seggi_senato": sen,
                "maggioranza_camera": cam >= S["soglie"]["camera"], "maggioranza_senato": sen >= S["soglie"]["senato"],
                "schieramenti": sch,
                "trasversale": "maggioranza" in sch and len(sch) > 1,
            }
        json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        top = sorted(d["questioni"], key=lambda q: -q["forza"]["seggi_camera"])[:5]
        print(os.path.basename(f), len(d["questioni"]), "questioni; trasversali:", sum(q["forza"]["trasversale"] for q in d["questioni"]))
        for q in top:
            print("  ", q["forza"]["seggi_camera"], q["forza"]["trasversale"], q["domanda"][:80])


if __name__ == "__main__":
    main()
