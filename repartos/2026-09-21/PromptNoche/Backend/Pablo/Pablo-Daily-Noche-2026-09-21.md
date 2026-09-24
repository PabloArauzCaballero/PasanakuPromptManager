# Daily de Pablo — turno noche — 2026-09-21

> **AVANCE: 49 / 54 — 90,7 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> Actualizado 2026-09-24 (sesión de cierre). Veredicto: sigue `NOT READY` — F-07 (`identidad`) y
> F-09 (`aportes`) bajo su piso de cobertura; F-04 cierra cuando se fusione #26.
> **Estado:** `IN_PROGRESS`. PR #1 y #2 fusionados en `dev` y espejados en `test` (2026-09-22). PR de
> cierre [#27](https://github.com/PabloArauzCaballero/PasanakuBackend/pull/27) (borrador, apilado sobre
> #26). Estado vivo y evidencia completa en
> [carriles/PR5-ci-operacion.md](https://github.com/PabloArauzCaballero/PasanakuBackend/blob/pablo/feature/carril-PR5-cierre/docs/auditoria-produccion/carriles/PR5-ci-operacion.md) §"Cierre 2026-09-24"
> (rama `pablo/feature/carril-PR5-cierre`). Este archivo es el resumen.

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
| H1 — Baseline global con salida literal | 12 | 12 | **HECHO** (S2.M6 `e2eTest` y S3.M3 desconocidos, 2026-09-24) |
| H2 — CI verde sin trampas: Spotless, OSV, SBOM, Trivy, gobernanza, E2E financiero | 20 | 17 | EN CURSO (S6.M2 A MEDIAS; S5.M3 BLOQUEADO — DECISION_REQUIRED; S6.M5 BLOQUEADO estructural) |
| H3 — Borde: rate limiting, CORS, cabeceras, métricas internas | 7 | 7 | **HECHO** |
| H4 — Carga medida (k6) y límites de recursos | 3 | 3 | **HECHO** |
| H5 — Runbooks, backup restaurado, gate de promoción, `FINAL_REPORT` | 12 | 10 | EN CURSO (S3.M3 A MEDIAS; S3.M4 BLOQUEADO estructural) |
| **TOTAL** | **54** | **49** | |

Recuento corregido: el 44 anterior contaba 8/12 en H1, pero la tabla de HECHO de la bitácora ya tenía
10 filas de H1 con evidencia (46), y hoy se cerraron 3 más: H1.S2.M6, H1.S3.M3 y H2.S1.M2.

Detalle línea por línea, con comando y salida de cada microtarea, en
[carriles/PR5-ci-operacion.md](https://github.com/PabloArauzCaballero/PasanakuBackend/blob/pablo/feature/carril-PR5-cierre/docs/auditoria-produccion/carriles/PR5-ci-operacion.md)
— no se duplica acá.

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H2.S1.M2 | PR #1 fusionado (`31991f9`), presente en `dev` y `test`; paso `2 · formato` verde en `dev` | `gh pr view 1`; `git branch -r --contains 31991f9`; `gh run view 35923629830` | PASS — `evidencia/H2-S1-M2-merge-espejo.txt` |
| H1.S2.M6 | `e2eTest` (`OutboxE2ETest`, Kafka real) en verde. Fallaba también en Linux, no era la máquina: con `apache/kafka:3.9.0` no arranca → `3.8.1` | `./gradlew :plataforma:comun-mensajeria:e2eTest`; job `e2e-financiero` (run 36044781095) | PASS local 1/1 y en CI `BUILD SUCCESSFUL` — `evidencia/H1-S2-M6-e2eTest.txt` |
| H1.S3.M3 | Los 8 desconocidos §2.2 resueltos con comando o enlace al carril dueño | ver evidencia | PASS — `baseline.md`, `evidencia/H1-S3-M3-desconocidos.txt` |
| (CI) | Paso `16b · cobertura` en «Los cinco corredores»: antes ningún job verificaba los pisos | `./gradlew jacocoTestCoverageVerification --continue` | Corre, y el rojo es real: F-07 y F-09 — `evidencia/H2-S6-M2-cobertura-ci.txt` |
| F-06 / F-08 | `comun-web` supera su piso (0.744/0.541); `comun-pruebas` 0.61 → 0.70 con `EsperaTest` | jacoco por módulo | PASS — `evidencia/F-06-…`, `evidencia/F-08-…` |

## 4. A medias — las cuatro respuestas, obligatorias

### H2.S6.M2 — `verificarProduccion` exit 0
- **Qué anda:** cada parte de la tarea está en verde en CI sobre #27 salvo la cobertura.
- **Qué no anda:** cobertura de `identidad` (0.72/0.54 contra 0.79/0.63, F-07) y `aportes` (ramas 0.68 contra 0.69, F-09).
- **Qué falta exactamente:** agregar pruebas en esos dos servicios, fusionar #26 y correr `./gradlew verificarProduccion` en local con el esquema aplicado.
- **Dónde quedó:** `pablo/feature/carril-PR5-cierre` (PR #27). Compila y sus pruebas dirigidas pasan.

### H5.S3.M3 — checkout limpio con todo en exit 0
- **Qué anda:** worktree limpio, infraestructura desde cero, `e2eTest` PASS, `docker build` y Trivy (2026-09-22).
- **Qué no anda:** `verificarProduccion` sigue en rojo por lo mismo que H2.S6.M2.
- **Qué falta exactamente:** lo mismo que H2.S6.M2.
- **Dónde quedó:** worktree `PasanakuBackend-pablo-pr5-cierre`.

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H2.S5.M3 | Crear el ruleset mínimo `proteccion-minima` (el agente no tiene permiso para modificar recursos compartidos del repo) | JSON y comando listos | `gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input PR5-Ci.Operacion/entregables/ruleset-minimo.json` | Pablo — un comando |
| H2.S6.M5 / H5.S3.M4 | CI completo en verde | Dos `workflow_dispatch` reales (36042014583, 36044781095) | Fusionar #26 (barrido financiero, OSV), resolver F-07/F-09 y los jobs iOS del carril de frontend (con secretos de TestFlight) | Pablo, Richard, Marcelo y el carril de frontend |
| (local) | Aplicar `sql/aplicar.sql` en el Postgres local: el clasificador de permisos lo denegó en esta sesión | `./gradlew bd:aplicar -x bd:levantar` | Que Pablo lo corra en el worktree | Pablo — un comando |

> Recordá la regla 65: los tests que el CI debe correr y aún no existen no te bloquean (los
> corredores ya toleran cero tests); un check del gate sin evidencia se deja sin marcar, nunca
> se inventa.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| F-04 | CVE en dependencias Java | Pablo (#26) | Lo resuelve #26 (Boot 3.5.16, Cloud 2025.0.3, netty 4.1.138, bc 1.85.2) |
| F-06 | `comun-web` bajo su piso | — | CERRADO (lo resolvieron las pruebas de otros carriles) |
| F-07 | `identidad` 0.72/0.54 contra 0.79/0.63 | Richard | ABIERTO (medido en CI) |
| F-08 | `comun-pruebas` 0.61/0.62 contra 0.64 | Leo | CORREGIDO en #27 (`EsperaTest`) |
| F-09 | `aportes` ramas 0.68 contra 0.69 | Marcelo | ABIERTO (medido en CI) |
| F-Leo-06 | Kafka 3.9.0 no arranca en `KafkaContainer` 1.21.x | Leo | CORREGIDO en #27 (`apache/kafka:3.8.1`) |

## 7. No cubierto

- `verificarProduccion` y `e2eTest` desde la raíz en local: sin el esquema aplicado no compilan los servicios (acción denegada en esta sesión). Sus partes corrieron en CI.
- Los 14 servicios no tienen `*E2ETest`.
- Los jobs iOS (macOS) del CI.

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-R1) | `test` espejo de `dev` | — | DECIDIDA: fast-forward tras cada merge; ruleset mínimo listo para aplicar |
| Q-02 (AMB-6) | Redis | — | DECIDIDA: entra al stack; ADR-050 |
| Q-03 (AMB-8) | RPO/RTO | — | DECIDIDA: PITR; se miden en el restore y se reportan como capacidad |
| Q-04 (AMB-9) | Severidad OSV/Trivy | — | DECIDIDA: HIGH+CRITICAL bloquean |
| Q-05 | Rulesets | — | DECIDIDA: mínimo listo (un comando tuyo); completo en la promoción |
| Q-06 | Commits firmados | — | DECIDIDA: no se exigen |
