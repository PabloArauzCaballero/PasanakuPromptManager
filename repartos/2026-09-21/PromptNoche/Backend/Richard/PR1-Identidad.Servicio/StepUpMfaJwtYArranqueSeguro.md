# Identidad: el challenge MFA con propósito, la evidencia step-up que el núcleo puede verificar solo, y un servicio que no arranca con claves de juguete

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Richard · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio(s):** `identidad`
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Richard-Daily-Noche-2026-09-21.md](../Richard-Daily-Noche-2026-09-21.md)
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (este encargo cubre H3.S2, H3.S3.M1, H5.S1, H5.S2.M2/M4/M5, H5.S3, H5.S4 y la parte de `identidad` de H5.S5.M3, H7.S2, H9.S1)
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `richard/feature/carril-PR1-identidad`
- **3 hitos · 9 subtareas · 28 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar (este repo) dentro de `PasanakuBackend/`. El backend trae sus propias skills en `.claude/skills/` (`back-spring`, `autenticacion-jwt`, `idempotencia-reintentos`…): **se suman, no se reemplazan**.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `authn-identity` | Challenge MFA, evidencia step-up, rotación de refresh, reset de contraseña |
| `environment-secrets-config` | Clave de firma y pimienta desde secretos; perfiles por entorno; fallar al arrancar |
| `security-guardrails` | Gate de todo lo que toca credenciales y tokens |
| `data-privacy-financial` | Ni OTP ni tokens ni documentos en logs, bitácora ni evidencia |
| `audit-trail-history` | Rastro append-only del challenge, del reuso de refresh y del login fallido |
| `api-testing` | Matriz de autorización negativa de sesiones y dispositivos |
| `test-case-design-techniques` | Los tres niveles del doble de OTP: correcto, límite, inválido |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre del turno con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 65 · **90** · 98

## 2. Resultado observable

Un titular autenticado pide un desafío MFA con propósito `RETIRO`, presenta su factor y recibe una **evidencia step-up** (JWT RS256 de ≤ 5 minutos) que `nucleo-financiero` puede verificar con el JWKS público sin llamar a `identidad`; y `identidad` con perfil `production` **no arranca** sin `JWT_CLAVE_FIRMA`, emite `iss`/`aud`, publica JWKS con solapamiento de claves, y rechaza un refresh reutilizado invalidando la familia entera.

**Kill-test:** arrancar `identidad` con `SPRING_PROFILES_ACTIVE=production` y `JWT_CLAVE_FIRMA` vacía. Si levanta y loguea "se genero una clave EN MEMORIA", esto NO está hecho.

## 3. Alcance

**IN:** `servicios/identidad/**` (contrato OpenAPI, aplicación, dominio, infraestructura, tests, `application*.yml`), `docs/operacion/jwt-key-rotation.md`, `docs/auditoria-produccion/contratos/step-up-jwt.md`, `docs/auditoria-produccion/carriles/PR1-identidad.md` (tu bitácora de carril), `docs/Arquitectura/ADR-048 MFA step-up para operaciones sensibles.md`, y **un micro-PR al troncal** para la tabla del desafío en `scripts/modelo.py` / `docs/entidades/*.puml` → `sql/` regenerado.

**OUT:** `nucleo-financiero` (Justin valida tu evidencia; vos no tocás su código aunque veas cómo la consume). `plataforma/comun-web` (el decodificador común con validación de `iss`/`aud` es de Leo: vos **emitís** los claims, él los **exige**). `.github/workflows` (Pablo). Frontends. `main` y `test` no se tocan a mano: `test` se espeja desde `dev` (ver ritual).

**Reservas de archivos:** todo `servicios/identidad/**`; `docs/operacion/jwt-key-rotation.md`; `docs/auditoria-produccion/contratos/step-up-jwt.md`; `docs/auditoria-produccion/carriles/PR1-identidad.md`; `docs/Arquitectura/ADR-048*.md`. En `sql/` solo lo que genere tu micro-PR de la tabla del desafío.

### Ritual de entrega — `dev` y `test`, sin esperar a nadie

```bash
git fetch origin && git checkout -b richard/feature/carril-PR1-identidad origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply :servicios:identidad:webTest :servicios:identidad:integrationTest spotlessCheck
git push -u origin HEAD
gh pr create --base dev --fill --title "feat(identity): <subtarea>"
gh pr merge --rebase                       # dev no tiene protección: mergea ya; el CI corre igual
git fetch origin && git push origin origin/dev:test   # test es espejo de dev (AMB-R1)
```

