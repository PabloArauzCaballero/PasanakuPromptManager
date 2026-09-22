# Reporte — Actualizar el estado real de los carriles de Justin

- Fecha: 2026-09-22 · Plan: [PLAN.md](./PLAN.md) · Ramas: `justin/docs/actualizar-carriles`, `justin/fix/pr12-reconciliacion`, `justin/fix/pr2-cierre`
- Peldaño de evidencia: `TESTED` para la porción Angular de PR12; `DISCOVERED` para el estado de PR2 que no pudo ejecutar integración; `WRITTEN` para los dailies corregidos.
- Avance del plan documental: 3 / 6 microtareas HECHO (50 %). Las restantes dependen del gate de PostgreSQL, de Flutter o de corregir estados documentales preexistentes, y no se maquillan como cierre.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M2 | PR7 no conserva cambios pendientes frente a `dev` | `git diff --quiet origin/dev origin/justin/frontend/tabla-datos` | exit 0 |
| H1.S1.M3 (Angular) | PR12 reconciliado sobre un `dev` limpio: el test seguro ya no toma el reemplazo demo y el dev-server resuelve imports ESM | `corepack yarn workspace @aportaya/backoffice test:front`; `test:a11y`; `build` | 296/296 unitarios; 32/32 a11y; build exit 0 |
| H2.S1.M1–M2 | Dailies de Justin y filas de equipo corrigen el falso `NOT_RUN` y declaran evidencia/límites | revisión de diff | sin estados de cierre inventados para Justin |

## A medias

### H1.S1.M1 — Gate de PR2

- **Qué anda:** `origin/dev` contiene las clases y pruebas de idempotencia, MFA step-up, doble aprobación, proveedor y reconciliación.
- **Qué no anda:** el gate dirigido no llega a pruebas: `generateJooq` recibe `Connection to 127.0.0.1:5433 refused`.
- **Qué falta exactamente:** iniciar PostgreSQL de Pasanaku y repetir `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11*' --tests '*SegundoFactorStepUpTest*' --tests '*ArranqueProduccionTest*'`.
- **Dónde quedó:** worktree `justin/fix/pr2-cierre`; `docker ps` confirmó que Docker Desktop no está disponible.

### H1.S1.M3 — Flutter de PR12

- **Qué anda:** los dos commits se aplicaron sin conflicto y Angular pasó sus gates.
- **Qué no anda:** `flutter` no existe en `PATH`; no se ejecutaron `configuracion_test.dart`, `configuracion_invalida_test.dart` ni `flutter analyze`.
- **Qué falta exactamente:** ejecutar esos comandos con SDK Flutter instalado y registrar la salida; después, revisar/mergear la PR.
- **Dónde quedó:** rama `justin/fix/pr12-reconciliacion`.

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| H1.S1.M1 | BLOQUEADO | PostgreSQL/Docker operativo para JOOQ e integración de PR2 |
| H1.S1.M3 (Flutter) | BLOQUEADO | SDK Flutter en `PATH` |
| H2.S1.M3 | A MEDIAS | Corregir los estados inventados preexistentes de PR10/PR15 en un trabajo de Pablo y repetir el validador |
| Cierre formal de PR7 | A MEDIAS | Recuperar o volver a ejecutar sus DoD microtarea por microtarea; no basta que el árbol esté integrado |
| Cableado raíz de PR12 | A MEDIAS | Richard, dueño de `app.config.ts` y componente raíz, aplica el contrato en `entregables/cableado-app-config.md` |

## Evidencia

```text
$ corepack yarn workspace @aportaya/backoffice test:front
Test Files  52 passed (52)
Tests  296 passed (296)

$ corepack yarn workspace @aportaya/backoffice test:a11y
Test Files  26 passed (26)
Tests  32 passed (32)

$ corepack yarn workspace @aportaya/backoffice build
Application bundle generation complete.
exit=0

$ ./gradlew :servicios:nucleo-financiero:integrationTest ...
Execution failed for task ':servicios:nucleo-financiero:generateJooq'.
Connection to 127.0.0.1:5433 refused.
exit=1

$ flutter --version
flutter: command not found
exit=1

$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: ESTRUCTURA INCOMPLETA en 2026-09-21
  - 2026-09-21/PromptNoche/Frontend/Pablo/PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md: le FALTA estados inventados: ...
  - 2026-09-21/PromptNoche/Frontend/Pablo/PR15-Contratos.Frontend/LineaBaseContratosAuthzYCierre.md: le FALTA estados inventados: ...
exit=1

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 89 skill(s) distinta(s), 0 inexistentes
```

## No cubierto

- No se ejecutó integración, E2E de compose ni JWKS real para PR2.
- No se ejecutaron Flutter test/analyze ni E2E Playwright de PR12.
- No se atribuyó un conteo de microtareas terminadas basado solo en commits previos.
- `check_reparto.py` no está verde por contenido preexistente de los carriles de Pablo; no es evidencia de cierre para este reporte.

## Decisiones y ambigüedades

- Se aplicaron por cherry-pick exclusivamente `cb55269` y `e18f823` sobre una rama nueva de `origin/dev`, porque la rama antigua de configuración estaba desfasada y un rebase completo habría incluido eliminaciones ajenas.
- No se cambió código financiero de PR2: sin un fallo dirigido reproducible, hacerlo sería una modificación de alto riesgo sin evidencia.
