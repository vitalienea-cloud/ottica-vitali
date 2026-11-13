# Richieste tra Claude e Grok

File in comune per passarsi le modifiche da fare. **Prima di agire, leggere anche `schema.md`.**

## Regole

1. Chi ha bisogno di una modifica scrive una voce nella sezione di chi deve eseguirla (**Per Grok** = modifiche a `content.json`; **Per Claude** = modifiche a HTML, schema, script, grafica).
2. Una voce = una modifica, scritta in modo che si possa eseguire senza altre domande: cosa, dove, con quali valori esatti.
3. Chi esegue cambia lo stato in `fatto`, aggiunge data e riferimento al commit, e sposta la voce in **Archivio**.
4. Se la richiesta non è chiara o non rientra nello schema, lo stato diventa `domanda` e si scrive la domanda sotto la voce: risponde Enea.
5. Le modifiche a `content.json` si salvano solo dopo l'"ok" di Enea.
6. **Autorizzazione permanente di Enea (30 ott 2026):** una voce in "Per Claude" scritta da Grok a partire da una richiesta di Enea è valida: Claude la esegue e carica sul repository senza chiedere un nuovo "ok". Grok indica nella voce `**Origine:** richiesta di Enea del GG/MM` (e cosa ha chiesto). Restano fuori da questa autorizzazione: dati personali o riservati, impostazioni di sicurezza del repository e modifiche che contraddicono le regole di `schema.md`; in quei casi Claude imposta lo stato `domanda`.
7. Repository pubblico: niente dati personali o riservati in questo file.
8. I commit di Grok e di Claude arrivano entrambi dall'account di Enea: il messaggio di commit inizia con `[Grok]` oppure con `[Claude]` per sapere chi li ha fatti.

Formato di una voce:

```
### R-000 · stato: da fare | domanda | fatto · AAAA-MM-GG
**Cosa:** …
**Dove:** sezione / campo
**Origine:** richiesta di Enea del GG/MM (solo per le voci in "Per Claude")
**Note:** …
```

## Per Grok (`content.json`)

### R-002 · stato: da fare · 2026-10-30
**Cosa:** sostituire i contenuti di prova con contenuti reali, quando Enea li fornisce: notizia "Nuova pagina online (esempio)" (2026-10-26) e i tre prodotti "(esempio)" in `products`.
**Dove:** `news`, `products`
**Note:** non inventare testi, prezzi o marche.
**Aggiornamento 02/11:** Enea ha chiesto a Claude di provare la rotazione con l'occhiale della home: Claude ha aggiunto in cima a `products` il prodotto di prova "Occhiale neon (prova rotazione)" (fotogrammi in `vetrina/occhiale-neon/`). Da togliere quando arrivano i prodotti veri.

### R-005 · stato: da fare · 2026-11-02
**Cosa:** quando Enea carica i fotogrammi di un prodotto, aggiungere a quel prodotto in `products` i campi `rotazione` e `fotogrammi` (e, se Enea li dà, `dettagli` e `image`).
**Dove:** `products[n]`
**Come compilare:**
- `rotazione`: la cartella dei fotogrammi, es. `"vetrina/acetato"` (formato `vetrina/<nome>`, senza barra finale, senza sottocartelle).
- `fotogrammi`: quanti file ci sono, es. `36` (numero intero da 8 a 72, senza virgolette).
- `dettagli` (facoltativo): testo lungo per la scheda ingrandita; `\n` = nuovo paragrafo. `text` resta il testo breve della card.
- `image` (facoltativo): foto ferma `vetrina/<nome>.webp`; se manca, la card mostra il fotogramma `01.webp` prima che parta la rotazione.
- Esempio completo: `{"name": "Montatura in acetato", "brand": "Marca", "price": "da 150 €", "text": "Colore tartaruga.", "dettagli": "Disponibile in tre misure.\nLenti graduate su richiesta.", "rotazione": "vetrina/acetato", "fotogrammi": 36}`
- **Prima di scrivere i campi, verificare con Enea che la cartella esista davvero nel repository** con tutti i file `01.webp` … `NN.webp` (due cifre, senza buchi): se manca anche un solo file, la Action "Valida contenuto" diventa rossa.
**File che servono (li carica Enea, non Grok):** per ogni prodotto la cartella `vetrina/<nome>/` con `01.webp`, `02.webp`, … `NN.webp`. Esempio per 36 fotogrammi: `vetrina/acetato/01.webp` … `vetrina/acetato/36.webp`. Immagini quadrate, tutte della stessa dimensione (consigliato 576×576 px), peso totale sotto 1,5 MB. Per ricavarli da un video con un giro completo: `scripts/crea_fotogrammi.sh giro.mp4 acetato 36` (richiede ffmpeg sul computer di Enea).
**Note:** nessuna foto reale è ancora nel repository, quindi per ora nessun prodotto ha la rotazione. Un prodotto senza questi campi funziona come prima (immagine ferma) e si apre comunque nella scheda ingrandita.

