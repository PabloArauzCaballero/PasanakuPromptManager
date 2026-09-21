# Núcleo financiero: la clave de idempotencia con el scope del índice, el retiro que exige evidencia MFA real y la doble aprobación que la aplicación hace cumplir

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Justin · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio(s):** `nucleo-financiero`
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Justin-Daily-Noche-2026-09-21.md](../Justin-Daily-Noche-2026-09-21.md)
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (este encargo cubre H1.S2, H1.S3, H1.S5.M1/M4, H3.S1, H3.S3.M2–M5, H3.S4, H4 completo, H8.S1.M4, H9.S4.M1–M3/M5 y la parte de `nucleo-financiero` de H7.S2, H9.S1, H10.S1.M3, H0)
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `justin/feature/carril-PR2-nucleo-financiero`
- **4 hitos · 13 subtareas · 42 microtareas** — es el carril más largo y la ruta crítica del dinero: lo que no cierre va `A MEDIAS` con las cuatro respuestas, nunca disfrazado

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar (este repo) dentro de `PasanakuBackend/`. El backend trae sus propias skills (`dinero-decimal`, `idempotencia-reintentos`, `frontera-transaccional`, `desembolsos-payouts`…): **se suman, no se reemplazan**.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `money-movement-safety` | Retención antes del pago, idempotencia, nada se promete antes de estar cobrado |
| `concurrency-and-locking` | Precondición en el `UPDATE`, carreras de aprobadores, 50 reintentos con la misma clave |
| `state-machines-workflows` | La máquina de estados del retiro con los estados que ya existen en el CHECK |
| `authz-access-control` | `RETIRO_APROBAR`, segregación solicitante ≠ aprobador, propiedad del recurso |
| `disbursement-payouts` | Estados del retiro con proveedor, timeout ≠ fallo, reconciliación |
| `resilience-patterns` | Timeouts, retry solo idempotente, cortacircuito en el cotizador y el proveedor |
| `accounting-double-entry` | El pago del retiro asienta débito/crédito; el rechazo no ensucia el libro |
| `test-case-design-techniques` | Válido · límite (umbral exacto) · error, y los tres niveles de cada doble |
| `data-privacy-financial` | Ni evidencia MFA, ni cuentas, ni importes atribuibles en logs y salidas |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre del turno con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 65 · 90 · **91** · 96 · 98

## 2. Resultado observable

Un titular que reintenta un retiro con la misma `Idempotency-Key` recibe la misma orden, y otro titular con esa misma clave recibe la suya (no la ajena); un retiro sin evidencia step-up válida de `identidad` no crea orden; un retiro de monto ≥ umbral queda `EN_REVISION` y solo un usuario con `RETIRO_APROBAR` **distinto del solicitante** lo pasa a `AUTORIZADA`; dos aprobadores simultáneos producen una sola transición; `nucleo-financiero` con perfil `production` no arranca con el adaptador de MFA de desarrollo.

**Kill-test:** con dos billeteras A y B, mandar `POST /billetera/retiros` con la misma `Idempotency-Key` desde A y desde B. Si B recibe `ordenRetiroId` de A, esto NO está hecho.

## 3. Alcance

**IN:** `servicios/nucleo-financiero/**` (contrato, aplicación, dominio, infraestructura, tests, `application*.yml`), `docs/operacion/provider-timeout.md`, `docs/operacion/withdrawal-reconciliation.md`, `docs/Arquitectura/ADR-049 Doble aprobación de retiros.md`, `docs/auditoria-produccion/carriles/PR2-nucleo-financiero.md`, y **dos micro-PR al troncal**: la tabla `nucleo_financiero.evidencia_mfa_consumida` (generador) y el permiso `RETIRO_APROBAR` (`sql/60_semillas/10-roles-y-permisos.sql` o su generador).

**OUT:** `identidad` (Richard emite la evidencia; vos la verificás con un doble hasta que su PR esté en `dev`). `plataforma/comun-web` y `comun-mensajeria` (Leo: helper `Idempotencia`, decodificador, `Relevo`). Los tests transversales de Marcelo (`LibroInvariantesTest`, `LibroBenchmarkTest`, `AppendOnlyTest` viven en tu módulo pero **son de él**: no los edites). `.github/workflows` (Pablo). Frontends: el contrato cambia (`evidenciaMfa`, endpoint de aprobación) con compatibilidad hacia atrás; los clientes se regeneran, las apps no se tocan.

