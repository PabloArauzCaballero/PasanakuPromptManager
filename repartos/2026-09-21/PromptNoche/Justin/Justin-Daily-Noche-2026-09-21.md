# Daily de Justin — turno noche — 2026-09-21

> **AVANCE: 0 / 42 — 0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`.

- **Persona:** Justin · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** `nucleo-financiero`
- **Tu encargo:** [Núcleo financiero: idempotencia con scope, MFA step-up y doble aprobación de retiro](PR2-NucleoFinanciero.Servicio/IdempotenciaMfaYDobleAprobacionDeRetiro.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../Daily-Noche-2026-09-21.md)
- **Rama:** `justin/feature/carril-PR2-nucleo-financiero` → PRs a `dev`, espejo a `test`

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `money-movement-safety`, `concurrency-and-locking`, `state-machines-workflows`, `authz-access-control`, `disbursement-payouts`, `resilience-patterns`, `accounting-double-entry`, `test-case-design-techniques`, `data-privacy-financial`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — Idempotencia del núcleo con el scope del índice | 8 | 0 | TODO |
| H2 — Retiro con evidencia step-up; sin bypass en producción | 12 | 0 | TODO |
| H3 — Doble aprobación en la aplicación | 12 | 0 | TODO |
| H4 — Proveedor con estados, clientes resilientes, propiedad, métricas | 10 | 0 | TODO |
| **TOTAL** | **42** | **0** | |

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

> Recordá la regla 65: la evidencia de Richard tiene su doble (H2.S2.M1), el proveedor de
> retiros tiene su doble (H4.S2.M2). Nada de este encargo espera a nadie. Solo una decisión de
> negocio queda abierta.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-4) | Endpoint y permiso de aprobación | — | DECIDIDA: `/billetera/retiros/{ordenId}/aprobacion`, `RETIRO_APROBAR` → rol `TESORERIA` |
| Q-02 (AMB-5) | Retiro < umbral | — | DECIDIDA: `AUTORIZADA` automática en la misma transacción |
| Q-03 (AMB-2) | Consumo del `jti` | — | DECIDIDA: tabla `evidencia_mfa_consumida` por generador |
| Q-04 | Proveedor real de retiros | Negocio | DECIDIDA para el turno: puerto + doble; producción sin adaptador no arranca |
| Q-05 | Rol para `RETIRO_APROBAR` | — | DECIDIDA: `TESORERIA` |
