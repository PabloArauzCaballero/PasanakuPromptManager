# Pagos: la cadena obligación → orden → QR → pago, y un webhook que no acredita dos veces ni acredita de más

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Marcelo · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `pagos` (M3)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../../Daily-Dia-2026-09-20.md) · **Tu daily:** [Marcelo-Daily-Dia-2026-09-20.md](../Marcelo-Daily-Dia-2026-09-20.md)
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
| `payments-qr-integration` | Orden, QR, webhook y reconsulta |
| `money-movement-safety` | Las cinco evidencias de la regla 91.6 |
| `service-to-service-security` | Confianza cero entre servicios |
| `async-messaging-events` | Outbox y consumidores idempotentes |
| `payment-reconciliation` | Excepciones cuando el monto no coincide |
| `resilience-patterns` | Timeout, reintento y degradación declarada |
| `microservices-testing` | Duplicado, dependido caído y contrato |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **91** · **98**

## 2. Resultado observable

Un participante paga su aporte escaneando un QR y el sistema lo acredita exactamente una vez, aunque la pasarela mande el webhook tres veces, publicando el evento por outbox en la misma unidad de trabajo.

**Kill-test:** Mandar el mismo webhook dos veces y contar pagos y mensajes de outbox. Si hay más de uno de cada uno, no está hecho.

## 3. Alcance

**IN:** Servicio `pagos`: `obligacion_aporte`, `orden_cobro`, `qr_cobro`, `intento_pago`, `pago`, `webhook_pasarela` y el evento `aporte.acreditado` publicado por outbox.

**OUT:** El mayor contable, que es de `contabilidad`: acá solo se publica el evento. La conciliación bancaria completa. El proveedor real: se trabaja contra un stub de su contrato (regla 65).

**Reservas de archivos:** Todo bajo el servicio `pagos` y su esquema; el stub del proveedor vive en ese repo.

## 4. Plan

### H1 — La cadena completa, sin eslabones salteados

**CA:** Dada una obligación vigente, cuando se pide cobrarla, entonces existe una orden con su clave de idempotencia y un QR atado a esa orden por monto y vigencia.
**DoD:** `npm test -- cadena-cobro` en verde, con las filas creadas pegadas.
**Estado:** TODO

#### H1.S1 — Obligación y orden de cobro

**CA:** Dada la misma intención de cobro pedida dos veces, cuando se crean las órdenes, entonces hay una sola.
**DoD:** `npm test -- orden-idempotente` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Modelar `orden_cobro` con `clave_idempotencia` y su índice UNIQUE | La segunda creación devuelve la orden existente, no una nueva | `npm test -- orden-idempotente` | TODO |
| H1.S1.M2 | Importe en DECIMAL(14,2) con moneda, sin float en ninguna capa | El DTO serializa el monto como string decimal | `grep -rniE 'parseFloat|Number\(' src/ | grep -i monto` | TODO |
| H1.S1.M3 | Rechazar orden sobre una obligación ya cumplida | Respuesta 409 con el motivo | `npm test -- orden-obligacion-cumplida` | TODO |

#### H1.S2 — QR e intentos de pago

**CA:** Dado un QR vencido, cuando se intenta pagar con él, entonces no acredita y se ofrece reemitir.
**DoD:** `npm test -- qr-vigencia` en verde, con el rechazo pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Generar `qr_cobro` con monto atado a la orden y vigencia explícita | Un QR de otra orden no sirve para esta | `npm test -- qr-atado` | TODO |
| H1.S2.M2 | Reemitir genera un intento nuevo sin pisar el anterior | Quedan los dos intentos en la base | `npm test -- qr-reemision` | TODO |
| H1.S2.M3 | No persistir ni loguear el payload del QR | El grep sobre logs y base sale vacío | `npm test -- cadena-cobro && grep -r "$QR_PAYLOAD" logs/` | TODO |

### H2 — El webhook: la única fuente de acreditación

**CA:** Dado el mismo evento del proveedor entregado tres veces, cuando se procesa, entonces existe un solo pago y un solo evento publicado.
**DoD:** `npm test -- webhook` en verde, con el conteo de pagos y de mensajes de outbox pegado.
**Estado:** TODO

