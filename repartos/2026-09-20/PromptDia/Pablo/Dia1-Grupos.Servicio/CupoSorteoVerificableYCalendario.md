# Grupos: el cupo como posición económica, el sorteo que cualquiera puede recomputar y el calendario que no miente

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Pablo · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `grupos` (M2)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../../Daily-Dia-2026-09-20.md) · **Tu daily:** [Pablo-Daily-Dia-2026-09-20.md](../Pablo-Daily-Dia-2026-09-20.md)
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
| `rosca-group-lifecycle` | Cupo, reglamento, acuerdos y sorteo verificable |
| `contribution-calendar` | Periodos, vencimientos y días no hábiles |
| `state-machines-workflows` | Transiciones con precondición en el servidor |
| `concurrency-and-locking` | La carrera por el último cupo |
| `audit-trail-history` | Bitácora append-only del sorteo y los estados |
| `microservices-architecture` | De quién es cada dato |
| `terminology-value-sets` | Catálogo cerrado de tipos de documento y motivos |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **91** · **98**

## 2. Resultado observable

Un grupo pasa a `EN_CURSO` con su sorteo publicado y su calendario generado; cualquier participante puede recomputar el orden de cobro desde la semilla revelada y obtener exactamente el mismo resultado.

**Kill-test:** Correr la herramienta de verificación del sorteo con la semilla publicada. Si el orden que sale no es idéntico al del sistema, no está hecho.

## 3. Alcance

**IN:** Servicio `grupos`: `cupo`, `participante`, `sorteo_turnos`, `turno`, `periodo`, `dia_no_habil`, las transiciones de estado del grupo y la herramienta de verificación del sorteo.

**OUT:** Cobros y pagos (son de `pagos`). Mora y sanciones (son de `garantia`). La UI. El emparejamiento automático.

**Reservas de archivos:** Todo bajo el servicio `grupos` y su esquema.

## 4. Plan

### H1 — El cupo es la posición económica, no la persona

**CA:** Dado un cupo con obligaciones y turno asignado, cuando se traspasa a otro participante, entonces el turno y las obligaciones no se mueven.
**DoD:** `npm test -- traspaso-cupo` en verde, con el calendario antes y después pegado.
**Estado:** TODO

#### H1.S1 — Modelo cupo / participante

**CA:** Dada una persona con dos manos, cuando se consultan sus obligaciones, entonces hay dos cupos independientes.
**DoD:** `npm test -- cupos-multiples` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Modelar `cupo` con FK a participante y a grupo, con monto propio | Media mano es un cupo con monto distinto, no un caso especial | `npm test -- cupos-multiples` | TODO |
| H1.S1.M2 | Colgar turno y obligaciones del cupo, no del participante | El esquema no tiene FK de obligación a participante | `psql -c '\d obligacion_aporte'` | TODO |
| H1.S1.M3 | Traspaso de cupo que conserva la posición | El turno del cupo es el mismo antes y después | `npm test -- traspaso-cupo` | TODO |

#### H1.S2 — Transiciones de estado del grupo con precondiciones

**CA:** Dado un grupo sin todos los cupos llenos, cuando se intenta pasarlo a `CONFORMADO`, entonces se rechaza con el motivo.
**DoD:** `npm test -- transiciones-grupo` en verde, con el rechazo pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Implementar la máquina de estados con precondiciones en el servidor | No existe endpoint que setee el estado directamente | `grep -rn 'estado =' src/controllers/` | TODO |
| H1.S2.M2 | Historial append-only con actor y motivo | El historial no admite UPDATE | `psql -c 'update historial_estado_grupo ...'` | TODO |
| H1.S2.M3 | Rechazo de CONFORMADO sin reglamento aceptado por todos | Respuesta 409 con el motivo | `npm test -- transiciones-grupo` | TODO |

### H2 — Sorteo verificable: commit, reveal y recomputo

**CA:** Dado el hash publicado antes del sorteo y la semilla revelada después, cuando un tercero recomputa el orden, entonces obtiene exactamente el mismo resultado.
**DoD:** Salida de la herramienta de verificación coincidiendo con el orden del sistema, pegada.
**Estado:** TODO

