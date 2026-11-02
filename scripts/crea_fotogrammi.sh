#!/usr/bin/env bash
# Crea i fotogrammi per la rotazione 360° di un prodotto a partire da un breve video
# (un giro completo dell'oggetto). Richiede ffmpeg.
#
# Uso:   scripts/crea_fotogrammi.sh video.mp4 nome-prodotto [numero_fotogrammi]
# Esempio: scripts/crea_fotogrammi.sh giro.mp4 acetato 36
#
# Scrive vetrina/<nome-prodotto>/01.webp … NN.webp (576x576, sfondo come il sito).
# Poi in content.json il prodotto avrà:  "rotazione": "vetrina/<nome-prodotto>", "fotogrammi": NN
set -euo pipefail
[ $# -ge 2 ] || { sed -n '2,9p' "$0"; exit 1; }
VIDEO="$1"; NOME="$2"; N="${3:-36}"
[[ "$NOME" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "Il nome può avere solo lettere, numeri, - e _"; exit 1; }
[[ "$N" =~ ^[0-9]+$ ]] && [ "$N" -ge 8 ] && [ "$N" -le 72 ] || { echo "Il numero di fotogrammi va da 8 a 72"; exit 1; }
cd "$(dirname "$0")/.."
OUT="vetrina/$NOME"; mkdir -p "$OUT"; rm -f "$OUT"/*.webp
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
FPS=$(awk -v n="$N" -v d="$DUR" 'BEGIN{printf "%.6f", n/d}')
ffmpeg -v error -y -i "$VIDEO" \
  -vf "fps=$FPS,scale=576:576:force_original_aspect_ratio=decrease,pad=576:576:(ow-iw)/2:(oh-ih)/2:color=0x050c19" \
  -frames:v "$N" -start_number 1 -c:v libwebp -quality 68 "$OUT/%02d.webp"
CNT=$(ls "$OUT"/*.webp | wc -l); KB=$(du -sk "$OUT" | cut -f1)
echo "Creati $CNT fotogrammi in $OUT/ (circa ${KB} KB in totale)."
[ "$CNT" -eq "$N" ] || echo "ATTENZIONE: attesi $N fotogrammi, creati $CNT: usare \"fotogrammi\": $CNT"
echo "In content.json: \"rotazione\": \"$OUT\", \"fotogrammi\": $CNT"
