# Plan — repartir el refactor frontend dentro del prompt de la noche

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (solo este) · Predecesor: `docs/trabajo/2026-09-21-reparto-produccion-ready/`
- Resultado observable: el turno noche de 2026-09-21 queda dividido en dos áreas (`Backend/` y `Frontend/`), cada una con sus cinco personas, su encargo y su daily; `python tools/check_reparto.py repartos/2026-09-21` sale 0 con la estructura nueva.
- Kill-test: `python tools/check_reparto.py repartos/2026-09-21` → si sale 1, o si `repartos/2026-09-21/PromptNoche/Frontend/` no tiene las cinco personas con su encargo, esto NO está hecho.

## Alcance

- IN: `repartos/2026-09-21/PromptNoche/**` (reorganización por área + cinco encargos y cinco dailies de frontend + daily de equipo consolidado); `tools/check_reparto.py` (nivel opcional de área + self-test); `docs/trabajo/2026-09-21-reparto-frontend-refactor/**`.
- OUT: el contenido de los cinco encargos de **backend** ya repartidos — se mueven de carpeta y se les corrigen los enlaces relativos, **no se reescribe una línea de su alcance**. `repartos/2026-09-20/**`. `.claude/rules/**` y `.claude/skills/**`. El repositorio frontend `mdavila-2001/mantra-core-health` (no está en esta máquina: nada se ejecuta contra él desde acá). `tools/check_skills_citadas.py`. `tools/sync_agents.py` y el espejo `.agents/`.
- Ambigüedades registradas: ver la sección de ambigüedades. Ninguna se resuelve acá: se arrastran a los encargos y al daily de equipo.

## H1 — El turno noche está dividido en dos áreas y el validador lo acepta

**CA:** Dado `repartos/2026-09-21/PromptNoche/`, cuando se lista, entonces hay exactamente dos carpetas de área (`Backend/`, `Frontend/`), cada una con las cinco personas, y el daily de equipo sigue colgando del turno; `python tools/check_reparto.py repartos/2026-09-21` sale 0.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21 repartos/2026-09-20` → exit 0, salida pegada en `evidencia/`.
**Estado:** HECHO

### H1.S1 — Reorganización de las carpetas y de los enlaces

**CA:** Dado el reparto movido, cuando se abre cualquier daily o encargo, entonces sus enlaces relativos resuelven a un archivo existente.
**DoD:** script que resuelve todo enlace relativo `.md` de `repartos/2026-09-21` → 0 rotos.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Crear `PromptNoche/Backend/` y mover ahí las cinco carpetas de persona existentes | Las cinco están bajo `Backend/` y ninguna quedó en la raíz del turno | `ls repartos/2026-09-21/PromptNoche` → `Backend`, `Daily-Noche-2026-09-21.md`, `Frontend` | HECHO |
| H1.S1.M2 | Corregir los enlaces relativos al daily de equipo en los diez archivos movidos | Ningún enlace `.md` roto en el área Backend | script de enlaces → `0 rotos` | HECHO |
| H1.S1.M3 | Crear `PromptNoche/Frontend/<Persona>/<Lote>.Frontend/{entregables,evidencia}` para las cinco personas | Las cinco carpetas existen con lote con punto y `.gitkeep` | `find repartos/2026-09-21/PromptNoche/Frontend -name .gitkeep -type f` → 10 líneas | HECHO |

### H1.S2 — El validador acepta el nivel de área sin dejar de exigir lo de siempre

**CA:** Dado un turno con carpetas de área, cuando corre el validador, entonces las reconoce; y dado un área con nombre inventado o una persona desconocida dentro de un área, entonces las reporta.
**DoD:** `python tools/check_reparto.py --self-test` → exit 0 con los casos nuevos incluidos.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | `check_reparto.py`: aceptar un nivel opcional `Backend`/`Frontend` entre turno y persona, conservando el área en el mensaje de error | Un árbol con área válida no reporta problemas | `python tools/check_reparto.py --self-test` → exit 0 | HECHO |
| H1.S2.M2 | Self-test: caso de área válida, área con nombre inventado y persona desconocida dentro de un área | Los tres casos aparecen en la salida del self-test | `python tools/check_reparto.py --self-test` → tres líneas nuevas con "área" | HECHO |
| H1.S2.M3 | No regresión: el reparto del 2026-09-20 (sin áreas) sigue pasando | Exit 0 | `python tools/check_reparto.py repartos/2026-09-20` → exit 0 | HECHO |

## H2 — Las cinco personas tienen encargo de frontend ejecutable

**CA:** Dado `Frontend/<Persona>/`, cuando se abre el encargo, entonces trae instalación del estándar, kill-test, alcance OUT, reservas, las tres capas con CA/DoD/Estado y la tabla de ambigüedades; y todas las skills citadas existen.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21` exit 0 y `python tools/check_skills_citadas.py` exit 0, salidas pegadas.
**Estado:** HECHO

