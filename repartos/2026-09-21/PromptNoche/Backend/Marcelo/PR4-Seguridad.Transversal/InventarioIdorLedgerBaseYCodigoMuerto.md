# Seguridad transversal: el inventario de endpoints que el CI vigila, la idempotencia de `aportes`, las invariantes del libro medidas, la base que cada servicio solo ve por su esquema, y el código muerto que se va

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Marcelo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio(s):** `aportes`, `scripts/verificar_*.py` y nuevos, `sql/50_verificacion`, tests transversales en los servicios (archivos nombrados), `docs/auditoria-produccion/{endpoints,security-matrix,financial-invariants,dependencias,mutation-testing}.md`
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Marcelo-Daily-Noche-2026-09-21.md](../Marcelo-Daily-Noche-2026-09-21.md)
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (este encargo cubre H1.S4.M1–M3, H7.S1, H7.S3, H7.S6, H8.S1.M1, H8.S2, H8.S3, H9.S4.M4, H10.S1, H10.S2, H10.S4, H11.S2, H11.S3)
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `marcelo/feature/carril-PR4-seguridad`
- **6 hitos · 11 subtareas · 40 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar (este repo) dentro de `PasanakuBackend/`. El backend trae sus propias skills (`datos-jooq`, `restriccion`, `extraccion-de-datos`…): **se suman, no se reemplazan**.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `api-pentest` | OWASP API Top 10:2023: inventario, BOLA/BFLA, mass assignment, consumo no restringido |
| `secure-code-review` | SQL con jOOQ, SSRF, uploads, logs: qué buscar y cómo demostrarlo |
| `integrity-testing` | RLS, grants, append-only, constraints contra PostgreSQL real |
| `accounting-double-entry` | `SUM(debe)=SUM(haber)`, libro inmutable, cadena de hash |
| `performance-load-testing` | Benchmark del advisory lock: qué medir y cómo reportar sin inventar objetivos |
| `postgresql-advanced` | `pg_stat_activity`, `pg_locks`, advisory locks, índices parciales |
| `payments-qr-integration` | Firma, ventana temporal y replay del webhook de la pasarela en `aportes` |
| `dead-code-duplication` | Qué borrar, qué no, y cómo verificar el wiring antes de borrar |
| `dependency-management` | Higiene sin upgrades masivos |
| `python-tooling-standards` | Los scripts nuevos con la misma forma que `verificar_seguridad.py` |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre del turno con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 65 · **90** · **91** · 97

## 2. Resultado observable

El CI falla si un endpoint implementado no está en su OpenAPI (o viceversa), si un contrato de escritura acepta campos no declarados o sin límites, o si aparece SQL con entrada interpolada; `aportes` distingue claves de idempotencia por obligación y valida firma, ventana y replay del webhook; las once invariantes del libro están demostradas con PostgreSQL real y el advisory lock de la cadena de hash tiene p50/p95/p99 medidos; cada `svc_*` solo ve su esquema, no puede saltar `FORCE ROW LEVEL SECURITY` ni editar el libro; PIT reporta qué mutantes sobreviven en dinero/idempotencia/MFA; los adapters muertos y los `TODO` de P0 ya no están.

**Kill-test:** `python3 scripts/inventario_endpoints.py --check` no existe o sale 0 con un endpoint agregado a mano sin contrato. Si pasa, la vigilancia NO está hecha.

## 3. Alcance

**IN:** `servicios/aportes/**`; `scripts/verificar_seguridad.py`, `scripts/inventario_endpoints.py` (nuevo), `scripts/verificar_contratos_limites.py` (nuevo); `sql/50_verificacion/**`; tests transversales **con nombre reservado** en cualquier servicio: `LibroInvariantesTest`, `LibroBenchmarkTest`, `AppendOnlyTest`, `AislamientoEsquemaTest` (ampliación, en `comun-pruebas` se coordina con Leo: vos escribís el parametrizado por servicio en cada `servicios/<x>/src/test`), `AuditoriaCriticaTest`; `docs/auditoria-produccion/{endpoints,security-matrix,financial-invariants,dependencias,mutation-testing}.md`; `docs/operacion/schema-changes.md`; `docs/auditoria-produccion/carriles/PR4-seguridad.md`; plugin PIT (micro-PR al troncal: `libs.versions.toml` + `buildSrc`, coordinado con Leo y Pablo).