- **Micro-PR al troncal** (`sql/` vía generador, `gradle/libs.versions.toml`, `buildSrc/`, plantilla `scripts/nuevo_servicio.py`): un commit con solo eso, título `troncal(<que>): …`, mergeado a `dev` **dentro de la hora**; después rebaseás. Nunca mezcles troncal con carril.
- **Jamás te detenés.** Si lo que necesitás es de otro carril y todavía no está en `dev`, nombrás el contrato, construís el doble en **tres niveles** (correcto · límite · inválido) bajo `@Profile({"local","test"})` o en `src/test`, cerrás contra el doble **declarándolo** en tu daily §4/§5, y dejás la microtarea de integración diferida. Lo único que queda abierto es una decisión de negocio (`DECISION_REQUIRED`).
- Un CI rojo por un job ajeno a tu carril (hoy `dev` ya está rojo en Spotless hasta que Pablo lo cierre) se anota en tu daily §6 con el job y **no te detiene**; tu gate local en verde es la condición de merge.
- Un test tuyo en rojo sí te detiene esa microtarea: se corrige o va `A MEDIAS` con las cuatro respuestas. Nunca `skip`, nunca `@Disabled`.

### Contrato fijado con Justin — el JWT de evidencia step-up (no se negocia en el chat: está acá)

| Claim | Valor | Quién lo exige |
|---|---|---|
| `alg` / `kid` | `RS256`, `kid` de la misma `RSAKey` que firma el token de acceso | Justin (vía JWKS) |
| `iss` | `aportaya-identidad` | Leo (decoder común) y Justin |
| `aud` | `["aportaya-nucleo-financiero"]` | Justin |
| `sub` | UUID del usuario | Justin (= usuario de la sesión) |
| `jti` | UUID, **un solo uso** | Justin (tabla `evidencia_mfa_consumida`) |
| `iat` / `exp` | `exp − iat ≤ PT5M` (`aportaya.mfa.vigencia-evidencia`, sin literal en código) | Justin |
| `proposito` | `RETIRO` \| `CAMBIO_CUENTA` \| `ADMIN` | Justin (`RETIRO`) |
| `desafio_id` | UUID del desafío verificado | trazabilidad |
| `acr` | `mfa` | Justin |
| `amr` | `["otp"]` \| `["totp"]` \| `["biometria"]` | informativo |

Ese contrato va escrito en `docs/auditoria-produccion/contratos/step-up-jwt.md` (H1.S2.M1) **antes** de implementar. Justin construye su doble con esta tabla; vos construís tu emisor con esta tabla. Si uno de los dos necesita cambiarla, lo anota en el daily §6 y **no cambia nada hasta cerrar el turno**.

## 4. Plan

### H1 — El desafío MFA con propósito existe, verifica un factor real y emite la evidencia

**CA:** Dado un usuario autenticado con factor enrolado, cuando crea un desafío `RETIRO` y presenta el factor correcto, entonces recibe una evidencia que cumple el contrato de arriba; sin factor enrolado → `FACTOR_NO_ENROLADO`; factor incorrecto N veces → `DEMASIADOS_INTENTOS`; el OTP no aparece en ningún log ni bitácora.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*CU04Desafio*' --tests '*EvidenciaStepUp*'` PASS (≥ 9 tests) y `./gradlew :servicios:identidad:webTest` PASS, salidas en `evidencia/`; `python3 scripts/verificar_seguridad.py` exit 0; gate `data-privacy-financial` revisado.
**Estado:** TODO

#### H1.S1 — Contrato, persistencia y caso de uso del desafío (plan H3.S2)

