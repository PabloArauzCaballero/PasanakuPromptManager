# Contrato del diálogo — releído contra el código real (H3.S1.M1)

> **Peldaño:** `DISCOVERED`. Fuente: `packages/ui/src/dialogo/dialogo.ts` (repo `PasanakuBackend`,
> SHA `a23bcb117effe7ce66d069a97ebd2c25c8390306`). No existe `dialogo.spec.ts` hoy (confirmado:
> `Read` sobre esa ruta devuelve "no existe" — cero cobertura de test sobre el organismo actual).

## 1. Qué es hoy (no lo que debería ser)

`Dialogo` (selector `ap-dialogo`) es un envoltorio de `<dialog>` nativo, especializado en
**confirmación de una sola acción**, no un diálogo de contenido genérico:

- **Título**: `titulo = input.required<string>()` (línea 34) — string, no proyectado.
- **Contenido**: `<ng-content />` (línea 16) — proyectado, sin restricción de forma.
- **Acciones**: **no proyectadas**. Son dos botones fijos generados por el propio componente
  (líneas 18-19): cancelar (`textoDeCancelar`, default `'Cancelar'`) y confirmar
  (`textoDeConfirmar`, requerido). Cardinalidad fija: siempre exactamente dos, nunca cero, nunca
  más de dos, nunca un footer distinto (por ejemplo, tres acciones o ninguna).
- **Apertura**: `abierto = model(false)` (línea 39, two-way).
- **Semántica accesible del título**: `aria-labelledby` apunta al `id` del `<h2>` (línea 14) — el
  diálogo **tiene** nombre accesible.

## 2. Foco — lo que el navegador ya da gratis, y lo que falta

`showModal()` nativo (línea 49) da, sin código adicional: foco inicial dentro del diálogo (el
navegador enfoca el primer elemento enfocable, o el propio `<dialog>` si no hay ninguno), trampa de
foco (Tab no sale del `<dialog>` mientras está `open` con `showModal`), y en la mayoría de
navegadores, restauración del foco al elemento que invocó `showModal()` al cerrar. **Esto no está
verificado con un E2E real en este repo** (no hay `dialogo.spec.ts`; no se corrió Playwright en
esta sesión — bloqueo de entorno, ver `REPORTE.md`). Es un supuesto respaldado por la especificación
HTML del elemento `dialog`, no por una prueba propia.

## 3. Las tres rutas de cierre — hoy NO son la misma política (hallazgo central de H3)

| Ruta | Qué pasa hoy | Evidencia |
|---|---|---|
| Botón "Cancelar" | Llama `cerrar()` (línea 55-58): `abierto.set(false)` + `cancelar.emit()`. | `dialogo.ts:18,55-58` |
| `Escape` | El navegador dispara el evento nativo `cancel` sobre `<dialog>`, que **por defecto cierra el diálogo** (el UA lo cierra solo); el handler `(cancel)="cancelar.emit()"` (línea 14) solo emite el output, **no llama a `cerrar()`** — es el cierre nativo el que dispara luego `(close)="abierto.set(false)"` (línea 14). | `dialogo.ts:14` |
| Clic en el fondo (`::backdrop`) | **No hay ningún handler.** `showModal()` con `<dialog>` no cierra por clic en el backdrop por defecto (a diferencia de otros patrones de modal); no hay `(click)` en la propia etiqueta `<dialog>` que compare `event.target`. | `dialogo.ts:14-21`, ausencia confirmada por lectura completa del archivo |

**Conclusión (kill-test del encargo, aplicado hoy):** el clic en el fondo directamente **no cierra
el diálogo** en absoluto (ni protegido ni sin proteger — no hace nada), y **no existe ninguna
política de descarte de borrador sucio** en ninguna de las tres rutas: no hay `dirty`, no hay
`beforeClose`, no hay confirmación. Botón y Escape terminan ambos en `cancelar.emit()` (por rutas
distintas), pero **ninguno de los dos pregunta si hay cambios sin guardar**. Migrar los dos modales
elegidos (H3.S2.M1) sobre este organismo *tal cual está* dejaría el kill-test del encargo en rojo:
abrir con formulario sucio y cerrar por Escape perdería lo cargado, igual que por botón — es
"igual" pero porque **ninguna ruta protege**, no porque las tres compartan una protección real.

## 4. Qué requiere el contrato pedido (H3.S1.M1) — brecha a implementar, no implementada en esta sesión

1. Una única función de guardia (`onIntentoDeCierre` o equivalente) que las tres rutas —botón,
   `cancel` nativo (Escape), clic en `::backdrop`— consulten antes de cerrar, parametrizada por un
   predicado de "hay cambios sin guardar" que **el consumidor** provee (el diálogo no conoce el
   dominio del formulario, regla de alcance: "el diálogo no valida reglas de negocio").
2. Clic en backdrop: agregar `(click)` sobre `<dialog>` comparando `event.target === caja().nativeElement`
   (el backdrop es parte del propio elemento `dialog` en la implementación de los navegadores) y
   enrutarlo por la misma guardia.
