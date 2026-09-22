# Daily de Richard — turno noche — 2026-09-21

> **AVANCE: 0 / 28 — 0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`.

- **Persona:** Richard · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** `identidad`
- **Tu encargo:** [Identidad: challenge MFA con propósito, evidencia step-up y arranque seguro](PR1-Identidad.Servicio/StepUpMfaJwtYArranqueSeguro.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Rama:** `richard/feature/carril-PR1-identidad` → PRs a `dev`, espejo a `test`

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `authn-identity`, `environment-secrets-config`, `security-guardrails`, `data-privacy-financial`, `audit-trail-history`, `api-testing`, `test-case-design-techniques`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — Desafío MFA con propósito y evidencia step-up | 11 | 0 | TODO |
| H2 — Arranque seguro: clave obligatoria, `iss`/`aud`, JWKS con solapamiento | 8 | 0 | TODO |
| H3 — Refresh, contraseñas, propiedad y métricas | 9 | 0 | TODO |
| **TOTAL** | **28** | **0** | |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|

## 4. A medias — las cuatro respuestas, obligatorias

### <ID> — <título>
- **Qué anda:**
- **Qué no anda:**
- **Qué falta exactamente:**
- **Dónde quedó:** <rama, archivos, si compila>

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|

> Recordá la regla 65: si el contrato de lo que falta se puede nombrar, **se simula en tres
> niveles y se cierra**. En este encargo el proveedor de OTP ya viene con su doble (H1.S1.M4)
> y el decodificador de Leo no te hace falta para emitir. Solo una decisión de negocio queda abierta.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-3) | Factor real del desafío | — | DECIDIDA: TOTP interno + OTP por `notificaciones`; ver encargo §5 |
| Q-02 (AMB-2) | `aud` global vs por servicio | — | DECIDIDA: acceso `["aportaya"]`, evidencia `["aportaya-nucleo-financiero"]` |
| Q-03 | `token_verificacion` vs `desafio_mfa` | — | DECIDIDA: reutilizar `token_verificacion` con `proposito='MFA_RETIRO'` |
| Q-04 | Parámetros Argon2 vs OWASP | — | DECIDIDA: piso `m ≥ 19456 KiB`, `t ≥ 2`, `p = 1` |
