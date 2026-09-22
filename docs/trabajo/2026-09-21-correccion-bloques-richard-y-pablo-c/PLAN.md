# Plan — Corregir el bloque B y C de Richard (frontend) y cerrar los rastros que quedaron en el C de Pablo

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (este repo, solo documentos) ·
  Predecesor: [docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku](../2026-09-21-correccion-bloque-b-pablo-pasanaku/PLAN.md)
- Resultado observable: el carril de Richard (bloque B `PR6-SmartPresentational.Frontend` y bloque
  C `PR11-Sesion.Frontend`) referencia el repo real de Pasanaku, igual que ya quedó el de Pablo; y
  las dos frases que en `PR11` (Richard) y `PR15` (Pablo) decían "el bloque B es de
  `mantra-core-health`" quedan corregidas, porque ahora es falso: el bloque B de Pablo (`PR10`) y el
  de Richard (`PR6`) ya son Pasanaku.
- Kill-test: `grep -rn "mantra-core-health" repartos/2026-09-21/PromptNoche/Frontend/Richard/ repartos/2026-09-21/PromptNoche/Frontend/Pablo/PR15-Contratos.Frontend/`
  no debe devolver ninguna línea operativa (solo, si acaso, notas explícitas de corrección con fecha).

## Contexto (verificado antes de tocar nada)

- `PR11-Sesion.Frontend` (bloque C de Richard) **ya apunta correctamente** a
  `https://github.com/PabloArauzCaballero/PasanakuBackend.git`, rama `dev`, y ya está mapeado al
  plan madre (`H1`, `H2`, `H3` de `docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`) —
  mismo patrón que `PR15` de Pablo. Solo le quedaron 2 líneas colgando (7 y 44) que describían el
  bloque B como `mantra-core-health`, correctas cuando se escribió, falsas ahora que `PR6` se corrige.
- `PR6-SmartPresentational.Frontend` (bloque B de Richard) apunta a `mdavila-2001/mantra-core-health`,
  rama `mockup` — mismo error que tenía `PR10` de Pablo antes de la sesión anterior.
- `PR15-Contratos.Frontend` (bloque C de Pablo) tiene las mismas 2 líneas colgando (7 y 49) que
  `PR11`: quedaron sin tocar en la corrección anterior porque esa sesión solo verificó la cabecera
  `Repo:`, no un `grep` completo del archivo. Es el "faltó" que señaló Pablo.
- A diferencia de `PR10` (que tenía un equivalente real y discreto — `packages/ui/src/catalogo`),
  `PR6` no necesita un paquete específico: su H1.S2.M1 **es** la microtarea que elige la pantalla
  piloto real dentro de `apps/web` o `apps/backoffice`. No se inventa acá cuál es; se corrige el
  encabezado, la rama y los comandos para que quien la elija lo haga contra el repo correcto.

## Alcance

- **IN:**
  - `repartos/2026-09-21/PromptNoche/Frontend/Richard/PR6-SmartPresentational.Frontend/QuienDecideYQuienDibuja.md`
  - `repartos/2026-09-21/PromptNoche/Frontend/Richard/Richard-Daily-Noche-2026-09-21.md`
  - `repartos/2026-09-21/PromptNoche/Frontend/Richard/PR11-Sesion.Frontend/RefrescoRestauracionYAuditoria.md` (solo las 2 líneas colgando)
  - `repartos/2026-09-21/PromptNoche/Frontend/Pablo/PR15-Contratos.Frontend/LineaBaseContratosAuthzYCierre.md` (solo las 2 líneas colgando)
  - `repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md` (agregar a Richard a la nota de
    corrección que ya menciona solo a Pablo)
- **OUT:** `PR7`, `PR8`, `PR9` (Justin, Leo, Marcelo) y sus bloques C (`PR12`–`PR14`) — mismo criterio
  de diff mínimo que la sesión anterior: no se pidieron, quedan como hallazgo. El backend de Richard
  (bloque A). Ejecutar cualquier microtarea real de `PR6` o `PR11`.
- Ambigüedades registradas: ninguna nueva. Se reutiliza el criterio de `AMB-F2` ya sentado en el
  trabajo predecesor.

## H1 — El bloque B de Richard referencia el repo real de Pasanaku