**CA:** Dado `POST /sesiones/desafios` con `proposito=RETIRO` e `Idempotency-Key`, cuando el usuario tiene factor enrolado, entonces `201 {desafioId, expiraEn}` y el OTP sale por su canal; sin sesión `401`; cuerpo con campo no declarado `400`.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*CU04DesafioTest*'` → 5 PASS; `./gradlew :servicios:identidad:webTest --tests '*SesionesControllerWebTest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Contrato `identidad.yaml`: `POST /sesiones/desafios`, `POST /sesiones/desafios/{desafioId}/verificacion`; esquemas `EntradaDesafio{proposito}`, `SalidaDesafio{desafioId, expiraEn}`, `EntradaVerificacion{factor: FactorPresentado}`, `SalidaEvidencia{evidencia, expiraEn, jti}`; 401/403/409/422; `Idempotency-Key` obligatoria; `additionalProperties: false` | Clientes generan sin error | `./gradlew :servicios:identidad:generarClientes` → exit 0 | TODO |
| H1.S1.M2 | Persistencia del desafío: leer `docs/Modelos/Entidades/01…/token_verificacion.md` y `politica_token`; **decidir** reutilizar `token_verificacion` con `proposito` nuevo o tabla `desafio_mfa`; cambio en `scripts/modelo.py`/`.puml` → `generar_ddl.py` → **micro-PR al troncal** | `generar_ddl.py` no deja diff residual; `verificar_boveda.py` verde | `python3 scripts/generar_ddl.py && python3 scripts/verificar_boveda.py` → exit 0; PR `troncal(sql): desafio mfa` mergeado | TODO |
| H1.S1.M3 | Tests rojos `CU04DesafioTest` (5): crea; sin factor enrolado; N intentos; expirado; idempotente con la misma clave | 5 FAIL por aserción | `./gradlew :servicios:identidad:integrationTest --tests '*CU04DesafioTest*'` → 5 FAIL | TODO |
| H1.S1.M4 | `CU04CrearDesafio` + `CU04VerificarDesafio` (aplicación): hash del OTP con la pimienta, TTL desde `politica_token`, intentos desde `aportaya.acceso.*`, envío por el puerto de notificación existente; **doble del proveedor OTP** `@Profile({"local","test"})` en tres niveles: correcto (OTP fijo por desafío), límite (OTP presentado en el último segundo de vigencia → acepta; un segundo después → rechaza), inválido (OTP ajeno, ya usado, malformado) | 5 PASS + 3 del doble | mismo comando → PASS; `DobleOtpTest` PASS | TODO |
| H1.S1.M5 | Controlador con `@Permiso`/autenticado, `SabanaDeSeguridadWeb` cubre las 2 rutas; auditoría append-only `desafio_creado / verificado / fallido` con `usuario_id`, `desafio_id`, `resultado`, correlación — **sin el OTP** | 401/403/400 PASS; grep de logs sin OTP | `./gradlew :servicios:identidad:webTest` PASS; `grep -rn "<otp del test>" servicios/identidad/build/test-results` → vacío | TODO |

#### H1.S2 — Emisión de la evidencia step-up (plan H3.S3.M1) y su contrato escrito

**CA:** Dado un desafío verificado, cuando se emite la evidencia, entonces el JWT cumple los 10 claims de la tabla del contrato y vence en ≤ 5 min según `Reloj` inyectado.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*EvidenciaStepUpTest*'` → 4 PASS; `docs/auditoria-produccion/contratos/step-up-jwt.md` escrito.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Escribir `docs/auditoria-produccion/contratos/step-up-jwt.md` con la tabla de claims **tal cual** está arriba + ejemplo de token decodificado (claves de prueba, nunca reales) | Archivo existe antes de tocar código | `test -f docs/auditoria-produccion/contratos/step-up-jwt.md` | TODO |
| H1.S2.M2 | `EmisorDeEvidencia` (reusa la `RSAKey` y el `kid` de `EmisorDeAcceso`; `Reloj` en vez de `Instant.now()`); test de los 10 claims, de `exp − iat`, de `aud` y de firma verificable con el JWKS publicado | 4 PASS | `./gradlew :servicios:identidad:integrationTest --tests '*EvidenciaStepUpTest*'` | TODO |
| H1.S2.M3 | `CU04VerificarDesafio` devuelve `SalidaEvidencia`; el desafío queda consumido (segundo intento de verificación → `409`) | PASS | `./gradlew :servicios:identidad:integrationTest --tests '*CU04DesafioTest*'` (caso nuevo) | TODO |
| H1.S2.M4 | Métrica `mfa_failures_total{motivo}` (sin `usuario_id` como etiqueta) desde el CU | Aparece en `/actuator/prometheus` | `curl -s localhost:8080/actuator/prometheus \| grep mfa_failures_total` (servicio levantado con compose) → 1 línea | TODO |

#### H1.S3 — Cierre del hito: ADR y bitácora de carril