**Reservas de archivos:** todo `servicios/nucleo-financiero/**` **salvo** los tres archivos de test de Marcelo nombrados arriba; los dos runbooks; `ADR-049*`; `carriles/PR2-nucleo-financiero.md`; en `sql/` solo lo de tus dos micro-PR.

### Ritual de entrega — `dev` y `test`, sin esperar a nadie

```bash
git fetch origin && git checkout -b justin/feature/carril-PR2-nucleo-financiero origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply :servicios:nucleo-financiero:webTest :servicios:nucleo-financiero:integrationTest spotlessCheck
git push -u origin HEAD
gh pr create --base dev --fill --title "fix(wallet): <subtarea>"
gh pr merge --rebase
git fetch origin && git push origin origin/dev:test   # test es espejo de dev (AMB-R1)
```

- **Micro-PR al troncal** (`sql/` vía generador, seeds, `libs.versions.toml`, `buildSrc/`): un commit solo con eso, título `troncal(<que>): …`, mergeado a `dev` dentro de la hora; después rebaseás.
- **Jamás te detenés.** Contrato ajeno que no está en `dev` → doble en **tres niveles** bajo `@Profile({"local","test"})` o en `src/test`, cerrás contra el doble declarándolo, y dejás la microtarea de integración diferida. Solo una decisión de negocio queda abierta.
- CI rojo por job ajeno (Spotless de `dev` hasta que Pablo lo cierre) → hallazgo en tu daily §6, **no te detiene**. Tu gate local en verde es la condición de merge.
- Un test tuyo en rojo te detiene **esa** microtarea. Nunca `skip`, nunca `@Disabled`, nunca borrar una constraint para que pase.

### Contrato fijado con Richard — el JWT de evidencia step-up (idéntico al de su encargo)

`RS256` con el `kid` del JWKS de identidad · `iss=aportaya-identidad` · `aud=["aportaya-nucleo-financiero"]` · `sub`=usuario · `jti` UUID de **un solo uso** · `exp − iat ≤ PT5M` · `proposito ∈ {RETIRO, CAMBIO_CUENTA, ADMIN}` · `desafio_id` · `acr=mfa` · `amr`. Está escrito en `docs/auditoria-produccion/contratos/step-up-jwt.md` (lo escribe Richard en su H1.S2.M1; si todavía no está en `dev` cuando arrancás, usás esta línea y lo anotás).

**Tu doble (H2.S2.M1):** en `src/test`, una `RSAKey` de prueba, un JWKS servido por `HttpServer` del JDK o `MockWebServer` en `aportaya.jwt.jwks-uri`, y un `EmisorDeEvidenciaDePrueba` con los tres niveles: **correcto** (todos los claims), **límite** (`exp` = ahora + 1 s → acepta; `exp` = ahora − 1 s → rechaza; `jti` presentado dos veces → segunda rechaza), **inválido** (otra clave, otro `sub`, `proposito=ADMIN`, `aud` distinto, sin `acr`). Con eso cerrás H2 entero sin Richard. La integración real es H2.S4.M2.

## 4. Plan

### H1 — La idempotencia del núcleo tiene exactamente el scope de su índice único

**CA:** Dado dos titulares con la misma clave, cuando cada uno transfiere, retira o recarga, entonces cada uno obtiene su propia transacción/orden; dado el mismo titular reintentando, obtiene la misma; dado 50 reintentos simultáneos de una transferencia, hay exactamente una transacción nueva.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU10*' --tests '*CU11Test*' --tests '*CU12*'` PASS con los casos nuevos; `CU12ConcurrenciaTest` PASS con conteos pegados.
**Estado:** TODO

#### H1.S1 — Ledger: `porClaveIdempotencia` con la identidad de `uq_tx_idem` (plan H1.S2)

