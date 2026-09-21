# Daily de Marcelo — turno día — 2026-09-20

> **AVANCE: 0 / 18 — 0 %.**
> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno: nadie ejecutó nada todavía.

- **Persona:** Marcelo · **Turno:** día · **Fecha:** 2026-09-20 · **Servicio:** `pagos` (M3)
- **Tu encargo:** [Pagos: la cadena obligación → orden → QR → pago, y un webhook que no acredita dos veces ni acredita de más](Dia1-Pagos.Servicio/OrdenQRWebhookIdempotente.md)
- **Daily del equipo:** [Daily-Dia-2026-09-20.md](../Daily-Dia-2026-09-20.md)
- **3 hitos · 6 subtareas · 18 microtareas**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → pegar salida abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → pegar salida abajo.
- [ ] Skills cargadas: `payments-qr-integration` · `money-movement-safety` · `service-to-service-security` · `async-messaging-events` · `payment-reconciliation` · `resilience-patterns` · `microservices-testing`

```text
$ ls .claude/skills | wc -l
<pegar>
$ python .claude/hooks/plan_gate.py --self-test
<pegar>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| **H1** — La cadena completa, sin eslabones salteados | 6 | 0 | `TODO` |
| **H2** — El webhook: la única fuente de acreditación | 6 | 0 | `TODO` |
| **H3** — Cuando el proveedor no responde | 6 | 0 | `TODO` |
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
| Q-M1 | ¿Se aceptan QR de monto abierto o siempre monto fijo atado a la orden? | Negocio | `ABIERTA` |
| Q-M2 | ¿A partir de qué monto hay que reconsultar el estado antes de acreditar? | Negocio / cumplimiento | `ABIERTA` |
