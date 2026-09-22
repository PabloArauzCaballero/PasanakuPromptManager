# Daily de Pablo — turno noche — área frontend — 2026-09-21

> **AVANCE: 2 / 38 — 5,3 %.** ← sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> **Estado:** `IN_PROGRESS`. Ejecución real arrancada 2026-09-21 contra `Pasanaku/PasanakuFrontend`.

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
| H1 — La base y el runtime actual del catálogo auditados | 7 | 2 | EN CURSO |
| H2 — Las cuatro pruebas de fidelidad, por separado | 7 | 0 | TODO |
| H3 — Escenarios explícitos, no props adivinadas | 7 | 0 | TODO |
| H4 — El preview aislado de verdad | 7 | 0 | TODO |
| H5 — Los gates y el cierre del alcance | 10 | 0 | TODO |
| **TOTAL** | **38** | **2** | |

## 4. Qué quedó andando (con evidencia)

Solo entra acá lo que tiene su Definition of Done ejecutado y su salida literal pegada.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Rama `pablo/frontend/catalogo-ui` creada desde `origin/dev` @ `a23bcb1`, árbol limpio | `git rev-parse HEAD && git status --short` | HECHO — `evidencia/baseline.md` |
| H1.S2.M1 | Auditado el runtime real del catálogo: importa la implementación canónica (no copia), sin iframe, montado como ruta `loadComponent` en `apps/web` | lectura citada archivo:línea | HECHO — `entregables/auditoria-catalogo.md` |

## 5. A medias — las cuatro respuestas, obligatorias

### <ID> — <título>
- **Qué anda:**
- **Qué no anda:**
- **Qué falta exactamente:**
- **Dónde quedó:** <rama, archivos, si compila>

## 6. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|

> Regla 65: si el contrato de lo que falta **se puede nombrar, se simula en tres niveles**
> —correcto, límite, inválido— y se cierra contra el doble, declarándolo. Solo una decisión de
> negocio o una acción destructiva sobre algo compartido justifican dejarlo abierto.

## 7. Hallazgos para el equipo

Lo roto que encontrás fuera de tu alcance va acá con su ruta. **No se arregla** (regla 00 §3).

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| F-1 | `packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts:26` — 2 errores de lint preexistentes (`click-events-have-key-events`, `interactive-supports-focus`) | Dueño de `foco-de-tutorial` (fuera de las reservas de este carril) | ABIERTO |
| F-2 | `packages/ui/src/monto/monto.spec.ts:21` — test "pasa los mismos vectores que el Monto de Flutter" falla por timeout de 5000ms, preexistente | Dueño de `monto` (fuera de las reservas de este carril) | ABIERTO |

## 8. No cubierto

- H1.S2.M2 (aislamiento del preview): la lectura de código sugiere que el catálogo **comparte**
  inyectores/router/sesión con el anfitrión (es una ruta `loadComponent` normal de `apps/web`, sin
  iframe ni entrada propia), pero **no se ejecutó todavía** la comprobación real que exige el DoD.
  No se afirma como verificado.
- H1.S1.M4 (bundle size): no medido — requiere build real de `apps/web`/`apps/backoffice`, no
  corrido por tiempo.
- `packages/diseno_flutter` (equivalente Flutter del catálogo): nada corrido — Flutter no está
  instalado en esta máquina.
- El resto de H1 (H1.S2.M3) y la totalidad de H2–H5 (31 microtareas): no arrancadas.

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F6 | Cuál es el runner de cada capa, con tres coexistiendo | Vos, en H1.S1.M2 — y lo publicás para los cinco | ABIERTA |
| Q-P1 | Si el preview sigue compartiendo cookies o almacenamiento con el anfitrión | Tu comprobación (H4.S1.M3) | ABIERTA |
| Q-P2 | Si se puede verificar algo contra un entorno compartido | Coordinación / dueño del entorno | ABIERTA |
| Q-P3 | Qué organismos de Justin y Leo llegan a tiempo para acreditar sus fichas | Justin y Leo, durante el turno | ABIERTA |
| Q-P4 | Si el repo frontend tiene CI y qué corre hoy | Tu baseline | ABIERTA |

## 10. Tus reservas de archivos en este turno

el runtime del catálogo y su ficha; la entrada de preview; el generador de props sintéticas; la configuración de CI; el documento de cierre y el registro de ejecución

Tu lote: `PR10-CatalogoYGates.Frontend/` — entregables en `PR10-CatalogoYGates.Frontend/entregables/`, evidencia en `PR10-CatalogoYGates.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR15-Contratos.Frontend/`

- **Avance del bloque C:** 0 / 58 — 0 %. (5 hitos · 10 subtareas.)
- Entregables en `PR15-Contratos.Frontend/entregables/`, evidencia en `PR15-Contratos.Frontend/evidencia/`.
- **Tus reservas:** `.gitignore`, `.gitattributes`, `clientes/**`, `docs/auditoria/**`, los ADR, `scripts/verificar_remotos.sh`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
