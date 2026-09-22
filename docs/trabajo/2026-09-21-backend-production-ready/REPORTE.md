# Reporte — PasanakuBackend: `dev` → production ready (consolidado, turno noche 2026-09-21/22)

> **AVANCE (carril PR5 — CI y operación, el único con ejecución real hasta ahora): 41 / 54 —
> 75,9 %.** El plan madre de acá tiene 210 microtareas repartidas en 5 carriles (H0–H12, mapeadas
> a los 5 encargos de `repartos/2026-09-21/PromptNoche/Backend/`); **no se recalcula el 0/210
> global** porque los otros cuatro carriles (PR1-identidad, PR2-núcleo-financiero,
> PR3-plataforma-infra, PR4-seguridad) todavía no publicaron su propia bitácora ni su propio
> reporte (hallazgo F-01, ver `PasanakuBackend/docs/auditoria-produccion/FINAL_REPORT.md`) —
> inventarles un número sería una cifra sin evidencia (regla 00 §1.2). Esta sección de arriba se
> actualiza sola cuando esa evidencia exista; hasta entonces, la cifra real y verificable es la
> del único carril que sí se ejecutó esta noche.

- Fecha: 2026-09-22 (turno noche 2026-09-21, cierre parcial) · Plan: [PLAN.md](./PLAN.md) · Rama
  del backend: `pablo/feature/carril-PR5-ci-operacion` @ `1639734` (PR #1 y #2 abiertos, sin
  mergear — el clasificador de permisos de la sesión deniega `gh pr merge`); este repo: rama
  actual de esta sesión
- Peldaño de evidencia alcanzado: **`VERIFIED` por área** (regla 30.5) para H3 (borde) y H4 (carga
  medida) del carril PR5 — comportamiento observado en runtime real (gateway corriendo, Redis
  apagado a propósito, CI real disparado con `workflow_dispatch`). **`WRITTEN`/`A MEDIAS`** para el
  resto de H2/H5 (cobertura y CI completo bloqueados por hallazgos fuera de alcance: F-04, F-06,
  F-07). **`UNKNOWN`** para los carriles PR1–PR4 — sin bitácora, no hay evidencia que citar. El
  detalle línea por línea, con comando y salida de cada microtarea, vive en
  `PasanakuBackend/docs/auditoria-produccion/carriles/PR5-ci-operacion.md`, no se duplica acá.
- Esta sección reemplaza la de la sesión de planificación original (0/210, `DISCOVERED`, sin JDK
  en la máquina de entonces) — esa sesión solo produjo el plan; esta produjo ejecución real.

## Completado (carril PR5 — CI y operación; único carril ejecutado esta noche)

Tabla completa, cada fila con su comando y su salida enlazada, en
`PasanakuBackend/docs/auditoria-produccion/carriles/PR5-ci-operacion.md`. Resumen:

| Bloque | Qué se logró | Resultado |
|---|---|---|
| H3 (borde) | Rate limiting Redis fail-closed, CORS fail-closed por perfil, `/actuator` bloqueado — con dos bugs de seguridad reales encontrados y corregidos verificando contra el gateway corriendo de verdad | **7/7 HECHO** |
| H4 (carga) | 6 escenarios k6, baseline ×3 medido | **3/3 HECHO** |
| H5.S1/S2 | 4 runbooks + backup/restore real (401/401 tablas), `promotion-gate.md` sin checks sin enlazar | HECHO |
| H5.S3.M1 | Revisión independiente del diff (regla 70.4.8): 2 hallazgos reales, ambos corregidos y reverificados (gap de `/actuator` sin barra; regresión de `ConfiguracionCors`) | HECHO |
| H2.S6.M1/M3/M4 | `e2e-financiero` verificado con CI real (`workflow_dispatch`); pasos de Marcelo cableados con guard; 0 trampas en workflows/buildSrc | HECHO |

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| — (sesión de planificación previa) | plan madre escrito, Fases 0–2, sin JDK en esa máquina | `python .claude/hooks/plan_status.py` | `0/210` era el estado ANTES de que arrancara la ejecución — ver nota arriba |

## A medias

- **H2.S6.M2 / H5.S3.M3 (`verificarProduccion`)**: la tarea existe, compila, su grafo de
  dependencias resuelve, y corrió de punta a punta dentro de un checkout limpio (`git worktree`) —
  pero no llega a exit 0 porque `plataforma/comun-web` y `servicios/identidad` no pasan su propio
  gate de cobertura (jacoco), hallazgos F-06/F-07, ambos fuera del alcance de este carril.
  Reproducido dos veces (máquina normal y worktree limpio): determinista, no es un artefacto del
  entorno.
- **H2.S1.M2**: PR #1 con el gate local en verde, sin mergear (permiso denegado al agente).

