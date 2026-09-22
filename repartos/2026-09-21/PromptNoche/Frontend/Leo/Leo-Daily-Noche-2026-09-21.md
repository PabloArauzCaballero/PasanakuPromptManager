# Daily de Leo — turno noche — área frontend — 2026-09-21

> **AVANCE: 8 / 26 — 30,8 %.** ← `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> **Estado:** `IN_PROGRESS`, cerrado por bloqueo de entorno (no de coordinación). Ver
> `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` para el detalle completo, las 4
> respuestas de cada `A MEDIAS`/`BLOQUEADO`, y el bloqueo de git contra este repo desde esta sesión.
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
| H1 — La base y el contrato de estado publicado | 7 | 5 | HECHO salvo 2 `A MEDIAS` |
| H2 — El contrato de estado se renderiza en un solo lugar | 6 | 0 | BLOQUEADO (entorno) |
| H3 — El diálogo tiene anatomía, foco y una sola política de descarte | 7 | 2 | parcial — contratos y reserva HECHOS, implementación BLOQUEADA |
| H4 — El formulario tiene un dueño y dos modales lo demuestran | 6 | 1 | parcial — contrato HECHO, resto BLOQUEADO/A MEDIAS |
| **TOTAL** | **26** | **8** | **30,8 %** |

## 4. Qué quedó andando (con evidencia)

Solo entra acá lo que tiene su Definition of Done ejecutado y su salida literal pegada. Detalle
completo en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §Completado.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M2 | Tabla de comandos reales completada | `cat package.json` (raíz, `ui`, `web`, `backoffice`), `cat turbo.json` | PASS — `evidencia/h1-sha-y-comandos.md` |
| H1.S1.M3 | Rojo previo real (root y scoped) | `turbo run {lint,typecheck,test:front,build}` (+ `--filter`) | exit codes reales pegados — `evidencia/h1-comandos-base.md` |
| H1.S1.M4 | `estado-de-pantalla.ts`/`estado-vacio.ts`/`dialogo.ts` confirmados por compilador | `turbo run typecheck --filter=@aportaya/ui` | `@aportaya/ui#typecheck` PASS, cero errores sobre esas rutas |
| H1.S2.M1 | Contrato de estado releído y comparado contra las 10 variantes heredadas | lectura directa | `entregables/contrato-view-state.md` |
| H1.S2.M2 | PR publicado en `dev` con el contrato | `gh pr create` | https://github.com/PabloArauzCaballero/PasanakuBackend/pull/3 (OPEN) |
| H3.S1.M1 | Contrato del diálogo contra el código real | lectura directa | `entregables/contrato-dialogo.md` |
| H3.S2.M1 | Dos modales reales elegidos y publicados | — | fila Modal 1/2 en `Daily-Noche-2026-09-21.md` §4 |
| H4.S1.M1 | Dueño único del borrador declarado | lectura directa | `entregables/contrato-formulario.md` |

## 5. A medias — las cuatro respuestas, obligatorias

Detalle completo (H1.S1.M1, H1.S2.M3, H4.S1.M3) en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §A medias.

### H1.S1.M1 — SHA registrado, `git status` no
- **Qué anda:** SHA real confirmado por dos vías (`.git/HEAD` local + API de GitHub contra `origin/dev`): `a23bcb117effe7ce66d069a97ebd2c25c8390306`.
- **Qué no anda:** `git status --short` no se pudo correr (git bloqueado para esta sesión).
- **Qué falta exactamente:** correrlo desde una sesión con git real.
- **Dónde quedó:** checkout compartido sin tocar, en `leo/feature/carril-PR3-plataforma`.

### H1.S2.M3 — test de exhaustividad escrito, no ejecutado
- **Qué anda:** `estado-de-pantalla.exhaustividad.spec.ts` escrito y publicado vía API en la rama del PR.
- **Qué no anda:** no se corrió (bloqueo de escritura local + el pool de Vitest de `@aportaya/ui` no arranca en este entorno de todos modos).
- **Qué falta exactamente:** correr `yarn workspace @aportaya/ui test:front` desde un checkout real, en una máquina donde el pool de Vitest funcione.
- **Dónde quedó:** commiteado en `leo/frontend/dialogo-estados`, dentro del PR #3.

### H4.S1.M3 — política de entidad cambiada declarada, no implementada
- **Qué anda:** rama conservadora escrita y justificada en `entregables/contrato-formulario.md` §5.
- **Qué no anda:** ningún código la aplica todavía.
- **Qué falta exactamente:** snapshot del `input()` al abrir + comparación antes de guardar.
- **Dónde quedó:** `ficha-de-cobro.ts`/`ficha-de-factura.ts` sin tocar, igual que en `dev`.

