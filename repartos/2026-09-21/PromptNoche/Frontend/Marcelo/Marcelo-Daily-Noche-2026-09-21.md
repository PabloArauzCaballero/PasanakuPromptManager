# Daily de Marcelo — turno noche — área frontend — 2026-09-21

> **AVANCE: 0 / 31 — 0 %.** ← sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> **Estado:** `IN_PROGRESS`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Marcelo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [El mapa que no miente: inventario con procedencia, grafo de usos diferenciado y matriz de familias](PR9-InventarioYFamilias.Frontend/InventarioGrafoDeUsosYFamilias.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 40 microtareas → [Marcelo-Daily-Noche-2026-09-21.md](../../Backend/Marcelo/Marcelo-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Corrección 2026-09-21 (Pablo, en sesión):** este bloque B se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura).
  Confirmado: también es trabajo de Pasanaku. Ver
  [docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md](../../../../../docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md).
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `PasanakuFrontend` · rama base `dev` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 59 microtareas → [Fronteras que se hacen cumplir solas, un núcleo compartido y un proxy que deja de ser accidental](PR14-Fronteras.Frontend/FronterasNucleoCompartidoYCalidad.md)
  - **Mismo repo que el bloque B desde la corrección de hoy:** los dos bloques son `PasanakuBackend`/`PasanakuFrontend` (antes, el bloque B decía `mantra-core-health`, otro repo). La regla 91 (dinero) y la 98 (microservicios) aplican en los dos bloques donde corresponda.
  - **Orden del turno:** A (backend) → B (inventario) → C (fronteras). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** exports explícitos, boundaries, núcleo HTTP compartido, errores, telemetría y calidad.
  - **Tus reservas en el bloque C:** `packages/{ui,tutoriales}/package.json`, el package de núcleo HTTP, `tsconfig.base.json`, los dos `eslint.config.js`, `web/src/server.ts`, `web/src/app/app.routes.ts`, `scripts/verificar_frontend.py`. Ningún otro carril las toca, y vos no tocás las suyas.

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
| H1 — La base y el generador actual auditados | 7 | 0 | TODO |
| H2 — El inventario se resuelve con el compilador | 7 | 0 | TODO |
| H3 — El grafo distingue relaciones | 7 | 0 | TODO |
| H4 — La matriz de familias decide con evidencia y contraejemplo | 7 | 0 | TODO |
| H5 — Se retira lo que de verdad quedó sin consumidores | 3 | 0 | TODO |
| **TOTAL** | **31** | **0** | |

## 4. Qué quedó andando (con evidencia)

Solo entra acá lo que tiene su Definition of Done ejecutado y su salida literal pegada.

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|

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

## 8. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 9. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-M1 | Qué herramienta de análisis usar si el repo no trae ninguna capaz de resolver plantillas | Coordinación | ABIERTA |
| Q-M2 | Si el inventario es todo el frontend o un subconjunto | Coordinación | ABIERTA |
| Q-M3 | Si una diferencia entre dos piezas parecidas es de dominio | Producto | ABIERTA |
| Q-M4 | Qué consumidores están comprometidos por PR6, PR7 y PR8 | Richard, Justin y Leo, primera hora | ABIERTA |

## 10. Tus reservas de archivos en este turno

el generador del índice y sus artefactos generados; los documentos de inventario, grafo y familias

Tu lote: `PR9-InventarioYFamilias.Frontend/` — entregables en `PR9-InventarioYFamilias.Frontend/entregables/`, evidencia en `PR9-InventarioYFamilias.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR14-Fronteras.Frontend/`

- **Avance del bloque C:** 0 / 59 — 0 %. (5 hitos · 13 subtareas.)
- Entregables en `PR14-Fronteras.Frontend/entregables/`, evidencia en `PR14-Fronteras.Frontend/evidencia/`.
- **Tus reservas:** `packages/{ui,tutoriales}/package.json`, el package de núcleo HTTP, `tsconfig.base.json`, los dos `eslint.config.js`, `web/src/server.ts`, `web/src/app/app.routes.ts`, `scripts/verificar_frontend.py`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
