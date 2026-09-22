# PR8 — Diálogo, host de estados y borrador — cierre del carril

> **AVANCE: 13 / 26 — 50 %** (`microtareas HECHO / total`, regla 40: avance real, no estimado).
> Partía de 8/26 (30,8 %) al abrir esta sesión de continuación. `A MEDIAS` NO cuenta como hecha —
> hay además 6 microtareas `A MEDIAS` con progreso real (código escrito y, en algunos casos,
> typecheck limpio) que no llegan a cerrar por un bloqueo de entorno genuino, no por pereza.

- Fecha de esta sesión: 2026-09-22 (continuación, mismo turno noche 2026-09-21)
- Repo: `PabloArauzCaballero/PasanakuBackend` · rama base `dev`
- Rama de trabajo: `leo/frontend/dialogo-estados` — **esta sesión SÍ tuvo `git` real** contra un
  worktree dedicado (`PasanakuBackend-pr8-leo`), a diferencia de la sesión anterior (que solo pudo
  publicar vía GitHub Contents API). Se agregaron commits reales, con `yarn`/`ng`/`vitest`
  corridos contra el árbol de trabajo.
- PR abierto (no mergeado, por instrucción explícita del dueño del repo):
  https://github.com/PabloArauzCaballero/PasanakuBackend/pull/3
- Peldaño de evidencia alcanzado (regla 30): **`TESTED` real** para `dialogo.ts` y
  `estado-de-pantalla.ts` (23 tests propios corridos y en verde, salida literal pegada en
  `evidencia/h3-h2-ui-tests.md`); **`WRITTEN` + typecheck limpio confirmado** (no `RUNS`) para
  `ficha-de-cobro.ts`/`ficha-de-factura.ts` y sus specs, bloqueados por un hallazgo de entorno
  ajeno a este carril (ver §Bloqueos).

## 1. Qué se hizo en esta sesión de continuación (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Cerrado del todo: `git status --short` corrido de verdad (la sesión anterior no pudo) | `git status --short` | limpio antes de empezar a editar; ver `evidencia/` |
| H2.S1.M1 | Host con plantillas de contexto tipado (`<ng-template #plantillaVacio let-motivo>` / `#plantillaError let-error>`), opcionales, sin romper a los 11 consumidores reales | `yarn workspace @aportaya/ui test:front` | 16/17 archivos en verde (el 1 rojo es preexistente, ajeno) — `evidencia/h3-h2-ui-tests.md` |
| H2.S1.M2 | `trazaId` (ya existía) confirmado con test explícito presente/ausente; acción de siguiente paso del vacío vía plantilla, probada; "obsoleto" confirmado que NO existe en el contrato real (N/A, no pendiente) | mismo comando | mismo archivo, mismo resultado |
| H2.S1.M3 | Test que falla si el host importa `HttpClient`/`Router`/algo de sesión — sigue sin aparecer | mismo comando | PASS |
| H3.S1.M4 | Bug real encontrado y arreglado (`d.close is not a function` en jsdom, mismo patrón de fallback que ya tenía `showModal`); listener del backdrop agregado en `ngAfterViewInit`/sacado en `ngOnDestroy`; conteo antes (1 agregado) / después (1 sacado) probado; 100 aperturas/cierres sin fuga | `yarn workspace @aportaya/ui test:front` | PASS, salida pegada en `evidencia/h3-h2-ui-tests.md` |
| — | Hallazgo H-5 (bloqueo de Vitest, ya registrado por la sesión anterior) **arreglado dentro de mi carril**: `pool: 'threads'` + `fileParallelism: false` vía `vitest-base.config.ts` + `runnerConfig: true` en `angular.json`, en `packages/ui` y `apps/backoffice` | ver `evidencia/h3-h2-ui-tests.md` §0 | de 100 % de fallo a corridas mayormente en verde (no 100 % libre de flakiness, documentado) |

## 2. A medias — las cuatro respuestas, obligatorias

### H3.S2.M2 — política única de descarte: implementada y probada por unidad; el DoD pide E2E, que está bloqueado
- **Qué anda:** `intentarCerrar()` es la única puerta de cierre; botón, `Escape` (vía `preventDefault` sobre `cancel`) y clic en el fondo (listener nativo comparando `event.target`) pasan los tres por la misma guardia. `hayCambiosSinGuardar` lo calcula el consumidor (el diálogo sigue sin conocer el dominio). 13 tests unitarios reales, en verde, cubren las tres rutas con y sin borrador sucio, incluida la ruta de "Confirmar" (que nunca debe pasar por la guardia).
- **Qué no anda:** el DoD literal del encargo (H3.S2.M2, línea 240) pide `<CMD_E2E> --grep "descarte"` → PASS. Ningún E2E corrió.
- **Qué falta exactamente:** un E2E de Playwright contra un modal real con sesión abierta.
- **Dónde quedó:** `packages/ui/src/dialogo/dialogo.ts` + `dialogo.spec.ts`, commiteado en la rama. Ver bloqueo de E2E abajo (no es un bloqueo mío de resolver).

