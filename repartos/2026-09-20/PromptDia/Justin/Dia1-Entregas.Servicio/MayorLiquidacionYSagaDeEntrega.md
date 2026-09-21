# Entregas: el mayor que no se edita, la liquidación que se explica línea por línea y la saga que no paga dos veces

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Justin · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `entregas` (M4) + `contabilidad` (M3)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../../Daily-Dia-2026-09-20.md) · **Tu daily:** [Justin-Daily-Dia-2026-09-20.md](../Justin-Daily-Dia-2026-09-20.md)
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
| `accounting-double-entry` | Asientos balanceados y mayor inmutable |
| `disbursement-payouts` | Liquidación, enfriamiento y orden única |
| `money-movement-safety` | Las cinco evidencias de la regla 91.6 |
| `saga-distributed-transactions` | Compensaciones y punto de no retorno |
| `distributed-data-integrity` | Que los números cuadren entre servicios |
| `microservices-testing` | Duplicado, dependido caído y contrato |
| `concurrency-and-locking` | La carrera por el último cupo |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **91** · **98**

## 2. Resultado observable

Se liquida la entrega de un turno: la bolsa bruta sale del mayor, cada deducción tiene su línea con el registro que la respalda, y la orden de desembolso se emite una sola vez aunque el paso se reintente.

**Kill-test:** Disparar la misma liquidación dos veces en paralelo y contar las órdenes de desembolso. Si hay dos, no está hecho.

## 3. Alcance

**IN:** Servicio `contabilidad`: plan de cuentas, `asiento_contable`, `movimiento_contable` y la invariante en base. Servicio `entregas`: `entrega_fondo`, `deduccion_entrega`, `orden_desembolso` y la saga de liquidación.

**OUT:** El proveedor real de transferencias: se trabaja contra un stub. El cálculo de deuda, que es de `garantia`: también se simula (regla 65). La UI.

**Reservas de archivos:** Los esquemas de `contabilidad` y de `entregas`.

## 4. Plan

### H1 — El mayor: partida doble con la invariante en la base

**CA:** Dado un asiento desbalanceado, cuando se intenta persistir, entonces lo rechaza la base, no el servicio.
**DoD:** Salida del INSERT rechazado por la constraint, pegada.
**Estado:** TODO

#### H1.S1 — Plan de cuentas y asientos

**CA:** Dado un asiento con dos líneas que no suman igual, cuando se hace commit, entonces falla.
**DoD:** `npm test -- asiento-balanceado` en verde y el error de base pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Crear `cuenta_contable` con naturaleza, más `asiento_contable` y `movimiento_contable` | Un asiento nace completo o no nace | `npm test -- asiento-completo` | TODO |
| H1.S1.M2 | Constraint diferida o trigger que verifica SUM(debe) = SUM(haber) | El INSERT desbalanceado falla en el commit | `psql -c 'begin; insert ...; commit;'` | TODO |
| H1.S1.M3 | Importes DECIMAL(14,2) con moneda y un único modo de redondeo | No hay float en ninguna capa | `grep -rniE 'float|double precision' migrations/` | TODO |

#### H1.S2 — Inmutabilidad y corrección por contra-asiento

**CA:** Dado un asiento existente, cuando se intenta actualizarlo, entonces la base lo impide por permisos.
**DoD:** Salida del UPDATE rechazado por permisos, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Revocar UPDATE y DELETE sobre las tablas del mayor en el rol de la aplicación | El UPDATE falla con error de permiso | `psql -c 'update asiento_contable set monto = 1;'` | TODO |
| H1.S2.M2 | Implementar la reversa como contra-asiento que referencia al original | El original queda visible y la suma neta es cero | `npm test -- contra-asiento` | TODO |
| H1.S2.M3 | Consulta de cuadre por periodo | La consulta devuelve diferencia cero | `npm run contabilidad:cuadre -- <periodo>` | TODO |

### H2 — La liquidación se explica línea por línea

**CA:** Dada una entrega con deuda propia y reposición de cobertura, cuando se liquida, entonces el neto se explica con una línea por deducción y su registro de origen.
**DoD:** Liquidación completa pegada: bruta, cada deducción con su origen, neto y asientos cuadrados.
**Estado:** TODO

