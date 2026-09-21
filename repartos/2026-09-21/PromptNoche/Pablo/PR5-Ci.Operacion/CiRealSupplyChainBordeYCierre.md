# CI y operación: el baseline que nadie discute, un CI verde sin trampas con escaneo real, SBOM e imagen, el borde con rate limiting y CORS explícitos, la carga medida, y el cierre que dice READY solo con evidencia

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Pablo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio(s):** `.github/workflows`, `despliegue/**`, `docker-compose.coolify.yml`, `plataforma/gateway`, `scripts/generar_{compose,gateway,k8s}.py`, `carga/`, `docs/operacion/**` (salvo los 3 runbooks de Richard y Justin), `docs/auditoria-produccion/{baseline,PLAN,promotion-gate,FINAL_REPORT,proveedores}.md`
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Pablo-Daily-Noche-2026-09-21.md](../Pablo-Daily-Noche-2026-09-21.md)
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (este encargo cubre H0.S2, H0.S3 global, H0.S4.M6, H0.S5, H6 completo, H7.S4, H7.S5.M1/M2, H9.S1.M1, H10.S3, H12 completo)
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `pablo/feature/carril-PR5-ci-operacion`
- **5 hitos · 17 subtareas · 54 microtareas** — sos además quien consolida: `baseline.md`, `promotion-gate.md` y `FINAL_REPORT.md` los escribís vos con las bitácoras `carriles/PR1…PR4` de los otros cuatro

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar (este repo) dentro de `PasanakuBackend/`. El backend trae sus propias skills (`ci-calidad`, `despliegue-contenedores`, `entorno-monorepo`…): **se suman, no se reemplazan**.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `github-actions-ci` | Jobs, `services`, artifacts, `workflow_dispatch`, sin `|| true` |
| `github-security-features` | Dependabot, secret scanning, code scanning con SARIF |
| `github-branch-protection-rulesets` | El ruleset exacto de `dev` y `main`, como JSON y como comando |
| `dependency-management` | OSV con política de severidad y excepciones con fecha |
| `dockerfile-production` | Digest fijado, read-only, sin herramientas de más, `HEALTHCHECK` |
| `api-gateway-bff` | Rate limiting y CORS en el borde, y nada más ahí |
| `performance-load-testing` | k6 reproducible y baseline sin objetivos inventados |
| `backup-restore-dr` | Backup y restore probados; RPO/RTO como decisión, no como número |
| `technical-docs-and-adr` | Runbooks con las 7 secciones; ADR-050 |
| `release-and-rollback` | La recomendación `dev → main` con orden de despliegue y rollback |
| `work-report-md` | `FINAL_REPORT.md` con las 16 secciones y `REPORTE.md` |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre del turno con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 65 · 70 · 90 · 98

## 2. Resultado observable

Un push a `dev` corre un CI donde todos los jobs terminan `success` sin `skipTests`, `ignoreFailures` ni `|| true`, con OSV que falla ante HIGH/CRITICAL, SBOM CycloneDX como artifact, Trivy sobre la imagen, CODEOWNERS y el E2E financiero; el gateway devuelve `429` con `Retry-After` en login/refresh/reset/MFA/retiro/transferencia/registro/OTP y rechaza orígenes no listados en `production`; existe un escenario k6 con baseline medida; `docs/operacion/` tiene los runbooks y el backup restaurado de verdad; `FINAL_REPORT.md` abre con `READY` / `READY WITH NON-BLOCKING RISKS` / `NOT READY` y cada check del `promotion-gate.md` enlaza su evidencia.

**Kill-test:** `gh run list --branch dev --limit 1` con un job `skipped` o `failure`, o un `[x]` en `promotion-gate.md` sin enlace a evidencia. Cualquiera de los dos y esto NO está hecho.

## 3. Alcance

**IN:** `.github/**` (workflows, `CODEOWNERS`, `dependabot.yml`, `osv-scanner.toml`, `.trivyignore`); `despliegue/**`, `docker-compose.coolify.yml`, `scripts/generar_{compose,gateway,k8s}.py`; `plataforma/gateway/**`; `carga/k6/**`; `docs/operacion/{branch-protection,backup-recovery,outbox-backlog,kafka-down,postgres-down,secret-rotation}.md`; `docs/auditoria-produccion/{baseline,PLAN,promotion-gate,FINAL_REPORT,proveedores}.md` y `docs/auditoria-produccion/carriles/PR5-ci-operacion.md`; `docs/Arquitectura/ADR-050 Rate limiting distribuido en el borde.md`; `README.md` (§levantar/tests); micro-PR al troncal para `gradle/libs.versions.toml` (cyclonedx, redis) coordinado con Leo y Marcelo; la tarea raíz `verificarProduccion` en `build.gradle.kts` (raíz, no `buildSrc`).

