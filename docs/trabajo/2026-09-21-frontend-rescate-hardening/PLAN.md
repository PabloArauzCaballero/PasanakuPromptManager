# Plan — PasanakuFrontend (AportaYa): rescate, refactorización y hardening de `apps/` y `packages/`

- Fecha: 2026-09-21 · Repos afectados: `PabloArauzCaballero/PasanakuFrontend` (rama `dev`), este repo (solo `docs/trabajo/`) · Predecesor: `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (mismo árbol, otro remoto; ese plan declara `apps/`, `packages/`, `landing/` como OUT — este plan los toma)
- **SHA inicial de `PasanakuFrontend@dev`: `19a621e666afdea5bdc40aced326d3f212a116f4`** (2026-09-21 19:22 UTC, "fix: los fronts no construian — el paquete de tutoriales no entraba en la imagen"). Único branch del remoto: `dev`. **Es el mismo commit que el código de `PasanakuBackend@dev`**: ambos remotos comparten el árbol completo (Gradle, `sql/`, `servicios/`, `apps/`, `packages/`). `PasanakuBackend@dev` ya está en `5d7948e` (= `19a621e6` + `docs/auditoria-produccion/`): **los dos remotos ya divergieron** en documentación.
- Resultado observable: quien despliegue `dev` del frontend contra el gateway real obtiene (a) un backoffice que ante N `401` simultáneos hace **un** refresh y no cierra la sesión de más; (b) un F5 sobre una ruta protegida que **restaura la sesión** desde la cookie HttpOnly antes de decidir mandar al login; (c) tres apps que **se niegan a arrancar/construir** en producción si la URL del gateway falta o apunta a `localhost`; (d) pantallas de `sistemas/` que muestran **error real** y no datos inventados cuando el contrato no existe; (e) un `yarn humo` que **falla** si una colección obligatoria falla; (f) un CI que corre lint, typecheck, unit, a11y, build y **E2E del backoffice**; (g) ocho documentos en `docs/auditoria/` que responden con hechos qué partes del frontend son confiables y cuáles no. Todo con salida literal pegada.
- Kill-test: en el backoffice compilado, abrir DevTools, simular expiración del access token y disparar 10 peticiones a la vez → hoy salen **10 `POST /sesion/refrescar`** (`sesion.interceptor.ts:28-32` hace el refresh dentro del propio `HttpClient` interceptado, sin single-flight). Segundo kill-test: `yarn humo` con una colección rota → hoy sale código 0 (`package.json:21`, `|| true`). Si al cerrar cualquiera de los dos sigue así, esto NO está hecho.

## 0. Cómo se ejecuta este plan

| Tema | Regla para este trabajo |
|---|---|
| Dónde vive | Se redacta acá. En **H0.S1.M6** se copia a `docs/auditoria/plan-de-remediacion.md` del monorepo (el nombre que exige el metaprompt §43) y desde ahí se actualiza en el momento; este archivo queda como espejo. Al cierre, `REPORTE.md` acá (regla 40) + `docs/auditoria/verificacion-final.md` en el repo (metaprompt §50), con el mismo avance. |
| Evidencia | Canónica en `docs/auditoria/evidencia/<ID>-<slug>.txt` del monorepo (salida literal, recortada, **sin datos de personas ni tokens**). Capturas en `evidencia/<ID>-<viewport>-<tema>.png`. Este repo enlaza, no duplica. |
| Hallazgos | Cada defecto confirmado se registra en `docs/auditoria/hallazgos.md` con el formato §44 del metaprompt (`F-XXX`, severidad, archivo, estado, evidencia, causa raíz, corrección, pruebas, resultado). El ID del hallazgo se cita en la microtarea que lo corrige. |
| Estados | Exactamente los seis de la regla 20. `HECHO` solo con la salida del DoD pegada. Avance = `microtareas HECHO / total` (`python .claude/hooks/plan_status.py`). |
| Orden | El del metaprompt §42: H0 → H1–H7 (P0, Fase 1) → H8 (Fase 2) → H9–H11 (Fase 3) → H12 (Fase 4) → H13 (§31) → H14 (Fase 5). **Ningún refactor cosmético (H12) antes de cerrar H1–H7.** |
| Una microtarea a la vez | Una sola en `EN CURSO`. Un commit atómico por microtarea o subtarea coherente, con el prefijo del metaprompt §45 indicado en cada fila (`fix(auth)`, `fix(config)`, `fix(ci)`, `refactor(boundaries)`, `test(auth)`, `docs(audit)`…). |
| Por cada fix (§37) | Test de caracterización → refactor → test del comportamiento nuevo → verificación. Ningún contrato público se cambia sin registrar la decisión en `docs/auditoria/decisiones.md`. |
| Fail closed | Si algo depende del backend real que no existe (auditoría server-side, contrato de `sistemas/`): **no se inventa el endpoint** (§6). Se aísla el contrato y se simula en tres niveles (regla 65) declarando el doble, y se registra la brecha en `docs/auditoria/brechas-backend.md`. |
| Rama y remotos | **D-A2:** un solo árbol; remoto canónico `PasanakuBackend` (va adelante: `5d7948e`). `PasanakuFrontend@dev` se mantiene como espejo por **fast-forward** hasta que Pablo lo archive (acción sobre recurso compartido: la ejecuta él). Cada push de este plan va a `PasanakuBackend@dev` y en el mismo paso hace fast-forward de `PasanakuFrontend@dev` (H13.S1.M6). No se tocan settings remotos de GitHub (§12) salvo los *secrets* del release iOS, que se listan y carga Pablo (H6.S3.M3). |
| Recursos (regla 70) | Un `yarn`/`flutter`/`gradle` a la vez; Playwright con `workers: 1` (ya está así en `apps/backoffice/playwright.config.ts:14`); un navegador; el servidor del backoffice para E2E se levanta a mano y se baja al cerrar el turno. |
| Máquina | Windows 11 sin `java`, `flutter`, `dart` en PATH (verificado con `command -v`). H0.S1 instala lo que falte o declara `BLOQUEADO` con qué lo destraba. `generateOpenApiClients` necesita JDK 21 (es una tarea Gradle): sin él no hay `clientes/angular` ni `clientes/dart` y las apps no compilan. |

## 1. Alcance

- **IN:**
  - `apps/web`, `apps/backoffice`, `apps/movil`, `packages/{ui,tokens,tutoriales,dominio-cliente,simulado,diseno_flutter}`, `scripts/verificar_frontend.py`, `scripts/verificar_maqueta.py`, el job `frontend` de `.github/workflows/ci.yml`, `package.json` raíz (scripts `humo`), `turbo.json`, `tsconfig.base.json`, `.yarnrc.yml`, `despliegue/coolify/backoffice.yml` y `despliegue/nginx/aportaya.conf` **solo en lo que sirve HTML del frontend** (cabeceras, `<meta aportaya-gateway>`), `docs/auditoria/**` (nuevo), `docs/Arquitectura/ADR-04x` nuevos que este plan decida.
  - La generación de clientes OpenAPI **del lado consumidor** (`clientes/angular`, `clientes/dart`, `apps/movil/scripts/generar-clientes.sh`, `buildSrc/.../aportaya.openapi.gradle.kts` solo en `configOptions` del generador TS/Dart).
  - Los ocho documentos del metaprompt §43.
- **OUT (aunque se vea roto):**
  - `servicios/**`, `plataforma/**`, `sql/**`, `buildSrc/**` fuera del archivo de openapi arriba, `despliegue/compose/**`, `landing/**` (Astro, otro producto según ADR-041), `postman/**` salvo el script `humo` de `package.json`.
  - Cualquier endpoint nuevo en el backend: la auditoría server-side (§6) y el contrato de `sistemas/` (§7) se **documentan como brecha**, no se implementan del lado Java.
  - Split de repositorios, protección de ramas remota, CODEOWNERS **aplicado** (se escribe el archivo `.github/CODEOWNERS` porque es un archivo del repo, pero que GitHub lo haga cumplir exige "Require review from Code Owners" en protección, que es OUT).
  - Upgrades mayores (Angular 22 → 23, Flutter, TypeScript 6): §41 separa `security patch` de `framework migration`. Solo parches de seguridad con advisory citado.
  - Goldens de Flutter: no se regeneran (baseline macOS, CI Linux, `turbo.json` "//" lo declara). Se documenta.
  - Contenido regulatorio **en sí** (tarifas, estado regulatorio): se centraliza la **estructura** con trazabilidad; los valores los confirma negocio/cumplimiento (regla 97.5.4).
- **Decisiones tomadas sobre las ambigüedades (2026-09-21, Pablo, en sesión; detalle en `docs/auditoria/decisiones.md` al copiar el plan):**
  - **D-A1 · `clientes/` debe existir.** Los clientes generados (`clientes/angular/*`, `clientes/dart/*`) pasan a **versionarse** en git (hoy `.gitignore:49-50` los ignora y solo existen tras `./gradlew generateOpenApiClients`). Se enmienda ADR-016: el gate deja de ser "compila" y pasa a ser "regenerar no produce diff" en CI. Consecuencias: el frontend compila sin JDK; el determinismo de la generación (§21) se demuestra con `git diff --exit-code`; un contrato cambiado sin regenerar pone el CI en rojo. → H0.S1.M7–M9, H11.S3.M4.
  - **D-A2 · Un solo árbol, un remoto canónico.** `PasanakuFrontend` es el mismo monorepo que `PasanakuBackend` bajo otro remoto y ya divergió. Canónico: `PasanakuBackend` (tiene el plan del backend y va adelante). `PasanakuFrontend@dev` se sincroniza por fast-forward en cada push de este plan y se recomienda archivarlo (o renombrar el canónico a un nombre neutro, p. ej. `aportaya`); archivar o renombrar lo ejecuta Pablo. → §0 "Rama y remotos", H13, H14.S1.M5.
  - **D-A3 · El refresh web es por cookie HttpOnly.** Backoffice y sitio refrescan con `POST /sesion/refrescar` sin cuerpo y `withCredentials: true`; el token de refresh **nunca** llega al JavaScript. El móvil guarda el refresh en `AlmacenSeguro` y lo manda en el cuerpo (no hay cookie jar confiable en la app). Si `identidad.yaml` no ofrece el modo cookie (H0.S3.M2), es **brecha del backend** (`brechas-backend.md`) y H1/H2 se construyen y verifican contra un doble que cumple el contrato con cookie (regla 65), declarándolo. → H1, H2, H8.S5.M5.
  - **D-A4 · Jobs `macos-latest` definitivos.** Goldens de Flutter e `integration_test/` (patrol) corren en CI en jobs macOS separados del job `frontend` Linux, con simulador iOS. El costo en minutos se acepta. → H8.S2.M2, H8.S2.M3.
  - **D-A5 · Hay release iOS en macOS, sí o sí.** Se agrega la subtarea H6.S3: job `ios-release` en `macos-latest` que corre el gate de capabilities, las pruebas en simulador y `flutter build ipa --release`; produce el IPA como artefacto en cada corrida de `dev`; la firma y la subida a TestFlight se activan cuando existan los *secrets* de App Store Connect (los carga Pablo; el paso se marca `skipped` explícito mientras no estén, nunca finge). → H6.S3.
  - **D-A6 · Hosts permitidos sin lista externa en web.** En producción, web y backoffice exigen gateway **same-origin**: `/api/v1` relativo (lo que ya inyecta `server.ts:101`) o absoluto `https://` con host igual a `location.host`; cualquier otro host es configuración inválida. El móvil exige `--dart-define=API=https://…` con host contenido en `--dart-define=API_HOSTS=<lista>` compilada en release; ambos defines obligatorios. Infra (Leo) fija los valores en Coolify. → H5.
- **Ambigüedades abiertas:** ninguna al 2026-09-21. Las que aparezcan en ejecución se agregan acá con supuesto y destinatario.

## 2. Descubrimiento factual (Fase 1) — contra el SHA `19a621e6`

Hecho contra el clon local de `PasanakuBackend` (`Entrypoint-GitHUb/Pasanaku/PasanakuBackend`), cuyo árbol de `apps/`, `packages/`, `scripts/`, `.github/` es idéntico al SHA del frontend (`git diff --stat 19a621e6 HEAD` → solo 4 archivos bajo `docs/auditoria-produccion/`).

### 2.1 Hechos (con ruta)

**Monorepo y toolchain**
- Yarn 4.18.0 con `nodeLinker: node-modules` y `enableTransparentWorkspaces: false` (`.yarnrc.yml`); workspaces `apps/*` y `packages/*` (`package.json:6-9`). Node `>=22`. Turbo 2.10 orquesta `contenido → typecheck/lint/test:front/test:a11y/build/test:e2e`; `test:goldens` **fuera** del CI por decisión escrita (`turbo.json` clave `//`).
- Angular `^22.1.0` y TypeScript `~6.0.2` en `apps/web`, `apps/backoffice`, `packages/ui`, `packages/tutoriales`; TypeScript `~5.9.2` en `packages/tokens`, `packages/dominio-cliente`, `packages/simulado` y raíz (`package.json` de cada uno). **Dos majors de TS conviven** (§30).
- Flutter 3.44.8 en CI (`ci.yml` job `frontend`, `subosito/flutter-action`), Riverpod 3, go_router 17, dio 5.7, flutter_secure_storage 10, connectivity_plus 7, mobile_scanner 7, patrol 3.15 (`apps/movil/pubspec.yaml`).
- `apps/movil/lib/`: `dominio/`, `infraestructura/`, `navegacion/`, `pantallas/`, `proveedores/` (152 `.dart`); tests: 31 archivos (`unidad`, `widget`=9, `contrato`=1, `a11y`=2, `identidad`, `pasanaku`, `goldens`) + 7 `integration_test/*_test.dart` (patrol).
- Máquina de planificación: node 22.23.1, yarn 4.18.0, python 3.14.2, gh 2.97 (autenticado como dueño), Docker 29.6.2; **sin `java`, `flutter`, `dart`**.

**Clientes OpenAPI**
- 14 contratos en `servicios/<svc>/src/main/resources/openapi/<svc>.yaml`. `buildSrc/src/main/kotlin/aportaya.openapi.gradle.kts` genera `typescript-angular` a `clientes/angular/<svc>` y `dart-dio` a `clientes/dart/<svc>`; ambas carpetas en `.gitignore:49-50` ("el gate es la compilación, no un diff", ADR-016). `tsconfig.base.json:26` mapea `clientes/angular/*`. `apps/movil/pubspec.yaml` depende por `path` de 11 clientes Dart; `apps/movil/scripts/generar-clientes.sh` corre `build_runner` en cada uno.
- CI: `f0 · ./gradlew generateOpenApiClients --no-parallel --no-build-cache -q` antes de `yarn install` (`ci.yml:200-266`).

**Autenticación — backoffice** (`apps/backoffice/src/app/nucleo/`)
- `sesion.ts:11`: access token en `signal` en memoria; `abierta = computed(() => acceso() !== null)` (`:22`). No hay estado `RESTORING`/`UNKNOWN`: solo abierta/cerrada.
- `sesion.interceptor.ts:16-49`: ante `401` sin `YA_REINTENTADA`, hace `http.post(`${gateway}/sesion/refrescar`, {}, {withCredentials: true})` **con el mismo `HttpClient` inyectado** (`:18,:28`) → el refresh pasa por la cadena completa de interceptores (`app.config.ts:21`: `traza, sesion, idempotencia, registroDeAcceso, errores`). **No hay single-flight**: cada `401` concurrente dispara su propio refresh. Si el segundo intento falla, `sesion.cerrar()` (`:43`) — N veces ante N fallos.
- `permisos.ts:24-29`: `requiereSesion()` devuelve `parseUrl('/ingreso')` si `!abierta()` **de forma síncrona**, sin intentar restaurar. **Nadie llama a `/sesion/refrescar` al arrancar**: grep de `abrirConToken|sesion/refrescar|provideAppInitializer` en `apps/backoffice/src` → solo el interceptor (`:29`) y `pantalla-de-ingreso.ts:126`. → **F5 en ruta protegida = login, siempre** (§5 confirmado).
- `sesion.ts:61-72` decodifica claims del JWT sin verificar firma, solo para UX (documentado).
- No existe `sesion.interceptor.spec.ts` ni `sesion.spec.ts` (`ls apps/backoffice/src/app/nucleo/*.spec.ts` → `permisos.spec.ts`, `secciones.spec.ts`). 66 specs en backoffice (23 a11y), 12 en web (2 a11y).

**Autenticación — móvil** (`apps/movil/lib/`)
- `dominio/cliente.dart:48-107`: `_TrazaYSesion` hace `_dio.post('/sesion/refrescar', data: {'refresco': refresco})` **con el mismo `Dio`** (`:93`), sin mutex: N `401` → N refresh; cada uno guarda `acceso`+`refresco` (`:101`), con rotación en el backend el segundo refresh usa un token ya rotado y falla → `cerrar()` (`:75`). No hay test de refresh (`grep -rln refrescar apps/movil/test` → solo pantallas de saldo).
- `proveedores/sesion.dart`: tokens en `AlmacenSeguro` (puerto), nunca `SharedPreferences`. Correcto.
- `cliente.dart:20-23`: `baseDelGateway = String.fromEnvironment('API', defaultValue: 'http://localhost/api/v1')` → **fallback a localhost en cualquier build**, incluido release (§8 confirmado). Timeouts explícitos 8 s/12 s (`:30-31`). `x-request-id` generado con `Random()` no seguro (`:146-152`), aceptable para traza.

**Auditoría de lectura** — `registro-de-acceso.interceptor.ts:20-43`: tras el éxito de la lectura, `http.post(`${gateway}/extraccion/accesos`, {recurso, id, rutaId: req.urlWithParams})` con `.pipe(catchError(() => of(null))).subscribe()` — **fire-and-forget, error tragado** (§6 confirmado). Además `rutaId` manda la URL con query completa (`:32`): si la URL llevara un identificador de persona, viajaría al log de accesos (regla 90.2.2, a verificar en H3.S1.M2).

**Datos simulados** — `apps/backoffice/src/app/rutas/sistemas/dominio/datos-simulados.ts` (138 líneas): declara el hueco en cabecera (`:1-14`: no existe contrato OpenAPI de indicadores/tablero); exporta `serviciosSimulados`, `desplieguesSimulados`, `interruptoresSimulados`, `migracionesSimuladas`, `respaldosSimulados`, `proveedoresSimulados`, `outboxSimulado`, `descartadosSimulados`, `webhooksSimulados`, `accesosSimulados`, `incidentesSimulados` + dos funciones puras (`puedeConfirmar`, `restauracionVencida`). **Nueve pantallas lo importan directo** (`rutas/sistemas/{accesos,base-datos,despliegues,incidentes,outbox,proveedores,respaldos,servicios,webhooks}/pantalla-*.ts`). Sin flag de entorno, sin banner, sin puerto: el mismo bundle de producción muestra `nucleo-financiero 99.95%` como si fuera real (§7 confirmado).

**Configuración del gateway**
- `apps/backoffice/src/app/nucleo/gateway.ts:7-10`: `meta[name=aportaya-gateway]` **o** `'http://localhost:4010/api/v1'`. `apps/web/src/app/nucleo/gateway.ts:7-11`: `process.env.APORTAYA_GATEWAY` **o** meta **o** `'http://localhost:4010/api/v1'`. Ambos se proveen como `useValue` en `app.config.ts` (backoffice `:23`, web `:19`). Sin validación de protocolo/host/entorno (§8 confirmado).
- El backoffice se despliega como imagen `aportaya/backoffice:test` (`despliegue/coolify/backoffice.yml:24`); **no se encontró quién inyecta el `<meta aportaya-gateway>`** en el HTML del backoffice (grep en `despliegue/` → solo `container_name: aportaya-gateway`; `nginx/aportaya.conf` no tiene `sub_filter`). → Desconocido D2.

**SSR / proxy** — `apps/web/src/server.ts`: Express + `AngularNodeAppEngine`; si `APORTAYA_GATEWAY_INTERNO` está definida, monta un **reverse proxy en `/api`** con `fetch` (`:53-91`): quita `host, connection, content-length, transfer-encoding` (`:54`) pero **no** `keep-alive`, `te`, `trailer`, `upgrade`, `proxy-*`; **sin timeout ni `AbortSignal`**, sin límite de cuerpo, `redirect: 'manual'` sin reescribir `Location`, sin request-id, sin log estructurado; inyecta `<meta aportaya-gateway content="/api/v1">` (`:100-105`). Comentarios de plantilla de Angular CLI intactos (`:15-25`, `:126-129`, `:141-143`). `console.log` en `:137`. Sin test. → Es un **BFF accidental** (§17 confirmado).

**Idempotencia** — `idempotencia.interceptor.ts`: clave por `HttpContextToken`, generada por el formulario al abrirse (`claveDeIdempotencia()` = `crypto.randomUUID()`), no se regenera en el reintento del `sesionInterceptor` (el `req.clone` conserva `context`). Correcto en diseño; **sin test** de doble click / retry-tras-refresh / F5 (§20).

**Autorización UI** — `permisos.ts:10-17` `requierePermiso` por `canMatch` (`app.routes.ts:24-56`); `shell-financiero.ts:13` declara que el servidor decide. `alcanza()` en `secciones.ts` con spec. Falta E2E de deep link sin permiso y de `403` del servidor (§19). E2E backoffice existentes: `accesibilidad.e2e.ts`, `tablero-y-permisos.e2e.ts`, `tutoriales.e2e.ts` (`apps/backoffice/e2e/`).

**Pruebas y CI**
- `package.json:21`: `humo` itera `postman/humo/*.json` con `|| true` → **nunca falla** (§10 confirmado). `ci.yml:150`: `grep -q "FALLA" humo.txt && exit 1 || true` (en job `base`, fuera de este alcance salvo por el script raíz).
- Job `frontend` (`ci.yml:200-265`, `needs: [codigo]`): `generateOpenApiClients` → `verificar_maqueta.py` → `yarn install --immutable` → builds de tokens/simulado/diseno-flutter/movil → `yarn lint` + `yarn typecheck` → `yarn test:front` → `yarn test:a11y` → build backoffice + web + chequeo `noindex` → **solo `@aportaya/web test:e2e`**. **El E2E del backoffice no corre en CI** (§11 confirmado). `apps/backoffice/playwright.config.ts:17-19`: sin `webServer`, "se levanta a mano".
- **Estado real en el remoto** (`gh run list -R …/PasanakuFrontend`): `CI` en **failure** en `19a621e6` y en `4bf13974`; falla en el job `codigo` (Spotless, según el plan del backend §2.1), por lo que `frontend` queda `skipped`. **Nunca se ejecutó el job `frontend` en verde en `dev` en las últimas corridas.**
- Protección de ramas: `gh api …/PasanakuFrontend/branches/dev/protection` → **403 "Upgrade to GitHub Pro or make this repository public"** (repo privado en plan gratuito: la protección de ramas clásica **no está disponible**; hay que evaluar rulesets). Sin `.github/CODEOWNERS`, sin `dependabot.yml`.
- `eslint-plugin-boundaries ^5.0.0` está en `devDependencies` de `apps/web` y `apps/backoffice` (`package.json:37,:46`) pero **no aparece en ningún `eslint.config.js`** (grep vacío) → instalado, no configurado. Lo único vigente: `no-restricted-globals: fetch` (`apps/backoffice/eslint.config.js:16`).
- `scripts/verificar_frontend.py` (172 líneas): barridos regex por app: "sin red en vista", "sin literal de diseño", "sin formato de dinero", "sin plataforma en vista", "sin print/console". Se invoca desde `lint` de cada workspace. Es el único enforcement de fronteras hoy (§15 confirmado).

**Fronteras de packages** — `@aportaya/ui` y `@aportaya/tutoriales` exportan `"./*": "./src/*"` (`packages/ui/package.json`, `packages/tutoriales/package.json`) y `tsconfig.base.json:24-25` mapea `@aportaya/ui/*` → `packages/ui/src/*`: **todo `src/` es API pública** (§13 confirmado). `@aportaya/tokens` sí tiene exports explícitos (`./tokens.json`, `./tokens.css`, `./dinero`, `./vectores/monto.json`). `@aportaya/dominio-cliente` exporta solo `.` (`src/index.ts`).

**Duplicación web/backoffice** — `nucleo/traza.interceptor.ts` (11 líneas) **idéntico** en ambas apps (`diff` vacío); `nucleo/errores.interceptor.ts` (23 líneas) idéntico; `nucleo/errores.ts` difiere solo en 6 códigos `AP-CU04-*` del backoffice; `nucleo/gateway.ts` casi idéntico (§16 confirmado).

**Dinero** — `packages/tokens/dinero/formatear.ts` es el formatter único exportado (`@aportaya/tokens/dinero`) con vectores `vectores/monto.json`. Grep de `parseFloat|toFixed|double.parse|toStringAsFixed` en `apps/` → 1 hit permitido y comentado (`apps/movil/lib/dominio/validacion.dart:24`). El regex de `verificar_frontend.py:58,:82,:115` lo vigila.

**Paridad iOS** — `apps/movil/lib/infraestructura/plataforma.dart:33-60`: `AlmacenSeguro` y `Haptica` tienen adaptador iOS; `Conectividad`, `Biometria`, `AvisosPush`, `ProteccionPantalla` devuelven **siempre el adaptador Android** (`:36,:41,:43,:59-60`), documentado como "hueco declarado" (`:27-32`). `apps/movil/ios/Runner/` tiene `AppDelegate.swift` y `SceneDelegate.swift` **sin ningún `FlutterMethodChannel`** (grep vacío) → los `MethodChannel` Android no tienen receptor en iOS (§9 confirmado). Cámara compartida vía `CamaraDelSistema`; `CamaraPrestada` solo con `--dart-define=CAMARA_DEV` (`:53-57`).

**Cabeceras HTTP** — `despliegue/nginx/aportaya.conf:14-16`: `X-Content-Type-Options`, `X-Frame-Options DENY`, `Referrer-Policy no-referrer`. **Sin CSP, sin HSTS, sin Permissions-Policy, sin `Cache-Control` para el backoffice** (§18). El `noindex` del backoffice se verifica en CI (`ci.yml` paso f4).

**Routing/contenido** — `apps/web/src/app/app.routes.ts` (182 líneas) mezcla rutas con 26 bloques `titulo/descripcion` de SEO/JSON-LD inline (§27 confirmado, severidad P2). Rutas del backoffice repartidas en 6 archivos `*.routes.ts` de 34-65 líneas: sanas.

**Documentación previa** — ADR-044 (Angular + Flutter, 2026-09-09) y ADR-036 (Android primero, iOS por pase); `planes/informes/carril-B{1..5}.md` y `_plantilla-frontend.md` (informes de carriles frontend previos); `docs/Frontend/`. **No existe `docs/auditoria/`** (sí `docs/auditoria-produccion/` del backend).

### 2.2 Desconocidos (se resuelven en H0 con comando y salida)
- **D1.** Resultado real de `yarn lint`, `yarn typecheck`, `yarn test:front`, `yarn test:a11y`, `yarn build`, `test:e2e` (web y backoffice) y `flutter test`/`dart analyze` en el SHA. El job `frontend` nunca corrió en `dev` en las corridas visibles.
- **D2.** Cómo llega `<meta name="aportaya-gateway">` al `index.html` del backoffice desplegado (Dockerfile de la imagen `aportaya/backoffice`, ¿dónde vive?). El commit `19a621e6` habla de "la imagen" de los fronts: hay que localizar el Dockerfile (¿en `despliegue/coolify/`? ¿generado?).
- **D3.** Contrato real de `POST /sesion/refrescar` en `identidad.yaml`: ¿cookie o cuerpo? ¿rota el refresh? ¿qué devuelve (`acceso`, `permisos`, `rol`)? Los dos clientes lo llaman distinto (ver A3).
- **D4.** Si `POST /extraccion/accesos` existe en algún `openapi/*.yaml` y qué exige (`rutaId`, `x-request-id`).
- **D5.** Qué hace `scripts/verificar_maqueta.py` y de qué "plan" y "maqueta" habla.
- **D6.** Cuántas pantallas del backoffice y de la web resuelven los cuatro estados (cargando/datos/vacío/error): hoy solo se sabe que `sistemas/` no tiene error posible porque nunca llama a la red.
- **D7.** Si `flutter build ios` compila siquiera sin Mac (no: exige Xcode). Qué parte de la paridad iOS se puede verificar en Windows/Linux (solo `dart analyze` + tests de capability con `debugDefaultTargetPlatformOverride`).
- **D8.** `yarn npm audit` / `flutter pub outdated` en el SHA: advisories reales.
- **D9.** Si el plan gratuito del repo privado permite **rulesets** (`gh api repos/…/rulesets`) aunque no permita branch protection clásica.

### 2.3 Hipótesis (nunca presentadas como hecho)
- **H-1.** El refresh concurrente en el backoffice hoy "funciona" en la práctica porque el gateway acepta varios refresh con la misma cookie mientras no rote; el día que `identidad` rote el refresh (trigger R-SEG-09 del backend: "reusarlo revoca la familia entera"), **N refresh concurrentes cierran la sesión de todos**. A confirmar en D3.
- **H-2.** El E2E del backoffice no corre en CI porque necesita backend real o Prism con sesión, y nadie cableó el `webServer` (comentario en `playwright.config.ts:17-20`).
- **H-3.** El `<meta aportaya-gateway>` del backoffice lo inyecta NGINX dentro de la imagen del front (no en `despliegue/nginx/aportaya.conf`), y esa imagen se construye desde un Dockerfile que no está en el árbol o está en `landing/`/`despliegue/coolify/`.
- **H-4.** `eslint-plugin-boundaries` se agregó a `devDependencies` en un carril anterior con intención de configurarlo y quedó a medias.

### 2.4 Revalidación de los problemas del metaprompt en `19a621e6`

| § | Problema | Estado en el SHA | Evidencia | Hito |
|---|---|---|---|---|
| 4 | Refresh concurrente (backoffice, móvil) | **VIGENTE** en ambos | `sesion.interceptor.ts:18,28`; `cliente.dart:93` | H1 |
| 5 | Restauración de sesión al F5/deep link | **VIGENTE** | `permisos.ts:26`; sin initializer | H2 |
| 6 | Auditoría fire-and-forget desde el navegador | **VIGENTE** | `registro-de-acceso.interceptor.ts:29-39` | H3 |
| 7 | Datos simulados en pantallas operativas | **VIGENTE**, sin flag ni banner | `datos-simulados.ts`; 9 importadores | H4 |
| 8 | Fallback a localhost | **VIGENTE** en las 3 apps | `gateway.ts:9` (bo), `:10` (web), `cliente.dart:22` | H5 |
| 9 | Paridad iOS fingida | **VIGENTE** (4 de 7 puertos) | `plataforma.dart:36,41,43,59`; sin canales en `ios/Runner` | H6 |
| 10 | `\|\| true` en humo | **VIGENTE** | `package.json:21` | H7 |
| 11 | CI incompleto (E2E backoffice) | **VIGENTE** | `ci.yml` paso f5 solo web | H8 |
| 12 | Protección de rama | **VIGENTE**, además **no disponible** en plan gratuito | `gh api` → 403 | H8 |
| 13 | `src/*` como API pública | **VIGENTE** (`ui`, `tutoriales`) | `package.json` exports `./*` | H9 |
| 14–15 | Boundaries por regex | **VIGENTE**; plugin instalado sin configurar | `verificar_frontend.py`; `eslint.config.js` | H9 |
| 16 | Duplicación web/backoffice | **VIGENTE** (4 archivos) | `diff` de `nucleo/` | H10 |
| 17 | Proxy accidental en SSR | **VIGENTE** | `server.ts:53-91` | H10 |
| 18 | Cabeceras HTTP | **PARCIAL** (3 de ~8) | `nginx/aportaya.conf:14-16` | H8 |
| 19–21 | Autorización, idempotencia, OpenAPI | Diseño correcto, **sin tests dirigidos** | `permisos.ts`, `idempotencia.interceptor.ts` | H11 |
| 25 | Dinero | **OK** (formatter único + regex) | `packages/tokens/dinero/` | H12 (solo test de caracterización) |
| 27 | Routing gigante | **VIGENTE** solo en `apps/web/app.routes.ts` | 182 líneas, 26 bloques SEO | H12 |
| 30 | Toolchain | **VIGENTE** (TS 5.9 y 6.0) | `package.json` de cada workspace | H12 |
| 31 | Fronteras de repo | **VIGENTE y agravado**: dos remotos, mismo árbol, ya divergidos | `gh api commits/dev` en ambos | H13 |

---

## H0 — Línea base reproducible: se sabe qué falla antes de tocar código (Fase 0, §42)
**CA:** Dado el SHA `19a621e6` clonado en limpio, cuando alguien lee `docs/auditoria/frontend-baseline.md`, entonces encuentra para cada comando del pipeline frontend (generar clientes, install, lint, typecheck, unit, a11y, build ×2, E2E ×2, `flutter analyze`, `flutter test`) su salida literal y su código de salida, y una lista de hallazgos `F-xxx` con estado `ABIERTO`.
**DoD:** `docs/auditoria/frontend-baseline.md` y `hallazgos.md` commiteados en `dev` · cada comando con `echo $?` pegado en `evidencia/H0-*.txt` · `python .claude/hooks/plan_status.py` muestra el plan copiado.
**Estado:** TODO

### H0.S1 — Entorno y clon de trabajo
**CA:** Dado Windows sin `java`/`flutter`/`dart`, cuando termina la subtarea, entonces existe un clon de `PasanakuFrontend@dev` con toolchain suficiente para correr el job `frontend` del CI localmente, o cada herramienta faltante está declarada `BLOQUEADO` con qué la destraba.
**DoD:** salidas de `java -version`, `flutter --version`, `dart --version`, `node -v`, `yarn -v` pegadas · `git ls-files clientes/` no vacío (D-A1).
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H0.S1.M1 | Clonar `PasanakuFrontend` rama `dev` con `core.longpaths=true` en `Entrypoint-GitHUb/PasanakuFrontend` | El clon existe y `git rev-parse HEAD` = `19a621e6…` | `git -C PasanakuFrontend rev-parse HEAD` → `19a621e666afdea5bdc40aced326d3f212a116f4` | TODO |
| H0.S1.M2 | Instalar JDK 21 (Temurin) para poder correr `./gradlew generateOpenApiClients` | `java -version` reporta 21 | `java -version` → `openjdk version "21…"` | TODO |
| H0.S1.M3 | Instalar Flutter 3.44.8 stable (misma versión que `ci.yml`) | `flutter --version` reporta 3.44.8 y `dart --version` funciona | `flutter --version` → `Flutter 3.44.8` | TODO |
| H0.S1.M4 | Generar clientes: `./gradlew generateOpenApiClients --no-parallel --no-build-cache -q` | Existen `clientes/angular/<14 svc>` y `clientes/dart/<14 svc>` | `ls clientes/angular clientes/dart` → 28 dirs + exit 0 | TODO |
| H0.S1.M5 | `corepack enable && yarn install --immutable` | Install termina con exit 0 sin modificar `yarn.lock` | `yarn install --immutable; echo $?` → 0 · `git status --short yarn.lock` vacío | TODO |
| H0.S1.M6 | Crear `docs/auditoria/` con los 8 archivos del §43 (esqueleto) y copiar este plan a `plan-de-remediacion.md` | Los 8 archivos existen con encabezado; el plan copiado pasa `plan_status.py` | `ls docs/auditoria` → 8 archivos · `python <ruta>/plan_status.py --path docs/auditoria/plan-de-remediacion.md` → total > 0 | TODO |
| H0.S1.M7 | (D-A1) Enmienda a ADR-016: `clientes/angular` y `clientes/dart` se versionan; quitar las dos líneas de `.gitignore:49-50`; el gate pasa a "regenerar no produce diff" | `git check-ignore clientes/angular/identidad` no devuelve nada; el ADR enmendado existe | `git check-ignore -q clientes/angular/identidad; echo $?` → 1 · `ls "docs/Arquitectura/ADR-016*"` → contiene "Enmienda 2026-09-21" | TODO |
| H0.S1.M8 | (D-A1) Commitear los clientes generados en H0.S1.M4 (`chore(contracts): clientes OpenAPI versionados`) y verificar que un clon limpio compila **sin** JDK | `git ls-files clientes/` > 0; en un clon nuevo sin `java`, `yarn install --immutable && yarn typecheck` sale 0 | `git ls-files clientes/ \| wc -l` → > 0 · clon limpio: `yarn typecheck; echo $?` → 0 | TODO |
| H0.S1.M9 | (D-A1) Paso CI `f0 · clientes al día`: `./gradlew generateOpenApiClients` + `git diff --exit-code -- clientes/` (mismo patrón que el gate de `generar_ddl.py` en `ci.yml:90-91`) | Un contrato cambiado sin regenerar pone el job en rojo | Commit de prueba con un campo nuevo en `tarifas.yaml` sin regenerar → `gh run view` job `frontend` `failure` en `f0` (salida pegada); revertido después | TODO |

### H0.S2 — Corrida completa del pipeline frontend en el SHA
**CA:** Dado el clon con toolchain, cuando se corre cada etapa del job `frontend` del CI en el orden del `ci.yml`, entonces cada una deja su salida literal y su exit code registrados, verde o rojo, sin corregir nada.
**DoD:** 12 archivos `evidencia/H0-S2-*.txt` con `exit=<n>` en la última línea.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H0.S2.M1 | `yarn workspace @aportaya/tokens build && yarn workspace @aportaya/simulado build` | Existen `packages/tokens/generado/tokens.css` y `packages/simulado/generado/prism/todos.yaml` | `ls packages/tokens/generado/tokens.css packages/simulado/generado/prism/todos.yaml` → ambos | TODO |
| H0.S2.M2 | `yarn workspace @aportaya/diseno-flutter build && yarn workspace @aportaya/movil build` | `tokens.dart` generado y `build_runner` de los 11 clientes Dart termina | `echo $?` → registrado (0 o no) en `evidencia/H0-S2-M2.txt` | TODO |
| H0.S2.M3 | `yarn lint` (turbo: angular-eslint + `dart format` + `verificar_frontend.py`) | Salida completa registrada, con lista de fallas por workspace | `yarn lint; echo exit=$?` → pegado | TODO |
| H0.S2.M4 | `yarn typecheck` | Salida registrada; si hay errores, cada uno con archivo:línea | `yarn typecheck; echo exit=$?` → pegado | TODO |
| H0.S2.M5 | `yarn test:front` (vitest ×5 workspaces + `flutter test` 5 carpetas) | Conteo `passed/failed` por workspace registrado | `yarn test:front; echo exit=$?` → pegado | TODO |
| H0.S2.M6 | `yarn test:a11y` | Conteo registrado | `yarn test:a11y; echo exit=$?` → pegado | TODO |
| H0.S2.M7 | `yarn workspace @aportaya/backoffice build` + chequeo `noindex` | `dist/backoffice/browser/index.html` existe y contiene `noindex`; tamaños de bundle registrados | `grep -c 'content="noindex' apps/backoffice/dist/backoffice/browser/index.html` → 1 | TODO |
| H0.S2.M8 | `yarn workspace @aportaya/web build` (con `contenido.mjs`) | `dist/web/server/server.mjs` y `browser/` existen; presupuesto registrado | `ls apps/web/dist/web/server/server.mjs` → existe · exit pegado | TODO |
| H0.S2.M9 | `yarn workspace @aportaya/web test:e2e` (Playwright + Prism, `webServer` propio) | Resultado por spec registrado | `…test:e2e; echo exit=$?` → pegado | TODO |
| H0.S2.M10 | `yarn workspace @aportaya/backoffice test:e2e` levantando a mano `ng serve --port 4300` contra Prism | Resultado de los 3 `*.e2e.ts` registrado; el servidor se baja al terminar | `…test:e2e; echo exit=$?` → pegado · `netstat -ano` sin `:4300` después | TODO |
| H0.S2.M11 | `dart analyze --fatal-infos` + `dart format --set-exit-if-changed` en `apps/movil` y `packages/diseno_flutter` | Salida registrada | `dart analyze --fatal-infos; echo exit=$?` → pegado | TODO |
| H0.S2.M12 | `yarn npm audit --all --recursive` y `flutter pub outdated` | Lista de advisories con severidad y paquete registrada (D8) | Salidas pegadas en `evidencia/H0-S2-M12.txt` | TODO |

### H0.S3 — Desconocidos D2–D5, D9 resueltos y hallazgos abiertos
**CA:** Dado el baseline, cuando se lee `hallazgos.md`, entonces cada problema vigente de §2.4 tiene su `F-xxx` con evidencia citada, y los desconocidos D2, D3, D4, D5, D9 tienen respuesta con ruta o comando.
**DoD:** `hallazgos.md` con ≥ 20 entradas `ABIERTO`; `frontend-baseline.md` con tabla comando/exit/duración.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H0.S3.M1 | Localizar el Dockerfile/NGINX de la imagen `aportaya/backoffice` y cómo inyecta `<meta aportaya-gateway>` (D2) | Ruta del Dockerfile y de la directiva citadas en `frontend-baseline.md`, o declarado "no existe en el árbol" | `grep -rn "aportaya-gateway" --include=Dockerfile* --include=*.conf --include=*.sh .` → salida pegada | TODO |
| H0.S3.M2 | Extraer el contrato de `POST /sesion/refrescar` de `identidad.yaml` (D3): request (cookie/cuerpo), response, rotación. **D-A3:** si no existe el modo cookie HttpOnly para web, se abre `F-xxx` como brecha del backend y H1/H2 se verifican contra un doble con cookie (regla 65) | Tabla contrato pegada en `brechas-backend.md` §sesión, con veredicto "cookie: sí / no (brecha F-xxx)" | `yq '.paths."/sesion/refrescar"' servicios/identidad/src/main/resources/openapi/identidad.yaml` → pegado | TODO |
| H0.S3.M3 | Buscar `POST /extraccion/accesos` en los 14 `openapi/*.yaml` (D4) | Existe con contrato citado, o se declara **inexistente** en `brechas-backend.md` | `grep -ln "/extraccion/accesos" servicios/*/src/main/resources/openapi/*.yaml` → pegado | TODO |
| H0.S3.M4 | Leer `scripts/verificar_maqueta.py` y registrar qué verifica (D5) | Párrafo en `frontend-baseline.md` con entradas y salidas del script | `python3 scripts/verificar_maqueta.py; echo exit=$?` → pegado | TODO |
| H0.S3.M5 | Consultar rulesets del remoto (D9): `gh api repos/PabloArauzCaballero/PasanakuFrontend/rulesets` | Respuesta registrada (lista, 403 o vacío) | comando → salida pegada en `evidencia/H0-S3-M5.txt` | TODO |
| H0.S3.M6 | Escribir `hallazgos.md` con F-001 (dos remotos divergidos) … F-0nn para cada fila VIGENTE de §2.4, formato §44 | Cada `F-xxx` tiene Severidad, Archivo(s), Estado=ABIERTO, Evidencia con ruta:línea | `grep -c "^## F-" docs/auditoria/hallazgos.md` → ≥ 20 | TODO |
| H0.S3.M7 | Escribir `frontend-baseline.md` (tabla comando → exit → duración → enlace a evidencia) y commit `docs(audit): línea base del frontend en 19a621e6` | El documento cubre los 12 comandos de H0.S2 | `git log --oneline -1` → el commit · `grep -c "exit=" docs/auditoria/frontend-baseline.md` → ≥ 12 | TODO |

---

## H1 — Refresh single-flight: N `401` concurrentes producen exactamente un refresh (P0, §4)
**CA:** Dado un access token vencido y un refresh válido (web: cookie HttpOnly con `withCredentials`, D-A3; móvil: refresh en `AlmacenSeguro` enviado en el cuerpo), cuando 10 peticiones reciben `401` a la vez, entonces sale **una** llamada a `/sesion/refrescar`, las 10 se reintentan una vez con el token nuevo y todas completan; si el refresh falla, la sesión se cierra **una** vez y las 10 fallan con el error original, sin segundo refresh.
**DoD:** specs `sesion.interceptor.spec.ts` (backoffice) y `cliente_refresco_test.dart` (móvil) con los 4 casos del §4 en verde, salida pegada · `yarn lint && yarn typecheck` verdes · E2E backoffice `sesion-expirada.e2e.ts` PASS.
**Estado:** TODO

### H1.S1 — Caracterización del comportamiento actual (backoffice)
**CA:** Dado el interceptor actual, cuando corre el test de 10 `401` concurrentes, entonces el test **falla** mostrando 10 refresh (documenta el defecto antes de corregirlo, §37).
**DoD:** `sesion.interceptor.spec.ts` en rojo con `expected 1 refresh, got 10` pegado en `evidencia/H1-S1-M2.txt`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Crear `sesion.interceptor.spec.ts` con `HttpTestingController` y el caso "1 `401` → 1 refresh → 1 reintento" (comportamiento actual correcto) | El spec pasa contra el código actual | `yarn workspace @aportaya/backoffice test:front --include='src/app/nucleo/sesion.interceptor.spec.ts'` → 1 passed | TODO |
| H1.S1.M2 | Agregar caso "10 `401` concurrentes → exactamente 1 refresh" | El spec **falla** contra el código actual con conteo 10 | mismo comando → `1 failed` con `expected 1 … received 10` pegado | TODO |

### H1.S2 — Single-flight en el backoffice
**CA:** Dado el interceptor nuevo, cuando llegan N `401` mientras un refresh está en vuelo, entonces todos esperan el mismo `Observable` compartido y ninguno dispara otro refresh; el refresh sale por un cliente que **no** pasa por `sesionInterceptor` ni `registroDeAccesoInterceptor`.
**DoD:** los 4 casos de §4 en verde; `yarn lint` sin `eslint-disable` nuevo; commit `fix(auth): refresh single-flight en el backoffice (F-00x)`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Extraer el refresh a un servicio `RefrescoDeSesion` en `nucleo/` con un `HttpBackend` propio (sin interceptores) y `shareReplay(1)` + `finalize` que limpia el vuelo | Existe un único método `refrescar(): Observable<string>`; el `POST` no atraviesa la cadena de interceptores | spec: `HttpTestingController.expectOne('/sesion/refrescar')` sin cabecera `Authorization` ni `x-request-id` del interceptor → PASS | TODO |
| H1.S2.M2 | Reescribir `sesionInterceptor` para usar `RefrescoDeSesion` y reintentar **una** vez | Caso "10 concurrentes → 1 refresh" pasa | spec de H1.S1.M2 → PASS | TODO |
| H1.S2.M3 | Caso límite: refresh lento, 5 peticiones nuevas llegan durante el vuelo | Cero refresh adicionales; las 5 se reintentan tras el mismo resultado | spec `refresh en vuelo no dispara otro` → PASS | TODO |
| H1.S2.M4 | Caso error: refresh responde `401`/`5xx`/red | `sesion.cerrar()` se llama **una** vez; las N peticiones fallan con su `HttpErrorResponse` original; ningún segundo `POST /sesion/refrescar` | spec `refresh falla → cerrar ×1, sin loop` con `expect(cerrar).toHaveBeenCalledTimes(1)` → PASS | TODO |
| H1.S2.M5 | Caso rotación: la respuesta trae `acceso` nuevo; el reintento usa **solo** el nuevo | Cabecera `Authorization` del reintento = `Bearer <nuevo>` | spec `reintento usa el token nuevo` → PASS | TODO |
| H1.S2.M6 | Protección de loop: una petición marcada `YA_REINTENTADA` que recibe `401` no vuelve a refrescar | Segundo `401` → error propagado, 0 refresh | spec `401 tras reintento no refresca` → PASS | TODO |
| H1.S2.M7 | Registrar en `decisiones.md` la separación cliente autenticado / cliente de refresh y por qué (`HttpBackend`) | Entrada con fecha, alternativa descartada (`HttpContext` flag) y consecuencia | `grep -n "HttpBackend" docs/auditoria/decisiones.md` → 1 entrada | TODO |

### H1.S3 — Single-flight en el móvil (Dart/Dio)
**CA:** Dado `_TrazaYSesion`, cuando N peticiones reciben `401`, entonces un único `Future` de refresh se comparte, el refresh sale por un `Dio` **sin** el interceptor de sesión, y con rotación el siguiente refresh usa exclusivamente el par nuevo guardado en `AlmacenSeguro`.
**DoD:** `test/unidad/cliente_refresco_test.dart` con 4 casos (`http_mock_adapter`) en verde; `dart analyze --fatal-infos` limpio; commit `fix(auth): refresh single-flight en la app`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Test de caracterización: 10 `401` concurrentes contra `_TrazaYSesion` actual con `DioAdapter` mock | El test falla mostrando 10 `POST /sesion/refrescar` | `flutter test test/unidad/cliente_refresco_test.dart` → `expected 1, actual 10` pegado | TODO |
| H1.S3.M2 | Introducir `_Refrescador` con `Completer`/`Future` compartido y un `Dio` de refresh separado (misma `BaseOptions`, sin `_TrazaYSesion`) | 10 `401` → 1 refresh; el `Dio` de refresh no agrega `Authorization` | mismo test → PASS | TODO |
| H1.S3.M3 | Caso límite: peticiones que llegan durante el refresh esperan el mismo `Future` | 0 refresh adicionales | test `en vuelo` → PASS | TODO |
| H1.S3.M4 | Caso error: refresh falla → `cerrar()` ×1, todas las pendientes reciben `ErrorDeApi(401)`, sin loop | `almacen.borrar` llamado exactamente 2 veces (acceso + refresco) | test `falla → cerrar una vez` → PASS | TODO |
| H1.S3.M5 | Caso rotación: tras refresh exitoso, `tokenDeRefresco()` devuelve el nuevo y un segundo refresh lo manda | Segundo `POST` lleva `refresco: <nuevo>` | test `rotación` → PASS | TODO |

### H1.S4 — Verificación de punta a punta y cierre del hito
**CA:** Dado el backoffice contra Prism con sesión, cuando el E2E expira el token y navega a tres secciones a la vez, entonces la red muestra un solo `POST /sesion/refrescar` y las tres pantallas cargan.
**DoD:** `apps/backoffice/e2e/sesion-expirada.e2e.ts` PASS con trace; consola sin errores; `hallazgos.md` F-refresh → `CORREGIDO`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S4.M1 | Escribir `sesion-expirada.e2e.ts`: `page.route` fuerza `401` en la primera respuesta de 3 recursos, cuenta `POST /sesion/refrescar` | Conteo = 1 y las 3 pantallas muestran datos | `yarn workspace @aportaya/backoffice test:e2e sesion-expirada` → 1 passed | TODO |
| H1.S4.M2 | Correr regresión dirigida: `test:front` backoffice completo + `flutter test test/unidad` | Todo en verde, conteos pegados | `yarn workspace @aportaya/backoffice test:front; flutter test test/unidad` → 0 failed | TODO |
| H1.S4.M3 | Actualizar `hallazgos.md` (F-refresh backoffice y móvil → `CORREGIDO` con pruebas y resultado) | Ambas entradas con sección Pruebas y Resultado llenas | `grep -c CORREGIDO docs/auditoria/hallazgos.md` → ≥ 2 | TODO |

---

## H2 — Restauración de sesión: F5 y deep link no mandan al login sin intentar refrescar (P0, §5)
**CA:** Dado un operador con cookie de refresh válida, cuando recarga el navegador sobre `/operacion/reclamos`, entonces ve un estado "restaurando" y después la pantalla pedida; con cookie inválida ve `/ingreso`; con `identidad` caído ve un error accionable, **nunca** un login silencioso mientras el estado es `UNKNOWN`.
**DoD:** `sesion.spec.ts` con la máquina de 5 estados; `permisos.spec.ts` extendido; E2E `restaurar-sesion.e2e.ts` con los 5 escenarios del §5 PASS; capturas del estado `RESTORING` en 3 viewports × 2 temas.
**Estado:** TODO

### H2.S1 — Máquina de estados de sesión
**CA:** Dado `Sesion`, cuando se consulta `estado()`, entonces devuelve exactamente uno de `UNKNOWN | RESTORING | AUTHENTICATED | ANONYMOUS | ERROR`, arranca en `UNKNOWN` y `abierta()` solo es `true` en `AUTHENTICATED`.
**DoD:** `sesion.spec.ts` cubre las transiciones válidas y rechaza `UNKNOWN → ANONYMOUS` sin pasar por `RESTORING`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Agregar `estado = signal<EstadoSesion>('UNKNOWN')` a `Sesion` y derivar `abierta` de `estado() === 'AUTHENTICATED'` | Los specs existentes que usan `abrir/cerrar` siguen pasando | `yarn workspace @aportaya/backoffice test:front --include='src/app/nucleo/*.spec.ts'` → 0 failed | TODO |
| H2.S1.M2 | Métodos `restaurando()`, `anonima()`, `fallo()` con transiciones permitidas; `cerrar()` → `ANONYMOUS` | Transición `UNKNOWN → ANONYMOUS` directa se rechaza (decisión registrada) | spec `no se puede pasar de UNKNOWN a ANONYMOUS sin restaurar` → PASS | TODO |
| H2.S1.M3 | `sesion.spec.ts` con tabla de transiciones (8 casos) | 8 passed | mismo comando → 8 passed | TODO |

### H2.S2 — `AuthBootstrap` con timeout controlado
**CA:** Dado el arranque de la app, cuando se resuelve el `provideAppInitializer`, entonces ya se intentó `RefrescoDeSesion.refrescar()` (H1) con timeout configurable (por defecto 5 s), y el estado quedó en `AUTHENTICATED`, `ANONYMOUS` (401) o `ERROR` (red/5xx/timeout).
**DoD:** `auth-bootstrap.spec.ts` con 5 casos; el arranque no bloquea más que el timeout.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Crear `nucleo/auth-bootstrap.ts` con `provideAppInitializer` que llama a `RefrescoDeSesion` y mapea resultado → estado | Con refresh 200 → `AUTHENTICATED` y `abrirConToken` invocado | spec `cookie válida → AUTHENTICATED` → PASS | TODO |
| H2.S2.M2 | Caso cookie inválida (`401`) → `ANONYMOUS` sin `ERROR` | Estado final `ANONYMOUS` | spec → PASS | TODO |
| H2.S2.M3 | Caso identidad caída (`503` / error de red) → `ERROR` | Estado final `ERROR`, ningún redirect a `/ingreso` | spec → PASS | TODO |
| H2.S2.M4 | Caso timeout (refresh no responde en 5 s con `fakeAsync`) → `ERROR` | Estado `ERROR` a los 5 s exactos | spec con `tick(5000)` → PASS | TODO |
| H2.S2.M5 | Caso concurrencia: un `401` de otra petición durante el bootstrap **no** dispara un segundo refresh (reusa el single-flight de H1) | `expectOne('/sesion/refrescar')` | spec → PASS | TODO |
| H2.S2.M6 | Registrar el `provideAppInitializer` en `app.config.ts` del backoffice | El backoffice compila y arranca | `yarn workspace @aportaya/backoffice build; echo $?` → 0 | TODO |

### H2.S3 — Guards y pantalla de espera/error
**CA:** Dado `requiereSesion()`, cuando el estado es `UNKNOWN`/`RESTORING`, entonces el guard espera (Observable) al desenlace; en `ANONYMOUS` redirige a `/ingreso` preservando la ruta pedida; en `ERROR` muestra la pantalla de error con botón "Reintentar".
**DoD:** `permisos.spec.ts` extendido (4 casos); componente `restaurando-sesion` con a11y spec; capturas.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S3.M1 | `requiereSesion()` devuelve `Observable<boolean \| UrlTree>` que espera a que `estado()` salga de `UNKNOWN`/`RESTORING` | Con `RESTORING` no emite hasta la transición | spec `espera mientras restaura` → PASS | TODO |
| H2.S3.M2 | En `ANONYMOUS` redirige a `/ingreso?volverA=<ruta>` | `parseUrl` contiene `volverA` | spec → PASS | TODO |
| H2.S3.M3 | `pantalla-de-ingreso.ts` lee `volverA` y navega ahí tras el login exitoso, solo si es ruta interna (sin `//`, sin esquema) | Ruta externa se ignora → `/tablero` | spec `volverA externo se ignora` → PASS | TODO |
| H2.S3.M4 | Componente `RestaurandoSesion` (shell mínimo con `aria-busy`, texto "Restaurando tu sesión…") mostrado mientras `RESTORING` | Spec a11y con `axe` sin violaciones | `yarn workspace @aportaya/backoffice test:a11y --include='**/restaurando-sesion.a11y.spec.ts'` → 0 violations | TODO |
| H2.S3.M5 | Estado `ERROR`: pantalla con mensaje accionable y botón "Reintentar" que vuelve a `RefrescoDeSesion` | Click → nuevo `POST /sesion/refrescar` | spec → `expectOne` tras el click | TODO |
| H2.S3.M6 | Prueba visual: capturas `RESTORING` y `ERROR` en 360×800, 768×1024, 1280×900, claro y oscuro (12 PNG), inspeccionadas | Sin recortes ni texto ilegible; consola limpia | `ls evidencia/H2-S3-M6-*.png` → 12 archivos + nota de inspección | TODO |