#### H2.S1 — Firma, ventana temporal y registro crudo

**CA:** Dado un webhook con firma inválida, cuando llega, entonces responde 401 y no toca ninguna tabla de negocio.
**DoD:** `npm test -- webhook-firma` en verde, con la respuesta y el conteo en cero pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Verificar la firma con comparación de tiempo constante | Firma inválida devuelve 401 y no produce efecto | `npm test -- webhook-firma` | TODO |
| H2.S1.M2 | Ventana temporal sobre el timestamp firmado | Un reenvío viejo se rechaza | `npm test -- webhook-replay` | TODO |
| H2.S1.M3 | Registrar el webhook crudo sin loguear el cuerpo | La fila existe y el log no contiene el cuerpo | `npm test -- webhook-crudo` | TODO |

#### H2.S2 — Idempotencia y validación contra la orden

**CA:** Dado un webhook cuyo monto no coincide con el de la orden, cuando se procesa, entonces no acredita y abre una excepción de conciliación.
**DoD:** `npm test -- webhook-monto` en verde, con la excepción creada pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Deduplicar por el id del evento del proveedor con índice UNIQUE | El segundo procesamiento no crea un segundo pago | `npm test -- webhook-duplicado` | TODO |
| H2.S2.M2 | Validar monto y moneda contra la orden antes de acreditar | La discrepancia abre excepcion_conciliacion en vez de acreditar | `npm test -- webhook-monto` | TODO |
| H2.S2.M3 | Publicar `aporte.acreditado` por outbox en la misma transacción | El mensaje existe y es uno solo | `npm test -- outbox-aporte` | TODO |

### H3 — Cuando el proveedor no responde

**CA:** Dado un intento de pago pendiente hace más de N minutos, cuando corre la reconsulta, entonces el estado se resuelve sin duplicar el efecto.
**DoD:** `npm test -- reconsulta` en verde y la prueba con el stub apagado, pegadas.
**Estado:** TODO

#### H3.S1 — Reconsulta de estado

**CA:** Dado que el webhook nunca llegó, cuando la reconsulta encuentra el pago confirmado, entonces acredita una sola vez.
**DoD:** `npm test -- reconsulta` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Job idempotente que busca intentos pendientes y consulta al proveedor | Correrlo dos veces no duplica | `npm test -- reconsulta` | TODO |
| H3.S1.M2 | Convivencia con el webhook tardío | Si llega después, no acredita de nuevo | `npm test -- reconsulta-y-webhook` | TODO |
| H3.S1.M3 | Backoff, tope y escalado a revisión manual con alerta | El caso agotado queda visible, no perdido | `npm test -- reconsulta-agotada` | TODO |

#### H3.S2 — Resiliencia ante el dependido caído

**CA:** Dado el proveedor apagado, cuando se pide emitir un QR, entonces la respuesta corta en el timeout y no cuelga.
**DoD:** Salida del `curl` con el stub apagado, con código y tiempo, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Timeout explícito en toda llamada al proveedor | La llamada corta en el timeout, no a los 30 s | `docker compose stop stub-pasarela && curl -w '%{time_total}' ...` | TODO |
| H3.S2.M2 | Sin reintento automático de cobro sin clave de idempotencia | El código no reintenta esa operación | `npm test -- sin-reintento-cobro` | TODO |
| H3.S2.M3 | Degradación declarada y mensaje honesto al cliente | No se inventa ningún estado de pago | `npm test -- degradacion-pagos` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00.1.7).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-M1 | ¿Se aceptan QR de monto abierto o siempre monto fijo atado a la orden? | Negocio | El tratamiento de sobrantes y faltantes | Se implementa solo monto fijo; el monto abierto queda fuera de alcance y se registra |
| Q-M2 | ¿A partir de qué monto hay que reconsultar el estado antes de acreditar? | Negocio / cumplimiento | El control de `payments-qr-integration` §4.5 | Configurable, sin valor por defecto en código |

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
