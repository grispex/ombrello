"""Aggiunge fonti e proposte al database, controllandole prima.

Uso:
  python3 -I strumenti/aggiungi.py fonti <partito> <file.json>
  python3 -I strumenti/aggiungi.py proposte <partito> <file.json>
  python3 -I strumenti/aggiungi.py stato <partito>

<file.json> contiene una lista JSON di oggetti. Le voci che non passano i controlli
vengono rifiutate con il motivo; le altre vengono aggiunte in coda ai file .jsonl.
Il controllo principale: ogni citazione deve comparire nel testo salvato della sua fonte.
"""
import glob
import json
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREE = {a["id"] for a in json.load(open(os.path.join(BASE, "metodo", "aree.json"), encoding="utf-8"))["aree"]}
TIPI = {"A", "B", "C", "D", "E", "F"}
STATI = {"annunciata", "depositata", "in discussione", "approvata", "attuata", "respinta", "abbandonata"}
AMBITI = {"nazionale", "europeo"}
DATA_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    for a, b in (("’", "'"), ("‘", "'"), ("`", "'"), ("´", "'"), ("“", '"'), ("”", '"'), ("«", '"'), ("»", '"'), ("–", "-"), ("—", "-")):
        s = s.replace(a, b)
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def citazione_presente(citazione, testo_norm):
    segmenti = [norm(x) for x in re.split(r"\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\(\s*(?:\.\.\.|…)\s*\)|…|\.\.\.)\s*", citazione)]
    segmenti = [x.strip(" .,;:") for x in segmenti if len(x.strip(" .,;:")) >= 12]
    if not segmenti:
        return False
    pos = 0
    for seg in segmenti:
        i = testo_norm.find(seg, pos)
        if i < 0:
            return False
        pos = i + len(seg)
    return True


def leggi_jsonl(path):
    if not os.path.exists(path):
        return []
    righe = []
    with open(path, encoding="utf-8") as f:
        for l in f:
            if l.strip():
                try:
                    righe.append(json.loads(l))
                except json.JSONDecodeError:
                    pass  # riga in scrittura da un altro processo
    return righe


def tutte_le_fonti():
    fonti = {}
    for p in glob.glob(os.path.join(BASE, "dati", "fonti", "*.jsonl")):
        for r in leggi_jsonl(p):
            fonti[r["id"]] = r
    return fonti


def aggiungi_fonti(partito, voci):
    os.makedirs(os.path.join(BASE, "dati", "fonti"), exist_ok=True)
    dest = os.path.join(BASE, "dati", "fonti", partito + ".jsonl")
    esistenti = tutte_le_fonti()
    ok, ko = [], []
    for v in voci:
        errori = []
        for campo in ("id", "partiti", "tipo", "titolo", "data", "url", "testo_salvato"):
            if not v.get(campo):
                errori.append(f"manca '{campo}'")
        if v.get("id") and not ID_RE.match(v["id"]):
            errori.append("id non valido (minuscole, cifre, trattini)")
        if v.get("tipo") and v["tipo"] not in TIPI:
            errori.append("tipo deve essere A-F")
        if v.get("data") and not DATA_RE.match(str(v["data"])):
            errori.append("data deve essere AAAA, AAAA-MM o AAAA-MM-GG")
        if v.get("partiti") and not isinstance(v["partiti"], list):
            errori.append("partiti deve essere una lista")
        if v.get("testo_salvato") and not os.path.exists(os.path.join(BASE, v["testo_salvato"])):
            errori.append(f"testo_salvato non esiste: {v['testo_salvato']}")
        if v.get("id") in esistenti:
            errori.append("id già presente (scegline un altro o riusa la fonte esistente)")
        if errori:
            ko.append((v.get("id"), errori))
        else:
            ok.append(v)
            esistenti[v["id"]] = v
    with open(dest, "a", encoding="utf-8") as f:
        for v in ok:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
    print(f"Fonti aggiunte: {len(ok)}  rifiutate: {len(ko)}")
    for i, e in ko:
        print(f"  RIFIUTATA {i}: {'; '.join(e)}")