**CA:** Dado `uq_tx_idem (COALESCE(iniciada_por,…), origen_tipo, clave)`, cuando U1 y U2 transfieren con la clave K, entonces hay dos transacciones y cada uno recibe la suya.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU12Test*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Test rojo en `CU12Test`: misma clave, dos `ContextoSesion` → dos `transaccionId` distintos | 1 FAIL hoy (devuelve la de U1) | comando → 1 FAIL | TODO |
| H1.S1.M2 | `LibroDeBilletera.porClaveIdempotencia(dsl, iniciadaPor, origenTipo, clave)` con el mismo `COALESCE` del índice (`restricciones.sql:236-238`); adaptar `CU12TransferirSaldo:72` y `CU14ReversarTransaccion` | PASS | comando → PASS | TODO |
| H1.S1.M3 | Test de replay legítimo: mismo titular, misma clave → misma `transaccionId`, saldo sin cambio | PASS | comando | TODO |

#### H1.S2 — Retiro y recarga: lookup por `(cuenta_billetera_id, clave)` (plan H1.S3)

**CA:** Dado una orden de A con clave K, cuando B pide con K, entonces orden nueva para B; el replay de A devuelve el costo **almacenado**, no el recotizado.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11Test*' --tests '*CU10Test*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Tests rojos en `CU11Test` y `CU10Test`: misma clave/otra cuenta → distinta; misma clave/misma cuenta → misma | 2 FAIL hoy | comando → 2 FAIL | TODO |
| H1.S2.M2 | `OrdenRetiroRepositorio.porClaveIdempotencia(dsl, cuentaId, clave)` (`:87-92`) y `OrdenRecargaRepositorio` (`:70-75`); adaptar `CU11:85`, `CU10:82` | PASS | comando → PASS | TODO |
| H1.S2.M3 | Replay de retiro devuelve `costo_retiro`/`monto_neto` de la orden (`CU11:88-93` hoy devuelve `entrada.costo()`) | Test con costo distinto en la entrada → costo original | comando | TODO |

#### H1.S3 — 50 reintentos simultáneos, un solo efecto (plan H1.S5.M1/M4)

**CA:** Dado 50 hilos con la misma clave sobre `CU12`, cuando terminan, entonces 1 `transaccion_billetera` nueva, suma de saldos preservada, y los demás obtienen la misma salida o `409`.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU12ConcurrenciaTest*'` PASS con conteos.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S3.M1 | `CU12ConcurrenciaTest` (patrón `CU10ConcurrenciaTest`): 50 hilos, misma clave, misma cuenta | 1 transacción; suma preservada | comando → PASS + conteos pegados | TODO |
| H1.S3.M2 | Regresión del módulo y merge de H1 a `dev` + espejo `test` | Verde y mergeado | `./gradlew :servicios:nucleo-financiero:webTest :servicios:nucleo-financiero:integrationTest spotlessCheck` → exit 0; `gh pr merge --rebase` | TODO |

### H2 — Retirar exige evidencia step-up real; el adaptador de desarrollo no existe en producción

**CA:** Dado un retiro sin evidencia, con evidencia inválida, vencida, de otro usuario, de otro propósito o ya consumida, entonces `MFA_REQUERIDO`/`MFA_INVALIDO` y ninguna orden; con evidencia válida → orden con `mfa_verificado=true`; con perfil `production` y sin adaptador real → el proceso no arranca.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*SegundoFactorStepUpTest*' --tests '*ArranqueProduccionTest*'` PASS (9 tests); `./gradlew :servicios:nucleo-financiero:webTest` PASS; `verificar_seguridad.py` exit 0.
**Estado:** TODO

#### H2.S1 — Confinar `SegundoFactorLocal` a `local`/`test` (plan H3.S1)

**CA:** Dado perfil `production`, cuando arranca sin un `SegundoFactor` real, entonces falla nombrando el bean; con `local`, el adaptador local deniega salvo `aportaya.mfa.doble-local=true`, propiedad que **no tiene efecto** fuera de `local/test`.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*Arranque*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | `application-{local,test,staging,production}.yml` de `nucleo-financiero` (misma forma que la plantilla de Leo si ya está en `dev`; si no, a mano y lo anotás); `ArranqueTest` activa `test` | `ArranqueTest` PASS | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*ArranqueTest*'` | TODO |
| H2.S1.M2 | `@Profile({"local","test"})` en `SegundoFactorLocal` (patrón `identidad/infraestructura/DesafioDeDesarrollo.java:32`); `ArranqueProduccionTest` (`@ActiveProfiles("production")`) falla por bean ausente **hasta** H2.S2 | 1 FAIL esperado | comando → FAIL `NoSuchBeanDefinitionException: SegundoFactor` | TODO |
| H2.S1.M3 | Reemplazar `aportaya.mfa.exigido` por `aportaya.mfa.doble-local` leída solo bajo `local/test`; test de que en `production` no tiene efecto | PASS | `./gradlew :servicios:nucleo-financiero:webTest --tests '*BilleteraControllerWebTest*'` | TODO |