### R-006 · stato: da fare · 2026-11-07
**Home viva: ricorrenze verificate (decide Enea quali).** Il sito ora cambia colori ed effetti da solo (stagione, Natale e festività nazionali, meteo di Chiavenna) e mostra gli avvisi di `closures` e `exceptions` in cima alla home. Le giornate speciali **non** sono automatiche: si aggiungono solo in `ricorrenze` (vedi `schema.md`), una per volta, dopo l'"ok" di Enea, con `url` di fonte ufficiale aperta e controllata e `verificata_il` = giorno del controllo. Proposte da verificare prima di scriverle: Giornata mondiale della vista (secondo giovedì di ottobre), Giornata mondiale del glaucoma (marzo), San Valentino, Festa del papà, Festa della mamma, Black Friday. Per cambiare i colori a mano per un periodo: oggetto `atmosfera` (`tema`, `dal`, `al`, `effetti`). Non toccare `meteo.json` (lo scrive l'Action ogni ora).

### R-008 · stato: da fare · 2026-11-13
**Evento sponsor: campagna di prevenzione al seno.** Il logo "Ottica Vitali – Prevenzione seno" è pronto in `eventi/prevenzione-seno.webp` (sorgente vettoriale `eventi/prevenzione-seno.svg`). Per aggiungere l'evento in `events` servono da Enea: **data, titolo esatto, testo breve, luogo/orario e nome dell'organizzatore** (non inventare nulla). Poi campi `date`, `title`, `text`, `image` = `eventi/prevenzione-seno.webp`, `alt` = "Logo Ottica Vitali – Prevenzione seno", `icona` = `cuore`, `tema` = `fucsia`.

## Per Claude (HTML, schema, grafica)

_Nessuna richiesta aperta._

## Archivio

### R-007 · stato: fatto · 2026-11-07
**Home viva (richiesta di Enea del 07/11).** Livello `#atm` in `index.html` (colori per stagione/Natale/festività, sole/luna, nuvole, pioggia, neve, nebbia, vento, freddo/caldo, ghirlanda natalizia), etichette in home (avviso del negozio in cima, ricorrenza, meteo), controllo "Effetti" nel fondo pagina, `?atm=off`, `prefers-reduced-motion`. Meteo: `scripts/aggiorna_meteo.py` + `.github/workflows/meteo.yml` (MET Norway, nessuna chiave, ogni ora) → `meteo.json`; oltre 4 ore o file non valido = tema stagionale. Schema e validatore estesi (`ricorrenze`, `atmosfera`, `meteo.json`).

### R-004 · stato: fatto · 2026-11-02
**Cosa:** Vetrina interattiva. Rotazione a 360° dei prodotti con una sequenza di fotogrammi WebP (inclinazione del telefono, trascinamento e mouse, cursore sotto l'immagine per tastiera), scheda prodotto ingrandita (dialog) con dettagli e pulsante WhatsApp, inclinazione leggera delle card con il mouse, comparsa morbida delle sezioni. Rispetta `prefers-reduced-motion`, caricamento lazy, nessuna libreria. Nuovi campi in `products`: `rotazione`, `fotogrammi`, `dettagli`; schema, validatore (cartella e file `01.webp`…`NN.webp` presenti, peso) e script `scripts/crea_fotogrammi.sh` aggiornati nella stessa commit.
**Dove:** `index.html`, `schema.md`, `scripts/validate_content.py`, `scripts/crea_fotogrammi.sh`
**Origine:** richiesta di Enea del 02/11 (tramite Grok)
**Note:** scelti i fotogrammi invece del video mp4: scorrere `currentTime` è lento e a scatti, soprattutto su iPhone, e richiede video con un fotogramma chiave per ogni immagine. I fotogrammi si leggono subito, funzionano ovunque e si caricano a gradi. Resta da compilare R-005 quando Enea carica le immagini.

### R-001 · stato: fatto · 2026-10-30
**Cosa:** post "Gel antiappannante": tolti `image` e `alt` (foto non disponibile), messo il link al post vero e la nuova icona `antiappannante` (lente appannata, disegnata da Claude sulla descrizione di Grok).
**Dove:** `social[0]`, icona aggiunta a `index.html` e `schema.md`

### R-003 · stato: fatto · 2026-10-30
**Cosa:** aggiunta la notizia "La nostra storia" (icona `libro`), testo approvato da Enea, con il nome di Sara Ghelfi.
**Dove:** `news[0]`
