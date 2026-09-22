# Daily de Leo — turno noche — 2026-09-21

> **AVANCE: 0 / 49 — 0 %.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS`.

- **Persona:** Leo · **Turno:** noche · **Fecha:** 2026-09-21 · **Servicio:** `plataforma/comun-*`, `buildSrc`, plantilla de servicios
- **Tu encargo:** [Plataforma: outbox que publica, helper de idempotencia y guardas comunes](PR3-Plataforma.Infra/OutboxQuePublicaYGuardasComunes.md)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../Daily-Noche-2026-09-21.md)
- **Rama:** `leo/feature/carril-PR3-plataforma` → PRs a `dev`, espejo a `test`. **La plantilla de perfiles (H3.S3.M1) se mergea en la primera hora.**

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `async-messaging-events`, `concurrency-and-locking`, `microservices-testing`, `distributed-tracing-correlation`, `backend-observability`, `environment-secrets-config`, `error-handling-contract`, `authn-identity`, `static-analysis-linting`, `evidence-and-verification`, `finish-your-turn`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — Helper `Idempotencia` con usuario, operación y hash | 11 | 0 | TODO |
| H2 — Outbox que publica: bean, lock, cabeceras, backoff, Kafka caído, reinicio | 20 | 0 | TODO |
| H3 — Guardas comunes: decodificador, guarda de producción, perfiles, errores | 7 | 0 | TODO |
| H4 — Barridos, `Dinero`, logs JSON, probes, ArchUnit compartido | 11 | 0 | TODO |
| **TOTAL** | **49** | **0** | |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|

## 4. A medias — las cuatro respuestas, obligatorias

### <ID> — <título>
- **Qué anda:**
- **Qué no anda:**
- **Qué falta exactamente:**
- **Dónde quedó:** <rama, archivos, si compila>

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|

> Recordá la regla 65: el outbox se prueba de punta a punta con un emisor y un consumidor de
> prueba propios (H2.S2); no necesitás ningún caso de uso ajeno. Solo una decisión de negocio
> queda abierta.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
| Q-01 (AMB-10) | Consumidor Kafka | — | DECIDIDA: solo de prueba en `src/e2eTest` |
| Q-02 | Backoff e `intentos-maximos` | — | DECIDIDA: 10 · PT1S · PT5M · jitter ±20 % · timeout PT10S, en configuración |
| Q-03 | `FALLIDO` vs tema DLQ | — | DECIDIDA: misma tabla + métrica + runbook |
| Q-04 (AMB-12) | Perfiles | — | DECIDIDA: `local/test/staging/production`; productivo = todo lo que no sea local/test |
| Q-05 | `aud` | — | DECIDIDA: global para acceso, por servicio para evidencia |