### H2.S1 — Los cinco encargos

**CA:** Dado el prompt maestro de refactorización frontend, cuando se reparte, entonces cada fase y cada familia candidata del documento tiene dueño único, y ningún archivo tiene dos dueños.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21` → exit 0.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Richard — `PR6-SmartPresentational.Frontend`: responsabilidad, propiedad del estado y plantilla declarativa en la pantalla piloto | El encargo existe y pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` → exit 0 | HECHO |
| H2.S1.M2 | Justin — `PR7-DataTable.Frontend`: organismo tabla canónico y dos consumidores reales migrados | El encargo existe y pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` → exit 0 | HECHO |
| H2.S1.M3 | Leo — `PR8-DialogoYEstados.Frontend`: `ViewStateHost`, `ContentDialog` y contrato de borrador | El encargo existe y pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` → exit 0 | HECHO |
| H2.S1.M4 | Marcelo — `PR9-InventarioYFamilias.Frontend`: inventario con procedencia, grafo de usos y matriz de familias | El encargo existe y pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` → exit 0 | HECHO |
| H2.S1.M5 | Pablo — `PR10-CatalogoYGates.Frontend`: catálogo fiel, preview aislado, gates visual/a11y y cierre | El encargo existe y pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` → exit 0 | HECHO |

### H2.S2 — Los cinco dailies personales del área frontend

**CA:** Dado cada daily, cuando se abre, entonces su primera línea es el avance `0 / <total>` con el total que declara su encargo.
**DoD:** los cinco archivos existen y su primera línea de cita trae `AVANCE:`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Daily de Richard (frontend) | Existe y su primera línea trae el avance | `head -3` del archivo → línea `AVANCE:` | HECHO |
| H2.S2.M2 | Daily de Justin (frontend) | Existe y su primera línea trae el avance | `head -3` del archivo → línea `AVANCE:` | HECHO |
| H2.S2.M3 | Daily de Leo (frontend) | Existe y su primera línea trae el avance | `head -3` del archivo → línea `AVANCE:` | HECHO |
| H2.S2.M4 | Daily de Marcelo (frontend) | Existe y su primera línea trae el avance | `head -3` del archivo → línea `AVANCE:` | HECHO |
| H2.S2.M5 | Daily de Pablo (frontend) | Existe y su primera línea trae el avance | `head -3` del archivo → línea `AVANCE:` | HECHO |

### H2.S3 — Los gates del reparto en verde

**CA:** Dado el reparto completo, cuando corren los dos validadores, entonces salen 0 los dos.
**DoD:** las dos salidas pegadas en `evidencia/`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S3.M1 | Estructura y contenido mínimo del reparto | Exit 0 | `python tools/check_reparto.py repartos/2026-09-21` | HECHO |
| H2.S3.M2 | Toda skill citada existe en `.claude/skills/` | Exit 0 | `python tools/check_skills_citadas.py` | HECHO |

## H3 — El daily del turno consolida las dos áreas sin mentir el avance

**CA:** Dado el daily de equipo, cuando alguien que no vio la sesión lo lee, entonces sabe quién tiene qué en cada área, en qué orden, qué archivos están reservados y qué ambigüedades se arrastran.
**DoD:** el total del encabezado es la suma de las microtareas declaradas por los diez encargos, verificada contando las filas de microtarea.
**Estado:** HECHO

### H3.S1 — Secciones nuevas del daily de equipo

**CA:** Dado el daily, cuando se busca "Frontend", entonces aparece en la tabla de personas, en dependencias, en reservas, en ambigüedades y en el cierre.
**DoD:** recuento de microtareas por encargo → coincide con el total del encabezado.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Sección 1: dos bloques (Backend / Frontend) con hitos, subtareas y microtareas por persona, y el total recalculado | El total del encabezado es igual a la suma de las diez filas | recuento de filas de microtarea en los diez encargos | HECHO |
| H3.S1.M2 | Sección 3: orden de dependencia del área frontend y qué hace cada uno mientras espera (regla 65) | Toda espera declarada tiene su doble o su trabajo alternativo | revisión: ninguna fila sin columna "mientras tanto" | HECHO |
| H3.S1.M3 | Sección 4: reservas de archivos del área frontend, sin solapamiento con backend ni entre personas | Ningún archivo aparece en dos filas | revisión de la tabla de reservas | HECHO |
| H3.S1.M4 | Sección 5: ambigüedades `AMB-F1` a `AMB-F7` con supuesto y quién la cierra | Las siete están, ninguna marcada como resuelta | búsqueda de `AMB-F` en el daily → 7 o más | HECHO |
| H3.S1.M5 | Sección 6: tabla de cierre con las diez filas (cinco por área) y sus dailies enlazados | Diez filas, diez enlaces que resuelven | script de enlaces → `0 rotos` | HECHO |

