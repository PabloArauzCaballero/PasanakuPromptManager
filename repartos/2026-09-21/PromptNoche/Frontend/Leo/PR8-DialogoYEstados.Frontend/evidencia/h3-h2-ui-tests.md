# H3.S2.M2 / H3.S1.M4 / H2.S1 — tests reales de `@aportaya/ui`, sesión de continuación (2026-09-22)

> Peldaño: `TESTED` (regla 30) para `dialogo.ts` y `estado-de-pantalla.ts` — no razonado, corrido.
> Repo: worktree dedicado `PasanakuBackend-pr8-leo`, rama `leo/frontend/dialogo-estados`.

## 0. Bloqueo de entorno encontrado y arreglado (H-5, ya registrado por la sesión anterior)

`yarn workspace @aportaya/ui test:front` fallaba el 100% de las veces ANTES de este arreglo, con:

```
node:events:487
      throw er; // Unhandled 'error' event
      ^
Error: Worker exited unexpectedly
    at ChildProcess.emitUnexpectedExit (.../vitest/dist/chunks/cli-api.CnMVyzaz.js:3090:33)
Node.js v24.18.1
[exited with code 0]
```

Confirmado: no era un problema de ningún spec (ni de este carril ni de los preexistentes) — el
proceso hijo del pool por defecto de Vitest 4 (`forks`) muere antes de ejecutar una sola prueba, en
esta combinación Node 24.18.1 + Vitest 4.1.11 + Windows. Arreglo aplicado (dentro de mi carril,
`packages/ui/` y `apps/backoffice/` son mis reservas o las necesito para mis dos modales):

- `packages/ui/vitest-base.config.ts` y `apps/backoffice/vitest-base.config.ts` nuevos:
  `{ test: { pool: 'threads', fileParallelism: false } }`.
- `"runnerConfig": true` agregado al target `test` de `packages/ui/angular.json` y
  `apps/backoffice/angular.json` (opción soportada oficialmente por `@angular/build:unit-test`,
  no un hack por fuera del framework).

Con esto, el mismo comando corrió limpio la mayoría de las veces (ver §1). **No queda 100% libre
de flakiness**: en un intento posterior el arranque del pool de threads tardó más de lo que Vitest
espera y volvió a tirar `Timeout waiting for worker to respond` una vez — mejor que el 100% de
fallo anterior, pero no una garantía. Se documenta así, sin inflar.

## 1. Corrida real, completa, de `@aportaya/ui` (todo el paquete, no solo mis archivos)

```
$ yarn workspace @aportaya/ui test:front
...
❯ Building...
✔ Building...
Application bundle generation complete. [43.818 seconds] - 2026-09-22T06:21:26.025Z

 ❯ ui src/monto/monto.spec.ts (2 tests | 1 failed) 5137ms
     × pasa los mismos vectores que el Monto de Flutter 5082ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
FAIL ui src/monto/monto.spec.ts > ap-monto > pasa los mismos vectores que el Monto de Flutter
Error: Test timed out in 5000ms.

 Test Files  1 failed | 16 passed (17)
      Tests  1 failed | 68 passed (69)
   Start at 02:21:32
   Duration 67.21s (transform 29.67s, setup 8.23s, import 40.72s, tests 10.45s, environment 4.46s)
```

17 archivos de spec en total en `packages/ui/src` (15 preexistentes + `dialogo.spec.ts` +
`estado-de-pantalla.spec.ts`, los dos nuevos de esta sesión). El único que falla
(`monto.spec.ts`) es preexistente, no tocado por este carril, y falla por timeout — ver hallazgo
H-6 más abajo. Los 16 archivos restantes, incluidos los dos nuevos, en verde.

## 2. Corrida aislada de `dialogo.spec.ts` (13 casos), para confirmar el detalle caso por caso

```
$ npx ng test --include='src/dialogo/**/*.spec.ts' --runner-config --watch=false
...
 Test Files  1 passed (1)
      Tests  11 passed (11)
   Duration  20.14s
```

