#!/bin/sh
# Genera modelos y funciones, verifica y empaqueta el .jar para la carpeta mods.
set -e
cd "$(dirname "$0")/.."
python3 tools/gen_models.py
python3 tools/gen_functions.py
python3 tools/check.py
VER=$(sed -n 's/^version="\(.*\)"/\1/p' src/META-INF/mods.toml)
mkdir -p build
OUT="build/canon-event-$VER-1.20.1.jar"
rm -f "$OUT"
(cd src && zip -qr -X "../$OUT" META-INF fabric.mod.json pack.mcmeta pack.png canon_logo.png assets data)
echo "Listo: $OUT"