**OUT:** el código de producción de `identidad`, `nucleo-financiero` y `plataforma/*` (si tu test lo deja en rojo, el fix es del dueño: hallazgo en tu daily §6 y en el suyo; tu test **no se mergea en rojo**: queda en tu rama `A MEDIAS` y seguís con la siguiente). `.github/workflows` (Pablo: vos le dejás el paso listo como comando en `carriles/PR4-seguridad.md` §"Para el CI"). `gateway`, `despliegue/`.

**Reservas de archivos:** `servicios/aportes/**`; los scripts nombrados; `sql/50_verificacion/**`; los cinco nombres de test reservados en cualquier módulo; los cinco documentos de `docs/auditoria-produccion/` nombrados; `schema-changes.md`; `carriles/PR4-seguridad.md`.

### Ritual de entrega — `dev` y `test`, sin esperar a nadie

```bash
git fetch origin && git checkout -b marcelo/feature/carril-PR4-seguridad origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply :servicios:aportes:webTest :servicios:aportes:integrationTest spotlessCheck
python3 scripts/verificar_seguridad.py && python3 scripts/verificar_boveda.py
git push -u origin HEAD
gh pr create --base dev --fill --title "test(security): <subtarea>"
gh pr merge --rebase
git fetch origin && git push origin origin/dev:test   # test es espejo de dev (AMB-R1)
```

- **Micro-PR al troncal** (`libs.versions.toml`, `buildSrc/`, `sql/` vía generador): un commit solo con eso, `troncal(<que>): …`, mergeado dentro de la hora.
- **Jamás te detenés.** Test transversal en rojo por un bug ajeno → hallazgo con ruta:línea y clase (`PRODUCT_BUG`), el test queda en tu rama, seguís. Contrato ajeno que falta (p. ej. la pasarela real del webhook) → doble en **tres niveles**, declarado.
- CI rojo por job ajeno → hallazgo, no te detiene. Tu gate local en verde es la condición de merge.

## 4. Plan

### H1 — `aportes` con la idempotencia de su índice y un webhook que no se puede repetir ni falsificar

**CA:** Dado dos obligaciones con la misma clave de pago, entonces dos pagos; dado un webhook con firma inválida, fuera de ventana o repetido (`uq_webhook_idem (proveedor_id, clave)`), entonces rechazo sin efecto; dado uno válido, un solo pago aunque llegue dos veces.
**DoD:** `./gradlew :servicios:aportes:integrationTest --tests '*CU21*' --tests '*Webhook*'` PASS; `docs/auditoria-produccion/idempotencia-scope.md` completo.
**Estado:** TODO

#### H1.S1 — Baseline y barrido de lecturas de idempotencia (plan H0.S3.M6 parcial, H1.S4.M1–M3)

**CA:** Dado cada índice único con `clave_idempotencia` (12 en `restricciones.sql:236-263` + `uq_respuesta_idempotente`), cuando se busca su lectura Java, entonces filtra por las mismas columnas o solo escribe con `ON CONFLICT`.
**DoD:** tabla índice → clase:línea → veredicto sin filas `FUERA DE SCOPE` (las de `nucleo-financiero` las cierra Justin: vos las listás y las marcás "dueño: PR2").
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | **Primero del turno:** baseline de `aportes` (`webTest` + `integrationTest`) con rojos clasificados en `docs/auditoria-produccion/baseline-PR4-aportes.md` | Archivo con veredicto | `./gradlew :servicios:aportes:webTest :servicios:aportes:integrationTest; echo exit=$?` pegado | TODO |
| H1.S1.M2 | Grep repo-wide (`clave_idempotencia`, `Idempotency-Key`, `porClaveIdempotencia`, `idempoten`) → `docs/auditoria-produccion/idempotencia-scope.md` (índice · lectura · veredicto · dueño) | ≥ 13 filas | `grep -rn "porClaveIdempotencia" --include=*.java servicios plataforma` pegado | TODO |
| H1.S1.M3 | `aportes/PagoRepositorio.porClaveIdempotencia(dsl, obligacionId, clave)` (`:53`; índice `uq_pago_idem`); test rojo → verde en `CU21` (misma clave, otra obligación → dos pagos) | PASS | `./gradlew :servicios:aportes:integrationTest --tests '*CU21*'` | TODO |
| H1.S1.M4 | Cualquier otra lectura fuera de scope en servicios que no sean `nucleo-financiero` → corregir acá con su test (una microtarea nueva por caso, agregada al encargo) | 0 filas fuera de scope fuera de PR2 | tabla | TODO |

