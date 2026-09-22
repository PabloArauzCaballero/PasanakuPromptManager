"""Resuelve todo enlace relativo a .md de un arbol de reparto. Sale 1 si alguno no existe."""
import re
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
ENLACE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
rotos = []
total = 0

for md in sorted(RAIZ.rglob("*.md")):
    for destino in ENLACE.findall(md.read_text(encoding="utf-8")):
        if destino.startswith(("http://", "https://", "#", "mailto:")):
            continue
        destino = destino.split("#")[0]
        if not destino:
            continue
        total += 1
        if not (md.parent / destino).resolve().exists():
            rotos.append("{0} -> {1}".format(md.relative_to(RAIZ).as_posix(), destino))

print("enlaces relativos revisados: {0}".format(total))
print("rotos: {0}".format(len(rotos)))
for r in rotos:
    print("  - " + r)
sys.exit(1 if rotos else 0)
