# Reporte — PasanakuFrontend (AportaYa): rescate, refactorización y hardening (sesión de planificación)

> **AVANCE: 0 / 247 — 0,0 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) v2 · Rama(s): monorepo sin tocar — `PasanakuBackend@dev` @ `5d7948e` (canónico por D-A2) y su espejo `PasanakuFrontend@dev` @ `19a621e6`; este repo: `main` (archivos nuevos sin commitear en `docs/trabajo/2026-09-21-frontend-rescate-hardening/`)
- Peldaño de evidencia alcanzado: `DISCOVERED` (regla 30). No se escribió ni ejecutó código del frontend: esta sesión produjo el plan (Fases 0–2 de la regla 10) a partir del metaprompt del usuario y del descubrimiento factual contra el clon local de `PasanakuBackend` (`Entrypoint-GitHUb/Pasanaku/PasanakuBackend`), cuyo árbol de `apps/`, `packages/`, `scripts/` y `.github/` es idéntico al SHA `19a621e6` de `PasanakuFrontend@dev` (`git diff --stat 19a621e6 HEAD` → solo 4 archivos bajo `docs/auditoria-produccion/`).

## Completado
| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| — | ninguna microtarea del plan: las 247 están en `TODO` (la sesión fue Fase 0–2; el plan es el entregable) | `python .claude/hooks/plan_status.py --path docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md` | `0/247 microtareas HECHO (0.0%) · TODO=247` · 15 hitos, 49 subtareas, todas con CA y DoD · 0 IDs duplicados |

## A medias
ninguna.

## Pendiente
| ID | Estado | Qué lo destraba |
|---|---|---|
| H0 (Línea base) | TODO | Instalar JDK 21 y Flutter 3.44.8 en la máquina (hoy `java`, `flutter`, `dart` no están en PATH). El JDK hace falta **una vez** para generar y commitear `clientes/` (D-A1); después el front compila sin él. |
| H1–H7 (P0: refresh single-flight, restauración de sesión, auditoría, mocks, config fail-fast, iOS, humo) | TODO | H0 cerrado. H1/H2 asumen refresh por **cookie HttpOnly** (D-A3): si `identidad.yaml` no lo ofrece, se cierran contra un doble que cumple ese contrato y se abre brecha de backend. H3 depende de que exista `POST /extraccion/accesos` (D4). |
| H8 (CI, protección de rama, cabeceras, dependencias) | TODO | H1–H7. Incluye los dos jobs `macos-latest` (D-A4: `goldens-macos`, `movil-integracion-macos`). La protección de rama clásica **no está disponible** en el remoto espejo: `403 Upgrade to GitHub Pro or make this repository public`; se reevalúa sobre el remoto canónico `PasanakuBackend` y se documenta. |
| H9–H11 (fronteras, duplicación/SSR/errores/telemetría, authz/idempotencia/OpenAPI) | TODO | H8. |
| H6.S3 (release iOS en macOS) | TODO | H6.S1–S2. El IPA sin firmar sale en cada corrida; TestFlight queda `skipped` hasta que Pablo cargue los 5 secrets de App Store Connect (D-A5). |
| H12 (calidad P2), H13 (fronteras de repo), H14 (verificación final) | TODO | H9–H11. H13 ya no espera decisión: aplica D-A2 (canónico `PasanakuBackend`, espejo por fast-forward) y deja el archivado del remoto para Pablo. |

## Evidencia
Toda la evidencia de esta sesión es de descubrimiento (peldaño 1); está citada con ruta:línea en `PLAN.md` §2.1. Comandos clave y su salida recortada:

```text
$ python .claude/hooks/plan_status.py --path docs/.../PLAN.md   # v2, tras aplicar D-A1..D-A6
  Avance: 0/247 microtareas HECHO  (0.0%)
  Estados: TODO=247

$ gh api repos/PabloArauzCaballero/PasanakuFrontend/commits/dev --jq '.sha + " " + .commit.committer.date + " " + (.commit.message|split("\n")[0])'
19a621e666afdea5bdc40aced326d3f212a116f4 2026-09-21T19:22:50Z fix: los fronts no construian — el paquete de tutoriales no entraba en la imagen

$ gh api repos/PabloArauzCaballero/PasanakuFrontend/branches --jq '.[].name'
dev

$ git -C Pasanaku/PasanakuBackend diff --stat 19a621e666afdea5bdc40aced326d3f212a116f4 HEAD | tail -1
 4 files changed, 1029 insertions(+)        # solo docs/auditoria-produccion/

$ gh run list -R PabloArauzCaballero/PasanakuFrontend --limit 3
2026-09-21T19:23:02Z Bóveda, esquema, semillas y despliegue completed/success 19a621e6
2026-09-21T19:23:02Z CI completed/failure 19a621e6
2026-09-21T18:13:52Z CI completed/failure 4bf13974

$ gh api repos/PabloArauzCaballero/PasanakuFrontend/branches/dev/protection
{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature.", "status":"403"}

$ grep -rnE "\|\| true|continue-on-error" package.json .github/workflows/ci.yml
package.json:21:    "humo": "for c in postman/humo/*.json; do yarn newman run ... || true; done",
.github/workflows/ci.yml:150:          grep -q "FALLA" humo.txt && exit 1 || true

$ grep -n "boundaries" apps/backoffice/eslint.config.js apps/web/eslint.config.js   # vacío
$ grep -n "eslint-plugin-boundaries" apps/backoffice/package.json apps/web/package.json
apps/backoffice/package.json:37:    "eslint-plugin-boundaries": "^5.0.0",
apps/web/package.json:46:    "eslint-plugin-boundaries": "^5.0.0",

$ grep -rn "MethodChannel" apps/movil/ios/Runner/*.swift      # vacío: los canales Android no tienen receptor iOS

$ for C in node yarn flutter dart java python gh docker; do ...; done
node v22.23.1 · yarn 4.18.0 · flutter NO en PATH · dart NO en PATH · java NO en PATH · python 3.14.2 · gh 2.97.0 · docker 29.6.2

$ python .claude/hooks/plan_status.py --path docs/.../PLAN.md   # v1, antes de las decisiones
  Avance: 0/237 microtareas HECHO  (0.0%)
  Estados: TODO=237
```