#### H1.S2 — Webhook de la pasarela en tres niveles (plan H9.S4.M4)

**CA:** Dado `webhook_pasarela`, cuando llega un evento, entonces se valida firma, ventana temporal, duplicado por `(proveedor_id, clave)`, monto contra la orden y versión de esquema; se audita; el doble de la pasarela cubre correcto / límite (timestamp al borde de la ventana; mismo evento dos veces) / inválido (firma mala, monto distinto, orden inexistente).
**DoD:** `./gradlew :servicios:aportes:integrationTest --tests '*Webhook*'` PASS (≥ 7 tests).
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Localizar el CU del webhook (`grep -rn webhook servicios/aportes/src/main`) y su validación actual; tabla de cobertura en `carriles/PR4-seguridad.md` | Tabla | revisión | TODO |
| H1.S2.M2 | Doble de la pasarela `@Profile({"local","test"})` con los tres niveles | Doble testeado | `./gradlew :servicios:aportes:integrationTest --tests '*PasarelaDoble*'` | TODO |
| H1.S2.M3 | Tests rojos → verdes por cada control faltante; auditoría append-only del webhook sin payload sensible | PASS | comando; grep del log sin payload | TODO |

### H2 — Inventario de endpoints y endurecimiento de entrada que el CI vigila

**CA:** Dado los 15 contratos OpenAPI y las anotaciones `@Permiso`/`@Publico`, cuando corre `inventario_endpoints.py --check`, entonces genera `endpoints.md` (Service, Method, Path, Permission, Ownership, Idempotency, Rate limit, MFA, Audit, Tests, sensible) y falla ante endpoint sin contrato o contrato sin endpoint; todo schema de request tiene `additionalProperties: false` y límites; no hay SQL con entrada interpolada; clientes HTTP con URL de configuración; uploads con tamaño, MIME real y nombre aleatorio.
**DoD:** `python3 scripts/inventario_endpoints.py --check` exit 0; `python3 scripts/verificar_contratos_limites.py` exit 0; `python3 scripts/verificar_seguridad.py` exit 0 con reglas nuevas; `./gradlew :plataforma:comun-archivos:integrationTest` PASS (tests nuevos, archivo `ArchivosSeguridadTest` **coordinado con Leo**: es su módulo, vos escribís solo ese test).
**Estado:** TODO

#### H2.S1 — Inventario generado (plan H7.S1)

**CA:** Dado un endpoint agregado a mano sin contrato, cuando corre el script, entonces sale 1 y lo nombra.
**DoD:** `endpoints.md` generado + prueba negativa pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | `scripts/inventario_endpoints.py` (misma forma que `verificar_pruebas_web.py`/`auditar_backend.py`: `--check`, `--self-test`) cruzando `openapi/*.yaml` × controladores × `*WebTest` | Tabla completa | `python3 scripts/inventario_endpoints.py --self-test && python3 scripts/inventario_endpoints.py --check` | TODO |
| H2.S1.M2 | Columna `sensible` según metaprompt §90.5 y §26; sección "Para el CI" en `carriles/PR4-seguridad.md` con el paso exacto para Pablo | Columna + paso | revisión | TODO |
| H2.S1.M3 | Prueba negativa: endpoint sin contrato en una rama temporal → exit 1 → revertir | Rojo demostrado | evidencia | TODO |

#### H2.S2 — Entrada: mass assignment, límites, SQL, SSRF, uploads (plan H7.S3)