## H4 — El trabajo queda reportado

**CA:** Dado `REPORTE.md`, cuando se lee, entonces la primera línea es el avance calculado y están las tres secciones obligatorias.
**DoD:** el reporte escrito con las tres secciones, avance calculado y evidencia enlazada.
**Estado:** HECHO

### H4.S1 — Reporte del reparto

**CA:** Dado el reporte, cuando se busca "A medias" y "Pendiente", entonces existen aunque digan "ninguna".
**DoD:** el archivo existe y trae los tres encabezados de sección.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H4.S1.M1 | `REPORTE.md` con avance en la primera línea y las tres secciones | Los tres encabezados existen | búsqueda de `## Completado`, `## A medias`, `## Pendiente` → 3 | HECHO |

## Ambigüedades registradas

| ID | Ambigüedad | Supuesto tomado | A quién confirmárselo |
|---|---|---|---|
| AMB-F1 | El turno noche ya tenía 213 microtareas de backend. Sumar el frontend deja a cada persona con dos carriles, y la regla 70.1 permite **un** trabajo activo por vez | Se reparte el frontend **completo y ordenado por dependencia**, sin recortar el backend. El backend es el bloque A y el frontend el bloque B; lo que no entre en el turno va `A MEDIAS` con las cuatro respuestas. **Recortar es decisión de coordinación** | Coordinación (Pablo) |
| AMB-F2 | `mdavila-2001/mantra-core-health` no es un repo de Pasanaku | Las reglas 91 (dinero) y 98 (microservicios) no aplican; la 90.2 sí, leyendo "dato financiero" como "dato clínico e identificatorio" | Coordinación / cumplimiento |
| AMB-F2 (actualización 2026-09-21) | **Resuelta solo para el carril de Pablo (`PR10-CatalogoYGates.Frontend`):** Pablo (Coordinación) confirmó en sesión que ese bloque también es de Pasanaku, no de `mantra-core-health`. Corregido en `PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md` y en `Pablo-Daily-Noche-2026-09-21.md` (Frontend) — ver `docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku/`. **Sigue abierta, sin corregir, para `PR6` (Richard), `PR7` (Justin), `PR8` (Leo) y `PR9` (Marcelo)**: sus encargos todavía apuntan a `mantra-core-health` | Los cuatro carriles restantes, si alguien los ejecuta tal cual están hoy | Coordinación (Pablo) — pendiente decidir si se corrigen igual |
| AMB-F3 | Las rutas del documento antecedente (`component-stock.ts`, `core/mock/faker/props.ts`, `scripts/generate-component-index.mjs`, `core/view-state/view-state.types.ts`, `DataTable`, `DirectoryPage`, `ContentDialog`) | Son **hipótesis heredadas**, no hechos verificados: cada encargo las confirma o las refuta en su primera microtarea, antes de usarlas | El propio baseline de cada persona |
| AMB-F4 | El SHA `5a0776c66b005ad4d2d6722321e933cd7adea621` del documento original | Referencia histórica. La base es `mockup` en el SHA que cada uno registre al empezar. **No se resetea nada** | — |
| AMB-F5 | A qué rama se integra el trabajo (el documento dice que la base funcional y visual es `mockup`, no `dev`) | PR contra `mockup`; nadie toca `main` ni `dev` | `DECISION_REQUIRED` — dueño del repo frontend |
| AMB-F6 | Coexisten Vitest, Playwright y Cypress | El runner de cada capa se registra en el baseline y se usa el que ya esté cableado. No se instala nada nuevo | El propio baseline (Pablo consolida) |
| AMB-F7 | Cuál es la pantalla piloto y cuáles los dos consumidores que se migran | Se fijan en la primera hora y se publican en el daily de equipo, antes de que nadie escriba código. Un archivo no puede ser piloto de Richard y consumidor de Justin a la vez | Coordinación (Pablo), dentro de la primera hora |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Tocar `check_reparto.py` rompe la validación del reparto del 2026-09-20 | El gate del equipo queda rojo por una razón ajena al reparto | H1.S2.M3 corre el validador sobre el 2026-09-20 antes de cerrar |
| Mover carpetas rompe enlaces relativos en silencio | Encargos que enlazan a la nada; nadie lo nota al leerlos | H1.S1.M2 resuelve todos los enlaces con un script, no a ojo |
| Escribir el encargo con rutas del repo frontend que no verifiqué | Regla 00: convertir probabilidad en hecho | Toda ruta heredada va marcada como hipótesis y se confirma en la primera microtarea de cada encargo (AMB-F3) |
| Dos personas sobre el mismo componente del frontend | Defecto del reparto, no accidente | Tabla de reservas del daily de equipo + AMB-F7 resuelta en la primera hora |
