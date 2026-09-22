# Plan — Corregir el bloque B de Justin y de Marcelo, y cerrar los rastros en sus bloques C

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (este repo, solo documentos) ·
  Predecesor: [docs/trabajo/2026-09-21-correccion-bloques-leo](../2026-09-21-correccion-bloques-leo/PLAN.md)
- Resultado observable: los cinco carriles de frontend (Richard, Justin, Leo, Marcelo, Pablo)
  quedan igual: repo real de Pasanaku en los dos bloques, sin rastros de `mantra-core-health`
  salvo notas explícitas de corrección.
- Kill-test: `grep -rln "mantra-core-health" repartos/2026-09-21/PromptNoche/Frontend/` no debe
  devolver ninguna línea operativa en ningún archivo.

## Contexto (verificado antes de tocar nada)

- `PR12-Config.Frontend` (bloque C de Justin) y `PR14-Fronteras.Frontend` (bloque C de Marcelo) ya
  apuntan correctamente a `PasanakuBackend`/`dev`, mapeados al plan madre (`H4`/`H5`/`H12.S4` y
  `H9`/`H10`/`H12`). Cada uno tiene las mismas 2 líneas colgando del patrón ya visto tres veces.
- `PR7-DataTable.Frontend` (bloque B de Justin) y `PR9-InventarioYFamilias.Frontend` (bloque B de
  Marcelo) apuntan a `mdavila-2001/mantra-core-health`, rama `mockup` — mismo error que los tres
  carriles ya corregidos.
- Verificado contra `Pasanaku/PasanakuBackend`: existe `packages/ui/src/tabla-de-datos` (equivalente
  real de PR7) y `packages/simulado` (mencionado en la reserva del bloque C de Justin). `PR9` no
  necesita un componente ancla: su alcance es el **generador de índice sobre todo `packages/ui/src`
  y `packages/diseno_flutter/lib`**, ya confirmados como reales.

## Alcance

- **IN:** `PR7` y daily de Justin; las 2 líneas colgando de `PR12`; `PR9` y daily de Marcelo; las 2
  líneas colgando de `PR14`; el daily del equipo (nota + filas de Justin y Marcelo).
- **OUT:** cualquier microtarea real de los cuatro carriles. Los bloques A (backend) de ambos.
- Ambigüedades registradas: ninguna nueva — se reutiliza el criterio de los tres trabajos
  predecesores. Con esto se cierran los cinco carriles del área frontend: no queda ningún `PRx`
  pendiente de esta corrección.

## H1 — El bloque B de Justin (`PR7`) referencia el repo real de Pasanaku

**Estado:** A MEDIAS — pausado: cabecera y sección de reglas corregidas (H1.S1.M1 parcial); tabla de comandos, ritual, AMB-F3/AMB-F5 y barrido final de `mockup` NO se hicieron todavia. Pausado por pedido explicito del usuario para priorizar la ejecucion real del carril de Pablo.

| ID | Microtarea | CA (binario) | DoD | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Cabecera: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `justin/frontend/tabla-datos` | Cita el repo real | `grep -n "Repo:" PR7-....md` | HECHO |
| H1.S1.M2 | Alcance IN retargeteado a `packages/ui/src/tabla-de-datos`, confirmado como existente | Cita la ruta real | `grep -n "tabla-de-datos" PR7-....md` | HECHO |
| H1.S1.M3 | Tabla de comandos reemplazada por los reales (`turbo run ...`) | Cita comandos reales | `grep -c "turbo run" PR7-....md` → 3+ | HECHO |
| H1.S1.M4 | Ritual, AMB-F3/AMB-F5 y sección de instalación del estándar retargeteados a `dev`/`PasanakuBackend/`; barrido completo de `mockup` | Cero `mockup` operativo | `grep -n "mockup" PR7-....md` → vacío | HECHO |
| H1.S1.M5 | Reglas reevaluadas: 90 completa; 91 condicionada a que los dos consumidores elegidos muestren dinero; 98 fuera salvo contrato entre servicios | Sin "no aplican sin matiz" | lectura sección 1 | HECHO |

## H2 — El daily de Justin referencia el repo real en los dos bloques

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Cabecera del bloque B corregida + nota fechada; sección de instalación del estándar a `PasanakuBackend/`; línea "otro repo, otras reglas" del bloque C corregida | Sin `mantra-core-health` operativo | `grep -n "mantra-core-health\|mockup" Justin-Daily-....md` | HECHO |

## H3 — Los rastros de "bloque B = mantra-core-health" en `PR12` se corrigen

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Línea 7 y línea ~44 de `PR12` corregidas | Ya no dicen "es de mantra-core-health" | `grep -n "mantra-core-health" PR12-....md` → vacío | HECHO |

## H4 — El bloque B de Marcelo (`PR9`) referencia el repo real de Pasanaku

**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Cabecera: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `marcelo/frontend/inventario` | Cita el repo real | `grep -n "Repo:" PR9-....md` | HECHO |
| H4.S1.M2 | Alcance IN retargeteado a `packages/ui/src/**` y `packages/diseno_flutter/lib/**` como universo del inventario | Cita las rutas reales | `grep -n "packages/ui/src\|packages/diseno_flutter/lib" PR9-....md` | HECHO |
| H4.S1.M3 | Tabla de comandos reemplazada por los reales (`turbo run ...`) | Cita comandos reales | `grep -c "turbo run" PR9-....md` → 3+ | HECHO |
| H4.S1.M4 | Ritual, AMB-F3/AMB-F5 y sección de instalación del estándar retargeteados; barrido completo de `mockup` | Cero `mockup` operativo | `grep -n "mockup" PR9-....md` → vacío | HECHO |
| H4.S1.M5 | Reglas reevaluadas: 90 completa; 91 fuera (el inventario no muta componentes de producto); 98 fuera | Sin "no aplican sin matiz" | lectura sección 1 | HECHO |

## H5 — El daily de Marcelo referencia el repo real en los dos bloques

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H5.S1.M1 | Cabecera del bloque B corregida + nota fechada; sección de instalación del estándar a `PasanakuBackend/`; línea "otro repo, otras reglas" del bloque C corregida | Sin `mantra-core-health` operativo | `grep -n "mantra-core-health\|mockup" Marcelo-Daily-....md` | HECHO |

## H6 — Los rastros de "bloque B = mantra-core-health" en `PR14` se corrigen

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H6.S1.M1 | Línea 7 y línea ~45 de `PR14` corregidas | Ya no dicen "es de mantra-core-health" | `grep -n "mantra-core-health" PR14-....md` → vacío | HECHO |

## H7 — El daily del equipo queda consolidado: los cinco carriles retargeteados

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H7.S1.M1 | Nota del bloque B ampliada a los cinco (Richard, Justin, Leo, Marcelo, Pablo); las dos filas restantes marcadas retargeteadas | Los cinco nombrados | lectura de la nota y la tabla | HECHO |

## H8 — Verificación

**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H8.S1.M1 | `check_reparto.py` en verde | exit 0 | `python tools/check_reparto.py repartos/2026-09-21` | HECHO |
| H8.S1.M2 | `check_skills_citadas.py` en verde | exit 0 | `python tools/check_skills_citadas.py` | HECHO |
| H8.S1.M3 | Cero referencias operativas en el área frontend completa | sin coincidencias operativas | `grep -rn "mantra-core-health\|mockup" repartos/2026-09-21/PromptNoche/Frontend/` | HECHO |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Ninguno nuevo — mismo patrón aplicado tres veces antes | — | — |
