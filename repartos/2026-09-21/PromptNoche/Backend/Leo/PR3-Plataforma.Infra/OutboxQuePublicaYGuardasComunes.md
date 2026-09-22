# Plataforma: el outbox que por fin publica en Kafka sin bloquear PostgreSQL, el helper de idempotencia con la identidad del índice, y las guardas comunes que ningún servicio puede olvidar

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Leo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio(s):** `plataforma/comun-web`, `comun-mensajeria`, `comun-pruebas`, `comun-dominio`, `buildSrc`, plantilla `scripts/nuevo_servicio.py`
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Leo-Daily-Noche-2026-09-21.md](../Leo-Daily-Noche-2026-09-21.md)
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (este encargo cubre H1.S1, H1.S4.M4, H2 completo, H5.S2.M1/M3, H5.S5.M1/M2/M4 y la plantilla de H5.S5.M3, H7.S5.M3, H8.S1.M2/M3, H9.S1.M3, H9.S2, H9.S3, H11.S1)
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `leo/feature/carril-PR3-plataforma`
- **4 hitos · 13 subtareas · 49 microtareas** — el carril del que dependen los otros cuatro: **mergeás chico y seguido**, nunca un PR gigante al final

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar (este repo) dentro de `PasanakuBackend/`. El backend trae sus propias skills (`trabajos-outbox`, `entorno-monorepo`, `errores-api`…): **se suman, no se reemplazan**.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `async-messaging-events` | Outbox, at-least-once, consumidor idempotente, backoff y DLQ |
| `concurrency-and-locking` | `SKIP LOCKED`, tomar-publicar-marcar sin lock durante la red, reserva por índice único |
| `microservices-testing` | Kafka y PostgreSQL reales en Testcontainers; apagar el broker a propósito |
| `distributed-tracing-correlation` | `correlationId` de HTTP a Kafka y vuelta |
| `backend-observability` | Métricas del outbox, logs JSON, cardinalidad, probes |
| `environment-secrets-config` | Perfiles por entorno y la guarda de arranque que falla cerrado |
| `error-handling-contract` | `{codigo, mensaje, correlationId, timestamp}` sin stacktrace ni SQL |
| `authn-identity` | Validación de `iss`/`aud`/skew en el decodificador común |
| `static-analysis-linting` | Reglas de barrido y ArchUnit compartidas |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre del turno con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 65 · 90 · 96 · **98**

## 2. Resultado observable

Cualquier servicio que escriba en su `evento_dominio` ve el evento en Kafka en menos de 5 segundos con `event_id`, `correlation_id` y `trace_id` en las cabeceras, la fila pasa a `PUBLICADO`, y con Kafka apagado el evento espera con backoff y se publica al volver; el helper `Idempotencia` distingue usuarios y operaciones y devuelve `409` ante la misma clave con otro cuerpo; ningún servicio con perfil `production` arranca con placeholders, CORS `*` ni dobles de desarrollo; todo token con `iss`/`aud` equivocados da `401` en cualquier servicio.

**Kill-test:** con `compose --profile base` + un servicio, insertar a mano una fila `PENDIENTE` en `<esquema>.evento_dominio` y esperar 10 s. Si sigue `PENDIENTE`, el relevo no existe y esto NO está hecho. (Hoy es exactamente lo que pasa: `Relevo.java` no es bean en ningún servicio.)

## 3. Alcance

**IN:** `plataforma/comun-web/**`, `plataforma/comun-mensajeria/**`, `plataforma/comun-pruebas/**`, `plataforma/comun-dominio/**`, `buildSrc/**`, `scripts/nuevo_servicio.py` (plantilla de `application*.yml` de los 14), `docs/Arquitectura/ADR-046 Alcance de la idempotencia.md`, `ADR-047 Semántica de entrega del outbox.md`, `docs/auditoria-produccion/carriles/PR3-plataforma.md`, y **micro-PR al troncal** para las columnas nuevas de `evento_dominio` y la tabla `respuesta_idempotente` en los esquemas que la adopten (generador → `sql/`).

**OUT:** el código de los 14 servicios (cada dueño aplica tu plantilla y tus beans; vos no editás `servicios/**` salvo `ArranqueTest` **no**: ni eso — si un `ArranqueTest` falla por tu bean, el hallazgo va al dueño y vos ajustás el `@ConditionalOn…`). `plataforma/gateway` (Pablo). `.github/workflows` (Pablo). `scripts/verificar_*.py` (Marcelo). Frontends.