**CA:** Igual que `H1` del trabajo predecesor, aplicado a `PR6`.
**DoD:** `grep` de cierre sin resultados operativos + validadores del repo en verde.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Cabecera de `PR6`: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `richard/frontend/pantalla-piloto` | Cita el repo real | `grep -n "Repo:" PR6-....md` → URL de PasanakuBackend | HECHO |
| H1.S1.M2 | Tabla de comandos candidatos reemplazada por los reales (`turbo run lint/typecheck/test:front/build`; E2E a confirmar por app en H1 del propio carril) | Cada alias cita comando real o "a confirmar en H1" | `grep -n "turbo run" PR6-....md` → 3 o más | HECHO |
| H1.S1.M3 | Ritual de entrega: rama base `dev`, PR contra `dev`, sin `mockup` | Ritual usa `dev` | `grep -n "mockup" PR6-....md` → vacío | HECHO |
| H1.S1.M4 | Reglas aplicables reevaluadas: 90 completa; 91 condicionada a que la pantalla piloto elegida muestre un importe (se determina en H1.S2.M1 del propio carril, no acá); 98 no aplica (frontend puro) | La sección ya no dice "No aplican la 91 ni la 98: este repo no es Pasanaku" sin matiz | lectura de la sección 1 | HECHO |
| H1.S1.M5 | `AMB-F3`/`AMB-F5` del carril actualizadas: rutas heredadas marcadas como de `mantra-core-health`, ya no como hipótesis "del repo actual"; integración contra `dev`, no `mockup` | Las dos filas reflejan Pasanaku | lectura de la sección 5 | HECHO |
| H1.S1.M6 | Sección de instalación del estándar: carpeta `PasanakuBackend/`, no `mantra-core-health/` | La ruta es la real | `grep -n "\.claude/.*dentro de" PR6-....md` | HECHO |

## H2 — El daily de Richard referencia el repo real en los dos bloques

**CA:** El daily ya no describe el bloque B como `mantra-core-health`, y aclara que B y C comparten
repo desde esta corrección.
**DoD:** `grep` de cierre.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Cabecera del bloque B en el daily corregida, con nota de corrección fechada | Cita el repo real | `grep -n "Repo:" Richard-Daily-....md` | HECHO |
| H2.S1.M2 | Línea "Otro repo, otras reglas" del bloque C corregida: ya no dice que B es `mantra-core-health` | La línea refleja que ambos son Pasanaku | lectura de la línea | HECHO |

## H3 — Los rastros de "bloque B = mantra-core-health" en los bloques C se corrigen

**CA:** `PR11` (Richard) y `PR15` (Pablo) ya no afirman que el bloque B de su propio carril es de
otro repo, porque dejó de serlo.
**DoD:** `grep` de cierre en los dos archivos.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Línea 7 y línea ~44 de `PR11` corregidas | Ya no dicen "es de mantra-core-health" | `grep -n "mantra-core-health" PR11-....md` → vacío | HECHO |
| H3.S1.M2 | Línea 7 y línea ~49 de `PR15` corregidas (esto es lo que Pablo señaló como faltante) | Ya no dicen "es de mantra-core-health" | `grep -n "mantra-core-health" PR15-....md` → vacío | HECHO |

## H4 — El daily del equipo refleja que Richard también quedó retargeteado

**CA:** La nota agregada en la sesión anterior (que decía "solo la fila de Pablo") ahora incluye a
Richard, y la fila de Richard en la tabla del bloque B lo indica.
**DoD:** lectura de la nota y de la fila.
**Estado:** HECHO

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Nota de corrección del bloque B ampliada a Richard | Menciona a Pablo y a Richard | lectura de la nota bajo "Bloque B" | HECHO |
| H4.S1.M2 | Fila de Richard en la tabla del bloque B marcada como retargeteada | La fila lo indica | lectura de la fila | HECHO |

## H5 — Verificación

**CA:** Validadores del repo en verde; cero referencias operativas a `mantra-core-health`/`mockup`
en los archivos de Richard y en los dos rastros de `PR15`.
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
| `PR7`–`PR9` y sus bloques C siguen con el mismo patrón sin corregir | Quien los lea puede confundirse igual que con `PR6`/`PR10` | Se registra como hallazgo en el reporte, igual que la vez anterior |