**OUT:** `servicios/**` y `plataforma/comun-*` (los otros cuatro). `buildSrc/**` (Leo): el plugin CycloneDX se agrega a `aportaya.servicio.gradle.kts` **por micro-PR tuyo que Leo revisa**, nunca en tu rama de carril. `main` no se toca: la promoción se recomienda, no se ejecuta. Aplicar los rulesets: solo con tu confirmación explícita registrada en el daily (es acción compartida; el agente la deja preparada, no la ejecuta sola).

**Reservas de archivos:** todo lo de IN. `gradle/libs.versions.toml` solo por micro-PR.

### Ritual de entrega — `dev` y `test`, sin esperar a nadie

```bash
git fetch origin && git checkout -b pablo/feature/carril-PR5-ci-operacion origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply spotlessCheck :plataforma:gateway:integrationTest
python3 scripts/generar_compose.py && python3 scripts/generar_gateway.py && python3 scripts/generar_k8s.py && git diff --exit-code despliegue/ plataforma/gateway/src/main/resources/rutas.yml
git push -u origin HEAD
gh pr create --base dev --fill --title "ci(security): <subtarea>"
gh pr merge --rebase
git fetch origin && git push origin origin/dev:test   # test es espejo de dev (AMB-R1)
```

- **H2.S1 (Spotless) va primero y se mergea en la primera media hora**: es lo que hoy tiene rojo el CI de `dev` y deja `skipped` todo lo demás; los otros cuatro rebasean después.
- **Micro-PR al troncal** (`libs.versions.toml`, `aportaya.servicio.gradle.kts`): un commit solo con eso, `troncal(<que>): …`, mergeado dentro de la hora.
- **Jamás te detenés.** Los tests que el CI debe correr y todavía no existen (los escriben los otros cuatro) no te frenan: los corredores ya tienen `failOnNoDiscoveredTests=false`; el job queda cableado y corre lo que haya. Un check del gate sin evidencia se deja **sin marcar**, nunca se inventa. Un dato que es decisión de negocio (RPO/RTO) se escribe como `DECISION_REQUIRED`.
- CI rojo por un job ajeno (un test de otro carril mergeado en rojo, cosa que el reparto prohíbe) → hallazgo en tu daily §6 al dueño; no te detiene.

### Lo que consolidás de los otros cuatro (no lo escribís vos: lo enlazás)

| Artefacto | Quién lo produce | Vos |
|---|---|---|
| `carriles/PR1-identidad.md` … `PR4-seguridad.md` | Richard, Justin, Leo, Marcelo | Los leés al cierre y llenás `FINAL_REPORT.md` §4–§14 con sus evidencias enlazadas |
| `baseline-PR1…PR4-*.md` (por módulo) | cada uno | `baseline.md` los enlaza y agrega los gates globales (H1.S2) |
| Pasos de CI listos (`inventario_endpoints.py --check`, `verificar_contratos_limites.py`) | Marcelo (sección "Para el CI" de su bitácora) | Los cableás en `ci.yml` job `boveda` (H2.S6.M3) si ya están en `dev`; si no, dejás el paso preparado con `continue-on-error: false` y lo declarás |
| `contratos/step-up-jwt.md`, `contratos/evento-kafka.md` | Richard, Leo | Los citás en `security-matrix` y `proveedores` |

## 4. Plan

### H1 — Baseline global: qué anda y qué no en `19a621e6`, con salida literal

**CA:** Dado `docs/auditoria-produccion/baseline.md`, cuando alguien lo lee, entonces encuentra versiones, cada comando global del gate con salida y veredicto, jOOQ y clientes generando, y la tabla A–J revalidada con ruta y línea, más los enlaces a los baselines por módulo de los otros cuatro.
**DoD:** `baseline.md` con las 7 corridas globales; `python3 scripts/auditar_backend.py --json` guardado; `python3 scripts/verificar_boveda.py` exit 0 (la bóveda enlaza el documento si su índice lo exige).
**Estado:** TODO

#### H1.S1 — Estado inicial registrado (plan H0.S2)

**CA:** Dado `baseline.md` §Estado, entonces contiene branch, SHA, fecha, Java, Gradle, Docker, PostgreSQL y las versiones del catálogo.
**DoD:** salidas de `git log -1`, `./gradlew --version`, `docker --version`, `docker exec aportaya-postgres postgres --version`, `grep -E '^(spring-boot|jooq|shedlock|resilience4j) ' gradle/libs.versions.toml` pegadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Copiar el plan madre a `docs/auditoria-produccion/PLAN.md` (con una nota de que el estado vivo está en los `carriles/PR*.md`) y crear `evidencia/`, `carriles/`, `contratos/` | Archivos existen | `test -f docs/auditoria-produccion/PLAN.md && ls docs/auditoria-produccion` | TODO |
| H1.S1.M2 | `baseline.md` §Estado con las 8 líneas + `auditar_backend.py --json` guardado | Archivo | `python3 scripts/auditar_backend.py --json > docs/auditoria-produccion/evidencia/H1-auditar-backend-inicial.json; echo exit=$?` | TODO |

