# Daily de Marcelo — turno noche — 2026-09-21

> **AVANCE: 0 / 40 — 0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`.

- **Persona:** Marcelo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** `aportes`, seguridad transversal, base, scripts de verificación
- **Tu encargo:** [Seguridad transversal: inventario, idempotencia de aportes, ledger, base y código muerto](PR4-Seguridad.Transversal/InventarioIdorLedgerBaseYCodigoMuerto.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Rama:** `marcelo/feature/carril-PR4-seguridad` → PRs a `dev`, espejo a `test`

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `api-pentest`, `secure-code-review`, `integrity-testing`, `accounting-double-entry`, `performance-load-testing`, `postgresql-advanced`, `payments-qr-integration`, `dead-code-duplication`, `dependency-management`, `python-tooling-standards`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — `aportes`: idempotencia de su índice y webhook en tres niveles | 7 | 0 | TODO |
| H2 — Inventario de endpoints y endurecimiento de entrada | 7 | 0 | TODO |
| H3 — Invariantes del libro y benchmark del advisory lock | 8 | 0 | TODO |
| H4 — Base: RLS, grants, append-only, esquema desde cero y re-aplicado | 7 | 0 | TODO |
| H5 — Auditoría de operaciones críticas y matriz de seguridad | 3 | 0 | TODO |
| H6 — PIT, código muerto, dependencias | 8 | 0 | TODO |
| **TOTAL** | **40** | **0** | |

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

> Recordá la regla 65: un test transversal en rojo por un bug ajeno **no te bloquea**: queda en
> tu rama `A MEDIAS`, el hallazgo va al dueño (§6) y seguís. La pasarela del webhook tiene su
> doble (H1.S2.M2). Solo una decisión de negocio queda abierta.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-7) | Migraciones versionadas | — | DECIDIDA: `aplicar.sql` aditivo este turno; Flyway en ADR posterior |
| Q-02 | Pasarela del webhook | — | DECIDIDA: doble HMAC-SHA256 + timestamp ±5 min, tres niveles |
| Q-03 | Advisory lock | — | DECIDIDA: mantener; alternativa solo con medición y ADR |
| Q-04 | Código muerto con reflexión | — | DECIDIDA: nada se borra sin `ArranqueTest` ×14 verde después |
| Q-05 | Tests transversales en módulos ajenos | — | DECIDIDA en el reparto: archivos reservados |