#### H2.S2 — `SegundoFactorStepUp`: validación local de la evidencia con consumo del `jti` (plan H3.S3.M2–M5)

**CA:** Dado la evidencia del contrato, cuando llega a `solicitarRetiro`, entonces se valida firma (JWKS), `iss`, `aud`, `sub`=sesión, `proposito=RETIRO`, `acr=mfa`, vigencia, y el `jti` se consume **dentro** de la transacción del CU-11 (revierte con la orden).
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*SegundoFactorStepUpTest*'` → 7 PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | **Doble de Richard en `src/test`** (ver §3): clave RSA de prueba, JWKS servido, `EmisorDeEvidenciaDePrueba` con los tres niveles | Doble emite los 3 niveles | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*EmisorDeEvidenciaDePruebaTest*'` PASS | TODO |
| H2.S2.M2 | Tabla `nucleo_financiero.evidencia_mfa_consumida (jti PK, usuario_id, proposito, consumida_en)` en `scripts/modelo.py`/`.puml` → `generar_ddl.py`; `GRANT INSERT` a `svc_nucleo_financiero`, sin `UPDATE/DELETE` → **micro-PR al troncal** | `aplicar.sql` en limpio; permisos verdes | `python3 scripts/generar_ddl.py && python3 scripts/verificar_boveda.py`; `psql -f sql/50_verificacion/verificaciones.sql` sin FALLA; PR `troncal(sql): evidencia mfa consumida` mergeado | TODO |
| H2.S2.M3 | Tests rojos `SegundoFactorStepUpTest` (7): sin evidencia; firma ajena; vencida; otro `sub`; otro `proposito`; `jti` ya consumido; válida | 7 FAIL | comando → 7 FAIL | TODO |
| H2.S2.M4 | `SegundoFactorStepUp implements SegundoFactor` usando `JwtDecoder` común + validadores propios de `aud`/`proposito`/`acr`; consumo del `jti` con `INSERT … ON CONFLICT DO NOTHING` (patrón `Consumidos`) dentro de `datos.conContexto`; activo salvo `local/test` con doble | 7 PASS | comando → PASS | TODO |
| H2.S2.M5 | Contrato: `EntradaRetiro.factorMfa` → `evidenciaMfa` aceptando ambos hasta `2026-12-31` (compatibilidad, §63); regenerar clientes; códigos `MFA_REQUERIDO` (ya `CodigoError.de(11,2)`) y `MFA_INVALIDO` nuevo en el catálogo | Clientes generan; `erroresCatalogo` PASS | `./gradlew generateOpenApiClients --no-parallel --no-build-cache && ./gradlew erroresCatalogo` | TODO |

#### H2.S3 — Arranque de producción y E2E del retiro con evidencia (plan H3.S4.M1/M2)

**CA:** Dado perfil `production` con `SegundoFactorStepUp`, cuando arranca, entonces levanta; con `doble-local=true` en `production` → no levanta; dado el stack de compose, el retiro completo con evidencia del doble (o de Richard si ya está) → `201` con `mfa_verificado=true`.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*ArranqueProduccionTest*'` → 2 PASS; `./gradlew :servicios:nucleo-financiero:e2eTest --tests '*RetiroConMfaE2ETest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S3.M1 | `ArranqueProduccionTest` 2 casos | 2 PASS | comando | TODO |
| H2.S3.M2 | `RetiroConMfaE2ETest` sobre `compose --profile todo` con la evidencia del doble (JWKS de prueba) | PASS | comando | TODO |

#### H2.S4 — Integración diferida con `identidad` y cierre

**CA:** Dado el PR de Richard en `dev`, cuando se reemplaza el JWKS de prueba por el real de `identidad`, entonces `RetiroConMfaE2ETest` sigue verde; si Richard no llegó, el hito cierra contra el doble **declarado**.
**DoD:** salida del E2E con JWKS real, o línea en el daily: "cerrado contra doble; integración real pendiente de PR1".
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S4.M1 | `docs/auditoria-produccion/carriles/PR2-nucleo-financiero.md` §H2: problema · causa raíz · solución · test · evidencia · riesgo residual; `docs/Seguridad.md` con el control y su comando | 6 campos | `python3 scripts/verificar_seguridad.py` exit 0 | TODO |
| H2.S4.M2 | Integración real: `git fetch && git rebase origin/dev`; si `identidad` ya emite evidencia, correr el E2E contra el stack real; si no, declarar el doble y dejar esta fila `A MEDIAS` con "qué falta: PR1 en dev" | E2E real PASS o `A MEDIAS` declarada | comando E2E o daily §4 | TODO |

### H3 — La doble aprobación la hace cumplir la aplicación, no solo el CHECK de la base

**CA:** Dado monto ≥ `aportaya.retiro.doble-aprobacion-desde`, cuando se crea, entonces `EN_REVISION`; solicitante que se aprueba → `RETIRO_AUTOAPROBACION_PROHIBIDA`; sin `RETIRO_APROBAR` → `403`; aprobador distinto → `AUTORIZADA` con `aprobada_por`; dos aprobadores a la vez → una transición; pagar sin `AUTORIZADA` → `RETIRO_APROBACION_REQUERIDA`; monto < umbral → `AUTORIZADA` automática (AMB-5).
**DoD:** `./gradlew :servicios:nucleo-financiero:test --tests '*EstadoDeRetiroTest*'` PASS; `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11*'` PASS (≥ 20 tests); `./gradlew :servicios:nucleo-financiero:webTest` PASS; ADR-049.
**Estado:** TODO

