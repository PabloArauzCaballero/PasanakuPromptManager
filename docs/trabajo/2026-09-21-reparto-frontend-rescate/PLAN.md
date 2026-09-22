# Plan — repartir el rescate del frontend de AportaYa en los cinco carriles del turno noche

- Fecha: 2026-09-21 · Repos afectados: `PasanakuPromptManager` (solo este) · Predecesor: [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../2026-09-21-frontend-rescate-hardening/PLAN.md) v2 (247 microtareas, plan madre)
- Resultado observable: cada una de las cinco personas abre `repartos/2026-09-21/PromptNoche/Frontend/<persona>/PR1x-<Tema>.Frontend/<Encargo>.md` y encuentra su parte del rescate del frontend de AportaYa con las tres capas, CA y DoD por capa, reservas de archivos que no se pisan con las de nadie, y su daily personal actualizado con el segundo bloque; `python tools/check_reparto.py repartos/2026-09-21` sale 0.
- Kill-test: `python tools/check_reparto.py repartos/2026-09-21; echo $?` → si sale 1, o si el daily del equipo sigue diciendo `0 / 359` cuando ya hay cinco lotes nuevos, o si dos encargos reclaman el mismo archivo en sus reservas, esto NO está hecho.

## 0. Cómo se ejecuta este plan

| Tema | Regla para este trabajo |
|---|---|
| Dónde vive | Acá. Los artefactos son los cinco encargos, los cinco dailies personales de área frontend y el daily del equipo, todos bajo `repartos/2026-09-21/PromptNoche/`. |
| Evidencia | `docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/`: salida literal de los dos validadores y de los conteos. |
| Estados | Los seis de la regla 20. |
| Recursos | Trabajo documental; sin builds ni navegadores. Un solo trabajo activo: el anterior (`2026-09-21-frontend-rescate-hardening`) está cerrado con su `REPORTE.md`. |
| Qué NO se toca | El plan madre (queda como fuente; los encargos lo citan, no lo reescriben), el área `Backend/` del turno, los lotes `PR6`–`PR10` de `mantra-core-health`, y el código del monorepo de AportaYa. |

## 1. Alcance

- **IN:**
  - `repartos/2026-09-21/PromptNoche/Frontend/{Richard,Justin,Leo,Marcelo,Pablo}/PR1x-<Tema>.Frontend/` (encargo + `entregables/` + `evidencia/`).
  - Los cinco `<Persona>-Daily-Noche-2026-09-21.md` del área frontend: se les agrega el segundo bloque.
  - `repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md`: pasa de dos bloques a tres y de 359 a 615 microtareas.
  - `docs/trabajo/2026-09-21-reparto-frontend-rescate/{PLAN.md,REPORTE.md,evidencia/}`.
- **OUT (aunque se vea mejorable):**
  - Los encargos `PR6`–`PR10` (`mantra-core-health`) y los dailies del área `Backend/`: no se editan salvo el daily del equipo, que es uno solo por turno y tiene que consolidar.
  - `tools/check_reparto.py` y `tools/check_skills_citadas.py`: se **usan**, no se modifican. Si un encargo no pasa, se corrige el encargo.
  - El plan madre del frontend: no se renumera ni se recorta. Los encargos referencian sus IDs.
  - Crear un turno nuevo (`2026-09-22`): decidido en contra por Pablo en esta sesión (D-R1).
- **Decisiones tomadas (Pablo, 2026-09-21, en sesión):**
  - **D-R1 · Lote extra, no turno nuevo.** Los cinco encargos se agregan como segundo lote dentro de los carriles `Frontend/` existentes del turno noche del 2026-09-21. Consecuencia asumida: el área frontend pasa a tener **dos repos** (`mantra-core-health` para `PR6`–`PR10`, el monorepo de AportaYa para `PR11`–`PR15`) y el daily del equipo debe declararlo sin ambigüedad, porque las reglas 91 y 98 **sí** aplican al bloque de AportaYa y **no** al de mantra.
  - **D-R2 · Corte por tema técnico.** Es el único corte que deja las reservas de archivos disjuntas: por app, H1 (refresh) y H5 (configuración) tocan las tres apps a la vez y dos personas se pisarían dentro del mismo hito; por fase, los carriles quedan encadenados y nadie puede arrancar hasta que termine el anterior.