**Reservas de archivos:** los seis módulos de `plataforma/` salvo `gateway`; `buildSrc/**`; `scripts/nuevo_servicio.py`; `ADR-046*`, `ADR-047*`; `carriles/PR3-plataforma.md`; `gradle/libs.versions.toml` **solo por micro-PR** (Pablo también lo toca por micro-PR: coordinan en el chat el orden, nunca en el mismo commit). En `sql/` solo lo de tus micro-PR.

### Ritual de entrega — `dev` y `test`, sin esperar a nadie

```bash
git fetch origin && git checkout -b leo/feature/carril-PR3-plataforma origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply :plataforma:comun-web:webTest :plataforma:comun-web:integrationTest :plataforma:comun-mensajeria:integrationTest spotlessCheck
./gradlew integrationTest --tests '*ArranqueTest*'      # tus beans levantan en los 14: es TU gate, aunque los servicios sean ajenos
git push -u origin HEAD
gh pr create --base dev --fill --title "fix(outbox): <subtarea>"
gh pr merge --rebase
git fetch origin && git push origin origin/dev:test   # test es espejo de dev (AMB-R1)
```

- **Micro-PR al troncal** (`sql/` vía generador, `libs.versions.toml`, `buildSrc/`): un commit con solo eso, `troncal(<que>): …`, mergeado dentro de la hora.
- **Jamás te detenés.** Para probar el outbox de punta a punta **no necesitás a Justin**: un emisor de prueba en `comun-mensajeria/src/e2eTest` escribe la fila igual que `Outbox.emitir`. Para el consumidor tampoco: el consumidor es de prueba (AMB-10). Contrato ajeno que no está → doble en tres niveles, declarado.
- CI rojo por job ajeno (Spotless en `dev` hasta que Pablo lo cierre) → hallazgo en tu daily §6, no te detiene. Tu gate local en verde es la condición de merge.
- Un test tuyo en rojo te detiene esa microtarea. Nunca `skip`, nunca `@Disabled`.

### Contratos que vos fijás para los otros (van escritos antes de codificar)

| Contrato | Dónde lo escribís | Quién lo consume |
|---|---|---|
| Cabeceras Kafka del envelope: `event_id`, `type`, `version`, `occurred_at`, `producer`, `correlation_id`, `causation_id`, `trace_id` | `docs/auditoria-produccion/contratos/evento-kafka.md` (H2.S2.M1) | Pablo (traza en gateway), consumidores futuros |
| Propiedades comunes: `aportaya.outbox.{habilitado, intervalo, intentos-maximos, backoff-base, backoff-tope, timeout-publicacion}`, `aportaya.jwt.{emisor, audiencia, tolerancia}`, `aportaya.entorno.productivo`, `aportaya.cors.origenes` | plantilla de `scripts/nuevo_servicio.py` (H3.S3.M1) | Richard, Justin, Marcelo (sus `application-*.yml`), Pablo (compose) |
| `iss=aportaya-identidad`, `aud` de acceso `["aportaya"]`, de evidencia `["aportaya-nucleo-financiero"]` | mismo archivo que Richard: `contratos/step-up-jwt.md` (lo escribe Richard; vos **no** lo editás, lo exigís en el decoder) | Richard emite, Justin valida, vos validás |

## 4. Plan

### H1 — El helper `Idempotencia` distingue usuario y operación, compara el cuerpo y no sirve respuestas ajenas

**CA:** Dado `(U,O,K,H)`: no existe → reserva; existe con `H` igual → respuesta previa; existe con `H` distinto → `409 IDEMPOTENCIA_CONFLICTO`; otro usuario u otra operación con `K` → independiente; expirada → nueva; 50 hilos → 1 reserva.
**DoD:** `./gradlew :plataforma:comun-web:integrationTest --tests '*IdempotenciaRepositorioTest*'` → 10 PASS; `./gradlew :plataforma:comun-web:webTest` PASS; `./gradlew testBarrido` PASS con la regla nueva; ADR-046.
**Estado:** TODO

#### H1.S1 — Los diez casos en rojo y la identidad completa (plan H1.S1.M1–M4)

