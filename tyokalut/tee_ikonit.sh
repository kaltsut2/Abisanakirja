#!/bin/sh
# Tekee kotinäytön ikonit yhdestä lähdekuvasta macOS:n sips-työkalulla.
#
#   1. Tallenna alkuperäinen kuva nimellä ikoni-lahde.png projektin juureen
#      (neliö, mieluiten vähintään 1024 × 1024).
#   2. sh tyokalut/tee_ikonit.sh
#
# VERSIONUMERO: Safari välimuistittaa kotinäytön ikonin tiedostonimen mukaan,
# eikä huomaa sisällön muuttumista. Kun ikoni vaihdetaan, nosta VERSIO ja
# päivitä sama numero index.html:ään ja manifest.webmanifest-tiedostoon.
set -e
VERSIO=v1
JUURI=$(cd "$(dirname "$0")/.." && pwd)
LAHDE="$JUURI/ikoni-lahde.png"

if [ ! -f "$LAHDE" ]; then
  echo "Puuttuu: $LAHDE" >&2
  exit 1
fi

for KOKO in 1024 512 192 180 64; do
  sips -s format png -z "$KOKO" "$KOKO" "$LAHDE" \
       --out "$JUURI/ikoni-$KOKO-$VERSIO.png" >/dev/null
  echo "ikoni-$KOKO-$VERSIO.png"
done