## 6. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H2 completo, H3.S1.M2/M3/M4, H3.S2.M2/M3, H4.S1.M2, H4.S2.M1/M2/M3 | Escribir y ejecutar código Angular real + E2E/visual contra `PasanakuBackend` | Documenté cada brecha real contra el código leído (contratos en `entregables/`); intenté `git` local (3 formas), `EnterWorktree`, y escribir con `Write` en el checkout compartido — las tres rechazadas por el sandbox de esta sesión | Una sesión con acceso de escritura git real a `PasanakuBackend` (o un worktree real de ese repo, no de `PasanakuPromptManager`) | Configuración del entorno de ejecución, no de otro carril |

> Regla 65: si el contrato de lo que falta **se puede nombrar, se simula en tres niveles**
> —correcto, límite, inválido— y se cierra contra el doble, declarándolo. Solo una decisión de
> negocio o una acción destructiva sobre algo compartido justifican dejarlo abierto.

## 7. Hallazgos para el equipo

Lo roto que encontrás fuera de tu alcance va acá con su ruta. **No se arregla** (regla 00 §3).
Detalle completo con evidencia en `PR8-DialogoYEstados.Frontend/evidencia/h1-comandos-base.md` §4.

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| H-1 | `apps/web/scripts/contenido.mjs:25` revienta sin capturar por un `.md` sin frontmatter (`apps/web/contenido/legal/contrato-de-adhesion.md`) | Cualquiera que dependa de `@aportaya/web` typecheck/build/test | Registrado |
| H-2 | Faltan ~30 módulos generados `clientes/angular/*` en este checkout (identidad, erp, organizador, nucleo-financiero, publicidad, transparencia, grupos, tarifas) | `@aportaya/{web,backoffice}` no typechequean/buildean limpio | Registrado |
| H-3 | `python3`/`python` no resuelven en este entorno (alias de Microsoft Store) | Rompe `verificar_frontend.py` (parte de `lint`) y `plan_gate.py --self-test` de la sección 1 del encargo, para todo el bloque B/C | Registrado |
| H-4 | `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` — 2 errores reales de `ng lint` (accesibilidad de teclado) | Bloquea `@aportaya/ui#lint` en verde | Registrado, fuera de mi alcance |
| H-5 | El pool de workers de Vitest no arranca en este tipo de entorno para `@aportaya/ui:test:front` (`Timeout waiting for worker to respond`, proceso completo termina) | Nadie puede correr `test:front` de `@aportaya/ui` en esta clase de sesión | Registrado |

## 8. No cubierto

- Ningún E2E de foco/teclado/descarte se ejecutó en navegador real (Playwright no se orquestó en esta sesión).
- Ninguna captura visual (3 viewports × 2 temas) se tomó.
- No se verificó en runtime que `role="status"`/`role="alert"` anuncien realmente a un lector de pantalla (supuesto respaldado por ARIA, no observado).
- `CampoMonto`, `GrupoRadio`, `Boton` (moléculas que usan los dos modales elegidos) no se leyeron en profundidad.
- `apps/movil` (Flutter) no se revisó — fuera de alcance.
- Los 8 consumidores de `estado-de-pantalla` no leídos en detalle (se leyeron 3 de 11) no se inspeccionaron uno por uno.
- Ver el detalle consolidado en `PR8-DialogoYEstados.Frontend/entregables/PR8-carril.md` §No cubierto.

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F3 | Que el tipo de estado tenga diez variantes y esos nombres | Tu baseline (H1.S2.M1) | **RESUELTA por este carril**: no existe tal tipo; ver `entregables/contrato-view-state.md` |
| Q-L1 | Qué pasa con el borrador si la entidad cambia mientras se edita | Producto | ABIERTA — rama conservadora declarada, no implementada |
| Q-L2 | Si la proyección alcanza o hace falta una plantilla diferida | Tu verificación en la versión instalada | **RESUELTA**: la proyección actual (`ng-content`) alcanza para los dos modales elegidos |
| Q-L3 | Si algún modal evita a propósito la protección de descarte | Producto | ABIERTA — ningún modal leído protege hoy; no hay evidencia de que sea intencional |

## 10. Tus reservas de archivos en este turno

el tipo de estado y su contrato; el host de estados; el organismo de diálogo y sus estilos; los dos modales que publiques en H3.S2.M1

Tu lote: `PR8-DialogoYEstados.Frontend/` — entregables en `PR8-DialogoYEstados.Frontend/entregables/`, evidencia en `PR8-DialogoYEstados.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR13-Ci.Frontend/`

- **Avance del bloque C:** 0 / 52 — 0 %. (5 hitos · 12 subtareas.)
- Entregables en `PR13-Ci.Frontend/entregables/`, evidencia en `PR13-Ci.Frontend/evidencia/`.
- **Tus reservas:** `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