**CA:** Dado el índice `(usuario_id, clave_idempotencia, operacion)` (`sql/30_indices/10_billetera_custodia.sql:148-149`), cuando `exigirNueva` y `guardarRespuesta` filtran, entonces usan exactamente esas tres columnas y el hash se compara.
**DoD:** los casos "otro usuario", "otra operación", "cuerpo distinto → 409" y "replay" en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | **Primero del turno:** baseline de `plataforma/*` (`test`, `webTest`, `integrationTest` de los seis módulos) con rojos clasificados en `docs/auditoria-produccion/baseline-PR3-plataforma.md` | Archivo con veredicto por módulo | `for m in comun-dominio comun-datos comun-web comun-mensajeria comun-archivos comun-pruebas; do ./gradlew :plataforma:$m:test :plataforma:$m:webTest :plataforma:$m:integrationTest; echo "$m exit=$?"; done` pegado | TODO |
| H1.S1.M2 | `IdempotenciaRepositorioTest` (Testcontainers, esquema `nucleo_financiero`) con los 10 casos **en rojo**: nueva; replay mismo hash; misma clave/cuerpo distinto; otro usuario; otra operación; 50 hilos; expirada; rollback sin reserva; fallo tras reservar → reintento posible; reintento tras error transitorio | 10 tests fallan por aserción | comando → FAIL ×10 | TODO |
| H1.S1.M3 | `exigirNueva`: `SELECT` por `(usuario_id, operacion, clave_idempotencia)` (`Idempotencia.java:43-47`) | 2 casos PASS | comando | TODO |
| H1.S1.M4 | Comparación de `hash_solicitud`: igual → `OperacionRepetida`; distinto → `ErrorDeNegocio` con código `IDEMPOTENCIA_CONFLICTO` (convención `CodigoError.de(...)` + `erroresCatalogo`) → `409` en `ManejadorGlobalDeErrores` | PASS + webTest | comando; `./gradlew :plataforma:comun-web:webTest --tests '*ManejadorGlobalDeErroresWebTest*'`; `./gradlew erroresCatalogo` | TODO |
| H1.S1.M5 | `guardarRespuesta(dsl, ctx, operacion, clave, codigo, cuerpo)` actualiza por la identidad completa (`:85-90`) | Replay devuelve la respuesta de ese usuario | comando | TODO |

#### H1.S2 — Expiración, reserva en proceso y tabla por esquema (plan H1.S1.M5–M7)

**CA:** Dado `expira_en < now()`, cuando se reserva, entonces se reemplaza; dado una reserva sin respuesta final, cuando llega el segundo, entonces `409 EN_PROCESO` (`:77-81` conservado); dado un esquema que adopte el helper, entonces tiene su `respuesta_idempotente`.
**DoD:** casos "expirada", "50 hilos" y `SinUmbralLiteral` en verde; `generar_ddl.py` sin diff residual.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Expiración con `aportaya.idempotencia.vigencia` (default `PT24H`, sin literal; `Reloj` inyectado en vez de `OffsetDateTime.now()`) | PASS; barrido verde | comando; `./gradlew :plataforma:comun-web:testBarrido` | TODO |
| H1.S2.M2 | Reserva en proceso → `409`; 50 hilos → 1 efecto, 49 × 409 | PASS | comando | TODO |
| H1.S2.M3 | `respuesta_idempotente` en los esquemas que adopten el helper (decisión H1.S3.M1) vía `scripts/modelo.py`/`.puml` → **micro-PR al troncal**; grants | `aplicar.sql` en limpio | `python3 scripts/generar_ddl.py && python3 scripts/verificar_boveda.py`; PR `troncal(sql): respuesta_idempotente por esquema` mergeado | TODO |

#### H1.S3 — Regla de barrido y ADR (plan H1.S4.M4, H1.S5.M2/M3)

**CA:** Dado cualquier `.where(DSL.field("clave_idempotencia")` sin otra condición en la misma cadena, cuando corre `testBarrido`, entonces falla nombrando archivo y línea.
**DoD:** `./gradlew testBarrido` PASS; prueba negativa (introducir y revertir) pegada; ADR-046 enlazado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Decisión de adopción del helper: solo operaciones con efecto financiero o irreversible (los 7 comentarios de esqueleto en `grupos/CU59,60,62,63,65,68`, `identidad/CU09` los resuelve Marcelo en su barrido de código muerto según esta decisión) → `ADR-046 Alcance de la idempotencia.md` + enlace en `_Arquitectura.md` | Bóveda verde | `python3 scripts/verificar_boveda.py` | TODO |
| H1.S3.M2 | Regla en `comun-pruebas/Barrido` (o `ReglasPropiasTest`): `clave_idempotencia` solo con otra condición | Negativo demostrado | `./gradlew testBarrido` PASS; evidencia del rojo provocado | TODO |
| H1.S3.M3 | Merge de H1 a `dev` + espejo `test` | Mergeado | `gh pr merge --rebase`; `git push origin origin/dev:test` | TODO |

