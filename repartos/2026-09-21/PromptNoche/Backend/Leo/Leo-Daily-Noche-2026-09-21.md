# Daily de Leo — turno noche — 2026-09-21

> **AVANCE: 25 / 49 — 51,0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`. Worktree aislado: `PasanakuBackend-leo`. PRs #4, #9, #10, #12, #13,
> #14, #16, #20 mergeados a `dev` (ninguno bloqueado por el clasificador de permisos) y
> espejados a `test`. **PR #22 abierto y verde, bloqueado por el clasificador de permisos**
> (`Merge Without Review`) — listo para merge humano, no un bloqueo de trabajo real. **H1 cerrado
> salvo H1.S2.M3** (hallazgo real, §6). **H2.S1/S2/S3 cerrados salvo H2.S3.M5 y el verde de la CA
> de punta a punta**: `Relevo` con envelope de 8 cabeceras (`EnvelopeDeEvento.java`),
> tomar-publicar-marcar en 2 transacciones cortas (nunca Kafka dentro de una transacción de
> PostgreSQL), backoff con jitter, `FALLIDO` como DLQ lógica; `Consumidos.registrar` probado
> contra PostgreSQL real (H2.S2.M5, verde real); `OutboxE2ETest` escrito con Kafka real de
> Testcontainers (H2.S2.M3, rojo real — el DoD literal de esa microtarea). **Hallazgo nuevo
> F-Leo-06: `BaseDePrueba.kafka()` no arranca en esta máquina** (Docker Desktop/Windows/npipe +
> `testcontainers-kafka` 1.21.3 calcula `advertised.listeners=0.0.0.0`) — tres intentos reales de
> solución sin éxito, diagnosticado hasta la causa real, registrado sin fabricar un verde. Falta
> H2.S3.M5 y todo H2.S4 (bloqueados por F-Leo-06). `ArranqueTest` × 14 confirmado en verde después
> de cada merge (único rojo persistente: `nucleo-financiero` `ArranqueProduccionTest`,
> pre-existente y documentado en ese carril, no el mío).
>
> **Nota de sesión:** un rate-limit semanal de la cuenta cortó la sesión a mitad de H2.S3.M4; se
> retomó sin pérdida de trabajo (worktree tenía exactamente los cambios en curso, sin nada
> corrupto ni descartado) y se cerró la microtarea normalmente.

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
| H2 — Outbox que publica: bean, lock, cabeceras, backoff, Kafka caído, reinicio | 20 | 14 | H2.S1/S2/S3 cerrados salvo H2.S3.M5 y el verde de la CA (F-Leo-06); H2.S4 TODO |
| H3 — Guardas comunes: decodificador, guarda de producción, perfiles, errores | 9 | 1 | H3.S3.M1 (plantilla de perfiles) mergeado en la primera hora; resto TODO |
| H4 — Barridos, `Dinero`, logs JSON, probes, ArchUnit compartido | 8 | 0 | TODO |
| **TOTAL** | **49** | **25** | |

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
| H2.S3.M4 | `comun-mensajeria` sin `BarridoTest` todavía; `sin-umbral-literal` ya daba verde (`aportaya.outbox.*` vía `@Value` desde H2.S1.M2/H2.S3.M3), pero `tamano-archivo` dio rojo real: `Relevo.java` en 306 líneas. Separado `mensaje()`/`trazaDe()` a `EnvelopeDeEvento.java` (73 líneas nuevas); `Relevo.java` queda en 250 | `./gradlew :plataforma:comun-mensajeria:testBarrido` | Ciclo rojo→verde real: `Expecting empty but was: ["...Relevo.java  306 lineas (limite 300)"]` → `BUILD SUCCESSFUL in 11s`. Gate completo (`test`+`testBarrido`+`integrationTest`) verde antes Y después del merge con el remoto. `ArranqueTest`×14: único rojo, `nucleo-financiero ArranqueProduccionTest`, pre-existente y documentado en ese carril. **PR #22** abierto, bloqueado por el clasificador (`Merge Without Review`) |
| H2.S2.M5 | `Consumidos.registrar` (ya existía) probado contra PostgreSQL real: primera vez registra, entrega doble no repite el efecto, dos consumidores independientes. Nombrado `ConsumidosRepositorioTest` (no `ConsumidosTest` literal) para caer en `integrationTest` | `./gradlew :plataforma:comun-mensajeria:integrationTest --tests '*ConsumidosRepositorioTest*'` | `BUILD SUCCESSFUL in 40s` — verde real, 3/3 |
| H2.S2.M3 | `OutboxE2ETest`: `Relevo` real publica por `KafkaTemplate` real a un broker de Testcontainers, `KafkaConsumer` real verifica las 8 cabeceras. Al arrancar el contenedor de Kafka por primera vez de verdad en este carril (antes solo se había *compilado* la fixture, nunca arrancado), no levanta en esta máquina | `./gradlew :plataforma:comun-mensajeria:e2eTest --tests '*OutboxE2ETest*'` | **Rojo real — es el DoD literal de esta microtarea** ("`OutboxE2ETest` en rojo... comando → FAIL"). Diagnosticado hasta la causa real: `advertised.listeners cannot use the nonroutable meta-address 0.0.0.0` — ver F-Leo-06 |

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
| F-Leo-06 | `BaseDePrueba.kafka()` (mi propio archivo, H2.S2.M2) no arranca en esta máquina: `org.testcontainers.kafka.KafkaContainer` (`testcontainers-kafka` 1.21.3) falla con `Timed out waiting for log output matching '.*Transitioning from RECOVERY to RUNNING.*'`. Diagnosticado hasta la causa real (`TESTCONTAINERS_RYUK_DISABLED` + `.withLogConsumer` temporal): Kafka mismo aborta con `IllegalArgumentException: advertised.listeners cannot use the nonroutable meta-address 0.0.0.0`. La imagen está sana (`docker run apache/kafka:3.9.0` sin Testcontainers arranca en ~8s); es un defecto de cómo el módulo calcula el listener contra Docker Desktop/Windows con `npipe`. Tres intentos reales sin éxito: `TESTCONTAINERS_HOST_OVERRIDE=localhost`, reinicio del daemon de Gradle, y verificación (sin aplicar, sin evidencia de que aplique) de `KafkaContainer.withListener(String)` vía `javap` | Todo el equipo — cualquiera que use `BaseDePrueba.kafka()` en esta máquina | Registrado con diagnóstico completo, no arreglado (necesita subir versión de `testcontainers-kafka` o reconfigurar Docker Desktop, ninguna decisión de un solo carril) |

## 7. No cubierto

- `respuesta_idempotente` en esquemas fuera de `nucleo_financiero` (H1.S2.M3, bloqueado — ver §5).
- La regla `ClaveIdempotenciaSuelta` solo corre en `comun-web`: no se validó (ni se intentó) contra
  `servicios/**`, donde F-Leo-04 vive sin que ningún gate automático lo detecte hoy.
- `docker port aportaya-postgres` puede cambiar si el contenedor se reinicia con otro mapeo — el
  valor `5543` usado en esta sesión no está garantizado para la próxima.
- La CA de punta a punta de H2.S2 (fila → Kafka real → consumidor → `PUBLICADO`) y todo H2.S4
  (kill-test Kafka abajo/arriba, huérfano `TOMADO` al reiniciar) — bloqueados por F-Leo-06, no por
  falta de código: `OutboxE2ETest` ya está escrito con las aserciones completas, solo falta que
  el broker de Testcontainers pueda arrancar en esta máquina.

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-10) | Consumidor Kafka | — | DECIDIDA: solo de prueba en `src/e2eTest` |
| Q-02 | Backoff e `intentos-maximos` | — | DECIDIDA: 10 · PT1S · PT5M · jitter ±20 % · timeout PT10S, en configuración |
| Q-03 | `FALLIDO` vs tema DLQ | — | DECIDIDA: misma tabla + métrica + runbook |
| Q-04 (AMB-12) | Perfiles | — | DECIDIDA: `local/test/staging/production`; productivo = todo lo que no sea local/test |
| Q-05 | `aud` | — | DECIDIDA: global para acceso, por servicio para evidencia |
