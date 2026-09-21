# Daily — turno noche — 2026-09-21

> **AVANCE DEL TURNO: 0 / 213 — 0 %.**
> **Estado:** `IN_PROGRESS`. Escrito **al repartir**, antes del turno: todo resultado está en
> `NOT_RUN` a propósito, porque nadie ejecutó nada todavía.

- **Turno:** noche · **Fecha:** 2026-09-21
- **Modelo de datos de referencia:** `Pasanaco_backendBO/docs/Index.md`
- **Plan madre:** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (210 microtareas; este reparto suma 213 porque cada carril arranca con el baseline de su módulo)
- **Repo objetivo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · `test` = espejo de `dev`
- **Objetivo del turno:** `dev` production-ready, técnicamente demostrable: idempotencia con el scope del índice, outbox que publica, MFA step-up sin bypass, doble aprobación en la aplicación, JWT/arranque seguros, CI verde con SCA/SBOM/Trivy, borde con rate limiting, y `FINAL_REPORT.md` con estado sustentado.

## 1. Quién tiene qué

| Persona | Servicio | Encargo | Hitos | Subtareas | Microtareas | Estado |
|---|---|---|---:|---:|---:|---|
| **Richard** | `identidad` | [Challenge MFA con propósito, evidencia step-up y arranque seguro](Richard/PR1-Identidad.Servicio/StepUpMfaJwtYArranqueSeguro.md) | 3 | 9 | 28 | `NOT_RUN` |
| **Justin** | `nucleo-financiero` | [Idempotencia con scope, MFA step-up y doble aprobación de retiro](Justin/PR2-NucleoFinanciero.Servicio/IdempotenciaMfaYDobleAprobacionDeRetiro.md) | 4 | 13 | 42 | `NOT_RUN` |
| **Leo** | `plataforma/comun-*`, `buildSrc`, plantilla | [Outbox que publica, helper de idempotencia y guardas comunes](Leo/PR3-Plataforma.Infra/OutboxQuePublicaYGuardasComunes.md) | 4 | 13 | 49 | `NOT_RUN` |
| **Marcelo** | `aportes`, seguridad transversal, base, scripts | [Inventario, idempotencia de aportes, ledger, base y código muerto](Marcelo/PR4-Seguridad.Transversal/InventarioIdorLedgerBaseYCodigoMuerto.md) | 6 | 11 | 40 | `NOT_RUN` |
| **Pablo** | CI, supply chain, `gateway`, `despliegue/`, operación | [Baseline, CI verde sin trampas, borde, carga y cierre](Pablo/PR5-Ci.Operacion/CiRealSupplyChainBordeYCierre.md) | 5 | 17 | 54 | `NOT_RUN` |
| | | | **22** | **63** | **213** | |

## 2. Lo primero, para todos

Antes de la primera microtarea: instalar el estándar (sección 1 del encargo) y **pegar la salida
de los dos comandos** en el daily personal. Después, **el baseline de tu módulo** (es la primera
microtarea de cada encargo): nadie toca código sin saber qué estaba rojo antes.

Los dos merges que abren el turno, en este orden:

1. **Pablo · H2.S1 — Spotless** en la primera media hora: hoy `dev` está rojo en "2 · formato" y
   deja `skipped` todo lo demás (`gh run view 35644455765`). Cuando avise, todos rebasean.
2. **Leo · H3.S3.M1 — plantilla de perfiles** (`application-{local,test,staging,production}.yml`
   en `scripts/nuevo_servicio.py`) en la primera hora. Richard, Justin y Pablo (gateway) la
   aplican a su servicio; si no llegó, la escriben a mano con la misma forma y lo anotan.

### Un comando para Pablo antes de arrancar — el ruleset mínimo

El agente que armó el reparto intentó crearlo y **no tiene permiso** para modificar recursos compartidos del repo. Es una línea:

```bash
gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input repartos/2026-09-21/PromptNoche/Pablo/PR5-Ci.Operacion/entregables/ruleset-minimo.json
gh api repos/PabloArauzCaballero/PasanakuBackend/rulesets --jq '.[].name'   # → proteccion-minima
```

Bloquea force-push y borrado en `dev`, `test` y `main`; **no** exige PR ni aprobaciones, así que no frena a nadie. El ruleset completo va en la promoción.

### El ritual de entrega es el mismo para los cinco

```bash
git fetch origin && git checkout -b <persona>/feature/carril-PR<n>-<slug> origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply <gate del módulo> spotlessCheck
git push -u origin HEAD
gh pr create --base dev --fill --title "<prefijo>: <subtarea>"
gh pr merge --rebase                                   # dev sin protección: mergea ya, el CI corre igual
git fetch origin && git push origin origin/dev:test    # test es espejo de dev
```

