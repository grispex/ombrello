# Ombrello: regole di raccolta e codifica

Bozza v0.1, 16 ottobre 2026. Questo documento definisce cosa entra nel database e come viene classificato. Diventerà la pagina pubblica "Metodo" del visualizzatore.

## 1. Perimetro

- **Partiti**: tutti i partiti con almeno un parlamentare in carica alla Camera o al Senato, contati singolarmente anche quando sono stati eletti in liste comuni o fanno parte di federazioni (per esempio Europa Verde e Sinistra Italiana separati, anche se in Parlamento formano AVS). Restano fuori i parlamentari senza partito e i senatori a vita.
- **Livello**: politica nazionale. I programmi e i voti europei del 2024 entrano quando riguardano l'Italia.
- **Periodo**: da settembre 2022 a oggi, con più peso alle fonti 2024–2026. Ogni voce ha una data.
- **Fotografia**: la prima versione è datata 16 ottobre 2026. Ogni aggiornamento successivo è una nuova versione numerata.

## 2. Che cos'è una proposta

Una proposta è **un'azione precisa su un oggetto preciso**, attribuibile a un partito.

- Una frase che contiene più azioni si divide in più proposte.
- Le dichiarazioni di valore senza azione ("crediamo nella famiglia") si registrano solo se su quel tema il partito non dice nient'altro, con concretezza 1.
- La stessa proposta presente in più fonti è una sola voce con più fonti collegate.
- Se la posizione è cambiata nel tempo, si registrano entrambe le versioni con le date, e la più recente è marcata come attuale.
- Ogni voce ha una **citazione testuale** dalla fonte (massimo circa 400 caratteri) e una **sintesi neutra** di una riga.

## 3. Concretezza (da 1 a 4)

| Livello | Nome | Esempio |
|---|---|---|
| 1 | Principio | "Più attenzione alla sanità pubblica" |
| 2 | Obiettivo | "Aumentare la spesa sanitaria" |
| 3 | Misura | "Portare la spesa sanitaria al 7,5% del PIL" |
| 4 | Misura quantificata | La stessa misura, con cifre e almeno uno tra copertura economica e tempi |

## 4. Tipi di fonte, in ordine di peso

| Codice | Tipo | Note |
|---|---|---|
| A | Programma elettorale (politiche 2022, europee 2024) o programma ufficiale | Fonte principale |
| B | Documento ufficiale del partito | Mozioni congressuali, manifesti, piattaforme, pagine "proposte" del sito |
| C | Atto parlamentare | Proposta di legge, emendamento, mozione, ordine del giorno; con numero e firmatari |
| D | Voto parlamentare | Mostra il comportamento reale; serve per l'indicatore di coerenza |
| E | Atto di governo | Solo per i partiti di maggioranza |
| F | Dichiarazione pubblica di un leader o portavoce | Solo se mancano fonti A–C; sempre datata |

Giornali, Openpolis, Pagella Politica e simili servono a **trovare** le fonti primarie, non a sostituirle. Se una voce poggia solo su una fonte secondaria, è segnalata come tale.

**Atti parlamentari.** Entrano come proposte del partito le proposte di legge presentate o rivendicate dal partito (prima firma del capogruppo o del segretario, oppure presentate dal partito come "sua" proposta) e quelle firmate da parlamentari di partiti diversi. Le altre restano collegate come prove, ma non diventano voci della libreria.

## 5. Stato della proposta

`annunciata` → `depositata` → `in discussione` → `approvata` → `attuata`, più `respinta` e `abbandonata`.

## 6. Questioni e posizioni (livello mappa)

Le proposte vengono raggruppate in **questioni**, scritte come domande neutre a cui si può rispondere sì o no ("Introdurre un salario minimo legale?").

Per ogni partito la posizione è una di queste:

- `favorevole`
- `favorevole con riserve`: d'accordo sull'obiettivo, con condizioni o strumenti diversi
- `contrario`
- `ambiguo`: fonti recenti in contraddizione tra loro
- `non espresso`: nessuna fonte trovata. **Non equivale a contrario.**

Ogni posizione è collegata alle proposte o ai voti che la dimostrano.

## 7. Touchpoint e fratture

- **Touchpoint**: una questione su cui almeno due partiti hanno la stessa posizione.
- **Grado**:
  - `pieno`: stessa misura, stessi parametri;
  - `parziale`: stesso obiettivo, strumenti o parametri diversi;
  - `nominale`: stessa etichetta, contenuti diversi.
- **Tipo**: `interno` (partiti della stessa coalizione) o `trasversale` (coalizioni diverse).
- **Frattura**: una questione su cui partiti della stessa coalizione hanno posizioni opposte.
- **Maggioranza possibile**: la somma dei seggi dei partiti favorevoli, alla Camera e al Senato, confrontata con la metà più uno.

L'appartenenza alle coalizioni è un dato con data e fonte, perché cambia nel tempo.

## 8. Neutralità

- Le domande sono formulate senza termini carichi; nella libreria restano le parole dei partiti.
- Per ogni partito si cercano le stesse tipologie di fonte, con lo stesso impegno.
- Nessun giudizio di merito: si registra cosa propone un partito, non se è giusto.
- Si usano nomi e colori, non i loghi ufficiali.
- Esiste un canale pubblico per segnalare errori e un registro delle correzioni.

## 9. Verifica

1. **Controllo automatico**: ogni citazione deve comparire nel testo della fonte salvata.
2. **Controllo indipendente**: un secondo passaggio ricontrolla sintesi, area, concretezza e posizione.
3. **Revisione umana a campione** prima della pubblicazione.
4. Ogni voce riporta la data dell'ultima verifica.