### H2.S4 — E2E de los cinco escenarios del §5
**CA:** Dado el backoffice contra Prism con sesión, cuando corre `restaurar-sesion.e2e.ts`, entonces F5 en ruta protegida, deep link con cookie válida, cookie inválida, identidad caída y refresh concurrente durante el bootstrap se comportan según §5.
**DoD:** 5 tests PASS con trace; `hallazgos.md` F-restauración → `CORREGIDO`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S4.M1 | E2E "F5 sobre `/operacion/reclamos` con cookie válida" | Tras `reload()` la URL sigue siendo `/operacion/reclamos` y la tabla carga | `test:e2e restaurar-sesion -g F5` → passed | TODO |
| H2.S4.M2 | E2E "deep link a `/cumplimiento/verificaciones` en pestaña nueva" | Llega sin pasar por `/ingreso` | `-g "deep link"` → passed | TODO |
| H2.S4.M3 | E2E "cookie inválida" (`page.route` → 401) | Termina en `/ingreso?volverA=…` | `-g "inválida"` → passed | TODO |
| H2.S4.M4 | E2E "identidad no disponible" (`page.route` → abort) | Pantalla de error con "Reintentar" visible; sin redirect | `-g "no disponible"` → passed | TODO |
| H2.S4.M5 | E2E "refresh concurrente durante bootstrap" | 1 solo `POST /sesion/refrescar` en `page.on('request')` | `-g concurrente` → passed | TODO |
| H2.S4.M6 | Actualizar `hallazgos.md` F-restauración → `CORREGIDO` y commit `fix(auth): restauración de sesión al arrancar (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

---

## H3 — Auditoría de lectura: el navegador deja de fingir que garantiza el registro (P0, §6)
**CA:** Dado un operador que abre un expediente, cuando la lectura se completa, entonces ningún código del frontend afirma que la auditoría quedó registrada; el frontend manda solo el contexto que el backend exige (si el contrato existe) de forma que un fallo del registro **se observa** (estado visible o telemetría), y `brechas-backend.md` describe el contrato server-side que falta.
**DoD:** `registro-de-acceso.interceptor.spec.ts` con 3 niveles (correcto/límite/inválido) en verde · `brechas-backend.md` §auditoría con contrato esperado · ningún `catchError(() => of(null))` sobre la llamada de auditoría · `grep -rn "auditoría garantizada\|queda registrado" apps/backoffice/src` vacío.
**Estado:** TODO

### H3.S1 — Decisión según exista o no el contrato (`D4`)
**CA:** Dado el resultado de H0.S3.M3, cuando se lee `brechas-backend.md`, entonces dice si `POST /extraccion/accesos` existe en OpenAPI y, si existe, qué campos exige; si no existe, describe el contrato esperado (gateway registra la lectura por `x-request-id` + `sub` + ruta, sin que el cliente lo pida).
**DoD:** sección escrita con cita a `openapi/*.yaml` o "inexistente"; decisión en `decisiones.md`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Escribir `brechas-backend.md` §"Auditoría de lectura server-side": amenaza (cliente omite el POST), control esperado (gateway/servicio registra en `auditoria` toda lectura marcada sensible por ruta), contrato mínimo | La sección nombra el servicio dueño (`auditoria`, M9) y el evento esperado | `grep -c "extraccion/accesos" docs/auditoria/brechas-backend.md` → ≥ 1 | TODO |
| H3.S1.M2 | Verificar que `rutaId: req.urlWithParams` (`:32`) no lleve identificadores de persona en ninguna pantalla que marque `ACCESO_A_DATOS` (regla 90.2.2) | Lista de las pantallas que usan `ACCESO_A_DATOS` con su URL de lectura; ninguna lleva documento/cuenta en path o query, o se registra F-xxx | `grep -rn "ACCESO_A_DATOS" apps/backoffice/src --include=*.ts` → tabla en `hallazgos.md` | TODO |
| H3.S1.M3 | Registrar en `decisiones.md`: el frontend **no** es fuente de auditoría; qué se conserva (metadata `x-request-id` + marca de contexto) y qué se elimina (garantía implícita) | Entrada con alternativas (quitar el interceptor / mantener con observabilidad) y la elegida | `grep -n "fuente de auditoría" docs/auditoria/decisiones.md` → 1 | TODO |

### H3.S2 — Interceptor sin fire-and-forget silencioso
**CA:** Dado el interceptor, cuando el registro de acceso falla, entonces el fallo se reporta al puerto de telemetría (H10) con `x-request-id`, la pantalla muestra un aviso no bloqueante "no se pudo registrar el acceso" y **no** se traga el error; cuando el registro no está soportado por el contrato, el interceptor no manda nada y lo declara.
**DoD:** spec con los 3 niveles; `yarn lint` limpio.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Test de caracterización del interceptor actual: la lectura se muestra aunque el POST falle y el error desaparece | El spec documenta `catchError → of(null)` (pasa contra el código actual) | `…test:front --include='**/registro-de-acceso.interceptor.spec.ts'` → passed | TODO |
| H3.S2.M2 | Nivel correcto: el POST sale **después** del éxito de la lectura con `recurso`, `id`, `x-request-id` y sin la URL completa (`rutaId` → solo el `path` sin query) | `expectOne` con cuerpo exacto; sin `?` en `rutaId` | spec → PASS | TODO |
| H3.S2.M3 | Nivel límite: la lectura responde `204`/vacío → no se registra; dos lecturas iguales en 1 s → dos registros (no se deduplica en cliente) | Conteos exactos | spec → PASS | TODO |
| H3.S2.M4 | Nivel inválido: el POST falla (`500`/red) → se emite `telemetria.error('auditoria.registro_fallido', {requestId})` y `Avisos.mostrar(...)`; ningún `of(null)` | `expect(telemetria.error).toHaveBeenCalledTimes(1)` | spec → PASS | TODO |
| H3.S2.M5 | Si el contrato no existe (H0.S3.M3 = inexistente): el interceptor queda detrás de un flag de configuración `auditoriaCliente: 'desactivada'` y **no** manda nada; comentario del archivo reescrito sin la palabra "garantiza" | Con flag desactivado, `expectNone('/extraccion/accesos')` | spec → PASS · `grep -n garant apps/backoffice/src/app/nucleo/registro-de-acceso.interceptor.ts` vacío | TODO |
| H3.S2.M6 | Actualizar `hallazgos.md` F-auditoría → `CORREGIDO` (frontend) + `BLOQUEADO` (backend, con la brecha enlazada) y commit `fix(security): la auditoría de lectura no depende del navegador (F-00x)` | Dos estados declarados en la misma entrada | `grep -A3 "F-00. — Auditoría" docs/auditoria/hallazgos.md` → ambos | TODO |