**CA:** Dado cada contrato, `additionalProperties: false` y `maxLength/maximum/maxItems/paginación con máximo`; dado el código, ningún `DSL.field(variable)`, `DSL.condition(String)`, `execute(String)` ni `String.format` con SQL sin `// SQL-SEGURO:`; ninguna URL saliente provista por el usuario; `comun-archivos` valida tamaño, magic bytes, nombre aleatorio, objeto privado, URL firmada corta.
**DoD:** 3 scripts exit 0; `ArchivosSeguridadTest` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | `scripts/verificar_contratos_limites.py` (`--self-test`) + corregir contratos de `aportes`; para otros servicios, hallazgo al dueño con ruta | exit 0 en `aportes`; hallazgos listados | comando | TODO |
| H2.S2.M2 | Regla SQL en `verificar_seguridad.py` (whitelist con comentario `SQL-SEGURO:`); revisar los `fetchOne(String, ?)` con bind (p. ej. `OrdenRetiroRepositorio:140-150`) y marcarlos | exit 0 | `python3 scripts/verificar_seguridad.py` | TODO |
| H2.S2.M3 | Inventario de clientes HTTP salientes y URLs (`*PorHttp`, `RestClient`, `HttpClient`) → `security-matrix.md` §SSRF; si hay fetch de URL de usuario → whitelist de esquemas, bloqueo de rangos privados/metadata, timeout, ≤ 3 redirects + test | Tabla; tests si aplica | revisión / comando | TODO |
| H2.S2.M4 | `ArchivosSeguridadTest` en `comun-archivos`: tamaño máximo, magic bytes ≠ MIME → rechazo, nombre aleatorio, objeto privado, URL firmada con TTL corto | PASS o hallazgos a Leo | `./gradlew :plataforma:comun-archivos:integrationTest --tests '*ArchivosSeguridadTest*'` | TODO |

### H3 — Las invariantes del libro demostradas y el advisory lock medido antes de tocarlo

**CA:** Dado los 11 escenarios del plan §H8.S2, cuando corren contra PostgreSQL real, entonces `SUM(debe)=SUM(haber)` por transacción y la suma de saldos del sistema se preserva, sin deadlocks; dado 200 transferencias concurrentes, existen throughput, p50/p95/p99, espera del advisory lock, conexiones y deadlocks medidos; `financial-invariants.md` documenta cada invariante con dónde vive y qué test la demuestra.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*LibroInvariantesTest*'` PASS (11); `evidencia/H3-benchmark-hashchain.txt`; `financial-invariants.md`.
**Estado:** TODO

#### H3.S1 — Grep de dinero y once escenarios (plan H8.S1.M1, H8.S2)

**CA:** Dado las 12 palabras del metaprompt §14, cuando se buscan junto a `double|float`, entonces la tabla de ocurrencias tiene veredicto por fila; dado cada escenario, el cuadre por transacción es 0.
**DoD:** `LibroInvariantesTest` 11 PASS con la consulta de cuadre pegada por escenario.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | `grep -rnE "\b(double\|float\|Double\|Float)\b" --include=*.java servicios plataforma` + las 12 palabras → tabla en `financial-invariants.md` | Tabla con veredicto | grep pegado | TODO |
| H3.S1.M2 | Escenarios 1–5 (transferencia OK, saldo insuficiente, moneda distinta, cuenta bloqueada, P2P no permitido) sobre `BaseDeBilletera`; cuadre `SELECT transaccion_id, SUM(CASE sentido …) FROM movimiento_billetera GROUP BY 1` = 0 | 5 PASS | comando | TODO |
| H3.S1.M3 | Escenarios 6–8: 100 hilos sobre una cuenta (sin saldo negativo, sin pérdida, sin duplicación, suma preservada); dos opuestas simultáneas; replay idempotente (usa el scope corregido por Justin si ya está en `dev`; si no, la aserción de replay queda `A MEDIAS` declarada) | 3 PASS | comando + conteos | TODO |
| H3.S1.M4 | Escenarios 9–11: rollback; excepción tras débito dentro de `Datos.conContexto`; transferencias cruzadas A→B/B→A ×50 con `pg_stat_database.deadlocks` sin incremento | 3 PASS | comando + `SELECT deadlocks FROM pg_stat_database WHERE datname=current_database()` | TODO |

#### H3.S2 — Benchmark del advisory lock y documento de invariantes (plan H8.S3)

