# Daily de Richard — turno día — 2026-09-20

> **AVANCE: 0 / 18 — 0 %.**
> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Richard · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `identidad` (M1)
- **Tu encargo:** [Identidad: tokens que no se filtran, documento único y niveles que el servidor hace cumplir](Dia1-Identidad.Servicio/TokensKYCYContratoDeIdentidad.md)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../Daily-Dia-2026-09-20.md)
- **3 hitos · 6 subtareas · 18 microtareas**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → pegar salida abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → pegar salida abajo.
- [ ] Skills cargadas: `kyc-identity-verification` · `authn-identity` · `authz-access-control` · `data-privacy-financial` · `terminology-value-sets` · `service-contracts-versioning` · `service-to-service-security` · `api-testing`

```text
$ ls .claude/skills | wc -l
<pegar>
$ python .claude/hooks/plan_gate.py --self-test
<pegar>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| **H1** — Tokens de verificación que nunca guardan el valor plano | 6 | 0 | `TODO` |
| **H2** — Documento único y niveles que el servidor hace cumplir | 6 | 0 | `TODO` |
| **H3** — El contrato que los demás servicios consumen | 6 | 0 | `TODO` |
| **TOTAL** | **18** | **0** | **0 / 18 = 0 %** |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| | | | |

## 4. A medias — las cuatro respuestas, obligatorias

Ninguna todavía. **No borrar esta sección:** su ausencia se lee como que no hubo nada que decir.

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| | | | | |

> Regla 65: si el contrato de lo que falta se puede nombrar, **se simula en tres niveles
> —correcto, límite, inválido— y se cierra contra el doble**, declarándolo. Solo una decisión de
> negocio o una acción destructiva sobre algo compartido justifican dejarlo abierto.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| | | | |

## 7. No cubierto

Lo que se hizo pero **no** se probó. Distinto de pendiente.

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-R1 | ¿Qué proveedor de verificación biométrica se va a usar y qué devuelve exactamente? | Negocio / coordinación | `ABIERTA` |
| Q-R2 | ¿Cuánto dura un KYC antes de exigir revalidación? | Cumplimiento | `ABIERTA` |
