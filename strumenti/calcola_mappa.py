"""Calcola le coordinate 3D dei partiti per la mappa.

Modalità "testi" (dati veri): ogni partito è un documento fatto delle sintesi delle sue proposte;
la distanza è 1 - somiglianza del coseno sui pesi tf-idf delle parole. Misura quanto si somigliano
temi e parole delle proposte, non quanto i partiti sono d'accordo.
Modalità "prova": distanza = disaccordo medio sulle questioni di prova.
Le coordinate vengono dal multidimensional scaling classico in 3 dimensioni.
"""
import glob
import json
import math
import os
import re
from collections import Counter

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("""
della delle degli dello dell nell nella nelle negli nello dalla dalle dagli dallo dall alla alle agli allo sulla sulle sugli sullo
come anche altri altre altro altra ogni ciascun quali quale quello quella questi queste questo questa essere sono hanno ogni tutte tutti
tutto tutta loro suoi sulla verso senza sotto sopra tra fra più meno molto solo ogni anni anno parte fino fine delle dei del per con che non
cui possibilità prevedere nuovo nuova nuovi nuove nazionale nazionali italia italiano italiana italiani italiane
""".split())
MIN_PROPOSTE_AREA = 4


def parole(testo):
    p = re.findall(r"[a-zàèéìòù]{4,}", testo.lower())
    return [w for w in p[1:] if w not in STOP]  # il primo termine è il verbo all'infinito


def carica():
    prop = []
    propri = {os.path.basename(f)[:-6] for f in glob.glob(os.path.join(BASE, "dati", "proposte", "*.jsonl"))}
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "proposte", "*.jsonl"))):
        for l in open(f, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                r["partiti"] = [x for x in r["partiti"] if x in propri or x == "si"]
                prop.append(r)
    return prop


def tfidf(docs):
    """docs: {id: Counter}. Restituisce matrice normalizzata e vocabolario."""
    ids = list(docs)
    df = Counter()
    for c in docs.values():
        df.update(c.keys())
    n = len(ids)
    voc = [w for w, d in df.items() if (3 <= d < n) or (n <= 3 and d >= 1)]
    idx = {w: i for i, w in enumerate(voc)}
    M = np.zeros((n, len(voc)))
    for r, i in enumerate(ids):
        for w, c in docs[i].items():
            if w in idx:
                M[r, idx[w]] = (1 + math.log(c)) * math.log((1 + n) / (1 + df[w])) + 1e-9
    norm = np.linalg.norm(M, axis=1, keepdims=True)
    norm[norm == 0] = 1
    return ids, M / norm, voc


def mds(D, k=3):
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    w, v = np.linalg.eigh(B)
    o = np.argsort(w)[::-1][:k]
    X = v[:, o] * np.sqrt(np.maximum(w[o], 0))
    if X.shape[1] < k:
        X = np.hstack([X, np.zeros((n, k - X.shape[1]))])
    return X


def allinea(X, ids, rif):
    comuni = [i for i, p in enumerate(ids) if p in rif["pos"]]
    if len(comuni) < 4:
        return X
    A = X[comuni] - X[comuni].mean(0)
    B = np.array([rif["xyz"][rif["pos"][ids[i]]] for i in comuni])
    B = B - B.mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    R = U @ Vt
    return (X - X[comuni].mean(0)) @ R


def scala(X):
    m = np.abs(X).max()
    return X / m if m else X


def scheda(ids, D, X, termini=None):
    return {"p": ids, "xyz": np.round(scala(X), 3).tolist(), "d": np.round(D, 3).tolist(),
            "termini": termini or {}}


def da_testi(prop):
    scope = {}
    per = {"tutte": {}}
    for r in prop:
        w = parole(r["sintesi"])
        for p in r["partiti"]:
            per["tutte"].setdefault(p, Counter()).update(w)
            for a in r["aree"]:
                per.setdefault(a, {}).setdefault(p, Counter()).update(w)
    n_ar = Counter()
    for r in prop:
        for a in r["aree"]:
            for p in r["partiti"]:
                n_ar[(a, p)] += 1
    out, rif = {}, None
    for chiave in ["tutte"] + sorted(k for k in per if k != "tutte"):
        docs = {p: c for p, c in per[chiave].items() if chiave == "tutte" or n_ar[(chiave, p)] >= MIN_PROPOSTE_AREA}
        if len(docs) < 3:
            continue
        ids, M, voc = tfidf(docs)
        S = np.clip(M @ M.T, 0, 1)
        D = np.sqrt(np.maximum(2 * (1 - S), 0))
        X = mds(D)
        if rif is not None:
            X = allinea(X, ids, rif)
        termini = {}
        for r_i, p in enumerate(ids):
            top = np.argsort(M[r_i])[::-1][:6]
            termini[p] = [voc[j] for j in top if M[r_i, j] > 0]
        out[chiave] = scheda(ids, D, X, termini)
        if chiave == "tutte":
            rif = {"pos": {p: i for i, p in enumerate(ids)}, "xyz": X.tolist()}
    return out, rif


def da_prova(rif):
    q = json.load(open(os.path.join(BASE, "sito", "questioni-prova.json"), encoding="utf-8"))["questioni"]
    val = {"S": 1.0, "R": 0.5, "N": 0.0}
    ids = sorted({p for x in q for p in x["pos"]})
    n = len(ids)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            c = [abs(val[x["pos"][ids[i]]] - val[x["pos"][ids[j]]]) for x in q if ids[i] in x["pos"] and ids[j] in x["pos"]]
            D[i, j] = np.mean(c) if c else 0.5
    X = allinea(mds(D), ids, rif)
    return scheda(ids, D, X)


def main():
    prop = carica()
    testi, rif = da_testi(prop)
    out = {"testi": testi, "prova": da_prova(rif)}
    path = os.path.join(BASE, "dati", "mappa.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"scope testi: {len(testi)}, partiti nella mappa generale: {len(testi['tutte']['p'])}, prova: {len(out['prova']['p'])}")
    t = testi["tutte"]
    for i, p in enumerate(t["p"]):
        vic = sorted(((t["d"][i][j], t["p"][j]) for j in range(len(t["p"])) if j != i))[:2]
        print(p, [f"{q}:{d:.2f}" for d, q in vic], t["termini"][p][:4])


if __name__ == "__main__":
    main()