---

## H4 — Datos simulados aislados: producción no puede mostrar cifras inventadas (P0, §7)
**CA:** Dado un build de producción del backoffice, cuando un operador abre cualquier pantalla de `sistemas/`, entonces ve un estado de error/“fuente no disponible” accionable y **nunca** los valores de `datos-simulados.ts`; en `dev`/`demo` ve los mismos datos de ejemplo con un banner persistente "Datos de ejemplo" y los tipos `Mock*` viven en un package aparte.
**DoD:** `yarn workspace @aportaya/backoffice build --configuration production` + `grep -c "99.95%" dist/backoffice/browser/*.js` → 0 · specs de los 9 adaptadores con 3 niveles · E2E `sistemas-sin-contrato.e2e.ts` PASS · capturas del banner.
**Estado:** TODO

### H4.S1 — Puerto por fuente y adaptador simulado separado
**CA:** Dado cada pantalla de `sistemas/`, cuando pide datos, entonces lo hace a un puerto (`FuenteDeServicios`, `FuenteDeDespliegues`, …) inyectado por DI, y la implementación simulada vive en `@aportaya/simulado/backoffice-sistemas` con tipos `Mock*`, no en `rutas/sistemas/dominio/`.
**DoD:** `grep -rn "datos-simulados" apps/backoffice/src` → 0 hits fuera de tests; `yarn typecheck` verde.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Definir en `rutas/sistemas/dominio/puertos.ts` un `InjectionToken` por fuente (9) con la forma `Observable<T[]>` o `Resource` (patrón de `cu13-consultar-saldo.ts` con `httpResource`) | Los 9 tokens exportados y tipados con los tipos existentes | `yarn workspace @aportaya/backoffice typecheck` → 0 errores | TODO |
| H4.S1.M2 | Mover los arrays `*Simulados` a `packages/simulado/src/backoffice-sistemas/` renombrando tipos a `Mock*`; dejar en `dominio/` solo `puedeConfirmar` y `restauracionVencida` (funciones puras) con su spec | `datos-simulados.spec.ts` sigue verde; `packages/simulado` exporta `./backoffice-sistemas` | `yarn workspace @aportaya/simulado test:front` → passed · `grep -c "Simulados" apps/backoffice/src/app/rutas/sistemas/dominio/*.ts` → 0 | TODO |
| H4.S1.M3 | Adaptador `FuenteSimulada` (en `simulado`) que implementa los 9 puertos con los `Mock*` y un retardo determinista | Spec: emite los datos; nunca falla | spec → PASS | TODO |
| H4.S1.M4 | Adaptador `FuenteNoDisponible` (en `backoffice/nucleo/`) que devuelve error de dominio `CONTRATO_NO_DISPONIBLE` para los 9 puertos | Spec: cada puerto emite el error tipado | spec → PASS | TODO |
| H4.S1.M5 | Reescribir las 9 `pantalla-*.ts` para inyectar el puerto y resolver los 4 estados (cargando / datos / vacío / error) con los componentes de `@aportaya/ui` ya existentes | Cada pantalla tiene spec de los 4 estados (36 casos) | `…test:front --include='src/app/rutas/sistemas/**/*.spec.ts'` → 36+ passed | TODO |