**CA:** Dado `docs/Arquitectura/`, cuando se lee `_Arquitectura.md`, entonces enlaza `ADR-048` con contexto, decisión, alternativas (MFA del login reutilizado · llamada síncrona a identidad · JWT step-up), consecuencias y riesgos.
**DoD:** `python3 scripts/verificar_boveda.py` → exit 0.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S3.M1 | `ADR-048 MFA step-up para operaciones sensibles.md` + enlace en `_Arquitectura.md` + fila en `docs/Seguridad.md` con el comando que lo comprueba | Bóveda y seguridad verdes | `python3 scripts/verificar_boveda.py && python3 scripts/verificar_seguridad.py` → exit 0 | TODO |
| H1.S3.M2 | `docs/auditoria-produccion/carriles/PR1-identidad.md`: problema · causa raíz · solución · test · evidencia · riesgo residual (metaprompt §60) del hito | 6 campos | revisión | TODO |

### H2 — `identidad` arranca seguro: clave obligatoria, `iss`/`aud`, JWKS con solapamiento

**CA:** Dado perfil `production` sin `JWT_CLAVE_FIRMA`, cuando arranca, entonces falla nombrando la propiedad; dado un token emitido, entonces lleva `iss=aportaya-identidad`, `aud` y `kid`; dado dos claves configuradas (vigente + anterior), entonces ambos tokens validan contra el JWKS publicado.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*ArranqueProduccionTest*' --tests '*JwksRotacionTest*'` PASS; `./gradlew :servicios:identidad:test --tests '*EmisorDeAcceso*'` PASS; runbook escrito.
**Estado:** TODO

#### H2.S1 — Sin RSA efímera fuera de `local`/`test` (plan H5.S1)

**CA:** Dado `aportaya.jwt.clave-firma` vacía y perfil `production`, cuando arranca, entonces `IllegalStateException("aportaya.jwt.clave-firma es obligatoria en production")`; con perfil `test`, genera en memoria y avisa.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*ArranqueProduccionTest*'` → 2 PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Test rojo `ArranqueProduccionTest`: `@ActiveProfiles("production")` + clave vacía → el contexto falla; `test` + vacía → levanta | 1 FAIL hoy | comando → 1 FAIL | TODO |
| H2.S1.M2 | `EmisorDeAcceso.java:52-66`: inyectar `Environment`; `generar()` solo si perfil ∈ {local,test}; si no, lanzar | 2 PASS | comando → PASS | TODO |
| H2.S1.M3 | `application-production.yml`: `aportaya.jwt.clave-firma: ${JWT_CLAVE_FIRMA}` **sin default**; `application-local.yml`/`-test.yml` conservan el default vacío | PASS | comando → PASS | TODO |

#### H2.S2 — `iss`, `aud`, `kid` y rotación con solapamiento (plan H5.S2.M2/M4/M5)

**CA:** Dado el emisor, cuando firma acceso o evidencia, entonces incluye `iss` y `aud` de configuración; dado `aportaya.jwt.claves-anteriores` con una JWK pública, cuando se consulta `/.well-known/jwks.json`, entonces publica ambas y un token firmado con la anterior sigue validando.
**DoD:** `./gradlew :servicios:identidad:test --tests '*EmisorDeAccesoTest*'` PASS; `./gradlew :servicios:identidad:integrationTest --tests '*JwksRotacionTest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | `iss` (`aportaya.jwt.emisor`, default `aportaya-identidad`) y `aud` (`aportaya.jwt.audiencia`, lista) en `emitir` y en `EmisorDeEvidencia`; **no dependés del decodificador de Leo**: verificás tus claims parseando con Nimbus en el test | Test de claims PASS | `./gradlew :servicios:identidad:test --tests '*EmisorDeAccesoTest*'` | TODO |
| H2.S2.M2 | `jwks()` publica la vigente + `aportaya.jwt.claves-anteriores` (solo parte pública); `kid` distinto por clave; test: token firmado con la anterior valida contra el JWKS | PASS | `./gradlew :servicios:identidad:integrationTest --tests '*JwksRotacionTest*'` | TODO |
| H2.S2.M3 | `docs/operacion/jwt-key-rotation.md` con las 7 secciones (síntomas, dashboards/consultas, diagnóstico, acciones seguras, recuperación, validación, escalamiento): generar JWK, cargar en secretos, desplegar con ambas, esperar 2 × vigencia, retirar | 7 secciones | `grep -c "^## " docs/operacion/jwt-key-rotation.md` ≥ 7 | TODO |

#### H2.S3 — Perfiles de `identidad` (parte de plan H5.S5.M3)

**CA:** Dado `SPRING_PROFILES_ACTIVE=test`, cuando corren `ArranqueTest` y la suite, entonces levantan con los valores de prueba; dado `production`, exige `JWT_CLAVE_FIRMA`, `SEGURIDAD_PIMIENTA` real, `BD_URL`, `KAFKA_URL`.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*Arranque*'` PASS (los 3 perfiles cubiertos por test).
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S3.M1 | `application-{local,test,staging,production}.yml` de `identidad` (si Leo ya mergeó la plantilla en `scripts/nuevo_servicio.py`, regenerá desde ella; si no, escribilos a mano con la misma forma y lo anotás en §6 para que él la incorpore) | 4 archivos | `ls servicios/identidad/src/main/resources/application-*.yml \| wc -l` → 4 | TODO |
| H2.S3.M2 | `ArranqueTest` activa `test`; `ArranqueProduccionTest` cubre `production` con placeholders (`pimienta-de-prueba`, `cambiar`) → falla | PASS | `./gradlew :servicios:identidad:integrationTest --tests '*Arranque*'` | TODO |

