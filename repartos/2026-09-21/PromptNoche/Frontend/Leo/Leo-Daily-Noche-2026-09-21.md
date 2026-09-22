# Daily de Leo — turno noche — área frontend — 2026-09-21

> **AVANCE: 13 / 26 — 50 %.** ← `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> Partía de 8/26 (30,8 %) al abrir esta sesión de continuación (con `git` real, a diferencia de la
> anterior). **Estado:** `IN_PROGRESS`, cerrado por bloqueos de entorno reales y ya registrados
> (sin login en `apps/backoffice` para E2E; `clientes/angular/*` no generado para correr tests de
> `apps/backoffice`), no por pereza ni por falta de coordinación. Ver
> `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` para el detalle completo y las 4
> respuestas de cada `A MEDIAS`/`BLOQUEADO`.
> PR abierto (no mergeado): https://github.com/PabloArauzCaballero/PasanakuBackend/pull/3

- **Persona:** Leo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [Diálogo, host de estados y borrador: la interacción compartida vive en un solo lugar](PR8-DialogoYEstados.Frontend/DialogoHostDeEstadosYBorrador.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 49 microtareas → [Leo-Daily-Noche-2026-09-21.md](../../Backend/Leo/Leo-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Corrección 2026-09-21 (Pablo, en sesión):** este bloque B se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura).
  Confirmado: también es trabajo de Pasanaku. Ver
  [docs/trabajo/2026-09-21-correccion-bloques-leo/PLAN.md](../../../../../docs/trabajo/2026-09-21-correccion-bloques-leo/PLAN.md).
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `PasanakuFrontend` · rama base `dev` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 52 microtareas → [El CI deja de mentir: E2E del backoffice, dos jobs macOS, release iOS y cero `|| true`](PR13-Ci.Frontend/CiRealMacosYReleaseIos.md)
  - **Mismo repo que el bloque B desde la corrección de hoy:** los dos bloques son `PasanakuBackend`/`PasanakuFrontend` (antes, el bloque B decía `mantra-core-health`, otro repo). La regla 91 (dinero) y la 98 (microservicios) aplican en los dos bloques donde corresponda.
  - **Orden del turno:** A (backend) → B (diálogo y estados) → C (CI). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** capabilities iOS, release iOS en macOS, humo honesto, CI real y cabeceras.
  - **Tus reservas en el bloque C:** `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts`. Ningún otro carril las toca, y vos no tocás las suyas.

## 1. Instalación del estándar — lo primero

- [ ] `.claude/` del estándar copiado o enlazado dentro de `PasanakuBackend/` (sirve para los
      bloques B y C: es el mismo repo). Ya hay una copia sin commitear ahí de una sesión anterior —
      verificala antes de volver a copiar.
- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas por `skills-router`: solo las de la tabla de tu encargo, **no el catálogo entero**.

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Comandos reales del repo — se completan en H1.S1.M2

Los alias del encargo son **hipótesis heredadas del documento antecedente**. Pegá acá los reales.

| Alias | Comando real | Existe |
|---|---|---|
| `CMD_LINT` | `turbo run lint` (root); scoped `--filter=@aportaya/{ui,web,backoffice}` | Sí, con reservas — ver evidencia |
| `CMD_TYPECHECK` | `turbo run typecheck` (root); scoped igual | Sí |
| `CMD_TEST` | `turbo run test:front` (root); scoped igual; `yarn workspace @aportaya/ui test:front` | Sí, ver bloqueo del pool de Vitest en evidencia |
| `CMD_BUILD` | `turbo run build` (root); scoped igual | Sí |
| `CMD_E2E` | `yarn workspace @aportaya/backoffice test:e2e` → `playwright test` | Sí, script existe; no ejecutado esta sesión |

Detalle completo, con exit codes y salida pegada: `PR8-DialogoYEstados.Frontend/evidencia/h1-sha-y-comandos.md` y `.../h1-comandos-base.md`.

## 3. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — La base y el contrato de estado publicado | 7 | 6 | HECHO salvo 1 `A MEDIAS` (test escrito, no ejecutable en este entorno) |
| H2 — El contrato de estado se renderiza en un solo lugar | 6 | 3 | H2.S1 completo y `TESTED`; H2.S2.M1 verificado N/A; H2.S2.M2/M3 sin empezar |
| H3 — El diálogo tiene anatomía, foco y una sola política de descarte | 7 | 3 | política de descarte implementada y `TESTED` por unidad; foco/apilamiento y el E2E de descarte BLOQUEADOS (sin login) |
| H4 — El formulario tiene un dueño y dos modales lo demuestran | 6 | 1 | contrato + Q-L1 implementado; ejecución de tests BLOQUEADA (`clientes/angular/*` ausente) |
| **TOTAL** | **26** | **13** | **50 %** |

## 4. Qué quedó andando (con evidencia)

Todo lo de abajo tiene su Definition of Done ejecutado y su salida literal pegada (salvo lo
marcado). Detalle completo en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §1.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | `git status --short` corrido de verdad (sesión anterior no pudo) | `git status --short` | limpio antes de editar |
| H1.S1.M2..M4, H1.S2.M1/M2 | Como antes (sesión anterior) | — | sin cambios |
| H2.S1.M1/M2/M3 | Host con plantillas de contexto tipado (vacío/error), `trazaId`/acción/"obsoleto" resueltos, test de dependencias del host | `yarn workspace @aportaya/ui test:front` | 16/17 archivos en verde — `evidencia/h3-h2-ui-tests.md` |
| H3.S1.M4 | Bug real encontrado y arreglado (`d.close is not a function` en jsdom); listener del backdrop con conteo antes/después probado; 100 aperturas/cierres sin fuga | mismo comando | PASS |
| H3.S2.M1 | Dos modales reales elegidos y publicados (sesión anterior) | — | sin cambios |

**Arreglo de entorno dentro de mi carril (no un hallazgo ajeno esta vez):** el bloqueo H-5 de la
sesión anterior (pool de Vitest muere al arrancar) se resolvió con `pool: 'threads'` +
`fileParallelism: false` en `packages/ui/vitest-base.config.ts` y `apps/backoffice/vitest-base.config.ts`,
activado con `runnerConfig: true` en los `angular.json` de esos dos proyectos. No 100 % libre de
flakiness (documentado), pero pasó de 100 % de fallo a corridas mayormente en verde.

## 5. A medias — las cuatro respuestas, obligatorias

Detalle completo en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §2. Resumen:

- **H3.S2.M2** — política de descarte implementada y probada por unidad (13 tests, en verde); el
  DoD pide E2E (`<CMD_E2E> --grep "descarte"`), bloqueado por falta de login real en
  `apps/backoffice` (hallazgo ya del carril F12, no mío).
- **H3.S1.M2/M3** — el comportamiento nativo de `<dialog>` ya da foco/trampa/restauración según la
  especificación; sin E2E que lo confirme (mismo bloqueo de login).
- **H4.S1.M3** — política de entidad cambiada, de "declarada" a **implementada** en los dos
  modales; el test del caso está escrito, no ejecutado (`apps/backoffice` no compila como bundle
  completo en este entorno por `clientes/angular/*` ausente — H-2, ya registrado).
- **H4.S2.M1/M2** — los dos modales cableados con `hayCambiosSinGuardar` + doble envío corregido +
  Q-L1; typecheck y `ng lint` limpios confirmados; tests no ejecutados (mismo bloqueo que arriba).
- **H3.S2.M3** — "error de guardado conserva el borrador" ya era cierto (sin tocar); "muestra el
  error de campo del servidor" NO implementado — trabajo nuevo, no solo verificación.

## 6. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H3.S1.M2/M3, H3.S2.M2 (parte E2E), H4.S2.M3 | Todo E2E de foco/teclado/descarte + comparación visual | Confirmé Playwright+Chromium instalados y funcionales; intenté apuntar a `apps/backoffice` real | Que exista login real o un mecanismo de e2e para abrir sesión sin él (hallazgo ya de F12, no mío) | Producto / otro carril |
| H4.S1.M2/M3, H4.S2.M1/M2, H3.S2.M3 (ejecución) | `test:front` de `apps/backoffice` no corre ningún spec | Confirmé con la lista completa de errores de un build real: 0 en mis 4 archivos, ~30 por `clientes/angular/*` ausente + 1 nuevo por `tokens.css` ausente | Generar `clientes/angular/*` (no encontré script de generación en este checkout) | Carril dueño de los clientes HTTP generados |

> Regla 65: estos son huecos de infraestructura pre-existentes, ya registrados por otras sesiones
> (F12, H-2) antes de que empezara este carril — no un problema de coordinación entre carriles de
> hoy.

## 7. Hallazgos para el equipo

Lo roto que encontrás fuera de tu alcance va acá con su ruta. **No se arregla** (regla 00 §3),
salvo H-5 que sí entraba en mi carril y se arregló.

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| H-1 | `apps/web/scripts/contenido.mjs:25` revienta sin capturar por un `.md` sin frontmatter | `@aportaya/web` typecheck/build/test | Registrado (sesión anterior) |
| H-2 | Faltan ~30 módulos generados `clientes/angular/*` en este checkout | `@aportaya/{web,backoffice}` no typechequean/buildean limpio | Confirmado de nuevo en esta sesión, sin script de generación local encontrado |
| H-3 | `python3`/`python` no resuelven en este entorno | `verificar_frontend.py` / `plan_gate.py --self-test` | Registrado (sesión anterior) |
| H-4 | `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` — 2 errores de `ng lint` | Bloquea `@aportaya/ui#lint` en verde | Registrado, fuera de mi alcance |
| H-5 | Pool de Vitest muere al arrancar (Node 24.18.1 + Windows) | Nadie podía correr `test:front` en esta clase de sesión | **Arreglado** dentro de `packages/ui` y `apps/backoffice` (ver §4) — otros proyectos del monorepo necesitan el mismo arreglo si lo sufren |
| H-6 (nuevo) | `@aportaya/tokens/generado/tokens.css` no existe hasta correr el build de `tokens` | Bundle completo de `web`/`backoffice` | Registrado, no commiteado (carpeta gitignored) |
| H-7 (nuevo) | `packages/ui/src/monto/monto.spec.ts` hace timeout a los 5000ms de forma reproducible, preexistente | `@aportaya/ui#test:front` en verde al 100% | Registrado, fuera de mi alcance |

## 8. No cubierto

- H2.S2.M2/M3: no se escribieron tests de variantes/accesibilidad para los 7 consumidores reales de
  `estado-de-pantalla` sin spec (distinto de H2.S2.M1, que sí se verificó como N/A real).
- H3.S2.M3: "error de campo identificado por el servidor" no implementado.
- Ningún E2E ni comparación visual en ningún viewport/tema — bloqueo real, documentado en §6.
- `CampoMonto`, `GrupoRadio`, `Boton` siguen sin leerse en profundidad.
- `apps/movil` (Flutter) fuera de alcance.
- Detalle consolidado en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §5.

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F3 | Que el tipo de estado tenga diez variantes y esos nombres | Tu baseline (H1.S2.M1) | **RESUELTA**: no existe tal tipo; ver `entregables/contrato-view-state.md` |
| Q-L1 | Qué pasa con el borrador si la entidad cambia mientras se edita | Producto | Rama conservadora **implementada** (no solo declarada); decisión de producto sigue pendiente |
| Q-L2 | Si la proyección alcanza o hace falta una plantilla diferida | Tu verificación en la versión instalada | **RESUELTA**: la proyección actual alcanza |
| Q-L3 | Si algún modal evita a propósito la protección de descarte | Producto | Los dos modales ahora protegen (diseño conservador); sin dato nuevo sobre intención previa |
| — (nueva) | H2.S2.M1 ("reemplazar dos ramas repetidas por el host") — el precondición no existe en este repo | Ya resuelta por este carril | **VERIFICADO N/A**, ver `contrato-view-state.md` §5 |

## 10. Tus reservas de archivos en este turno

el tipo de estado y su contrato; el host de estados; el organismo de diálogo y sus estilos; los dos modales que publiques en H3.S2.M1

Tu lote: `PR8-DialogoYEstados.Frontend/` — entregables en `PR8-DialogoYEstados.Frontend/entregables/`, evidencia en `PR8-DialogoYEstados.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR13-Ci.Frontend/`

- **Avance del bloque C:** 0 / 52 — 0 %. (5 hitos · 12 subtareas.)
- Entregables en `PR13-Ci.Frontend/entregables/`, evidencia en `PR13-Ci.Frontend/evidencia/`.
- **Tus reservas:** `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