## Pendiente
| ID | Estado | Qué lo destraba |
|---|---|---|
| Carriles PR1 (identidad), PR2 (núcleo financiero), PR3 (plataforma/infra), PR4 (seguridad) | `TODO` — sin bitácora publicada (F-01) | Richard, Justin, Leo, Marcelo — cada uno cierra y publica su `carriles/PR*.md` |
| H2.S6.M5 / H5.S3.M4 (CI completo en verde) | `BLOQUEADO` estructural | F-04 (CVE reales, exige upgrade de Spring Boot/Cloud/Netty — no autorizado este turno) + F-06/F-07 (cobertura de módulos ajenos) |
| H2.S5.M3 — ruleset mínimo `proteccion-minima` | `BLOQUEADO — DECISION_REQUIRED` | Un comando de Pablo: `gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input entregables/ruleset-minimo.json` (el JSON ya está listo en el repo del backend) |
| Mergear PR #1 y PR #2 del carril PR5 | `BLOQUEADO` | El clasificador de permisos deniega `gh pr merge`; Pablo mergea con un clic |
| Recomendación `dev → main` | Redactada, sin ejecutar | Ver `PasanakuBackend/docs/auditoria-produccion/FINAL_REPORT.md` §4 — no se promueve hasta que F-01/F-04/F-06/F-07 se cierren |

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
- **Los carriles PR1–PR4 completos**: identidad, núcleo financiero, plataforma/infra y seguridad
  transversal no tienen ni bitácora ni ejecución verificable desde este reporte (F-01). Este
  reporte no puede — ni debe — afirmar nada sobre ellos.
- `H1.S2.M6` / `e2eTest` real contra los 14 servicios: no se construyeron las 14 imágenes
  (trabajo de horas, causa explícitamente autorizada por el encargo de PR5).
- `mutation-testing.md`, `security-matrix.md`, `financial-invariants.md`, `endpoints.md`: no
  existen todavía (fuera del carril PR5, ver `promotion-gate.md` en el backend).
- (Histórico, sesión de planificación) Ningún comando de build/test del backend se ejecutó en esa
  sesión (sin JDK en esa máquina): eso ya no aplica — esta noche SÍ hubo ejecución real, ver arriba.
- Los hallazgos A–J se revalidaron **leyendo código y consultando la API de GitHub**, no ejecutando: eso alcanza para `DISCOVERED`, no para afirmar comportamiento en runtime.
- No se revisaron: contenido del trigger R-SEG-09 en detalle, `AislamientoEsquemaTest`, mecanismo de bitácora encadenada, clientes HTTP salientes, formato de logs (quedan como desconocidos §2.2 del plan).

## Desvíos del plan
- **H2.S2.M3 (carril PR5)**: en vez de la prueba negativa sintética que pide el plan (dependencia
  vulnerable agregada y revertida en una rama temporal), se usó la evidencia real ya existente —
  el lockfile real tiene 1122 vulnerabilidades conocidas que bloquean el job por diseño. Prueba
  más fuerte que la sintética, declarada como desvío explícito (regla 00 §1.7). Detalle en
  `PasanakuBackend/docs/auditoria-produccion/evidencia/H2-S2-M3-osv-negativo.txt`.
- **Kafka en `e2e-financiero`**: el plan/encargo no fija imagen; se usó `confluentinc/cp-kafka`
  (la que ya corre en este repo) en vez de una imagen sin verificar contra el proyecto real.
- (Histórico) ninguno en la sesión de planificación original — el plan se escribió esa sesión, sin plan previo.

## Riesgos residuales
- **F-04 (CRITICAL sin parche en dependencias reales)**: `netty-handler`, `bcprov-jdk18on`,
  `spring-security-web` — corregir exige un upgrade de Spring Boot/Cloud/Netty no autorizado este
  turno. Riesgo real si se despliega sin resolverlo.
- **F-06/F-07 (cobertura real por debajo del umbral propio)** en `comun-web` e `identidad`: código
  en producción con menos tests de los que el propio proyecto exige.
- **F-05**: 0/14 servicios exponen `prometheus` — sin métricas reales en producción hoy.
- **Sin merge**: mientras los PR #1/#2 del carril PR5 sigan abiertos, cualquier otro carril que
  rebase contra `dev` no tiene el estándar de seguridad ni CycloneDX/Redis instalados.
- (Histórico) El plan asume que el generador `scripts/generar_ddl.py` y la bóveda permiten agregar columnas/tablas (H1.S1.M7, H2.S3.M1, H3.S3.M2); si el modelo `.puml` exige más pasos, esas microtareas crecen.
- El SHA de `dev` cambia con frecuencia; H0 debe volver a registrar el SHA y re-verificar A–J antes de tocar nada.
- Tabla completa en `PLAN.md` §6.

## Decisiones y ambigüedades
- Las doce ambigüedades de `PLAN.md` §3 quedaron **decididas** el 2026-09-21 a pedido de Pablo; la lista con cada decisión está en `PLAN.md` §3.1 y se replicó en los cinco encargos del reparto. Las que más pesan: TOTP interno como factor real (sin proveedor externo, AMB-3); `RETIRO_APROBAR` al rol `TESORERIA` (AMB-4); Redis en el stack (AMB-6); esquema aditivo por generador este turno, Flyway después (AMB-7); RPO/RTO medidos en el restore, no prometidos (AMB-8).
- El plan vive acá y su copia ya está en `PasanakuBackend/docs/auditoria-produccion/PLAN.md` en `dev` y `test` (AMB-1). El ruleset mínimo no pudo aplicarlo el agente (permiso denegado); queda para Pablo.
- **Ambigüedad nueva, registrada, no resuelta por conveniencia**: el encargo de PR5 pide "las 16
  secciones del metaprompt §86" para `FINAL_REPORT.md`; ese documento no es accesible desde esta
  sesión en ninguno de los dos repos. Se usó la estructura de la regla 40 más el contenido que el
  propio encargo pide explícitamente (12 secciones reales, sin relleno). A confirmar con quien
  escribió el encargo dónde vive "el metaprompt".