#### H1.S2 — Gates globales uno por uno, en serie (plan H0.S3.M1–M5, M7, M8)

**CA:** Dado cada comando, cuando se ejecuta en serie (regla 70), entonces su cola y exit code quedan en `evidencia/` con veredicto PASS/FAIL/BLOCKED; cada rojo se clasifica (regla 80.4).
**DoD:** 7 archivos `H1-S2-M*.txt`; tabla de rojos clasificados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | `spotlessCheck` con la lista de archivos que fallan (hoy es el rojo del CI) | Lista | `./gradlew spotlessCheck; echo exit=$?` | TODO |
| H1.S2.M2 | `check -x test` (estático, ArchUnit, `sinJpa`) | Veredicto | `./gradlew check -x test -x jacocoTestCoverageVerification -x jacocoTestReport; echo exit=$?` | TODO |
| H1.S2.M3 | `testBarrido` | Veredicto | `./gradlew testBarrido; echo exit=$?` | TODO |
| H1.S2.M4 | `test` y `webTest` (raíz) | Veredicto + conteo | `./gradlew test; echo exit=$?; ./gradlew webTest; echo exit=$?` | TODO |
| H1.S2.M5 | `contractTest` y `sagaTest` | Veredicto | `./gradlew contractTest; echo exit=$?; ./gradlew sagaTest; echo exit=$?` | TODO |
| H1.S2.M6 | `e2eTest` sobre `compose --profile todo` (o `BLOCKED` con causa si no hay imágenes construidas: seguí el README para construirlas de a una) | Veredicto | `./gradlew e2eTest; echo exit=$?` | TODO |
| H1.S2.M7 | `generateJooq` y `generateOpenApiClients` | exit 0 | `./gradlew generateJooq; ./gradlew generateOpenApiClients --no-parallel --no-build-cache` | TODO |

#### H1.S3 — Consolidación (plan H0.S3.M9, H0.S5)

**CA:** Dado cada rojo global, entonces tiene clase, hipótesis y dueño (carril) o "fuera de alcance, anotado"; la tabla A–J del plan madre §2.4 está copiada con correcciones; los desconocidos §2.2 del plan madre tienen comando y salida (los de módulos ajenos, enlazados desde sus baselines).
**DoD:** secciones escritas; `python .claude/hooks/plan_status.py` en este repo muestra tu avance.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Tabla de rojos clasificados con dueño | Cada FAIL con clase + carril | revisión | TODO |
| H1.S3.M2 | Tabla A–J en `baseline.md` | 10 filas con ruta:línea | revisión | TODO |
| H1.S3.M3 | Desconocidos resueltos (o enlazados a `baseline-PR*.md`) | 8 ítems | revisión | TODO |

### H2 — CI verde sin trampas: Spotless, SCA real, SBOM, imagen, gobernanza, E2E financiero y agregador local

**CA:** Dado un push a `dev`, cuando corre el CI, entonces todos los jobs `success`; OSV falla ante HIGH/CRITICAL no exceptuados; hay `bom.json` por módulo como artifact; Trivy escanea la imagen; existen `CODEOWNERS` y `branch-protection.md`; el E2E financiero corre en `dev`; `./gradlew verificarProduccion` corre local sin secretos.
**DoD:** `gh run view <id> --json jobs --jq '.jobs[].conclusion'` → solo `success`; artifacts visibles; `./gradlew verificarProduccion` exit 0.
**Estado:** TODO

#### H2.S1 — Spotless en verde, primero de todo (plan H6.S1)

**CA:** Dado el repo, cuando corre `spotlessCheck`, entonces exit 0 y el diff es solo formato.
**DoD:** `./gradlew spotlessCheck` exit 0 local; job `codigo` verde; **mergeado en la primera media hora**.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | `./gradlew spotlessApply`; revisar `git diff` (solo whitespace/imports/orden; ningún cambio semántico) | Diff revisado | `git diff --stat` pegado; `./gradlew spotlessCheck` exit 0 | TODO |
| H2.S1.M2 | Commit `style: apply spotless across the repo`, PR, merge, espejo; avisar en el chat del turno: "rebaseen" | Job `codigo` success | `gh run list --branch dev --limit 1` | TODO |

#### H2.S2 — SCA real con OSV y Dependabot (plan H6.S2)

