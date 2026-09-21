# Plataforma: el borde que autentica y correlaciona, el outbox que no pierde eventos y la traza que permite diagnosticar

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Leo · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** plataforma: gateway, broker y observabilidad
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../../Daily-Dia-2026-09-20.md) · **Tu daily:** [Leo-Daily-Dia-2026-09-20.md](../Leo-Daily-Dia-2026-09-20.md)
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
| `api-gateway-bff` | Autenticación, correlación y rate limiting en el borde |
| `async-messaging-events` | Outbox y consumidores idempotentes |
| `distributed-tracing-correlation` | Reconstruir una operación por correlationId |
| `service-to-service-security` | Confianza cero entre servicios |
| `docker-local-stack` | Levantar los servicios necesarios, no los diez |
| `resilience-patterns` | Timeout, reintento y degradación declarada |
| `microservices-deployment` | Desplegar sin romper a los vecinos |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 90 · **98**

## 2. Resultado observable

Cualquier operación que cruza servicios se puede reconstruir con un solo `correlationId`, ningún evento se pierde aunque el broker esté caído al momento del commit, y el equipo puede levantar el stack local con un comando.

**Kill-test:** Matar el broker, hacer una operación, levantarlo y ver si el evento sale igual. Si se perdió, el outbox no está hecho.

## 3. Alcance

**IN:** Gateway (autenticación, correlación, rate limiting), librería compartida de outbox y relay, propagación de contexto en consumidores, `docker-compose` del stack local y el tablero mínimo de colas.

**OUT:** La lógica de negocio de cualquier servicio. El despliegue en producción. El BFF de cada cliente, que lo hará quien construya ese cliente.

**Reservas de archivos:** Gateway, librería de plataforma, `docker-compose.yml` y configuración del broker.

## 4. Plan

### H1 — El borde: autentica, correlaciona y limita — y nada más

**CA:** Dado un request sin `X-Correlation-Id`, cuando entra por el gateway, entonces se le asigna uno y ese mismo id aparece en los logs de todos los servicios que toca.
**DoD:** Traza y líneas de log de tres servicios con el mismo id, pegadas.
**Estado:** TODO

#### H1.S1 — Autenticación, correlación y cabeceras

**CA:** Dado un token inválido, cuando llega al gateway, entonces responde 401 sin llegar a ningún servicio.
**DoD:** `curl` con token inválido devolviendo 401 y el log del servicio vacío, pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Validar el token en el borde y propagarlo, sin inyectar identidad a secas | No se agrega ninguna cabecera X-User-Id creída | `grep -rn 'X-User-Id' gateway/` | TODO |
| H1.S1.M2 | Generar o propagar X-Correlation-Id y traceparent | El id llega al último servicio de la cadena | `npm test -- correlacion-e2e` | TODO |
| H1.S1.M3 | Log de borde estructurado y sin datos sensibles | La línea de log no tiene documentos, cuentas ni importes | `npm test -- log-borde` | TODO |

#### H1.S2 — Rate limiting y CORS

**CA:** Dado un exceso de pedidos a un endpoint sensible, cuando se supera el límite, entonces responde 429 con `Retry-After`.
**DoD:** Salida del 429 con su cabecera, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Rate limiting por IP y por identificador en login y emisión de QR | El 429 aparece exactamente en el límite configurado | `npm test -- rate-limit` | TODO |
| H1.S2.M2 | CORS con lista blanca, sin comodín con credenciales | La configuración no tiene asterisco | `npm test -- cors` | TODO |
| H1.S2.M3 | Health check del borde que no depende de todos los dependidos | Con un servicio secundario caído, el borde sigue sano | `docker compose stop notificaciones && curl -s localhost:8080/health` | TODO |

### H2 — Outbox: el evento no se pierde ni se duplica el efecto

**CA:** Dado el broker caído en el momento del commit, cuando vuelve, entonces el evento se publica igual y el consumidor produce el efecto una sola vez.
**DoD:** Salida del escenario completo con el broker apagado y reencendido, pegada.
**Estado:** TODO