- **Micro-PR al troncal** para `sql/` (siempre vía `scripts/generar_ddl.py`, nunca DDL a mano),
  `gradle/libs.versions.toml`, `buildSrc/`, `scripts/nuevo_servicio.py`: un commit con solo eso,
  título `troncal(<que>): …`, mergeado a `dev` **dentro de la hora**; después todos rebasean.
  Es el contrato de carril del backend (`planes/07` §6, `planes/19` §3).
- **Merge = tu gate local en verde.** Un CI rojo por un job ajeno se anota como hallazgo y no
  detiene a nadie. Un test propio en rojo detiene **esa** microtarea, nunca el carril.
- **Nunca** `skip`, `@Disabled`, `|| true`, borrar una constraint, bajar un permiso ni apagar RLS.

## 3. Orden de dependencia — quién espera a quién

| Quien espera | De quién | Qué exactamente | Qué hace mientras tanto |
|---|---|---|---|
| Justin (H2) | **Richard (H1.S2)** | La evidencia step-up (JWT) | **Doble en tres niveles** (`EmisorDeEvidenciaDePrueba` + JWKS de prueba, H2.S2.M1): correcto / al borde de `exp` y `jti` repetido / otra clave, otro `sub`, otro propósito. Cierra H2 entero; la integración real es H2.S4.M2 y si no llega queda `A MEDIAS` declarada |
| Richard (H2.S2) | **Leo (H3.S1)** | El decodificador común que exige `iss`/`aud` | No espera: **emite** los claims del contrato y los verifica parseando con Nimbus en su test |
| Justin, Richard, Marcelo | **Leo (H3.S3.M1)** | La plantilla de `application-*.yml` | Si no está en `dev` a la hora: la escriben a mano con la misma forma y lo anotan en §6 |
| Leo (H2.S2) | nadie | Un caso de uso que emita al outbox | **Emisor y consumidor de prueba propios** en `comun-mensajeria/src/e2eTest` (AMB-10) |
| Marcelo (H3.S1.M3) | **Justin (H1)** | El scope corregido del ledger para la aserción de replay | Escribe el escenario; si el fix no está, esa aserción queda `A MEDIAS` declarada y sigue con los otros 10 |
| Marcelo (H5.S1.M2) | Richard, Justin (auditoría en sus CU) | Que los CU críticos usen la bitácora | Escribe `AuditoriaCriticaTest`; en rojo por bug ajeno → hallazgo al dueño, test en su rama, sigue |
| Pablo (H2.S6.M1/M3) | Justin, Leo, Marcelo | Los E2E financieros y los scripts de inventario | Cablea los jobs igual: los corredores toleran cero tests; los pasos de scripts quedan preparados y declarados |
| Pablo (H5.S4) | los cuatro | Las bitácoras `carriles/PR1…PR4.md` | Consolida al cierre con lo que haya; lo que falte va `A MEDIAS`/`PENDIENTE` en `FINAL_REPORT.md`, nunca `READY` sin evidencia |
| Todos | proveedor de OTP, pasarela, proveedor de retiros (no existen) | Los contratos externos | **Dobles en tres niveles** bajo `@Profile({"local","test"})`; producción sin adaptador real **no arranca** (fail closed) |

> **Nadie se queda esperando (regla 65).** Si el contrato de lo que falta se puede nombrar, se
> simula en tres niveles —correcto, límite, inválido— y se cierra contra el doble, declarándolo.
> Lo único que queda abierto es una decisión de negocio (`DECISION_REQUIRED`) o una acción sobre
> algo compartido (aplicar rulesets: solo Pablo, por escrito).

**Si dos personas miden lo mismo y les da distinto, eso es un hallazgo, no un empate a resolver
charlando.** Gana el archivo abierto, y la diferencia se registra en §6.

## 4. Reservas de archivos y servicios — para que nadie se pise

