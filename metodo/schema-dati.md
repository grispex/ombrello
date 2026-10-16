# Ombrello: schema dei dati

Bozza v0.1, 16 ottobre 2026.

Il database è l'unica fonte di verità. Tutte le viste, dalla libreria alla futura mappa 3D, leggono gli stessi file. Gli identificativi sono stabili: una voce non cambia ID tra una versione e l'altra.

Gli esempi qui sotto mostrano solo la forma dei dati: i valori sono illustrativi e non ancora verificati.

## File

| File | Contenuto |
|---|---|
| `dati/partiti.json` | Partiti, seggi, coalizione con data e fonte |
| `dati/fonti/<partito>.jsonl` | Un documento per riga: programmi, atti, voti, dichiarazioni |
| `dati/proposte/<partito>.jsonl` | Una proposta per riga (la libreria) |
| `dati/questioni.json` | Le questioni e le posizioni dei partiti (la mappa) |
| `dati/grafo.json` | Generato: nodi, archi e coordinate per le visualizzazioni |
| `corpus/<partito>/<id-fonte>.txt` | Testo integrale delle fonti, usato per verificare le citazioni |

## Proposta

```json
{
  "id": "pd-0142",
  "partito": "pd",
  "sintesi": "Introdurre un salario minimo legale di 9 euro lordi l'ora",
  "citazione": "…testo esatto dalla fonte…",
  "fonti": [{ "id": "pd-pdl-salario-minimo", "punto": "art. 2" }],
  "data": "AAAA-MM-GG",
  "aree": ["lavoro"],
  "sottotema": "Salario minimo",
  "destinatari": ["lavoratori"],
  "concretezza": 4,
  "parametri": [{ "cosa": "soglia oraria", "valore": "9 €/h lordi" }],
  "copertura": null,
  "stato": "depositata",
  "questione": "q-lavoro-salario-minimo-legale",
  "attuale": true,
  "sostituisce": null,
  "verifica": { "citazione_trovata": true, "controllo_indipendente": false, "revisione_umana": false, "ultima_verifica": "2026-10-16" }
}
```

## Fonte

```json
{
  "id": "pd-pdl-salario-minimo",
  "partiti": ["pd", "m5s", "ev", "si", "azione", "piu-europa"],
  "tipo": "C",
  "titolo": "Proposta di legge sul salario minimo",
  "data": "AAAA-MM-GG",
  "url": "https://…",
  "riferimento": "AC …",
  "firmatari": ["…"],
  "testo_salvato": "corpus/pd/pd-pdl-salario-minimo.txt"
}
```

## Questione e posizioni

```json
{
  "id": "q-lavoro-salario-minimo-legale",
  "domanda": "Introdurre un salario minimo legale?",
  "area": "lavoro",
  "sottotema": "Salario minimo",
  "posizioni": [
    { "partito": "pd", "posizione": "favorevole", "parametri": "9 €/h", "prove": ["pd-0142"] },
    { "partito": "fdi", "posizione": "contrario", "prove": ["…"] }
  ],
  "touchpoint": { "grado": "parziale", "tipo": "trasversale" },
  "frattura": false,
  "maggioranza_possibile": { "camera": 0, "senato": 0, "soglia_camera": 201, "soglia_senato": 104 }
}
```

I seggi e le soglie sono calcolati da `partiti.json` alla data della fotografia.

## Grafo per le visualizzazioni

Generato da uno script a ogni nuova versione: non si modifica a mano. Serve sia alle mappe 2D sia a quella 3D.

```json
{
  "nodi": [
    { "id": "pd", "tipo": "partito" },
    { "id": "lavoro", "tipo": "area" },
    { "id": "q-lavoro-salario-minimo-legale", "tipo": "questione", "area": "lavoro" }
  ],
  "archi": [
    { "da": "pd", "a": "q-lavoro-salario-minimo-legale", "tipo": "posizione", "valore": "favorevole" },
    { "da": "pd", "a": "m5s", "tipo": "affinita", "peso": 0.71, "area": null },
    { "da": "pd", "a": "m5s", "tipo": "affinita", "peso": 0.80, "area": "lavoro" }
  ],
  "coordinate": {
    "affinita-3d": { "pd": [0.12, -0.40, 0.08] }
  }
}
```

- **Affinità** tra due partiti: la quota di questioni su cui hanno la stessa posizione, calcolata solo sulle questioni dove entrambi si sono espressi. Esiste in versione generale e per ogni area.
- **Coordinate**: calcolate dalle affinità, così che i partiti che concordano più spesso stiano più vicini. Nessuna posizione è assegnata a mano.