#### H2.S1 — Tabla de outbox y relay

**CA:** Dado un cambio de negocio, cuando se hace commit, entonces la fila de outbox se escribió en la misma transacción.
**DoD:** `npm test -- outbox-atomico` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Tabla outbox con sobre completo: id, type, version, correlationId, occurredAt | El sobre tiene todos los campos obligatorios | `npm test -- sobre-evento` | TODO |
| H2.S1.M2 | Relay con SELECT FOR UPDATE SKIP LOCKED y marca de publicado | Dos relays en paralelo no publican el mismo mensaje | `npm test -- relay-concurrente` | TODO |
| H2.S1.M3 | Métrica y alerta de antigüedad del pendiente más viejo | La métrica existe y dispara al superar el umbral | `curl -s localhost:8080/metrics | grep outbox_lag` | TODO |

#### H2.S2 — Consumidores idempotentes y DLQ

**CA:** Dado el mismo mensaje entregado dos veces, cuando se procesa, entonces el efecto ocurre una sola vez.
**DoD:** `npm test -- consumidor-duplicado` en verde, con el conteo pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Helper de deduplicación transaccional por message_id | El segundo procesamiento no repite el efecto | `npm test -- consumidor-duplicado` | TODO |
| H2.S2.M2 | Reintentos con backoff y tope, y DLQ con dueño y alerta | El mensaje agotado va a DLQ y dispara alerta | `npm test -- dlq` | TODO |
| H2.S2.M3 | Reconstrucción de contexto (correlación, actor) desde el sobre | Los logs del consumidor llevan el correlationId original | `npm test -- contexto-consumidor` | TODO |

### H3 — Se puede diagnosticar y se puede levantar

**CA:** Dado un `correlationId`, cuando se corre el comando del runbook, entonces sale la historia completa de la operación en orden.
**DoD:** Salida del comando sobre un caso real, pegada.
**Estado:** TODO

#### H3.S1 — Traza distribuida y runbook

**CA:** Dada una operación que cruza tres servicios, cuando se busca su traza, entonces los tres aparecen en el mismo trace.
**DoD:** Captura o salida de la traza completa, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Instrumentar los saltos que importan, sin ruido y sin atributos sensibles | Ningún span lleva importes ni documentos | `npm test -- spans-sin-datos` | TODO |
| H3.S1.M2 | Muestreo: 100 % en errores y caminos de dinero, decidido en el borde | La política está en configuración y se propaga | `npm test -- muestreo` | TODO |
| H3.S1.M3 | Escribir el comando de reconstrucción en el runbook y probarlo | El comando devuelve la historia ordenada | `bash runbook/reconstruir.sh <correlationId>` | TODO |

#### H3.S2 — Stack local reproducible

**CA:** Dado un clon limpio, cuando se corre un comando, entonces el equipo tiene los servicios necesarios arriba y sanos.
**DoD:** Salida de `docker compose ps` con todos los servicios sanos, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | docker-compose con los servicios, su base y el broker, con healthchecks | docker compose up deja todo sano | `docker compose up -d && docker compose ps` | TODO |
| H3.S2.M2 | Perfiles para levantar solo lo necesario, no los diez servicios | Se puede levantar pagos sin notificaciones | `docker compose --profile pagos up -d` | TODO |
| H3.S2.M3 | Documentar el comando y el tiempo que tarda en el README de plataforma | El README lo dice y coincide con lo medido | `time docker compose up -d` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00.1.7).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-L1 | ¿El broker va a ser Redis/BullMQ o un broker con tópicos? | **Coordinación / arquitectura** — `DECISION_REQUIRED` | El diseño del relay y de la DLQ | Se implementa contra una interfaz propia y se simula el contrato; no se acopla al broker |
| Q-L2 | ¿Autenticación entre servicios con mTLS o con token de servicio? | Coordinación | `service-to-service-security` | Se implementa token de servicio con alcance, dejando el punto de extensión para mTLS |

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