- **Ambigüedades registradas:**
  - **Q-R1.** Un trabajo activo por vez (regla 70.1.1) y ahora cada persona del área frontend tiene **tres** bloques en el turno (backend, mantra, AportaYa). Supuesto: el orden es A (backend) → B (mantra) → C (AportaYa), y cada bloque se cierra o se declara `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente; el daily del equipo lo fija. → Confirmar con Pablo si el orden real es otro.
  - **Q-R2.** El turno noche pasa a 615 microtareas repartidas entre cinco personas. Supuesto: el bloque C se escribe **completo y ordenado por dependencia** aunque no entre en un turno (README de `repartos/`), y lo que no se cierre va `A MEDIAS`; recortar alcance es decisión de coordinación y se registra. → Pablo.

## 2. Descubrimiento factual

### 2.1 Hechos (con ruta)

- `tools/check_reparto.py:44-50`: personas `("Richard","Pablo","Marcelo","Justin","Leo")`, turnos `PromptDia|PromptNoche`, áreas `("Backend","Frontend")`; o están las dos carpetas de área o ninguna.
- `check_reparto.py:55-72` exige en **cada** encargo: la cadena `instalación OBLIGATORIA`, `skills-router`, `plan_gate.py --self-test`, `Kill-test`, `Ambigüedades registradas`, un encabezado `#+ .*Definition of Done`, y `**OUT:**`.
- `check_reparto.py:78-84` + `_revisar_capas:200-239`: hitos `^#+ H<n> — `, subtareas `^#+ H<n>.S<m> — `, microtareas en tabla `^\| H<n>.S<m>.M<k> \|`; `**CA:**`, `**DoD:**` y `**Estado:**` se cuentan y tiene que haber **al menos uno por hito y por subtarea**; ninguna subtarea huérfana; ninguna subtarea sin microtareas; estados solo los seis válidos.
- `tools/check_skills_citadas.py`: las skills van en tabla encabezada `| Skill |` con el nombre entre backticks en la primera celda.
- `repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md:3`: `AVANCE DEL TURNO: 0 / 359 — 0 %`; bloque A backend `PasanakuBackend` 213 micro, bloque B frontend **`mantra-core-health` @ `mockup`** 146 micro. Declara explícitamente que en mantra no aplican las reglas 91 ni 98.
- Lotes frontend existentes: `Frontend/{Richard/PR6-SmartPresentational,Justin/PR7-DataTable,Leo/PR8-DialogoYEstados,Marcelo/PR9-InventarioYFamilias,Pablo/PR10-CatalogoYGates}.Frontend/` → los nuevos arrancan en `PR11`.
- Cada daily personal de área (`Frontend/Richard/Richard-Daily-Noche-2026-09-21.md`) ya trae la sección "Tu otro carril de este turno" con la regla 70.1: el patrón para el tercer bloque existe y se copia.
- Plan madre: 15 hitos, 49 subtareas, 247 microtareas (`plan_status.py --path docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md` → `0/247`).

### 2.2 El corte por tema y las reservas (D-R2)

Ningún archivo tiene dos dueños. Lo que un carril necesita de otro se pide como **entrega**, no se escribe en el archivo ajeno.

