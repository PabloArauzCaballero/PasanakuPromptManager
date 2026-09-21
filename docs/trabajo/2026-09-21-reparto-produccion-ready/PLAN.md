# Plan — Reparto en carriles del plan "dev → production ready"

- Fecha: 2026-09-21 · Repos afectados: este repo (`repartos/2026-09-21/PromptNoche/`) · Predecesor: `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (210 microtareas, 0 HECHO)
- Resultado observable: cada una de las cinco personas abre su carpeta en `repartos/2026-09-21/PromptNoche/<Persona>/` y encuentra un encargo autocontenido, sin dependencias bloqueantes (todo contrato ajeno viene con su doble en tres niveles), con reservas de archivos disjuntas y el ritual exacto para pushear a `dev` y espejar en `test`; el daily del equipo suma 213 microtareas repartidas (210 del plan madre + 5 baselines por módulo − 2 fundidas).
- Kill-test: `python tools/check_reparto.py repartos/2026-09-21` sale 1, o dos encargos reservan el mismo archivo, o un encargo tiene una fila "espera a X" sin doble declarado.

## Alcance
- IN: `repartos/2026-09-21/PromptNoche/**` (daily de equipo, 5 dailies personales, 5 encargos con `entregables/` y `evidencia/` vacíos), este `PLAN.md` y su `REPORTE.md`.
- OUT: el backend (no se toca código), `planes/17|18|19` del backend (sus fichas de carril no se editan desde acá; se cita el contrato), `tools/check_reparto.py` (la lista de personas no cambia), el plan predecesor (solo se referencia).
- Ambigüedades registradas: ver tabla en el daily del equipo §5 (se arrastran las AMB-1…12 del plan predecesor). Nueva: **AMB-R1** el pedido dice "pushear a dev y test"; supuesto: `test` es espejo de `dev` (hoy tienen el mismo SHA) y se actualiza con `git push origin origin/dev:test` después de cada merge a `dev`. Confirmar: Pablo.

## H1 — Los cinco encargos existen, pasan el validador y no se pisan
**CA:** Dado `repartos/2026-09-21`, cuando corre `check_reparto.py` y `check_skills_citadas.py`, entonces ambos salen 0; y ninguna ruta aparece en la reserva de dos personas.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21` → exit 0 · `python tools/check_skills_citadas.py` → exit 0 · revisión manual de la tabla de reservas.
**Estado:** A MEDIAS — H1.S1 y H1.S2 HECHO; H1.S3 con una microtarea BLOQUEADO (ruleset, un comando de Pablo)

### H1.S1 — Estructura y encargos
**CA:** Dado cada persona, cuando abre su carpeta, entonces hay un encargo con secciones 1–6 de la plantilla, tres capas con CA/DoD/Estado y la tabla de contratos simulados.
**DoD:** 5 encargos escritos; validador en verde.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Crear árbol `repartos/2026-09-21/PromptNoche/{Richard,Pablo,Marcelo,Justin,Leo}/<Lote>.<Modulo>/{entregables,evidencia}` | 5 carpetas con `.gitkeep` | `find repartos/2026-09-21 -type d | wc -l` ≥ 16 | HECHO |
| H1.S1.M2 | Encargo de Richard (`identidad`) | pasa el validador | `python tools/check_reparto.py repartos/2026-09-21` no lo nombra | HECHO |
| H1.S1.M3 | Encargo de Justin (`nucleo-financiero`) | ídem | ídem | HECHO |
| H1.S1.M4 | Encargo de Leo (plataforma) | ídem | ídem | HECHO |
| H1.S1.M5 | Encargo de Marcelo (seguridad transversal, base, `aportes`) | ídem | ídem | HECHO |
| H1.S1.M6 | Encargo de Pablo (CI, supply chain, gateway, operación, cierre) | ídem | ídem | HECHO |

### H1.S2 — Dailies y validación
**CA:** Dado el daily del equipo, cuando se lee §3 y §4, entonces toda espera tiene su doble declarado y toda reserva tiene un solo dueño.
**DoD:** validadores en verde + suma de microtareas = las del plan predecesor (± las agregadas por el reparto, declaradas).
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | 5 dailies personales desde la plantilla, con enlace a su encargo | existen | `ls repartos/2026-09-21/PromptNoche/*/*-Daily-Noche-2026-09-21.md | wc -l` → 5 | HECHO |
| H1.S2.M2 | Daily del equipo con §1 (conteos), §3 (esperas → dobles), §4 (reservas), §5 (ambigüedades) | tablas completas | revisión | HECHO |
| H1.S2.M3 | Validadores | exit 0 ×2 | `python tools/check_reparto.py repartos/2026-09-21 && python tools/check_skills_citadas.py` | HECHO |
| H1.S2.M4 | `REPORTE.md` de este trabajo | avance en la primera línea | `python .claude/hooks/plan_status.py` | HECHO |

### H1.S3 — Decisiones, contratos y publicación (agregada el 2026-09-21 a pedido de Pablo)
**CA:** Dado cada ambigüedad de los cinco encargos, cuando se lee su fila, entonces dice `DECIDIDA` con la decisión; este repo está en `origin/main`; la copia del plan y los dos contratos están en `dev` y `test` del backend; un ruleset bloquea force-push y borrado en las tres ramas.
**DoD:** `grep -c DECIDIDA` en los 11 archivos > 0 · `git log origin/main -1` con el commit · `git ls-remote origin dev test` del backend con el SHA nuevo · `gh api …/rulesets` no vacío.
**Estado:** A MEDIAS — anda todo salvo el ruleset (M5): el agente no tiene permiso para crearlo; queda el JSON y el comando para Pablo

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Reemplazar toda ambigüedad por su decisión en plan madre §3.1, daily del equipo §5, 5 encargos §5, 5 dailies §8 | 0 filas `ABIERTA`/`DECISION_REQUIRED` sin decisión | `grep -rn "ABIERTA\|DECISION_REQUIRED" repartos/2026-09-21` → solo menciones históricas dentro de decisiones | HECHO |
| H1.S3.M2 | Escribir los contratos `step-up-jwt.md` y `evento-kafka.md` en el backend | 2 archivos | `ls docs/auditoria-produccion/contratos/` | HECHO |
| H1.S3.M3 | Commit + push de este repo a `origin/main` | `origin/main` = HEAD | `git status --short` vacío; `git rev-parse origin/main` = `git rev-parse HEAD` | HECHO |
| H1.S3.M4 | Backend: `docs/auditoria-produccion/{PLAN.md,README.md,contratos/}` en `dev` y espejo `test`, con `verificar_boveda.py` y `verificar_seguridad.py` en verde antes de pushear | SHA nuevo en ambas ramas | `git ls-remote origin dev test` | HECHO |
| H1.S3.M5 | Ruleset mínimo `proteccion-minima` (non_fast_forward + deletion) en `dev`, `test`, `main` — intentado por `gh api`, denegado por permisos del agente; JSON y comando entregados a Pablo | `gh api` lo lista | `gh api repos/PabloArauzCaballero/PasanakuBackend/rulesets --jq '.[].name'` | BLOQUEADO — DECISION_REQUIRED (Pablo: un comando; no se simula, es un recurso compartido) |

## Riesgos y bloqueos previstos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Un contrato entre carriles queda sin doble y alguien espera | Se viola el pedido ("jamás detenerse") | Tabla §3 del daily: cada espera lleva doble en tres niveles y la microtarea de integración diferida |
| Dos carriles necesitan tocar `sql/` (generador), `libs.versions.toml`, `buildSrc/` | Conflictos | Protocolo micro-PR al troncal (planes/07 §6 del backend): commit mínimo, merge a `dev` dentro de la hora, todos rebasean |
| El validador exige CA/DoD/Estado en hito y subtarea | Encargo rechazado | Copiar la forma de la plantilla; correr el validador antes de cerrar |