| Servicio / área | Reservado para |
|---|---|
| `servicios/identidad/**`; `docs/operacion/jwt-key-rotation.md`; `docs/auditoria-produccion/contratos/step-up-jwt.md`; `ADR-048` | **Richard** |
| `servicios/nucleo-financiero/**` (salvo los 3 tests de Marcelo); `docs/operacion/{provider-timeout,withdrawal-reconciliation}.md`; `ADR-049` | **Justin** |
| `plataforma/comun-{dominio,datos,web,mensajeria,archivos,pruebas}/**`; `buildSrc/**`; `scripts/nuevo_servicio.py`; `contratos/evento-kafka.md`; `ADR-046`, `ADR-047` | **Leo** |
| `servicios/aportes/**`; `scripts/verificar_seguridad.py`, `scripts/inventario_endpoints.py`, `scripts/verificar_contratos_limites.py`; `sql/50_verificacion/**`; los tests `LibroInvariantesTest`, `LibroBenchmarkTest`, `AppendOnlyTest`, `AislamientoEsquemaTest` (por servicio), `AuditoriaCriticaTest`, `ArchivosSeguridadTest` en cualquier módulo; `docs/auditoria-produccion/{endpoints,security-matrix,financial-invariants,dependencias,mutation-testing,idempotencia-scope}.md`; `docs/operacion/schema-changes.md` | **Marcelo** |
| `.github/**`; `despliegue/**`; `docker-compose.coolify.yml`; `scripts/generar_{compose,gateway,k8s}.py`; `plataforma/gateway/**`; `carga/**`; `build.gradle.kts` raíz; `README.md`; `docs/operacion/{branch-protection,backup-recovery,outbox-backlog,kafka-down,postgres-down,secret-rotation}.md`; `docs/auditoria-produccion/{baseline,PLAN,promotion-gate,FINAL_REPORT,proveedores,limites-de-recursos}.md`; `ADR-050` | **Pablo** |
| `docs/auditoria-produccion/carriles/PR<n>-*.md`, `baseline-PR<n>-*.md` | Cada uno el suyo |
| `sql/**` (generado), `gradle/libs.versions.toml`, `docs/Arquitectura/_Arquitectura.md`, `docs/Seguridad.md`, `docs/Arquitectura/Entornos y despliegue.md` | Compartido **solo por micro-PR al troncal**: cada uno agrega lo suyo, nadie edita lo ajeno, merge dentro de la hora |
| `servicios/{cumplimiento,entregas,erp,garantia,grupos,notificaciones,organizador,publicidad,tarifas,transparencia}` | **Sin dueño este turno**: solo lectura. Lo que se encuentre roto ahí va a §6 como hallazgo con ruta |
| `main` | **Nadie.** Se recomienda la promoción en `FINAL_REPORT.md`; no se ejecuta |

**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

## 5. Ambigüedades abiertas — se arrastran, no se resuelven

| ID | Qué | Quién la cierra | Estado |
|---|---|---|---|
| AMB-R1 | `test` es espejo de `dev` (`git push origin origin/dev:test` tras cada merge) | Pablo | **DECIDIDA (2026-09-21)**: `test` es espejo fast-forward de `dev` (`git push origin origin/dev:test` tras cada merge); el ruleset mínimo `proteccion-minima` (JSON y comando en el daily del equipo §2, lo aplica Pablo con una línea) bloquea force-push y borrado en `dev`, `test` y `main` |
| AMB-2 | Evidencia step-up = JWT corto validado localmente; `jti` consumido en tabla del núcleo | Pablo (arquitectura) | **DECIDIDA (2026-09-21)**: JWT step-up RS256 emitido por `identidad`, validado localmente por `nucleo-financiero` con el JWKS; `jti` consumido una sola vez en `nucleo_financiero.evidencia_mfa_consumida`; contrato ya en `dev`: `docs/auditoria-produccion/contratos/step-up-jwt.md` |
| AMB-3 | Factor real del desafío MFA | Pablo · negocio | **DECIDIDA (2026-09-21)**: el factor real de producción es **TOTP (RFC 6238)** verificado dentro de `identidad` desde `factor_mfa.secreto_cifrado` (tipo `TOTP` ya existe en el CHECK): **sin proveedor externo**; SMS/WhatsApp (`factor_mfa.tipo` `SMS`/`WHATSAPP`) salen por el servicio `notificaciones` como segundo canal, con doble en tres niveles solo en `local/test`. El desafío **reutiliza `token_verificacion`** (`tipo_token='OTP'`, `proposito='MFA_RETIRO'`, `politica_id`, `intentos_fallidos`/`max_intentos`, `uso_unico=true`): sin tabla nueva |
| AMB-4 / AMB-5 | Endpoint/permiso de aprobación; retiro < umbral | Pablo · negocio | **DECIDIDA (2026-09-21)**: `POST /billetera/retiros/{ordenId}/aprobacion` con `desenlace ∈ {AUTORIZADA, RECHAZADA}`; permiso nuevo `RETIRO_APROBAR` asignado al rol **`TESORERIA`** del seed (`sql/60_semillas/10-roles-y-permisos.sql`), nunca a `PARTICIPANTE`/`ORGANIZADOR`. siempre `PENDIENTE → AUTORIZADA → EN_PROCESO → PAGADA`; por debajo del umbral la autorización es automática en la misma transacción de creación (`aprobada_por = NULL`); nunca `PENDIENTE → PAGADA` |
| AMB-6 | Redis para rate limiting distribuido | Pablo (infra) | **DECIDIDA (2026-09-21)**: **Redis entra al stack** (`despliegue/compose/base.yml`, `infra.yml`, Coolify) para `RequestRateLimiter` del gateway; con Redis caído las rutas sensibles deniegan (fail closed); ADR-050 lo registra |
| AMB-7 | Migraciones versionadas (no existen) | Pablo (arquitectura) | **DECIDIDA (2026-09-21)**: este turno sigue con `sql/aplicar.sql` generado (idempotente) y **solo cambios aditivos** al esquema (sin `DROP COLUMN`/`DROP TABLE`/cambio de tipo); se verifica `empty→latest` y `latest→latest` con datos; la adopción de Flyway/Liquibase queda como ADR posterior a la promoción, no se hace ahora |
| AMB-8 | RPO/RTO | Operación | **DECIDIDA (2026-09-21)**: se implementa PITR (base + WAL) y el restore se ejecuta de verdad; el **RPO y el RTO se miden** en ese restore y se reportan como capacidad medida (no como compromiso comercial, que sigue siendo de negocio) |
| AMB-9 | Severidad que bloquea en OSV/Trivy | Pablo | **DECIDIDA (2026-09-21)**: `HIGH` y `CRITICAL` bloquean en OSV y Trivy; `MEDIUM` reporta; toda excepción lleva motivo y fecha de revisión (≤ 30 días) |
| AMB-10 | Consumidor Kafka: solo de prueba | Pablo | **DECIDIDA (2026-09-21)**: consumidor Kafka **de prueba** en `comun-mensajeria/src/e2eTest`; ningún consumidor productivo este turno; contrato del envelope ya en `dev`: `docs/auditoria-produccion/contratos/evento-kafka.md` |
| AMB-12 | Perfiles `local/test/staging/production` | Pablo | **DECIDIDA (2026-09-21)**: perfiles `local`, `test`, `staging`, `production`; `aportaya.entorno.productivo = true` para todo perfil que no sea `local`/`test` (fail closed) |
| Q-Pablo-05 | Aplicar rulesets de protección de ramas | Pablo | **DECIDIDA (2026-09-21)**: durante el turno `dev` **no exige PR ni aprobaciones** (los cinco mergean solos con su gate local); queda **listo** el ruleset mínimo `proteccion-minima` (bloquea force-push y borrado en `dev`, `test` y `main`; el agente no tiene permiso para crearlo, Pablo lo aplica con el comando del daily §2); el ruleset **completo** (PR obligatorio, checks requeridos, CODEOWNERS, 2 aprobaciones en `main`) se activa en la promoción `dev → main` (Pablo H2.S5.M2 lo deja escrito) |

