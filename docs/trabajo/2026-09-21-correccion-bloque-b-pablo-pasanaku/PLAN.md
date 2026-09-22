# Plan — Corregir el bloque B de Pablo (frontend) para que apunte a Pasanaku, no a mantra-core-health

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (este repo, solo documentos) ·
  Predecesor: [docs/trabajo/2026-09-21-reparto-frontend-refactor](../2026-09-21-reparto-frontend-refactor/PLAN.md)
  y [docs/trabajo/2026-09-21-reparto-frontend-rescate](../2026-09-21-reparto-frontend-rescate/PLAN.md)
- Resultado observable: quien lee el encargo `PR10-CatalogoYGates.Frontend` de Pablo, su daily de
  frontend, y las referencias cruzadas en los documentos de coordinación, encuentra el repo real de
  Pasanaku (`PasanakuBackend`/`PasanakuFrontend`), no `mdavila-2001/mantra-core-health`; y los
  validadores del repo (`check_reparto.py`, `check_skills_citadas.py`) siguen en verde.
- Kill-test: `grep -ril "mantra-core-health\|mdavila-2001" repartos/2026-09-21/PromptNoche/Frontend/Pablo/`
  no debe devolver nada después del cambio.

## Contexto (hallazgo de esta sesión)

- `PR15-Contratos.Frontend` (bloque C de Pablo) **ya apunta correctamente** a
  `https://github.com/PabloArauzCaballero/PasanakuBackend.git` — no necesita corrección de repo.
- `PR10-CatalogoYGates.Frontend` (bloque B de Pablo) apunta a `https://github.com/mdavila-2001/mantra-core-health`,
  un repo de salud (`alovida`) ajeno a Pasanaku. La sesión que lo escribió lo sabía y lo registró
  como ambigüedad explícita (`AMB-F2` en `docs/trabajo/2026-09-21-reparto-frontend-refactor/PLAN.md:129`):
  "`mdavila-2001/mantra-core-health` no es un repo de Pasanaku" — decisión previa: usarlo igual,
  con las reglas 91/98 desactivadas para ese carril.
- El mismo patrón (`mantra-core-health` como repo del bloque B) aparece también en los carriles de
  Richard (`PR6`), Justin (`PR7`), Leo (`PR8`) y Marcelo (`PR9`) — **fuera de alcance de este
  trabajo** (regla 00 §3): se registran como hallazgo, no se tocan.
- Pablo (dueño de la decisión, `Coordinación` en `AMB-F2`) confirmó en esta sesión: el bloque B
  también es de Pasanaku. Esto **resuelve AMB-F2** para el carril de Pablo, no la anula para los
  otros cuatro.
- Verificado contra el clon local `Pasanaku/PasanakuBackend` (`git rev-parse HEAD` → `5d7948e`):
  existe `packages/ui/src/catalogo` (Angular) y `packages/diseno_flutter/lib/catalogo` (Flutter) —
  el tema del carril (catálogo de componentes, preview aislado, gates) tiene un equivalente real
  para retargetear, no hace falta inventarlo.

## Alcance

- **IN:**
  - `repartos/2026-09-21/PromptNoche/Frontend/Pablo/PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md`
  - `repartos/2026-09-21/PromptNoche/Frontend/Pablo/Pablo-Daily-Noche-2026-09-21.md`
  - `docs/trabajo/2026-09-21-reparto-frontend-refactor/PLAN.md` (nota `AMB-F2` y la línea OUT que
    excluye el repo) y su `REPORTE.md` si hace falta reflejar el cambio
  - `docs/trabajo/2026-09-21-reparto-frontend-rescate/PLAN.md` / `REPORTE.md` (menciones del riesgo
    "dos repos con reglas distintas" en el área frontend)
  - `repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md` (advertencia de los dos repos, si
    nombra a Pablo/bloque B específicamente)
- **OUT:** el contenido de `PR6`–`PR9` (Richard, Justin, Leo, Marcelo) — se anota como hallazgo, no
  se reescribe (regla 00 §3). El bloque A (backend) de Pablo. El bloque C (`PR15`), que ya está
  correcto. Ejecutar ninguna microtarea real del carril (eso es trabajo aparte, mucho más grande,
  a decidir después de esta corrección).
- Ambigüedades registradas: la que resuelve este trabajo es `AMB-F2` (solo para el carril de
  Pablo). Ninguna otra se resuelve por conveniencia.

## H1 — El bloque B de Pablo referencia el repo real de Pasanaku

**CA:** Dado el encargo `PR10-CatalogoYGates.Frontend` y el daily de Pablo, cuando alguien lee su
repo, rama, comandos y alcance de archivos, entonces apuntan a `PasanakuBackend`/`PasanakuFrontend`
y a paquetes reales (`packages/ui`, `packages/diseno_flutter`), no a `mantra-core-health`.
**DoD:** `grep` de verificación sin resultados + validadores del repo en verde.
**Estado:** HECHO

### H1.S1 — Corregir el encargo PR10-CatalogoYGates.Frontend