(11 de los 13 casos existían en el momento de esta corrida puntual; los 2 casos agregados después
—`removeEventListener` al destruir— se sumaron tras encontrar el bug de `d.close is not a
function` documentado en `contrato-dialogo.md` §6 y quedaron corriendo dentro de la corrida
completa de la §1, que ya reporta el archivo entero en verde.)

## 2.1. Bug propio encontrado y corregido en el camino (regla de honestidad: no se esconde)

El primer intento de test de "conteo de escuchas antes/después" (H3.S1.M4) espiaba
`HTMLDialogElement.prototype.addEventListener` y esperaba exactamente 1 llamada — pero con
`isolate: false` (necesario para que el pool no muera, ver §0) varios archivos de spec del mismo
paquete corren en el mismo realm de jsdom, así que la cuenta GLOBAL de `addEventListener` sobre
`<dialog>` incluye instancias de otros tests (por ejemplo, `Catalogo` monta su propio `ap-dialogo`
de muestra). Falló así:

```
AssertionError: expected "addEventListener" to be called 1 times, but got 3 times
 ❯ src/dialogo/dialogo.spec.ts:142:21
```

Primer intento de arreglo: filtrar las llamadas por `agregar.mock.instances[i] === caja` — no
alcanzó (seguía dando 3, no 1, incluso filtrando por instancia). Segundo intento: espiar
`removeEventListener` directamente en la instancia (`vi.spyOn(caja, 'removeEventListener')`, sin
tocar el prototipo) — **tampoco** alcanzó: `expected "removeEventListener" to be called 1 times,
but got 3 times`, de nuevo. Con `isolate: false` (necesario para que el pool no muera) y varios
específicos que montan `Dialogo` sin destruirlo explícitamente compartiendo el mismo realm de
jsdom, contar invocaciones de un método de `EventTarget` — aunque se lo espíe "en la instancia" —
no dio un número estable de una corrida a otra.

**Decisión:** se abandonó el conteo de invocaciones (una técnica fràgil bajo estas condiciones de
entorno) a favor de una prueba **funcional**, sin espiar nada de la API de eventos: un test prueba
que el backdrop SÍ reacciona mientras el componente está montado (con borrador sucio, un clic
dispara `confirm()`), y otro prueba que DEJA de reaccionar después de `fixture.destroy()` (el mismo
clic, después de destruir, no dispara nada). Esto prueba lo mismo que le importa a quien consume el
organismo — que la limpieza funciona de verdad — sin depender de contar llamadas internas en un
entorno donde ese conteo no es confiable.

**Confirmación final, literal, después del arreglo:**

```
$ yarn workspace @aportaya/ui test:front
...
Application bundle generation complete. [16.502 seconds] - 2026-09-22T07:02:17.067Z

 ❯ ui src/monto/monto.spec.ts (2 tests | 1 failed) 5449ms
     × pasa los mismos vectores que el Monto de Flutter 5154ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
FAIL ui src/monto/monto.spec.ts > ap-monto > pasa los mismos vectores que el Monto de Flutter
Error: Test timed out in 5000ms.

 Test Files  1 failed | 16 passed (17)
      Tests  1 failed | 70 passed (71)
   Start at 03:02:19
   Duration 22.24s (transform 3.88s, setup 3.35s, import 4.87s, tests 8.10s, environment 4.44s)
```

Único rojo: `monto.spec.ts`, preexistente, ajeno a este carril (H-7). Los 16 archivos restantes,
incluidos `dialogo.spec.ts` (13 casos) y `estado-de-pantalla.spec.ts`, en verde. Peldaño `TESTED`
real, no razonado.

## 3. Qué NO se cubrió (honesto)

- Un reintento posterior de correr `dialogo.spec.ts` + `estado-de-pantalla.spec.ts` juntos por
  separado (fuera de la corrida completa) volvió a pegarle al timeout de arranque del pool
  (`Timeout waiting for worker to respond`) — no es determinístico al 100 %. La evidencia de la §1
  (corrida completa, en verde) es la que cuenta como `TESTED`.
- E2E de foco/teclado real en navegador: no corrido — ver `contrato-dialogo.md` §6 (bloqueo real:
  no hay login en `apps/backoffice`, las rutas de negocio redirigen sin sesión).