#### H3.S1 — Máquina de estados explícita con los estados del CHECK (plan H4.S1)

**CA:** Dado `EstadoDeRetiro`, cuando se intenta una transición fuera de `PENDIENTE→{EN_REVISION,AUTORIZADA,RECHAZADA}`, `EN_REVISION→{AUTORIZADA,RECHAZADA}`, `AUTORIZADA→{EN_PROCESO,RECHAZADA}`, `EN_PROCESO→{PAGADA,RECHAZADA}`, `PAGADA→REVERSADA`, entonces error de dominio.
**DoD:** `./gradlew :servicios:nucleo-financiero:test --tests '*EstadoDeRetiroTest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | `EstadoDeRetiro` (dominio, sin Spring) con `puedePasarA` y test de toda la tabla, válidas e inválidas | PASS | comando | TODO |
| H3.S1.M2 | `CU11.solicitar`: `EN_REVISION` si `requiereDobleAprobacion`, si no `AUTORIZADA`; `SalidaRetiro.estado` lo refleja; tests umbral−0.01 / umbral exacto / umbral+1 | 3 PASS | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11Test*'` | TODO |
| H3.S1.M3 | `confirmarPago` exige `EN_PROCESO` (precondición en el `UPDATE`, `OrdenRetiroRepositorio.pasarA`); pagar `EN_REVISION` → `RETIRO_APROBACION_REQUERIDA` (y la base además rechaza por `ck_retiro_doble_aprobacion`) | PASS | mismo comando | TODO |

#### H3.S2 — Permiso, contrato y caso de uso de aprobación (plan H4.S2)