**CA:** El documento del carril no contiene ninguna referencia a `mantra-core-health` ni a
`mdavila-2001`, y sus comandos/rutas son los reales del monorepo de Pasanaku.
**DoD:** `grep -c "mantra-core-health\|mdavila-2001" PR10-....md` → `0`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Reemplazar cabecera de repo/rama por `PasanakuBackend` (canónico) / `PasanakuFrontend` (espejo), rama base `dev`, rama de trabajo `pablo/frontend/catalogo-ui` | La cabecera cita el repo real y una rama de trabajo consistente con `PR15` | `grep -n "Repo:" PR10-....md` → URL de PasanakuBackend | HECHO |
| H1.S1.M2 | Reemplazar la tabla de comandos candidatos (`yarn lint`, `yarn pw`, …) por los reales de la raíz (`turbo run lint`, `turbo run typecheck`, `turbo run test:front`, `turbo run test:a11y`, `turbo run build`) | Cada alias cita el comando real de `package.json` | `grep -n "turbo run" PR10-....md` → 5 o más líneas | HECHO |
| H1.S1.M3 | Retargetear alcance IN/OUT y reservas de archivo: `packages/ui/src/catalogo/**` (Angular) y `packages/diseno_flutter/lib/catalogo/**` (Flutter), en vez de las rutas hipotéticas de mantra-core-health | El alcance cita las dos rutas reales confirmadas | `grep -n "packages/ui/src/catalogo\|packages/diseno_flutter/lib/catalogo" PR10-....md` → 1 o más | HECHO |
| H1.S1.M4 | Marcar las rutas de nivel de microtarea (`component-stock.ts`, `core/mock/faker/props.ts`, etc.) como hipótesis heredadas **de mantra-core-health, ya descartadas**, y dejar que H1 del propio carril las redescubra contra Pasanaku | La nota de ambigüedad ya no dice "hipótesis heredadas del documento antecedente" sin más: aclara que son de otro repo y quedan por confirmar | lectura de la sección 5 / AMB-F3 del carril | HECHO |
| H1.S1.M5 | Reevaluar reglas aplicables: activar 90 completa (dato financiero real, no "leído como clínico"), 91 donde el catálogo cubra componentes de dinero (`campo-monto`, `desglose-de-cobro`, `cuenta-enmascarada`, confirmados en `packages/ui/src`); dejar 98 fuera salvo que el carril termine tocando un contrato entre servicios | La sección de reglas ya no dice "No aplican la 91 ni la 98" sin matiz | lectura de la sección 1 del carril | HECHO |

### H1.S2 — Corregir referencias cruzadas

**CA:** El daily de Pablo y los documentos de coordinación que hablan del bloque B de Pablo ya no
lo describen como `mantra-core-health`, y el estado de `AMB-F2` queda actualizado para su carril.
**DoD:** `grep` de verificación en cada archivo tocado.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Corregir la cabecera del bloque B en `Pablo-Daily-Noche-2026-09-21.md` (Frontend) | El daily cita el repo real de Pasanaku para el bloque B | `grep -n "Repo:" Pablo-Daily-....md` → URL de PasanakuBackend | HECHO |
| H1.S2.M2 | Actualizar `AMB-F2` en `docs/trabajo/2026-09-21-reparto-frontend-refactor/PLAN.md`: resuelta para el carril de Pablo (`PR10`), abierta para `PR6`–`PR9` | La fila de `AMB-F2` distingue el estado por carril | lectura de la fila `AMB-F2` | HECHO |
| H1.S2.M3 | Anotar en `docs/trabajo/2026-09-21-reparto-frontend-rescate/REPORTE.md` (riesgos residuales) que el bloque B de Pablo dejó de ser un repo ajeno, sin tocar la afirmación general sobre `PR6`–`PR9` | La nota aclara el alcance real de la corrección | lectura de la sección de riesgos | HECHO |
| H1.S2.M4 | Registrar hallazgo: `PR6`–`PR9` (Richard, Justin, Leo, Marcelo) tienen el mismo mismatch, sin corregir, en el `REPORTE.md` de este trabajo | El hallazgo queda citado con ruta y estado `ABIERTO` | lectura del `REPORTE.md` de este trabajo | HECHO |

### H1.S3 — Verificación

**CA:** Los validadores del repo siguen en verde después del cambio, y ninguna referencia a
`mantra-core-health`/`mdavila-2001` queda en los archivos del carril de Pablo.
**DoD:** las tres salidas pegadas en `evidencia/`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S3.M1 | `check_reparto.py` sigue en verde | exit 0 | `python tools/check_reparto.py repartos/2026-09-21` → `exit=0` | HECHO |
| H1.S3.M2 | `check_skills_citadas.py` sigue en verde | exit 0 | `python tools/check_skills_citadas.py` → `exit=0` | HECHO |
| H1.S3.M3 | Cero referencias a mantra-core-health en los archivos de Pablo tocados | sin coincidencias | `grep -ril "mantra-core-health\|mdavila-2001" repartos/2026-09-21/PromptNoche/Frontend/Pablo/` → vacío | HECHO |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Las rutas de microtarea de `PR10` (nivel `H1`–`H5`) siguen citando componentes/archivos genéricos que no se verificaron uno a uno contra `packages/ui` | Quien ejecute el carril puede toparse con rutas que no existen tal cual | El propio `H1` del carril es una auditoría: su DoD ya exige comprobación real antes de usar cualquier ruta, no cambia con esta corrección |
| `PR6`–`PR9` quedan con el mismo error, sin corregir | El resto del área frontend (Richard/Justin/Leo/Marcelo) sigue documentado contra un repo ajeno | Queda registrado como hallazgo explícito en el reporte, para que el equipo decida si se corrige |