### H3.S1.M2/M3 — foco y apilamiento: el organismo ya da lo que el navegador da gratis; sin E2E que lo confirme
- **Qué anda:** `showModal()` nativo (documentado en `contrato-dialogo.md` §2) da foco inicial, trampa de foco y restauración al cerrar, según la especificación HTML. `jsdom` no implementa `showModal`, así que ningún test unitario puede observar esto de verdad — se documenta la limitación en el propio spec (`dialogo.spec.ts`, describe "foco").
- **Qué no anda:** cero observación real en un navegador. Cero capturas de apilamiento en 3 viewports.
- **Qué falta exactamente:** el mismo E2E bloqueado de abajo.
- **Dónde quedó:** sin cambios de código (no hacía falta ninguno: el comportamiento nativo ya cumple, falta solo la prueba).

### H4.S1.M3 — política de entidad cambiada: implementada (no solo declarada), test escrito y no ejecutado
- **Qué anda:** snapshot de la entidad al recibir el primer `input()`; si cambia mientras `hayCambiosSinGuardar()` es `true`, se bloquea `confirmar()` y se avisa (`role="alert"`) sin tocar el borrador. Implementado igual en los dos modales (`ficha-de-cobro.ts`, `ficha-de-factura.ts`).
- **Qué no anda:** el test del caso (`ficha-de-cobro.spec.ts`/`ficha-de-factura.spec.ts`, casos "Q-L1") no se ejecutó — `apps/backoffice` no compila como bundle completo en este entorno (ver bloqueo abajo).
- **Qué falta exactamente:** correr `test:front` de `apps/backoffice` una vez exista `clientes/angular/*`.
- **Dónde quedó:** commiteado, typecheck limpio confirmado (`evidencia/h4-fichas-typecheck.md`).

### H4.S2.M1/M2 — los dos modales migrados al diálogo reforzado: compilan, tests no corridos
- **Qué anda:** los dos modales ya usaban `<ap-dialogo>` (no hacía falta "migrarlos" en el sentido de cambiar de organismo); se cableó `[hayCambiosSinGuardar]`, se corrigió el doble envío (`if (this.enviando()) return`), y se implementó la rama de Q-L1. Cero cambio de apariencia (no se tocó ninguna plantilla visual, solo lógica + un `<p role="alert">` nuevo que solo aparece en el caso borde de Q-L1).
- **Qué no anda:** `<CMD_TEST> --grep "<modal>"` no corrió — mismo bloqueo de `apps/backoffice`.
- **Qué falta exactamente:** lo mismo que H4.S1.M3.
- **Dónde quedó:** commiteado, typecheck limpio, `ng lint` limpio (`evidencia/h4-fichas-typecheck.md`).

### H3.S2.M3 — guardar es intención: parcialmente cierto, no completo
- **Qué anda:** un error de guardado ya conservaba el borrador (comportamiento preexistente, confirmado leyendo el código: `error: () => this.enviando.set(false)` no toca `monto`/`forma`) y sigue así.
- **Qué no anda:** "muestra el error asociado a su campo cuando el servidor lo identifica" — no implementado; hoy no hay mapeo de un error de campo del backend a `errorDeMonto` o similar.
- **Qué falta exactamente:** el backend tendría que identificar el campo (no confirmado que lo haga) y el modal necesitaría un `computed` que lo lea y lo muestre en `[error]` de `ap-campo-monto`.
- **Dónde quedó:** sin tocar; es trabajo nuevo, no solo verificación.

## 3. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H3.S1.M2/M3, H3.S2.M2 (parte E2E), H4.S2.M3 | Todo E2E de foco/teclado/descarte + comparación visual sobre los dos modales reales | Confirmé que Playwright + Chromium YA están instalados en esta máquina (`npx playwright --version` → 1.63.0, `chromium-1234` presente) e intenté apuntarlo a `apps/backoffice` real. Bloqueado: `apps/backoffice` no tiene ninguna pantalla de login (hallazgo ya registrado por el carril F12, ver `apps/backoffice/e2e/tablero-y-permisos.e2e.ts`), y toda ruta con `canMatch: [requierePermiso(...)]` —incluida `contabilidad`, donde viven los dos modales— redirige en silencio a `/tablero` sin sesión abierta | Que exista una pantalla de login real, o un mecanismo de e2e para abrir sesión sin ella (no es una decisión mía: no soy dueño de pantallas de negocio ni de ese hallazgo) | Producto/otro carril (F12 ya lo documentó, no es nuevo) |
| H4.S1.M2/M3 (ejecución), H4.S2.M1/M2 (ejecución), H3.S2.M3 (ejecución) | `test:front` de `apps/backoffice` no corre NINGÚN spec, mío o ajeno | Confirmé leyendo la lista COMPLETA de errores de un build real: 0 errores en mis 4 archivos, ~30 en archivos de otras rutas por `clientes/angular/*` faltante (H-2, ya registrado) + 1 nuevo (`@aportaya/tokens/generado/tokens.css` faltante, generable con `yarn workspace @aportaya/tokens build` pero gitignored) | Generar `clientes/angular/*` (fuera de mi alcance: no encontré ningún script de generación en este checkout — no es un simple build local) | Carril que sea dueño de la generación de clientes HTTP |

