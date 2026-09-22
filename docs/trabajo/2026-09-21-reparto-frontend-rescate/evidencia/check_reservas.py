"""Colisiones de reservas entre los encargos del bloque C (AportaYa) del turno.

Por que existe: "dos personas escribiendo el mismo archivo es un defecto del reparto, no un
accidente" (README de repartos/). Este script lo comprueba en vez de confiar en la lectura.

Extrae las rutas entre backticks de la seccion "**IN:**" de cada encargo PR11..PR15 y reporta
toda ruta reclamada por mas de una persona. No juzga si la reserva esta bien elegida: solo que
no haya dos duenos del mismo archivo.

    python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py
    python ... --self-test
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path("repartos/2026-09-21/PromptNoche/Frontend")
LOTES = ("PR11", "PR12", "PR13", "PR14", "PR15")
RUTA = re.compile(r"`([a-z0-9_.\-/*{},]+/[a-z0-9_.\-/*{},]*)`", re.I)


def seccion_in(texto: str) -> str:
    """El bloque entre '**IN:**' y '**OUT:**'. Sin IN no hay reserva que comprobar."""
    ini = texto.find("**IN:**")
    fin = texto.find("**OUT:**", ini + 1)
    if ini < 0 or fin < 0:
        return ""
    return texto[ini:fin]


def normalizar(ruta: str) -> str:
    """Quita el comodin final para que `apps/x/**` y `apps/x/` colisionen igual."""
    return ruta.rstrip("/*")


def reclamos(base: Path) -> dict[str, set[str]]:
    porruta: dict[str, set[str]] = defaultdict(set)
    for archivo in sorted(base.glob("*/PR*/*.md")):
        if not archivo.parent.name.startswith(LOTES):
            continue
        persona = archivo.parent.parent.name
        for ruta in RUTA.findall(seccion_in(archivo.read_text(encoding="utf-8"))):
            porruta[normalizar(ruta)].add(persona)
    return porruta


def informar(porruta: dict[str, set[str]]) -> int:
    colisiones = {r: p for r, p in porruta.items() if len(p) > 1}
    print(f"rutas reclamadas: {len(porruta)}")
    for ruta, personas in sorted(colisiones.items()):
        print(f"  COLISION  {ruta} -> {', '.join(sorted(personas))}")
    print(f"{len(colisiones)} colisiones")
    return 1 if colisiones else 0


def self_test() -> int:
    fallas = 0

    def check(nombre: str, ok: bool) -> None:
        nonlocal fallas
        print(f"  {'OK   ' if ok else 'FALLA'} · {nombre}")
        fallas += 0 if ok else 1

    texto = "**IN:**\n- `apps/web/src/server.ts` y `packages/ui/**`.\n**OUT:** `otro/x.ts`"
    rutas = [normalizar(r) for r in RUTA.findall(seccion_in(texto))]
    check("lee las rutas del IN", rutas == ["apps/web/src/server.ts", "packages/ui"])
    check("no lee las del OUT", "otro/x.ts" not in rutas)
    check("normaliza el comodin", normalizar("apps/x/**") == "apps/x")
    check("sin IN devuelve vacio", seccion_in("sin secciones") == "")
    check("detecta colision", informar({"a/b": {"Leo", "Pablo"}}) == 1)
    check("sin colision sale 0", informar({"a/b": {"Leo"}}) == 0)
    print(f"check_reservas self-test: {6 - fallas} PASS, {fallas} FAIL")
    return 1 if fallas else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    if not BASE.is_dir():
        print(f"no encuentro {BASE}; corré esto desde la raíz del repo", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(informar(reclamos(BASE)))
