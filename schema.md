# Schema di `content.json`

Contratto tra chi scrive i contenuti (Grok, che modifica solo `content.json`) e chi scrive il sito (Claude, che modifica l'HTML). Il controllo automatico `scripts/validate_content.py` lo verifica a ogni push.

## Regole di collaborazione

1. **Prima di modificare qualsiasi cosa, leggere questo file.** Vale per entrambi.
2. **Chi cambia la struttura (campi, tipi, sezioni, icone, temi) aggiorna `schema.md` nella stessa commit.** Il controllo fallisce se un campo previsto dal codice non è documentato qui.
3. Grok modifica solo `content.json`; Claude modifica `index.html`, `privacy.html`, `scripts/`, `.github/` e questo file.
4. Se un campo serve e non esiste, **non inventarlo**: si propone la modifica allo schema e si aspetta che il sito la supporti. Un campo sconosciuto è un errore, non viene ignorato.
5. Il repository è pubblico: niente dati personali o riservati.
6. Le richieste di modifica tra Claude e Grok si scrivono in `richieste.md` (voci con stato, eseguite poi spostate in archivio). Prima di agire si legge anche quel file.

## Formato generale

- File UTF-8, JSON valido (virgolette doppie, niente virgole finali, niente commenti, niente chiavi ripetute).
- **Date:** `AAAA-MM-GG`, giorno esistente (es. `2026-11-14`).
- **Link:** devono iniziare con `https://`. Solo nei link delle card è ammesso anche `tel:+39…`.
- **Immagini:** solo file già presenti nel repository in `eventi/` o `vetrina/` (jpg, png, webp). Il file deve esistere. I fotogrammi della rotazione 360° stanno in `vetrina/<nome>/` (vedi `products`).
- **Testi:** testo semplice, niente HTML. `\n` va a capo (nelle card).
- Ogni sezione è facoltativa: se manca o è vuota, il sito mostra un messaggio ("Nessuna notizia…").

## Valori ammessi

**Temi** (`tema`): `blu`, `ambra`, `verde`, `fucsia`, `giallo`. Se manca, il sito sceglie.

**Icone** (`icona`): `pizza`, `festa`, `regalo`, `sole`, `cuore`, `stella`, `caffe`, `natale`, `sconto`, `novita`, `calendario`, `occhio`, `lente`, `orologio`, `pin`, `telefono`, `torta`, `brindisi`, `musica`, `fiore`, `foto`, `trofeo`, `lampadina`, `ombrello`, `gelato`, `chat`, `persone`, `link`, `occhiali`, `occhialisole`, `bambino`, `schermo`, `eclissi`, `scudo`, `auto`, `libro`, `spunta`, `forottero`, `mappa`, `recensione`, `antiappannante`, `assistenza`.
Quando si parla di visite o controlli: `forottero`. Per avvisi e chiusure: `novita`. Per antiappannante o lenti appannate: `antiappannante`. Per storia e libri: `libro`. Per assistenza, riparazioni e saldature: `assistenza` (chiave inglese).

## Sezioni

### `news` — Notizie (lista, ordinate dalla più recente)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `date` | data | sì | data di pubblicazione |
| `title` | testo | sì | |
| `text` | testo | no | riassunto breve |
| `source` | testo | no | es. "ZEISS": appare prima della data |
| `url` | link https | no | mostra "Leggi la fonte" |
| `icona` | icona | no | senza, usa `novita` |
| `tema` | tema | no | |
| `image` | percorso | no | `eventi/…` o `vetrina/…` |
| `alt` | testo | no | descrizione dell'immagine |

```json
{"date": "2026-10-26", "title": "Nuove lenti progressive", "text": "Disponibili da questo mese.", "source": "ZEISS", "url": "https://www.zeiss.it/", "icona": "lente", "tema": "blu"}
```

### `events` — Eventi (lista; quelli passati spariscono da soli)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `date` | data | sì | giorno dell'evento |
| `title` | testo | sì | |
| `text` | testo | no | |
| `icona` | icona | no | |
| `tema` | tema | no | |
| `image` | percorso | no | |
| `alt` | testo | no | |

```json
{"date": "2026-11-14", "title": "Giornata controllo vista", "text": "Controllo gratuito su appuntamento.", "icona": "forottero", "tema": "verde"}
```

### `closures` — Chiusure (lista; le passate spariscono da sole)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `from` | data | sì | primo giorno di chiusura |
| `to` | data | no | ultimo giorno; non prima di `from`. Se manca, un solo giorno |
| `reason` | testo | sì | motivo mostrato al pubblico |
| `icona` | icona | no | |
| `tema` | tema | no | senza, `ambra` |

```json
{"from": "2026-12-24", "to": "2026-12-26", "reason": "Festività natalizie", "icona": "natale"}
```

### `exceptions` — Orari speciali di un giorno (lista)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `date` | data | sì | |
| `text` | testo | sì | es. "Aperti solo la mattina" |
| `icona` | icona | no | |
| `tema` | tema | no | senza, `blu` |

```json
{"date": "2026-10-31", "text": "Chiusura alle 17:00", "icona": "orologio"}
```

Compare nella sezione Chiusure e modifica la riga del giorno nella tabella orari.

### `hours` e `hours_note` — Orari settimanali

`hours` è un oggetto con i giorni in inglese: `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`. Ogni valore è testo; "Chiuso" (o vuoto) indica il giorno di chiusura. `hours_note` è una nota facoltativa sotto la tabella.

```json
"hours": {"monday": "Chiuso", "tuesday": "9:00-12:30, 15:00-19:00", "wednesday": "9:00-12:30, 15:00-19:00", "thursday": "9:00-12:30, 15:00-19:00", "friday": "9:00-12:30, 15:00-19:00", "saturday": "9:00-12:30", "sunday": "Chiuso"},
"hours_note": "Su appuntamento."
```

### `products` — Vetrina (lista)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `name` | testo | sì | |
| `brand` | testo | no | |
| `price` | testo | no | testo libero, es. "da 150 €" |
| `text` | testo | no | breve, compare nella card |
| `dettagli` | testo | no | testo più lungo, compare solo nella scheda ingrandita; `\n` = nuovo paragrafo |
| `image` | percorso | no | foto ferma, `vetrina/…`. Senza rotazione è l'unica immagine; con la rotazione è quella mostrata prima che parta |
| `alt` | testo | no | descrizione dell'immagine |
| `rotazione` | cartella | no | cartella dei fotogrammi, es. `vetrina/rb3025`. Va insieme a `fotogrammi` |
| `fotogrammi` | intero 8–72 | no | quanti fotogrammi ci sono nella cartella. Va insieme a `rotazione` |

```json
{"name": "Montatura in acetato", "brand": "Marca", "price": "da 150 €", "text": "Colore tartaruga.", "dettagli": "Disponibile in tre misure.\nLenti graduate su richiesta.", "image": "vetrina/acetato.webp", "rotazione": "vetrina/acetato", "fotogrammi": 36}
```

**Rotazione a 360°.** Se un prodotto ha `rotazione` e `fotogrammi`, l'immagine ruota: su smartphone inclinando il telefono (su iPhone serve toccare "Attiva rotazione"), su computer trascinando o muovendo il mouse sopra l'immagine, con tastiera o cursore sotto l'immagine. Senza questi campi si vede l'immagine ferma.

I fotogrammi sono immagini già presenti nel repository (Grok non le carica):
- cartella `vetrina/<nome>/` con `<nome>` in minuscolo, senza spazi (lettere, numeri, `-`, `_`);
- file `01.webp`, `02.webp`, … `NN.webp`, **sempre a due cifre, senza buchi**, con `NN` uguale a `fotogrammi`;
- tutti della stessa dimensione e proporzioni (di norma quadrati, consigliato 576×576 px; per oggetti larghi come gli occhiali va bene anche 576×288), WebP, sempre nello stesso senso di rotazione; il peso totale dovrebbe stare sotto 1,5 MB (con 36 fotogrammi, circa 25 KB ciascuno);
- `scripts/crea_fotogrammi.sh` li ricava da un breve video (giro completo dell'oggetto) e scrive i file con i nomi giusti.

Il controllo "Valida contenuto" verifica che la cartella esista e che ci siano tutti i file da `01.webp` a `NN.webp`.

### `social` — Post dei social (lista)

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `title` | testo | sì | |
| `network` | testo | no | "Instagram" o "Facebook" (sceglie l'icona) |
| `date` | data | no | |
| `url` | link https | no | link al post |
| `text` | testo | no | |
| `icona` | icona | no | |
| `tema` | tema | no | |
| `image` | percorso | no | |
| `alt` | testo | no | |

```json
{"title": "Novità in negozio", "network": "Instagram", "date": "2026-10-28", "url": "https://www.instagram.com/p/XXXX/", "text": "Nuovi occhiali da sole.", "icona": "foto"}
```

### `servizi`, `organizzazione`, `contatti` — Card

Tre liste con la stessa struttura. **Se la lista è presente sostituisce tutte le card predefinite: va riscritta per intero.** Se manca o è vuota, il sito usa quelle predefinite.

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `titolo` | testo | sì | scritto nel banner |
| `icona` | icona | no | senza, `novita` |
| `tema` | tema | no | senza, alternanza blu/fucsia/verde |
| `evidenza` | testo | no | riga in evidenza sopra il testo |
| `testo` | testo | no | `\n` = nuovo paragrafo |
| `elenco` | lista | no | elementi `{ "titolo": …, "testo": … }`, entrambi obbligatori |
| `testo_dopo` | testo | no | dopo l'elenco |
| `link_testo` | testo | no | va insieme a `link_url` |
| `link_url` | link | no | `https://…` oppure `tel:+39…` |

```json
{"titolo": "100% green", "icona": "fiore", "testo": "Il nostro impegno:", "elenco": [{"titolo": "Energia rinnovabile:", "testo": "Solo fonti rinnovabili."}], "testo_dopo": "Una scelta quotidiana.", "link_testo": "Scrivici", "link_url": "https://wa.me/393738155967"}
```

### `testi` — Titoli e sottotitoli delle sezioni

Oggetto con chiavi `titolo_<sezione>` e `sub_<sezione>`, valore testo. Sezioni: `notizie`, `eventi`, `vetrina`, `chiusure`, `orari`, `social`, `servizi`, `organizzazione`, `contatti`. Chiavi extra: `cantiere_titolo` e `cantiere_testo` (testo del cartello, vedi `cantiere`). Esempio: `"titolo_eventi": "Prossimi appuntamenti"`. La chiave `hero_sottotitolo` non è più usata.

```json
"testi": {"titolo_notizie": "Novità", "sub_notizie": "Dal negozio e dai nostri fornitori."}
```

### `ricorrenze` — Giornate e ricorrenze verificate (lista)

Compaiono come etichetta sotto il titolo della home nei giorni indicati. **Solo ricorrenze pertinenti all'ottica o alla vista, con fonte ufficiale controllata**: il sito non ne inventa e non ne aggiunge da solo (le festività nazionali e il Natale cambiano solo i colori, senza testo). Se più ricorrenze coincidono vince quella con `from` più recente.

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `from` | data | sì | primo giorno |
| `to` | data | no | ultimo giorno; senza, solo `from` |
| `title` | testo | sì | es. "Giornata mondiale della vista" |
| `text` | testo | no | se presente, l'etichetta apre una scheda con il testo (`\n` = nuovo paragrafo) |
| `url` | link | sì | fonte ufficiale, `https://…` (mostrata come "fonte") |
| `verificata_il` | data | sì | quando Claude o Grok hanno controllato data e fonte |
| `atmosfera` | tema atmosfera | no | colori da usare in quei giorni (vedi sotto) |

```json
"ricorrenze": [{"from": "2026-10-08", "title": "Giornata mondiale della vista", "url": "https://www.iapb.it/", "verificata_il": "2026-11-07", "atmosfera": "vista"}]
```

### `atmosfera` — Tema manuale dell'home (oggetto, facoltativo)

Forza i colori della home per un periodo. Priorità dei colori: `atmosfera` manuale → `atmosfera` di una ricorrenza → festività nazionali/Natale → stagione (meteorologica, data di Roma). Gli avvisi di chiusura e orario speciale restano sempre in cima, qualunque tema.

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `tema` | tema atmosfera | no | uno tra `neutro`, `inverno`, `primavera`, `estate`, `autunno`, `natale`, `vista`, `amore`, `festa` |
| `dal` | data | no | primo giorno di validità (senza: subito) |
| `al` | data | no | ultimo giorno di validità (senza: nessun limite) |
| `effetti` | testo | no | `auto` (predefinito), `calmi` (meno particelle) oppure `spenti` (nessuna animazione) per tutti i visitatori |

```json
"atmosfera": {"tema": "natale", "dal": "2026-12-01", "al": "2027-01-06", "effetti": "calmi"}
```

### `passi` — Stato dei passi (lista, scritto a mano con fonte)

Per mostrare in home **Aperto, Chiuso o Limitato** nella casella del passo (Maloja e Spluga hanno una casella con il meteo; il nome deve contenere "Maloja" o "Spluga"/"Splügen") e per avvisare se un altro passo è chiuso, con catene/limitazioni o aperto. **Non è automatico**: lo stato si scrive solo guardando una fonte ufficiale e si mostra in home per 3 giorni dalla `verificata_il`, poi sparisce da solo (meglio nessuna informazione che una vecchia). Massimo 3 voci mostrate.

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `nome` | testo | sì | es. "Passo del Maloja" |
| `stato` | testo | sì | `chiuso`, `limitato` (catene o restrizioni) oppure `aperto` |
| `testo` | testo | no | dettaglio breve, es. "neve, obbligo di catene" |
| `al` | data | no | ultimo giorno di validità, se la fonte indica la fine |
| `url` | link | sì | fonte `https://…` (mostrata come "fonte"); vedi le fonti accettate sotto |
| `verificata_il` | data | sì | giorno in cui è stata guardata la fonte |
| `stagionale` | `true`/`false` | no | `true` per una chiusura invernale prevista: la voce resta visibile 14 giorni dalla `verificata_il` invece di 3 |

**Fonti accettate per Maloja e Spluga** (controllate il 13/11/2026; nessuna offre un feed automatico né condizioni d'uso per il riuso, quindi si leggono a mano e non si copiano i loro testi): TCS, `https://www.tcs.ch/de/tools/verkehrsinfo-verkehrslage/paesse-in-der-schweiz.php` (tempo reale, fonte principale); Provincia di Sondrio / Valtellina, `https://www.valtellina.it/it/situazione-passi` (riscontro italiano); Canton Grigioni, `https://www.strassen.gr.ch/` (ufficiale, per comunicati su lavori e chiusure); IAP Alpenpässe, `https://alpen-paesse.ch/alpenpaesse/malojapass/` (stato con data di validità, utile come riscontro). Il Maloja è di norma aperto tutto l'anno: ha senso inserire una voce soprattutto per `chiuso` o `limitato` (neve, catene, lavori). Lo Spluga ha invece una chiusura invernale abituale (TCS indica da novembre a marzo): finché il passo è chiuso, una voce `chiuso` (`nome`: "Passo dello Spluga") con `testo` "chiusura invernale" e `stagionale: true` resta visibile 14 giorni e va rinnovata guardando la fonte almeno ogni due settimane (la casella mostra il fiocco di neve).

```json
"passi": [{"nome": "Passo del Maloja", "stato": "chiuso", "testo": "neve", "url": "https://www.strassen.gr.ch", "verificata_il": "2026-11-08"}]
```

### `cantiere` — Cartello "Bots at work" (lista di sezioni, facoltativa)

Mostra il cartello con il robottino in coda a una sezione ancora incompleta. Il cartello compare **da solo** al posto del messaggio quando una sezione è vuota; con `cantiere` si può mostrarlo anche in una sezione che ha già qualche voce. Per toglierlo basta cancellare la sezione dalla lista. Sezioni ammesse: `notizie`, `eventi`, `vetrina`, `chiusure`, `social`. Il testo si cambia in `testi` con `cantiere_titolo` (predefinito "Bots at work") e `cantiere_testo` (predefinito "Qui stiamo ancora lavorando: torna a trovarci presto.").

```json
"cantiere": ["vetrina", "social"]
```

### `meteo.json` — Meteo di Chiavenna (automatico, non si modifica a mano)

File scritto ogni ora dal workflow `Aggiorna meteo` (`scripts/aggiorna_meteo.py`) con i dati di MET Norway (gratuiti, licenza CC BY 4.0, nessuna chiave; credito nel fondo pagina). Campi: `aggiornato` (UTC), `cielo` (`sereno`, `nuvoloso`, `pioggia`, `neve`, `nebbia`), `temp_c`, `vento_kmh`, più `maloja` (Engadina, 1.815 m) e `spluga` (2.113 m), facoltativi, con `cielo` e `temp_c`: compaiono in un'unica etichetta "Maloja … · Spluga …" con link "stato strade" alla pagina TCS dei passi. Il sito non chiede la posizione al visitatore. Se il file manca, non è valido o ha più di 4 ore, la home usa solo il tema stagionale e non mostra il meteo. Sole e luna dietro la home seguono l'ora reale di Chiavenna (alba, mezzogiorno, tramonto, fase lunare) e si attenuano con nuvole, pioggia o nebbia; senza meteo valido restano visibili in modo più tenue. Con il tema `natale` si accendono anche le luci; con `prefers-reduced-motion` o `?atm=off` le animazioni sono spente.

## Come funziona il controllo

`scripts/validate_content.py` gira a ogni push (workflow `.github/workflows/valida-contenuto.yml`, controllo "Valida contenuto"). Segnala come **errore**: JSON rotto, chiavi ripetute, campi o sezioni sconosciuti, campi obbligatori mancanti, date inesistenti, icone o temi inesistenti, link non https, immagini mancanti, `closures` con fine prima dell'inizio, campi del codice non documentati qui. Segnala come **avviso**: liste di card vuote, `link_testo` senza `link_url` (o viceversa), giorni mancanti negli orari.
