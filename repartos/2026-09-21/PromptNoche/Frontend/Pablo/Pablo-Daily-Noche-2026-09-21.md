# Daily de Pablo — turno noche — área frontend — 2026-09-21

> **AVANCE: 8 / 38 — 21,1 %.** ← sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha
> (quedan 3 en A MEDIAS: H1.S1.M2, H1.S1.M3, H5.S1.M3; 14 BLOQUEADO por Q-P5).
> **Estado:** `IN_PROGRESS`. F-4 (JDK) resuelto en sesión — desbloqueó H1.S1.M4, H1.S2.M2 y H2.S1.M4.

- **Persona:** Pablo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [El catálogo que monta el componente real, el preview aislado de verdad, y los gates que no se pueden falsear](PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 54 microtareas → [Pablo-Daily-Noche-2026-09-21.md](../../Backend/Pablo/Pablo-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Corrección 2026-09-21 (Pablo, en sesión):** este bloque B se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura —
  `AMB-F2`). Pablo confirmó que también es trabajo de Pasanaku: repo y rama corregidos abajo. Ver
  [docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku/PLAN.md](../../../../../docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku/PLAN.md).
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `PasanakuFrontend` · rama base `dev` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 58 microtareas → [La línea base que nadie discute, los contratos como frontera y el cierre con hechos](PR15-Contratos.Frontend/LineaBaseContratosAuthzYCierre.md)
  - **Mismo repo que el bloque B desde la corrección de hoy:** los dos bloques son `PasanakuBackend`/`PasanakuFrontend` (antes, el bloque B decía `mantra-core-health`, otro repo). La regla 91 (dinero) y la 98 (microservicios) aplican en los dos bloques donde corresponda — ver la nota de reglas de `PR10` para el detalle del bloque B.
  - **Orden del turno:** A (backend) → B (catálogo) → C (contratos). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** línea base global, clientes versionados, autorización, idempotencia, contratos y cierre.
  - **Tus reservas en el bloque C:** `.gitignore`, `.gitattributes`, `clientes/**`, `docs/auditoria/**`, los ADR, `scripts/verificar_remotos.sh`. Ningún otro carril las toca, y vos no tocás las suyas.

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
| `CMD_LINT` | | |
| `CMD_TYPECHECK` | | |
| `CMD_TEST` | | |
| `CMD_BUILD` | | |
| `CMD_E2E` | | |

## 3. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — La base y el runtime actual del catálogo auditados | 7 | 4 | EN CURSO |
| H2 — Las cuatro pruebas de fidelidad, por separado | 7 | 4 | EN CURSO |
| H3 — Escenarios explícitos, no props adivinadas | 7 | 0 | BLOQUEADO (Q-P5) |
| H4 — El preview aislado de verdad | 7 | 0 | BLOQUEADO (Q-P5) |
| H5 — Los gates y el cierre del alcance | 10 | 0 | EN CURSO |
| **TOTAL** | **38** | **8** | |

## 4. Qué quedó andando (con evidencia)

Solo entra acá lo que tiene su Definition of Done ejecutado y su salida literal pegada.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Rama `pablo/frontend/catalogo-ui` creada desde `origin/dev` @ `a23bcb1`, árbol limpio | `git rev-parse HEAD && git status --short` | HECHO — `evidencia/baseline.md` |
| H1.S2.M1 | Auditado el runtime real del catálogo: importa la implementación canónica (no copia), sin iframe, montado como ruta `loadComponent` en `apps/web` | lectura citada archivo:línea | HECHO — `entregables/auditoria-catalogo.md` |
| H2.S1.M1 | Fuente confirmada: `packages/ui/src/catalogo.spec.ts` (test existente, no escrito por mí) pasa contra la implementación real | `yarn workspace @aportaya/ui test:front` | HECHO — 13/14 archivos, 46/47 tests, catálogo entre los que pasan |
| H2.S1.M2 | Composición confirmada: el mismo test verifica contenido real montado, no un contenedor vacío | mismo comando | HECHO |
| — | Gate de accesibilidad automático del catálogo (axe, claro y oscuro + área táctil) — test existente, no escrito por mí | `yarn workspace @aportaya/ui test:a11y` | HECHO — `3 passed (3)` |
| H2.S1.M3 | Interacción con salida observable: escribí `catalogo-interaccion.spec.ts`, click real → output `pulsado` del primer `ap-boton` | `yarn workspace @aportaya/ui test:front` | HECHO — 14/15 archivos, 47/48 tests (único rojo: `monto.spec.ts`, preexistente) |
| F-4 resuelto | Instalé JDK 21, generé los 14 clientes Angular reales | `./gradlew :servicios:*:generarClienteAngular` | HECHO — `BUILD SUCCESSFUL`, `clientes/angular/` con 14 carpetas |
| H1.S1.M4 | Build real de `apps/web`, bundle del catálogo medido: 160.03 kB, lazy chunk separado del inicial | `yarn workspace @aportaya/web build` | HECHO — exit 0 |
| H1.S2.M2 | Aislamiento demostrado con E2E real: el catálogo **comparte** `localStorage` con el anfitrión, sin iframe | `yarn workspace @aportaya/web test:e2e catalogo-aislamiento` | HECHO — `2 passed (2.5s)` |
| H2.S1.M4 | Capturas reales por tema/viewport generadas y miradas, catálogo maduro y consistente | `yarn workspace @aportaya/web test:e2e catalogo.spec` | HECHO — `4 passed (5.1s)` |

## 5. A medias — las cuatro respuestas, obligatorias

### H1.S1.M2/M3 — Comandos publicados y baseline de fallos
- **Qué anda:** comandos reales confirmados y pegados (`turbo run lint/typecheck/test:front/build`); lint, typecheck, test y build corridos sobre `packages/ui` con exit code real.
- **Qué no anda:** no se publicaron en un daily de equipo real (no hay turno coordinado); no se corrió cobertura; el scope fue solo `packages/ui`, no el repo entero.
- **Qué falta exactamente:** correr `<CMD_LINT>`/`<CMD_TYPECHECK>`/`<CMD_TEST>`/`<CMD_BUILD>` a nivel de todo el repo, no solo `packages/ui`.
- **Dónde quedó:** `evidencia/baseline.md`, rama `pablo/frontend/catalogo-ui`, nada commiteado.

### H2.S1.M4 — Apariencia (capturas del catálogo)
- **Qué anda:** el spec real ya existe (`apps/web/pruebas/e2e/catalogo.spec.ts`) y hace exactamente lo que pide el DoD (capturas por tema/viewport, chequeo de 44px, no-indexado).
- **Qué no anda:** no se pudo correr — `apps/web` no compila hoy.
- **Qué falta exactamente:** resolver F-4 (generar `clientes/angular`, necesita JDK) o simular contra un doble, y entonces correr `yarn workspace @aportaya/web test:e2e`.
- **Dónde quedó:** sin tocar, spec preexistente sin ejecutar.

### H5.S1.M3 — Gate de accesibilidad
- **Qué anda:** la parte automática (axe) corre y pasa, 3/3.
- **Qué no anda:** no hay recorrido documentado por teclado.
- **Qué falta exactamente:** navegar el catálogo entero solo con teclado y describir el recorrido en `entregables/`.
- **Dónde quedó:** nada escrito todavía para el recorrido manual.

## 6. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H1.S2.M2, H2.S1.M4, H4 completo | Toda comprobación que necesite `apps/web` compilando (aislamiento, capturas, E2E) | Build real (`yarn workspace @aportaya/web build`); typecheck completo; normalicé localmente el CRLF de `contenido/legal/*.md` (F-3) para descartar esa causa | Generar `clientes/angular/{grupos,tarifas,transparencia}` — necesita JDK, no instalado en esta máquina (confirmado, ver memoria de sesión anterior). Es literalmente H2.S1.M1 de mi propio bloque C (`PR15`) | Instalar JDK en esta máquina, o que alguien con JDK genere y commitee `clientes/` |

> Regla 65: si el contrato de lo que falta **se puede nombrar, se simula en tres niveles**
> —correcto, límite, inválido— y se cierra contra el doble, declarándolo. Solo una decisión de
> negocio o una acción destructiva sobre algo compartido justifican dejarlo abierto.

## 7. Hallazgos para el equipo

Lo roto que encontrás fuera de tu alcance va acá con su ruta. **No se arregla** (regla 00 §3).

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| F-1 | `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` — 2 errores de lint preexistentes (`click-events-have-key-events`, `interactive-supports-focus`) | Dueño de `foco-de-tutorial` (fuera de las reservas de este carril) | ABIERTO |
| F-2 | `packages/ui/src/monto/monto.spec.ts:21` — test "pasa los mismos vectores que el Monto de Flutter" falla por timeout de 5000ms, preexistente | Dueño de `monto` (fuera de las reservas de este carril) | ABIERTO |
| F-3 | Todos los `.md` de `apps/web/contenido/**` tienen CRLF (confirmado con `file`), y el parser de `apps/web/scripts/contenido.mjs:23` exige `\n` exacto (`/^---\n(...)\n---\n/`), así que el build de `apps/web` falla en **cualquier checkout Windows** con `core.autocrlf=true` (`git config core.autocrlf` → `true` en esta máquina) sin un `.gitattributes` que fuerce LF en `contenido/**`. Normalicé los `.md` localmente (sin commitear) solo para poder seguir probando. `.gitattributes` es reserva de mi propio bloque C (`PR15`) — lo resuelvo ahí | Quien mantiene `apps/web/scripts/contenido.mjs`, y yo mismo en `PR15` | ABIERTO — mitigado localmente, no corregido en el repo |
| F-4 | `apps/web` no compilaba: faltaban `clientes/angular/{grupos,tarifas,transparencia}` (entre otros) | — | **RESUELTO 2026-09-22**: instalé JDK 21 Temurin (`winget install EclipseAdoptium.Temurin.21.JDK` — ya estaba instalado, solo faltaba en el PATH de la sesión) y corrí `./gradlew :servicios:{aportes,auditoria,cumplimiento,entregas,erp,garantia,grupos,identidad,notificaciones,nucleo-financiero,organizador,publicidad,tarifas,transparencia}:generarClienteAngular` → `BUILD SUCCESSFUL`, 14 clientes generados en `clientes/angular/`. `yarn workspace @aportaya/web build` → exit 0 |
| F-5 | `apps/web/playwright.config.ts:37` arranca el server con sintaxis Unix (`PORT=4173 ... node ...`), que no corre en `cmd.exe` de Windows (`"PORT" no se reconoce como un comando`). Lo rodeé arrancando el server a mano con las variables exportadas para poder correr el E2E; no toqué el archivo (no es mi reserva) | Dueño de `apps/web/playwright.config.ts` (Justin, PR12, reserva `nucleo/gateway.ts`/`rutas/sistemas` — no es exactamente este archivo; a confirmar de quién es) | ABIERTO — afecta a cualquiera que corra `test:e2e` de `apps/web` en Windows sin un shell compatible |

## 8. No cubierto

- H1.S2.M2 (aislamiento del preview): la lectura de código sugiere que el catálogo **comparte**
  inyectores/router/sesión con el anfitrión (es una ruta `loadComponent` normal de `apps/web`, sin
  iframe ni entrada propia), pero **no se ejecutó todavía** la comprobación real que exige el DoD.
  **Actualizado:** ya se demostró con E2E real (H1.S2.M2 → HECHO). Esta línea queda como registro
  histórico de que primero fue hipótesis y después prueba, no al revés.
- `apps/backoffice` no se buildeó todavía (solo `apps/web`) — sus propios `clientes/angular` ya
  existen (generados junto con los de `apps/web`, son el mismo `clientes/angular/`), pero no se
  corrió su build/typecheck/E2E en esta sesión.
- `packages/diseno_flutter` (equivalente Flutter del catálogo): nada corrido — Flutter no está
  instalado en esta máquina (JDK sí, ahora; Flutter sigue sin instalar).
- Las capturas se miraron a resolución de escritorio en la revisión de esta sesión; no se hizo una
  comparación pixel a pixel contra un baseline anterior (no existía uno).
- **`H3` (factories/hosts/edición) y `H4` (preview aislado) completos — 14 microtareas — resultaron
  `BLOQUEADO`, no `TODO`: asumen un catálogo tipo playground editable con preview en iframe que el
  catálogo real de Pasanaku no tiene (es una página estática). Ver `Q-P5` y
  `entregables/auditoria-catalogo.md`.**
- H1.S2.M3 (generador de props): no localicé ninguno — coherente con el hallazgo de arriba, las
  props están escritas a mano, no generadas.

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F6 | Cuál es el runner de cada capa, con tres coexistiendo | Vos, en H1.S1.M2 — y lo publicás para los cinco | ABIERTA |
| **Q-P5** | **`H3`/`H4` (14 microtareas) asumen un playground editable con preview aislado en iframe. El catálogo real es una página estática sin eso. Construirlo es una funcionalidad nueva (semanas), no una auditoría** | **Coordinación/producto: ¿se construye, o se recorta el alcance de `H3`/`H4` a "no aplica, catálogo estático"?** | **ABIERTA — bloquea 14/38 microtareas** |
| Q-P1 | Si el preview sigue compartiendo cookies o almacenamiento con el anfitrión | Tu comprobación (H4.S1.M3) | ABIERTA |
| Q-P2 | Si se puede verificar algo contra un entorno compartido | Coordinación / dueño del entorno | ABIERTA |
| Q-P3 | Qué organismos de Justin y Leo llegan a tiempo para acreditar sus fichas | Justin y Leo, durante el turno | ABIERTA |
| Q-P4 | Si el repo frontend tiene CI y qué corre hoy | Tu baseline | ABIERTA |

## 10. Tus reservas de archivos en este turno

el runtime del catálogo y su ficha; la entrada de preview; el generador de props sintéticas; la configuración de CI; el documento de cierre y el registro de ejecución

Tu lote: `PR10-CatalogoYGates.Frontend/` — entregables en `PR10-CatalogoYGates.Frontend/entregables/`, evidencia en `PR10-CatalogoYGates.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR15-Contratos.Frontend/`

- **Avance del bloque C:** 32 / 58 — 55,2 %. (H5.S3.M1 sumó los seis riesgos residuales reales de
  `docs/auditoria/riesgos.md`, con dueño, incluyendo el hallazgo nuevo de que la clave de
  idempotencia no sobrevive un reintento tras timeout.) (`grep -cE '^\| H[0-9]+\.S[0-9]+\.M[0-9]+ \|'` sobre
  el plan → 58 filas; 31 `HECHO`.) `H1` completo (4/4). `H2.S1` completo salvo M4 (kill-test
  estricto en clon nuevo, A MEDIAS). `H2.S2` 5/7 — M6/M7 (hallazgos y línea base) A MEDIAS porque
  sus DoD piden consolidar lo que midieron/encontraron Richard/Leo/Justin/Marcelo, fuera de mi
  alcance producir por ellos. `H3.S1` 4/5 — probé con un test real que la interfaz no es barrera
  de autorización (`crearCobro()` manda la petición igual sin pasar por el botón oculto; el
  servidor la rechaza con `403` y se traduce a texto de permiso, no error crudo). `H3.S2` 3/7,
  `H3.S3` 3/7 (+1 `BLOQUEADO` por falta de Flutter/Dart en esta máquina). Ocho documentos de
  `docs/auditoria/` creados con el plan madre copiado (247 microtareas parseables) y 13 hallazgos
  reales con evidencia — dos más confirmados en la corrida (`scripts/verificar_frontend.py` roto
  en Windows; `packages/ui/monto.spec.ts` en rojo, fuera de mi reserva). Commits en
  `pablo/frontend/contratos`: `1d96639` … `d61c3f7` (16 commits totales del bloque C). Probé
  también que el menú del backoffice se recalcula solo por construcción cuando cambian los
  permisos de la sesión (`shell-financiero.spec.ts`); la mitad que falta (redirigir fuera de una
  ruta que dejó de alcanzar) no existe y no se inventa sin confirmar la semántica — registrado
  como decisión pendiente, igual que la vida de la clave de idempotencia entre reintentos.
- Entregables en `PR15-Contratos.Frontend/entregables/`, evidencia en `PR15-Contratos.Frontend/evidencia/`.
- **Tus reservas:** `.gitignore`, `.gitattributes`, `clientes/**`, `docs/auditoria/**`, los ADR, `scripts/verificar_remotos.sh`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
