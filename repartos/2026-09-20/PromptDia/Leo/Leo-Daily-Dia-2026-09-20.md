# Daily de Leo — turno día — 2026-09-20

> **AVANCE: 0 / 18 — 0 %.**
> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Leo · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** plataforma: gateway, broker y observabilidad
- **Tu encargo:** [Plataforma: el borde que autentica y correlaciona, el outbox que no pierde eventos y la traza que permite diagnosticar](Dia1-Plataforma.Infra/GatewayOutboxYTrazaDistribuida.md)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../Daily-Dia-2026-09-20.md)
- **3 hitos · 6 subtareas · 18 microtareas**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → pegar salida abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → pegar salida abajo.
- [ ] Skills cargadas: `api-gateway-bff` · `async-messaging-events` · `distributed-tracing-correlation` · `service-to-service-security` · `docker-local-stack` · `resilience-patterns` · `microservices-deployment`

```text
$ ls .claude/skills | wc -l
<pegar>
$ python .claude/hooks/plan_gate.py --self-test
<pegar>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| **H1** — El borde: autentica, correlaciona y limita — y nada más | 6 | 0 | `TODO` |
| **H2** — Outbox: el evento no se pierde ni se duplica el efecto | 6 | 0 | `TODO` |
| **H3** — Se puede diagnosticar y se puede levantar | 6 | 0 | `TODO` |
| **TOTAL** | **18** | **0** | **0 / 18 = 0 %** |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| | | | |

## 4. A medias — las cuatro respuestas, obligatorias

Ninguna todavía. **No borrar esta sección:** su ausencia se lee como que no hubo nada que decir.

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|
| | | | | |

> Regla 65: si el contrato de lo que falta se puede nombrar, **se simula en tres niveles
> —correcto, límite, inválido— y se cierra contra el doble**, declarándolo. Solo una decisión de
> negocio o una acción destructiva sobre algo compartido justifican dejarlo abierto.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|
| | | | |

## 7. No cubierto

Lo que se hizo pero **no** se probó. Distinto de pendiente.

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-L1 | ¿El broker va a ser Redis/BullMQ o un broker con tópicos? | **Coordinación / arquitectura** — `DECISION_REQUIRED` | `ABIERTA` |
| Q-L2 | ¿Autenticación entre servicios con mTLS o con token de servicio? | Coordinación | `ABIERTA` |