#### H2.S1 — Commit y reveal

**CA:** Dado un sorteo por hacer, cuando se publica el commit, entonces la semilla todavía no la conoce nadie, incluido el organizador.
**DoD:** `npm test -- sorteo-commit` en verde y el registro en bitácora, pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Generar la semilla con un generador criptográficamente seguro | La semilla no es derivable de datos del grupo | `npm test -- semilla` | TODO |
| H2.S1.M2 | Publicar hash(semilla) y la lista congelada de cupos antes de sortear | El commit tiene timestamp anterior al sorteo | `npm test -- sorteo-commit` | TODO |
| H2.S1.M3 | Revelar la semilla sin poder pisar el sorteo | Un segundo sorteo exige acuerdo y deja los dos registros | `npm test -- sorteo-inmutable` | TODO |

#### H2.S2 — Función determinista y herramienta de verificación

**CA:** Dada la misma semilla y la misma lista, cuando se recomputa el orden mil veces, entonces sale siempre el mismo.
**DoD:** `npm run sorteo:verificar` con salida OK y el orden idéntico, pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Función de ordenamiento determinista y documentada | Mil corridas dan el mismo orden | `npm test -- sorteo-determinista` | TODO |
| H2.S2.M2 | Herramienta de verificación ejecutable por cualquiera | Corre solo con los datos públicos, sin acceso a producción | `npm run sorteo:verificar -- <grupo>` | TODO |
| H2.S2.M3 | Publicar commit, semilla y orden en el bloque de transparencia | Los tres datos son consultables por el endpoint público | `curl -s localhost:3002/publico/grupos/<id>/sorteo` | TODO |

### H3 — Calendario determinista y vencimientos que no se equivocan de día

**CA:** Dado un grupo en UTC−4 con vencimiento el día 10, cuando son las 23:59 del 10 hora local, entonces la obligación todavía no está vencida.
**DoD:** `npm test -- vencimientos` en verde, con los casos de borde pegados.
**Estado:** TODO

#### H3.S1 — Generación del calendario

**CA:** Dadas las mismas entradas, cuando se genera el calendario dos veces, entonces las dos salidas son idénticas.
**DoD:** `diff` de las dos generaciones vacío, pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Generar periodos y turnos desde el reglamento y el sorteo | Cantidad de periodos igual a cantidad de cupos, sin huecos ni solapamientos | `npm test -- calendario-invariantes` | TODO |
| H3.S1.M2 | Verificar el determinismo de la generación | El diff de dos generaciones es vacío | `npm run calendario:generar -- --dry-run | diff - esperado.txt` | TODO |
| H3.S1.M3 | Cargar `dia_no_habil` como catálogo con política de corrimiento | El feriado mueve el vencimiento según la política declarada | `npm test -- dias-no-habiles` | TODO |

#### H3.S2 — Vencimientos con zona horaria y casos de borde

**CA:** Dado el 31 de enero en un grupo mensual, cuando se calcula el vencimiento de febrero, entonces cae en el último día del mes y no falla.
**DoD:** `npm test -- vencimientos-borde` en verde, con los cuatro casos pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Función única de vencimiento con la zona del grupo | No hay `new Date()` comparado contra un vencimiento en ningún lado | `grep -rn 'new Date()' src/ | grep -i vence` | TODO |
| H3.S2.M2 | Tests de borde: fin de mes, bisiesto, día 31 y feriado | Los cuatro casos pasan | `npm test -- vencimientos-borde` | TODO |
| H3.S2.M3 | Job de mora idempotente, una vez por día por grupo | Correrlo dos veces no duplica efectos | `npm run job:mora && npm run job:mora && npm test -- mora-idempotente` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00.1.7).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-P1 | Si falta plata para la entrega de un periodo, ¿cubre el fondo, se prorratea o se posterga? | **Negocio** — `DECISION_REQUIRED` | La rama del calendario ante impago del grupo | No se implementa ninguna rama: se deja el punto de extensión y se registra |
| Q-P2 | ¿El quórum para aprobar una permuta sale del reglamento o hay un mínimo de plataforma? | Negocio | La validación de acuerdos | Se lee del reglamento, sin mínimo hardcodeado |

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
