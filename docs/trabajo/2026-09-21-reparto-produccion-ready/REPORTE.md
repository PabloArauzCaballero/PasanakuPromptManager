# Reporte — Reparto en carriles del plan "dev → production ready"

> **AVANCE: 14 / 15 — 93,3 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): este repo `main` @ `674b5c1` (+ el commit de cierre); backend `dev` y `test` @ `5d7948e` (solo `docs/auditoria-produccion/`; el código sigue en `19a621e6`)
- Peldaño de evidencia alcanzado: `VERIFIED` para el artefacto documental (validadores del repo y verificadores del backend ejecutados; pushes confirmados con `git ls-remote`). Sobre el código del backend nada cambia de peldaño: sigue en `DISCOVERED`.

## Completado
| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Árbol del reparto (5 personas, `entregables/`, `evidencia/`) | `find repartos/2026-09-21 -type d \| wc -l` | `22` |
| H1.S1.M2–M6 | 5 encargos (Richard 28 · Justin 42 · Leo 49 · Marcelo 40 · Pablo 54 microtareas) | `python tools/check_reparto.py repartos/2026-09-21` | `OK, 2026-09-21 cumple la estructura obligatoria` |
| H1.S2.M1 | 5 dailies personales | `ls repartos/2026-09-21/PromptNoche/*/*-Daily-Noche-2026-09-21.md \| wc -l` | `5` |
| H1.S2.M2 | Daily del equipo (22 H · 63 S · 213 M; esperas → dobles; reservas disjuntas; ambigüedades) | revisión | ninguna espera sin doble; ninguna ruta con dos dueños |
| H1.S2.M3 | Validadores | `python tools/check_reparto.py … && python tools/check_skills_citadas.py` | exit 0 ×2; `52 skills citadas, 0 inexistentes` |
| H1.S2.M4 | Este reporte (primera versión) | `python .claude/hooks/plan_status.py` | avance calculado |
| H1.S3.M1 | **Todas las ambigüedades decididas** (plan madre §3.1, daily §5, 5 encargos §5, 5 dailies §8) | `python decidir_ambiguedades.py` | `filas reemplazadas: 65 / 65; bloques: 4`; 12 archivos con `DECIDIDA` |
| H1.S3.M2 | Contratos `step-up-jwt.md` y `evento-kafka.md` + `README.md` + copia del plan en el backend | `python scripts/verificar_boveda.py` · `python scripts/verificar_seguridad.py` (en el backend) | `TODO OK` · `TODO OK · 2 aviso(s)` (avisos S-8/S-9 preexistentes, no de estos archivos) |
| H1.S3.M3 | Push de este repo a `origin/main` | `git push origin main` | `41d1e0a..674b5c1  main -> main`; `git rev-parse HEAD origin/main` iguales |
| H1.S3.M4 | Push de `docs/auditoria-produccion/` del backend a `dev` y espejo `test` | `git push origin HEAD:dev && git push origin HEAD:test` | `19a621e..5d7948e  HEAD -> dev` · `19a621e..5d7948e  HEAD -> test`; `git ls-remote origin dev test` → ambas `5d7948e` |

## A medias
ninguna.

## Pendiente
| ID | Estado | Qué lo destraba |
|---|---|---|
| H1.S3.M5 — ruleset mínimo `proteccion-minima` (bloquea force-push y borrado en `dev`, `test`, `main`) | BLOQUEADO — `DECISION_REQUIRED` | El agente intentó `gh api --method POST …/rulesets` y **el clasificador de permisos lo denegó** (modificación de un recurso compartido); no se rodeó. Pablo lo aplica con un comando: `gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input repartos/2026-09-21/PromptNoche/Pablo/PR5-Ci.Operacion/entregables/ruleset-minimo.json` |
| El turno (213 microtareas en `NOT_RUN`) | TODO | Cada persona arranca por la sección 1 de su encargo y el baseline de su módulo |

