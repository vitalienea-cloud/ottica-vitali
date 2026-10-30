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

## Per Claude (HTML, schema, grafica)

_Nessuna richiesta aperta._

## Archivio

### R-001 · stato: fatto · 2026-10-30
**Cosa:** post "Gel antiappannante": tolti `image` e `alt` (foto non disponibile), messo il link al post vero e la nuova icona `antiappannante` (lente appannata, disegnata da Claude sulla descrizione di Grok).
**Dove:** `social[0]`, icona aggiunta a `index.html` e `schema.md`

### R-003 · stato: fatto · 2026-10-30
**Cosa:** aggiunta la notizia "La nostra storia" (icona `libro`), testo approvato da Enea, con il nome di Sara Ghelfi.
**Dove:** `news[0]`

<!-- prova scrittura Grok -->