### H2 — El outbox publica de verdad: bean, lock, cabeceras, tomar-publicar-marcar, backoff, Kafka caído y reinicio

**CA:** Dado una fila `PENDIENTE` en cualquier esquema, cuando pasan ≤ 5 s, entonces está en `aportaya.<tipo>` con las 8 cabeceras y la fila es `PUBLICADO`; con Kafka caído queda `PENDIENTE` con backoff y se publica al volver; ninguna transacción PostgreSQL queda abierta durante la llamada a Kafka; el consumidor de prueba con `Consumidos` no duplica.
**DoD:** `./gradlew :plataforma:comun-mensajeria:integrationTest` PASS (`RelevoConfiguracionTest`, `RelevoTest`, `ConsumidosTest`); `./gradlew :plataforma:comun-mensajeria:e2eTest` PASS (`OutboxE2ETest`, `OutboxResilienciaE2ETest`); `./gradlew integrationTest --tests '*ArranqueTest*'` PASS ×14; kill-test verde; ADR-047.
**Estado:** TODO

#### H2.S1 — `Relevo` existe en cada productor, con scheduling y `LockProvider` (plan H2.S1)

**CA:** Dado cualquier servicio con `aportaya.esquema` y `KafkaTemplate`, cuando arranca, entonces hay bean `Relevo`, `@Scheduled` activo y `LockProvider` sobre `<esquema>.shedlock`; en `webTest`/`test` no se levanta.
**DoD:** `./gradlew :plataforma:comun-mensajeria:integrationTest --tests '*RelevoConfiguracionTest*'` PASS; `ArranqueTest` ×14 PASS; `webTest` raíz PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Test rojo `RelevoConfiguracionTest`: bean `Relevo`, `LockProvider`, `ScheduledAnnotationBeanPostProcessor` presentes | 3 FAIL | comando → FAIL | TODO |
| H2.S1.M2 | `ConfiguracionMensajeria` (`@EnableScheduling`, `@EnableSchedulerLock(defaultLockAtMostFor="PT30S")`, bean `LockProvider` = `JdbcTemplateLockProvider` con tabla `<esquema>.shedlock` — **verificá la API en el README de ShedLock 6.9.0 antes de escribir**), importada desde `ConfiguracionComunWeb` con `@ConditionalOnMissingBean` | 3 PASS | comando | TODO |
| H2.S1.M3 | Bean `Relevo` condicionado a `aportaya.outbox.habilitado` (default `true`) y a `KafkaTemplate` presente; `webTest` sin Kafka sigue verde | `ArranqueTest` ×14 PASS; `webTest` PASS | `./gradlew integrationTest --tests '*ArranqueTest*'`; `./gradlew webTest` | TODO |
| H2.S1.M4 | `@EnableScheduling` duplicado en `cumplimiento/Aplicacion.java:20`: **no lo tocás** (es de otro módulo); anotás en §6 que la configuración común ya lo cubre para que su dueño lo quite | Hallazgo registrado | daily §6 | TODO |
| H2.S1.M5 | Permisos de `svc_*` sobre su `shedlock` (`INSERT/UPDATE/DELETE`): verificar en `sql/00_base/03_permisos.sql`; si falta → generador → **micro-PR al troncal** | Lock adquirido con el rol del servicio | test de integración con `svc_nucleo_financiero` o `psql -U svc_… -c "INSERT INTO nucleo_financiero.shedlock …"` | TODO |

#### H2.S2 — Punta a punta: fila → Kafka → consumidor → `PUBLICADO` (plan H2.S2)