> Regla 65: estos bloqueos no son "esperar a otro carril de coordinación" — son huecos de
> infraestructura pre-existentes (login inexistente, clientes HTTP no generados), ya registrados
> por otras sesiones (F12, H-2) antes de que empezara este carril. No hay un doble de tres niveles
> que sustituya "un navegador real con sesión abierta" o "el cliente HTTP generado real".

## 4. Hallazgos para el equipo (no se arreglan más allá de lo ya hecho, regla 00 §3)

| ID | Qué | Ruta | A quién le pega | Estado |
|---|---|---|---|---|
| H-5 | Pool de Vitest 4 (`forks`, por defecto) muere al arrancar en Node 24.18.1 + Windows | cualquier `test:front` de este monorepo en esta clase de entorno | Cualquier carril que necesite correr tests en esta máquina | **Arreglado dentro de mi carril** (`packages/ui`, `apps/backoffice`) con `pool: 'threads'` + `fileParallelism: false`; no se tocó ningún otro proyecto del monorepo — si `apps/web` o `packages/dominio-cliente` etc. lo sufren, necesitan el mismo arreglo aplicado ahí, fuera de mi alcance |
| H-6 (nuevo) | `@aportaya/tokens/generado/tokens.css` no existe hasta correr `yarn workspace @aportaya/tokens build` (o su script de CSS a solas); rompe cualquier bundle completo de `apps/{web,backoffice}` | `packages/ui/src/estilos.css:2` → `@import '@aportaya/tokens/tokens.css'` | Cualquier carril que necesite un build completo de `web`/`backoffice` en un checkout fresco | Registrado, no commiteado (carpeta gitignored) |
| H-2 (confirmado, no nuevo) | `clientes/angular/*` no existe en este checkout — sin script de generación local encontrado | imports en `apps/{web,backoffice}/src/app/**` | Cualquier carril que dependa de un bundle completo de `web`/`backoffice` | Sigue igual que lo registró la sesión anterior |
| H-7 (nuevo) | `packages/ui/src/monto/monto.spec.ts` ("pasa los mismos vectores que el Monto de Flutter") hace timeout a los 5000ms de forma reproducible, en todas las corridas de esta sesión — preexistente, no tocado por este carril (`monto.ts`/`monto.spec.ts` no están en mis reservas) | `packages/ui/src/monto/monto.spec.ts:21` | Cualquiera que necesite `@aportaya/ui#test:front` completamente en verde | Registrado, no investigado (fuera de mi alcance) |
| — (confirmado, no nuevo) | No hay pantalla de login en `apps/backoffice`; rutas con permiso redirigen sin sesión | `apps/backoffice/e2e/tablero-y-permisos.e2e.ts` (carril F12) | Cualquier E2E de una pantalla detrás de permiso, incluidos los dos modales de este carril | Sigue igual que lo registró F12 |

## 5. No cubierto (distinto de pendiente)

- H2.S2.M2/M3: no se escribieron tests nuevos de variantes/accesibilidad para los 7 consumidores
  reales de `estado-de-pantalla` que hoy no tienen ningún spec (`pantalla-de-expedientes.ts`,
  `pantalla-de-desempeno.ts`, `pantalla-de-liquidacion.ts`, `simulador-de-costos.ts`,
  `verificador-de-cadena.ts`, `verificador-de-certificado.ts`, `verificador-de-sorteo.ts`). No es
  `N/A` como H2.S2.M1 — esto sí se puede hacer, no se llegó por tiempo.
- H3.S2.M3: no se implementó "error de campo identificado por el servidor" (ver §2).
- `CampoMonto`, `GrupoRadio`, `Boton` siguen sin leerse en profundidad más allá de lo que ya se usó
  para escribir los specs de los dos modales.
- `apps/movil` (Flutter) fuera de alcance, como en la sesión anterior.
- Ningún E2E ni comparación visual en ningún viewport/tema — bloqueo real, documentado arriba.
- La rama `leo/frontend/dialogo-estados` no se compiló "de punta a punta" contra `apps/backoffice`
  completo en ningún momento (el bloqueo de `clientes/angular/*` lo impide estructuralmente, no
  solo para mis archivos).

## 6. Decisiones y ambigüedades — actualización

- **H2.S2.M1** — cerrada como **`VERIFICADO N/A`**: no existe ninguna vista real que hoy duplique a
  mano las ramas de `estado-de-pantalla` (confirmado con exploración exhaustiva de
  `apps/{backoffice,web}/src/app/**`, ver `contrato-view-state.md` §5). No cuenta como "hecha" en
  el conteo de 13/26 (para no inflar), pero tampoco es un pendiente real: no hay nada que migrar.
- **Q-L1** — de "declarada, no implementada" a **implementada** en ambos modales (ver §2,
  H4.S1.M3).
- **Q-L3** — sigue abierta: ningún dato nuevo sobre si algún modal evitaba la protección a
  propósito. Ahora los dos modales SÍ protegen (por diseño conservador, regla del encargo).