**CA:** Dado 200 transferencias concurrentes en 3 corridas, cuando termina el benchmark, entonces hay throughput, p50/p95/p99, `wait_event` del advisory lock, conexiones, CPU y deadlocks; la decisión es **mantener** salvo medición que muestre el lock como cuello de botella, y cualquier alternativa preserva la integridad criptográfica y queda `DECISION_REQUIRED`.
**DoD:** `evidencia/H3-benchmark-hashchain.txt` con las 6 métricas; sección de decisión en `financial-invariants.md`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Localizar el advisory lock en `sql/40_reglas/restricciones.sql` (trigger de `transaccion_billetera`/`hash_registro`) y documentarlo con línea | ruta:línea | revisión | TODO |
| H3.S2.M2 | `LibroBenchmarkTest` `@Tag("benchmark")` (excluido de los corredores; se corre a mano) o script k6 contra compose: 200 hilos × 3 corridas | Métricas pegadas | comando del test | TODO |
| H3.S2.M3 | Decisión escrita (mantener por omisión); si se propone alternativa → ADR + `DECISION_REQUIRED` sin implementar | Sección | revisión | TODO |
| H3.S2.M4 | `financial-invariants.md` completo: balances, ledger, transfer, withdrawal, fees, guarantees, settlements, reconciliation, redondeo, idempotencia — invariante · dónde vive (SQL/Java) · test | 10 secciones | `grep -c "^## " docs/auditoria-produccion/financial-invariants.md` ≥ 10 | TODO |

### H4 — La base desde cada servicio: RLS, grants, append-only, esquema desde cero y re-aplicado

**CA:** Dado la conexión de cada `svc_*`, cuando intenta leer/escribir fuera de su esquema, saltar `FORCE ROW LEVEL SECURITY`, o editar el libro/bitácoras/`evento_consumido`, entonces la base lo rechaza; el rol auditor solo lee; `aplicar.sql` aplica en vacío y **re-aplica** sobre una base con datos sin perderlos.
**DoD:** `./gradlew integrationTest --tests '*AislamientoEsquemaTest*'` PASS ×14; `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*AppendOnlyTest*'` PASS; conteos antes/después de la re-aplicación iguales; `docs/operacion/schema-changes.md`.
**Estado:** TODO

#### H4.S1 — RLS, grants y append-only por servicio (plan H10.S1)

**CA:** Dado la tabla de cobertura de `AislamientoEsquemaTest` + `verificaciones.sql` contra el metaprompt §47, cuando falta un caso, entonces se agrega parametrizado por servicio.
**DoD:** ×14 PASS; `AppendOnlyTest` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Leer `comun-pruebas/AislamientoEsquemaTest` y `sql/50_verificacion/verificaciones.sql`; tabla de cobertura (lectura/escritura permitida, otros esquemas, RLS, `FORCE RLS`, auditor, migración con privilegios limitados) en `carriles/PR4-seguridad.md` | Tabla | revisión | TODO |
| H4.S1.M2 | Casos faltantes como test parametrizado por servicio (conexión real `svc_<x>` del contenedor) en cada `servicios/<x>/src/test/.../AislamientoEsquemaTest` (archivo reservado para vos) | ×14 PASS | comando | TODO |
| H4.S1.M3 | `AppendOnlyTest` (nucleo-financiero): `UPDATE`/`DELETE` con `svc_nucleo_financiero` sobre `transaccion_billetera`, `movimiento_billetera`, bitácoras y `evento_consumido` → error de permiso/trigger | PASS | comando | TODO |

#### H4.S2 — Esquema desde cero, re-aplicación y semillas (plan H10.S2)

**CA:** Dado una base vacía → `aplicar.sql` exit 0 y 305 tablas; dado una base con semillas dev y filas de prueba → re-aplicar `aplicar.sql` conserva las filas (AMB-7); la guarda de semillas dev en producción está referenciada como evidencia del CI.
**DoD:** salidas pegadas; `schema-changes.md` escrito.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | `empty → latest` local con salida | exit 0; conteo de tablas | `docker exec -i aportaya-postgres psql -v ON_ERROR_STOP=1 -U pasanaku -d pasanaku -f - < sql/aplicar.sql; echo exit=$?` | TODO |
| H4.S2.M2 | `latest → latest` con datos: sembrar dev, insertar filas sintéticas, re-aplicar, comparar conteos | Iguales | consultas antes/después pegadas | TODO |
| H4.S2.M3 | `docs/operacion/schema-changes.md`: no hay migraciones versionadas; cómo se expande/contrae hoy; `DECISION_REQUIRED` Flyway/Liquibase | Documento | revisión | TODO |
| H4.S2.M4 | Guarda de semillas dev en producción: enlazar la corrida del CI (job `base`, paso 10) como evidencia; reproducir local | Salida pegada | pasos de `ci.yml` job `base` 9–10 | TODO |

