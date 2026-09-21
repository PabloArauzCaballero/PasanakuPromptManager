#!/usr/bin/env python
"""Puntúa el eval de disparo de skills.

Compara el veredicto a ciegas de los jueces contra el set dorado y reporta
precisión top-1 y top-3, global y desagregada por tipo (directo / oblicuo).

Uso:
    python docs/evals/score.py
    python docs/evals/score.py --json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ESCENARIOS = RAIZ / "escenarios"
VEREDICTOS = RAIZ / "veredictos"


def cargar_jsonl(patron: str, carpeta: Path) -> list[dict]:
    filas: list[dict] = []
    for archivo in sorted(carpeta.glob(patron)):
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                filas.append(json.loads(linea))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{archivo.name}:{n} no parsea: {exc}") from exc
    return filas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="salida JSON para consumo automático")
    ap.add_argument("--veredictos", default="veredictos",
                    help="carpeta de veredictos a puntuar (por defecto 'veredictos'; usar 'veredictos-r2' para la ronda 2)")
    args = ap.parse_args()

    global VEREDICTOS
    VEREDICTOS = RAIZ / args.veredictos

    dorado = {f["id"]: f for f in cargar_jsonl("lote-*.jsonl", ESCENARIOS)}
    if not dorado:
        raise SystemExit("No hay set dorado en docs/evals/escenarios/")

    if not VEREDICTOS.exists():
        raise SystemExit("Todavía no hay veredictos de los jueces en docs/evals/veredictos/")
    fallos_juez = cargar_jsonl("*.jsonl", VEREDICTOS)
    if not fallos_juez:
        raise SystemExit("La carpeta de veredictos está vacía")

    top1 = top3 = evaluados = 0
    por_tipo: dict[str, Counter] = defaultdict(Counter)
    errores: list[dict] = []
    confusion: Counter = Counter()
    sin_juzgar = set(dorado)

    for v in fallos_juez:
        ident = v.get("id")
        esperado = dorado.get(ident)
        if esperado is None:
            continue
        sin_juzgar.discard(ident)
        evaluados += 1
        tipo = esperado.get("tipo", "?")
        elegidas = [s for s in (v.get("elegidas") or []) if s]
        correcta = esperado["esperada"]

        acierto1 = bool(elegidas) and elegidas[0] == correcta
        acierto3 = correcta in elegidas[:3]
        top1 += acierto1
        top3 += acierto3
        por_tipo[tipo]["total"] += 1
        por_tipo[tipo]["top1"] += acierto1
        por_tipo[tipo]["top3"] += acierto3

        if not acierto3:
            errores.append({
                "id": ident,
                "tipo": tipo,
                "esperada": correcta,
                "elegidas": elegidas[:3],
                "prompt": esperado.get("prompt", ""),
            })
            if elegidas:
                confusion[(correcta, elegidas[0])] += 1

    def pct(n: int, d: int) -> float:
        return round(100.0 * n / d, 1) if d else 0.0

    resumen = {
        "escenarios_dorados": len(dorado),
        "evaluados": evaluados,
        "sin_juzgar": sorted(sin_juzgar),
        "top1_pct": pct(top1, evaluados),
        "top3_pct": pct(top3, evaluados),
        "por_tipo": {
            t: {
                "total": c["total"],
                "top1_pct": pct(c["top1"], c["total"]),
                "top3_pct": pct(c["top3"], c["total"]),
            }
            for t, c in sorted(por_tipo.items())
        },
        "fallos": errores,
        "confusiones_frecuentes": [
            {"esperada": a, "elegida": b, "veces": n}
            for (a, b), n in confusion.most_common(20)
        ],
    }

    if args.json:
        print(json.dumps(resumen, ensure_ascii=False, indent=1))
        return 0

    print(f"Set dorado: {resumen['escenarios_dorados']} | evaluados: {evaluados}")
    if resumen["sin_juzgar"]:
        print(f"SIN JUZGAR: {len(resumen['sin_juzgar'])} -> {resumen['sin_juzgar'][:5]} ...")
    print(f"\nTop-1: {resumen['top1_pct']}%   Top-3: {resumen['top3_pct']}%")
    for t, c in resumen["por_tipo"].items():
        print(f"  {t:9s} n={c['total']:3d}  top1={c['top1_pct']:5.1f}%  top3={c['top3_pct']:5.1f}%")

    if errores:
        print(f"\nFALLOS (no estaba en top-3): {len(errores)}")
        for e in errores:
            print(f"  [{e['tipo']}] esperada={e['esperada']} -> eligió={e['elegidas']}")
            print(f"      «{e['prompt'][:110]}»")
    if confusion:
        print("\nCONFUSIONES MÁS FRECUENTES (candidatas a delimitar fronteras):")
        for c in resumen["confusiones_frecuentes"]:
            print(f"  {c['esperada']}  ->  {c['elegida']}   x{c['veces']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