3. Acciones proyectadas en vez de fijas, con cardinalidad explícita (mínimo una acción primaria;
   cero o más secundarias) para servir a los dos modales reales elegidos, que hoy usan el par fijo
   confirmar/cancelar y **no necesitan** una API más amplia todavía — **Q-L2 abierta**: los dos
   modales candidatos (`ficha-de-cobro.ts`, `ficha-de-factura.ts`) consumen exactamente el patrón
   actual (un confirmar + un cancelar), así que la proyección de contenido actual **alcanza** para
   ellos; ampliar la cardinalidad de acciones más allá de eso no tiene un consumidor real todavía
   y se registra como decisión diferida, no como trabajo de este carril (regla 00 §3.2: no se
   generaliza sin un segundo consumidor real que lo pida).

## 5. No cubierto (al cerrar la sesión que escribió este contrato)

- Ningún E2E de foco/teclado/descarte corrido en esa sesión (bloqueo de entorno: sin `git` para
  ramas/PR reales y sin verificación en navegador — ver `REPORTE.md`).
- Apilamiento en tres viewports: no capturado (no hay build/servidor de desarrollo corrido en esa
  sesión).
- Limpieza de listeners al destruir (H3.S1.M4): no medida; `effect()` de Angular se limpia solo al
  destruir el componente por el framework, pero el listener manual de backdrop propuesto en §4.2
  **no existe todavía**, así que no hay nada que medir en el código actual más allá de lo que
  Angular ya gestiona.

## 6. Sesión de continuación (2026-09-22) — H3.S2.M2 implementado y verificado en verde

Esta sesión SÍ tuvo `git` real contra `PasanakuBackend` (worktree dedicado, rama
`leo/frontend/dialogo-estados`). Se implementó exactamente la brecha del §3-4: `dialogo.ts` ahora
tiene:

1. **Una única puerta de cierre**, `intentarCerrar()`. Botón "Cancelar" la llama directo; `Escape`
   pasa por `onCancelNativo()` que hace `event.preventDefault()` sobre el `cancel` nativo (frena el
   cierre automático del navegador) y llama a la misma puerta; el clic en el fondo se detecta
   comparando `event.target === <dialog>` (nunca los hijos) con un listener nativo agregado en
   `ngAfterViewInit` y sacado en `ngOnDestroy` — **no** con `(click)` en la plantilla, porque
   `@angular-eslint/template/click-events-have-key-events` e `interactive-supports-focus` lo
   marcan como error real de accesibilidad (el backdrop no tiene equivalente de teclado propio, y
   no lo necesita — `Escape` ya cierra por la otra ruta). El listener manual es también lo que le
   da a H3.S1.M4 algo real que limpiar (antes no había nada que hacer `removeEventListener` de).
2. `hayCambiosSinGuardar = input(false)` — el diálogo sigue sin conocer el dominio; el consumidor
   calcula el borrador sucio y se lo pasa. Si es `true`, `intentarCerrar()` pide confirmación
   (`window.confirm`, aislado en `confirmarDescarte()` para mockear en tests) antes de cerrar; si
   se rechaza, el diálogo queda exactamente como estaba (nada se pierde, nada se cierra a medias).
3. El botón "Confirmar" **nunca** pasa por esta guardia — guardar es una intención explícita, no
   un cierre (ver `contrato-formulario.md`).

**Kill-test del encargo, verificado en verde, no solo razonado:** `packages/ui/src/dialogo/dialogo.spec.ts`
(13 casos) corre contra el organismo real vía `yarn workspace @aportaya/ui test:front` (con el
arreglo de entorno del §7) y las tres rutas —botón, `Escape`, fondo— quedan probadas compartiendo
la misma guardia, con y sin borrador sucio, incluidas 100 aperturas/cierres seguidas sin fuga
(H3.S1.M4) y un caso explícito de `removeEventListener` al destruir. Salida real:
`evidencia/h3-dialogo-tests.md` (11→13 tests, todos en verde).

**Bug real encontrado y corregido en el camino (no estaba en el contrato original):** el `effect()`
que sincroniza `abierto()` con el `<dialog>` llamaba a `d.close()` sin verificar que el método
existiera; en el jsdom de este entorno `close()` no está implementado (igual que `showModal()`,
que sí tenía su propio fallback) y el primer intento de cerrar tiraba `TypeError: d.close is not a
function`. Se agregó el mismo patrón de fallback (`removeAttribute('open')`) que ya existía para
`showModal()`. Sin los tests reales de esta sesión, este bug seguía sin detectarse.

**Sigue sin cubrirse (honesto, no fabricado):** foco inicial real, trampa de `Tab` y restauración
de foco al elemento que abrió — todo eso requiere un navegador real. Se intentó Playwright
(Chromium ya está instalado en esta máquina) contra las rutas reales de `contabilidad/cobros` y
`contabilidad/compras`, pero **está genuinamente bloqueado**: `apps/backoffice` no tiene ninguna
pantalla de login (hallazgo ya registrado por el carril F12,
`apps/backoffice/e2e/tablero-y-permisos.e2e.ts`) y toda ruta con `canMatch: [requierePermiso(...)]`
—incluida `contabilidad`— redirige en silencio a `/tablero` sin sesión. No es mío de resolver
(no soy dueño de una pantalla de login que no existe), así que queda `BLOQUEADO`, no inventado.
Apilamiento en 3 viewports y comparación visual 2 temas: mismo bloqueo (dependen del mismo E2E).
