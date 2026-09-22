# Daily de Pablo — turno noche — 2026-09-21

> **AVANCE: 0 / 54 — 0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`.

- **Persona:** Pablo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** CI, supply chain, `gateway`, `despliegue/`, operación, cierre
- **Tu encargo:** [CI y operación: baseline, CI verde sin trampas, borde, carga y cierre](PR5-Ci.Operacion/CiRealSupplyChainBordeYCierre.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Rama:** `pablo/feature/carril-PR5-ci-operacion` → PRs a `dev`, espejo a `test`. **Spotless (H2.S1) se mergea en la primera media hora.**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `github-actions-ci`, `github-security-features`, `github-branch-protection-rulesets`, `dependency-management`, `dockerfile-production`, `api-gateway-bff`, `performance-load-testing`, `backup-restore-dr`, `technical-docs-and-adr`, `release-and-rollback`, `work-report-md`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — Baseline global con salida literal | 12 | 0 | TODO |
| H2 — CI verde sin trampas: Spotless, OSV, SBOM, Trivy, gobernanza, E2E financiero | 20 | 0 | TODO |
| H3 — Borde: rate limiting, CORS, cabeceras, métricas internas | 7 | 0 | TODO |
| H4 — Carga medida (k6) y límites de recursos | 3 | 0 | TODO |
| H5 — Runbooks, backup restaurado, gate de promoción, `FINAL_REPORT` | 12 | 0 | TODO |
| **TOTAL** | **54** | **0** | |

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
| H2.S5.M3 | Crear el ruleset mínimo `proteccion-minima` (el agente no tiene permiso para modificar recursos compartidos del repo) | JSON y comando listos | `gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input PR5-Ci.Operacion/entregables/ruleset-minimo.json` | Pablo — un comando |

> Recordá la regla 65: los tests que el CI debe correr y aún no existen no te bloquean (los
> corredores ya toleran cero tests); un check del gate sin evidencia se deja sin marcar, nunca
> se inventa.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-R1) | `test` espejo de `dev` | — | DECIDIDA: fast-forward tras cada merge; ruleset mínimo listo para aplicar |
| Q-02 (AMB-6) | Redis | — | DECIDIDA: entra al stack; ADR-050 |
| Q-03 (AMB-8) | RPO/RTO | — | DECIDIDA: PITR; se miden en el restore y se reportan como capacidad |
| Q-04 (AMB-9) | Severidad OSV/Trivy | — | DECIDIDA: HIGH+CRITICAL bloquean |
| Q-05 | Rulesets | — | DECIDIDA: mínimo listo (un comando tuyo); completo en la promoción |
| Q-06 | Commits firmados | — | DECIDIDA: no se exigen |