**CA:** Dado `POST /billetera/retiros/{ordenId}/aprobacion {desenlace: AUTORIZADA|RECHAZADA, motivo?}` con `Idempotency-Key`, cuando lo llama alguien con `RETIRO_APROBAR` distinto del solicitante, entonces transiciona, audita y emite `retiro_autorizado`/`retiro_rechazado`; solicitante → `409`; sin permiso → `403`; inexistente → `404`; ya resuelta → `409`.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11AprobacionTest*'` → 8 PASS; `./gradlew :servicios:nucleo-financiero:webTest --tests '*BilleteraControllerWebTest*'` → 5 casos nuevos PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Permiso `RETIRO_APROBAR` en `sql/60_semillas/10-roles-y-permisos.sql` (o su generador) asignado a un rol de backoffice existente (localizarlo en el seed; **nunca** a `PARTICIPANTE`/`ORGANIZADOR`) → **micro-PR al troncal**; seed ×2 idéntico | 2.ª corrida no inserta | `psql -f sql/60_semillas/sembrar.sql` ×2 → mismo conteo; PR `troncal(seeds): permiso RETIRO_APROBAR` mergeado | TODO |
| H3.S2.M2 | Contrato: ruta, `EntradaAprobacionRetiro`, `SalidaAprobacionRetiro{ordenRetiroId, estado, aprobadaPor}`, 401/403/404/409, ejemplo, `Idempotency-Key` | Clientes generan | `./gradlew generateOpenApiClients --no-parallel --no-build-cache` | TODO |
| H3.S2.M3 | Tests rojos `CU11AprobacionTest` (8): aprueba; rechaza; auto-aprobación; sin permiso (en el CU, además del controller); inexistente; ya resuelta; reintento idempotente; auditoría/outbox | 8 FAIL | comando → 8 FAIL | TODO |
| H3.S2.M4 | `CU11.aprobar` / `CU11.rechazarRevision`: bloqueo de la orden, `aprobador != solicitada_por`, `UPDATE … WHERE estado='EN_REVISION'`, outbox, bitácora con actor/target/correlación | 8 PASS | comando → PASS | TODO |
| H3.S2.M5 | Controller con `@Permiso("RETIRO_APROBAR")`, `SabanaDeSeguridadWeb`, `BilleteraControllerWebTest` (201, 403, 401, 409, 400 sin clave); códigos `RETIRO_APROBACION_REQUERIDA`, `RETIRO_AUTOAPROBACION_PROHIBIDA` en el catálogo | 5 PASS; `erroresCatalogo` PASS | `./gradlew :servicios:nucleo-financiero:webTest && ./gradlew erroresCatalogo` | TODO |

#### H3.S3 — Carreras y fallo del proveedor tras autorizar (plan H4.S3)

**CA:** Dado dos aprobadores simultáneos → uno `AUTORIZADA`, otro `409`; approve/reject concurrentes → uno gana; reintento del mismo aprobador → misma respuesta; proveedor (doble) falla tras `AUTORIZADA` → `RECHAZADA`, retención liberada, cero filas en `movimiento_billetera`.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11AprobacionConcurrenciaTest*'` → 4 PASS con conteos.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | Escenarios 1–3 (race, approve/reject, reintento) | 3 PASS | comando | TODO |
| H3.S3.M2 | Escenario 4 con el doble de proveedor de H4.S2 (o un stub local si todavía no lo escribiste: lo hacés acá y lo reusás) | PASS + `SELECT count(*) FROM movimiento_billetera WHERE transaccion_id IN (…)` = 0 | comando + consulta pegada | TODO |
| H3.S3.M3 | `ADR-049 Doble aprobación de retiros.md` + enlace en `_Arquitectura.md` + `docs/Seguridad.md`; regresión del módulo; merge a `dev` + espejo `test` | Bóveda verde; mergeado | `python3 scripts/verificar_boveda.py`; `./gradlew :servicios:nucleo-financiero:webTest :servicios:nucleo-financiero:integrationTest spotlessCheck`; `gh pr merge --rebase` | TODO |
| H3.S3.M4 | `carriles/PR2-nucleo-financiero.md` §H3 (6 campos del §60) | 6 campos | revisión | TODO |

### H4 — El núcleo se puede operar: proveedor con estados, clientes resilientes, propiedad, append-only y métricas

**CA:** Dado el proveedor de retiros que responde timeout, entonces la orden queda `EN_PROCESO` con `referencia_proveedor` y un job de reconciliación la resuelve; dado el cotizador caído, el retiro se rechaza (fail closed) sin transacción abierta; dado usuario A, no ve la billetera de B; `UPDATE` sobre el libro con `svc_nucleo_financiero` falla; las métricas de negocio se exponen.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11ProveedorTest*' --tests '*ClientesResilientesTest*' --tests '*AutorizacionNegativaTest*'` PASS (`AppendOnlyTest` es de Marcelo: no lo corrés vos); `curl … prometheus` con 5 métricas; 2 runbooks.
**Estado:** TODO

#### H4.S1 — Baseline del módulo y `Dinero` en el costo (plan H0.S3.M6 parcial, H8.S1.M4)