**CA:** Dado una fila escrita por el emisor de prueba, cuando pasan ≤ 5 s, entonces el consumidor de prueba recibe el mensaje con `event_id` = `evento_dominio.id` y las 8 cabeceras, la fila es `PUBLICADO`, y una segunda entrega del mismo `event_id` no repite el efecto.
**DoD:** `./gradlew :plataforma:comun-mensajeria:e2eTest --tests '*OutboxE2ETest*'` PASS con salida.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | `docs/auditoria-produccion/contratos/evento-kafka.md` (cabeceras, tema `aportaya.<tipo>`, clave de partición = `agregado_id`) **antes** de codificar | Archivo existe | `test -f docs/auditoria-produccion/contratos/evento-kafka.md` | TODO |
| H2.S2.M2 | Fixture Kafka en `comun-pruebas`: `BaseDePrueba.kafka()` singleton con `org.testcontainers.kafka.KafkaContainer` e imagen `apache/kafka:<versión fijada>` — **verificá el nombre de la clase en la versión del BOM** | Contenedor levanta una vez por JVM | `./gradlew :plataforma:comun-pruebas:test` PASS | TODO |
| H2.S2.M3 | `OutboxE2ETest` en rojo: emisor de prueba escribe la fila (misma forma que `Outbox.emitir`), espera por condición (Awaitility si está en el BOM; si no, polling acotado sin `sleep` fijo) a `PUBLICADO`, consume con `KafkaConsumer` | FAIL por timeout hoy | comando → FAIL | TODO |
| H2.S2.M4 | Cabeceras del envelope desde las columnas/`metadatos` de `evento_dominio` en `Relevo.publicar` (`:76-80`) | Test verifica las 8 | comando → PASS | TODO |
| H2.S2.M5 | Consumidor de prueba (`src/e2eTest`) que aplica `Consumidos.registrar`; entrega doble → 1 efecto; `ConsumidosTest` de integración | PASS | comando + `./gradlew :plataforma:comun-mensajeria:integrationTest --tests '*ConsumidosTest*'` | TODO |

#### H2.S3 — Tomar, publicar fuera de la transacción, marcar; backoff y `FALLIDO` (plan H2.S3)

**CA:** Dado 100 pendientes y Kafka con 2 s de latencia, cuando el relevo corre, entonces `pg_stat_activity` no muestra `idle in transaction` del relevo; ante fallo `intentos++`, `ultimo_error`, `proximo_intento_en` con backoff exponencial + jitter; tras `intentos-maximos` → `FALLIDO` con métrica; `TOMADO` huérfano se recupera; dos relevos no publican dos veces.
**DoD:** `./gradlew :plataforma:comun-mensajeria:integrationTest --tests '*RelevoTest*'` → 6 PASS; consulta de `pg_stat_activity` pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S3.M1 | Columnas `tomado_en`, `tomado_por`, `ultimo_error`, `proximo_intento_en` y estado `TOMADO` en el CHECK de `evento_dominio` de los 14 esquemas; `GRANT UPDATE` ampliado (`03_permisos.sql:139-141` es generado) → generador → **micro-PR al troncal** | `aplicar.sql` en limpio; `verificaciones.sql` sin FALLA | `python3 scripts/generar_ddl.py && psql -f sql/aplicar.sql && psql -f sql/50_verificacion/verificaciones.sql`; PR `troncal(sql): outbox tomado y backoff` mergeado | TODO |
| H2.S3.M2 | `RelevoTest` rojo con los 6 escenarios | 6 FAIL | comando → FAIL | TODO |
| H2.S3.M3 | Refactor de `Relevo.relevar` (`:48-69`): tx1 `UPDATE … SET estado='TOMADO' … WHERE id IN (SELECT … FOR UPDATE SKIP LOCKED)` + commit; `send().get(timeout)` **fuera** de transacción; tx2 marcar `PUBLICADO` o fallo con backoff; sin `@Transactional` en el método externo | 6 PASS | comando → PASS | TODO |
| H2.S3.M4 | Propiedades `aportaya.outbox.*` sin literales en la plantilla de `nuevo_servicio.py`; `SinUmbralLiteral` verde | `testBarrido` PASS | `./gradlew testBarrido` | TODO |
| H2.S3.M5 | Latencia inyectada (Toxiproxy de Testcontainers o `KafkaTemplate` decorado en test) y consulta `SELECT state, query FROM pg_stat_activity WHERE state LIKE 'idle in transaction%'` vacía para el relevo | Consulta vacía | salida pegada en `evidencia/` | TODO |

#### H2.S4 — Kafka caído, reinicio, métricas y ADR (plan H2.S4)

