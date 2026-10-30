# Richieste tra Claude e Grok

File in comune per passarsi le modifiche da fare. **Prima di agire, leggere anche `schema.md`.**

## Regole

1. Chi ha bisogno di una modifica scrive una voce nella sezione di chi deve eseguirla (**Per Grok** = modifiche a `content.json`; **Per Claude** = modifiche a HTML, schema, script, grafica).
2. Una voce = una modifica, scritta in modo che si possa eseguire senza altre domande: cosa, dove, con quali valori esatti.
3. Chi esegue cambia lo stato in `fatto`, aggiunge data e riferimento al commit, e sposta la voce in **Archivio**.
4. Se la richiesta non è chiara o non rientra nello schema, lo stato diventa `domanda` e si scrive la domanda sotto la voce: risponde Enea.
5. Le modifiche a `content.json` si salvano solo dopo l'"ok" di Enea; le modifiche al sito si caricano dopo il suo "ok".
6. Repository pubblico: niente dati personali o riservati in questo file.

Formato di una voce:

```
### R-000 · stato: da fare | domanda | fatto · AAAA-MM-GG
**Cosa:** …
**Dove:** sezione / campo
**Note:** …
```

## Per Grok (`content.json`)

### R-001 · stato: da fare · 2026-10-30
**Cosa:** il post social "Gel antiappannante" usa l'immagine `eventi/antifog-polaroid.jpg`, che non esiste nel repository. Se Enea carica la foto non serve fare nulla; altrimenti togliere i campi `image` e `alt` da quel post.
**Dove:** `social[0]`
**Note:** il controllo "Valida contenuto" resta rosso finché non è risolto.

### R-002 · stato: da fare · 2026-10-30
**Cosa:** sostituire i contenuti di prova con contenuti reali, quando Enea li fornisce: notizia "Nuova pagina online (esempio)" (2026-10-26) e i tre prodotti "(esempio)" in `products`.
**Dove:** `news`, `products`
**Note:** non inventare testi, prezzi o marche.

### R-003 · stato: da fare · 2026-10-30
**Cosa:** recuperare dal sito originale (Google Sites) la storia della famiglia Vitali e proporla come notizia, con `icona` `libro`. Mostrare il testo a Enea prima di salvare.
**Dove:** `news`

## Per Claude (HTML, schema, grafica)

_Nessuna richiesta aperta._

## Archivio

_Vuoto._