### H3 — Refresh, contraseñas, propiedad y métricas: lo que ya parecía bien queda demostrado

**CA:** Dado refresh A rotado a B, cuando A vuelve, entonces `401`, familia invalidada y evento de auditoría; dado el hasher, cumple Argon2id con parámetros OWASP y pimienta de entorno; dado usuario A, no lee sesiones/dispositivos de B; `auth_login_failures_total` se expone.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*RefrescoReuso*' --tests '*AutorizacionNegativa*' --tests '*CU09*'` PASS; `./gradlew :servicios:identidad:test --tests '*ArgonParametros*'` PASS.
**Estado:** TODO

#### H3.S1 — Reuso de refresh detectado en la aplicación (plan H5.S3)

**CA:** Dado A→B→A, cuando A se presenta, entonces `401`, `sesion`/token en `INVALIDADO`, fila en bitácora y evento `sesion.familia_revocada` en el outbox.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*RefrescoReusoTest*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Localizar el CU de refresco (`grep -rn refresc servicios/identidad/src/main`; `CorteDeCredencial.java`) y el trigger R-SEG-09 (`sql/40_reglas/restricciones.sql`); documentar flujo con ruta:línea en `carriles/PR1-identidad.md` | Flujo documentado | revisión | TODO |
| H3.S1.M2 | `RefrescoReusoTest` A→B→A sobre el trigger real; aserciones: 401, estado `INVALIDADO`, bitácora | PASS o FAIL clasificado `PRODUCT_BUG` → M3 | comando → salida pegada | TODO |
| H3.S1.M3 | Si la app no emite auditoría/evento: agregarlo en el CU (outbox `sesion.familia_revocada`, bitácora con actor, target, correlación) | PASS | comando → PASS | TODO |

#### H3.S2 — Contraseñas, pimienta y reset (plan H5.S4)

**CA:** Dado el hasher real, cuando se inspecciona, entonces Argon2id con `m ≥ 19 MiB`, `t ≥ 2`, `p = 1` (o valores justificados en ADR) y comparación timing-safe; dado un reset, el token vence, es de un solo uso e invalida las sesiones.
**DoD:** `./gradlew :servicios:identidad:test --tests '*ArgonParametrosTest*'` PASS; `./gradlew :servicios:identidad:integrationTest --tests '*CU09*'` PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | `ArgonParametrosTest` contra la clase real (localizar el hasher con `grep -rn Argon2 servicios/identidad/src/main`) | PASS | comando | TODO |
| H3.S2.M2 | Reset (CU-09): tests de expiración, un solo uso, invalidación de sesiones tras el reset; corregir lo que falte | PASS | `./gradlew :servicios:identidad:integrationTest --tests '*CU09*'` | TODO |
| H3.S2.M3 | Barrido de logs de `identidad`: ningún `BITACORA.*` con contraseña, OTP, token, JWT ni JWK privada; corregir y pegar el grep | grep vacío | `grep -rnE "BITACORA\.[a-z]+\(.*(token\|otp\|clave\|jwk)" servicios/identidad/src/main` → solo identificadores | TODO |

