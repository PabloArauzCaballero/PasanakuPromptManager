# Daily de Richard — turno noche — área frontend — 2026-09-21

> **AVANCE: 0 / 24 — 0 %.** ← sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> **Estado:** `IN_PROGRESS`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Richard · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [Quién decide y quién dibuja: la pantalla piloto con su estado con dueño y su plantilla declarativa](PR6-SmartPresentational.Frontend/QuienDecideYQuienDibuja.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 28 microtareas → [Richard-Daily-Noche-2026-09-21.md](../../Backend/Richard/Richard-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Corrección 2026-09-21 (Pablo, en sesión):** este bloque B se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura —
  `AMB-F2`). Confirmado: también es trabajo de Pasanaku. Ver
  [docs/trabajo/2026-09-21-correccion-bloques-richard-y-pablo-c/PLAN.md](../../../../../docs/trabajo/2026-09-21-correccion-bloques-richard-y-pablo-c/PLAN.md).
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `PasanakuFrontend` · rama base `dev` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 51 microtareas → [La sesión deja de mentir: un refresh, una restauración y una auditoría que no finge](PR11-Sesion.Frontend/RefrescoRestauracionYAuditoria.md)
  - **Mismo repo que el bloque B desde la corrección de hoy:** los dos bloques son `PasanakuBackend`/`PasanakuFrontend` (antes, el bloque B decía `mantra-core-health`, otro repo). La regla 91 (dinero) y la 98 (microservicios) aplican en los dos bloques donde corresponda.
  - **Orden del turno:** A (backend) → B (pantalla piloto) → C (sesión). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** refresh single-flight, restauración de sesión y auditoría de lectura.
  - **Tus reservas en el bloque C:** `nucleo/sesion*`, `permisos.ts`, `registro-de-acceso*`, `app.config.ts`, `rutas/ingreso/**`, `movil/lib/dominio/cliente.dart`, `movil/lib/proveedores/sesion.dart`. Ningún otro carril las toca, y vos no tocás las suyas.

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
| H1 — La base es un hecho registrado | 8 | 0 | TODO |
| H2 — Cada estado mutable tiene dueño escrito | 6 | 0 | TODO |
| H3 — El contenedor decide y la presentación dibuja | 7 | 0 | TODO |
| H4 — La paridad está demostrada | 3 | 0 | TODO |
| **TOTAL** | **24** | **0** | |

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
| AMB-F7 | Que la pantalla piloto no choque con los consumidores de Justin | Coordinación, primera hora | ABIERTA |
| Q-R1 | Si la pantalla piloto usa el organismo tabla que Justin reemplaza | Justin + coordinación | ABIERTA |
| Q-R2 | Cuántas variantes tiene el contrato de estado real | Leo (PR8), primera hora | ABIERTA |

## 10. Tus reservas de archivos en este turno

la pantalla piloto que publiques en H1.S2.M1 y los componentes privados de esa pantalla

Tu lote: `PR6-SmartPresentational.Frontend/` — entregables en `PR6-SmartPresentational.Frontend/entregables/`, evidencia en `PR6-SmartPresentational.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR11-Sesion.Frontend/`

- **Avance del bloque C:** 0 / 51 — 0 %. (4 hitos · 11 subtareas.)
- Entregables en `PR11-Sesion.Frontend/entregables/`, evidencia en `PR11-Sesion.Frontend/evidencia/`.
- **Tus reservas:** `nucleo/sesion*`, `permisos.ts`, `registro-de-acceso*`, `app.config.ts`, `rutas/ingreso/**`, `movil/lib/dominio/cliente.dart`, `movil/lib/proveedores/sesion.dart`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