#### H2.S1 — Bolsa bruta desde el mayor y congelamiento

**CA:** Dado un pago que entra mientras se liquida, cuando la bolsa ya se calculó, entonces el neto no cambia a mitad del proceso.
**DoD:** `npm test -- liquidacion-congelada` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Calcular la bolsa bruta desde el mayor, no desde la tabla de pagos | La consulta lee movimiento_contable | `npm test -- bolsa-desde-mayor` | TODO |
| H2.S1.M2 | Congelar el cálculo al iniciar la liquidación | Un pago posterior no altera esta entrega | `npm test -- liquidacion-congelada` | TODO |
| H2.S1.M3 | Invariante en base: la suma de deducciones no supera la bruta | El caso que la supera se rechaza | `npm test -- deducciones-tope` | TODO |

#### H2.S2 — Validaciones previas obligatorias

**CA:** Dada una cuenta bancaria cambiada hace una hora, cuando se intenta desembolsar, entonces se rechaza por el periodo de enfriamiento.
**DoD:** Salida del rechazo con su motivo, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Implementar `validacion_pre_entrega` con sus siete verificaciones y su registro | Una que falla detiene la entrega, no se continúa | `npm test -- validaciones-previas` | TODO |
| H2.S2.M2 | Periodo de enfriamiento tras cambio de cuenta, no saltable por soporte | No existe parámetro que lo omita | `grep -rniE 'skipCooldown|forzarDesembolso' src/` | TODO |
| H2.S2.M3 | Notificación del cambio de cuenta por un canal distinto | El registro del envío existe | `npm test -- aviso-cambio-cuenta` | TODO |

### H3 — La saga: compensa antes del punto de no retorno

**CA:** Dado un fallo al asentar la liquidación, cuando la saga compensa, entonces las deducciones reservadas se liberan y no queda nada a medio camino.
**DoD:** Un test por paso fallando, con el estado final consistente, pegados.
**Estado:** TODO

#### H3.S1 — Estado persistido y compensaciones

**CA:** Dado el orquestador muerto entre guardar el estado y disparar el paso, cuando reinicia, entonces retoma sin duplicar.
**DoD:** `npm test -- saga-reinicio` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Persistir el estado de la saga antes de disparar cada paso, con timeout | El estado está en base, no en memoria del worker | `npm test -- saga-estado` | TODO |
| H3.S1.M2 | Una compensación idempotente por paso, hasta el punto de no retorno | Compensar dos veces deja el mismo resultado | `npm test -- saga-compensa` | TODO |
| H3.S1.M3 | Estado terminal FALLIDA_REQUIERE_HUMANO con alerta y dueño | El caso queda visible y con responsable | `npm test -- saga-escala` | TODO |

#### H3.S2 — Idempotencia del desembolso y prueba de caída

**CA:** Dada la misma liquidación disparada dos veces en paralelo, cuando terminan, entonces existe una sola orden de desembolso.
**DoD:** Salida de las dos peticiones en paralelo y el conteo en 1, pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Orden de desembolso única por entrega, con la clave propagada al proveedor | Dos peticiones en paralelo producen una sola orden | `npm test -- desembolso-idempotente` | TODO |
| H3.S2.M2 | Timeout del proveedor tratado como estado desconocido: se consulta, no se reintenta | No hay reintento ciego en el código | `npm test -- desembolso-timeout` | TODO |
| H3.S2.M3 | Prueba con el stub de garantia apagado | La saga compensa y el sistema queda consistente | `docker compose stop stub-garantia && npm test -- saga-dependido-caido` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00.1.7).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-J1 | ¿Cuál es el orden de imputación de un abono: primero cargos o primero capital? | Negocio / contabilidad | El cálculo de deducciones y de recuperación | Se implementa configurable y se declara el valor usado en las pruebas |
| Q-J2 | ¿Qué proveedor de transferencias se va a usar y soporta clave de idempotencia? | Coordinación | El diseño del reintento del desembolso | Se asume que NO la soporta: sin reintento automático, consulta de estado y escalado |

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
