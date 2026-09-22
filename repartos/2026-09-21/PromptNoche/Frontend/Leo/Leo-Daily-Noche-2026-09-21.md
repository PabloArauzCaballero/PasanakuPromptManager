# Daily de Leo — turno noche — área frontend — 2026-09-21

> **AVANCE: 0 / 26 — 0 %.** ← sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como no hecha.
> **Estado:** `IN_PROGRESS`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Leo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Tu encargo:** [Diálogo, host de estados y borrador: la interacción compartida vive en un solo lugar](PR8-DialogoYEstados.Frontend/DialogoHostDeEstadosYBorrador.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Tu otro carril de este turno:** backend, 49 microtareas → [Leo-Daily-Noche-2026-09-21.md](../../Backend/Leo/Leo-Daily-Noche-2026-09-21.md). **Un trabajo activo por vez** (regla 70.1): el backend es el bloque A y este es el bloque B. El de backend se cierra, o se declara `A MEDIAS` con las cuatro respuestas, **antes** de abrir este.
- **Repo:** `https://github.com/mdavila-2001/mantra-core-health` · rama base `mockup` · **el SHA lo registrás vos en H1.S1.M1**

- **Tu SEGUNDO lote de esta área — bloque C · AportaYa:** 52 microtareas → [El CI deja de mentir: E2E del backoffice, dos jobs macOS, release iOS y cero `|| true`](PR13-Ci.Frontend/CiRealMacosYReleaseIos.md)
  - **Otro repo, otras reglas:** el bloque B es `mantra-core-health`; el bloque C es el monorepo de AportaYa, y ahí **sí aplican la regla 91 (dinero) y la 98 (microservicios)**.
  - **Orden del turno:** A (backend) → B (mantra) → C (AportaYa). **Un trabajo activo por vez** (regla 70.1): el anterior se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente.
  - **Qué te toca:** capabilities iOS, release iOS en macOS, humo honesto, CI real y cabeceras.
  - **Tus reservas en el bloque C:** `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts`. Ningún otro carril las toca, y vos no tocás las suyas.

## 1. Instalación del estándar — lo primero

- [ ] `.claude/` del estándar copiado o enlazado dentro de `mantra-core-health/`.
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
| H1 — La base y el contrato de estado publicado | 7 | 0 | TODO |
| H2 — El contrato de estado se renderiza en un solo lugar | 6 | 0 | TODO |
| H3 — El diálogo tiene anatomía, foco y una sola política de descarte | 7 | 0 | TODO |
| H4 — El formulario tiene un dueño y dos modales lo demuestran | 6 | 0 | TODO |
| **TOTAL** | **26** | **0** | |

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
| AMB-F3 | Que el tipo de estado tenga diez variantes y esos nombres | Tu baseline (H1.S2.M1) | ABIERTA |
| Q-L1 | Qué pasa con el borrador si la entidad cambia mientras se edita | Producto | ABIERTA |
| Q-L2 | Si la proyección alcanza o hace falta una plantilla diferida | Tu verificación en la versión instalada | ABIERTA |
| Q-L3 | Si algún modal evita a propósito la protección de descarte | Producto | ABIERTA |

## 10. Tus reservas de archivos en este turno

el tipo de estado y su contrato; el host de estados; el organismo de diálogo y sus estilos; los dos modales que publiques en H3.S2.M1

Tu lote: `PR8-DialogoYEstados.Frontend/` — entregables en `PR8-DialogoYEstados.Frontend/entregables/`, evidencia en `PR8-DialogoYEstados.Frontend/evidencia/`.
**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Bloque C — AportaYa · `PR13-Ci.Frontend/`

- **Avance del bloque C:** 0 / 52 — 0 %. (5 hitos · 12 subtareas.)
- Entregables en `PR13-Ci.Frontend/entregables/`, evidencia en `PR13-Ci.Frontend/evidencia/`.
- **Tus reservas:** `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts`.
- Verificado sin colisiones: `python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 0 colisiones.
