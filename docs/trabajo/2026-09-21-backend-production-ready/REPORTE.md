# Reporte — PasanakuBackend: `dev` → production ready (sesión de planificación)

> **AVANCE: 0 / 210 — 0,0 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): ninguna todavía en el backend (`origin/dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` sin tocar); este repo: `main`, solo `docs/trabajo/`
- Peldaño de evidencia alcanzado: `DISCOVERED` (regla 30). No se escribió ni ejecutó código del backend: esta sesión produjo el plan (Fases 0–2) contra un clon de solo lectura del SHA actual.

## Completado
| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| — | ninguna microtarea del plan: todas están en `TODO` (la sesión fue Fase 0–2, el plan es el entregable) | `python .claude/hooks/plan_status.py` | `0/210 microtareas HECHO (0.0%) · TODO=209 · BLOQUEADO=1` |

## A medias
ninguna.

## Pendiente
| ID | Estado | Qué lo destraba |
|---|---|---|
| H0 → H12 (209 microtareas) | TODO | Ejecutar H0.S1.M1 (JDK 21 en la máquina) y arrancar por H0 en el orden del plan |
| H6.S5.M3 — aplicar rulesets de protección de ramas | BLOQUEADO — `DECISION_REQUIRED` (Pablo): acción sobre algo compartido; no se simula. Se destraba con confirmación explícita; los comandos quedan en `docs/operacion/branch-protection.md` (H6.S5.M2) | — |

## Evidencia
Descubrimiento (Fase 1), todo de solo lectura sobre el clon en scratchpad; las citas ruta:línea están en `PLAN.md` §2.1 y §2.4. Comandos y salidas recortadas:

```text
$ git ls-remote --heads https://github.com/PabloArauzCaballero/PasanakuBackend.git
19a621e666afdea5bdc40aced326d3f212a116f4	refs/heads/dev
519747a53d2cc2ddcbc1d63f0506368029b0bbc8	refs/heads/main
19a621e666afdea5bdc40aced326d3f212a116f4	refs/heads/test

$ gh api repos/PabloArauzCaballero/PasanakuBackend/branches/dev/protection
{"message":"Branch not protected", ... "status":"404"}      (ídem para main; rulesets → [])

$ gh run view 35644455765 --json jobs --jq '.jobs[] | "\(.conclusion)\t\(.name)"'
success   La boveda y el esquema no divergen
success   Dependencias, secretos e imagen
success   Base efimera, semillas y permisos
failure   Formato, reglas propias y compilacion        ← paso fallido: "2 · formato"
skipped   Los cinco corredores / bootJar y docker build / Contratos y clientes / Frontend / Punta a punta

$ grep -rn "new Relevo(\|LockProvider\|EnableSchedulerLock" --include=*.java --include=*.kts .
(sin resultados)                                        ← Relevo no es bean; sin LockProvider

$ grep -rln "KafkaContainer\|EmbeddedKafka\|@KafkaListener" --include=*.java .
(sin resultados)                                        ← no hay consumidores ni Kafka en pruebas

$ sed -n 43,47p plataforma/comun-web/.../idempotencia/Idempotencia.java
        Record previa = dsl.select(...).from(tabla)
                .where(DSL.field("clave_idempotencia").eq(clave.valor()))
                .and(DSL.field("operacion").eq(operacion))   ← sin usuario_id; el índice es (usuario_id, clave, operacion)

$ sed -n 31,40p servicios/nucleo-financiero/.../SegundoFactorLocal.java
        if (!exigido) { return factor != null && !factor.isBlank(); }
        return false;                                   ← @Component sin @Profile

$ java -version
bash: java: command not found                           ← la máquina de planificación no tiene JDK en PATH
```

## No cubierto
- Ningún comando de build/test del backend se ejecutó (sin JDK en esta máquina): el estado real de `verificar`, `integrationTest`, `sagaTest` y `e2eTest` en el SHA es **desconocido** hasta H0.S3.
- Los hallazgos A–J se revalidaron **leyendo código y consultando la API de GitHub**, no ejecutando: eso alcanza para `DISCOVERED`, no para afirmar comportamiento en runtime.
- No se revisaron: contenido del trigger R-SEG-09 en detalle, `AislamientoEsquemaTest`, mecanismo de bitácora encadenada, clientes HTTP salientes, formato de logs (quedan como desconocidos §2.2 del plan).

## Desvíos del plan
ninguno (el plan se escribió en esta sesión; no había plan previo).

## Riesgos residuales
- El plan asume que el generador `scripts/generar_ddl.py` y la bóveda permiten agregar columnas/tablas (H1.S1.M7, H2.S3.M1, H3.S3.M2); si el modelo `.puml` exige más pasos, esas microtareas crecen.
- El SHA de `dev` cambia con frecuencia (3 pushes el 2026-09-21): H0 debe volver a registrar el SHA y re-verificar A–J antes de tocar nada.
- Tabla completa en `PLAN.md` §6.

## Decisiones y ambigüedades
- Doce ambigüedades registradas con supuesto y responsable en `PLAN.md` §3 (AMB-1 … AMB-12). Ninguna se resolvió como hecho; las de arquitectura (AMB-2, AMB-6, AMB-7) y de negocio (AMB-3, AMB-8) requieren confirmación de Pablo antes de su hito.
- Decisión de esta sesión: el plan vive acá y se copia al backend en H0.S1.M4 (AMB-1); la protección de ramas no se aplica sin confirmación aunque `gh` tenga permisos (§1 OUT).
