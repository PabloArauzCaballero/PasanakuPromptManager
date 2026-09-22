# Daily de Justin — turno noche — área frontend — 2026-09-21

> **AVANCE FORMAL PR7: 0 / 27 — 0 %.** No se reconstruye el porcentaje a partir de commits sin cerrar cada DoD.
> **Estado:** `A MEDIAS`. Revisión 2026-09-22: PR7 está integrado en `dev`; PR12 tiene una rama de reconciliación con gates Angular verdes y Flutter sin verificar en este entorno.

- **Persona:** Justin · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [La tabla canónica: un contrato, cero banderas por pantalla, y dos consumidores reales migrados](PR7-DataTable.Frontend/TablaCanonicaYDosConsumidores.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 42 microtareas → [Justin-Daily-Noche-2026-09-21.md](../../Backend/Justin/Justin-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Corrección 2026-09-21 (Pablo, en sesión):** este bloque B se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura).
  Confirmado: también es trabajo de Pasanaku. Ver
  [docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md](../../../../../docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md).
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `PasanakuFrontend` · rama base `dev` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 36 microtareas → [Producción no muestra cifras inventadas ni llama a la máquina del usuario](PR12-Config.Frontend/ConfiguracionFailFastYMocksAislados.md)
  - **Mismo repo que el bloque B desde la corrección de hoy:** los dos bloques son `PasanakuBackend`/`PasanakuFrontend` (antes, el bloque B decía `mantra-core-health`, otro repo). La regla 91 (dinero) y la 98 (microservicios) aplican en los dos bloques donde corresponda.
  - **Orden del turno:** A (backend) → B (tabla de datos) → C (config). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** datos simulados aislados, configuración fail-fast y estados de UI.
  - **Tus reservas en el bloque C:** los dos `nucleo/gateway.ts`, `rutas/sistemas/**`, `packages/simulado/**`, `dominio-cliente/src/configuracion.ts`, `movil/lib/dominio/configuracion.dart`. Ningún otro carril las toca, y vos no tocás las suyas.

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
| H1 — La base y el mapa de usos de la tabla | 7 | 0 | A MEDIAS — implementación integrada, DoD no reconstruido |
| H2 — El contrato escrito antes de tocar la implementación | 7 | 0 | A MEDIAS — implementación integrada, DoD no reconstruido |
| H3 — Una implementación, variantes con significado | 7 | 0 | A MEDIAS — implementación integrada, DoD no reconstruido |
| H4 — Dos consumidores reales la usan y la vieja se retira | 6 | 0 | A MEDIAS — implementación integrada, DoD no reconstruido |
| **TOTAL** | **27** | **0** | |

## 4. Qué quedó andando (con evidencia)

Solo entra acá lo que tiene su Definition of Done ejecutado y su salida literal pegada.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| PR7, revisión 2026-09-22 | `origin/justin/frontend/tabla-datos` no difiere de `origin/dev`; la tabla y sus dos consumidores ya están integrados | `git diff --quiet origin/dev origin/justin/frontend/tabla-datos` | exit 0 (árboles iguales) |
| PR12, revisión 2026-09-22 | Los fixes de configuración se reconciliaron sobre `dev` limpio | `test:front`, `test:a11y`, `build` de backoffice | 296 unitarios, 32 a11y y build verdes |

## 5. A medias — las cuatro respuestas, obligatorias

### PR7 — Cierre documental pendiente
- **Qué anda:** la rama remota de tabla tiene el mismo árbol que `dev`; no hay cambio de producto por fusionar.
- **Qué no anda:** sus 27 DoD no se registraron microtarea a microtarea en este daily.
- **Qué falta exactamente:** recuperar o ejecutar evidencia dirigida antes de marcar microtareas `HECHO`.
- **Dónde quedó:** `origin/dev`; no hay rama pendiente de PR7.

### PR12 — Reconciliación de gates de configuración
- **Qué anda:** `justin/fix/pr12-reconciliacion` incorpora los dos fixes pendientes; backoffice pasa 296 tests unitarios, 32 a11y y build de producción.
- **Qué no anda:** no hay SDK Flutter en `PATH`, por lo que no se ejecutaron sus 21 tests ni análisis; el cableado del componente raíz sigue siendo de Richard.
- **Qué falta exactamente:** ejecutar Flutter en un entorno con SDK, abrir/mergear la PR y que Richard cablee `app.config.ts`/raíz según `entregables/cableado-app-config.md`.
- **Dónde quedó:** rama `justin/fix/pr12-reconciliacion` sobre `origin/dev`.

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

## 8. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F7 | Que los dos consumidores no choquen con la pantalla piloto de Richard | Coordinación, primera hora | ABIERTA |
| Q-J1 | Cuántas variantes tiene el tipo de estado real | Leo (PR8), primera hora | ABIERTA |
| Q-J2 | Si la paginación es por cursor o por índice | Tu baseline (H1.S2.M1) | ABIERTA |
| Q-J3 | Si alguna diferencia entre las dos pantallas es de dominio y no decoración | Coordinación / producto | ABIERTA |

## 10. Tus reservas de archivos en este turno

el organismo de tabla y sus estilos; los dos consumidores que publiques en H1.S2.M2

Tu lote: `PR7-DataTable.Frontend/` — entregables en `PR7-DataTable.Frontend/entregables/`, evidencia en `PR7-DataTable.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR12-Config.Frontend/`

- **Avance formal del bloque C:** 0 / 36 — 0 %. La implementación está avanzada, pero no se reasigna un porcentaje sin el cierre por DoD; ver PR12 arriba.
- Entregables en `PR12-Config.Frontend/entregables/`, evidencia en `PR12-Config.Frontend/evidencia/`.
- **Tus reservas:** los dos `nucleo/gateway.ts`, `rutas/sistemas/**`, `packages/simulado/**`, `dominio-cliente/src/configuracion.ts`, `movil/lib/dominio/configuracion.dart`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
