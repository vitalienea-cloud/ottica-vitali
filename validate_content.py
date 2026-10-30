#!/usr/bin/env python3
"""Valida content.json contro le regole di schema.md e il codice di index.html.

Uso:  python3 scripts/validate_content.py [percorso/content.json]
Esce con codice 1 se ci sono errori (la Action GitHub diventa rossa).
Solo libreria standard: nessuna dipendenza da installare.
"""
import json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "content.json")
errors, warnings = [], []
err = lambda p, m: errors.append(f"{p}: {m}")
warn = lambda p, m: warnings.append(f"{p}: {m}")

# ---------- fonti di verità condivise con index.html ----------
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
m = re.search(r"const ICONE = \[(.*?)\];", html, re.S)
ICONE = re.findall(r'"([a-z0-9]+)"', m.group(1)) if m else []
m = re.search(r"const TEMI = \{(.*?)\};", html, re.S)
TEMI = re.findall(r"([a-z]+):\"#", m.group(1)) if m else []
if not ICONE or not TEMI:
    print("::error::Impossibile leggere ICONE/TEMI da index.html (struttura cambiata?)"); sys.exit(1)
SEZIONI = ["notizie","eventi","vetrina","chiusure","orari","social","servizi","organizzazione","contatti"]

# ---------- regole per sezione: campo -> (tipo, obbligatorio) ----------
DATE, STR, HTTPS, ICON, TEMA, IMG, LST = "date","str","https","icona","tema","img","list"
COMMON_VIS = {"icona": (ICON, False), "tema": (TEMA, False)}
IMGF = {"image": (IMG, False), "alt": (STR, False)}
RULES = {
  "news":       {"date": (DATE, True), "title": (STR, True), "text": (STR, False), "source": (STR, False), "url": (HTTPS, False), **COMMON_VIS, **IMGF},
  "events":     {"date": (DATE, True), "title": (STR, True), "text": (STR, False), **COMMON_VIS, **IMGF},
  "closures":   {"from": (DATE, True), "to": (DATE, False), "reason": (STR, True), **COMMON_VIS},
  "exceptions": {"date": (DATE, True), "text": (STR, True), **COMMON_VIS},
  "products":   {"name": (STR, True), "brand": (STR, False), "price": (STR, False), "text": (STR, False), **IMGF},
  "social":     {"title": (STR, True), "network": (STR, False), "date": (DATE, False), "url": (HTTPS, False), "text": (STR, False), **COMMON_VIS, **IMGF},
}
CARD = {"titolo": (STR, True), "icona": (ICON, False), "tema": (TEMA, False), "evidenza": (STR, False), "testo": (STR, False),
        "elenco": (LST, False), "testo_dopo": (STR, False), "link_testo": (STR, False), "link_url": ("link", False)}
CARD_ITEM = {"titolo": (STR, True), "testo": (STR, True)}
CARDS = ["servizi", "organizzazione", "contatti"]
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
TESTI_OK = {f"{p}_{s}" for s in SEZIONI for p in ("titolo","sub")}
TOP = set(RULES) | set(CARDS) | {"testi","hours","hours_note"}

def isdate(v):
    if not isinstance(v, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v): return False
    try: datetime.date.fromisoformat(v); return True
    except ValueError: return False

def check_value(path, kind, v):
    if kind == STR:
        if not isinstance(v, str): err(path, "deve essere testo"); return
        if not v.strip(): err(path, "testo vuoto")
    elif kind == DATE:
        if not isdate(v): err(path, f"data non valida ({v!r}): usare AAAA-MM-GG, giorno esistente")
    elif kind == HTTPS:
        if not (isinstance(v, str) and re.match(r"https://[^\s]+$", v)): err(path, "deve essere un link che inizia con https://")
    elif kind == "link":
        if not (isinstance(v, str) and re.match(r"(https://[^\s]+|tel:\+?\d+)$", v)): err(path, "deve iniziare con https:// oppure essere tel:+numero")
    elif kind == ICON:
        if v not in ICONE: err(path, f"icona {v!r} inesistente. Valide: {', '.join(ICONE)}")
    elif kind == TEMA:
        if v not in TEMI: err(path, f"tema {v!r} inesistente. Validi: {', '.join(TEMI)}")
    elif kind == IMG:
        if not (isinstance(v, str) and re.fullmatch(r"(eventi|vetrina)/[\w\-.]+\.(jpe?g|png|webp)", v, re.I) and ".." not in v):
            err(path, "immagine: solo file in eventi/ o vetrina/ (jpg, png, webp)")
        elif not os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(CONTENT)), v)):
            err(path, f"il file {v} non esiste nel repository (verrebbe nascosto in silenzio)")