**CA:** Dado los lockfiles de Gradle de los módulos desplegables, cuando corre `osv-scanner`, entonces falla ante HIGH/CRITICAL no listados en `.github/osv-scanner.toml` (con motivo y fecha); Dependabot abre PRs semanales de gradle y actions.
**DoD:** job `seguridad` verde con SARIF subido; prueba negativa pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | **Verificar en la doc de OSV-Scanner qué formatos de Gradle soporta** (`gradle.lockfile`, `libs.versions.toml`); habilitar dependency locking en `aportaya.servicio.gradle.kts` (micro-PR con Leo) y commitear `gradle.lockfile` de los 14 + gateway | Lockfiles commiteados | `ls servicios/*/gradle.lockfile plataforma/gateway/gradle.lockfile \| wc -l` → 15 | TODO |
| H2.S2.M2 | Reemplazar el paso "19c" (`ci.yml:396-407`) por `google/osv-scanner-action` con `--config .github/osv-scanner.toml` (HIGH/CRITICAL bloquean, AMB-9) y `upload-sarif` | Job verde | `gh run view --job <id>` | TODO |
| H2.S2.M3 | Prueba negativa en rama temporal: dependencia con CVE alta conocida → rojo → revertir | Rojo demostrado | `evidencia/H2-S2-M3-osv-negativo.txt` | TODO |
| H2.S2.M4 | `.github/dependabot.yml` (gradle + github-actions, semanal, agrupado) | Válido | `gh api repos/PabloArauzCaballero/PasanakuBackend/dependabot/alerts?per_page=1` responde (o revisión de sintaxis) | TODO |

#### H2.S3 — SBOM CycloneDX (plan H6.S3)

**CA:** Dado un build de CI, entonces hay `bom.json` por módulo desplegable como artifact `sbom-<sha>`.
**DoD:** `./gradlew :servicios:identidad:cyclonedxBom` exit 0 local; artifact en la corrida.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S3.M1 | Plugin `org.cyclonedx.bom` (**verificar versión y API en su doc**) en el catálogo y en `aportaya.servicio.gradle.kts` → micro-PR `troncal(build): cyclonedx` (Leo revisa) | `bom.json` generado | `./gradlew :servicios:identidad:cyclonedxBom && ls servicios/identidad/build/reports/bom.json` | TODO |
| H2.S3.M2 | Paso CI + `upload-artifact` | Artifact visible | `gh run view <id>` lista `sbom-…` | TODO |

#### H2.S4 — Imagen: Trivy y endurecimiento (plan H6.S4)

**CA:** Dado `aportaya/identidad:ci`, cuando Trivy la escanea, entonces sin CRITICAL/HIGH no exceptuados; `User=app`; base por digest; `read_only: true` + `tmpfs` en compose; `HEALTHCHECK` funciona sin `wget` si hay alternativa.
**DoD:** paso Trivy verde; `docker inspect` y `docker compose … --wait` exit 0.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S4.M1 | `aquasecurity/trivy-action` sobre la imagen del job `imagenes` (`severity: CRITICAL,HIGH`, `exit-code: 1`, `ignore-unfixed: true`), `.trivyignore` con motivo/fecha | Job verde | `gh run view --job <id>` | TODO |
| H2.S4.M2 | Base por digest en las dos etapas del `despliegue/Dockerfile` | 2 líneas `@sha256` | `grep -c "@sha256" despliegue/Dockerfile` → 2 | TODO |
| H2.S4.M3 | `read_only: true` + `tmpfs: /tmp` en `generar_compose.py` y Coolify; el servicio arranca | Healthy | `docker compose -f despliegue/compose/base.yml -f despliegue/compose/servicios.yml --profile todo up -d --no-build --wait` exit 0 | TODO |
| H2.S4.M4 | Healthcheck sin `wget` (`java` con `HttpClient` o `curl` de la base) o dejarlo y documentar en ADR-025 | Decisión escrita | `docker image inspect … \| grep -c wget` → 0, o nota en ADR-025 | TODO |

#### H2.S5 — CODEOWNERS y protección de ramas (plan H6.S5)

**CA:** Dado `.github/CODEOWNERS` con los 7 paths, entonces sin errores; `docs/operacion/branch-protection.md` contiene el ruleset JSON de `dev` y `main` y el comando `gh api` exacto; aplicarlo queda listo y **solo se ejecuta con tu confirmación escrita en el daily**.
**DoD:** `gh api repos/PabloArauzCaballero/PasanakuBackend/codeowners/errors` → `{"errors":[]}`; documento completo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S5.M1 | `CODEOWNERS`: `/sql`, `/servicios/nucleo-financiero`, `/servicios/identidad`, `/servicios/cumplimiento`, `/plataforma/comun-web`, `/plataforma/comun-mensajeria`, `/.github/workflows` | Sin errores | comando | TODO |
| H2.S5.M2 | `branch-protection.md`: PR obligatorio, 1 aprobación (`dev`) / 2 (`main`), CODEOWNERS, checks requeridos = nombres exactos de los jobs de `ci.yml` y `boveda-y-esquema.yml`, up-to-date, sin force push, sin borrado, commits firmados (decisión); `ruleset-dev.json`, `ruleset-main.json` y `gh api --method POST repos/…/rulesets --input …` | Documento + 2 JSON | revisión | TODO |
| H2.S5.M3 | Aplicar el ruleset **completo** (PR obligatorio, checks requeridos, CODEOWNERS, 2 aprobaciones en `main`) en el momento de la promoción `dev → main`; el ruleset mínimo `proteccion-minima` (sin force-push ni borrado en `dev`/`test`/`main`) está **listo en `entregables/ruleset-minimo.json`** y lo aplicás vos con `gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input entregables/ruleset-minimo.json` (el agente no tiene permiso sobre recursos compartidos del repo) | `gh api …/rulesets` lista `proteccion-minima` | `gh api repos/PabloArauzCaballero/PasanakuBackend/rulesets --jq '.[].name'` → `proteccion-minima` | BLOQUEADO — DECISION_REQUIRED (Pablo: un comando) |

