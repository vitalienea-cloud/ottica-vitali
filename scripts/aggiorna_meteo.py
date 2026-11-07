#!/usr/bin/env python3
"""Scrive meteo.json con il tempo attuale di Chiavenna (MET Norway, Locationforecast 2.0).

Fonte gratuita anche per uso commerciale, licenza CC BY 4.0 (credito nel fondo pagina).
Richiede uno User-Agent che identifichi il sito: vedi UA. Non serve nessuna chiave.
Se la richiesta fallisce il file precedente resta com'è e il sito, dopo 4 ore, torna al tema stagionale.
"""
import json, sys, urllib.request, datetime as dt

LAT, LON, ALT = 46.3195, 9.4017, 333
UA = "OtticaVitaliSito/1.0 github.com/vitalienea-cloud/ottica-vitali servizioclienti@otticavitali.com"
URL = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={LAT}&lon={LON}&altitude={ALT}"
OUT = sys.argv[1] if len(sys.argv) > 1 else "meteo.json"


def cielo(code: str) -> str:
    c = code.split("_")[0]
    if c in ("clearsky", "fair"):
        return "sereno"
    if c == "partlycloudy":
        return "sereno"  # poco nuvoloso: resta il tema sereno
    if c == "cloudy":
        return "nuvoloso"
    if c == "fog":
        return "nebbia"
    if "snow" in c or "sleet" in c:
        return "neve"
    if "rain" in c:
        return "pioggia"
    return "nuvoloso"


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.load(r)
    ts = j["properties"]["timeseries"][0]
    det = ts["data"]["instant"]["details"]
    sym = (ts["data"].get("next_1_hours") or ts["data"].get("next_6_hours") or {}).get("summary", {}).get("symbol_code")
    if sym is None or "air_temperature" not in det or "wind_speed" not in det:
        raise SystemExit("risposta MET Norway senza i campi attesi")
    out = {
        "aggiornato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cielo": cielo(sym),
        "temp_c": round(float(det["air_temperature"]), 1),
        "vento_kmh": round(float(det["wind_speed"]) * 3.6),
        "simbolo": sym,
        "fonte": "MET Norway (CC BY 4.0)",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(out)


if __name__ == "__main__":
    main()