**CA:** Dado el SHA base, cuando corren `webTest` e `integrationTest` de `nucleo-financiero`, entonces su veredicto y clasificación de rojos están en `baseline-PR2-nucleo-financiero.md`; el redondeo de `CostoDeOperacion` declara modo y destino del residuo.
**DoD:** archivo de baseline + `./gradlew :servicios:nucleo-financiero:test --tests '*CostoDeOperacionTest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | **Primero de todo el turno:** baseline del módulo (`webTest` + `integrationTest`), rojos clasificados (regla 80.4; la auditoría previa cita CU-12 en rojo: confirmalo) | Archivo con veredicto | `./gradlew :servicios:nucleo-financiero:webTest :servicios:nucleo-financiero:integrationTest; echo exit=$?` pegado | TODO |
| H4.S1.M2 | `CostoDeOperacionTest`: `RoundingMode` explícito, residuo asignado (nunca perdido), moneda obligatoria | PASS | comando | TODO |

#### H4.S2 — Proveedor de retiros: estados, timeout ≠ fallo, reconciliación (plan H9.S4.M1–M3/M5)

**CA:** Dado `AUTORIZADA`, cuando se instruye al proveedor, entonces `EN_PROCESO` con `referencia_proveedor`; respuesta OK → `PAGADA` (asiento débito/crédito); rechazo firme → `RECHAZADA` (retención liberada); timeout → sigue `EN_PROCESO` y el job de reconciliación (ShedLock `nucleo_financiero.reconciliar_retiros`) consulta y resuelve.
**DoD:** `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11ProveedorTest*'` → 3 niveles PASS; ficha del proveedor en `docs/auditoria-produccion/proveedores.md` (sección tuya) y 2 runbooks.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Inventario de clientes salientes del núcleo (`CotizadorPorHttp`, otros `*PorHttp`) y de quién llama hoy a `confirmarPago`/`rechazar` (nadie por HTTP: confirmalo); ficha §75 en `proveedores.md` bajo `## nucleo-financiero` | Tabla | revisión | TODO |
| H4.S2.M2 | Puerto `ProveedorDeRetiro { instruir(orden) → Referencia; consultar(referencia) → Estado }` + **doble en tres niveles** `@Profile({"local","test"})`: acepta / responde tarde (límite: justo antes y justo después del timeout) / rechaza y timeout | Doble con 3 niveles testeado | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*ProveedorDeRetiroDoble*'` PASS | TODO |
| H4.S2.M3 | `CU11.instruirPago` (`AUTORIZADA→EN_PROCESO`, fuera de transacción la llamada), `confirmarPago` (`EN_PROCESO→PAGADA`), `rechazar` (`EN_PROCESO→RECHAZADA`), y `CU11ReconciliarRetiros` programado (`@Scheduled` + `@SchedulerLock("nucleo_financiero.reconciliar_retiros")`) que consulta los `EN_PROCESO` con `referencia_proveedor` | 3 niveles PASS | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11ProveedorTest*'` | TODO |
| H4.S2.M4 | `docs/operacion/provider-timeout.md` y `docs/operacion/withdrawal-reconciliation.md` (7 secciones cada uno) | 14 secciones | `grep -c "^## " docs/operacion/provider-timeout.md docs/operacion/withdrawal-reconciliation.md` | TODO |

#### H4.S3 — Clientes resilientes, propiedad, append-only y métricas (plan H9.S4.M2, H7.S2.M1–M2, H10.S1.M3, H9.S1.M2)