### Las ambigüedades de arriba ya están decididas

Todas las filas de §5 llevan su decisión del 2026-09-21. Los encargos §5 y los dailies §8 dicen lo mismo. Si durante el turno una decisión resulta imposible de aplicar, se registra en §6 del daily personal con la razón y **se sigue con la alternativa declarada**; no se reabre la discusión en el chat.

Los dos contratos entre carriles ya están en `dev` y `test`: `docs/auditoria-produccion/contratos/step-up-jwt.md` (Richard ↔ Justin ↔ Leo) y `docs/auditoria-produccion/contratos/evento-kafka.md` (Leo ↔ todos). Richard H1.S2.M1 y Leo H2.S2.M1 pasan a ser "verificar que está y ajustar solo lo que el código exija".

## 6. Cierre del turno — completar acá

| Persona | HECHO / total | Hitos cerrados | `A MEDIAS` | `BLOQUEADO` | Su daily |
|---|---|---|---|---|---|
| Richard | 0 / 28 | | | | [Richard-Daily-Noche-2026-09-21.md](Richard/Richard-Daily-Noche-2026-09-21.md) |
| Justin | 0 / 42 | | | | [Justin-Daily-Noche-2026-09-21.md](Justin/Justin-Daily-Noche-2026-09-21.md) |
| Leo | 0 / 49 | | | | [Leo-Daily-Noche-2026-09-21.md](Leo/Leo-Daily-Noche-2026-09-21.md) |
| Marcelo | 0 / 40 | | | | [Marcelo-Daily-Noche-2026-09-21.md](Marcelo/Marcelo-Daily-Noche-2026-09-21.md) |
| Pablo | 0 / 54 | | | H2.S5.M3 (ruleset mínimo: un comando de Pablo, ver §2) | [Pablo-Daily-Noche-2026-09-21.md](Pablo/Pablo-Daily-Noche-2026-09-21.md) |

### Qué NO se puede escribir en este documento

- Un `PASS` sin comando y exit code pegados.
- «Listo», «funciona» o «implementado» sobre algo que no se ejecutó.
- Un porcentaje que no salga de `HECHO / total`.
- Un `BLOQUEADO` disfrazado de `PASS` porque «igual compila», ni un `BLOQUEADO` por un contrato
  ajeno que se podía simular.
- `READY` en `FINAL_REPORT.md` con un P0 sin evidencia.
- Datos reales de participantes, cuentas bancarias, documentos, OTP o tokens en cualquier salida pegada.
