# Daily de Leo — turno noche — 2026-09-21

> **AVANCE: 22 / 49 — 44,9 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`. Worktree aislado: `PasanakuBackend-leo`. PRs #4, #9, #10, #12, #13,
> #14, #16, #20 mergeados a `dev` (ninguno bloqueado por el clasificador de permisos) y
> espejados a `test`. **H1 cerrado salvo H1.S2.M3** (hallazgo real, §6). **H2.S1 cerrado; gran
> parte de H2.S2/H2.S3 también**: `Relevo` con envelope de 8 cabeceras, tomar-publicar-marcar en
> 2 transacciones cortas (nunca Kafka dentro de una transacción de PostgreSQL), backoff con
> jitter, `FALLIDO` como DLQ lógica. Falta `OutboxE2ETest` con Kafka real (H2.S2.M3/M5), el resto
> de H2.S3 y todo H2.S4. `ArranqueTest` × 14 confirmado en verde después de cada merge.

- **Persona:** Leo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** `plataforma/comun-*`, `buildSrc`, plantilla de servicios
- **Tu encargo:** [Plataforma: outbox que publica, helper de idempotencia y guardas comunes](PR3-Plataforma.Infra/OutboxQuePublicaYGuardasComunes.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Rama:** `leo/feature/carril-PR3-plataforma` → PRs a `dev`, espejo a `test`. **La plantilla de perfiles (H3.S3.M1) se mergea en la primera hora.**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `async-messaging-events`, `concurrency-and-locking`, `microservices-testing`, `distributed-tracing-correlation`, `backend-observability`, `environment-secrets-config`, `error-handling-contract`, `authn-identity`, `static-analysis-linting`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
261
$ python .claude/hooks/plan_gate.py --self-test
plan_gate self-test: 11 PASS, 0 FAIL
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — Helper `Idempotencia` con usuario, operación y hash | 12 | 10 | Cerrado salvo H1.S2.M3 (hallazgo, §6) |
| H2 — Outbox que publica: bean, lock, cabeceras, backoff, Kafka caído, reinicio | 20 | 11 | H2.S1 cerrado; H2.S2/S3 parciales; H2.S4 TODO |
| H3 — Guardas comunes: decodificador, guarda de producción, perfiles, errores | 9 | 1 | H3.S3.M1 (plantilla de perfiles) mergeado en la primera hora; resto TODO |
| H4 — Barridos, `Dinero`, logs JSON, probes, ArchUnit compartido | 8 | 0 | TODO |
| **TOTAL** | **49** | **22** | |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H3.S3.M1 | Plantilla `application-{local,test,staging,production}.yml` en `nuevo_servicio.py` + `management.endpoints.web.exposure.include` (hallazgo F-05 de Pablo, PR5) | `gh pr merge 4 --rebase` | PR #4 mergeado, primera hora del turno |
| H1.S1.M1 | Baseline de `plataforma/*` (6 módulos) | ver `docs/auditoria-produccion/baseline-PR3-plataforma.md` | 4/6 PASS; 2 rojos de entorno (Testcontainers timeout por contención, `python3` roto en Windows — corregido) |
| H1.S1.M2–M5 | `IdempotenciaRepositorioTest` (10 casos) — identidad completa `(usuario_id, operacion, clave)`, hash comparado, `IdempotenciaConflicto`/`IdempotenciaEnProceso` (409) | `./gradlew :plataforma:comun-web:integrationTest --tests '*IdempotenciaRepositorioTest*'` | Ciclo rojo→verde real (3 corridas, 2 bugs genuinos encontrados y corregidos) → `BUILD SUCCESSFUL in 7m 42s`; `ArranqueTest` × 14 → `BUILD SUCCESSFUL in 41m 10s` |
| H1.S2.M1 | `aportaya.idempotencia.vigencia` externalizada (default `PT24H`) | gate local `comun-web` completo | `BUILD SUCCESSFUL in 8m 44s`; `ArranqueTest` × 14 → `BUILD SUCCESSFUL in 29m 46s` |
| H1.S2.M2 | "En proceso"/50 hilos | ya cubierto por `IdempotenciaRepositorioTest` | Sin código nuevo |
| H1.S3.M1 | `ADR-046` enlazado; bóveda tenía 3 FALLAs reales (mías) | `python3 scripts/verificar_boveda.py` | `TODO OK` (antes: 3 FALLAS) |
| H1.S3.M2 | Regla `ClaveIdempotenciaSuelta` (opt-in, `comun-web`); primer `BarridoTest` de `plataforma/` encontró 2 hallazgos reales propios (falso positivo `sin-umbral-literal`, archivo de 338 líneas) | gate local | `BUILD SUCCESSFUL in 3m 25s` |
| H2.S1.M1-M5 | `Relevo` como bean real (`ConfiguracionMensajeria`: `@EnableScheduling`+`@EnableSchedulerLock`, `LockProvider` sobre `<esquema>.shedlock`, condicionado a `KafkaTemplate` presente); API de ShedLock 6.9.0 verificada con `javap` contra el jar, no adivinada | `RelevoConfiguracionTest` | 3/3 PASS tras rojo genuino (compile error); `ArranqueTest`×14 `BUILD SUCCESSFUL in 19m41s`/`29m46s` |
| H2.S2.M2/M4, H2.S3.M1-M3 | Envelope de 8 cabeceras Kafka; `tomado_en/tomado_por/ultimo_error/proximo_intento_en`+`TOMADO` en `evento_dominio` (14 esquemas); `relevar()` sin `@Transactional`, tomar/publicar-fuera-de-tx/marcar en 2 transacciones cortas; backoff exponencial+jitter; `FALLIDO`=DLQ lógica | `RelevoRepositorioTest` | 5/5 PASS tras 2 corridas rojas (bug real: cast sin tipar de jOOQ a `OffsetDateTime`); `ArranqueTest`×14 confirmado (con el hallazgo de `identidad` abajo) |

## 4. A medias — las cuatro respuestas, obligatorias

### <ID> — <título>
- **Qué anda:**
- **Qué no anda:**
- **Qué falta exactamente:**
- **Dónde quedó:** <rama, archivos, si compila>

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| H1.S2.M3 | `respuesta_idempotente` en esquemas `grupos`/`identidad` | Agregué el entity a los `.puml` y corrí `generar_ddl.py` (generó limpio) — pero antes de commitear encontré que `sql/40_reglas/restricciones.sql` aplica sus `CHECK` con `ALTER TABLE respuesta_idempotente` **sin calificar esquema**, bajo un `search_path` compartido: con la tabla en 3 esquemas, el `CHECK` solo alcanzaría al primero (`grupos`), dejando `identidad`/`nucleo_financiero` sin validar. Revertí `sql/`/`docs/entidades/*.puml` para no mergear el defecto | Calificar `ALTER TABLE <esquema>.respuesta_idempotente` (o generar el bloque una vez por esquema) en el generador de `docs/Restricciones.md` → `scripts/extraer_sql.py` — no es mi archivo | Quien tenga `docs/Restricciones.md`/`scripts/extraer_sql.py` (posiblemente Pablo) |

> Recordá la regla 65: el outbox se prueba de punta a punta con un emisor y un consumidor de
> prueba propios (H2.S2); no necesitás ningún caso de uso ajeno. Solo una decisión de negocio
> queda abierta.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| F-Leo-01 | `restricciones.sql` no escala a una tabla en más de un esquema (`ALTER TABLE <tabla>` sin calificar, bajo `search_path` compartido) | Quien tenga `docs/Restricciones.md`/`scripts/extraer_sql.py` | Registrado, no arreglado (fuera de mi alcance) |
| F-Leo-02 | `plataforma/comun-web/build.gradle.kts` (`erroresCatalogo`) y el `build.gradle.kts` raíz usaban `executable = "python3"`, que en Windows resuelve al alias de la Microsoft Store (exit 9009) y no al intérprete real, aunque `python` sí funciona | Corregido en `comun-web` (mío). El mismo patrón sigue en el `build.gradle.kts` raíz — dueño de CI/build (Pablo) | Corregido parcialmente; raíz pendiente |
| F-Leo-03 | `generateJooq` (y por transitividad `ArranqueTest`) usa por defecto `jdbc:postgresql://127.0.0.1:5433/pasanaku`; en esta máquina el contenedor real `aportaya-postgres` está en `127.0.0.1:5543` (verificado con `docker port`), no en 5433 ni en 5435 como decía `local-override.postgres.yml`. Hay que pasar `BD_URL_ADMIN`/`BD_USUARIO_ADMIN`/`BD_CLAVE_ADMIN` explícitos | Cualquiera que corra `generateJooq`/`ArranqueTest` en esta máquina compartida | Hallazgo de entorno, no de código — workaround documentado, no una corrección de repo |
| F-Leo-04 | `.where(DSL.field("clave_idempotencia")` sin `.and(...)` en `servicios/aportes/PagoRepositorio.java:56`, `servicios/notificaciones/EnvioRepositorio.java:66`, `servicios/organizador/AutomatizacionRepositorio.java:87` — puede ser intencional (diseño de unicidad propio de esas tablas, no relacionado con el helper `Idempotencia`), no investigado a fondo | Dueños de `aportes`, `notificaciones`, `organizador` | Registrado, no investigado (`servicios/**` fuera de mi alcance) |
| F-Leo-05 | `generateJooq` lee del contenedor **compartido** `aportaya-postgres`, no de un Testcontainers efímero. Un cambio de esquema (mi H2.S3.M1) queda invisible para `generateJooq` hasta aplicarlo también ahí — `identidad:ArranqueTest` falló por esto (`EsquemaAlDiaRepositorioTest` comparando jOOQ stale vs. Testcontainers fresco). Corregido con una migración aditiva contra el contenedor compartido; **cualquiera que agregue una columna a una tabla compartida (outbox, shedlock) va a pisar esto de nuevo** salvo que se documente el paso | Todo el equipo — cualquier cambio de esquema compartido | Workaround aplicado esta vez; sin mecanismo automático todavía |

## 7. No cubierto

- `respuesta_idempotente` en esquemas fuera de `nucleo_financiero` (H1.S2.M3, bloqueado — ver §5).
- La regla `ClaveIdempotenciaSuelta` solo corre en `comun-web`: no se validó (ni se intentó) contra
  `servicios/**`, donde F-Leo-04 vive sin que ningún gate automático lo detecte hoy.
- `docker port aportaya-postgres` puede cambiar si el contenedor se reinicia con otro mapeo — el
  valor `5543` usado en esta sesión no está garantizado para la próxima.

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-10) | Consumidor Kafka | — | DECIDIDA: solo de prueba en `src/e2eTest` |
| Q-02 | Backoff e `intentos-maximos` | — | DECIDIDA: 10 · PT1S · PT5M · jitter ±20 % · timeout PT10S, en configuración |
| Q-03 | `FALLIDO` vs tema DLQ | — | DECIDIDA: misma tabla + métrica + runbook |
| Q-04 (AMB-12) | Perfiles | — | DECIDIDA: `local/test/staging/production`; productivo = todo lo que no sea local/test |
| Q-05 | `aud` | — | DECIDIDA: global para acceso, por servicio para evidencia |