| Persona | Lote | Del plan madre | Micro | Reserva exclusiva de archivos |
|---|---|---|---:|---|
| **Richard** | `PR11-Sesion.Frontend` | H1, H2, H3 | 51 | `apps/backoffice/src/app/nucleo/{sesion.ts,sesion.interceptor.ts,refresco-de-sesion.ts,auth-bootstrap.ts,permisos.ts,registro-de-acceso.interceptor.ts}`, `apps/backoffice/src/app/app.config.ts`, `apps/backoffice/src/app/rutas/ingreso/**`, `apps/movil/lib/dominio/cliente.dart`, `apps/movil/lib/proveedores/sesion.dart`, E2E `sesion-expirada`, `restaurar-sesion` |
| **Justin** | `PR12-Config.Frontend` | H4, H5, H12.S4 | 36 | `apps/*/src/app/nucleo/gateway.ts` (los dos), `apps/backoffice/src/app/rutas/sistemas/**`, `packages/simulado/**`, `packages/dominio-cliente/src/configuracion.ts`, `apps/movil/lib/dominio/configuracion.dart`, E2E `sistemas-sin-contrato`, `config-invalida` |
| **Leo** | `PR13-Ci.Frontend` | H6, H7, H8, más el paso `f0` de H0.S1.M9 | 52 | `.github/workflows/**`, `.github/CODEOWNERS`, `.github/dependabot.yml`, `package.json` raíz, `scripts/humo.mjs`, `apps/movil/lib/infraestructura/**`, `apps/movil/ios/**`, `apps/movil/pubspec.yaml`, `despliegue/nginx/**`, `apps/*/playwright.config.ts` |
| **Marcelo** | `PR14-Fronteras.Frontend` | H9, H10, H12.S1–S3, H12.S5 | 59 | `packages/{ui,tutoriales,tokens,http-nucleo}/package.json` y sus `exports`, `tsconfig.base.json`, `apps/*/eslint.config.js`, `apps/web/src/server.ts`, `apps/web/src/app/app.routes.ts`, `scripts/verificar_frontend.py`, `apps/movil/test/arquitectura/**` |
| **Pablo** | `PR15-Contratos.Frontend` | H0 global, H11, H13, H14 | 58 | `.gitignore`, `.gitattributes`, `clientes/**`, `docs/auditoria/**`, `docs/Arquitectura/ADR-016` (enmienda), `ADR-047`, `scripts/verificar_remotos.sh`, E2E `autorizacion`, `idempotencia` |

**Entregas entre carriles** (cada una es microtarea en el carril que la recibe, no un permiso para editar):

| Entrega | De | Para | Cómo se cierra sin esperar (regla 65) |
|---|---|---|---|
| `provideFuentesDeSistemas()` y `provideGateway()` cableados en `app.config.ts` | Justin | Richard (dueño del archivo) | Justin prueba sus providers con `TestBed.configureTestingModule({providers:[provideX()]})`; Richard los cablea en una microtarea propia |
| Pasos de CI nuevos (`f6` E2E backoffice, `f0` clientes al día, jobs macOS) | todos | Leo (dueño de `ci.yml`) | Cada uno deja el comando exacto en `entregables/`; Leo lo cablea y pega la salida de `gh run view` |
| `@aportaya/http-nucleo` con traza, errores y telemetría | Marcelo | Richard y Justin | Marcelo publica el package con sus `exports`; hasta entonces los otros importan de su `nucleo/` local y la migración es microtarea de Marcelo |
| `clientes/` versionados | Pablo | todos | Hasta el commit de Pablo, cada uno genera con `./gradlew generateOpenApiClients`; después el clon limpio compila sin JDK |
| Contrato real de `/sesion/refrescar` (cookie, D-A3) | Pablo (H0.S3) | Richard | Richard arranca contra el doble con cookie y declara el peldaño |

### 2.3 Desconocidos
- **D-R1.** Si `check_skills_citadas.py` valida también los dailies o solo los encargos (se resuelve corriéndolo).
- **D-R2.** Si el daily del equipo tiene un formato de bloque que el validador exija (no aparece en `MARCAS_OBLIGATORIAS`, que solo se aplica a los `.md` de tarea; se confirma con la corrida).