## Evidencia
```text
$ python decidir_ambiguedades.py
filas reemplazadas: 65 / 65; bloques: 4
exit=0

$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 52 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)

(PasanakuBackend) $ python scripts/verificar_boveda.py | tail -1
TODO OK
(PasanakuBackend) $ python scripts/verificar_seguridad.py | tail -3
  AVISO · S-8 · 24 permisos que un CU exige y el catálogo no tiene: …   ← preexistente
  AVISO · S-9 · 3 propósitos de token sin canal activo …               ← preexistente
TODO OK · 2 aviso(s)

(PasanakuBackend) $ git push origin HEAD:dev && git push origin HEAD:test
   19a621e..5d7948e  HEAD -> dev
   19a621e..5d7948e  HEAD -> test
$ git ls-remote origin dev test
5d7948eeddba3fa68ee7389984772689bfb977f1	refs/heads/dev
5d7948eeddba3fa68ee7389984772689bfb977f1	refs/heads/test

(PasanakuPromptManager) $ git push origin main
   41d1e0a..674b5c1  main -> main

$ gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input ruleset-minimo.json
Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Modify Shared Resources].
```

## No cubierto
- Los validadores comprueban estructura, no calidad; que cada DoD sea ejecutable se sabrá en el turno.
- Las reservas de archivos se cruzaron a mano (cinco encargos vs daily §4); no hay script.
- El CI del backend corre sobre `5d7948e` (solo docs): no se esperó su resultado. Los verificadores de bóveda y seguridad se corrieron localmente antes de pushear y pasaron; el job `codigo` seguirá rojo por Spotless hasta Pablo H2.S1, como estaba.
- Ninguna microtarea del backend se ejecutó.

## Desvíos del plan
- Se agregó H1.S3 (5 microtareas) a pedido de Pablo ("corregí las ambigüedades y pusheá"): decidir, escribir contratos, publicar en `main`/`dev`/`test`, ruleset. Denominador 10 → 15.
- La decisión sobre el ruleset se redactó primero como "aplicado" y, al ser denegado el comando, se reescribió en los 12 archivos como "listo, lo aplica Pablo". Ninguna versión con "aplicado" llegó a un commit.

## Riesgos residuales
- Sin el ruleset mínimo, un `git push --force` accidental sobre `dev`/`test` puede reescribir historia durante el turno. Es un comando de Pablo.
- Carga desigual (Pablo 54, Leo 49 vs Richard 28): deliberada por ruta crítica y conflicto cero; lo que no cierre va `A MEDIAS`.
- Archivos compartidos por micro-PR (`sql/` generado, `libs.versions.toml`, `buildSrc/`, `_Arquitectura.md`, `docs/Seguridad.md`, `Entornos y despliegue.md`) dependen de disciplina, no de candado.
- Merge con gate local, sin CI verde previo (por autonomía y porque `dev` no exige PR): un test ajeno roto se detecta después del merge.
- Windows: `core.longpaths=true` antes de clonar; anotado en el daily si alguien lo sufre.

## Decisiones y ambigüedades
Todas decididas el 2026-09-21 y escritas en los 12 archivos (plan madre §3.1 tiene la lista completa). Las que más pesan:
- **AMB-3 (factor MFA real)**: TOTP RFC 6238 verificado dentro de `identidad` desde `factor_mfa.secreto_cifrado` — **sin proveedor externo**; SMS/WhatsApp por `notificaciones` como segundo canal; el desafío reutiliza `token_verificacion` (`proposito='MFA_RETIRO'`), sin tabla nueva.
- **AMB-4/Q-05 (aprobación)**: `POST /billetera/retiros/{ordenId}/aprobacion`; `RETIRO_APROBAR` al rol **`TESORERIA`** (existe en el seed; `RESPONSABLE_RIESGOS` conserva `REVERSO_AUTORIZAR`).
- **AMB-6**: Redis entra al stack (ADR-050). **AMB-7**: `aplicar.sql` generado y solo cambios aditivos este turno; Flyway en ADR posterior. **AMB-8**: PITR; RPO/RTO se miden en el restore, no se prometen. **AMB-9**: HIGH+CRITICAL bloquean.
- **AMB-R1**: `test` es espejo fast-forward de `dev` (ya aplicado hoy: ambas en `5d7948e`).
- **Ruleset**: durante el turno `dev` no exige PR ni aprobaciones; el mínimo (sin force-push/borrado) queda listo para Pablo; el completo va en la promoción `dev → main`.