### H4.S2 — Flag de entorno inequívoco y bloqueo en producción
**CA:** Dado `environment.produccion === true`, cuando el DI resuelve los puertos de `sistemas/`, entonces recibe `FuenteNoDisponible` y el proveedor de `FuenteSimulada` **lanza en build** si alguien lo registra (`assertNoSimuladoEnProduccion`); dado `produccion === false`, se registra `FuenteSimulada` y el shell muestra el banner.
**DoD:** spec del provider en ambos modos; `ng build --configuration production` no contiene los strings de los mocks; banner con a11y spec.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Provider `provideFuentesDeSistemas()` que elige adaptador por `isDevMode()` + flag explícito `APORTAYA_MODO=demo` leído del `<meta>`/entorno (no solo `isDevMode`) | En `production` sin `demo` → `FuenteNoDisponible` | spec → PASS | TODO |
| H4.S2.M2 | Guard de build: `FuenteSimulada` se importa con `import()` dinámico solo en la rama no-producción, y un test verifica que el bundle de producción no contiene `serviciosSimulados` | 0 coincidencias en `dist/` | `yarn workspace @aportaya/backoffice build && grep -rc "nucleo-financiero.*99.95" apps/backoffice/dist/backoffice/browser/` → 0 | TODO |
| H4.S2.M3 | Banner `BannerDatosDeEjemplo` en el shell (rol `status`, no cerrable, visible en las 9 pantallas) solo cuando la fuente es simulada | a11y spec sin violaciones; spec: no se renderiza con `FuenteNoDisponible` | `test:a11y --include='**/banner-datos-de-ejemplo.a11y.spec.ts'` → 0 violations | TODO |
| H4.S2.M4 | Prohibir el fallback silencioso: test de arquitectura que falla si alguna pantalla de `sistemas/` importa desde `@aportaya/simulado` | `grep` en spec → 0 imports | spec `sin-simulado-en-pantallas.spec.ts` → PASS | TODO |
| H4.S2.M5 | Prueba visual: pantalla `servicios` en estado error (producción) y con banner (demo), 3 viewports × 2 temas (12 PNG) inspeccionadas | Sin recortes; el banner no tapa la navegación | `ls evidencia/H4-S2-M5-*.png` → 12 + nota | TODO |
| H4.S2.M6 | E2E `sistemas-sin-contrato.e2e.ts`: con `APORTAYA_MODO` ausente, las 9 rutas muestran el estado de error accionable | 9 aserciones `getByRole('alert')` visibles | `test:e2e sistemas-sin-contrato` → passed | TODO |
| H4.S2.M7 | `brechas-backend.md` §"Contrato de observabilidad para `sistemas/`": los 9 recursos con la forma que hoy espera la UI, marcados como **propuesta**, no como contrato | Sección con 9 subsecciones y la nota "no existe en OpenAPI" | `grep -c "^### " docs/auditoria/brechas-backend.md` → ≥ 9 | TODO |
| H4.S2.M8 | `hallazgos.md` F-mocks → `CORREGIDO`; commit `fix(security): datos simulados fuera del bundle de producción (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

---

## H5 — Configuración fail-fast: ninguna app arranca en producción contra `localhost` (P0, §8)
**CA:** Dado un despliegue de producción, cuando falta la URL del gateway o es `http://`, `localhost`, `127.0.0.1`, un host distinto del propio origen (web/backoffice, D-A6) o fuera de `API_HOSTS` (móvil), o sin `/api/v1`, entonces la app web/backoffice **no arranca** (pantalla de error de configuración, sin ninguna petición de red) y la app móvil **no compila** en release; en desarrollo el fallback a Prism sigue funcionando explícitamente.
**DoD:** `configuracion.spec.ts` (web, backoffice) y `configuracion_test.dart` con matriz válido/límite/inválido · `ng build --configuration production` sin `APORTAYA_GATEWAY` → falla o produce app que muestra error de config (decisión en `decisiones.md`) · `flutter build apk --release` sin `--dart-define=API=` → falla con mensaje.
**Estado:** TODO

### H5.S1 — Módulo de configuración en Angular (compartido)
**CA:** Dado `validarConfiguracion(entrada, modo)`, cuando recibe la URL y el modo (`produccion|desarrollo`), entonces devuelve `{ok, gateway}` o `{ok:false, motivo}` según la matriz del §8, sin efectos.
**DoD:** función pura en `packages/dominio-cliente/src/configuracion.ts` (package sin Angular, ya existe) con ≥ 14 casos.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H5.S1.M1 | `validarConfiguracion(url, {modo, origenPropio, hostsPermitidos?})` en `@aportaya/dominio-cliente` (D-A6): URL presente; en producción `/api/v1` relativo **o** `https://` con host = `origenPropio` (web) **o** host ∈ `hostsPermitidos` (móvil); host ∉ {`localhost`,`127.0.0.1`,`::1`,`10.0.2.2`}; path termina en `/api/v1` | Casos válidos: `/api/v1` OK en producción; `https://app.aportaya.bo/api/v1` OK si `origenPropio = app.aportaya.bo`; `http://localhost:4010/api/v1` OK solo en desarrollo | `yarn workspace @aportaya/dominio-cliente test:front` → casos válidos passed | TODO |
| H5.S1.M2 | Casos límite: URL con puerto, con `/` final, mayúsculas en host, `origenPropio` con puerto, `API_HOSTS` con espacios, `https://LOCALHOST` | Normaliza y decide igual | spec → passed | TODO |
| H5.S1.M3 | Casos inválidos: vacío, `ftp://`, `http://` en producción, host distinto del origen propio (web), host fuera de `API_HOSTS` (móvil), sin `/api/v1`, `javascript:`, `//otro-host/api/v1` | Cada uno → `ok:false` con `motivo` distinto y sin lanzar | spec → passed | TODO |
| H5.S1.M4 | Exportar `./configuracion` en `package.json` de `dominio-cliente` (export explícito, §13) | `import { validarConfiguracion } from '@aportaya/dominio-cliente/configuracion'` compila en las dos apps | `yarn typecheck` → 0 errores | TODO |

### H5.S2 — Backoffice y web: arranque fail-fast
**CA:** Dado `app.config.ts`, cuando `gatewayPorDefecto()` produce una config inválida para el modo detectado, entonces `provideAppInitializer` marca `ConfigInvalida` y el shell renderiza solo la pantalla "Configuración inválida" (sin datos de persona), y **no** se provee `HttpClient` funcional.
**DoD:** specs; build de producción sin meta → pantalla de error (captura); consola con un único `error` estructurado sin la URL.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H5.S2.M1 | Reescribir `nucleo/gateway.ts` (backoffice): lee `<meta aportaya-gateway>` + `<meta aportaya-modo>`; sin meta en producción → `null` (no `localhost`) | `gatewayPorDefecto()` devuelve `null` cuando falta la meta y `modo=produccion` | spec → PASS | TODO |
| H5.S2.M2 | Idem `apps/web/src/app/nucleo/gateway.ts` (SSR: `process.env.APORTAYA_GATEWAY` + `APORTAYA_MODO`; browser: meta); resultado idéntico en servidor y navegador | Spec con `PLATFORM_ID` servidor y browser → mismo valor | spec → PASS | TODO |
| H5.S2.M3 | Componente `ConfiguracionInvalida` (ambas apps, desde `@aportaya/ui`) con mensaje accionable para operaciones, sin mostrar la URL | a11y spec sin violaciones | `test:a11y` → 0 violations | TODO |
| H5.S2.M4 | Backoffice: `app.config.ts` provee `GATEWAY` desde la validación y, si es inválida, un `provideAppInitializer` que navega a `/configuracion-invalida` y bloquea `requiereSesion` | E2E: build prod servido sin meta → pantalla visible, 0 requests a `/api` | `test:e2e config-invalida` → passed; `page.on('request')` con `/api` → 0 | TODO |
| H5.S2.M5 | Web SSR: `server.ts` valida `APORTAYA_GATEWAY_INTERNO` al arrancar con la misma función y **sale con código 1** si es inválida en producción | `NODE_ENV=production node server.mjs` sin variable → exit 1 con mensaje | `echo $?` → 1 pegado | TODO |
| H5.S2.M6 | Prueba visual de `ConfiguracionInvalida` en 3 viewports × 2 temas | 6 PNG inspeccionadas | `ls evidencia/H5-S2-M6-*.png` → 6 | TODO |
| H5.S2.M7 | `decisiones.md`: por qué "arranca y muestra error" en el navegador (no se puede abortar un bundle estático) y "sale con 1" en SSR | Entrada registrada | `grep -n "fail-fast" docs/auditoria/decisiones.md` → 1 | TODO |

