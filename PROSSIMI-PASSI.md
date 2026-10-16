# Ombrello: stato e prossimi passi

Aggiornato il 16 ottobre 2026, ore 22:40 (ora italiana).

## Stato

Primo giro di raccolta concluso: 2.831 proposte, 214 fonti, 14 partiti, 26 aree coperte.
Il testo integrale delle fonti è in `corpus/`, le proposte in `dati/proposte/<partito>.jsonl`, le fonti in `dati/fonti/`, il censimento in `dati/censimento/`.
Regole e schema: `metodo/codebook.md`, `metodo/aree.json`, `metodo/schema-dati.md`.
Strumenti: `strumenti/scarica.py` (scarica e salva il testo di una fonte) e `strumenti/aggiungi.py` (valida e aggiunge fonti e proposte; rifiuta le citazioni non presenti nella fonte). Python sempre con `-I`.

Proposte per partito: Lega 816, PD 250, FdI 250, AVS (ev+si) 250, Azione 250, Futuro Nazionale 250, M5S 249, +Europa 162, Noi Moderati 125, Forza Italia 123, SVP 42, Italia Viva 38, UDC 16, MAIE 10.
Senza proposte: Sud chiama Nord, PATT, Campobase, autonomisti valdostani (censimento fatto).
Non sono partiti autonomi (nessuna proposta): Popolari Europeisti Riformatori, Centro Popolare, Civici d'Italia, Coraggio Italia, Italia al Centro.

## Decisioni dell'utente

- Piano Pro con crediti limitati: lavorare un passo per volta, un agente alla volta quando possibile, salvare su GitHub dopo ogni passo.
- Il repository è pubblico (grispex/ombrello). Sito da pubblicare in futuro.
- Orari sempre in ora italiana (UTC+2), mai in UTC.
- Mappa 3D da aggiungere in un secondo momento, calcolata dai dati (affinità tra partiti).
- Non serve la completezza assoluta adesso: prima far funzionare tutto, poi completare la ricerca.

## Prossimo passo

1. **Pilota questioni su 3 aree: Lavoro, Fisco, Energia.** Un agente per area (Opus consigliato, sono pochi agenti): legge le proposte dell'area in `dati/proposte/*.jsonl`, le raggruppa in questioni (domande sì/no neutre), assegna a ogni partito una posizione (favorevole / favorevole con riserve / contrario / ambiguo / non espresso) collegata alle proposte-prova, segna touchpoint (grado, tipo) e fratture. Output in `dati/questioni/<area>.json`, formato in `metodo/schema-dati.md`. Un controllo separato verifica a campione.
2. **Prototipo del visualizzatore** sui dati del pilota: libreria A-Z, tabella questioni x partiti, confronto tra partiti. Pagina web statica in `sito/`.
3. Se il pilota convince: le altre 23 aree, poi la mappa 3D, poi la pubblicazione.
4. In seguito: completare la ricerca (partiti senza proposte, Forza Italia, Italia Viva, voti parlamentari, più proposte di legge).