#### H2.S6 — E2E financiero en `dev`, agregador local y CI sin trampas (plan H6.S6)

**CA:** Dado un push a `dev` o `workflow_dispatch`, el job `e2e-financiero` corre con `services` postgres + kafka; `./gradlew verificarProduccion` corre formato, estático, tests, integración, contrato, saga, `verificar_seguridad.py`, `verificar_boveda.py`, `cyclonedxBom`, sin scanners que exijan token; ningún paso tapa fallos.
**DoD:** job verde en `dev`; `./gradlew verificarProduccion` exit 0; `grep` sin `|| true`/`ignoreFailures`/`skipTests` no justificados; corrida completa del CI con todos los jobs `success`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S6.M1 | Job `e2e-financiero` (`if: github.ref == 'refs/heads/dev' \|\| github.event_name == 'workflow_dispatch'`, `services` postgres:16 + `apache/kafka:<fijada>`) que corre `./gradlew :servicios:nucleo-financiero:e2eTest :plataforma:comun-mensajeria:e2eTest` (corre lo que exista: los tests los escriben Justin y Leo) | Job verde | `gh run view` | TODO |
| H2.S6.M2 | Tarea raíz `verificarProduccion` en `build.gradle.kts` (dependsOn `verificar`, `testBarrido`, `erroresCatalogo`, `cyclonedxBom`; `Exec` de los verificadores Python) | exit 0 | `./gradlew verificarProduccion` | TODO |
| H2.S6.M3 | Cablear en `boveda` los pasos de Marcelo (`inventario_endpoints.py --check`, `verificar_contratos_limites.py`) si ya están en `dev`; si no, dejarlos preparados y declararlo | Pasos presentes | `grep -n "inventario_endpoints\|verificar_contratos_limites" .github/workflows/*.yml` | TODO |
| H2.S6.M4 | Revisar y justificar cada `-x`, `continue-on-error`, `\|\| true` en workflows y buildSrc (el `-x test` del job `codigo` es legítimo: `pruebas` los corre; se documenta) | Grep con justificación | `grep -rn "|| true\|ignoreFailures\|skipTests\|continue-on-error" .github/workflows buildSrc` → vacío o justificado en el daily | TODO |
| H2.S6.M5 | Corrida completa del CI en `dev` con **todos** los jobs verdes (incluido `e2e-financiero`) | Solo `success` | `gh run view <id> --json jobs --jq '.jobs[].conclusion'` | TODO |

### H3 — El borde: rate limiting distribuido, CORS por entorno, cabeceras, métricas solo en la red interna

**CA:** Dado el gateway con Redis, cuando un cliente supera N req/min en las 8 rutas sensibles, entonces `429` + `Retry-After`; con Redis caído deniega en esas rutas (fail closed) y lo mide; en `production` un origen no listado se rechaza y `*` es imposible; NGINX manda HSTS solo si termina TLS, `Cache-Control: no-store` en `/api/`; `/actuator/prometheus` responde en la red interna y da `404` por el gateway.
**DoD:** `./gradlew :plataforma:gateway:integrationTest` PASS (`RateLimitGatewayTest`, `CorsGatewayTest`); `curl -sI` con cabeceras pegado; ADR-050; compose y Coolify con Redis.
**Estado:** TODO

#### H3.S1 — Rate limiting con Redis (plan H7.S4)

**CA:** Dado `RequestRateLimiter` con `KeyResolver` IP+usuario en las rutas marcadas sensibles en `PREFIJOS`/`generar_gateway.py`, entonces `429` al superar el límite configurado; Redis caído → `503`/deny en esas rutas + métrica.
**DoD:** `./gradlew :plataforma:gateway:integrationTest --tests '*RateLimitGatewayTest*'` PASS (Testcontainers Redis).
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | `ADR-050 Rate limiting distribuido en el borde.md` (Redis vs NGINX `limit_req`; decisión AMB-6) + enlace en `_Arquitectura.md` | Bóveda verde | `python3 scripts/verificar_boveda.py` | TODO |
| H3.S1.M2 | Redis (imagen fijada) en `despliegue/compose/base.yml`, `infra.yml` y `docker-compose.coolify.yml`; `spring-boot-starter-data-redis-reactive` al catálogo → micro-PR `troncal(deps): redis reactivo` | Contenedor healthy | `docker compose -f despliegue/compose/base.yml --profile base up -d --wait` | TODO |
| H3.S1.M3 | Marca `sensible` en `PREFIJOS`/`scripts/modelo.py` para login, refresh, reset, MFA/desafíos, retiro, transferencia, registro, OTP; `generar_gateway.py` emite el filtro `RequestRateLimiter` con `redis-rate-limiter.{replenishRate,burstCapacity}` por configuración | `rutas.yml` regenerado sin diff residual | `python3 scripts/generar_gateway.py && git diff --exit-code plataforma/gateway/src/main/resources/rutas.yml` | TODO |
| H3.S1.M4 | `RateLimitGatewayTest`: `429` + `Retry-After` al superar; Redis caído → deniega en sensibles + métrica `gateway_ratelimit_denegados_total` | PASS | comando | TODO |

