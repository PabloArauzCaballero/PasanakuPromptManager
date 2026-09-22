# H1.S1.M3 y H1.S1.M4 — evidencia literal (rojo previo + localización por compilador)

Todo lo de abajo corrió contra el árbol real de `dev` (SHA `a23bcb117…`), sin editar ningún
archivo (bloqueo de escritura en el checkout compartido, ver `PR8-carril.md`). `yarn install
--immutable` corrió primero (no había `node_modules`; no se agregó ni actualizó ninguna
dependencia, solo se materializó `yarn.lock`).

## 1. `turbo run <tarea>` en la raíz, sin `--filter` — rojo real, no relacionado con mi alcance

```text
$ yarn turbo run lint
...
@aportaya/movil:lint: "dart" no se reconoce como un comando interno o externo...
@aportaya/movil#lint:  ERROR  command exited (127)
Failed:    @aportaya/movil#lint
$ echo $?   # (medido aparte, correctamente): 
REAL_EXIT_LINT=127
```

Mismo patrón en `typecheck` (falla `@aportaya/diseno-flutter#typecheck` por falta de `dart`),
`test:front` (falla `@aportaya/diseno-flutter#test:front` por falta de `flutter`) y `build`
(mismo). **Causa real:** este entorno de ejecución no tiene instalados los SDK de Dart/Flutter, y
`turbo` sin `--filter` corre las 9 paquetes del workspace, incluidos `@aportaya/movil` y
`@aportaya/diseno-flutter` (Flutter, fuera del alcance IN de este carril). No es un defecto de
código en `packages/ui`/`apps/{web,backoffice}`.

## 2. `turbo run <tarea> --filter=@aportaya/{ui,web,backoffice} --continue` — mi alcance real

### `typecheck` — `REAL_EXIT=2`

```text
Tasks:    4 successful, 7 total
Failed:    @aportaya/backoffice#typecheck, @aportaya/web#contenido, @aportaya/web#typecheck
```

**`@aportaya/ui#typecheck` NO está en la lista de fallidos — pasó.** Esto es la confirmación por
compilador (H1.S1.M4) de que `estado-de-pantalla.ts`, `estado-vacio.ts` y `dialogo.ts` compilan
limpio hoy, tal como están. `web` y `backoffice` fallan por ~30 errores `TS2307: Cannot find
module 'clientes/angular/<servicio>'` — clientes HTTP generados que faltan en este checkout (no
se corrió el generador de clientes en esta sesión) — **no relacionado con diálogo/estado**, y por
un `contenido.json` que no se generó (`apps/web:contenido` revienta por un `.md` sin
frontmatter, ver hallazgo abajo).

### `test:front` — `REAL_EXIT=1`

```text
Failed:    @aportaya/backoffice#test:front, @aportaya/ui#test:front, @aportaya/web#contenido, @aportaya/web#test:front
```

**Hallazgo de entorno adicional, más allá del bloqueo de git:** `@aportaya/ui:test:front`
(Vitest 4.1.11, pool de forks) falla con `Timeout waiting for worker to respond` /
`Worker exited unexpectedly` en 14 archivos de spec, `Test Files: no tests`, y el proceso termina
con una excepción no capturada. Es un fallo de arranque del pool de workers de Vitest en esta
máquina (probablemente relacionado al sandboxing de procesos de este entorno de ejecución), **no
un test en rojo por código**: no llegó a ejecutarse ni un solo test. Esto significa que, incluso
si hubiera podido escribir código nuevo en el checkout, **tampoco habría podido correr
`test:front` de `@aportaya/ui` con éxito en esta sesión concreta** — es un segundo bloqueo,
independiente del bloqueo de `git`.

`web`/`backoffice` fallan en cascada por el mismo `contenido.json` faltante y los mismos módulos
`clientes/angular/*` ausentes que en `typecheck`.

### `build` — `REAL_EXIT=1`

```text
Tasks:    3 successful, 5 total
Failed:    @aportaya/backoffice#build, @aportaya/web#build
```