Archivos leídos completos (todos < 200 líneas, nombrados por el metaprompt como P0): `apps/backoffice/src/app/nucleo/{sesion.interceptor,sesion,registro-de-acceso.interceptor,gateway,idempotencia.interceptor,permisos}.ts`, `apps/web/src/app/nucleo/gateway.ts`, `apps/web/src/server.ts`, `apps/movil/lib/dominio/cliente.dart`, `apps/movil/lib/proveedores/sesion.dart`, `apps/movil/lib/infraestructura/plataforma.dart`. Leídos por rango o grep: `datos-simulados.ts`, `scripts/verificar_frontend.py`, `ci.yml` (job `frontend`), `package.json` de los 9 workspaces, `turbo.json`, `.yarnrc.yml`, `tsconfig.base.json`, `pubspec.yaml`, `playwright.config.ts` ×2, `eslint.config.js`, `despliegue/nginx/aportaya.conf`, ADR-044.

## No cubierto
- **Ningún comando del pipeline frontend se ejecutó** (`yarn install/lint/typecheck/test/build`, `flutter test`, Playwright): sin JDK ni Flutter en la máquina no se pueden generar los clientes ni compilar. El estado real de lint/tests/builds en el SHA es el desconocido D1 del plan y se resuelve en H0.S2.
- No se verificó el contrato real de `POST /sesion/refrescar` ni la existencia de `POST /extraccion/accesos` en los `openapi/*.yaml` (D3, D4): el plan los hace explícitos como primeras microtareas de H0.S3 porque cambian el diseño de H1 y H3.
- No se localizó el Dockerfile de la imagen `aportaya/backoffice` ni cómo llega `<meta aportaya-gateway>` al HTML desplegado (D2).
- No se leyó `landing/` (Astro, OUT por ADR-041) ni `packages/diseno_flutter` más allá de su presencia.
- No se leyeron los `carril-B*.md` de `planes/informes/` (informes de carriles frontend previos): pueden contener huecos ya declarados que H0.S3.M6 debe cruzar con `hallazgos.md`.

## Desvíos del plan
Esta sesión no ejecutó microtareas. Hubo **una corrección del plan (v1 → v2)**, registrada en su §"Registro de cambios": las seis ambigüedades A1–A6 pasaron a decisiones tomadas por Pablo en la misma sesión, lo que agregó 10 microtareas (237 → 247). Detalle:

| Decisión | Qué se resolvió | Impacto en el plan |
|---|---|---|
| **D-A1** | `clientes/angular` y `clientes/dart` **se versionan** (enmienda a ADR-016; hoy `.gitignore:49-50` los ignora). El gate pasa de "compila" a "regenerar no produce diff". | +3 microtareas (H0.S1.M7–M9); H11.S3.M4 usa `git diff --exit-code`. El front compila sin JDK tras el primer commit. |
| **D-A2** | Un solo árbol; remoto canónico `PasanakuBackend`; `PasanakuFrontend@dev` se mantiene por fast-forward y su archivado lo ejecuta Pablo. | +1 microtarea (H13.S1.M6); H13 pasa de "propuesta" a decisión aplicada; H14.S1.M5 pushea al canónico y sincroniza el espejo. |
| **D-A3** | El refresh web es por **cookie HttpOnly** (`withCredentials`, sin cuerpo); el móvil sigue con el refresh en `AlmacenSeguro` enviado en el cuerpo. | H1 y H2 fijan ese contrato; si `identidad.yaml` no lo ofrece, es brecha del backend y se cierra contra un doble (regla 65), declarado. |
| **D-A4** | Goldens e `integration_test/` corren en CI en jobs `macos-latest`. | H8.S2.M2 y M3 dejan de tener la salida "o se declara que no corren"; `turbo.json` se actualiza porque ahora sí corren. |
| **D-A5** | Hay release iOS en macOS sí o sí: IPA en cada corrida, gate de capabilities antes de compilar, TestFlight condicionado a secrets. | +6 microtareas (subtarea nueva **H6.S3**); H6.S2.M5 deja de marcar iOS como `BLOQUEADO`. |
| **D-A6** | Web/backoffice en producción exigen gateway **same-origin** (`/api/v1` relativo o `https://` con el propio host); el móvil exige `API` + `API_HOSTS` por `--dart-define`. | H5.S1.M1–M3 y H5.S3.M1/M3 reescritos con esa matriz; desaparece la "lista blanca" externa que no existía en ningún lado. |

