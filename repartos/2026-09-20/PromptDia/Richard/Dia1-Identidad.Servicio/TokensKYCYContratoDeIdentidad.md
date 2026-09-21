# Identidad: tokens que no se filtran, documento único y niveles que el servidor hace cumplir

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Richard · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `identidad` (M1)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../../Daily-Dia-2026-09-20.md) · **Tu daily:** [Richard-Daily-Dia-2026-09-20.md](../Richard-Daily-Dia-2026-09-20.md)
- **3 hitos · 6 subtareas · 18 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar dentro del repo en el que vas a trabajar.
2. Entrá por `skills-router` y cargá **solo** las skills que tu trabajo necesita. No leas el
   catálogo entero: no sirve.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre; no leas el catálogo entero.

| Skill | Para qué en este encargo |
|---|---|
| `kyc-identity-verification` | Niveles, documento único, estados del expediente |
| `authn-identity` | Tokens, OTP, sesión y no enumeración |
| `authz-access-control` | Que el servicio autorice por su cuenta |
| `data-privacy-financial` | Qué no puede aparecer en logs, URLs ni eventos |
| `terminology-value-sets` | Catálogo cerrado de tipos de documento y motivos |
| `service-contracts-versioning` | Publicar el contrato y su pacto |
| `service-to-service-security` | Confianza cero entre servicios |
| `api-testing` | Matriz de autorización negativa |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 90 · 98

## 2. Resultado observable

Una persona se registra, verifica su teléfono y su documento, y el servicio deja constancia de en qué nivel quedó; los demás servicios pueden preguntarle ese nivel por contrato, y ninguna de esas operaciones deja el valor plano de un token en la base ni en un log.

**Kill-test:** Buscar en la base y en los logs el valor plano de un OTP recién emitido. Si aparece, no está hecho.

## 3. Alcance

**IN:** Servicio `identidad`: `token_verificacion` y su política, `documento_identidad`, `verificacion_kyc`, los niveles de verificación y el endpoint interno que expone el nivel.

**OUT:** Cualquier otro servicio. La UI. El proveedor real de verificación biométrica, que se simula (regla 65). El cribado de listas, que es otro encargo.

**Reservas de archivos:** Todo bajo el servicio `identidad` y su esquema de base.

## 4. Plan

### H1 — Tokens de verificación que nunca guardan el valor plano

**CA:** Dado un OTP emitido, cuando se consulta la base y los logs, entonces solo aparece su hash y nunca el valor plano.
**DoD:** `npm test -- tokens` en verde, más el `grep` sobre base y logs con salida vacía, pegados en `evidencia/`.
**Estado:** TODO

#### H1.S1 — Modelo y política de token por propósito

**CA:** Dado un propósito con política de 5 minutos y 3 intentos, cuando se emite un token, entonces hereda esos valores sin que estén hardcodeados.
**DoD:** `npm test -- politica-token` en verde, con la política leída de base.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Crear `politica_token` con vigencia, intentos máximos y backoff de reenvío, por propósito | La política se lee de base, no de constantes en código | `npm test -- politica-token` | TODO |
| H1.S1.M2 | Persistir solo el hash con pepper en `token_verificacion` | No existe columna para el valor plano | `psql -c '\d token_verificacion'` | TODO |
| H1.S1.M3 | Registrar cada intento en `intento_validacion_token` | Tres intentos fallidos quedan registrados y el cuarto se rechaza | `npm test -- fuerza-bruta-token` | TODO |

#### H1.S2 — Emisión, validación y no enumeración

**CA:** Dado un teléfono registrado y uno que no, cuando se pide un código, entonces las dos respuestas son indistinguibles.
**DoD:** `npm test -- no-enumeracion` en verde, con las dos respuestas pegadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Endpoint de emisión con respuesta idéntica exista o no el teléfono | Mismo código HTTP, mismo cuerpo y tiempo comparable | `npm test -- no-enumeracion` | TODO |
| H1.S2.M2 | Validación que consume el token de un solo uso | Reusar el token devuelve el mismo error que uno inválido | `npm test -- token-un-solo-uso` | TODO |
| H1.S2.M3 | Verificar que ningún log contiene el valor del token | El grep sobre los logs del test sale vacío | `npm test -- tokens && grep -r "$OTP" logs/` | TODO |

### H2 — Documento único y niveles que el servidor hace cumplir

**CA:** Dado un documento ya registrado, cuando otra cuenta intenta usarlo con otro formato, entonces el alta se rechaza o se deriva a revisión.
**DoD:** `npm test -- documento-unico` y `npm test -- niveles` en verde, con salidas pegadas.
**Estado:** TODO