**CA:** Dado `CotizadorPorHttp` y el proveedor, cuando la red falla, entonces timeouts explícitos, retry solo con `Idempotency-Key`, cortacircuito con fallback = denegar; dado A y B, IDOR cubierto en saldo, extracto, retenciones, aprobación; dado el rol del servicio, no puede `UPDATE`/`DELETE` el libro; métricas `wallet_transfer_{success,failure}_total`, `withdrawal_{requested,approved,failed}_total` expuestas.
**DoD:** los 3 tests PASS + `curl … \| grep -E "wallet_|withdrawal_"` → 5 líneas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S3.M1 | resilience4j (ya en el catálogo) en `CotizadorPorHttp` y en el adaptador HTTP del proveedor: `TimeLimiter`/timeouts, `Retry` solo en idempotentes, `CircuitBreaker` con fallback denegar, métricas; `ClientesResilientesTest` (timeout, 500, CB abierto) con `MockWebServer`/`HttpServer` | 3 PASS | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*ClientesResilientesTest*'` | TODO |
| H4.S3.M2 | `AutorizacionNegativaTest` (dos sesiones) sobre `consultarSaldo`, `emitirExtracto`, `cerrarRetencion`, `acreditarRecarga`, `aprobacion`; corregir ownership en los CU | PASS (≥ 6) | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*AutorizacionNegativaTest*'` | TODO |
| H4.S3.M3 | Métricas de negocio desde los CU (sin etiquetas de usuario/cuenta) | 5 líneas en prometheus | `curl -s localhost:8080/actuator/prometheus \| grep -E "wallet_\|withdrawal_"` | TODO |
| H4.S3.M4 | Regresión final del módulo, `carriles/PR2-nucleo-financiero.md` §H4, merge a `dev` + espejo `test` | Verde y mergeado | `./gradlew :servicios:nucleo-financiero:webTest :servicios:nucleo-financiero:integrationTest spotlessCheck`; `gh pr merge --rebase`; `git push origin origin/dev:test` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 (= AMB-4) | Nombre del endpoint y del permiso de aprobación | Pablo | Nada | **DECIDIDA (2026-09-21)**: `POST /billetera/retiros/{ordenId}/aprobacion` con `desenlace ∈ {AUTORIZADA, RECHAZADA}`; permiso nuevo `RETIRO_APROBAR` asignado al rol **`TESORERIA`** del seed (`sql/60_semillas/10-roles-y-permisos.sql`), nunca a `PARTICIPANTE`/`ORGANIZADOR` |
| Q-02 (= AMB-5) | Retiro < umbral | Pablo · negocio | Nada | **DECIDIDA (2026-09-21)**: siempre `PENDIENTE → AUTORIZADA → EN_PROCESO → PAGADA`; por debajo del umbral la autorización es automática en la misma transacción de creación (`aprobada_por = NULL`); nunca `PENDIENTE → PAGADA` |
| Q-03 (= AMB-2) | Consumo one-shot del `jti` en tabla propia del núcleo | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: JWT step-up RS256 emitido por `identidad`, validado localmente por `nucleo-financiero` con el JWKS; `jti` consumido una sola vez en `nucleo_financiero.evidencia_mfa_consumida`; contrato ya en `dev`: `docs/auditoria-produccion/contratos/step-up-jwt.md` |
| Q-04 | Proveedor real de retiros y si soporta clave de idempotencia | Negocio | Nada | **DECIDIDA (2026-09-21)**: puerto `ProveedorDeRetiro` + doble en tres niveles bajo `local/test`; en `production` sin adaptador real el servicio **no arranca**; el proveedor real y su soporte de clave de idempotencia siguen siendo decisión de negocio — eso no bloquea nada del turno |
| Q-05 | Rol de backoffice al que se asigna `RETIRO_APROBAR` | Pablo | Nada | **DECIDIDA (2026-09-21)**: rol **`TESORERIA`** (existe en el seed); `RESPONSABLE_RIESGOS` conserva `REVERSO_AUTORIZAR`; la segregación solicitante ≠ aprobador la garantiza `ck_retiro_doble_aprobacion` + el CU |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` solo
      por `DECISION_REQUIRED` (todo contrato ajeno se simuló en tres niveles).
- [ ] Bitácora `docs/auditoria-produccion/carriles/PR2-nucleo-financiero.md` y tu daily con el
      avance calculado en la primera línea.
- [ ] Evidencia literal en `evidencia/`: asientos del pago del retiro con débitos = créditos,
      prueba de idempotencia ejecutada dos veces, cuadre desde el libro, caso de reversa,
      redondeo declarado (regla 91.6).
- [ ] Gates: `evidence-and-verification` siempre; `money-movement-safety` y
      `accounting-double-entry` en H1, H3, H4; `security-guardrails` y `data-privacy-financial`
      en H2 y H4; `microservices-testing` en H2.S4 y H4.S2.
- [ ] Todo mergeado en `dev` y espejado en `test`; ninguna rama con trabajo verde sin pushear.
- [ ] Peldaño de evidencia declarado por hito (regla 30).