def check_obj(path, o, rules):
    if not isinstance(o, dict): err(path, "deve essere un oggetto { ... }"); return
    for k in o:
        if k not in rules: err(f"{path}.{k}", "campo non previsto dallo schema (aggiornare schema.md e la validazione insieme al codice)")
    for k, (kind, req) in rules.items():
        if k in o:
            if kind == LST: continue
            check_value(f"{path}.{k}", kind, o[k])
        elif req: err(f"{path}.{k}", "campo obbligatorio mancante")

# ---------- lettura del JSON (anche chiavi duplicate) ----------
def no_dups(pairs):
    d = {}
    for k, v in pairs:
        if k in d: err("json", f"chiave duplicata {k!r}: la seconda sovrascrive la prima in silenzio")
        d[k] = v
    return d
try:
    raw = open(CONTENT, encoding="utf-8").read()
except OSError as e:
    print(f"::error file={CONTENT}::{e}"); sys.exit(1)
try:
    D = json.loads(raw, object_pairs_hook=no_dups)
except json.JSONDecodeError as e:
    print(f"::error file=content.json,line={e.lineno}::JSON non valido: {e.msg} (riga {e.lineno}, colonna {e.colno})"); sys.exit(1)
if not isinstance(D, dict):
    print("::error file=content.json::La radice deve essere un oggetto { ... }"); sys.exit(1)

# ---------- struttura ----------
for k in D:
    if k not in TOP: err(k, "sezione non prevista dallo schema")
for sec, rules in RULES.items():
    if sec in D:
        if not isinstance(D[sec], list): err(sec, "deve essere una lista [ ... ]"); continue
        for i, it in enumerate(D[sec]): check_obj(f"{sec}[{i}]", it, rules)
for sec in CARDS:
    if sec in D:
        if not isinstance(D[sec], list): err(sec, "deve essere una lista [ ... ]"); continue
        if not D[sec]: warn(sec, "lista vuota: il sito usa i testi predefiniti")
        for i, c in enumerate(D[sec]):
            p = f"{sec}[{i}]"; check_obj(p, c, CARD)
            if isinstance(c, dict):
                if "elenco" in c:
                    if not isinstance(c["elenco"], list): err(p + ".elenco", "deve essere una lista")
                    else:
                        for j, e in enumerate(c["elenco"]): check_obj(f"{p}.elenco[{j}]", e, CARD_ITEM)
                if bool(c.get("link_testo")) != bool(c.get("link_url")): warn(p, "link_testo e link_url vanno insieme: altrimenti il link non appare")
if "testi" in D:
    if not isinstance(D["testi"], dict): err("testi", "deve essere un oggetto")
    else:
        for k, v in D["testi"].items():
            if k == "hero_sottotitolo": warn(f"testi.{k}", "non più usato: il sottotitolo è stato tolto dalla home")
            elif k not in TESTI_OK: err(f"testi.{k}", "chiave non prevista (valide: titolo_<sezione>, sub_<sezione>)")
            elif not isinstance(v, str): err(f"testi.{k}", "deve essere testo")
if "hours" in D:
    if not isinstance(D["hours"], dict): err("hours", "deve essere un oggetto con i giorni in inglese")
    else:
        for k, v in D["hours"].items():
            if k not in DAYS: err(f"hours.{k}", f"giorno non valido. Validi: {', '.join(DAYS)}")
            elif not isinstance(v, str): err(f"hours.{k}", "deve essere testo (es. \"9:00-12:30, 15:00-19:00\" oppure \"Chiuso\")")
        for d in DAYS:
            if d not in D["hours"]: warn(f"hours.{d}", "giorno mancante: verrà mostrato \"Chiuso\"")
if "hours_note" in D and not isinstance(D["hours_note"], str): err("hours_note", "deve essere testo")
for i, c in enumerate(D.get("closures", []) if isinstance(D.get("closures"), list) else []):
    if isinstance(c, dict) and isdate(c.get("from")) and isdate(c.get("to")) and c["to"] < c["from"]:
        err(f"closures[{i}].to", "la data di fine è prima di quella di inizio")

# ---------- coerenza con schema.md ----------
try:
    S = open(os.path.join(ROOT, "schema.md"), encoding="utf-8").read()
    need = set(RULES) | set(CARDS) | {"testi", "hours", "hours_note"} | set(ICONE) | set(TEMI)
    for rules in list(RULES.values()) + [CARD, CARD_ITEM]: need |= set(rules)
    need |= set(DAYS)
    for n in sorted(need):
        if f"`{n}`" not in S: err("schema.md", f"non documenta `{n}`: aggiornare schema.md nella stessa commit")
except OSError:
    err("schema.md", "file mancante nella root")

for w in warnings: print(f"::warning file=content.json::{w}")
for e in errors: print(f"::error file=content.json::{e}")
print(f"\ncontent.json: {len(errors)} errori, {len(warnings)} avvisi")
sys.exit(1 if errors else 0)