### H5.S3 — Móvil: configuración por `dart-define` obligatoria en release
**CA:** Dado `flutter build … --release`, cuando falta `--dart-define=API=` o su valor es inválido, entonces el build falla (`assert` de compilación / `const` inválido) o la app aborta al arrancar con pantalla de error antes de crear el `Dio`; en debug sigue el fallback a `http://localhost/api/v1` con log explícito.
**DoD:** `test/unidad/configuracion_test.dart` con la matriz; `flutter build apk --release` sin define → exit ≠ 0 pegado; con define válido → exit 0.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H5.S3.M1 | `lib/dominio/configuracion.dart`: `validarGateway(String url, {required bool release, required List<String> hostsPermitidos})` pura, misma matriz que H5.S1; `hostsPermitidos` viene de `--dart-define=API_HOSTS` (D-A6) | 14 casos en `configuracion_test.dart`, incluido `API_HOSTS` vacío en release → inválido | `flutter test test/unidad/configuracion_test.dart` → passed | TODO |
| H5.S3.M2 | `cliente.dart`: `baseDelGateway` sin `defaultValue` en release (`kReleaseMode`) → si vacío/inválido, `dioProvider` lanza `ConfiguracionInvalida` y `main.dart` muestra `PantallaConfiguracionInvalida` | Widget test: con URL inválida se renderiza la pantalla y `Dio` no se crea | `flutter test test/widget/configuracion_invalida_test.dart` → passed | TODO |
| H5.S3.M3 | Verificación de build: `flutter build apk --release` sin defines → falla; con `--dart-define=API=https://api.ejemplo.aportaya.bo/api/v1 --dart-define=API_HOSTS=api.ejemplo.aportaya.bo` → exit 0; con `API` fuera de `API_HOSTS` → falla | Ambos exit codes pegados | `evidencia/H5-S3-M3.txt` con ambos `exit=` | TODO |
| H5.S3.M4 | Documentar en `apps/movil/LEEME` o `docs/auditoria/decisiones.md` los defines obligatorios por plataforma (Android/iOS) y el `10.0.2.2` de emulador | Tabla plataforma × modo × valor | `grep -n "10.0.2.2" docs/auditoria/decisiones.md` → 1 | TODO |
| H5.S3.M5 | `hallazgos.md` F-localhost (3 apps) → `CORREGIDO`; commit `fix(config): configuración del gateway fail-fast en web, backoffice y app (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

---

## H6 — Paridad iOS declarada: ninguna capability finge soporte (P0, §9)
**CA:** Dado un dispositivo iOS, cuando la app consulta `capacidades()`, entonces cada uno de los 7 puertos (`AlmacenSeguro`, `Biometria`, `AvisosPush`, `Conectividad`, `ProteccionPantalla`, `Camara`, `Haptica`) responde `SUPPORTED | UNSUPPORTED | DEGRADED` con base en la plataforma real; las features cuyo puerto es `UNSUPPORTED` quedan deshabilitadas en la UI con explicación, y un build release iOS aborta al arrancar si una capability **crítica de seguridad** (`AlmacenSeguro`, `ProteccionPantalla`) no es `SUPPORTED`.
**DoD:** `test/unidad/capacidades_test.dart` con `debugDefaultTargetPlatformOverride` iOS/Android; `dart analyze` limpio; `decisiones.md` con la lista de capabilities críticas; sin `MethodChannel` Android usado bajo iOS.
**Estado:** TODO

### H6.S1 — Detección de capabilities
**CA:** Dado `plataforma.dart`, cuando se pide un puerto en iOS que hoy cae en el adaptador Android (`Conectividad`, `Biometria`, `AvisosPush`, `ProteccionPantalla`), entonces se obtiene un adaptador `NoSoportado` que declara `UNSUPPORTED` (o `DEGRADED` con detalle), nunca el `MethodChannel` Android.
**DoD:** test por puerto × plataforma (14 casos).
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H6.S1.M1 | Enum `Soporte { supported, unsupported, degraded }` y método `Soporte get soporte` en los 7 puertos de `lib/dominio/puertos/` | Los adaptadores Android existentes devuelven `supported`; `dart analyze` limpio | `dart analyze --fatal-infos` → 0 issues | TODO |
| H6.S1.M2 | Adaptadores `*NoSoportadoIos` para `Conectividad`, `Biometria`, `AvisosPush`, `ProteccionPantalla` (valor seguro + `soporte = unsupported`) | Ninguno abre `MethodChannel` | test: instanciarlos no toca `MethodChannel` (con `TestDefaultBinaryMessenger` que falla ante cualquier canal) → passed | TODO |
| H6.S1.M3 | `plataforma.dart` elige `*NoSoportadoIos` bajo `Platform.isIOS` para esos 4 puertos | Test con override iOS → tipos `NoSoportado`; Android → tipos `*Android` | `flutter test test/unidad/capacidades_test.dart` → 14 passed | TODO |
| H6.S1.M4 | `Conectividad`: evaluar si `connectivity_plus` (ya dependencia) es multiplataforma real → si sí, un solo adaptador `ConectividadPlugin` `supported` en ambas (registrar en `decisiones.md`) | Decisión con cita a la doc del plugin (versión instalada) | `grep -n connectivity_plus docs/auditoria/decisiones.md` → 1 | TODO |
| H6.S1.M5 | `Biometria`: idem con `local_auth` **solo si** ya es dependencia; si no lo es, queda `UNSUPPORTED` en iOS y se anota como deuda (no se agrega dependencia sin justificar, regla 90.4.2) | Decisión registrada | `grep -n "local_auth" apps/movil/pubspec.yaml` → resultado citado | TODO |

### H6.S2 — UI y gate de release
**CA:** Dado un puerto `UNSUPPORTED`, cuando la pantalla que lo usa se abre, entonces la acción aparece deshabilitada con texto "No disponible en este dispositivo"; dado un release iOS con `AlmacenSeguro`/`ProteccionPantalla` no `supported`, la app aborta al arrancar con pantalla de bloqueo.
**DoD:** widget tests; test de arranque con override; `hallazgos.md` actualizado.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H6.S2.M1 | Provider `capacidadesProvider` que expone el mapa puerto → `Soporte` | Test: en iOS 4 `unsupported` (o menos según H6.S1.M4/M5) | `flutter test test/unidad/capacidades_test.dart` → passed | TODO |
| H6.S2.M2 | Pantallas que usan biometría/push/protección: botón deshabilitado + `Semantics` con el motivo cuando `unsupported` | Widget tests con override iOS: botón `enabled == false` y semántica presente | `flutter test test/widget/capacidades_ui_test.dart` → passed | TODO |
| H6.S2.M3 | `main.dart`: en `kReleaseMode` + iOS, si `almacenSeguro.soporte != supported || proteccionPantalla.soporte != supported` → `PantallaBloqueoPlataforma` (sin crear `Dio`) | Widget test con override → pantalla de bloqueo | `flutter test test/widget/bloqueo_plataforma_test.dart` → passed | TODO |
| H6.S2.M4 | Actualizar comentario de `plataforma.dart:27-32` y ADR-036 (enmienda) con la tabla puerto × plataforma × soporte | Tabla presente en el ADR | `grep -c "UNSUPPORTED" "docs/Arquitectura/ADR-036*"` → ≥ 1 | TODO |
| H6.S2.M5 | `hallazgos.md` F-iOS → `CORREGIDO` (detección + simulador en CI, H6.S3) con nota "dispositivo físico: pendiente del IPA de TestFlight, dueño Pablo"; commit `fix(mobile): capabilities iOS declaradas, sin fallback Android (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

### H6.S3 — Release iOS en macOS (D-A5)
**CA:** Dado un push a `dev`, cuando corre el CI, entonces un job `ios-release` en `macos-latest` ejecuta el gate de capabilities y las pruebas en simulador iOS, construye el IPA de release con los defines de H5 y lo publica como artefacto; si existen los *secrets* de App Store Connect lo firma y lo sube a TestFlight; si no existen, el paso queda `skipped` con mensaje explícito y el job sigue verde por el artefacto sin firmar.
**DoD:** `gh run view <id>` con el job `ios-release` en verde y el artefacto `aportaya-ios-<run>.ipa` listado; fixture con capability crítica `unsupported` → job rojo (salida pegada) y restaurado; lista de *secrets* en `decisiones.md`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H6.S3.M1 | Job `ios-release` (`runs-on: macos-latest`, `needs: [frontend]`, Flutter 3.44.8, `flutter precache --ios`, CocoaPods) con paso `gate · capabilities iOS`: `flutter test test/unidad/capacidades_test.dart test/widget/bloqueo_plataforma_test.dart` | El job existe y el gate corre antes de compilar | `gh run view <id> --log` → paso `gate · capabilities iOS` `✓` | TODO |
| H6.S3.M2 | Paso `simulador`: `xcrun simctl` arranca un iPhone y corre `flutter test integration_test/deep_link_test.dart integration_test/doble_envio_test.dart -d <udid>` (o `patrol test` si el `patrol_cli` instalado lo soporta; verificar versión antes) | Pruebas en verde en simulador iOS | `gh run view --log` → paso `simulador` `✓` con conteo de tests | TODO |
| H6.S3.M3 | Paso `ipa`: `flutter build ipa --release --no-codesign --build-number=${{ github.run_number }} --dart-define=API=… --dart-define=API_HOSTS=…` (valores desde *variables* del repo, no hardcodeados) y `upload-artifact` del `.ipa`/`.xcarchive` | Artefacto presente en cada corrida | `gh run view <id> --json artifacts` → contiene `aportaya-ios-` | TODO |
| H6.S3.M4 | Firma y subida condicionadas: paso `testflight` con `if: ${{ secrets.ASC_KEY_ID != '' }}` que usa `xcodebuild -exportArchive` + `xcrun altool`/`asc` con `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY`, certificado y perfil; sin secrets imprime "TestFlight omitido: faltan secrets (ver decisiones.md)" y termina `skipped` | Nunca finge subida | Sin secrets: `gh run view --log` → paso `testflight` `skipped` con el mensaje; `decisiones.md` §"Release iOS" lista los 5 secrets y quién los carga (Pablo) | TODO |
| H6.S3.M5 | Kill-test del gate: fixture temporal que fuerza `AlmacenSeguroIos.soporte = unsupported` → el job `ios-release` falla en el gate y **no** produce IPA; se revierte | Rojo demostrado y verde posterior | `evidencia/H6-S3-M5.txt` con los dos `gh run view` | TODO |
| H6.S3.M6 | `verificacion-final.md` §iOS: qué cubre el simulador, qué solo cubre un dispositivo (biometría real, push real, Keychain con protección de hardware) y cómo probar el IPA de TestFlight | Sección con tabla capability × simulador × dispositivo | `grep -c "TestFlight" docs/auditoria/verificacion-final.md` → ≥ 1 | TODO |

---

## H7 — Sin falsos positivos: `humo` y toda verificación obligatoria fallan cuando deben (P0, §10, §36)
**CA:** Dado `yarn humo`, cuando una colección obligatoria falla, entonces el comando termina con exit ≠ 0 y nombra la colección; las colecciones informativas se declaran aparte y no bloquean; no queda ningún `|| true`, `continue-on-error`, `expect(true).toBe(true)`, `skip`/`only` ni `catch` que oculte fallo en gates obligatorios del frontend.
**DoD:** `yarn humo` con una colección rota → exit 1 pegado · `grep -rnE "\|\| true|continue-on-error" package.json .github/workflows/ci.yml` (job frontend) → 0 · `grep -rnE "\.only\(|\.skip\(|xit\(|xdescribe\(" apps packages --include=*.spec.ts --include=*_test.dart` → 0 o justificados por escrito.
**Estado:** TODO

### H7.S1 — `humo` honesto
**CA:** Dado `yarn humo` con una colección obligatoria que falla, cuando termina, entonces el código de salida es 1 y la salida nombra la colección; con una informativa que falla, sale 0 con aviso.
**DoD:** `yarn humo; echo $?` en los dos escenarios, salidas pegadas en `evidencia/H7-S1-*.txt`; spec del script en verde.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H7.S1.M1 | Reemplazar el `for … \|\| true` de `package.json:21` por `scripts/humo.mjs` que corre newman por colección, separa `postman/humo/obligatorias/` de `informativas/` y sale con 1 si alguna obligatoria falla | Con una colección obligatoria inválida → exit 1 y nombre en stderr | `yarn humo; echo $?` → 1 (con colección rota de prueba) · → 0 (todas OK) | TODO |
| H7.S1.M2 | Test de caracterización del script (`vitest`, `node:child_process` mockeado): 3 niveles — todas OK, una informativa falla (exit 0 + aviso), una obligatoria falla (exit 1) | 3 passed | `yarn vitest run scripts/humo.spec.mjs` → 3 passed | TODO |
| H7.S1.M3 | Alinear `ci.yml:150` (`grep -q FALLA … \|\| true`) con el nuevo script **solo** en lo que invoca `yarn humo`; el resto del job `base` es OUT | La línea usa el exit del script | `grep -n "yarn humo" .github/workflows/ci.yml` → sin `\|\| true` | TODO |

### H7.S2 — Barrido de tests débiles
**CA:** Dado el árbol de tests de `apps/` y `packages/`, cuando se buscan patrones de test falso (`expect(true)`, `.only`, `.skip`, esperas fijas, `catch` vacío, `echo` como test), entonces no queda ninguno sin justificación escrita al lado.
**DoD:** grep de los patrones → 0 (o cada resto con comentario de justificación y dueño); `yarn test:front` y `flutter test` en verde tras los cambios.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H7.S2.M1 | Inventariar en `hallazgos.md` todo `expect(true)`, `.only`, `.skip`, `xit`, `xdescribe`, `waitForTimeout`, `sleep`, `Future.delayed` en tests, `catch` vacío en `apps/` y `packages/` | Tabla archivo:línea → clase → acción | `grep -rnE "expect\(true\)|\.only\(|\.skip\(|waitForTimeout|Future\.delayed" apps packages --include=*.spec.ts --include=*.e2e.ts --include=*_test.dart` → salida pegada | TODO |
| H7.S2.M2 | Corregir cada hallazgo sin debilitar el requisito (regla 80.5): reemplazar esperas fijas por condición, quitar `only`, dar dueño y fecha a cualquier cuarentena | Re-grep → 0 o cada resto con justificación escrita al lado | mismo grep → 0 | TODO |
| H7.S2.M3 | `apps/movil/package.json` `test:e2e` deja de ser `echo` engañoso: pasa al comando real que corre en `movil-integracion-macos` (H8.S2.M3) y falla sin simulador/dispositivo con mensaje claro | El script no simula éxito | `yarn workspace @aportaya/movil test:e2e; echo $?` → ≠ 0 sin dispositivo, con mensaje claro | TODO |
| H7.S2.M4 | `hallazgos.md` F-humo → `CORREGIDO`; commit `fix(ci): las verificaciones obligatorias del frontend ya no pueden pasar en falso (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

---

## H8 — CI y seguridad del borde: el pipeline refleja la realidad y el HTML sale endurecido (P1, Fase 2, §11, §12, §18, §41)
**CA:** Dado un push a `dev`, cuando corre el CI, entonces web y backoffice pasan lint, typecheck, unit, a11y, build **y E2E** cada una; Flutter pasa `format`, `analyze --fatal-infos`, unit, widget, contract, a11y; cada package pasa lint/typecheck/test; los goldens corren en un job `macos-latest` separado o se declara que no corren; existe `.github/CODEOWNERS` y un documento con los checks requeridos; el HTML del backoffice sale con CSP, HSTS, `Permissions-Policy`, `Cache-Control: no-store`, `noindex`.
**DoD:** `gh run view` del CI en verde en el SHA final con todos los jobs listados · `curl -sI https://<backoffice>` (o contra la imagen local) con las 8 cabeceras · `yarn npm audit` sin `critical`/`high` sin triage escrito.
**Estado:** TODO

### H8.S1 — E2E del backoffice en CI
**CA:** Dado el job `frontend`, cuando llega al paso E2E, entonces levanta Prism + `ng serve` del backoffice mediante `webServer` de Playwright (no a mano) y corre los `*.e2e.ts` con `workers: 1`, subiendo trace en fallo.
**DoD:** paso `f6 · backoffice E2E` en `ci.yml` con `yarn workspace @aportaya/backoffice test:e2e` en verde en `gh run view`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S1.M1 | `apps/backoffice/playwright.config.ts`: `webServer: [{command: 'yarn workspace @aportaya/simulado mock', port: 4010}, {command: 'ng serve --port 4300', port: 4300}]` con `reuseExistingServer: !process.env.CI` (mismo patrón que `apps/web/playwright.config.ts:23-43`) | Local: `test:e2e` levanta y baja los dos procesos; CI: nunca reusa | `yarn workspace @aportaya/backoffice test:e2e; echo $?` → 0 · `netstat` sin `:4300` después | TODO |
| H8.S1.M2 | Login de E2E contra Prism: fixture `sesionDeOperador` que hace `POST /sesiones` real contra el mock (no inyecta el token a mano) | Los 3 E2E existentes + los nuevos (H1.S4, H2.S4, H4.S2.M6, H5.S2.M4) usan la fixture | `grep -c "sesionDeOperador" apps/backoffice/e2e/*.ts` → ≥ 6 | TODO |
| H8.S1.M3 | Paso `f6` en `ci.yml` job `frontend`: `playwright install --with-deps chromium` + `test:e2e` del backoffice + `upload-artifact` de `playwright-report/` en `if: failure()` | El paso existe y depende de `f4` (build) | `gh run view <id> --log` → paso `f6` `✓` | TODO |
| H8.S1.M4 | E2E vigilan consola y red (regla 80.3.9): fixture que falla el test ante `console.error` o respuesta `5xx` inesperada | Test artificial con `console.error` → falla; retirado después | `evidencia/H8-S1-M4.txt` con el fallo provocado y el verde posterior | TODO |

### H8.S2 — Flutter en CI: unit, widget, contract, a11y; goldens e integración en macOS
**CA:** Dado el job `frontend`, cuando corre la etapa Flutter, entonces ejecuta `dart format --set-exit-if-changed`, `dart analyze --fatal-infos`, `flutter test test/{unidad,widget,contrato,identidad,pasanaku,a11y}`; los goldens y las pruebas de integración corren en jobs `macos-latest` propios (D-A4).
**DoD:** jobs `goldens-macos` y `movil-integracion-macos` visibles y verdes en `gh run view`; `test:goldens` no aparece en `test:front`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S2.M1 | Separar en `ci.yml` los pasos Flutter con nombre propio (`f2a · dart format`, `f2b · dart analyze`, `f2c · flutter test unidad+widget+contrato`, `f3b · flutter test a11y`) en vez de embebidos en `yarn test:front` | Cada paso reporta su propio exit | `gh run view --log` → 4 pasos listados | TODO |
| H8.S2.M2 | (D-A4) Job `goldens-macos` (`runs-on: macos-latest`, Flutter 3.44.8, `flutter test test/goldens --timeout 60s`) en cada push a `dev`; la línea base sigue siendo la de macOS (`turbo.json` "//" se actualiza: ahora sí corren en CI) | Job en verde con las goldens actuales; una golden alterada a propósito lo pone en rojo | `gh run view --log` → job `goldens-macos` `✓` · `evidencia/H8-S2-M2.txt` con el rojo provocado y revertido | TODO |
| H8.S2.M3 | (D-A4) Job `movil-integracion-macos` (`macos-latest`, simulador iPhone vía `xcrun simctl`, `flutter test integration_test -d <udid>` o `patrol test` según lo que soporte el `patrol_cli` instalado — verificar primero) con los 7 `integration_test/*_test.dart` | 7 tests en verde en simulador; `apps/movil/package.json` `test:e2e` invoca esto mismo | `gh run view --log` → job `movil-integracion-macos` `✓` con 7 passed | TODO |

### H8.S3 — Packages y matriz del CI
**CA:** Dado cada package (`ui`, `tokens`, `tutoriales`, `dominio-cliente`, `simulado`, `diseno_flutter`), cuando corre el CI, entonces tiene lint, typecheck y test reales (no `echo`).
**DoD:** `yarn turbo run lint typecheck test:front --dry-run=json` muestra 6 packages con tareas reales.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S3.M1 | `@aportaya/tutoriales` `typecheck`: reemplazar `echo 'lo typechequean las apps'` por `tsc -p tsconfig.lib.json --noEmit` propio | El package se typechequea solo | `yarn workspace @aportaya/tutoriales typecheck; echo $?` → 0 | TODO |
| H8.S3.M2 | `@aportaya/tutoriales` `test:front`: agregar vitest con al menos los specs de su lógica pura (hoy no tiene script) | ≥ 1 spec real | `yarn workspace @aportaya/tutoriales test:front` → passed | TODO |
| H8.S3.M3 | `packages/diseno_flutter`: `lint` (`dart format` + `analyze`) y `test:front` (`flutter test`) en su `package.json` si faltan | Ambos scripts reales | `yarn workspace @aportaya/diseno-flutter lint && …test:front; echo $?` → 0 | TODO |
| H8.S3.M4 | Tabla en `verificacion-final.md` §CI: workspace × (lint, typecheck, unit, a11y, build, e2e) con ✓ / — / "no aplica (no renderiza)" | 9 filas completas | `grep -c "^| @aportaya" docs/auditoria/verificacion-final.md` → 9 | TODO |

### H8.S4 — Protección de rama y CODEOWNERS (documentado, no aplicado)
**CA:** Dado `docs/auditoria/decisiones.md` §"Protección de `dev`", cuando Pablo lo lee, entonces encuentra los checks requeridos exactos (nombres de jobs), la política de PR obligatorio, y la lista CODEOWNERS por carpeta sensible; y el archivo `.github/CODEOWNERS` existe en el repo.
**DoD:** archivo commiteado; sección escrita; comandos `gh api` **propuestos**, no ejecutados.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S4.M1 | `.github/CODEOWNERS` con `apps/backoffice/src/app/nucleo/` (auth), `apps/movil/lib/dominio/cliente.dart`, `apps/movil/lib/proveedores/`, `packages/tokens/dinero/`, `.github/workflows/`, `despliegue/`, `apps/*/src/app/nucleo/gateway.ts` → dueños (según `repartos/2026-09-21/…` de este repo: Pablo; infra: Leo) | Archivo válido según sintaxis GitHub | `gh api repos/…/PasanakuFrontend/codeowners/errors` (tras push) → `errors: []` | TODO |
| H8.S4.M2 | Sección §"Protección de `dev`" con: required checks = nombres exactos de jobs (`codigo`, `frontend`, `pruebas`, `imagenes`, `seguridad`), PR obligatorio, sin push directo, review de CODEOWNERS; y la **restricción real**: repo privado en plan gratuito → 403 (H0.S3.M5 dice si rulesets están disponibles) | Sección con los comandos `gh api` listos y marcados "NO EJECUTADO — requiere confirmación de Pablo" | `grep -n "NO EJECUTADO" docs/auditoria/decisiones.md` → ≥ 1 | TODO |
| H8.S4.M3 | `dependabot.yml` (npm en raíz + pub en `apps/movil` + github-actions), semanal, PRs agrupados por tipo | Archivo válido | `gh api repos/…/dependabot/…` (tras push) → sin error de parseo, o validación con `actionlint`/schema local | TODO |

### H8.S5 — Cabeceras HTTP del frontend
**CA:** Dado el `index.html` del backoffice servido por su NGINX (imagen `aportaya/backoffice`, localizada en H0.S3.M1), cuando se hace `curl -I`, entonces responde `Content-Security-Policy` (sin `unsafe-inline` en `script-src`; `connect-src` = gateway), `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Permissions-Policy` (cámara/micrófono/geolocalización deshabilitados), `X-Frame-Options: DENY` **o** `frame-ancestors 'none'`, `Cache-Control: no-store` en HTML, `X-Robots-Tag: noindex`.
**DoD:** salida de `curl -sI` pegada; el backoffice funciona con la CSP (E2E en verde con CSP activa); consola sin violaciones CSP.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S5.M1 | Escribir la CSP del backoffice en su `nginx.conf` (o en el Dockerfile localizado): `default-src 'self'; connect-src 'self' <gateway>; img-src 'self' data:; style-src 'self' 'unsafe-inline'` (Angular inyecta estilos; registrar el `unsafe-inline` de estilos como deuda con nonce futuro); `frame-ancestors 'none'`; `base-uri 'self'`; `form-action 'self'` | `curl -sI` muestra la cabecera | `docker run … && curl -sI http://localhost:8080/ \| grep -i content-security-policy` → pegado | TODO |
| H8.S5.M2 | HSTS (`max-age=31536000; includeSubDomains`), `Permissions-Policy`, `Cache-Control: no-store` para `text/html`, `X-Robots-Tag: noindex, nofollow` | 4 cabeceras presentes | `curl -sI … \| grep -iE "strict-transport|permissions-policy|cache-control|x-robots"` → 4 líneas | TODO |
| H8.S5.M3 | E2E del backoffice con la CSP activa (servir `dist/` con la misma config NGINX en Docker local) → ningún `SecurityPolicyViolation` | 0 violaciones en `page.on('console')` | `test:e2e` contra el contenedor → passed, log de consola pegado | TODO |
| H8.S5.M4 | Web SSR (`server.ts`): mismas cabeceras vía `helmet` **solo si** ya es dependencia; si no, `res.setHeader` explícito (no se agrega dependencia sin justificar) | `curl -sI http://localhost:4000/` con las cabeceras | salida pegada | TODO |
| H8.S5.M5 | `brechas-backend.md` §"Cookies": el frontend no controla `HttpOnly/Secure/SameSite` de la cookie de refresh — se documenta qué se espera del gateway y cómo verificarlo (`curl -i POST /sesiones` → `Set-Cookie`) | Sección escrita con el comando de verificación | `grep -n "SameSite" docs/auditoria/brechas-backend.md` → 1 | TODO |
| H8.S5.M6 | `hallazgos.md` F-cabeceras → `CORREGIDO`; commit `fix(security): cabeceras HTTP del backoffice y del sitio (F-00x)` | Entrada completa | `git log --oneline -1` → el commit | TODO |

### H8.S6 — Dependencias
**CA:** Dado `yarn npm audit --all --recursive` y `flutter pub outdated`, cuando se leen, entonces cada advisory `high`/`critical` tiene parche aplicado (mismo major) o triage escrito con motivo; no hay dependencias declaradas sin uso en `apps/*/package.json`.
**DoD:** salida de audit pegada antes/después; `knip` o `depcheck` **no se agregan**: se usa `yarn why` + grep por import.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H8.S6.M1 | Triage de advisories de H0.S2.M12 en `riesgos.md` §dependencias: paquete, severidad, ruta de dependencia (`yarn why`), acción (parche/aceptar/no aplica) | Tabla completa | `grep -c "^| " docs/auditoria/riesgos.md` → ≥ n advisories | TODO |
| H8.S6.M2 | Aplicar parches **dentro del mismo major** (`yarn up <pkg>@^x`) para `high`/`critical`; `yarn install --immutable` y suite dirigida en verde | audit sin `high`/`critical` no triado | `yarn npm audit --all --recursive --severity high; echo $?` → pegado | TODO |
| H8.S6.M3 | Inventario de dependencias no usadas: para cada `dependencies` de `apps/web`, `apps/backoffice`, `packages/*` → `grep -rl "from '<pkg>'"`; las que den 0 se quitan (p. ej. `eslint-plugin-boundaries` se **conserva** porque H9 lo configura) | Lista con uso/sin uso; `yarn install` limpio tras quitar | `evidencia/H8-S6-M3.txt` con la tabla | TODO |
| H8.S6.M4 | `yarn dedupe --check` y `flutter pub deps --style=compact` sin duplicados de major | Salidas pegadas | `yarn dedupe --check; echo $?` → 0 | TODO |

---

## H9 — Fronteras reales: packages con API explícita y capas con enforcement automatizado (P1, Fase 3, §13, §14, §15)
**CA:** Dado un import `@aportaya/ui/src/internos/x` o `apps/web/src/app/nucleo/*` desde un componente de presentación hacia infraestructura, cuando corre `yarn lint`, entonces falla con la regla de boundaries; cada package exporta solo lo declarado en `exports`; `verificar_frontend.py` queda reducido a lo que ESLint/Dart no cubren aún, con la lista escrita.
**DoD:** `yarn lint` verde en el SHA final; un import prohibido de prueba hace fallar `lint` (salida pegada) y se retira; `packages/*/package.json` sin `"./*": "./src/*"`.
**Estado:** TODO

### H9.S1 — Exports explícitos por package
**CA:** Dado `@aportaya/ui` y `@aportaya/tutoriales`, cuando una app importa, entonces solo resuelve entradas listadas en `exports` (subpath por componente/molécula) y `tsconfig.base.json` deja de mapear `@aportaya/ui/*` a todo `src/*`.
**DoD:** `yarn typecheck` verde con los `paths` acotados; un import a un archivo no exportado falla en `tsc`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H9.S1.M1 | Inventariar qué archivos de `packages/ui/src` y `packages/tutoriales/src` importan hoy las apps | Tabla módulo → consumidores en `arquitectura-objetivo.md` | `grep -rhoE "@aportaya/(ui\|tutoriales)/[a-z0-9/_-]+" apps/*/src \| sort -u` → pegado | TODO |
| H9.S1.M2 | `packages/ui/package.json` `exports`: una entrada por módulo público usado (`./boton`, `./tabla`, `./estados`, …) apuntando a `./src/<modulo>/index.ts`; quitar `"./*"` | Solo los módulos de la tabla | `node -e "console.log(Object.keys(require('./packages/ui/package.json').exports))"` → sin `./*` | TODO |
| H9.S1.M3 | Idem `packages/tutoriales` | Sin `./*` | mismo comando | TODO |
| H9.S1.M4 | `tsconfig.base.json` `paths`: reemplazar `@aportaya/ui/*` y `@aportaya/tutoriales/*` por entradas explícitas coherentes con `exports` | `yarn typecheck` verde | `yarn typecheck; echo $?` → 0 | TODO |
| H9.S1.M5 | Test negativo: import temporal a `@aportaya/ui/src/interno.ts` → `tsc` falla; se retira | Salida del error pegada | `evidencia/H9-S1-M5.txt` con `TS2307` | TODO |
| H9.S1.M6 | `arquitectura-objetivo.md` §packages: API pública de cada package con su propósito, y regla "un package nuevo solo con dos consumidores reales" | Sección escrita | `grep -c "^### @aportaya/" docs/auditoria/arquitectura-objetivo.md` → 6 | TODO |

### H9.S2 — `eslint-plugin-boundaries` configurado en Angular
**CA:** Dado `eslint.config.js` de web y backoffice, cuando un archivo de `rutas/**/pantalla-*.ts` (presentación) importa `HttpClient`, `nucleo/gateway`, o `clientes/angular/*`, entonces `ng lint` falla con `boundaries/element-types`; `dominio/` no puede importar `@angular/*` salvo `@angular/core` para `InjectionToken`/`signal` (decisión registrada).
**DoD:** 3 imports prohibidos de prueba fallan (salida pegada) y se retiran; `yarn lint` verde.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H9.S2.M1 | Verificar la API de `eslint-plugin-boundaries@5` instalada (`node_modules/eslint-plugin-boundaries/README.md` o `package.json` version) antes de escribir la config: `settings['boundaries/elements']`, regla `boundaries/element-types` | Cita de la doc de la versión instalada en `decisiones.md` | `yarn why eslint-plugin-boundaries` → versión pegada | TODO |
| H9.S2.M2 | Definir elementos por carpeta en backoffice: `nucleo` (infra), `rutas/**/dominio` (domain), `rutas/**/pantalla-*` + `layout` (presentation), `clientes/angular` (contract) | Config compila (`ng lint` arranca) | `yarn workspace @aportaya/backoffice lint; echo $?` → 0 en el estado actual **o** lista de violaciones existentes a corregir | TODO |
| H9.S2.M3 | Regla: presentation → {domain, ui}; domain → {contract, dominio-cliente}; infra (`nucleo`) → {domain, contract}; nadie → `nucleo/*.interceptor` salvo `app.config.ts` | 3 imports prohibidos de prueba fallan | `evidencia/H9-S2-M3.txt` con 3 errores `boundaries/element-types` | TODO |
| H9.S2.M4 | Corregir las violaciones reales que aparezcan (mover lógica de vista a `dominio/`, inyectar puertos) — cada una como fila nueva `H9.S2.Mx` agregada al plan antes de tocarla | 0 violaciones | `yarn workspace @aportaya/backoffice lint` → 0 problems | TODO |
| H9.S2.M5 | Misma config en `apps/web` (elementos: `nucleo`, `seo`, `paginas`/`rutas`, `contenido`) | `yarn workspace @aportaya/web lint` → 0 problems | comando → pegado | TODO |
| H9.S2.M6 | `no-restricted-imports` para `clientes/angular/*` fuera de `dominio/` e `infra` (complementa boundaries para el alias) | Import desde `pantalla-*.ts` falla | spec negativo → error pegado | TODO |

### H9.S3 — Enforcement en Flutter sin regex
**CA:** Dado `apps/movil/lib`, cuando corre `flutter test test/arquitectura`, entonces un test de arquitectura (AST con `package:analyzer`, ya transitiva del SDK) falla si `pantallas/**` importa `dio`, `flutter_secure_storage`, `dart:io` o `Platform.is*`; si `dominio/**` importa `flutter/material.dart`; o si alguien fuera de `infraestructura/` usa `MethodChannel`.
**DoD:** test con 3 violaciones sintéticas (fixtures) fallando y el árbol real pasando.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H9.S3.M1 | Verificar disponibilidad de `package:analyzer` en el SDK 3.44.8 instalado (`dart pub deps`) antes de usarlo; si requiere agregar `analyzer` a `dev_dependencies`, justificarlo en `decisiones.md` | Versión y decisión registradas | `dart pub deps \| grep analyzer` → pegado | TODO |
| H9.S3.M2 | `test/arquitectura/capas_test.dart`: recorre `lib/`, parsea imports con `parseFile`, aplica la matriz de capas | El árbol real pasa | `flutter test test/arquitectura` → passed | TODO |
| H9.S3.M3 | Fixtures negativas en `test/arquitectura/fixtures/` (pantalla con `Dio()`, dominio con `material.dart`, `Platform.isIOS` fuera de infra) → el test las detecta | 3 fallos esperados en el test de fixtures | `flutter test test/arquitectura/fixtures_test.dart` → passed (asegura que detecta) | TODO |
| H9.S3.M4 | Agregar `test/arquitectura` a `test:front` de `apps/movil/package.json` | Corre en CI | `grep -n "test/arquitectura" apps/movil/package.json` → 1 | TODO |

### H9.S4 — Reducir `verificar_frontend.py` a lo no cubierto
**CA:** Dado `scripts/verificar_frontend.py`, cuando se compara con las reglas de H9.S2/H9.S3, entonces cada barrido redundante (red en vista, plataforma en vista, imports prohibidos) se elimina del script con la referencia a la regla que lo reemplaza, y quedan solo los complementarios (literal de diseño en `.html/.css`, formato de dinero en `.html`, `console.*`/`print`), con tabla en `decisiones.md`.
**DoD:** script reducido, `--self-test` propio en verde, `yarn lint` sigue invocándolo.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H9.S4.M1 | Tabla regla regex → reemplazo (ESLint/Dart test) → estado (`reemplazada` / `complementaria`) en `decisiones.md` | 15 filas (una por `barrer(...)`) | `grep -c "barrer\|complementaria\|reemplazada" docs/auditoria/decisiones.md` → ≥ 15 | TODO |
| H9.S4.M2 | Mover `console.*` a ESLint `no-console` (con `allow` para `main.ts`) y `print` a `avoid_print` en `analysis_options.yaml` (ya viene con `flutter_lints`) | Ambas reglas activas; violación sintética falla | `evidencia/H9-S4-M2.txt` con los dos errores provocados | TODO |
| H9.S4.M3 | Quitar del script los barridos reemplazados; dejar `--self-test` que ejercita los complementarios con fixtures | Script más corto; self-test verde | `python3 scripts/verificar_frontend.py --self-test; echo $?` → 0 | TODO |
| H9.S4.M4 | `hallazgos.md` F-boundaries/F-exports/F-regex → `CORREGIDO`; commit `refactor(boundaries): fronteras de packages y capas con enforcement (F-00x…)` | Entradas completas | `git log --oneline -1` → el commit | TODO |

---

## H10 — Duplicación, SSR/BFF, errores y observabilidad: una sola implementación de la infraestructura compartida (P1, Fase 3, §16, §17, §22, §23)
**CA:** Dado el código de `nucleo/` de web y backoffice, cuando se compara, entonces traza, errores y configuración viven **una** vez en un package pequeño (`@aportaya/http-nucleo` o similar, nombre decidido y registrado); `server.ts` es explícitamente un BFF con timeouts, límites, saneo de cabeceras y tests, **o** dejó de proxear; los errores HTTP se mapean a las 10 categorías del §23 y el usuario nunca ve el mensaje crudo; existe un puerto `Telemetria` con implementación "consola en dev / nula en prod" sin PII.
**DoD:** specs del package y de `server.ts`; `diff` entre `apps/*/src/app/nucleo/{traza,errores}*` → archivos eliminados; E2E existentes en verde.
**Estado:** TODO

### H10.S1 — Package `@aportaya/http-nucleo` (nombre definitivo en `decisiones.md`)
**CA:** Dado web y backoffice, cuando se compara su `nucleo/`, entonces traza, errores base y configuración del gateway existen una sola vez en un package con `exports` explícitos y las dos apps lo consumen sin copia local.
**DoD:** `diff` de los archivos movidos → eliminados en ambas apps; `yarn workspace @aportaya/http-nucleo test:front` verde; `yarn typecheck` y E2E de ambas apps en verde.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H10.S1.M1 | Crear `packages/http-nucleo/` (vitest, TS 6, `exports` explícitos: `./traza`, `./errores`, `./configuracion-angular`) con `trazaInterceptor` movido tal cual + spec de caracterización | Spec verde; ambas apps importan del package | `yarn workspace @aportaya/http-nucleo test:front` → passed · `ls apps/*/src/app/nucleo/traza.interceptor.ts` → no existen | TODO |
| H10.S1.M2 | Mover `errores.interceptor.ts` y el catálogo base de `errores.ts`; el backoffice **extiende** el catálogo con sus `AP-CU04-*` vía `provideCatalogoDeErrores([...])` | Catálogo base en el package; extensión en backoffice | spec `catálogo extendido resuelve AP-CU04-01` → PASS | TODO |
| H10.S1.M3 | Mover `gateway.ts` + `validarConfiguracion` (H5) al package como `provideGateway(modo)` | Ambas apps lo usan; `yarn typecheck` verde | `grep -rn "gatewayPorDefecto" apps/*/src` → 0 | TODO |
| H10.S1.M4 | `arquitectura-objetivo.md` §"Qué se comparte y qué no": criterio (estable, transversal, sin UI) y lo que **no** se extrajo (idempotencia, sesión, registro de acceso son del backoffice) | Sección escrita | `grep -n "no se extrajo" docs/auditoria/arquitectura-objetivo.md` → 1 | TODO |

### H10.S2 — `server.ts`: BFF declarado o proxy eliminado
**CA:** Dado `APORTAYA_GATEWAY_INTERNO`, cuando el servidor recibe `/api/*`, entonces (opción BFF) reenvía con timeout 10 s + `AbortSignal`, límite de cuerpo 1 MB, quita hop-by-hop (`connection, keep-alive, proxy-authenticate, proxy-authorization, te, trailer, transfer-encoding, upgrade`), no sigue redirecciones, agrega `x-request-id` si falta, loguea JSON sin cuerpo ni cabeceras sensibles, y mapea fallos a `502/504` con `problem+json`; **o** (opción NGINX) el bloque se elimina y `despliegue/nginx` documenta la ruta `/api`.
**DoD:** decisión en `decisiones.md` con ADR nuevo; si BFF: `server.spec.ts` (supertest) con 3 niveles; si NGINX: `grep -c fetch apps/web/src/server.ts` → 0.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H10.S2.M1 | ADR-046 "El servidor SSR del sitio: BFF acotado o solo render" con la decisión tomada según H0.S3.M1 (si NGINX ya puede enrutar `/api`, la opción es quitar el proxy) | ADR con contexto, decisión, consecuencias | `ls "docs/Arquitectura/ADR-046*"` → existe | TODO |
| H10.S2.M2 | (Si BFF) `AbortSignal.timeout(10_000)` + mapeo a `504` con `problem+json` | Test: gateway que no responde → `504` en < 11 s | `yarn workspace @aportaya/web vitest run src/server.spec.ts -t timeout` → passed | TODO |
| H10.S2.M3 | (Si BFF) Lista hop-by-hop completa + no reenviar `cookie` hacia el gateway salvo lista blanca; no reenviar `set-cookie` de vuelta salvo lista blanca | Test: cabeceras filtradas | test → passed | TODO |
| H10.S2.M4 | (Si BFF) Límite de cuerpo (`express.raw({limit:'1mb'})`) → `413`; `redirect: 'manual'` → `Location` no se reenvía crudo | Tests → passed | test → passed | TODO |
| H10.S2.M5 | (Si BFF) `x-request-id` generado con `crypto.randomUUID()` si falta; log JSON `{ts, requestId, metodo, ruta, estado, ms}` sin query ni cuerpo | Test: log no contiene `?`; `console.log` de `:137` reemplazado por el logger | test → passed · `grep -c "console.log" apps/web/src/server.ts` → 0 | TODO |
| H10.S2.M6 | (Si NGINX) Eliminar el bloque `:53-91`, mantener la inyección de `<meta>`; `despliegue/nginx/aportaya.conf` documenta `/api` → gateway | `server.ts` sin `fetch` | `grep -c "fetch(" apps/web/src/server.ts` → 0 | TODO |
| H10.S2.M7 | Quitar los comentarios de plantilla del CLI (`:15-25`, `:126-129`, `:141-143`) y dejar solo invariantes | Sin "Example Express Rest API" | `grep -c "Example" apps/web/src/server.ts` → 0 | TODO |

### H10.S3 — Errores por categoría y sin fugas
**CA:** Dado cualquier `HttpErrorResponse` o `DioException`, cuando llega a la UI, entonces se clasifica en `NetworkError | TimeoutError | AuthenticationError | AuthorizationError | ValidationError | ConflictError | RateLimitError | BusinessRuleError | ServerError | UnknownError` conservando `codigo` y `trazaId`, y el texto mostrado sale del catálogo, nunca de `error.message` del backend.
**DoD:** specs de clasificación (10 categorías × 2 plataformas); grep de `error.message`/`err.toString()` en templates → 0.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H10.S3.M1 | `errores.ts` (package H10.S1): `clasificar(HttpErrorResponse): ErrorDeAplicacion` con las 10 categorías por `status` + `codigo`; `trazaId` de `x-request-id`/cuerpo | 10 casos + `0` (red) + timeout | spec → 12 passed | TODO |
| H10.S3.M2 | `errores.interceptor.ts` lanza `ErrorDeAplicacion` en vez de `HttpErrorResponse` a las pantallas; las pantallas existentes se adaptan (cada una es una fila nueva si requiere más que el tipo) | `yarn typecheck` verde; E2E existentes verdes | `yarn typecheck && yarn workspace @aportaya/backoffice test:e2e` → 0 failed | TODO |
| H10.S3.M3 | Móvil: `_TraduccionDeErrores` produce `ErrorDeApi` con `categoria` (mismo enum en Dart) | 12 casos en `test/unidad/errores_test.dart` | `flutter test test/unidad/errores_test.dart` → passed | TODO |
| H10.S3.M4 | Test de fuga: ningún template (`.html`, `.dart` en `pantallas/`) interpola `mensaje`/`message` del error crudo | grep → 0 | `grep -rnE "error\.(message\|mensaje)\|\.toString\(\)" apps/*/src/app --include=*.html apps/movil/lib/pantallas` → 0 | TODO |

### H10.S4 — Puerto de telemetría
**CA:** Dado un error inesperado (Angular `ErrorHandler`, Flutter `FlutterError.onError`/`runZonedGuarded`) o un error HTTP `5xx`, cuando ocurre, entonces se emite `telemetria.error(evento, {ruta, version, requestId, entorno, categoria})` sin PII, a un puerto cuya implementación por defecto es nula en producción y consola en desarrollo; ningún proveedor concreto se importa desde dominio o presentación.
**DoD:** specs del puerto y del `ErrorHandler`; test que verifica que el payload no contiene claves prohibidas (`password`, `otp`, `token`, `documento`, `telefono`, `cuenta`).
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H10.S4.M1 | `Telemetria` (interfaz + `InjectionToken`) en el package H10.S1 con `error`, `evento`; implementaciones `TelemetriaNula`, `TelemetriaConsola` | spec de ambas | `yarn workspace @aportaya/http-nucleo test:front` → passed | TODO |
| H10.S4.M2 | `ErrorHandler` de Angular que clasifica y emite; incluye `version` desde `environment`/`package.json` inyectada en build, `ruta` del `Router`, `requestId` si es HTTP | spec: emite una vez por error con el shape esperado | spec → PASS | TODO |
| H10.S4.M3 | Filtro de PII: `sanear(payload)` elimina claves prohibidas y trunca strings > 200 chars; test con payload envenenado | 0 claves prohibidas en la salida | spec → PASS | TODO |
| H10.S4.M4 | Móvil: `puertos/telemetria.dart` + `runZonedGuarded` en `main.dart` + implementación nula/consola | test unitario del saneo en Dart | `flutter test test/unidad/telemetria_test.dart` → passed | TODO |
| H10.S4.M5 | `hallazgos.md` F-duplicación/F-proxy/F-errores → `CORREGIDO`; commits `refactor(packages): nucleo http compartido`, `fix(security): server.ts …`, `refactor(errores): categorías …` | Entradas completas | `git log --oneline -3` → los commits | TODO |

---

## H11 — Autorización, idempotencia y contratos OpenAPI tienen pruebas dirigidas (P1, §19, §20, §21)
**CA:** Dado el backoffice, cuando un operador sin permiso navega directo a una ruta, pulsa una acción cuyo botón estaba oculto (vía `fetch` manual en E2E) o el servidor responde `403`, entonces la UI muestra el estado "sin permiso" accionable y ninguna acción se ejecuta dos veces ante doble click, reintento tras refresh o F5 en un formulario ya enviado; ningún DTO escrito a mano duplica uno existente en `clientes/angular` o `clientes/dart`.
**DoD:** E2E `autorizacion.e2e.ts` y `idempotencia.e2e.ts` PASS; `contratos.spec.ts` (Angular) y `test/contrato/*_test.dart` ampliados; inventario de DTOs manuales → 0 duplicados o cada uno justificado.
**Estado:** TODO

### H11.S1 — Autorización: UX gating ≠ server authorization
**CA:** Dado un operador sin el permiso, cuando navega directo, pulsa una acción oculta o el servidor responde `403`, entonces ve el estado "sin permiso" accionable y el código deja escrito que la UI oculta pero no protege.
**DoD:** `autorizacion.e2e.ts` (3 casos) PASS con trace; `autorizacion.spec.ts` PASS; sección en `arquitectura-objetivo.md`.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H11.S1.M1 | E2E: sesión con permisos `['ver:operacion']`, navegar directo a `/cumplimiento/verificaciones` → redirige a `/tablero` con aviso "sin permiso" (hoy redirige mudo, `permisos.ts:15`) | Aviso visible con rol `status` | `test:e2e autorizacion -g "deep link"` → passed | TODO |
| H11.S1.M2 | E2E: Prism devuelve `403` en `GET /operacion/reclamos` → la pantalla muestra estado "sin permiso" (categoría `AuthorizationError` de H10.S3), no "error" genérico | `getByText(/no tenés permiso/i)` visible | `-g "403"` → passed | TODO |
| H11.S1.M3 | E2E: los permisos cambian durante la sesión (refresh devuelve `permisos` distintos, H1) → el menú se recalcula y una ruta que ya no alcanza redirige | Menú sin la sección; URL en `/tablero` | `-g "cambian"` → passed | TODO |
| H11.S1.M4 | Spec: `puede()` con permiso ausente → botón oculto **y** el servicio de dominio igual manda la petición si se invoca → el `403` se clasifica (documenta que la UI no protege) | spec del contenedor → PASS | `…test:front --include='**/autorizacion.spec.ts'` → passed | TODO |
| H11.S1.M5 | `arquitectura-objetivo.md` §"Autorización": tabla "qué decide la UI / qué decide el servidor" citando `permisos.ts` y `shell-financiero.ts:13` | Sección escrita | `grep -n "UX permission gating" docs/auditoria/arquitectura-objetivo.md` → 1 | TODO |

### H11.S2 — Idempotencia con semántica probada
**CA:** Dado un formulario con efecto, cuando hay doble click, reintento tras refresh, timeout con reintento, navegación atrás/adelante o F5, entonces la misma operación lógica reutiliza su clave y una operación nueva genera otra; ningún envío llega dos veces.
**DoD:** `idempotencia.interceptor.spec.ts` (2) y `idempotencia.e2e.ts` (4) PASS con conteo de peticiones y claves pegado; tabla de formularios completa.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H11.S2.M1 | Spec `idempotencia.interceptor.spec.ts`: la clave del contexto llega como `Idempotency-Key`; sin contexto no se agrega | 2 casos | `…test:front --include='**/idempotencia.interceptor.spec.ts'` → passed | TODO |
| H11.S2.M2 | Spec: reintento tras refresh (H1) conserva la **misma** clave | `expectOne` ×2 con la misma cabecera | spec → PASS | TODO |
| H11.S2.M3 | Inventario de formularios que envían con efecto (grep `claveDeIdempotencia`) y verificación de que el botón se deshabilita mientras `enviando` (regla 95.3.4) | Tabla formulario → deshabilita sí/no | `grep -rln "claveDeIdempotencia" apps/backoffice/src` → lista + tabla en `hallazgos.md` | TODO |
| H11.S2.M4 | E2E `idempotencia.e2e.ts`: doble click en "Confirmar" de un formulario de dinero (p. ej. periodo contable) → 1 sola petición con 1 clave | `page.on('request')` cuenta 1 | `test:e2e idempotencia -g "doble click"` → passed | TODO |
| H11.S2.M5 | E2E: F5 con formulario ya enviado → al reabrir, clave **nueva** (operación lógica nueva); navegación atrás/adelante en el mismo formulario → misma clave | 2 aserciones | `-g "F5"` y `-g "atrás"` → passed | TODO |
| H11.S2.M6 | E2E: timeout con respuesta desconocida (Prism tarda > timeout) → la UI ofrece "Reintentar" y el reintento lleva la **misma** clave | Clave igual en las 2 peticiones | `-g "timeout"` → passed | TODO |
| H11.S2.M7 | Móvil: `integration_test/doble_envio_test.dart` ya existe → revisar que verifique la clave y no solo el conteo; ajustar como fila nueva si falta | Test verifica cabecera `Idempotency-Key` | `grep -n "Idempotency-Key" apps/movil/integration_test/doble_envio_test.dart` → ≥ 1 | TODO |

### H11.S3 — Clientes OpenAPI como frontera
**CA:** Dado el código de dominio de las tres apps, cuando se inventarían tipos y paths manuales, entonces ninguno duplica un modelo u operación de `clientes/angular` o `clientes/dart` sin justificación, y la generación es determinista.
**DoD:** Tabla de duplicados → 0 sin justificar; `diff -rq` de dos generaciones vacío; `contratos.spec.ts` y `test/contrato/` (≥ 4) en verde.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H11.S3.M1 | Inventario de tipos/DTOs/enums escritos a mano en `apps/*/src/app/**/dominio/*.ts` y `apps/movil/lib/dominio/*.dart` que coinciden por nombre o forma con `clientes/angular/*/model/*.ts` / `clientes/dart/*/lib/src/model/*.dart` | Tabla tipo manual → tipo generado → acción | `evidencia/H11-S3-M1.txt` con la tabla | TODO |
| H11.S3.M2 | Reemplazar duplicados por el tipo generado (una fila nueva por dominio tocado); los que no tengan equivalente quedan con comentario "sin contrato OpenAPI — hueco declarado en brechas-backend.md" | `yarn typecheck` verde; 0 duplicados sin justificar | `yarn typecheck; echo $?` → 0 | TODO |
| H11.S3.M3 | Paths hardcodeados: grep `` `${gateway}/ `` en `apps/*/src` fuera de `nucleo/` → cada uno migra al método del cliente generado o se justifica (p. ej. `/sesion/refrescar` si el cliente lo expone) | Lista → 0 o justificados | `grep -rn '\${gateway}/' apps/*/src/app --include=*.ts \| grep -v nucleo/` → pegado | TODO |
| H11.S3.M4 | Determinismo de la generación: correr `generateOpenApiClients` dos veces y `diff -r` de `clientes/` → vacío (el CI ya regenera; falta la prueba de idempotencia) | `diff` vacío | `diff -rq clientes/ /tmp/clientes-2/; echo $?` → 0 | TODO |
| H11.S3.M5 | Contract tests Angular: `contratos.spec.ts` que valida las respuestas de ejemplo de `@aportaya/simulado/ejemplos` contra los tipos generados para los 3 endpoints críticos (sesión, saldo, expediente) | 3 passed | `…test:front --include='**/contratos.spec.ts'` → passed | TODO |
| H11.S3.M6 | Contract tests Dart: `test/contrato/` pasa de 1 a ≥ 4 archivos (sesión, saldo, aporte, entrega) usando los mismos ejemplos | ≥ 4 passed | `flutter test test/contrato` → passed | TODO |
| H11.S3.M7 | `hallazgos.md` F-authz/F-idem/F-openapi → `CORREGIDO`; commits `test(auth): …`, `test(e2e): idempotencia …`, `refactor(contracts): …` | Entradas completas | `git log --oneline -3` → los commits | TODO |

---

## H12 — Calidad: dinero, fechas, contenido, estados de UI, comentarios y toolchain (P2, Fase 4, §24–§30, §38–§40)
**CA:** Dado el frontend, cuando se audita, entonces todo importe pasa por `@aportaya/tokens/dinero` (con vectores ampliados: negativos, cero, enormes, redondeo), toda fecha se parsea con formato contractual y zona explícita (`America/La_Paz`), `apps/web/app.routes.ts` solo declara navegación, cada pantalla con red resuelve sus estados, no quedan comentarios narrativos históricos en archivos de configuración y hay una sola versión de TypeScript declarada (o el motivo de dos).
**DoD:** specs de dinero y fechas; `wc -l apps/web/src/app/app.routes.ts` < 80; inventario de estados por pantalla completo; `yarn why typescript` con una versión.
**Estado:** TODO

### H12.S1 — Dinero (caracterización y bordes)
**CA:** Dado cualquier importe mostrado, cuando pasa por el formatter único, entonces cero, negativos, valores enormes y redondeo dan la misma salida en Angular y en Dart contra el mismo JSON de vectores.
**DoD:** `yarn workspace @aportaya/tokens test:front` y `flutter test test/unidad/dinero_vectores_test.dart` verdes con los vectores ampliados; regla estática contra `parseFloat`/`toFixed` fuera del formatter demostrada.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H12.S1.M1 | Test de caracterización de `packages/tokens/dinero/formatear.ts` con `vectores/monto.json` ampliado: cero, negativo, `999999999.99`, `0.005` (redondeo declarado), moneda distinta de `BOB`, locale | Cada vector con salida esperada; modo de redondeo documentado en el archivo | `yarn workspace @aportaya/tokens test:front` → passed | TODO |
| H12.S1.M2 | Mismos vectores en Dart (`packages/diseno_flutter` o donde viva el formatter Dart; localizar primero) → paridad Angular/Dart probada con el **mismo JSON** | 0 divergencias | `flutter test test/unidad/dinero_vectores_test.dart` → passed | TODO |
| H12.S1.M3 | Revisar `apps/movil/lib/dominio/validacion.dart:24` (`double.parse` "permitido") → reemplazar por parseo a `Decimal`/entero de centavos si el valor luego se usa en cálculo; si solo valida forma, dejar y documentar | Decisión con evidencia de uso | `grep -rn "validacion.dart" apps/movil/lib \| head` → uso pegado | TODO |
| H12.S1.M4 | Test de arquitectura (H9.S3) y regla ESLint `no-restricted-syntax` para `parseFloat`/`toFixed`/`Number(` fuera de `packages/tokens/dinero` | Violación sintética falla | `evidencia/H12-S1-M4.txt` con el error provocado | TODO |

### H12.S2 — Fechas y zona horaria
**CA:** Dada una fecha o timestamp del contrato, cuando se parsea o formatea, entonces se usa ISO-8601 estricto con zona `America/La_Paz` explícita y ningún `new Date(string)` ambiguo queda fuera del módulo de fechas.
**DoD:** Vectores de fechas en verde en TS y Dart; grep de parseos ambiguos → 0 fuera de `fechas.ts`/`fechas.dart`.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H12.S2.M1 | Inventario de `new Date(`, `Date.parse`, `DateTime.parse`, `toLocale*`, `Intl.DateTimeFormat` en `apps/` con su propósito (timestamp, fecha de corte, expiración, ordenamiento) | Tabla en `hallazgos.md` | `grep -rnE "new Date\(\|Date\.parse\|DateTime\.parse" apps --include=*.ts --include=*.dart \| grep -v spec \| grep -v _test` → pegado | TODO |
| H12.S2.M2 | Función única `fechas.ts` en el package H10.S1 (y `fechas.dart`): parseo ISO-8601 estricto, formato de salida, zona `America/La_Paz` explícita, sin `new Date(string)` ambiguo; con vectores compartidos (incluye cambio de día en UTC vs Bolivia) | Vectores pasan en TS y Dart | `yarn … test:front` + `flutter test` → passed | TODO |
| H12.S2.M3 | Migrar los usos del inventario (una fila nueva por pantalla si excede 3 archivos) y prohibir `new Date(string)` con `no-restricted-syntax` | grep → 0 fuera de `fechas.ts` | mismo grep → 0 | TODO |

### H12.S3 — Routing y contenido
**CA:** Dado `apps/web/src/app/app.routes.ts`, cuando se lee, entonces solo declara navegación; el SEO vive en un catálogo tipado y cada contenido regulatorio tiene versión, vigencia y fuente, o está marcado `DECISION_REQUIRED`.
**DoD:** `wc -l app.routes.ts` < 80; `yarn workspace @aportaya/web test:e2e` verde; `node scripts/contenido.mjs` falla con un `.md` regulatorio sin fuente.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H12.S3.M1 | Mover los 26 bloques `MetaDeRuta`/JSON-LD de `apps/web/src/app/app.routes.ts` a `apps/web/src/app/seo/meta-por-ruta.ts` (catálogo tipado), dejando en rutas solo `path`, `loadComponent`, `data: { seo: META.tutoriales }` | `app.routes.ts` < 80 líneas; E2E web verde | `wc -l apps/web/src/app/app.routes.ts` → < 80 · `yarn workspace @aportaya/web test:e2e` → passed | TODO |
| H12.S3.M2 | Contenido regulatorio (§28): inventariar en `apps/web/contenido/**/*.md` y en código los claims (estado regulatorio, tarifas, términos) y anotar `version`, `vigente_desde`, `fuente` en el frontmatter de cada uno; los que no tengan fuente → `DECISION_REQUIRED` a cumplimiento | Tabla contenido → versión → fecha → fuente | `grep -L "fuente:" apps/web/contenido/**/*.md` → lista de faltantes pegada | TODO |
| H12.S3.M3 | `scripts/contenido.mjs` falla si un `.md` regulatorio no tiene `fuente` y `vigente_desde` | Build falla con el `.md` de prueba sin fuente | `node scripts/contenido.mjs; echo $?` → 1 con fixture, 0 sin ella | TODO |

### H12.S4 — Estados de UI por pantalla
**CA:** Dada cada pantalla con red, cuando la API devuelve datos, vacío, error, `403` o no hay conexión, entonces se muestra el estado correspondiente, distinto entre sí y accionable.
**DoD:** Inventario completo; cada estado faltante corregido con spec + captura en su microtarea agregada al plan; `test:front` y `test:a11y` verdes.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H12.S4.M1 | Inventario: cada `pantalla-*.ts` (backoffice) y `pantallas/*.dart` (móvil) con red → columnas `cargando / datos / vacío / error / sin permiso / offline / stale` marcadas sí/no/no aplica | Tabla completa en `hallazgos.md` | `find apps/backoffice/src -name 'pantalla-*.ts' \| wc -l` = filas de la tabla | TODO |
| H12.S4.M2 | Por cada pantalla con estado faltante: fila nueva `H12.S4.Mx` con CA "dado la API devuelve `[]`/`500`/`403`, cuando …, entonces se ve …" y DoD spec + captura | Cada fila agregada al plan **antes** de tocar la pantalla | `python plan_status.py` refleja el total actualizado | TODO |
| H12.S4.M3 | Estado `offline` en móvil: `sin_conexion_test.dart` (integration) ya existe → verificar que distingue offline de error de servidor; spec widget si falta | Distinción probada | `flutter test test/widget/estado_offline_test.dart` → passed | TODO |

### H12.S5 — Comentarios y toolchain
**CA:** Dado el código y la configuración, cuando se leen, entonces los comentarios dicen qué invariante existe y por qué importa (la historia está en ADR/`decisiones.md`) y hay una sola versión de TypeScript, ESLint y Angular en el árbol o el motivo de la excepción está escrito.
**DoD:** grep de comentarios narrativos → 0 en los archivos listados; `yarn why typescript` con una versión (o decisión escrita); `yarn dedupe --check` exit 0.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H12.S5.M1 | Inventario de comentarios narrativos (> 5 líneas, con "antes", "existía", "se rompía") en `turbo.json` `//`, `.yarnrc.yml`, `server.ts`, `cliente.dart`, `plataforma.dart`, `datos-simulados.ts` → mover la historia a ADR/`decisiones.md`, dejar en código solo "qué invariante / por qué importa" | Cada comentario recortado con enlace al ADR | `grep -c "Antes\|antes\|existía" turbo.json apps/web/src/server.ts apps/movil/lib/dominio/cliente.dart` → 0 | TODO |
| H12.S5.M2 | TypeScript: `packages/{tokens,dominio-cliente,simulado}` y raíz pasan de `~5.9.2` a `~6.0.2` (la versión de las apps) **si** `yarn typecheck` + `test:front` siguen verdes; si no, documentar por qué dos versiones | Una sola versión en `yarn why typescript` o motivo escrito | `yarn why typescript \| grep -c "typescript@npm:"` → 1 | TODO |
| H12.S5.M3 | ESLint 9 y Angular 22: confirmar una sola versión de cada uno en el árbol | `yarn dedupe --check` limpio | comando → exit 0 | TODO |
| H12.S5.M4 | `hallazgos.md` F-P2 → `CORREGIDO`; commits `refactor(routing): …`, `test(dinero): …`, `chore(toolchain): …` | Entradas completas | `git log --oneline -3` → los commits | TODO |

---

## H13 — Fronteras de repositorio: un solo árbol, un remoto canónico; el espejo se sincroniza y su archivado queda para Pablo (P2, §31, D-A2)
**CA:** Dado `docs/auditoria/arquitectura-objetivo.md` §"Fronteras de repositorio" y el ADR-047, cuando alguien los lee, entonces encuentra los hechos (dos remotos, mismo árbol, ya divergidos; Gradle/SQL/servicios en el mismo árbol; el CI frontend depende del job Java `codigo`), la alternativa B (frontend puro) descartada con su motivo medido en el código, la decisión A tomada (monorepo, canónico `PasanakuBackend`), y `PasanakuFrontend@dev` apuntando al **mismo SHA** que `PasanakuBackend@dev`; el archivado/renombre del remoto queda como paso para Pablo, con los comandos escritos y **no ejecutados**.
**DoD:** sección y ADR-047 en estado `aceptada`; `git ls-remote` de ambos remotos con el mismo SHA en `dev`; ningún `gh repo archive`/`rename` ejecutado.
**Estado:** TODO

### H13.S1 — Hechos y recomendación
**CA:** Dado `arquitectura-objetivo.md` §fronteras y el ADR-047, cuando Pablo los lee, entonces ve la decisión A justificada con números del código, los dos remotos en el mismo SHA, y los comandos de archivado listos para que él los ejecute.
**DoD:** Sección + ADR en estado `aceptada`; `scripts/verificar_remotos.sh` sale 0 tras la sincronización; `git ls-remote` de ambos remotos con el mismo SHA.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H13.S1.M1 | Medir el acoplamiento real: cuántos archivos de `apps/`+`packages/` importan de `clientes/` (generado desde `servicios/*/openapi`), y cuántos jobs del CI frontend dependen de Gradle | Números con comando | `grep -rl "clientes/angular" apps packages --include=*.ts \| wc -l` + `grep -n "gradlew" .github/workflows/ci.yml` → pegados | TODO |
| H13.S1.M2 | Registrar la divergencia actual entre remotos con `git log PasanakuBackend/dev ^PasanakuFrontend/dev --oneline` y viceversa | Lista de commits en cada dirección | `evidencia/H13-S1-M2.txt` | TODO |
| H13.S1.M3 | Escribir alternativas A y B con costos concretos y la **decisión A** (D-A2) justificada con los números de M1 (acoplamiento a `clientes/` y a Gradle), más lo que B exigiría para ser viable en el futuro (publicar `clientes/` como paquete versionado) | Sección con criterio explícito y decisión | `grep -n "Decisión: A" docs/auditoria/arquitectura-objetivo.md` → 1 | TODO |
| H13.S1.M4 | ADR-047 "Un solo árbol, un remoto canónico: fronteras de AportaYa" en estado `aceptada` (D-A2), con los comandos de archivado/renombre del remoto `PasanakuFrontend` marcados "NO EJECUTAR — lo ejecuta Pablo" | ADR existe; ningún `gh repo archive`/`rename` corrido | `ls "docs/Arquitectura/ADR-047*"` → existe · `gh repo view PabloArauzCaballero/PasanakuFrontend --json isArchived` → `false` | TODO |
| H13.S1.M5 | Script `scripts/verificar_remotos.sh` que compara `dev` de ambos remotos y sale 1 si divergen (en cualquier ruta): se corre al inicio de cada sesión y en el CI del canónico | Sale 1 hoy (`5d7948e` ≠ `19a621e6`) y 0 tras H13.S1.M6 | `bash scripts/verificar_remotos.sh; echo $?` → ambas salidas pegadas | TODO |
| H13.S1.M6 | Sincronizar el espejo: `git push PasanakuFrontend PasanakuBackend/dev:dev` (fast-forward, no destructivo) y configurar en el clon `git remote set-url --add --push origin <PasanakuFrontend>` para que cada push llegue a ambos | `git ls-remote` de los dos remotos muestra el mismo SHA en `dev`; el push no fue `--force` | `git ls-remote https://github.com/PabloArauzCaballero/PasanakuFrontend.git dev` = `git ls-remote …/PasanakuBackend.git dev` → mismo SHA pegado | TODO |

---

## H14 — Verificación final, revisión ultraestricta e informe (Fase 5, §47–§50)
**CA:** Dado el SHA final de `dev`, cuando se corre **todo** el pipeline (H0.S2 completo) más los gates nuevos, entonces todo está en verde con salida pegada; una segunda pasada (rol revisor) y una tercera (solo seguridad) no encuentran shortcuts, tests débiles, loops de auth, mocks productivos ni imports internos — o lo encontrado se corrigió con su microtarea; `verificacion-final.md` responde con hechos la pregunta del §49.
**DoD:** los 8 documentos del §43 completos; `REPORTE.md` acá con avance en la primera línea; CI del remoto en verde en el SHA final (`gh run view`).
**Estado:** TODO

### H14.S1 — Corrida completa
**CA:** Dado el SHA final, cuando se corre todo el pipeline en serie más los kill-tests, entonces cada comando termina en 0 (o su fallo está declarado `BLOQUEADO` con causa) y el CI remoto queda verde.
**DoD:** Tabla comando → exit en `verificacion-final.md`; `gh run view <id> --json conclusion` → `success`.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H14.S1.M1 | Repetir H0.S2.M1–M12 en el SHA final, serial, con salidas en `evidencia/H14-S1-*.txt` | 12 exit codes = 0 (o cada ≠ 0 justificado como `BLOQUEADO`) | tabla en `verificacion-final.md` §"Tests ejecutados" | TODO |
| H14.S1.M2 | E2E backoffice completo (existentes + H1.S4, H2.S4, H4.S2.M6, H5.S2.M4, H11.S1, H11.S2) contra Prism, 1 worker | 0 failed | `yarn workspace @aportaya/backoffice test:e2e` → salida pegada | TODO |
| H14.S1.M3 | Kill-tests del encabezado: 10 `401` → 1 refresh (E2E H1.S4.M1) y `yarn humo` con colección rota → exit 1 | Ambos demostrados | salidas pegadas en `verificacion-final.md` | TODO |
| H14.S1.M4 | Config de producción incompleta falla (H5): build/arranque sin gateway en las 3 apps | 3 salidas de fallo controlado pegadas | `verificacion-final.md` §"Config" | TODO |
| H14.S1.M5 | Push a `PasanakuBackend@dev` (canónico) con fast-forward de `PasanakuFrontend@dev` en el mismo paso (D-A2) y `gh run watch` en el canónico hasta completar; todos los jobs verdes, incluidos `goldens-macos`, `movil-integracion-macos` e `ios-release` | `conclusion: success`; ambos remotos en el mismo SHA | `gh run view <id> --json conclusion` → `success` · `bash scripts/verificar_remotos.sh; echo $?` → 0 | TODO |

### H14.S2 — Revisión ultraestricta (§48)
**CA:** Dado el diff completo del trabajo, cuando lo revisa un segundo rol que no confía en la primera solución y un tercero enfocado solo en seguridad, entonces cada categoría del §48 y del OWASP Top 10 tiene veredicto con evidencia y lo encontrado está corregido o declarado.
**DoD:** Tabla de 12 categorías + tabla OWASP de 10 filas en `verificacion-final.md`; `F-1xx` todos `CORREGIDO`/`A MEDIAS` con las cuatro respuestas; grep de prohibiciones §46 pegado.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H14.S2.M1 | Segunda pasada con la lista del §48 (shortcuts, falsos positivos, tests débiles, carreras, subscriptions sin lifecycle, peticiones duplicadas, loops de auth, estados imposibles, código muerto, mocks productivos, imports internos, config ambigua) sobre el `git diff 19a621e6..HEAD` — puede delegarse a **un** agente revisor de solo lectura con contrato (regla 70.4) | Lista de hallazgos nuevos `F-1xx` con evidencia o "ninguno" por categoría (12 categorías) | `grep -c "^## F-1" docs/auditoria/hallazgos.md` → n · tabla de 12 categorías | TODO |
| H14.S2.M2 | Corregir cada `F-1xx` como microtarea nueva agregada al plan | Todos `CORREGIDO` o `A MEDIAS` con las 4 respuestas | `plan_status.py` sin `EN CURSO` | TODO |
| H14.S2.M3 | Tercera pasada solo seguridad: checklist OWASP Top 10:2025 aplicado al frontend (XSS/`innerHTML`, tokens en storage, CSP, open redirect en `volverA`, PII en logs/URLs, dependencias) | Tabla categoría → control → archivo:línea → estado | `grep -c "^| A0" docs/auditoria/verificacion-final.md` → 10 | TODO |
| H14.S2.M4 | Grep final de prohibiciones §46: `any` nuevos, `eslint-disable` sin justificación, `// ignore`, `localStorage` con token, `\|\| true`, `continue-on-error`, `.only`, `skip` | Todos → 0 o justificados en la misma línea | comandos y conteos pegados en `verificacion-final.md` | TODO |

### H14.S3 — Documentos y cierre
**CA:** Dado alguien que no vio la sesión, cuando lee `docs/auditoria/` y el `REPORTE.md`, entonces sabe qué quedó confiable, qué bloqueado y por qué, con el avance calculado en la primera línea y sin procesos huérfanos en la máquina.
**DoD:** Los 8 documentos del §43 completos; `report_gate.py` no bloquea; `netstat` sin 4010/4300/8080; commit y push finales con CI verde.
**Estado:** TODO
| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H14.S3.M1 | `riesgos.md`: riesgos residuales con impacto y mitigación (incluye lo `BLOQUEADO`: auditoría server-side, iOS en dispositivo, protección de rama en plan gratuito, goldens) | Cada riesgo con dueño | `grep -c "^## R-" docs/auditoria/riesgos.md` → ≥ 6 | TODO |
| H14.S3.M2 | `verificacion-final.md` con el formato §50 (Estado inicial, P0 corregidos, P1 corregidos, Deuda restante, Bloqueos externos, Tests ejecutados, Cambios arquitectónicos, Riesgos residuales, Recomendación) y la respuesta al §49 en tres columnas: **confiable / bloqueado / por qué**, por área (identidad, sesión, dinero, permisos, auditoría, configuración, producción, CI) | 8 áreas con veredicto y evidencia enlazada | `grep -c "^| " docs/auditoria/verificacion-final.md` → ≥ 8 en la tabla del §49 | TODO |
| H14.S3.M3 | Actualizar `hallazgos.md`: ningún `F-xxx` en estado distinto de `CORREGIDO`/`BLOQUEADO`/`ABIERTO` con motivo; conteo por estado en cabecera | Cabecera con conteos = `grep` | `grep -c "Estado: CORREGIDO" docs/auditoria/hallazgos.md` = número declarado | TODO |
| H14.S3.M4 | `REPORTE.md` en este repo (regla 40): avance en la primera línea, Completado/A medias/Pendiente, evidencia, no cubierto, desvíos, riesgos, decisiones | `report_gate.py` no bloquea | `python .claude/hooks/report_gate.py --self-test; echo $?` → 0 y reporte con las 3 secciones | TODO |
| H14.S3.M5 | Commit final `docs(audit): verificación final del frontend en <SHA>` y push; `gh run view` verde; procesos locales (Prism, `ng serve`, Docker del NGINX) cerrados | Nada escuchando en 4010/4300/8080 | `netstat -ano \| findstr ":4010 :4300 :8080"` → vacío | TODO |

---

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Sin JDK/Flutter en la máquina: no se pueden generar clientes ni compilar (ver H0.S1, microtareas M2 a M4) | Bloquea **todo** H0.S2 | Instalar Temurin 21 y Flutter 3.44.8 antes de cualquier otra cosa; si no se puede, H0 queda `BLOQUEADO` con el comando exacto y se usa el CI como runner (push a rama `pablo/auditoria-frontend`) |
| El contrato de `/sesion/refrescar` no rota el refresh o usa cuerpo en móvil y cookie en web (D3/A3) | H1 "caso rotación" no se puede verificar contra lo real | Simular los tres niveles contra Prism con el ejemplo del contrato; registrar en `brechas-backend.md`; nunca declarar `VERIFIED` la rotación sin backend real |
| `POST /extraccion/accesos` no existe (D4) | H3 solo puede cerrar el lado cliente | Flag `auditoriaCliente: desactivada` + brecha documentada; F-auditoría queda `BLOQUEADO` del lado backend |
| Sin Mac: iOS no se puede compilar ni probar en dispositivo | H6 solo llega a `TESTED` (detección) | Tests con `debugDefaultTargetPlatformOverride`; `BLOQUEADO` explícito para la verificación real con dueño Pablo |
| Repo privado en plan gratuito: sin branch protection (403) | §12 no aplicable tal cual | Documentar; evaluar rulesets (D9); recomendar hacer público o Pro como decisión de Pablo |
| El E2E del backoffice contra Prism necesita sesión válida que Prism no emite de forma consistente | H8.S1 podría depender de datos del mock | Fixture `sesionDeOperador` contra el ejemplo de `POST /sesiones` del contrato; si Prism no lo soporta, `@aportaya/simulado` extiende el ejemplo (es su propósito) |
| `eslint-plugin-boundaries@5` puede haber cambiado su API respecto a lo conocido | Config inválida | `H9.S2.M1` verifica la doc instalada **antes** de escribir la config (regla 00.1.3) |
| Extraer `nucleo/` a un package rompe el `boundaries` recién configurado o los E2E | Regresión en H10 | H10 corre después de H9 y re-ejecuta `yarn lint` + E2E como DoD |
| Los dos remotos siguen divergiendo mientras se trabaja (hasta que Pablo archive `PasanakuFrontend`) | Conflictos al final; el backend puede haber tocado `apps/` | D-A2: canónico `PasanakuBackend`; `scripts/verificar_remotos.sh` (H13.S1.M5) al inicio de cada sesión; fast-forward del espejo en cada push (H13.S1.M6) |
| Release iOS sin *secrets* de App Store Connect | El IPA queda sin firmar; no hay TestFlight hasta que Pablo cargue `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY`, certificado y perfil | El job produce el IPA sin firmar en cada corrida y marca `testflight` como `skipped` explícito (H6.S3.M4); la lista de secrets vive en `decisiones.md` |
| Versionar `clientes/` genera diffs grandes en cada cambio de contrato | PRs ruidosos | Es el costo aceptado de D-A1; `.gitattributes` con `linguist-generated=true` para `clientes/**` (colapsa el diff en GitHub) como microtarea de H0.S1.M8 |
| Presupuesto de minutos de GitHub Actions para `macos-latest` (D-A4/D-A5 suman 3 jobs macOS por push) | El CI del canónico puede agotar minutos del plan | Medir la duración en las primeras corridas (`gh run view --json jobs`); si supera lo aceptable, `ios-release` pasa a correr solo en `workflow_dispatch` y tags, **nunca** se elimina; decisión de Pablo registrada |
| Cambios de contrato en `identidad` durante el plan del backend (step-up JWT) | Los clientes generados cambian de forma | `generateOpenApiClients` en cada sesión; `yarn typecheck` detecta la ruptura; se agrega fila al plan |
| Un fix de P0 rompe `verificar_frontend.py` (p. ej. `HttpBackend` en `nucleo/` cae en "sin red en vista") | `yarn lint` rojo | Los archivos de `nucleo/` ya están en la lista permitida del barrido (`verificar_frontend.py:78`); verificar en el DoD de `H1.S2.M1` |

---

## Registro de cambios del plan

| Versión | Fecha | Qué cambió | Por qué |
|---|---|---|---|
| v1 | 2026-09-21 | Plan inicial: 15 hitos, 48 subtareas, 237 microtareas; seis ambigüedades A1–A6 registradas con supuesto y destinatario. | Fases 0–2 de la regla 10 a partir del metaprompt. |
| v2 | 2026-09-21 | Las seis ambigüedades pasan a decisiones D-A1…D-A6 tomadas por Pablo en sesión (§1). Se agregan H0.S1.M7–M9 (clientes versionados), H6.S3 (release iOS en macOS, 6 microtareas), H13.S1.M6 (sincronización del espejo); se reescriben H5 (same-origin / `API_HOSTS`), H8.S2.M2–M3 (jobs macOS definitivos), H13 (decisión A tomada), H14.S1.M5 y la fila "Rama y remotos" de §0; tres riesgos nuevos. | Regla 20 §6.7: el plan se corrige explícitamente, no se ejecuta algo distinto de lo escrito. |