#### H3.S2 — CORS por entorno y cabeceras (plan H7.S5.M1/M2)

**CA:** Dado `aportaya.cors.origenes` por perfil (métodos y cabeceras mínimos, `allowCredentials` solo si se usa), cuando un origen no listado hace preflight en `production`, entonces se rechaza; `GuardiaDeProduccion` (Leo) rechaza `*` — vos configurás, él exige; NGINX: HSTS si termina TLS, `Cache-Control: no-store` en `/api/`.
**DoD:** `./gradlew :plataforma:gateway:integrationTest --tests '*CorsGatewayTest*'` PASS; `curl -sI http://localhost/api/v1/...` pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | CORS en `gateway/application-{local,test,staging,production}.yml` (los perfiles de la plantilla de Leo si ya están; si no, a mano y anotado) | Test PASS | comando | TODO |
| H3.S2.M2 | NGINX `despliegue/nginx/aportaya.conf`: verificar dónde termina TLS (Coolify vs NGINX); HSTS solo ahí; `Cache-Control: no-store` para `/api/`; `Permissions-Policy` si aplica | Cabeceras presentes | `curl -sI` pegado | TODO |

#### H3.S3 — Métricas en la red interna (plan H9.S1.M1)

**CA:** Dado los 14 servicios, `management.endpoints.web.exposure.include` incluye `prometheus`, y el gateway/NGINX **no** enrutan `/actuator`.
**DoD:** `curl` interno con 200 y `curl` por el gateway con 404, pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | Verificar exposición en la plantilla (hallazgo a Leo si falta) y que `generar_gateway.py` no emita ruta a `/actuator`; `generar_k8s.py` con scrape interno | 200 interno / 404 externo | `docker exec aportaya-identidad wget -qO- localhost:8080/actuator/prometheus \| head -3`; `curl -s -o /dev/null -w "%{http_code}" http://localhost/api/v1/actuator/prometheus` → 404 | TODO |

### H4 — La carga medida, no imaginada

**CA:** Dado `carga/k6/` con login, saldo, transferencia, replay idempotente, retiro (proveedor doble) y `outbox_pending`, cuando corre 3 veces contra compose, entonces hay throughput, p50/p95/p99, errores, `pg_locks`, CPU, heap y lag de Kafka en `evidencia/`, sin objetivos inventados; los límites de recursos (§73) están tabulados con su fuente.
**DoD:** `k6 run carga/k6/transferencia.js` exit 0; `evidencia/H4-carga-baseline.txt`; tabla de límites en `proveedores.md` o `financial-invariants.md` (Marcelo) — vos la escribís en `docs/auditoria-produccion/limites-de-recursos.md`.
**Estado:** TODO

#### H4.S1 — k6 y límites (plan H10.S3)

**CA:** Dado las cuentas de prueba sembradas con `scripts/clave_dev.py` (sintéticas), cuando corren los escenarios, entonces terminan sin errores de contrato y registran las métricas.
**DoD:** salidas de k6 ×3 pegadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | `carga/k6/{login,saldo,transferencia,replay-idempotente,retiro,outbox}.js` + `README` con el comando | Corren contra compose | `k6 run carga/k6/transferencia.js` exit 0 | TODO |
| H4.S1.M2 | Baseline ×3 con throughput, p50/p95/p99, errores, `SELECT count(*) FROM pg_locks`, CPU (`docker stats`), heap (`/actuator/metrics/jvm.memory.used`), lag (`kafka-consumer-groups`) | Tabla | `evidencia/H4-carga-baseline.txt` | TODO |
| H4.S1.M3 | `limites-de-recursos.md`: `hikari.maximum-pool-size` × 14 vs `max_connections`/PgBouncer, tamaño de request/multipart, buffers Kafka, pool del `RestClient`, hilos — valor y archivo fuente | Tabla | revisión | TODO |

### H5 — Operación documentada y cierre demostrable: runbooks, backup restaurado, gate de promoción, `FINAL_REPORT`

