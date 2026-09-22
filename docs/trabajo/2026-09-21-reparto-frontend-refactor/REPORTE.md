# Reporte — repartir el refactor frontend dentro del prompt de la noche

> **AVANCE: 24 / 24 — 100 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` (sin commit; los cambios quedan en el árbol de trabajo)
- Peldaño de evidencia alcanzado: **`REGRESSION_VERIFIED`** para el área tocada (los dos validadores del repo, el self-test del que modifiqué, la no regresión sobre el reparto anterior y el chequeo de enlaces, todos con exit code pegado).
- Alcance: `repartos/2026-09-21/PromptNoche/**`, `repartos/README.md`, `tools/check_reparto.py`.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | `PromptNoche/` dividido en `Backend/` y `Frontend/`; las cinco carpetas de persona del backend movidas sin tocar su contenido | `ls repartos/2026-09-21/PromptNoche` | PASS — `Backend`, `Daily-Noche-2026-09-21.md`, `Frontend` |
| H1.S1.M2 | Enlaces relativos corregidos en los diez archivos movidos | `python evidencia/check_enlaces.py repartos/2026-09-21` | PASS — 67 enlaces revisados, **0 rotos** (`evidencia/enlaces-relativos.txt`) |
| H1.S1.M3 | Cinco lotes de frontend creados con `entregables/` y `evidencia/` | `find … -name .gitkeep -type f` | PASS — 10 archivos |
| H1.S2.M1 | `check_reparto.py` acepta el nivel opcional de área conservándola en la ruta del mensaje | `python tools/check_reparto.py --self-test` | PASS — 34 PASS, 0 FAIL (`evidencia/check_reparto-self-test.txt`) |
| H1.S2.M2 | Cuatro casos nuevos en el self-test: área válida, área con nombre inventado, persona desconocida dentro de un área, área vacía | mismo comando | PASS — los cuatro casos aparecen nombrados en la salida |
| H1.S2.M3 | No regresión: el reparto del 2026-09-20, sin áreas, sigue pasando | `python tools/check_reparto.py repartos/2026-09-20` | PASS — exit 0 (`evidencia/check_reparto-repartos.txt`) |
| H2.S1.M1 | Encargo de Richard — `PR6-SmartPresentational.Frontend` (4 hitos · 7 subtareas · 24 microtareas) | `python tools/check_reparto.py repartos/2026-09-21` | PASS — exit 0 |
| H2.S1.M2 | Encargo de Justin — `PR7-DataTable.Frontend` (4 · 8 · 27) | mismo comando | PASS — exit 0 |
| H2.S1.M3 | Encargo de Leo — `PR8-DialogoYEstados.Frontend` (4 · 8 · 26) | mismo comando | PASS — exit 0 |
| H2.S1.M4 | Encargo de Marcelo — `PR9-InventarioYFamilias.Frontend` (5 · 9 · 31) | mismo comando | PASS — exit 0 |
| H2.S1.M5 | Encargo de Pablo — `PR10-CatalogoYGates.Frontend` (5 · 11 · 38) | mismo comando | PASS — exit 0 |
| H2.S2.M1–M5 | Los cinco dailies personales del área frontend, con el avance en la primera línea y el total de su encargo | generador con `assert` de que los hitos suman el total declarado | PASS — cinco archivos, cinco asserts en verde |
| H2.S3.M1 | Estructura y contenido mínimo del reparto completo | `python tools/check_reparto.py repartos/2026-09-21` | PASS — exit 0 |
| H2.S3.M2 | Toda skill citada existe en `.claude/skills/` | `python tools/check_skills_citadas.py` | PASS — 80 skills distintas citadas, **0 inexistentes** (`evidencia/check_skills_citadas.txt`) |
| H3.S1.M1 | Daily de equipo con los dos bloques y el total recalculado | recuento de filas de microtarea | PASS — backend 213 + frontend 146 = **359**, igual al encabezado (`evidencia/conteo-microtareas.txt`) |
| H3.S1.M2 | Tabla de dependencias del área frontend: ocho filas, todas con columna "qué hace mientras tanto" | revisión | PASS — ninguna espera sin su doble o su trabajo alternativo |
| H3.S1.M3 | Reservas de archivos del área frontend, sin solapamiento con backend ni entre personas | revisión | PASS — más la tabla de reservas de pantallas que se publica en la primera hora |
| H3.S1.M4 | Ambigüedades `AMB-F1` … `AMB-F7` más `Q-frontend-borrador`, con supuesto y dueño | revisión | PASS — ocho filas, ninguna marcada como resuelta |
| H3.S1.M5 | Tabla de cierre con las diez filas y sus dailies enlazados | chequeo de enlaces | PASS — 0 rotos |
| H4.S1.M1 | Este reporte | — | PASS |

**Cómo quedó el reparto:**

| Persona | Backend | Frontend | Total |
|---|---:|---:|---:|
| Richard | 28 | 24 — pantalla piloto: smart/presentational y propiedad del estado | 52 |
| Justin | 42 | 27 — organismo tabla y dos consumidores reales migrados | 69 |
| Leo | 49 | 26 — contrato de estado, host de estados, diálogo y borrador | 75 |
| Marcelo | 40 | 31 — inventario, grafo de usos, matriz de familias y retirada | 71 |
| Pablo | 54 | 38 — catálogo fiel, preview aislado, gates y cierre | 92 |
| | **213** | **146** | **359** |

## A medias

Ninguna.

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| AMB-F1 — recorte del alcance del turno | `DECISION_REQUIRED` | El turno queda con 359 microtareas entre cinco personas. El reparto está escrito completo y ordenado por dependencia, como manda la regla del repo, pero **decidir qué se recorta es de coordinación**. Mientras no se decida, rige el supuesto: bloque A (backend) primero, bloque B (frontend) después, y lo que no cierre va `A MEDIAS`. |
| AMB-F5 — a qué rama se integra el frontend | `DECISION_REQUIRED` | Dueño del repo `mantra-core-health`. Supuesto aplicado: PR contra `mockup`; `main` y `dev` no se tocan. |
| Q-frontend-borrador | `DECISION_REQUIRED` | Producto: qué pasa con un borrador si la entidad cambia mientras se edita. Leo implementa la rama conservadora y la declara. |
| El commit de estos cambios | `TODO` | Nadie lo pidió y estamos en `main`. Los archivos quedan en el árbol de trabajo. |

## Evidencia

```text
$ python tools/check_reparto.py --self-test
  ... 34 casos ...
check_reparto self-test: 34 PASS, 0 FAIL
exit=0

$ python tools/check_reparto.py repartos/2026-09-21 repartos/2026-09-20
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
check_reparto: OK, 2026-09-20 cumple la estructura obligatoria
exit=0

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 80 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)
exit=0

$ python evidencia/check_enlaces.py repartos/2026-09-21
enlaces relativos revisados: 67
rotos: 0
exit=0

$ conteo de filas de microtarea por encargo
 42  Backend/Justin/PR2-NucleoFinanciero.Servicio/IdempotenciaMfaYDobleAprobacionDeRetiro.md
 49  Backend/Leo/PR3-Plataforma.Infra/OutboxQuePublicaYGuardasComunes.md
 40  Backend/Marcelo/PR4-Seguridad.Transversal/InventarioIdorLedgerBaseYCodigoMuerto.md
 54  Backend/Pablo/PR5-Ci.Operacion/CiRealSupplyChainBordeYCierre.md
 28  Backend/Richard/PR1-Identidad.Servicio/StepUpMfaJwtYArranqueSeguro.md
 27  Frontend/Justin/PR7-DataTable.Frontend/TablaCanonicaYDosConsumidores.md
 26  Frontend/Leo/PR8-DialogoYEstados.Frontend/DialogoHostDeEstadosYBorrador.md
 31  Frontend/Marcelo/PR9-InventarioYFamilias.Frontend/InventarioGrafoDeUsosYFamilias.md
 38  Frontend/Pablo/PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md
 24  Frontend/Richard/PR6-SmartPresentational.Frontend/QuienDecideYQuienDibuja.md
--- totales ---
backend  213
frontend 146
```

Archivos: [`evidencia/`](./evidencia/) — `check_reparto-self-test.txt`, `check_reparto-repartos.txt`,
`check_skills_citadas.txt`, `enlaces-relativos.txt`, `conteo-microtareas.txt` y el script
`check_enlaces.py` con el que se produjo el cuarto.

## No cubierto

Esto es lo que se hizo pero **no** se verificó, y lo que ningún script puede verificar:

1. **La calidad del contenido de los cinco encargos de frontend.** Los validadores comprueban que
   las piezas estén (instalación del estándar, kill-test, alcance OUT, tres capas con CA/DoD/Estado,
   ambigüedades, skills existentes). **Un encargo con las piezas presentes y mal escritas pasa el
   chequeo**, como dice el propio `README` de repartos. Eso lo tiene que revisar una persona.
2. **Nada se ejecutó contra el repo frontend.** `mdavila-2001/mantra-core-health` no está en esta
   máquina y no se clonó. Ninguna ruta, versión, script de `package.json` ni componente que aparece
   en los encargos fue verificado contra el código: **todos vienen del documento que pegó el usuario
   y están marcados como hipótesis** (AMB-F3), con la primera microtarea de cada carril dedicada a
   confirmarlos o refutarlos. Este reporte **no** afirma que ese repo exista con esa forma.
3. **El equilibrio de la carga no se validó contra la capacidad real del turno.** 359 microtareas
   entre cinco personas es un número, no una estimación de esfuerzo: el reparto no estima horas
   porque no tiene con qué (ver AMB-F1).
4. **El espejo `.agents/` no se regeneró.** No se tocó ninguna skill ni ninguna regla, así que no
   debería haber deriva; pero `python tools/sync_agents.py --check` **no se corrió**.
5. **Nada se commiteó ni se subió.** No se pidió.

## Desvíos del plan

1. **Se tocó `repartos/README.md`, que el plan no listaba en IN.** Motivo: el plan cambió la
   estructura obligatoria del reparto, y dejar el README describiendo la estructura vieja lo
   convertía en documentación que miente. Se agregó una sección de turnos divididos por área; no se
   modificó nada de lo que ya decía.
2. **El self-test del validador quedó con cuatro casos nuevos, no tres.** El plan (H1.S2.M2) pedía
   área válida, área inventada y persona desconocida dentro de un área; se agregó además el caso del
   área sin personas adentro, que el nuevo código podía dejar pasar en silencio.
3. **Los documentos largos se escribieron con la herramienta de escritura en vez de por consola.**
   La consola de esta sesión falla al parsear documentos con bloques de código anidados. No cambia
   el resultado; queda anotado porque explica por qué no hay salidas de consola de esos pasos.

## Riesgos residuales

| Riesgo | Impacto | Estado |
|---|---|---|
| Los encargos nombran rutas y comandos del repo frontend que nadie verificó | Alguien los toma como hechos y trabaja sobre una ruta que no existe | **Mitigado, no eliminado**: cada encargo abre con una microtarea de confirmación y marca las rutas como hipótesis. Depende de que se lea la advertencia |
| Cinco personas con dos carriles el mismo turno | Dos trabajos en `EN CURSO` a la vez, contra la regla 70.1 | **Abierto** (AMB-F1): el daily declara el orden de bloques, pero la decisión de recortar es de coordinación |
| Richard, Justin y Leo pueden reservar la misma pantalla | Dos personas escribiendo el mismo archivo | **Mitigado**: la tabla de reservas de §4 se publica en la primera hora y el primero se la queda. Si nadie la completa, el riesgo vuelve |
| Cambiar `check_reparto.py` afecta a cualquier reparto futuro | Un turno se valida mal | **Mitigado**: self-test en verde con 34 casos y no regresión sobre el reparto del 2026-09-20 |

## Decisiones y ambigüedades

| ID | Qué se decidió sin confirmación | Supuesto tomado | A quién confirmárselo |
|---|---|---|---|
| D-01 | Cómo repartir el frontend entre los cinco | Cada persona toma el carril frontend que se parece a su carril backend: Richard responsabilidad y estado, Justin la tabla, Leo las piezas compartidas, Marcelo el inventario, Pablo el catálogo y los gates | Coordinación |
| D-02 | Dónde vive el nivel de área | Dentro del turno, con el daily de equipo **único** a nivel de turno. La alternativa —dos dailies de equipo— se descartó porque el avance del turno dejaría de ser un solo número | Coordinación |
| AMB-F1 | Que no se recorta el backend | El reparto se escribe completo; lo que no entre va `A MEDIAS` | Coordinación (Pablo) |
| AMB-F2 | Que `mantra-core-health` no es Pasanaku | No rigen la regla 91 (dinero) ni la 98 (microservicios); la 90.2 se lee como dato clínico e identificatorio | Coordinación / cumplimiento |
| AMB-F3 | Que las rutas del documento antecedente son hipótesis | Ninguna se usa hasta confirmarla con archivo y línea | El baseline de cada persona |
| AMB-F4 | Que el SHA `5a0776c6…` es referencia histórica | No se resetea nada; la base es `mockup` en el SHA que registre cada uno | — |
| AMB-F5 | Contra qué rama se abren los PR | `mockup`; `main` y `dev` no se tocan | Dueño del repo frontend |
| AMB-F6 | Qué runner se usa, con Vitest, Playwright y Cypress coexistiendo | El que ya esté cableado; no se instala nada nuevo | Pablo, primera hora |
| AMB-F7 | Quién se queda con cada pantalla | El primero que la publica en el daily §4 | Richard, Justin y Leo, primera hora |