**CA:** Dado Kafka apagado, cuando se emite, entonces commit OK, fila `PENDIENTE`, readiness DOWN, liveness UP; al volver → `PUBLICADO` ≤ backoff máximo; dado un `TOMADO` entre publicar y marcar, al siguiente relevo se republica y el consumidor no duplica; las 4 métricas del outbox se exponen.
**DoD:** `./gradlew :plataforma:comun-mensajeria:e2eTest --tests '*OutboxResilienciaE2ETest*'` → 3 PASS; `curl … \| grep aportaya_outbox` → 4 líneas; ADR-047.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S4.M1 | Escenario Kafka caído (`kafka.stop()`): 4 aserciones | PASS | comando | TODO |
| H2.S4.M2 | Escenario Kafka vuelve (`kafka.start()`) | PASS | comando | TODO |
| H2.S4.M3 | Escenario reinicio (`TOMADO` huérfano publicado a mano) → republica; `Consumidos` → 1 efecto | PASS | comando | TODO |
| H2.S4.M4 | Métricas `aportaya.outbox.{pendientes, fallidos, publicaciones_total{resultado}, edad_mas_viejo_segundos}` | 4 líneas | `curl -s localhost:8080/actuator/prometheus \| grep aportaya_outbox` (servicio en compose) | TODO |
| H2.S4.M5 | `ADR-047 Semántica de entrega del outbox.md` + actualización de ADR-018/027 con enlace; `carriles/PR3-plataforma.md` §H2; merge + espejo | Bóveda verde; mergeado | `python3 scripts/verificar_boveda.py`; `gh pr merge --rebase`; `git push origin origin/dev:test` | TODO |

### H3 — Guardas comunes: decodificador con `iss`/`aud`, guarda de producción, perfiles por plantilla, errores unificados

**CA:** Dado un token con `iss`/`aud` malos, firma ajena, vencido, sin `kid` o fuera de skew, entonces `401` en todo servicio; dado perfil ∉ {local,test} con placeholder, CORS `*`, doble de desarrollo o URL `http://` de proveedor, entonces el arranque falla nombrando la propiedad; los 14 `application-*.yml` salen de la misma plantilla; todo error tiene `codigo, mensaje, correlationId, timestamp`.
**DoD:** `./gradlew :plataforma:comun-web:integrationTest --tests '*DecodificadorTest*'` → 6 PASS; `./gradlew :plataforma:comun-web:test --tests '*GuardiaDeProduccionTest*'` → 7 PASS; `./gradlew :plataforma:comun-web:webTest` PASS; `python3 scripts/nuevo_servicio.py --check` (o equivalente) sin diff.
**Estado:** TODO

#### H3.S1 — Decodificador común con validadores (plan H5.S2.M1/M3)

**CA:** Dado `NimbusJwtDecoder.withJwkSetUri(...)` (`ConfiguracionDelDecodificador.java:27-28`), cuando se construye, entonces lleva `JwtValidators.createDefaultWithIssuer`, validador de `aud` y `JwtTimestampValidator(tolerancia)`.
**DoD:** 6 casos PASS; `ArranqueTest` ×14 PASS con las propiedades nuevas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | `DecodificadorTest` rojo (JWKS servido por `HttpServer` del JDK): iss malo, aud malo, vencido, firma ajena, sin `kid`, skew | 6 FAIL | comando → FAIL | TODO |
| H3.S1.M2 | Validadores + propiedades `aportaya.jwt.{emisor, audiencia, tolerancia}` (defaults `aportaya-identidad`, `["aportaya"]`, `PT60S`) en la plantilla | 6 PASS; ×14 arrancan | comando; `./gradlew integrationTest --tests '*ArranqueTest*'` | TODO |

#### H3.S2 — `GuardiaDeProduccion` (plan H5.S5.M1/M2/M4)

**CA:** Dado `aportaya.entorno.productivo=true` (derivado del perfil), cuando falta clave de firma (identidad), pimienta o es placeholder (`pimienta-de-prueba`, `cambiar`, `example`), `BD_URL`/`KAFKA_URL`, CORS `*`, `aportaya.mfa.doble-local=true` o URL de proveedor sin `https://`, entonces `ApplicationContext` falla con mensaje que nombra la propiedad; en `local`/`test` no interviene.
**DoD:** `./gradlew :plataforma:comun-web:test --tests '*GuardiaDeProduccionTest*'` → 7 PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Tests rojos (7, `ApplicationContextRunner`) | 7 FAIL | comando | TODO |
| H3.S2.M2 | `GuardiaDeProduccion` (`SmartInitializingSingleton`) con lista de placeholders configurable; registrada en `ConfiguracionComunWeb` | 7 PASS | comando | TODO |
| H3.S2.M3 | `docs/Arquitectura/Entornos y despliegue.md`: tabla variable → obligatoria en qué perfil | Bóveda verde | `python3 scripts/verificar_boveda.py` | TODO |

#### H3.S3 — Plantilla de perfiles y formato de error (plan H5.S5.M3 plantilla, H7.S5.M3)