### H5 — Toda operación crítica deja rastro append-only y la matriz de seguridad lo demuestra

**CA:** Dado login, login fallido, challenge MFA, cambio de rol/permiso, transferencia, retiro, aprobación, rechazo, cambio de configuración sensible, cuando ocurren, entonces hay fila append-only con actor, acción, target, timestamp, correlationId, IP/dispositivo, estado anterior/nuevo (si aplica), sin secretos; `security-matrix.md` cubre OWASP API Top 10:2023 fila por fila.
**DoD:** `./gradlew integrationTest --tests '*AuditoriaCriticaTest*'` PASS en los servicios con operaciones críticas; `security-matrix.md` con 10 categorías + filas del §90.5.
**Estado:** TODO

#### H5.S1 — Auditoría y matriz (plan H7.S6)

**CA:** Dado el mecanismo de bitácora encadenada (`auditoria`, `Traza`, `bitacora_*`), cuando un CU crítico no lo usa, entonces `AuditoriaCriticaTest` lo deja en rojo y el hallazgo va al dueño.
**DoD:** tests verdes o hallazgos con ruta; matriz completa.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | Localizar la bitácora encadenada y qué CU la usan; tabla en `security-matrix.md` | Tabla | revisión | TODO |
| H5.S1.M2 | `AuditoriaCriticaTest` por servicio con operación crítica (identidad, nucleo-financiero, aportes, cumplimiento): rojo donde falte; en `aportes` lo corregís vos; en los demás, hallazgo al dueño (Richard, Justin; cumplimiento sin dueño este turno → queda `A MEDIAS` declarado) | PASS en `aportes`; hallazgos listados | `./gradlew :servicios:aportes:integrationTest --tests '*AuditoriaCriticaTest*'` | TODO |
| H5.S1.M3 | `security-matrix.md` (Componente, Amenaza, Control, Test, Evidencia, Estado, Riesgo residual) × OWASP API Top 10:2023 + áreas del §90.5 | 10 categorías | `grep -c "^## " docs/auditoria-produccion/security-matrix.md` ≥ 10 | TODO |

### H6 — Mutation testing evaluado, código muerto fuera, dependencias con higiene

**CA:** Dado PIT sobre `Dinero`, `CostoDeOperacion`, `CondicionesDeRetiro`, `EstadoDeRetiro`, `Idempotencia`, `SegundoFactorStepUp`, `EmisorDeEvidencia` (los que existan al momento), cuando corre, entonces hay score por clase y mutantes sobrevivientes documentados; no quedan adapters sin uso, `TODO` en P0, ni flags inseguros; el informe de dependencias no aplica majors.
**DoD:** `./gradlew :servicios:nucleo-financiero:pitest` exit 0; `mutation-testing.md`; `git grep -nE "TODO|FIXME" -- servicios plataforma` sin `TODO` en P0; `dependencias.md`.
**Estado:** TODO

#### H6.S1 — PIT (plan H10.S4)

**CA:** Dado el plugin PIT compatible con Gradle 9.7 y JUnit 5 (**verificá versión en su doc antes**), cuando se aplica solo a `nucleo-financiero`, `comun-web`, `identidad`, entonces genera reporte sin tocar el CI normal.
**DoD:** reporte + documento.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H6.S1.M1 | Plugin PIT en `buildSrc` bajo una convención opcional (`aportaya.mutacion`) → **micro-PR al troncal** coordinado con Leo (dueño de `buildSrc`) y Pablo (`libs.versions.toml`) | `pitest` corre | `./gradlew :servicios:nucleo-financiero:pitest` exit 0 | TODO |
| H6.S1.M2 | `mutation-testing.md`: score por clase, sobrevivientes relevantes, qué test se agregó (en tu módulo) o hallazgo al dueño | Documento | revisión | TODO |

#### H6.S2 — Código muerto, flags y dependencias (plan H11.S2, H11.S3)

