"""Mostra stato iter e link al testo di un AC (XIX leg.) dalla scheda camera.it.
Uso: python3 -I scheda_ac.py <numero> [<cartella_download>]"""
import re
import subprocess
import sys

from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
n = sys.argv[1]
d = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/dl"
out = f"{d}/ac{n}.html"
subprocess.run(["curl", "-sSL", "-m", "60", "-A", UA, "-o", out,
                f"https://www.camera.it/leg19/126?tab=&leg=19&idDocumento={n}&sede=&tipo="], check=False)
s = BeautifulSoup(open(out, "rb").read(), "html.parser")
t = re.sub(r"\n\s*\n+", "\n", s.get_text("\n"))
i = t.find("Proposta di legge")
for kw in ["Stato iter", "Iter", "Assegnato", "Approvat", "Respint", "Ritirat", "In corso"]:
    j = t.find(kw)
    if j >= 0:
        print(kw, "->", t[j:j + 200].replace("\n", " "))
        break
m = re.search(r"Presentat[ao] il ([0-9]+ \w+ [0-9]{4})", t)
if m:
    print("Presentata:", m.group(1))
seen = set()
for a in s.find_all("a", href=True):
    h = a["href"]
    if "testo_pdl" in h and h not in seen and "epub" not in h:
        seen.add(h)
        print(h)
