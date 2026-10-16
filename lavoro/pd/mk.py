import ast, json, subprocess, sys
AL = {"p22":"pd-programma-politiche-2022","e24":"pd-programma-europee-2024","moz23":"pd-mozione-congressuale-schlein-2023",
"w26":"pd-tre-proposte-welfare-2026","gd26":"pd-giusta-e-democratica-2026","dos26":"pd-dossier-legge-bilancio-2026-alternativa",
"r301":"pd-risoluzione-6-00301-consiglio-ue-ott-2026","r293":"pd-risoluzione-6-00293-scostamento-2026","r294":"pd-risoluzione-6-00294-dpfp-2026"}
import os
src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
items = ast.literal_eval(open(src, encoding="utf-8").read())
res = []
for it in items:
    f, punto, s, c, a, t, k = it[:7]
    ex = it[7] if len(it) > 7 else {}
    fonte = AL.get(f) or (f if f.startswith("pd-") else "pd-" + f)
    isc = fonte.startswith("pd-pdl") or fonte.startswith("pd-risol")
    d = {"partiti": ["pd"], "sintesi": s, "citazione": c, "fonte": fonte, "punto": punto, "aree": a, "sottotema": t,
         "concretezza": k, "stato": "depositata" if isc else "annunciata",
         "ambito": "europeo" if f == "e24" else "nazionale"}
    d.update(ex)
    res.append(d)
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False)
subprocess.run(["python3", "-I", "/home/user/ombrello/strumenti/aggiungi.py", "proposte", "pd", out], cwd="/home/user/ombrello")