Desvío respecto del **metaprompt**, que se mantiene: trata `PasanakuFrontend` como repo independiente y es el mismo árbol que `PasanakuBackend` (F-001, resuelto por D-A2).

## Riesgos residuales
- **Toolchain**: sin JDK 21 y Flutter 3.44.8 locales, H0 no cierra. Alternativa prevista: usar el CI como runner en una rama de auditoría.
- **Dos remotos del mismo árbol**: cualquier trabajo del plan del backend sobre `apps/` (p. ej. regenerar clientes por cambio de contrato de `identidad`) puede pisar este trabajo. Mitigación planificada: `scripts/verificar_remotos.sh` (H13.S1.M5) al inicio de cada sesión.
- **Protección de rama imposible en el plan actual de GitHub** (403): mientras no se decida hacer el repo público o pasar a Pro, el CI se puede saltear con un push directo. Documentado en H8.S4.
- **iOS**: sin Mac no hay verificación en dispositivo; H6 solo puede llegar a `TESTED` con `debugDefaultTargetPlatformOverride`.
- **Auditoría server-side**: si `/extraccion/accesos` no existe (D4), la auditoría de lectura queda `BLOQUEADO` del lado backend y el frontend solo puede dejar de fingir que la garantiza.
- El total de 247 microtareas **va a crecer**: H9.S2.M4, H11.S3.M2, H12.S4.M2 y H14.S2.M2 agregan filas por cada violación/pantalla/duplicado que aparezca. El porcentaje bajará; es información correcta.
- **Minutos de macOS**: D-A4 y D-A5 suman tres jobs `macos-latest` por push (goldens, integración, release iOS). Si el consumo resulta inviable, la mitigación escrita es mover `ios-release` a `workflow_dispatch` + tags, nunca eliminarlo.
- **Versionar `clientes/`** (D-A1) hace ruidosos los PRs que tocan contratos; se mitiga con `.gitattributes linguist-generated=true` en H0.S1.M8.

## Decisiones y ambigüedades
**Las seis ambigüedades quedaron decididas por Pablo en esta sesión** (D-A1…D-A6, §1 del plan y tabla de desvíos arriba). No quedan ambigüedades abiertas al 2026-09-21. Lo que sigue dependiendo de terceros no es ambigüedad sino insumo, y está declarado como tal:

| Insumo | De quién | Qué pasa mientras no esté |
|---|---|---|
| Modo cookie HttpOnly en `POST /sesion/refrescar` | dueño de `identidad` | H1/H2 se cierran contra un doble que cumple el contrato con cookie (regla 65), declarado en `brechas-backend.md` |
| 5 secrets de App Store Connect (`ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY`, certificado, perfil) | Pablo | El IPA sale sin firmar como artefacto; el paso `testflight` queda `skipped` explícito, nunca finge |
| Archivar o renombrar el remoto `PasanakuFrontend` | Pablo | El espejo se sincroniza por fast-forward en cada push (H13.S1.M6) |
| Valores de `API`/`API_HOSTS` en Coolify | Leo (infra) | El build de release falla por diseño (D-A6); no hay fallback |

Otras decisiones de esta sesión:
- **Plan en este repo, ejecución en el monorepo**: el plan se redactó en `docs/trabajo/` de `PasanakuPromptManager` (mismo patrón que `2026-09-21-backend-production-ready`) y se copiará a `docs/auditoria/plan-de-remediacion.md` del monorepo en H0.S1.M6, que es el nombre que exige el metaprompt §43.
- **Orden de hitos**: se respetó §42 del metaprompt (P0 antes que nada cosmético); H13 (fronteras de repo) se colocó antes de la verificación final porque su salida es solo documental.
- **No se agregan dependencias** (`helmet`, `local_auth`, `analyzer`, `knip`) sin verificar primero si ya están en el árbol y sin justificarlas por escrito (regla 90.4.2); cada caso está como microtarea de decisión.
- **Nada se commiteó en este repo** (el usuario no lo pidió): `docs/trabajo/2026-09-21-frontend-rescate-hardening/{PLAN.md,REPORTE.md}` quedan como archivos nuevos sin seguimiento, igual que los dos trabajos anteriores del mismo día.