**CA:** Dado un ingeniero nuevo, cuando lee `README` + `docs/operacion/` + `docs/auditoria-produccion/`, entonces levanta el entorno, corre los tests, entiende eventos, servicios y permisos, despliega staging y responde a un incidente con los runbooks; `promotion-gate.md` solo marca checks con enlace a evidencia; `FINAL_REPORT.md` abre con el estado y trae las 16 secciones; el diff completo fue revisado por un revisor independiente y validado en un checkout limpio.
**DoD:** 4 runbooks tuyos + `backup-recovery.md` con restore ejecutado; `promotion-gate.md`; `FINAL_REPORT.md`; `evidencia/H5-revision-diff.md`; `evidencia/H5-checkout-limpio.txt`; `REPORTE.md` en este repo con `report_gate.py` conforme.
**Estado:** TODO

#### H5.S1 — Runbooks y backup (plan H12.S1)

**CA:** Dado cada runbook, entonces tiene síntomas, dashboards/consultas, diagnóstico, acciones seguras, recuperación, validación, escalamiento; `backup-recovery.md` tiene un restore **ejecutado** con salida y RPO/RTO como `DECISION_REQUIRED`.
**DoD:** `grep -c "^## " docs/operacion/*.md` ≥ 7 en cada uno; `evidencia/H5-restore.txt`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | `outbox-backlog.md`, `kafka-down.md`, `postgres-down.md`, `secret-rotation.md` (los otros 3 son de Richard y Justin) | 4 × 7 secciones | `for f in outbox-backlog kafka-down postgres-down secret-rotation; do grep -c "^## " docs/operacion/$f.md; done` | TODO |
| H5.S1.M2 | `backup-recovery.md`: `pg_dump`/base + WAL/PITR según Coolify (`coolify-databases-backups` del catálogo si lo necesitás), RPO/RTO = `DECISION_REQUIRED`, Kafka (retención, no es fuente de verdad), secretos, runbook; **restore probado local** | Restore exit 0 + conteo de tablas | `evidencia/H5-restore.txt` | TODO |
| H5.S1.M3 | `README.md` (levantar, perfiles, tests, `verificarProduccion`), `docs/Arquitectura/Entornos y despliegue.md` (con Leo: él la tabla de perfiles, vos el despliegue), `docs/Pruebas.md` | Bóveda verde | `python3 scripts/verificar_boveda.py` | TODO |

#### H5.S2 — Matrices, ADR y gate de promoción (plan H12.S2)

**CA:** Dado los 11 documentos (ADR-046…050, `endpoints`, `security-matrix`, `financial-invariants`, `proveedores`, `dependencias`, `mutation-testing`), entonces existen y enlazan; `promotion-gate.md` tiene los 17 checks del metaprompt §85 + los de este reparto, cada `[x]` con enlace.
**DoD:** `ls` pegado; revisión línea por línea del gate.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S2.M1 | Verificar existencia y enlaces de los 11 (los ajenos que falten quedan como `[ ]` en el gate con el carril responsable) | Lista | `ls docs/Arquitectura/ADR-04[6-9]* docs/Arquitectura/ADR-050* docs/auditoria-produccion/*.md` | TODO |
| H5.S2.M2 | `promotion-gate.md` | Ningún `[x]` sin enlace | `grep -n "\[x\]" docs/auditoria-produccion/promotion-gate.md \| grep -v "evidencia/\|carriles/"` → vacío | TODO |

#### H5.S3 — Inspección final y checkout limpio (plan H12.S3)

**CA:** Dado `git diff origin/dev@{inicio}...HEAD` (usá el SHA inicial), cuando lo revisa un agente de solo lectura distinto del autor (regla 70.4.8) con contrato explícito (debug, secretos, `TODO`, mocks en prod, bypasses, imports muertos, logs sensibles, SQL peligroso, tests desactivados), entonces 0 hallazgos bloqueantes o microtareas nuevas; un worktree limpio pasa setup → `verificarProduccion` → base desde cero → `e2eTest` → imagen → Trivy.
**DoD:** `evidencia/H5-revision-diff.md`; `evidencia/H5-checkout-limpio.txt`; `gitleaks` y `verificar_seguridad.py` exit 0 en el SHA final; CI final verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S3.M1 | Revisión independiente del diff (subagente de solo lectura, **uno solo**, con contrato y sin editar) | Informe | `evidencia/H5-revision-diff.md` | TODO |
| H5.S3.M2 | `gitleaks detect --source . --no-git` + `verificar_seguridad.py` en el SHA final | exit 0 ×2 | salidas pegadas | TODO |
| H5.S3.M3 | `git worktree add ../pr-limpio <sha-final>` → setup → `./gradlew verificarProduccion` → base desde cero → `e2eTest` → `docker build` → Trivy local | Todo exit 0 | `evidencia/H5-checkout-limpio.txt` | TODO |
| H5.S3.M4 | CI verde en el SHA final, todos los jobs | Solo `success` | `gh run view <id> --json jobs --jq '.jobs[].conclusion'` | TODO |