#### H2.S1 — Normalización y unicidad del documento

**CA:** Dados `1234567 LP` y `1234567-LP` en cuentas distintas, cuando se registran, entonces el sistema los reconoce como el mismo documento.
**DoD:** `npm test -- documento-unico` en verde, incluidos los casos con complemento.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Función de normalización con su catálogo de tipos de documento | Los tres formatos de prueba normalizan al mismo valor | `npm test -- normalizacion-documento` | TODO |
| H2.S1.M2 | Índice UNIQUE sobre la forma normalizada | El segundo insert viola la constraint | `npm test -- documento-unico` | TODO |
| H2.S1.M3 | La coincidencia de documento abre revisión en vez de bloquear | El caso queda en REVISION_MANUAL con su motivo | `npm test -- duplicado-revision` | TODO |

#### H2.S2 — Niveles atados a acciones, verificados en el servidor

**CA:** Dado un usuario en nivel 1, cuando intenta tomar un cupo, entonces recibe 403 con un motivo accionable.
**DoD:** `npm test -- niveles` en verde, con el 403 y su cuerpo pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Definir los cuatro niveles y qué habilita cada uno, como configuración versionada | El mapa nivel→acción se lee de configuración | `npm test -- mapa-niveles` | TODO |
| H2.S2.M2 | Guard que resuelve el nivel en cada acción protegida | Llamada directa al endpoint con nivel insuficiente devuelve 403 | `npm test -- niveles` | TODO |
| H2.S2.M3 | Motivo accionable en la respuesta, sin exponer criterios antifraude | El cuerpo dice qué falta, no por qué se sospecha | `npm test -- motivo-accionable` | TODO |

### H3 — El contrato que los demás servicios consumen

**CA:** Dado otro servicio que necesita el nivel de un usuario, cuando lo pide por contrato, entonces obtiene el nivel y nada más que el nivel.
**DoD:** Pacto publicado, test de contrato en verde y la prueba de salteo del gateway en 403, con salidas pegadas.
**Estado:** TODO

#### H3.S1 — Contrato mínimo y su pacto

**CA:** Dado el contrato publicado, cuando el consumidor corre su pacto, entonces el productor lo cumple.
**DoD:** El job de pactos en verde, salida pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Definir la operación `nivelDe(usuarioId)` con payload mínimo | El payload no incluye documento, teléfono ni nombre | `npm test -- contrato-nivel` | TODO |
| H3.S1.M2 | Publicar el esquema en `contratos/` y el pacto del consumidor | El archivo existe y el CI lo lee | `npm run contratos:check` | TODO |
| H3.S1.M3 | Test de contrato corriendo en el CI del productor | El job falla si se rompe el pacto | `npm run test:pactos` | TODO |

#### H3.S2 — Confianza cero: el servicio autoriza por su cuenta

**CA:** Dado un pedido que entra por la red interna salteando el gateway, cuando trae el token de otro usuario, entonces el servicio responde 403.
**DoD:** Salida del `curl` directo al puerto interno con 401 y 403, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Validar firma, emisor, audiencia y alcance del token en el servicio | Un token con `aud` de otro servicio se rechaza | `npm test -- token-audiencia` | TODO |
| H3.S2.M2 | Prueba de salteo del gateway | Sin token devuelve 401; con token ajeno devuelve 403 | `curl -s -o /dev/null -w '%{http_code}' localhost:3001/interno/nivel/...` | TODO |
| H3.S2.M3 | Verificar permisos de base del servicio | El usuario de identidad no tiene SELECT sobre otros esquemas | `psql -c 'select * from information_schema.role_table_grants ...'` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00.1.7).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-R1 | ¿Qué proveedor de verificación biométrica se va a usar y qué devuelve exactamente? | Negocio / coordinación | El nivel 2 real | Se asume el contrato `{ aprobado, puntaje, motivo }` y se simula en tres niveles (regla 65) |
| Q-R2 | ¿Cuánto dura un KYC antes de exigir revalidación? | Cumplimiento | El vencimiento automático de nivel | Queda configurable, sin valor por defecto en código |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, en `A MEDIAS` con las cuatro respuestas, o en
      `BLOQUEADO` con evidencia — y solo si el bloqueo no se puede simular (regla 65).
- [ ] `PLAN.md` y `REPORTE.md` escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin datos reales de participantes (regla 90.2).
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `money-movement-safety`
      si toca importes (las cinco evidencias de la regla 91.6); `microservices-testing` si
      cruza servicios (duplicado, dependido caído, contrato); `data-privacy-financial` si
      toca datos de personas.
- [ ] Peldaño de evidencia declarado (regla 30).