#### H3.S3 — Propiedad, métricas y baseline del servicio (parte de plan H7.S2, H9.S1, H0)

**CA:** Dado usuario A, cuando pide sesiones, dispositivos o perfil de B alterando el id, entonces `403`/`404` sin datos de B; `auth_login_failures_total` sube con cada fallo.
**DoD:** `./gradlew :servicios:identidad:integrationTest --tests '*AutorizacionNegativaTest*'` PASS; `curl … \| grep auth_login_failures_total` → 1 línea; `docs/auditoria-produccion/baseline-PR1-identidad.md` con la corrida inicial del módulo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | **Primero de todo el turno:** baseline del módulo en el SHA base: `webTest` + `integrationTest` de `identidad` con salida y clasificación de rojos (regla 80.4) en `baseline-PR1-identidad.md` | Archivo con veredicto por corredor | `./gradlew :servicios:identidad:webTest :servicios:identidad:integrationTest; echo exit=$?` pegado | TODO |
| H3.S3.M2 | `AutorizacionNegativaTest` (dos sesiones) sobre todo endpoint de `identidad` con recurso identificado; corregir ownership en el CU, nunca en el controller | PASS | comando | TODO |
| H3.S3.M3 | `auth_login_failures_total{motivo}` desde `CU04Autenticar`, sin etiqueta de usuario | 1 línea en prometheus | `curl -s localhost:8080/actuator/prometheus \| grep auth_login_failures_total` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 (= AMB-3) | Qué factor real verifica `identidad` en el desafío | Pablo · negocio | Nada | **DECIDIDA (2026-09-21)**: el factor real de producción es **TOTP (RFC 6238)** verificado dentro de `identidad` desde `factor_mfa.secreto_cifrado` (tipo `TOTP` ya existe en el CHECK): **sin proveedor externo**; SMS/WhatsApp (`factor_mfa.tipo` `SMS`/`WHATSAPP`) salen por el servicio `notificaciones` como segundo canal, con doble en tres niveles solo en `local/test`. El desafío **reutiliza `token_verificacion`** (`tipo_token='OTP'`, `proposito='MFA_RETIRO'`, `politica_id`, `intentos_fallidos`/`max_intentos`, `uso_unico=true`): sin tabla nueva |
| Q-02 (= AMB-2) | `aud` global vs por servicio | Pablo (arquitectura) | Nada | **DECIDIDA (2026-09-21)**: token de acceso `aud=["aportaya"]` (global); evidencia step-up `aud=["aportaya-nucleo-financiero"]`; `iss=aportaya-identidad` en ambos |
| Q-03 | Reutilizar `token_verificacion` o crear `desafio_mfa` | Vos | Nada | **DECIDIDA (2026-09-21)**: **reutilizar `token_verificacion`** — ya tiene `proposito`, `tipo_token='OTP'`, `hash_token`, `politica_id`, `intentos_fallidos`, `max_intentos`, `uso_unico`, `familia_id`; se agrega el valor `'MFA_RETIRO'` a `proposito` y nada más; sin tabla `desafio_mfa` |
| Q-04 | Parámetros Argon2 actuales vs OWASP | Pablo | Nada | **DECIDIDA (2026-09-21)**: piso OWASP para Argon2id — `m ≥ 19456 KiB`, `t ≥ 2`, `p = 1`; si `Argon2Hasheador.{ITERACIONES, MEMORIA_KIB, PARALELISMO}` ya lo cumplen se dejan; si no, se suben a ese piso y se registra en ADR-048 |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia (solo `DECISION_REQUIRED` justifica un `BLOQUEADO`: todo contrato ajeno se simuló).
- [ ] Bitácora de carril `docs/auditoria-produccion/carriles/PR1-identidad.md` y tu daily con el
      avance calculado en la primera línea.
- [ ] Evidencia literal en `evidencia/`, sin datos reales de participantes, sin OTP ni tokens.
- [ ] Gates: `evidence-and-verification` siempre; `security-guardrails` y `data-privacy-financial`
      en todo el encargo; `audit-trail-history` en H1.S1.M5 y H3.S1.
- [ ] Todo mergeado en `dev` y espejado en `test` con el ritual; ninguna rama de carril con
      trabajo verde sin pushear.
- [ ] Peldaño de evidencia declarado por hito (regla 30).
