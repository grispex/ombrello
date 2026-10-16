"""Scarica una fonte e ne salva il testo integrale nel corpus.

Uso:
  python3 -I strumenti/scarica.py <partito> <id-fonte> <url>

Salva l'originale in corpus/<partito>/raw/ e il testo in corpus/<partito>/<id-fonte>.txt.
Se il sito blocca lo scaricamento, riprova con la copia dell'Internet Archive.
"""
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def scarica(url, dest):
    r = subprocess.run(
        ["curl", "-sSL", "-m", "120", "-A", UA, "-o", dest, "-w", "%{http_code} %{content_type}", url],
        capture_output=True, text=True,
    )
    out = r.stdout.strip().split(" ", 1)
    code = out[0] if out else "000"
    ctype = out[1] if len(out) > 1 else ""
    return code, ctype, r.stderr.strip()


def testo_html(path):
    raw = open(path, "rb").read()
    try:
        import trafilatura
        t = trafilatura.extract(raw, include_tables=True, include_comments=False, favor_recall=True)
        if t and len(t) > 200:
            return t
    except Exception:
        pass
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    return soup.get_text("\n")


def testo_pdf(path):
    r = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], capture_output=True, text=True)
    return r.stdout


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    partito, fid, url = sys.argv[1:]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", partito) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fid):
        print("ERRORE: partito e id-fonte devono essere minuscoli, cifre e trattini")
        sys.exit(2)
    rawdir = os.path.join(BASE, "corpus", partito, "raw")
    os.makedirs(rawdir, exist_ok=True)
    dest = os.path.join(rawdir, fid + ".bin")

    tentativi = [url]
    if "web.archive.org" not in url:
        tentativi.append("https://web.archive.org/web/2026id_/" + url)
    code, ctype, err = "000", "", ""
    usato = None
    for u in tentativi:
        code, ctype, err = scarica(u, dest)
        if code.startswith("2") and os.path.getsize(dest) > 500:
            usato = u
            break
    if not usato:
        print(f"ERRORE: scaricamento fallito (HTTP {code}) {err}")
        sys.exit(1)

    head = open(dest, "rb").read(5)
    if head.startswith(b"%PDF") or "pdf" in ctype:
        os.rename(dest, dest[:-4] + ".pdf")
        dest = dest[:-4] + ".pdf"
        testo = testo_pdf(dest)
    else:
        os.rename(dest, dest[:-4] + ".html")
        dest = dest[:-4] + ".html"
        testo = testo_html(dest)

    testo = (testo or "").replace("\r", "")
    txt = os.path.join(BASE, "corpus", partito, fid + ".txt")
    with open(txt, "w", encoding="utf-8") as f:
        f.write(f"URL: {usato}\n\n")
        f.write(testo)
    print(f"OK {len(testo)} caratteri -> corpus/{partito}/{fid}.txt (da {usato})")
    if len(testo) < 500:
        print("ATTENZIONE: testo molto corto, la pagina potrebbe essere vuota o caricata via JavaScript")
    print("--- inizio ---")
    print(testo[:600])


if __name__ == "__main__":
    main()
