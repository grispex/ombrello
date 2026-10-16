#!/bin/sh
# uso: run.sh partito specfile prefix
cd /home/user/ombrello
rm -f lavoro/nuovi-autonomie/$3_*.json
python3 -I lavoro/nuovi-autonomie/mk.py $1 lavoro/nuovi-autonomie/$2 lavoro/nuovi-autonomie/$3 || true
for f in lavoro/nuovi-autonomie/$3_*.json; do python3 -I strumenti/aggiungi.py proposte $1 $f | grep -v "duplicato\|^Proposte aggiunte: 0" ; done