**CA:** Dado el inventario (beans sin uso verificando wiring por reflexión/Spring, configs duplicadas, endpoints abandonados, `TODO`/`FIXME`, dobles sin `@Profile`), cuando cada ítem tiene decisión, entonces lo confirmado muerto **en tus módulos** se borra y lo ajeno va como hallazgo; los 7 comentarios `idempotencia.exigirNueva` se resuelven según ADR-046 de Leo (adoptar o borrar) — si el ADR no está en `dev`, aplicás el supuesto "solo efecto financiero/irreversible" y lo declarás.
**DoD:** `./gradlew check` verde en `aportes`; `dependencias.md`; `git grep` pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H6.S2.M1 | Inventario con decisión por ítem en `carriles/PR4-seguridad.md` | Tabla | `git grep -nE "TODO\|FIXME" -- servicios plataforma` pegado | TODO |
| H6.S2.M2 | Borrar lo confirmado muerto en `aportes` y `scripts/`; hallazgos para el resto | `check` verde | `./gradlew :servicios:aportes:check` | TODO |
| H6.S2.M3 | Los 7 esqueletos `idempotencia.exigirNueva` (`grupos`, `identidad/CU09`): hallazgo con la decisión aplicable por CU (los archivos son de otros: no los editás) | 7 filas | tabla | TODO |
| H6.S2.M4 | `dependencias.md`: sin uso, obsoletas, duplicadas, transitivas innecesarias (por módulo, con `./gradlew :<m>:dependencies`), **sin** majors | Documento | revisión | TODO |
| H6.S2.M5 | Parches/minors con CVE aplicables en `aportes` (uno por commit, `verificar` verde); el resto como hallazgo a Pablo (OSV) | Verde | `./gradlew :servicios:aportes:webTest :servicios:aportes:integrationTest` | TODO |
| H6.S2.M6 | `carriles/PR4-seguridad.md` completo (6 campos por hito), merge final + espejo `test` | Mergeado | ritual | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 (= AMB-7) | Migraciones `N-1 → N`: no existen | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: este turno sigue con `sql/aplicar.sql` generado (idempotente) y **solo cambios aditivos** al esquema (sin `DROP COLUMN`/`DROP TABLE`/cambio de tipo); se verifica `empty→latest` y `latest→latest` con datos; la adopción de Flyway/Liquibase queda como ADR posterior a la promoción, no se hace ahora |
| Q-02 | Pasarela real del webhook y su esquema de firma | Negocio | Nada | **DECIDIDA (2026-09-21)**: doble de la pasarela con firma HMAC-SHA256 sobre el cuerpo crudo + `X-Firma` + `X-Timestamp` (ventana ±5 min), en tres niveles; si el CU ya define otro esquema de firma, manda el CU y se anota |
| Q-03 | Alternativa al advisory lock global | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: mantener el advisory lock global; cualquier alternativa exige la medición de H3.S2 y un ADR, y no se implementa este turno |
| Q-04 | Qué es "código muerto" cuando Spring cablea por reflexión | Vos | Nada | **DECIDIDA (2026-09-21)**: nada se borra sin `ArranqueTest` ×14 en verde después; lo que Spring cablea por reflexión se busca con `grep -rn` del nombre simple y de `@Bean`/`@Import` antes de decidir |
| Q-05 | Tests transversales en módulos ajenos | Coordinación | Nada | **DECIDIDA (2026-09-21)**: los nombres de archivo de test reservados (§4 del daily) son de Marcelo en cualquier módulo; el código de producción es del dueño |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` solo
      por `DECISION_REQUIRED`.
- [ ] `carriles/PR4-seguridad.md` y tu daily con el avance calculado en la primera línea, y la
      sección "Para el CI" con los pasos que Pablo debe agregar.
- [ ] Evidencia literal en `evidencia/`: consultas de cuadre, benchmark, conteos de re-aplicación,
      pruebas negativas de cada script; sin datos reales.
- [ ] Gates: `evidence-and-verification` siempre; `api-pentest` y `secure-code-review` en H2/H5;
      `accounting-double-entry` en H3; `integrity-testing` en H4; `data-privacy-financial` en H1.S2 y H5.
- [ ] Ningún test en rojo mergeado: lo rojo por bug ajeno queda en tu rama, declarado, con el
      hallazgo entregado al dueño.
- [ ] Todo lo verde mergeado en `dev` y espejado en `test`.
- [ ] Peldaño de evidencia declarado por hito (regla 30).