def aggiungi_proposte(partito, voci):
    os.makedirs(os.path.join(BASE, "dati", "proposte"), exist_ok=True)
    dest = os.path.join(BASE, "dati", "proposte", partito + ".jsonl")
    fonti = tutte_le_fonti()
    esistenti = leggi_jsonl(dest)
    visti = {(r["fonte"], norm(r["citazione"])) for r in esistenti}
    n = max([int(r["id"].rsplit("-", 1)[1]) for r in esistenti] or [0])
    cache = {}
    ok, ko = [], []
    for idx, v in enumerate(voci):
        errori = []
        for campo in ("partiti", "sintesi", "citazione", "fonte", "aree", "sottotema", "concretezza", "stato", "ambito"):
            if v.get(campo) in (None, "", []):
                errori.append(f"manca '{campo}'")
        if isinstance(v.get("partiti"), list) and partito not in v["partiti"]:
            errori.append(f"'partiti' deve includere '{partito}'")
        aree_bad = [a for a in v.get("aree") or [] if a not in AREE]
        if aree_bad:
            errori.append(f"aree sconosciute: {aree_bad}")
        if v.get("concretezza") not in (1, 2, 3, 4):
            errori.append("concretezza deve essere 1, 2, 3 o 4")
        if v.get("stato") and v["stato"] not in STATI:
            errori.append(f"stato non valido: {v['stato']}")
        if v.get("ambito") and v["ambito"] not in AMBITI:
            errori.append("ambito deve essere 'nazionale' o 'europeo'")
        if len(v.get("citazione") or "") > 700:
            errori.append("citazione troppo lunga (max ~600 caratteri): taglia o usa [...]")
        fonte = fonti.get(v.get("fonte"))
        if v.get("fonte") and not fonte:
            errori.append(f"fonte '{v.get('fonte')}' non registrata: aggiungila prima con 'fonti'")
        if fonte and v.get("citazione"):
            path = os.path.join(BASE, fonte["testo_salvato"])
            if path not in cache:
                cache[path] = norm(open(path, encoding="utf-8").read())
            if not citazione_presente(v["citazione"], cache[path]):
                errori.append("citazione NON trovata nel testo della fonte: copia il testo esatto")
        if fonte and v.get("citazione") and (v["fonte"], norm(v["citazione"])) in visti:
            errori.append("duplicato: stessa citazione e stessa fonte già presenti")
        if errori:
            ko.append((idx, (v.get("sintesi") or "")[:70], errori))
            continue
        n += 1
        r = {
            "id": f"{partito}-{n:04d}",
            "partiti": v["partiti"],
            "sintesi": v["sintesi"].strip(),
            "citazione": v["citazione"].strip(),
            "fonte": v["fonte"],
            "punto": v.get("punto"),
            "data": v.get("data") or fonte.get("data"),
            "aree": v["aree"],
            "sottotema": v["sottotema"],
            "destinatari": v.get("destinatari") or [],
            "concretezza": v["concretezza"],
            "parametri": v.get("parametri") or [],
            "copertura": v.get("copertura"),
            "stato": v["stato"],
            "ambito": v["ambito"],
            "attuale": v.get("attuale", True),
            "note": v.get("note"),
        }
        ok.append(r)
        visti.add((r["fonte"], norm(r["citazione"])))
    with open(dest, "a", encoding="utf-8") as f:
        for r in ok:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Proposte aggiunte: {len(ok)}  rifiutate: {len(ko)}  (totale {partito}: {len(esistenti) + len(ok)})")
    for idx, s, e in ko:
        print(f"  RIFIUTATA #{idx} «{s}»: {'; '.join(e)}")


def stato(partito):
    prop = leggi_jsonl(os.path.join(BASE, "dati", "proposte", partito + ".jsonl"))
    fonti = [f for f in tutte_le_fonti().values() if partito in f.get("partiti", [])]
    print(f"{partito}: {len(prop)} proposte, {len(fonti)} fonti")
    conta = {a: 0 for a in sorted(AREE)}
    for r in prop:
        for a in r["aree"]:
            conta[a] += 1
    for a, c in conta.items():
        print(f"  {a:32s} {c}")
    vuote = [a for a, c in conta.items() if c == 0]
    print(f"Aree senza proposte: {', '.join(vuote) if vuote else 'nessuna'}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd, partito = sys.argv[1], sys.argv[2]
    if not ID_RE.match(partito):
        print("ERRORE: id partito non valido")
        sys.exit(2)
    if cmd == "stato":
        stato(partito)
        return
    voci = json.load(open(sys.argv[3], encoding="utf-8"))
    if isinstance(voci, dict):
        voci = [voci]
    if cmd == "fonti":
        aggiungi_fonti(partito, voci)
    elif cmd == "proposte":
        aggiungi_proposte(partito, voci)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