#### H5.S4 — `FINAL_REPORT.md`, `REPORTE.md` y recomendación `dev → main` (plan H12.S4)

**CA:** Dado `FINAL_REPORT.md`, entonces abre con `READY` / `READY WITH NON-BLOCKING RISKS` / `NOT READY` (`READY` solo con todos los P0 `HECHO` con evidencia en las cuatro bitácoras), SHA inicial y final, 16 secciones del metaprompt §86, cambios manuales externos pendientes (rulesets, secretos, Redis en Coolify, decisiones abiertas) y la recomendación de promoción sin ejecutarla.
**DoD:** 16 secciones; `REPORTE.md` en este repo con avance en la primera línea; `python .claude/hooks/report_gate.py` conforme.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S4.M1 | `FINAL_REPORT.md` consolidando `carriles/PR1…PR5` | 16 secciones; estado sustentado | `grep -c "^## " docs/auditoria-produccion/FINAL_REPORT.md` ≥ 16 | TODO |
| H5.S4.M2 | `REPORTE.md` en `docs/trabajo/2026-09-21-backend-production-ready/` (este repo): avance calculado, Completado/A medias/Pendiente, evidencia, no cubierto, desvíos, riesgos, decisiones | `report_gate` no bloquea | `python .claude/hooks/plan_status.py` | TODO |
| H5.S4.M3 | Recomendación `dev → main`: PR de promoción con checklist del gate, orden de despliegue (identidad con claves, Redis, perfiles), rollback; **sin ejecutar el merge** | Sección en `FINAL_REPORT.md` | revisión | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 (= AMB-R1) | "Pushear a dev y test" | Vos | Nada | **DECIDIDA (2026-09-21)**: `test` es espejo fast-forward de `dev` (`git push origin origin/dev:test` tras cada merge); el ruleset mínimo `proteccion-minima` (JSON y comando en el daily del equipo §2, lo aplica Pablo con una línea) bloquea force-push y borrado en `dev`, `test` y `main` |
| Q-02 (= AMB-6) | Redis para rate limiting distribuido | Vos (infra) | Nada | **DECIDIDA (2026-09-21)**: **Redis entra al stack** (`despliegue/compose/base.yml`, `infra.yml`, Coolify) para `RequestRateLimiter` del gateway; con Redis caído las rutas sensibles deniegan (fail closed); ADR-050 lo registra |
| Q-03 (= AMB-8) | RPO/RTO | Operación | Nada | **DECIDIDA (2026-09-21)**: se implementa PITR (base + WAL) y el restore se ejecuta de verdad; el **RPO y el RTO se miden** en ese restore y se reportan como capacidad medida (no como compromiso comercial, que sigue siendo de negocio) |
| Q-04 (= AMB-9) | Severidad que bloquea en OSV/Trivy | Vos | Nada | **DECIDIDA (2026-09-21)**: `HIGH` y `CRITICAL` bloquean en OSV y Trivy; `MEDIUM` reporta; toda excepción lleva motivo y fecha de revisión (≤ 30 días) |
| Q-05 | Aplicar rulesets (H2.S5.M3) | Vos | Nada | **DECIDIDA (2026-09-21)**: durante el turno `dev` **no exige PR ni aprobaciones** (los cinco mergean solos con su gate local); queda **listo** el ruleset mínimo `proteccion-minima` (bloquea force-push y borrado en `dev`, `test` y `main`; el agente no tiene permiso para crearlo, Pablo lo aplica con el comando del daily §2); el ruleset **completo** (PR obligatorio, checks requeridos, CODEOWNERS, 2 aprobaciones en `main`) se activa en la promoción `dev → main` (Pablo H2.S5.M2 lo deja escrito) |
| Q-06 | Commits firmados como requisito del ruleset | Vos | Nada | **DECIDIDA (2026-09-21)**: commits firmados **no** se exigen en el ruleset (documentado como opcional) |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` solo
      por `DECISION_REQUIRED` (H2.S5.M3 es la única prevista).
- [ ] `carriles/PR5-ci-operacion.md` y tu daily con el avance calculado en la primera línea;
      `FINAL_REPORT.md` con el estado sustentado y `REPORTE.md` en este repo.
- [ ] Evidencia literal en `evidencia/`: corridas de CI, pruebas negativas de OSV/Trivy, k6 ×3,
      restore, revisión del diff, checkout limpio; sin secretos ni datos reales.
- [ ] Gates: `evidence-and-verification` siempre; `github-security-features` y
      `dependency-management` en H2; `api-gateway-bff` y `security-guardrails` en H3;
      `release-and-rollback` en H5.S4.
- [ ] Spotless mergeado en la primera media hora; todo lo demás mergeado en `dev` y espejado en
      `test` con el ritual.
- [ ] Peldaño de evidencia declarado por hito (regla 30). `READY` solo en el peldaño 6.