## H1 — Los cinco carriles del rescate del frontend existen, validan y no se pisan
**CA:** Dado el turno noche del 2026-09-21, cuando una de las cinco personas abre su carpeta de área frontend, entonces encuentra dos lotes (el de `mantra-core-health` y el nuevo de AportaYa), su daily dice cuántas microtareas tiene cada bloque y en qué orden se trabajan, y ningún archivo del monorepo aparece reservado por dos personas.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21; echo $?` → 0 · `python tools/check_skills_citadas.py; echo $?` → 0 · el script de reservas no encuentra archivos repetidos entre encargos · el daily del equipo suma 615 y el número coincide con la suma de los cinco dailies personales de área.
**Estado:** HECHO

### H1.S1 — Reparto decidido y reservas sin colisión
**CA:** Dado el plan madre de 247 microtareas, cuando se lee la tabla de reparto, entonces cada hito del plan madre tiene exactamente un dueño y cada archivo reservado aparece una sola vez en los cinco encargos.
**DoD:** `python evidencia/check_reservas.py` → `0 colisiones`; la suma de microtareas de los cinco encargos coincide con el total declarado en el daily del equipo.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Escribir en este plan la tabla de reparto por tema (§2.2) con dueño por hito del plan madre | Los 15 hitos del plan madre tienen dueño; ninguno tiene dos | Revisión de §2.2 contra `grep -cE "^## H[0-9]+ " ../2026-09-21-frontend-rescate-hardening/PLAN.md` → 15 hitos cubiertos | HECHO |
| H1.S1.M2 | Escribir la tabla de entregas entre carriles (§2.2) con la vía de cierre sin esperar (regla 65) para cada una | Las 5 entregas tienen columna "cómo se cierra sin esperar" no vacía | Revisión de §2.2: 5 filas completas | HECHO |
| H1.S1.M3 | Escribir `evidencia/check_reservas.py`: extrae las rutas de la sección "Reservas de archivos" de los cinco encargos y reporta colisiones | El script corre y reporta el conteo | `python evidencia/check_reservas.py; echo $?` → 0 con `0 colisiones` | HECHO |

### H1.S2 — Los cinco encargos escritos y validados
**CA:** Dado cada uno de los cinco encargos, cuando lo revisa el validador, entonces tiene las tres capas con CA, DoD y Estado por capa, la sección de instalación del estándar, kill-test, alcance OUT, tabla de ambigüedades, Definition of Done del hito y su tabla de skills.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21` → sin líneas para `PR11`…`PR15`; `python tools/check_skills_citadas.py` → 0.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | `PR11-Sesion.Frontend/RefrescoRestauracionYAuditoria.md` (Richard, H1+H2+H3 del plan madre) | El encargo existe con sus 51 microtareas de tres capas | `grep -cE "^\| H[0-9]+\.S[0-9]+\.M[0-9]+ \|" <encargo>` → 51 | HECHO |
| H1.S2.M2 | `PR12-Config.Frontend/ConfiguracionFailFastYMocksAislados.md` (Justin, H4+H5+H12.S4) | Existe con sus 36 microtareas | mismo `grep` → 36 | HECHO |
| H1.S2.M3 | `PR13-Ci.Frontend/CiRealMacosYReleaseIos.md` (Leo, H6+H7+H8) | Existe con sus 52 microtareas | mismo `grep` → 52 | HECHO |
| H1.S2.M4 | `PR14-Fronteras.Frontend/FronterasNucleoCompartidoYCalidad.md` (Marcelo, H9+H10+H12) | Existe con sus 59 microtareas | mismo `grep` → 59 | HECHO |
| H1.S2.M5 | `PR15-Contratos.Frontend/LineaBaseContratosAuthzYCierre.md` (Pablo, H0+H11+H13+H14) | Existe con sus 58 microtareas | mismo `grep` → 58 | HECHO |
| H1.S2.M6 | Crear `entregables/` y `evidencia/` vacíos en los cinco lotes (el validador exige la carpeta del lote con su `.md`; las dos subcarpetas son el patrón del repo) | Las 10 carpetas existen | `find repartos/2026-09-21/PromptNoche/Frontend -type d -name entregables -o -type d -name evidencia \| wc -l` → 10 | HECHO |
| H1.S2.M7 | Correr `check_reparto.py` sobre el turno y corregir lo que reporte de los cinco lotes nuevos | 0 líneas que nombren `PR11`…`PR15` | `python tools/check_reparto.py repartos/2026-09-21 \| grep -c "PR1[1-5]"` → 0 | HECHO |
| H1.S2.M8 | Correr `check_skills_citadas.py` y corregir toda skill citada que no exista | Sale 0 | `python tools/check_skills_citadas.py; echo $?` → 0 | HECHO |