**CA:** Dado `scripts/nuevo_servicio.py`, cuando genera un servicio, entonces produce `application-{local,test,staging,production}.yml` con las propiedades comunes; dado un error, la respuesta es `{codigo, mensaje, correlationId, timestamp}` sin stacktrace, SQL ni `constraint_name`.
**DoD:** plantilla con los 4 archivos; `./gradlew :plataforma:comun-web:webTest --tests '*ManejadorGlobalDeErroresWebTest*'` PASS con `correlationId` y `timestamp`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | Plantilla en `nuevo_servicio.py` con los 4 perfiles y las propiedades comunes de la tabla de contratos; **mergeala primero** (micro-PR `troncal(plantilla): perfiles por entorno`) para que Richard, Justin y Marcelo la usen; los dueños aplican a sus servicios, vos no | PR mergeado en la primera hora del turno | `gh pr view --json mergedAt` | TODO |
| H3.S3.M2 | `ManejadorGlobalDeErrores`: `correlationId` (de `Traza`) y `timestamp` en todo error; `TraduccionDeRestricciones` no expone `constraint_name` ni nombres de tabla | webTest PASS | comando | TODO |

### H4 — Lo que todos heredan: barridos de dinero y logs, `Dinero` probado, logs JSON, probes, ArchUnit compartido

**CA:** Dado el repo, cuando corre `testBarrido`, entonces falla ante `double/float` en dinero, `divide(` sin `RoundingMode`, `BITACORA` con valores sensibles y `.tag("usuario"|"cuenta"|"id")` en métricas; `Dinero` rechaza moneda distinta y negativo; los logs son JSON con 7 campos en perfiles ≠ local; readiness incluye db+kafka y liveness no; las reglas ArchUnit del §55 corren en los 14.
**DoD:** `./gradlew testBarrido` PASS con pruebas negativas pegadas; `./gradlew :plataforma:comun-dominio:test --tests '*DineroTest*'` PASS; `LogsEstructuradosTest`, `ProbesTest`, `TrazaPropagadaE2ETest` PASS; `./gradlew test --tests '*ArquitecturaTest*'` PASS ×14.
**Estado:** TODO

#### H4.S1 — Barridos y `Dinero` (plan H8.S1.M2/M3, H9.S1.M3, H9.S2.M3)

**CA:** Dado las cuatro reglas nuevas en `comun-pruebas/Barrido`, cuando se introduce cada violación en un archivo temporal, entonces `testBarrido` la nombra.
**DoD:** 4 pruebas negativas pegadas; `DineroTest` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Regla dinero: `double|float|Double|Float` en tipos con `monto|saldo|importe|comision|tarifa|aporte|retiro|transferencia|Dinero`, y `divide(` sin `RoundingMode` | Negativo demostrado | `./gradlew testBarrido` + evidencia del rojo | TODO |
| H4.S1.M2 | Regla logs: ningún `BITACORA.*` con `cuerpo`, `payload`, `factor`, `token`, `documento`, `cuenta_bancaria` como valor | Negativo demostrado | ídem | TODO |
| H4.S1.M3 | Regla métricas: sin `.tag("usuario"|"cuenta"|"id", …)` | Negativo demostrado | ídem | TODO |
| H4.S1.M4 | `DineroTest` en `comun-dominio`: escala 2, moneda distinta → error, negativo → error, cero, JSON como string, compatible `NUMERIC(16,2)` | PASS | `./gradlew :plataforma:comun-dominio:test --tests '*DineroTest*'` | TODO |

#### H4.S2 — Logs JSON, traza de punta a punta y probes (plan H9.S2.M1/M2, H9.S3)

