# Reporte — Conflictos y merges bloqueados en todos los repos

> **AVANCE: 12 / 34 — 35,3 %.** (Los 12 microtareas de `H1`, completo. `H2` (17) y `H3` (11)
> siguen en `TODO`. Cálculo directo de la tabla del `PLAN.md`: `python .claude/hooks/plan_status.py`
> reportó `12/34 HECHO (35.3%)` en el aviso de cierre del candado.)

- Fecha: 2026-09-22 · Plan: [PLAN.md](./PLAN.md) · Repos afectados (reales, con push a rama de
  PR, sin tocar `dev`/`main`): `PabloArauzCaballero/PasanakuBackend` (PR #6),
  `mdavila-2001/mantra-core-health` (PR #435, pendiente #381), `PabloArauzCaballero/EcomicDataCenter`
  (PR #97), `AtlasBackend` (7 PRs `BLOCKED`, diagnóstico sin empezar).
- Peldaño de evidencia alcanzado: **`VERIFIED`** para los tres PRs de `H1` — cada uno se consultó
  con `gh pr view --json mergeable,mergeStateStatus` **después** del push, no se asume por haber
  resuelto los marcadores localmente. **`UNKNOWN`** para `H2` (el PR #381 más grande, 42
  conflictos) y para `H3` (los 7 `BLOCKED` de AtlasBackend): ninguna microtarea de esos dos hitos
  se ejecutó todavía.

Este reporte lo escribe una sesión distinta de la que hizo el trabajo de `H1` — el candado de
cierre (`report_gate.py`) bloqueaba el `Stop` de *esta* sesión por un trabajo ajeno sin reportar.
Se arma solo con lo que el `PLAN.md` y los tres archivos de `evidencia/` ya existentes registraban;
nada se ejecutó ni se inventó para escribir este documento.

## Completado

| ID | Qué se logró (observable) | Comando | Resultado |
|---|---|---|---|
| H1.S1 — `PasanakuBackend#6` | `.github/CODEOWNERS` y `.github/dependabot.yml` conciliados (unión de reglas de las dos ramas, sin perder ninguna), commit de merge pusheado a `leo/frontend/ci` | `gh pr view 6 -R PabloArauzCaballero/PasanakuBackend --json mergeable,mergeStateStatus` | `MERGEABLE` / `UNSTABLE` — evidencia en `evidencia/H1.S1-pasanakubackend-6.md` |
| H1.S2 — `mantra-core-health#435` | `content-dialog.ts` conciliado conservando el comportamiento de las dos ramas, pusheado a `claude/encuestas-surveymonkey` | `gh pr view 435 -R mdavila-2001/mantra-core-health --json mergeable,mergeStateStatus` | `MERGEABLE` / `UNSTABLE` — evidencia en `evidencia/H1.S2-mantra-core-health-435.md` |
| H1.S3 — `EcomicDataCenter#97` | `macro-annual-sectors.json` conciliado como **unión pura** (regla 97.4: ningún valor inventado ni alterado, solo claves de un lado + del otro), más `boot-seed.macro-annual-history.ts` y `macro-annual-history.schema.ts`, pusheado a `feat/sector-indicators` | `gh pr view 97 -R PabloArauzCaballero/EcomicDataCenter --json mergeable,mergeStateStatus` | `MERGEABLE` / `CLEAN` — evidencia en `evidencia/H1.S3-ecomicdatacenter-97.md` |

**Los tres PRs quedaron `MERGEABLE`, no mergeados** — es la decisión explícita del alcance (§OUT
del `PLAN.md`): el autor de cada PR revisa y mergea, esta sesión no tocó `dev` ni `main` de ningún
repo.

## A medias

ninguna. Lo que no se terminó de `H1` quedó en `TODO` explícito dentro de `H2`/`H3` (son hitos
distintos, no microtareas de `H1` a medio hacer).

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| `H2.S1` (4 microtareas) — fechar los dos borrados cruzados de `mantra-core-health#381` contra el historial y escribir la tabla de decisión | `TODO` | Es el primer paso del hito de mayor riesgo (42 conflictos, con borrados en los dos sentidos). No depende de nada externo — es trabajo directamente ejecutable. |
| `H2.S2` (7 microtareas) — resolver los 42 conflictos de `#381` (incluidos los `modify/delete`, `.claude/settings.json`, `.gitignore`, árbol de accesos, `features/account`, `features/agenda`) | `TODO` | Depende de que `H2.S1` fije primero qué borrado gana en cada archivo — resolverlos antes sería adivinar sobre una decisión de producto (regla 00 §1.7, ya registrada como ambigüedad en el `PLAN.md`). |
| `H2.S3` (2 microtareas) — correr los tests dirigidos del área y pushear `#381` | `TODO` | Depende de `H2.S2`. |
| `H3.S1` (6 microtareas) — bajar y clasificar los logs de los 7 `BLOCKED` de AtlasBackend (`gitleaks`, `yarn audit`, `migraciones+seeders+smoke`, más las causas propias de #24 y #46) | `TODO` | Trabajo directamente ejecutable, no depende de `H1` ni de `H2`. No se llegó a arrancar en esta sesión. |
| `H3.S2` (3 microtareas) — corregir la causa común si es corregible, re-verificar los 5 PRs de Dependabot, declarar `BLOQUEADO` lo que exceda el alcance | `TODO` | Depende de que `H3.S1` primero clasifique la causa (regla 80.4: la clasificación exige reproducción, no se adivina antes). |

## Evidencia

Los tres archivos de `H1` ya existentes en `evidencia/`:

```text
evidencia/H1.S1-pasanakubackend-6.md      → PasanakuBackend#6: MERGEABLE/UNSTABLE
evidencia/H1.S2-mantra-core-health-435.md → mantra-core-health#435: MERGEABLE/UNSTABLE
evidencia/H1.S3-ecomicdatacenter-97.md    → EcomicDataCenter#97: MERGEABLE/CLEAN
```

Salida del candado de cierre, que es lo que disparó este reporte:

```text
docs/trabajo/2026-09-22-conflictos-y-merges-bloqueados/
    microtareas: 12/34 HECHO (35.3%)
    en TODO/EN CURSO: H2.S1.M1, H2.S1.M2, H2.S1.M3, H2.S1.M4, H2.S2.M1, H2.S2.M2, H2.S2.M3, H2.S2.M4
```

## No cubierto

- **`H2` y `H3` completos (22 de las 34 microtareas) no se ejecutaron** — ver "Pendiente".
- **No se verificó si algún otro PR pasó de `MERGEABLE` a `CONFLICTING` desde que se resolvió `H1`**
  (por ejemplo, si alguien más pusheó a `dev` de esos repos mientras tanto). El kill-test del plan
  (`gh pr list --json number,mergeable` sin ningún `CONFLICTING`) no se volvió a correr al cerrar
  esta sesión de reporte.
- **`UNSTABLE` en `PasanakuBackend#6` y `mantra-core-health#435`** significa que el conflicto de
  merge se resolvió, pero esos PRs tienen otros checks (no de merge) todavía pendientes o en rojo
  — fuera del alcance declarado de `H1` (que solo pedía `mergeable=MERGEABLE`), pero vale que quien
  retome sepa que "mergeable" no es lo mismo que "listo para mergear sin mirar los checks".

## Desvíos del plan

Ninguno registrado en el `PLAN.md` para `H1`. La única nota es la de esta sesión: el `REPORTE.md`
no lo escribió quien hizo `H1` — se reconstruyó a partir del `PLAN.md` y la `evidencia/` ya
existentes, sin ejecutar ni verificar nada nuevo.

## Riesgos residuales

Los cinco del `PLAN.md` siguen vigentes y ninguno se cerró en esta sesión de reporte — en particular:
resolver mal un borrado cruzado en `#381` puede resucitar código retirado a propósito (mitigado
por el plan de `H2.S1`, todavía sin ejecutar), y `macro-annual-sectors.json` en `#97` ya se
verificó que no tuvo claves con valores divergentes entre ramas (si las hubiera tenido, `H1.S3.M3`
lo habría detenido y declarado `BLOQUEADO` en vez de elegir un valor — no fue necesario, la unión
fue limpia).

## Decisiones y ambigüedades

Las dos que ya trae el `PLAN.md`, sin resolver todavía porque pertenecen a `H2` (no ejecutado):

1. **`mantra-core-health#381`, borrados cruzados** (`features/consultation/*` borrado en `dev`,
   `my-profile/work-history/*` borrado en la rama). Supuesto a tomar en `H2.S1`: el borrado más
   reciente de cada lado gana, verificado commit por commit. A confirmar con el dueño del carril C
   antes de mergear — **todavía no se le confirmó, porque `H2.S1` no se ejecutó**.
2. **`EcomicDataCenter#97`, `macro-annual-sectors.json`** (regla 97.4): ya resuelto en `H1.S3` — la
   unión no encontró valores divergentes para la misma clave, así que la ambigüedad no llegó a
   activarse.