### H1.S3 — Dailies actualizados y consistentes
**CA:** Dado el daily del equipo, cuando se lee la primera línea, entonces el total del turno es la suma de los tres bloques y cada daily personal de área frontend declara sus dos lotes, su orden y la regla 70.1.
**DoD:** la suma de los cinco dailies personales de bloque C coincide con el número del daily del equipo; `grep` del total en las seis primeras líneas.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Daily del equipo: bloque C con la tabla de las cinco personas, sus encargos, hitos, subtareas y microtareas | La tabla del bloque C tiene 5 filas más la de totales | `grep -A8 "Bloque C" Daily-Noche-2026-09-21.md \| grep -c "^| \*\*"` → 5 | HECHO |
| H1.S3.M2 | Daily del equipo: primera línea pasa a `0 / 615` y el encabezado declara que el área frontend tiene **dos repos** con reglas distintas (91 y 98 aplican solo al bloque C) | La línea 3 dice `0 / 615` y existe la advertencia de los dos repos | `sed -n '3p' Daily-Noche-2026-09-21.md` → contiene `615` · `grep -c "dos repos"` → ≥ 1 | HECHO |
| H1.S3.M3 | Los cinco dailies personales de área frontend: sección "Tus dos lotes de este turno" con el orden A → B → C y el total propio actualizado | Los 5 dailies nombran su lote `PR1x` y su total de bloque C | `grep -l "PR1[1-5]" Frontend/*/[A-Z]*-Daily-Noche-2026-09-21.md \| wc -l` → 5 | HECHO |
| H1.S3.M4 | Verificar la aritmética: suma de los cinco totales de bloque C = 256 y 359 + 256 = 615 | Los dos números cierran | conteo de microtareas sobre los cinco encargos → `bloque C = 256 · turno = 615` | HECHO |

### H1.S4 — Cierre del reparto
**CA:** Dado alguien que no vio esta sesión, cuando abre el turno, entonces los dos validadores salen 0 y el `REPORTE.md` de este trabajo dice qué quedó escrito, qué no se verificó y qué ambigüedades se arrastran.
**DoD:** las dos salidas pegadas en `evidencia/`; `REPORTE.md` con las tres secciones y el avance calculado en la primera línea.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S4.M1 | Pegar en `evidencia/` la salida literal de `check_reparto.py`, `check_skills_citadas.py`, `check_reservas.py` y del conteo de microtareas | Los 4 archivos existen con su `exit=` | `ls evidencia/*.txt \| wc -l` → ≥ 4 | HECHO |
| H1.S4.M2 | No regresión del reparto anterior: `check_reparto.py repartos/2026-09-20` sigue saliendo 0 | Sale 0 | `python tools/check_reparto.py repartos/2026-09-20; echo $?` → 0 | HECHO |
| H1.S4.M3 | Escribir `REPORTE.md` con las tres secciones, el avance calculado y las ambigüedades Q-R1/Q-R2 | `report_gate.py` no bloquea | `python .claude/hooks/report_gate.py --self-test < /dev/null; echo $?` → 0 y el reporte con las tres secciones | HECHO |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El área frontend queda con dos repos y alguien aplica las reglas de mantra (sin 91/98) al bloque de AportaYa | Un cambio de dinero sin las prohibiciones de la regla 91 | El daily del equipo y los cinco encargos lo declaran en el encabezado; cada encargo de AportaYa lista 91 y 98 en "Reglas que aplican con prioridad" |
| 615 microtareas en un turno de cinco personas | Expectativa irreal; tentación de marcar `HECHO` sin DoD | README de `repartos/`: el encargo se escribe completo y ordenado por dependencia; lo que no entra va `A MEDIAS` con las cuatro respuestas. Recortar es decisión de coordinación y se registra (Q-R2) |
| Tres bloques por persona y un solo trabajo activo (regla 70.1.1) | Dos carriles abiertos a la vez | Orden A → B → C declarado en los seis dailies; el anterior se cierra o queda `A MEDIAS` antes de abrir el siguiente (Q-R1) |
| Las entregas entre carriles se vuelven espera | Carriles bloqueados unos por otros | Cada entrega trae su vía de cierre contra un doble (regla 65) en §2.2; ningún carril puede declararse `BLOQUEADO` por esperar a otro |
| `app.config.ts` y `ci.yml` los necesitan varios | Dos personas en el mismo archivo | Dueño único declarado (Richard y Leo); los demás entregan el comando/provider y la microtarea de cableado vive en el carril del dueño |
| El plan madre se renumera al repartirlo y se pierde la trazabilidad | Nadie puede cruzar encargo ↔ plan madre | Cada microtarea del encargo cita su ID del plan madre en la columna "Microtarea" (`(madre H1.S2.M1)`) |