**CA:** Dado perfil ≠ local, cuando se loguea, entonces JSON con `timestamp, level, service, traceId, correlationId, event, message`; dado una operación, el `correlationId` cruza HTTP → outbox → cabecera Kafka → consumidor de prueba; con Kafka o PostgreSQL apagados, liveness UP y readiness DOWN, sin `500` con stacktrace, y el pool se reconecta.
**DoD:** `LogsEstructuradosTest` PASS + línea pegada; `./gradlew :plataforma:comun-mensajeria:e2eTest --tests '*TrazaPropagadaE2ETest*' --tests '*ProbesE2ETest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | `logging.structured.format.console=ecs` en la plantilla para perfiles ≠ local (**verificá la propiedad en la doc de Spring Boot 3.5.6**); MDC de `Traza` con `service`, `traceId`, `correlationId`, `event` | Log JSON con 7 campos | `LogsEstructuradosTest` PASS + línea pegada (sin datos de persona) | TODO |
| H4.S2.M2 | `TrazaPropagadaE2ETest`: HTTP (`ControladorDeEnsayo`) → outbox → Kafka (cabeceras) → consumidor de prueba restaura el MDC; mismo id en los 4 saltos | PASS | comando | TODO |
| H4.S2.M3 | `ProbesTest`: `management.endpoint.health.group.readiness.include=db,kafka` en la plantilla; liveness sin ambos | PASS | `./gradlew :plataforma:comun-web:integrationTest --tests '*ProbesTest*'` | TODO |
| H4.S2.M4 | `ProbesE2ETest`: Kafka apagado → liveness UP / readiness DOWN; PostgreSQL apagado → `503` controlado, readiness DOWN, reconexión del pool al volver, sin loop agresivo (intentos/min acotados en el log) | PASS + conteo | comando | TODO |

#### H4.S3 — ArchUnit compartido y cierre (plan H11.S1)

**CA:** Dado `ReglasDeArquitectura` en `comun-pruebas`, cuando un servicio la usa en su `ArquitecturaTest`, entonces falla ante controller → repositorio, dominio → Spring/jOOQ, ciclos, `bo.aportaya.<otro>.{aplicacion,infraestructura}` importado, y JPA.
**DoD:** `./gradlew test --tests '*ArquitecturaTest*'` PASS ×14; negativo demostrado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S3.M1 | Leer `nucleo-financiero/ArquitecturaTest` y `comun-pruebas`; tabla de cobertura vs plan §H11.S1 en `carriles/PR3-plataforma.md` | Tabla | revisión | TODO |
| H4.S3.M2 | `ReglasDeArquitectura` compartida con las reglas faltantes; los 14 `ArquitecturaTest` la invocan (si un servicio tiene uno propio, la suma se hace con un `@Import` o método estático: **no editás el suyo**, anotás en §6 la línea que tiene que agregar) | ×14 PASS o hallazgo por servicio | comando | TODO |
| H4.S3.M3 | `carriles/PR3-plataforma.md` completo (6 campos por hito), regresión de `plataforma/*`, merge final + espejo `test` | Verde y mergeado | comandos del ritual | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 (= AMB-10) | No existe ningún consumidor Kafka productivo | Pablo | Nada | **DECIDIDA (2026-09-21)**: consumidor Kafka **de prueba** en `comun-mensajeria/src/e2eTest`; ningún consumidor productivo este turno; contrato del envelope ya en `dev`: `docs/auditoria-produccion/contratos/evento-kafka.md` |
| Q-02 | `intentos-maximos` y backoff del outbox (valores) | Pablo · operación | Nada | **DECIDIDA (2026-09-21)**: `intentos-maximos=10`, `backoff-base=PT1S`, `backoff-tope=PT5M`, jitter ±20 %, `timeout-publicacion=PT10S`; todos en configuración, ninguno literal en código |
| Q-03 | `FALLIDO` = DLQ lógica en la misma tabla vs tema `aportaya.dlq` | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: `FALLIDO` es la DLQ lógica en la misma tabla `evento_dominio` + métrica `aportaya.outbox.fallidos` + runbook `outbox-backlog.md`; sin tema `aportaya.dlq` este turno |
| Q-04 (= AMB-12) | Perfiles y `aportaya.entorno.productivo` | Pablo | Nada | **DECIDIDA (2026-09-21)**: perfiles `local`, `test`, `staging`, `production`; `aportaya.entorno.productivo = true` para todo perfil que no sea `local`/`test` (fail closed) |
| Q-05 | `aud` global vs por servicio | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: token de acceso `aud=["aportaya"]` (global); evidencia step-up `aud=["aportaya-nucleo-financiero"]`; `iss=aportaya-identidad` en ambos |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` solo
      por `DECISION_REQUIRED`.
- [ ] `carriles/PR3-plataforma.md` y tu daily con el avance calculado en la primera línea.
- [ ] Evidencia literal en `evidencia/`: kill-test del outbox en verde, consulta de
      `pg_stat_activity` vacía, salida de Kafka caído/vuelto, pruebas negativas de cada barrido.
- [ ] Gates: `evidence-and-verification` siempre; `microservices-testing` en H2 (broker apagado
      de verdad, no mockeado); `security-guardrails` en H3; `data-privacy-financial` en H4.S1/S2.
- [ ] `ArranqueTest` de los 14 servicios en verde después de cada merge tuyo.
- [ ] Todo mergeado en `dev` y espejado en `test`; la plantilla de perfiles mergeada en la
      primera hora.
- [ ] Peldaño de evidencia declarado por hito (regla 30).
