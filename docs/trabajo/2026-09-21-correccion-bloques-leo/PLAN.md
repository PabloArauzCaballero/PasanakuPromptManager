# Plan — Corregir el bloque B de Leo y cerrar los rastros que quedan en su bloque C

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (este repo, solo documentos) ·
  Predecesor: [docs/trabajo/2026-09-21-correccion-bloques-richard-y-pablo-c](../2026-09-21-correccion-bloques-richard-y-pablo-c/PLAN.md)
- Resultado observable: el carril de Leo (bloque B `PR8-DialogoYEstados.Frontend` y bloque C
  `PR13-Ci.Frontend`) referencia el repo real de Pasanaku, con el mismo criterio ya aplicado a
  Pablo (`PR10`/`PR15`) y a Richard (`PR6`/`PR11`).
- Kill-test: `grep -rn "mantra-core-health" repartos/2026-09-21/PromptNoche/Frontend/Leo/` no debe
  devolver ninguna línea operativa (solo notas explícitas de corrección con fecha).

## Contexto (verificado antes de tocar nada)

- `PR13-Ci.Frontend` (bloque C de Leo) **ya apunta correctamente** a `PasanakuBackend`, rama `dev`,
  y ya está mapeado al plan madre (`H6`, `H7`, `H8` + el paso de clientes de `H0.S1.M9`) — mismo
  patrón que `PR11` y `PR15`. Solo tiene 2 líneas colgando (7 y 45) que describen el bloque B como
  `mantra-core-health`, correctas cuando se escribieron, falsas ahora que `PR8` se corrige.
- `PR8-DialogoYEstados.Frontend` (bloque B de Leo) apunta a `mdavila-2001/mantra-core-health`, rama
  `mockup` — mismo error que tenían `PR6` y `PR10` antes de corregirse.
- Verificado contra el clon local `Pasanaku/PasanakuBackend`: existen `packages/ui/src/dialogo`,
  `packages/ui/src/estado-de-pantalla` y `packages/ui/src/estado-vacio` — el tema del carril
  (contrato de estado, host de estados, diálogo con foco y política de descarte) tiene equivalentes
  reales y discretos para retargetear, igual que pasó con `PR10` y `packages/ui/src/catalogo`.

## Alcance

- **IN:**
  - `repartos/2026-09-21/PromptNoche/Frontend/Leo/PR8-DialogoYEstados.Frontend/DialogoHostDeEstadosYBorrador.md`
  - `repartos/2026-09-21/PromptNoche/Frontend/Leo/Leo-Daily-Noche-2026-09-21.md`
  - `repartos/2026-09-21/PromptNoche/Frontend/Leo/PR13-Ci.Frontend/CiRealMacosYReleaseIos.md` (solo
    las 2 líneas colgando)
  - `repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md` (ampliar la nota de corrección del
    bloque B a Leo)
- **OUT:** `PR7`, `PR9` (Justin, Marcelo) y sus bloques C (`PR12`, `PR14`) — mismo criterio de diff
  mínimo: no se pidieron, quedan como hallazgo. El backend de Leo (bloque A). Ejecutar cualquier
  microtarea real de `PR8` o `PR13`.
- Ambigüedades registradas: ninguna nueva. Se reutiliza el criterio ya sentado en los dos trabajos
  predecesores.

## H1 — El bloque B de Leo referencia el repo real de Pasanaku

**CA:** Igual que en `PR6`/`PR10`, aplicado a `PR8`.
**DoD:** `grep` de cierre sin resultados operativos + validadores del repo en verde.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Cabecera de `PR8`: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `leo/frontend/dialogo-estados` | Cita el repo real | `grep -n "Repo:" PR8-....md` → URL de PasanakuBackend | HECHO |
| H1.S1.M2 | Alcance IN retargeteado a `packages/ui/src/estado-de-pantalla`, `packages/ui/src/estado-vacio` y `packages/ui/src/dialogo`, confirmados como existentes | El alcance cita las tres rutas reales | `grep -n "packages/ui/src/dialogo\|packages/ui/src/estado" PR8-....md` → 1 o más | HECHO |
| H1.S1.M3 | Tabla de comandos reemplazada por los reales (`turbo run lint/typecheck/test:front/build`; `CMD_UI_TEST` con `yarn workspace @aportaya/ui test:front`) | Cada alias cita comando real | `grep -n "turbo run" PR8-....md` → 3 o más | HECHO |
| H1.S1.M4 | Ritual de entrega retargeteado a `dev` (branch base, rebase, PR) | Sin `mockup` | `grep -n "mockup" PR8-....md` → vacío | HECHO |
| H1.S1.M5 | Reglas reevaluadas: 90 completa; 91 condicionada a que los dos modales elegidos en H3.S2.M1 muestren un importe/cobro; 98 fuera salvo contrato entre servicios | La sección ya no dice "No aplican la 91 ni la 98" sin matiz | lectura de la sección 1 | HECHO |
| H1.S1.M6 | `AMB-F3`/`AMB-F5` y la sección de instalación del estándar actualizadas (carpeta `PasanakuBackend/`, integración contra `dev`) | Reflejan Pasanaku | lectura de las secciones 1 y 5 | HECHO |

## H2 — El daily de Leo referencia el repo real en los dos bloques

**CA:** El daily ya no describe el bloque B como `mantra-core-health`, y aclara que B y C comparten
repo desde esta corrección.
**DoD:** `grep` de cierre.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Cabecera del bloque B en el daily corregida, con nota de corrección fechada | Cita el repo real | `grep -n "Repo:" Leo-Daily-....md` | HECHO |
| H2.S1.M2 | Línea "Otro repo, otras reglas" del bloque C corregida; sección de instalación del estándar corregida a `PasanakuBackend/` | Ya no dice `mantra-core-health` | lectura de las dos líneas | HECHO |

## H3 — Los rastros de "bloque B = mantra-core-health" en el bloque C de Leo se corrigen

**CA:** `PR13` ya no afirma que el bloque B de Leo es de otro repo.
**DoD:** `grep` de cierre.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Línea 7 y línea ~45 de `PR13` corregidas | Ya no dicen "es de mantra-core-health" | `grep -n "mantra-core-health" PR13-....md` → vacío | HECHO |

## H4 — El daily del equipo refleja que Leo también quedó retargeteado

**CA:** La nota del bloque B se amplía a Leo, y su fila en la tabla lo indica.
**DoD:** lectura de la nota y de la fila.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Nota de corrección del bloque B ampliada a Leo | Menciona a Pablo, Richard y Leo | lectura de la nota | HECHO |
| H4.S1.M2 | Fila de Leo en la tabla del bloque B marcada como retargeteada | La fila lo indica | lectura de la fila | HECHO |

## H5 — Verificación

**CA:** Validadores del repo en verde; cero referencias operativas a `mantra-core-health`/`mockup`
en los archivos de Leo.
**DoD:** salidas pegadas en `evidencia/`.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H5.S1.M1 | `check_reparto.py` en verde | exit 0 | `python tools/check_reparto.py repartos/2026-09-21` | HECHO |
| H5.S1.M2 | `check_skills_citadas.py` en verde | exit 0 | `python tools/check_skills_citadas.py` | HECHO |
| H5.S1.M3 | Cero referencias operativas en los archivos tocados | sin coincidencias operativas | `grep -rn "mantra-core-health\|mockup" <archivos IN>` | HECHO |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| `PR7`, `PR9` y sus bloques C siguen con el mismo patrón sin corregir | Confusión igual que antes de corregir `PR6`/`PR8`/`PR10` | Se registra como hallazgo en el reporte |