`@aportaya/ui#build` no está en la lista de fallidos (el mensaje "ui: se consume por alias de
tsconfig..." es el script real, no un error). `web`/`backoffice` fallan por los mismos módulos
`clientes/angular/*` faltantes.

### `lint` — `REAL_EXIT=49` (9009 en Windows, 9009 mod 256 = 49)

```text
Failed:    @aportaya/backoffice#lint, @aportaya/ui#lint, @aportaya/web#contenido, @aportaya/web#lint
```

Dos causas distintas mezcladas en el mismo comando:

1. **`@aportaya/ui#lint` — falla real, no relacionada con mi alcance:** `ng lint` reporta 2
   errores reales en `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` (`click` sin
   `keyup`/`keydown`/`keypress`, y elemento interactivo no enfocable —
   `@angular-eslint/template/click-events-have-key-events` y `.../interactive-supports-focus`).
   Archivo fuera de mi alcance (no es `estado-de-pantalla`, `estado-vacio` ni `dialogo`) —
   se registra como hallazgo, no se toca (regla 00 §3.2).
2. **`web`/`backoffice` — `ng lint` pasa** ("All files pass linting" para los dos, visto en la
   corrida), pero el script completo (`ng lint && python3 ../../scripts/verificar_frontend.py
   <app>`) falla igual porque **`python3` no está instalado en este entorno** (mismo problema que
   `python .claude/hooks/plan_gate.py --self-test` de la sección 1 del encargo, que tampoco pudo
   correr: "no se encontró Python").

## 3. Localización con el compilador (H1.S1.M4) — no con grep suelto

`Read` directo confirmó las tres rutas con archivo y línea (ver `contrato-view-state.md` y
`contrato-dialogo.md`). La confirmación **por compilador** es el resultado de `@aportaya/ui#typecheck`
de arriba: pasa, y ese target incluye `tsconfig.lib.json`/`tsconfig.spec.json` de todo
`packages/ui/src`, que resuelve los imports reales de los 11+ consumidores de
`estado-de-pantalla`/`estado-vacio` y de `dialogo` en `apps/{web,backoffice}` (los propios
consumidores, aunque están en paquetes que fallan por otra razón — `clientes/angular/*` — no
reportan ningún error sobre las rutas de `@aportaya/ui/estado-de-pantalla/…` ni
`@aportaya/ui/dialogo/…`: los errores listados arriba son todos sobre `clientes/angular/*`, cero
sobre mis tres archivos).

## 4. Hallazgos para el equipo (no se arreglan, regla 00 §3)

| Qué | Ruta | Impacto |
|---|---|---|
| `apps/web/scripts/contenido.mjs` revienta sin capturar la excepción por un `.md` sin frontmatter | `apps/web/contenido/legal/contrato-de-adhesion.md`, `apps/web/scripts/contenido.mjs:25` | Rompe `typecheck`/`test:front`/`build` de `@aportaya/web` para cualquier carril |
| Faltan los clientes HTTP generados (`clientes/angular/{identidad,erp,organizador,nucleo-financiero,publicidad,transparencia,grupos,tarifas}`) en este checkout | imports en `apps/backoffice/src/app/rutas/**/dominio/*.ts` y `apps/web/src/app/verificadores/*.ts` | Rompe `typecheck`/`test:front`/`build` de `@aportaya/{web,backoffice}`; parece un paso de generación de clientes no ejecutado en este checkout, no un bug de código |
| `python3`/`python` no resuelven a un intérprete real en este entorno (alias de Microsoft Store) | afecta `scripts/verificar_frontend.py` (parte de `lint` de cada app) y `.claude/hooks/plan_gate.py --self-test` | Rompe el paso de instalación del estándar (sección 1 del encargo) y el `lint` completo de `web`/`backoffice` para cualquier carril, en este tipo de entorno |
| `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` — 2 errores reales de accesibilidad (`click` sin evento de teclado, elemento no enfocable) | mismo archivo | Bloquea `ng lint` de `@aportaya/ui` para cualquier carril que dependa de que ese comando esté en verde; fuera de mi alcance (no es dialogo/estado) |
| El pool de workers de Vitest (`forks`) no arranca en este entorno para `@aportaya/ui:test:front` (`Timeout waiting for worker to respond` en los 14 primeros specs, luego el proceso completo muere) | entorno, no código | Nadie puede correr `test:front` de `@aportaya/ui` con éxito en este tipo de sesión hasta que se resuelva (probablemente el sandboxing de child_process de este entorno) |
