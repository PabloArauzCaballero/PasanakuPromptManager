# H4 — `ficha-de-cobro.ts` / `ficha-de-factura.ts`: typecheck limpio, `test:front` bloqueado (no por estos archivos)

> Peldaño: `WRITTEN` + typecheck confirmado sobre un build real (no `RUNS`). Ver
> `contrato-formulario.md` §7 para el detalle de qué se implementó.

## 1. `ng lint` sobre los cuatro archivos tocados — limpio

```
$ npx eslint src/app/rutas/contabilidad/cobros/ficha-de-cobro.ts \
              src/app/rutas/contabilidad/cobros/ficha-de-cobro.spec.ts \
              src/app/rutas/contabilidad/compras/ficha-de-factura.ts \
              src/app/rutas/contabilidad/compras/ficha-de-factura.spec.ts
(node:19608) [MODULE_TYPELESS_PACKAGE_JSON] Warning: ... (irrelevante, de eslint.config.js)
[exited with code 0]
```

Cero errores, cero warnings de regla en los cuatro archivos.

## 2. `ng test` de `apps/backoffice` bundlea TODA la app, no solo los specs incluidos — confirmado

`--include` filtra qué specs CORREN, no qué se bundlea: `@angular/build:unit-test` arma el
`buildTarget` completo (toda la app, todas las rutas) antes de correr cualquier test. Se confirmó
pidiendo *solo* mis dos specs y viendo que el build igual falla por archivos de OTRAS rutas
(publicidad, cumplimiento, identidad — nada de esto es mío ni de este carril):

```
$ npx ng test --include='src/app/rutas/contabilidad/cobros/ficha-de-cobro.spec.ts' \
              --include='src/app/rutas/contabilidad/compras/ficha-de-factura.spec.ts' \
              --runner-config --watch=false
Application bundle generation failed. [114.962 seconds]

X [ERROR] TS2307: Cannot find module 'clientes/angular/erp' ...
    src/app/rutas/contabilidad/dominio/cu100-periodos.ts:4:34
X [ERROR] TS2307: Cannot find module 'clientes/angular/identidad' ...
    src/app/rutas/cumplimiento/dominio/cu02-expedientes.ts:9:7
X [ERROR] TS2307: Cannot find module 'clientes/angular/organizador' ...
    src/app/rutas/cumplimiento/dominio/cu90-habilitacion.ts:4:34
... (25 errores más, todos en clientes/angular/* faltante o en archivos que dependen de él)
X [ERROR] Could not resolve "@aportaya/tokens/tokens.css"
    ../../packages/ui/src/estilos.css:2:8
```

**Ni un solo error mencionó `ficha-de-cobro.ts`, `ficha-de-factura.ts` ni sus specs.** Es la misma
brecha H-2 ya registrada por la sesión anterior (`clientes/angular/{identidad,erp,organizador,
nucleo-financiero,publicidad,...}` no existen en este checkout — `ls clientes/angular` da "no such
file or directory"), más un hallazgo nuevo, más chico:

**H-6 (nuevo):** `@aportaya/tokens/generado/tokens.css` tampoco existe hasta correr
`yarn workspace @aportaya/tokens build` (o su script `a-css.mjs` a solas). No estaba en `H-2`
porque el checkout de la sesión anterior nunca llegó a `yarn install` completo. Se ejecutó
`node packages/tokens/scripts/a-css.mjs` en este worktree para confirmar que el archivo se genera
sin depender de `dart`/`flutter` (el script de CSS es independiente del de Dart) — se generó
`generado/tokens.css` (230 líneas) correctamente. **No se commitea**: `packages/tokens/generado/`
está en `.gitignore` (es salida de build, ADR-016), así que sigue faltando en cualquier checkout
fresco hasta que alguien corra ese build — dato para el equipo, no algo para versionar a mano.

## 3. Conclusión

`ficha-de-cobro.ts` y `ficha-de-factura.ts` (y sus dos nuevos specs) son type-correct — verificado
leyendo la salida completa de un build real, no asumido. Correr sus tests de verdad
(`test:front` de `apps/backoffice`) sigue bloqueado en este entorno hasta que exista
`clientes/angular/*` — igual que estaba antes de esta sesión, para CUALQUIER spec de
`apps/backoffice`, no solo los míos.
