# Daily — turno noche — 2026-09-21

> **AVANCE DEL TURNO: 0 / 615 — 0 %.**
> **Estado:** `IN_PROGRESS`. Escrito **al repartir**, antes del turno: todo resultado está en
> `NOT_RUN` a propósito, porque nadie ejecutó nada todavía.

- **Turno:** noche · **Fecha:** 2026-09-21 · **Dos áreas y TRES bloques:** [`Backend/`](Backend/) (bloque A, 213 microtareas) y [`Frontend/`](Frontend/), bloque B (146) y bloque C (256) — **corrección 2026-09-21: los dos bloques del área frontend son el mismo repo, Pasanaku** (antes, el bloque B decía `mantra-core-health`)
- **Modelo de datos de referencia (backend):** `Pasanaco_backendBO/docs/Index.md`
- **Plan madre (backend):** `docs/trabajo/2026-09-21-backend-production-ready/PLAN.md` (210 microtareas; el área backend suma 213 porque cada carril arranca con el baseline de su módulo)
- **Repo del área backend:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` · `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · `test` = espejo de `dev`
- **Repo del área frontend:** el mismo que el backend — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico) · espejo `PasanakuFrontend` · rama base **`dev`** · **el SHA lo registra cada uno en su primera microtarea** (AMB-F4). Hasta el 2026-09-21 decía `mdavila-2001/mantra-core-health` @ `mockup` para el bloque B — corregido, ver la nota bajo "Bloque B" más abajo.
- **Objetivo del área backend:** `dev` production-ready, técnicamente demostrable: idempotencia con el scope del índice, outbox que publica, MFA step-up sin bypass, doble aprobación en la aplicación, JWT/arranque seguros, CI verde con SCA/SBOM/Trivy, borde con rate limiting, y `FINAL_REPORT.md` con estado sustentado.
- **Objetivo del área frontend:** el refactor del prompt maestro, demostrable: contenedores que deciden y presentación que dibuja, estado con dueño escrito, una tabla canónica con dos consumidores reales migrados, diálogo y host de estados compartidos, un inventario y un grafo de usos que no mienten, y un catálogo que monta la implementación real en un preview aislado.

> **Corrección 2026-09-21 (Pablo, en sesión):** hasta hoy, este párrafo decía que el área frontend
> tenía dos repos distintos (bloque B `mantra-core-health`, ajeno a Pasanaku, sin reglas 91/98; y
> bloque C AportaYa, con las dos). Era la lectura acordada del documento antecedente para los cinco
> carriles (`AMB-F2`), pero Pablo confirmó que el bloque B **también** es Pasanaku: los dos bloques
> son el mismo repo (`PasanakuBackend`/`PasanakuFrontend` @ `dev`). Las reglas 91 y 98 se evalúan
> **por carril**, no por bloque: ver la nota bajo "Bloque B" y el encabezado de cada `PRx` para el
> detalle. Lo que sigue igual: plan, evidencia, reporte, no inventar, alcance.

## 1. Quién tiene qué

### Bloque A — área backend · `PasanakuBackend` · 213 microtareas

| Persona | Servicio | Encargo | Hitos | Subtareas | Microtareas | Estado |
|---|---|---|---:|---:|---:|---|
| **Richard** | `identidad` | [Challenge MFA con propósito, evidencia step-up y arranque seguro](Backend/Richard/PR1-Identidad.Servicio/StepUpMfaJwtYArranqueSeguro.md) | 3 | 9 | 28 | `NOT_RUN` |
| **Justin** | `nucleo-financiero` | [Idempotencia con scope, MFA step-up y doble aprobación de retiro](Backend/Justin/PR2-NucleoFinanciero.Servicio/IdempotenciaMfaYDobleAprobacionDeRetiro.md) | 4 | 13 | 42 | `NOT_RUN` |
| **Leo** | `plataforma/comun-*`, `buildSrc`, plantilla | [Outbox que publica, helper de idempotencia y guardas comunes](Backend/Leo/PR3-Plataforma.Infra/OutboxQuePublicaYGuardasComunes.md) | 4 | 13 | 49 | `NOT_RUN` |
| **Marcelo** | `aportes`, seguridad transversal, base, scripts | [Inventario, idempotencia de aportes, ledger, base y código muerto](Backend/Marcelo/PR4-Seguridad.Transversal/InventarioIdorLedgerBaseYCodigoMuerto.md) | 6 | 11 | 40 | `NOT_RUN` |
| **Pablo** | CI, supply chain, `gateway`, `despliegue/`, operación | [Baseline, CI verde sin trampas, borde, carga y cierre](Backend/Pablo/PR5-Ci.Operacion/CiRealSupplyChainBordeYCierre.md) | 5 | 17 | 54 | `NOT_RUN` |
| | | | **22** | **63** | **213** | |

### Bloque B — área frontend · Pasanaku (`PasanakuBackend`/`PasanakuFrontend`) @ `dev` · 146 microtareas

> **Corrección 2026-09-21 (Pablo, en sesión) — los cinco carriles:** el bloque B completo
> (`PR6`, `PR7`, `PR8`, `PR9`, `PR10`) se escribió originalmente contra
> `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura).
> Confirmado y corregido para los cinco: repo, rama (`dev`, no `mockup`) y comandos reales de
> Pasanaku. Detalle por carril en `docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku/`,
> `docs/trabajo/2026-09-21-correccion-bloques-richard-y-pablo-c/`,
> `docs/trabajo/2026-09-21-correccion-bloques-leo/` y
> `docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/`. Las reglas 91 y 98 se reevaluaron
> por carril, no en bloque: 91 aplica condicionada a que el trabajo de cada uno toque un componente
> o pantalla de dinero (Pablo, Richard, Leo, Justin); 91 y 98 no aplican en el de Marcelo (inventario
> puro, no muta producto).

| Persona | Qué le toca | Encargo | Hitos | Subtareas | Microtareas | Estado |
|---|---|---|---:|---:|---:|---|
| **Richard** | pantalla piloto: smart / presentational y propiedad del estado — **retargeteado a Pasanaku 2026-09-21** | [Quién decide y quién dibuja](Frontend/Richard/PR6-SmartPresentational.Frontend/QuienDecideYQuienDibuja.md) | 4 | 7 | 24 | `NOT_RUN` |
| **Justin** | el organismo tabla y dos consumidores reales — **retargeteado a Pasanaku 2026-09-21** | [La tabla canónica y dos consumidores migrados](Frontend/Justin/PR7-DataTable.Frontend/TablaCanonicaYDosConsumidores.md) | 4 | 8 | 27 | `NOT_RUN` |
| **Leo** | contrato de estado, host de estados, diálogo y borrador — **retargeteado a Pasanaku 2026-09-21** | [Diálogo, host de estados y borrador](Frontend/Leo/PR8-DialogoYEstados.Frontend/DialogoHostDeEstadosYBorrador.md) | 4 | 8 | 26 | `NOT_RUN` |
| **Marcelo** | inventario, grafo de usos, matriz de familias y retirada | [El mapa que no miente](Frontend/Marcelo/PR9-InventarioYFamilias.Frontend/InventarioGrafoDeUsosYFamilias.md) | 5 | 9 | 31 | `NOT_RUN` |
| **Pablo** | catálogo fiel, preview aislado, gates y cierre del alcance — **retargeteado a Pasanaku 2026-09-21** | [Catálogo fiel, preview aislado y gates](Frontend/Pablo/PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md) | 5 | 11 | 38 | `NOT_RUN` |
| | | | **22** | **43** | **146** | |

### Carga por persona — y por qué está así

| Persona | Backend | Frontend | Total |
|---|---:|---:|---:|
| Richard | 28 | 24 | **52** |
| Justin | 42 | 27 | **69** |
| Leo | 49 | 26 | **75** |
| Marcelo | 40 | 31 | **71** |
| Pablo | 54 | 38 | **92** |
| | **213** | **146** | **359** |

> **Esto es más de lo que entra en un turno, y está escrito así a propósito.** La regla del
> reparto es que el encargo se escribe **completo y ordenado por dependencia**, aunque exceda el
> turno: lo que no se cierre va `A MEDIAS` con qué anda, qué no anda y qué falta exactamente.
> **Recortar el alcance es decisión de coordinación y se registra** (AMB-F1) — no se resuelve
> borrando microtareas ni marcando `HECHO` lo que no corrió.
>
> **Un trabajo activo por vez** (regla 70.1): el backend es el **bloque A** y el frontend el
> **bloque B**. Nadie abre su carril de frontend sin haber cerrado el de backend o haberlo dejado
> `A MEDIAS` con las cuatro respuestas en su daily. Dos carriles en `EN CURSO` a la vez es el
> defecto que esta regla existe para evitar.

### Bloque C — área frontend · **AportaYa** · monorepo @ `19a621e6` · 256 microtareas

> **Corrección 2026-09-21: mismo repositorio que el bloque B**, no otro. Acá las reglas 91 (dinero)
> y 98 (microservicios) **aplican siempre**, porque es la plataforma que administra plata de
> terceros — a diferencia del bloque B, donde aplican solo condicionadas al trabajo de cada carril.
> Leer el encabezado del encargo antes de arrancar.

- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 — 247 microtareas repartidas por tema técnico; cada carril suma su propia línea base, por eso el bloque suma 256.
- **Repo:** `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · `PasanakuFrontend` es su espejo y se sincroniza por fast-forward.
- **Objetivo:** que el frontend deje de fingir — un solo refresh ante N `401`, la sesión se restaura al recargar, producción no muestra datos de ejemplo ni llama a `localhost`, el CI corre lo que dice correr con release iOS en macOS, las fronteras se hacen cumplir solas, y un informe que responde con hechos qué es confiable y qué no.

| Persona | Qué le toca | Encargo | Hitos | Subtareas | Microtareas | Estado |
|---|---|---|---:|---:|---:|---|
| **Richard** | refresh single-flight, restauración de sesión y auditoría de lectura | [La sesión deja de mentir: un refresh, una restauración y una auditoría que no finge](Frontend/Richard/PR11-Sesion.Frontend/RefrescoRestauracionYAuditoria.md) | 4 | 11 | 51 | `NOT_RUN` |
| **Justin** | datos simulados aislados, configuración fail-fast y estados de UI | [Producción no muestra cifras inventadas ni llama a la máquina del usuario](Frontend/Justin/PR12-Config.Frontend/ConfiguracionFailFastYMocksAislados.md) | 4 | 7 | 36 | `NOT_RUN` |
| **Leo** | capabilities iOS, release iOS en macOS, humo honesto, CI real y cabeceras | [El CI deja de mentir: E2E del backoffice, dos jobs macOS, release iOS y cero `|| true`](Frontend/Leo/PR13-Ci.Frontend/CiRealMacosYReleaseIos.md) | 5 | 12 | 52 | `NOT_RUN` |
| **Marcelo** | exports explícitos, boundaries, núcleo HTTP compartido, errores, telemetría y calidad | [Fronteras que se hacen cumplir solas, un núcleo compartido y un proxy que deja de ser accidental](Frontend/Marcelo/PR14-Fronteras.Frontend/FronterasNucleoCompartidoYCalidad.md) | 5 | 13 | 59 | `NOT_RUN` |
| **Pablo** | línea base global, clientes versionados, autorización, idempotencia, contratos y cierre | [La línea base que nadie discute, los contratos como frontera y el cierre con hechos](Frontend/Pablo/PR15-Contratos.Frontend/LineaBaseContratosAuthzYCierre.md) | 5 | 10 | 58 | `NOT_RUN` |
| | | | **23** | **53** | **256** | |

**Reservas de archivos del bloque C** — dos personas en el mismo archivo es un defecto del
reparto, no un accidente. Verificado con
`python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py` → 37 rutas
reclamadas, **0 colisiones**.

| Persona | Es dueña de |
|---|---|
| **Richard** | `nucleo/sesion*`, `permisos.ts`, `registro-de-acceso*`, `app.config.ts`, `rutas/ingreso/**`, `movil/lib/dominio/cliente.dart`, `movil/lib/proveedores/sesion.dart` |
| **Justin** | los dos `nucleo/gateway.ts`, `rutas/sistemas/**`, `packages/simulado/**`, `dominio-cliente/src/configuracion.ts`, `movil/lib/dominio/configuracion.dart` |
| **Leo** | `.github/**`, `package.json` raíz, `scripts/humo.mjs`, `movil/lib/infraestructura/**`, `movil/ios/**`, `despliegue/nginx/**`, los dos `playwright.config.ts` |
| **Marcelo** | `packages/{ui,tutoriales}/package.json`, el package de núcleo HTTP, `tsconfig.base.json`, los dos `eslint.config.js`, `web/src/server.ts`, `web/src/app/app.routes.ts`, `scripts/verificar_frontend.py` |
| **Pablo** | `.gitignore`, `.gitattributes`, `clientes/**`, `docs/auditoria/**`, los ADR, `scripts/verificar_remotos.sh` |

**Entregas entre carriles** — ninguna autoriza a editar el archivo del otro, y ninguna habilita a
declararse `BLOQUEADO` por esperar: si el contrato se puede nombrar, se simula en tres niveles y se
cierra contra el doble (regla 65).

| Entrega | De | Para | Cómo sigue quien la espera |
|---|---|---|---|
| Providers de configuración y fuentes cableados en `app.config.ts` | Justin | Richard (dueño del archivo) | Justin los prueba con `TestBed`; el cableado es microtarea de Richard |
| Pasos de CI nuevos (E2E del backoffice, clientes al día, jobs macOS) | todos | Leo (dueño de los flujos) | Cada uno deja el comando exacto en `entregables/`; Leo lo cablea |
| Package de núcleo HTTP con traza, errores y telemetría | Marcelo | Richard y Justin | Hasta que exista, cada app usa su copia local; la migración de imports es microtarea de Marcelo |
| Clientes generados versionados | Pablo | todos | Hasta el commit, cada uno genera con la tarea del proyecto |
| Contrato real del refresco y del registro de accesos | Pablo | Richard | Richard arranca contra el doble con cookie y declara el peldaño |

## 2. Lo primero, para todos

Antes de la primera microtarea: instalar el estándar (sección 1 del encargo) y **pegar la salida
de los dos comandos** en el daily personal. Después, **el baseline de tu módulo** (es la primera
microtarea de cada encargo): nadie toca código sin saber qué estaba rojo antes.

Los dos merges que abren el turno, en este orden:

1. **Pablo · H2.S1 — Spotless** en la primera media hora: hoy `dev` está rojo en "2 · formato" y
   deja `skipped` todo lo demás (`gh run view 35644455765`). Cuando avise, todos rebasean.
2. **Leo · H3.S3.M1 — plantilla de perfiles** (`application-{local,test,staging,production}.yml`
   en `scripts/nuevo_servicio.py`) en la primera hora. Richard, Justin y Pablo (gateway) la
   aplican a su servicio; si no llegó, la escriben a mano con la misma forma y lo anotan.

### Un comando para Pablo antes de arrancar — el ruleset mínimo

El agente que armó el reparto intentó crearlo y **no tiene permiso** para modificar recursos compartidos del repo. Es una línea:

```bash
gh api --method POST repos/PabloArauzCaballero/PasanakuBackend/rulesets --input repartos/2026-09-21/PromptNoche/Pablo/PR5-Ci.Operacion/entregables/ruleset-minimo.json
gh api repos/PabloArauzCaballero/PasanakuBackend/rulesets --jq '.[].name'   # → proteccion-minima
```

Bloquea force-push y borrado en `dev`, `test` y `main`; **no** exige PR ni aprobaciones, así que no frena a nadie. El ruleset completo va en la promoción.

### El ritual de entrega es el mismo para los cinco

```bash
git fetch origin && git checkout -b <persona>/feature/carril-PR<n>-<slug> origin/dev
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/dev
./gradlew spotlessApply <gate del módulo> spotlessCheck
git push -u origin HEAD
gh pr create --base dev --fill --title "<prefijo>: <subtarea>"
gh pr merge --rebase                                   # dev sin protección: mergea ya, el CI corre igual
git fetch origin && git push origin origin/dev:test    # test es espejo de dev
```

- **Micro-PR al troncal** para `sql/` (siempre vía `scripts/generar_ddl.py`, nunca DDL a mano),
  `gradle/libs.versions.toml`, `buildSrc/`, `scripts/nuevo_servicio.py`: un commit con solo eso,
  título `troncal(<que>): …`, mergeado a `dev` **dentro de la hora**; después todos rebasean.
  Es el contrato de carril del backend (`planes/07` §6, `planes/19` §3).
- **Merge = tu gate local en verde.** Un CI rojo por un job ajeno se anota como hallazgo y no
  detiene a nadie. Un test propio en rojo detiene **esa** microtarea, nunca el carril.
- **Nunca** `skip`, `@Disabled`, `|| true`, borrar una constraint, bajar un permiso ni apagar RLS.

### Lo primero del bloque B — área frontend

Mismo arranque: instalar el estándar y pegar las dos salidas en el **daily de frontend** (es otro
archivo, en `Frontend/<Persona>/`), y después el baseline del repo. Nadie toca código sin saber qué
estaba rojo antes.

Las **tres publicaciones de la primera hora** del área frontend, que destraban a los demás:

1. **Pablo · H1.S1.M2 — la tabla de comandos reales.** Hoy nadie sabe si el runner es Vitest,
   Playwright o Cypress, ni cómo se llama cada script: el documento antecedente da candidatos, no
   hechos (AMB-F6). Pablo los confirma leyendo `package.json` y los publica acá, en §2-bis. Los
   otros cuatro los usan; nadie los redescubre por su cuenta.
2. **Leo · H1.S2.M2 — el contrato de estado.** PR con solo eso, título `contrato(estado): …`,
   mergeado a `dev` dentro de la hora. Es el equivalente frontend del micro-PR al troncal.
   Justin y Pablo construyen contra él; si no llega, trabajan contra un doble y lo declaran.
3. **Richard, Justin y Leo · las reservas de pantallas.** Richard publica su pantalla piloto,
   Justin sus dos consumidores y Leo sus dos modales, **en §4**, antes de escribir código. Un
   archivo no puede ser piloto de uno y consumidor de otro: el primero que lo publica se lo queda
   y el otro elige otro (AMB-F7).

### §2-bis. Tabla de comandos del repo frontend — corregida 2026-09-21

Los candidatos originales venían del documento antecedente de `mantra-core-health` y **eran
hipótesis, no hechos** de Pasanaku. Reemplazados por los reales, verificados contra `package.json`
raíz y `turbo.json` de `PasanakuBackend`:

| Alias | Candidato real (Pasanaku) | Confirmado por cada carril en su H1 |
|---|---|---|
| `CMD_LINT` | `turbo run lint` | |
| `CMD_TYPECHECK` | `turbo run typecheck` | |
| `CMD_TEST` | `turbo run test:front` | |
| `CMD_A11Y` | `turbo run test:a11y` | |
| `CMD_BUILD` | `turbo run build` | |
| `CMD_E2E` | `yarn workspace @aportaya/web test:e2e` o `@aportaya/backoffice`, según la app | |
| `CMD_STOCK` / `CMD_VISTAS` | no confirmados en la raíz — cada carril que los necesite los busca en H1, no los inventa | |

### El ritual de entrega del área frontend

```bash
git fetch origin && git checkout -b <persona>/frontend/<slug> origin/dev
git fetch origin && git rebase origin/dev
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base dev --fill --title "<prefijo>: <subtarea>"
```

- **PR contra `dev`**, la rama real de Pasanaku (corrección 2026-09-21: antes decía `mockup`, base
  de `mantra-core-health`). `main` **no se toca**. `PasanakuFrontend` (espejo) se sincroniza por
  fast-forward después, no en cada PR (decisión D-A2 del plan madre).
- **Prohibido actualizar una dependencia, instalar una librería nueva o mezclar gestores de
  paquetes** para facilitar el refactor. Si algo imprescindible falta, se documenta necesidad y
  compatibilidad, y se decide; no se instala de hecho.
- **Prohibido revertir cambios ajenos** o usar limpieza destructiva para conseguir una base cómoda.
- El SHA `5a0776c6…` del documento original es **referencia histórica, no una orden de resetear**
  el repositorio (AMB-F4).

## 3. Orden de dependencia — quién espera a quién

| Quien espera | De quién | Qué exactamente | Qué hace mientras tanto |
|---|---|---|---|
| Justin (H2) | **Richard (H1.S2)** | La evidencia step-up (JWT) | **Doble en tres niveles** (`EmisorDeEvidenciaDePrueba` + JWKS de prueba, H2.S2.M1): correcto / al borde de `exp` y `jti` repetido / otra clave, otro `sub`, otro propósito. Cierra H2 entero; la integración real es H2.S4.M2 y si no llega queda `A MEDIAS` declarada |
| Richard (H2.S2) | **Leo (H3.S1)** | El decodificador común que exige `iss`/`aud` | No espera: **emite** los claims del contrato y los verifica parseando con Nimbus en su test |
| Justin, Richard, Marcelo | **Leo (H3.S3.M1)** | La plantilla de `application-*.yml` | Si no está en `dev` a la hora: la escriben a mano con la misma forma y lo anotan en §6 |
| Leo (H2.S2) | nadie | Un caso de uso que emita al outbox | **Emisor y consumidor de prueba propios** en `comun-mensajeria/src/e2eTest` (AMB-10) |
| Marcelo (H3.S1.M3) | **Justin (H1)** | El scope corregido del ledger para la aserción de replay | Escribe el escenario; si el fix no está, esa aserción queda `A MEDIAS` declarada y sigue con los otros 10 |
| Marcelo (H5.S1.M2) | Richard, Justin (auditoría en sus CU) | Que los CU críticos usen la bitácora | Escribe `AuditoriaCriticaTest`; en rojo por bug ajeno → hallazgo al dueño, test en su rama, sigue |
| Pablo (H2.S6.M1/M3) | Justin, Leo, Marcelo | Los E2E financieros y los scripts de inventario | Cablea los jobs igual: los corredores toleran cero tests; los pasos de scripts quedan preparados y declarados |
| Pablo (H5.S4) | los cuatro | Las bitácoras `carriles/PR1…PR4.md` | Consolida al cierre con lo que haya; lo que falte va `A MEDIAS`/`PENDIENTE` en `FINAL_REPORT.md`, nunca `READY` sin evidencia |
| Todos | proveedor de OTP, pasarela, proveedor de retiros (no existen) | Los contratos externos | **Dobles en tres niveles** bajo `@Profile({"local","test"})`; producción sin adaptador real **no arranca** (fail closed) |

> **Nadie se queda esperando (regla 65).** Si el contrato de lo que falta se puede nombrar, se
> simula en tres niveles —correcto, límite, inválido— y se cierra contra el doble, declarándolo.
> Lo único que queda abierto es una decisión de negocio (`DECISION_REQUIRED`) o una acción sobre
> algo compartido (aplicar rulesets: solo Pablo, por escrito).

**Si dos personas miden lo mismo y les da distinto, eso es un hallazgo, no un empate a resolver
charlando.** Gana el archivo abierto, y la diferencia se registra en §6.

### Área frontend — quién espera a quién, y qué hace mientras tanto

| Quien espera | De quién | Qué exactamente | Qué hace mientras tanto |
|---|---|---|---|
| Todos | **Pablo (H1.S1.M2)** | La tabla de comandos reales del repo | No espera: cada uno lee `package.json` para lo suyo y lo contrasta con la tabla cuando se publica. Una diferencia entre dos mediciones es un hallazgo, no un empate |
| Justin (H2.S1.M4) | **Leo (H1.S2.M2)** | El contrato de estado con todas sus variantes | **Doble en tres niveles**: correcto (colección con filas válidas) · límite (colección vacía; una sola fila; respuesta marcada obsoleta) · inválido (error con identificador de petición; sin permiso; no encontrado). Cierra H2 contra el doble y deja la adopción del tipo real como microtarea diferida y declarada |
| Richard (H3.S1.M1) | **Leo (H1.S2.M2)** | El mismo contrato, para tipar su contrato de vista | Consume el tipo **actual** del repo y lo declara; si Leo publica antes de que cierre H3, lo adopta |
| Pablo (H2.S2.M2) | **Marcelo (H3)** | El grafo de usos para navegar de una familia a sus consumidores | Usa la fuente de usos que ya exista, declarándola; la navegación sobre el grafo nuevo queda diferida |
| Pablo (H2.S1, fichas) | **Justin (H4), Leo (H4)** | Los organismos migrados, para acreditar sus fichas | Acredita el **mecanismo** con componentes que ya existen y deja la adopción de esas dos fichas diferida y declarada. Mejorar el catálogo no es condición para que los otros avancen, ni al revés |
| Marcelo (H5) | **Richard, Justin, Leo** | Qué consumidores quedaron comprometidos | Toma lo publicado en §4; lo que llegue después queda diferido. **No retira nada con un consumidor de producto vivo** |
| Richard, Justin, Leo | entre sí | Que las pantallas reservadas no se solapen | Se publican en §4 en la primera hora; el primero que publica se la queda |
| Todos | producto (decisiones de negocio) | Qué debe pasar con un borrador si la entidad cambia; si una diferencia entre dos pantallas es de dominio | Se registra como ambigüedad con el supuesto conservador tomado, y se implementan las ramas que sí están definidas. **Ante la duda no se fusiona** |

> **Nadie se queda esperando, tampoco acá (regla 65).** Si el contrato de lo que falta se puede
> nombrar, se simula en tres niveles y se cierra contra el doble, declarándolo. Y **un doble no
> acredita la integración**: sustituye la espera, no la verificación final.

## 4. Reservas de archivos y servicios — para que nadie se pise

| Servicio / área | Reservado para |
|---|---|
| `servicios/identidad/**`; `docs/operacion/jwt-key-rotation.md`; `docs/auditoria-produccion/contratos/step-up-jwt.md`; `ADR-048` | **Richard** |
| `servicios/nucleo-financiero/**` (salvo los 3 tests de Marcelo); `docs/operacion/{provider-timeout,withdrawal-reconciliation}.md`; `ADR-049` | **Justin** |
| `plataforma/comun-{dominio,datos,web,mensajeria,archivos,pruebas}/**`; `buildSrc/**`; `scripts/nuevo_servicio.py`; `contratos/evento-kafka.md`; `ADR-046`, `ADR-047` | **Leo** |
| `servicios/aportes/**`; `scripts/verificar_seguridad.py`, `scripts/inventario_endpoints.py`, `scripts/verificar_contratos_limites.py`; `sql/50_verificacion/**`; los tests `LibroInvariantesTest`, `LibroBenchmarkTest`, `AppendOnlyTest`, `AislamientoEsquemaTest` (por servicio), `AuditoriaCriticaTest`, `ArchivosSeguridadTest` en cualquier módulo; `docs/auditoria-produccion/{endpoints,security-matrix,financial-invariants,dependencias,mutation-testing,idempotencia-scope}.md`; `docs/operacion/schema-changes.md` | **Marcelo** |
| `.github/**`; `despliegue/**`; `docker-compose.coolify.yml`; `scripts/generar_{compose,gateway,k8s}.py`; `plataforma/gateway/**`; `carga/**`; `build.gradle.kts` raíz; `README.md`; `docs/operacion/{branch-protection,backup-recovery,outbox-backlog,kafka-down,postgres-down,secret-rotation}.md`; `docs/auditoria-produccion/{baseline,PLAN,promotion-gate,FINAL_REPORT,proveedores,limites-de-recursos}.md`; `ADR-050` | **Pablo** |
| `docs/auditoria-produccion/carriles/PR<n>-*.md`, `baseline-PR<n>-*.md` | Cada uno el suyo |
| `sql/**` (generado), `gradle/libs.versions.toml`, `docs/Arquitectura/_Arquitectura.md`, `docs/Seguridad.md`, `docs/Arquitectura/Entornos y despliegue.md` | Compartido **solo por micro-PR al troncal**: cada uno agrega lo suyo, nadie edita lo ajeno, merge dentro de la hora |
| `servicios/{cumplimiento,entregas,erp,garantia,grupos,notificaciones,organizador,publicidad,tarifas,transparencia}` | **Sin dueño este turno**: solo lectura. Lo que se encuentre roto ahí va a §6 como hallazgo con ruta |
| `main` | **Nadie.** Se recomienda la promoción en `FINAL_REPORT.md`; no se ejecuta |

**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

### Área frontend, bloque B — Pasanaku (`PasanakuBackend`/`PasanakuFrontend`) @ `dev`

| Área / archivos | Reservado para |
|---|---|
| La **pantalla piloto** (se publica abajo) y los componentes privados de esa pantalla | **Richard** |
| El **organismo de tabla** y sus estilos; los **dos consumidores** que migra (se publican abajo) | **Justin** |
| El **tipo de estado** y su documento de contrato; el **host de estados**; el **organismo de diálogo** y sus estilos; los **dos modales** que migra (se publican abajo) | **Leo** |
| El **generador del índice de componentes** y sus artefactos generados; los documentos de inventario, grafo de usos y matriz de familias | **Marcelo** |
| El **runtime del catálogo** y su ficha; la **entrada de preview**; el generador de props sintéticas; la configuración de CI; el documento de cierre del refactor y el registro de ejecución | **Pablo** |
| **Tokens del sistema de diseño** (color, espaciado, radio, tipografía) | **Nadie este turno.** No se toca una variable. Lo que se encuentre mal va a §6 como hallazgo |
| Contratos del **backend** del producto (endpoints, DTO) | **Nadie este turno.** El frontend recibe y representa; no cambia el contrato |
| `main` del repo frontend | **Nadie.** Todo va contra `dev`, después se sincroniza el espejo `PasanakuFrontend` (corrección 2026-09-21, AMB-F5) |

**Se publican acá en la primera hora, antes de escribir código** (AMB-F7). El primero que publica
se queda con el archivo; el otro elige otro y lo anota:

| Qué se reserva | Quién | Archivo / ruta | Publicado |
|---|---|---|---|
| Pantalla piloto | Richard | | |
| Consumidor 1 de la tabla | Justin | | |
| Consumidor 2 de la tabla | Justin | | |
| Modal 1 | Leo | | |
| Modal 2 | Leo | | |

**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

## 5. Ambigüedades abiertas — se arrastran, no se resuelven

| ID | Qué | Quién la cierra | Estado |
|---|---|---|---|
| AMB-R1 | `test` es espejo de `dev` (`git push origin origin/dev:test` tras cada merge) | Pablo | **DECIDIDA (2026-09-21)**: `test` es espejo fast-forward de `dev` (`git push origin origin/dev:test` tras cada merge); el ruleset mínimo `proteccion-minima` (JSON y comando en el daily del equipo §2, lo aplica Pablo con una línea) bloquea force-push y borrado en `dev`, `test` y `main` |
| AMB-2 | Evidencia step-up = JWT corto validado localmente; `jti` consumido en tabla del núcleo | Pablo (arquitectura) | **DECIDIDA (2026-09-21)**: JWT step-up RS256 emitido por `identidad`, validado localmente por `nucleo-financiero` con el JWKS; `jti` consumido una sola vez en `nucleo_financiero.evidencia_mfa_consumida`; contrato ya en `dev`: `docs/auditoria-produccion/contratos/step-up-jwt.md` |
| AMB-3 | Factor real del desafío MFA | Pablo · negocio | **DECIDIDA (2026-09-21)**: el factor real de producción es **TOTP (RFC 6238)** verificado dentro de `identidad` desde `factor_mfa.secreto_cifrado` (tipo `TOTP` ya existe en el CHECK): **sin proveedor externo**; SMS/WhatsApp (`factor_mfa.tipo` `SMS`/`WHATSAPP`) salen por el servicio `notificaciones` como segundo canal, con doble en tres niveles solo en `local/test`. El desafío **reutiliza `token_verificacion`** (`tipo_token='OTP'`, `proposito='MFA_RETIRO'`, `politica_id`, `intentos_fallidos`/`max_intentos`, `uso_unico=true`): sin tabla nueva |
| AMB-4 / AMB-5 | Endpoint/permiso de aprobación; retiro < umbral | Pablo · negocio | **DECIDIDA (2026-09-21)**: `POST /billetera/retiros/{ordenId}/aprobacion` con `desenlace ∈ {AUTORIZADA, RECHAZADA}`; permiso nuevo `RETIRO_APROBAR` asignado al rol **`TESORERIA`** del seed (`sql/60_semillas/10-roles-y-permisos.sql`), nunca a `PARTICIPANTE`/`ORGANIZADOR`. siempre `PENDIENTE → AUTORIZADA → EN_PROCESO → PAGADA`; por debajo del umbral la autorización es automática en la misma transacción de creación (`aprobada_por = NULL`); nunca `PENDIENTE → PAGADA` |
| AMB-6 | Redis para rate limiting distribuido | Pablo (infra) | **DECIDIDA (2026-09-21)**: **Redis entra al stack** (`despliegue/compose/base.yml`, `infra.yml`, Coolify) para `RequestRateLimiter` del gateway; con Redis caído las rutas sensibles deniegan (fail closed); ADR-050 lo registra |
| AMB-7 | Migraciones versionadas (no existen) | Pablo (arquitectura) | **DECIDIDA (2026-09-21)**: este turno sigue con `sql/aplicar.sql` generado (idempotente) y **solo cambios aditivos** al esquema (sin `DROP COLUMN`/`DROP TABLE`/cambio de tipo); se verifica `empty→latest` y `latest→latest` con datos; la adopción de Flyway/Liquibase queda como ADR posterior a la promoción, no se hace ahora |
| AMB-8 | RPO/RTO | Operación | **DECIDIDA (2026-09-21)**: se implementa PITR (base + WAL) y el restore se ejecuta de verdad; el **RPO y el RTO se miden** en ese restore y se reportan como capacidad medida (no como compromiso comercial, que sigue siendo de negocio) |
| AMB-9 | Severidad que bloquea en OSV/Trivy | Pablo | **DECIDIDA (2026-09-21)**: `HIGH` y `CRITICAL` bloquean en OSV y Trivy; `MEDIUM` reporta; toda excepción lleva motivo y fecha de revisión (≤ 30 días) |
| AMB-10 | Consumidor Kafka: solo de prueba | Pablo | **DECIDIDA (2026-09-21)**: consumidor Kafka **de prueba** en `comun-mensajeria/src/e2eTest`; ningún consumidor productivo este turno; contrato del envelope ya en `dev`: `docs/auditoria-produccion/contratos/evento-kafka.md` |
| AMB-12 | Perfiles `local/test/staging/production` | Pablo | **DECIDIDA (2026-09-21)**: perfiles `local`, `test`, `staging`, `production`; `aportaya.entorno.productivo = true` para todo perfil que no sea `local`/`test` (fail closed) |
| Q-Pablo-05 | Aplicar rulesets de protección de ramas | Pablo | **DECIDIDA (2026-09-21)**: durante el turno `dev` **no exige PR ni aprobaciones** (los cinco mergean solos con su gate local); queda **listo** el ruleset mínimo `proteccion-minima` (bloquea force-push y borrado en `dev`, `test` y `main`; el agente no tiene permiso para crearlo, Pablo lo aplica con el comando del daily §2); el ruleset **completo** (PR obligatorio, checks requeridos, CODEOWNERS, 2 aprobaciones en `main`) se activa en la promoción `dev → main` (Pablo H2.S5.M2 lo deja escrito) |

### Las ambigüedades de arriba ya están decididas

Todas las filas de §5 llevan su decisión del 2026-09-21. Los encargos §5 y los dailies §8 dicen lo mismo. Si durante el turno una decisión resulta imposible de aplicar, se registra en §6 del daily personal con la razón y **se sigue con la alternativa declarada**; no se reabre la discusión en el chat.

Los dos contratos entre carriles ya están en `dev` y `test`: `docs/auditoria-produccion/contratos/step-up-jwt.md` (Richard ↔ Justin ↔ Leo) y `docs/auditoria-produccion/contratos/evento-kafka.md` (Leo ↔ todos). Richard H1.S2.M1 y Leo H2.S2.M1 pasan a ser "verificar que está y ajustar solo lo que el código exija".

### Área frontend

| ID | Qué | Quién la cierra | Estado |
|---|---|---|---|
| AMB-F1 | Cada persona queda con dos carriles el mismo turno, y la regla 70.1 permite uno activo por vez | Coordinación | ABIERTA — supuesto aplicado: bloque A (backend) primero, bloque B (frontend) después; **recortar es decisión de coordinación y se registra**, no se borran microtareas |
| AMB-F2 | `mantra-core-health` no es un repo de Pasanaku | Coordinación / cumplimiento | **RESUELTA 2026-09-21 por Pablo, para los cinco carriles del bloque B:** sí es trabajo de Pasanaku; repo, rama y reglas corregidos por carril (ver la nota bajo "Bloque B" y `docs/trabajo/2026-09-21-correccion-*`) |
| AMB-F3 | Las rutas del documento antecedente (runtime del catálogo, generador de props, generador del índice, tipo de estado, tabla, directorio, diálogo) | El baseline de cada uno, primera microtarea | ABIERTA — son **hipótesis heredadas**: ninguna se usa hasta confirmarla con archivo y línea |
| AMB-F4 | El SHA `5a0776c6…` del documento original | — | ABIERTA — referencia histórica, **no una orden de resetear**. La base es `dev` (corrección 2026-09-21; antes decía `mockup`) en el SHA que registre cada uno |
| AMB-F5 | A qué rama se integra el trabajo del frontend | Dueño del repo frontend | **RESUELTA 2026-09-21:** PR contra `dev`, rama real de Pasanaku; `main` no se toca; el espejo `PasanakuFrontend` se sincroniza por fast-forward |
| AMB-F6 | Coexisten Vitest, Playwright y Cypress: cuál es el runner de cada capa | Pablo, en la primera hora (§2-bis) | ABIERTA — se usa el que ya esté cableado; **no se instala nada nuevo** |
| AMB-F7 | Qué pantalla es el piloto y cuáles son los consumidores y modales migrados | Richard, Justin y Leo publican en §4, primera hora | ABIERTA — el primero que publica se queda con el archivo |
| Q-frontend-borrador | Qué debe pasar con un borrador si la entidad cambia mientras se edita | Producto | `DECISION_REQUIRED` — Leo implementa la rama conservadora y la declara; **no se elige una política de negocio en silencio** |

## 6. Cierre del turno — completar acá

### Bloque A — backend

| Persona | HECHO / total | Hitos cerrados | `A MEDIAS` | `BLOQUEADO` | Su daily |
|---|---|---|---|---|---|
| Richard | 0 / 28 | | | | [Richard-Daily-Noche-2026-09-21.md](Backend/Richard/Richard-Daily-Noche-2026-09-21.md) |
| Justin | 0 / 42 | | | | [Justin-Daily-Noche-2026-09-21.md](Backend/Justin/Justin-Daily-Noche-2026-09-21.md) |
| Leo | 0 / 49 | | | | [Leo-Daily-Noche-2026-09-21.md](Backend/Leo/Leo-Daily-Noche-2026-09-21.md) |
| Marcelo | 0 / 40 | | | | [Marcelo-Daily-Noche-2026-09-21.md](Backend/Marcelo/Marcelo-Daily-Noche-2026-09-21.md) |
| Pablo | 0 / 54 | | | H2.S5.M3 (ruleset mínimo: un comando de Pablo, ver §2) | [Pablo-Daily-Noche-2026-09-21.md](Backend/Pablo/Pablo-Daily-Noche-2026-09-21.md) |

### Bloque B — frontend

| Persona | HECHO / total | Hitos cerrados | `A MEDIAS` | `BLOQUEADO` | Su daily |
|---|---|---|---|---|---|
| Richard | 0 / 24 | | | | [Richard-Daily-Noche-2026-09-21.md](Frontend/Richard/Richard-Daily-Noche-2026-09-21.md) |
| Justin | 0 / 27 | | | | [Justin-Daily-Noche-2026-09-21.md](Frontend/Justin/Justin-Daily-Noche-2026-09-21.md) |
| Leo | 0 / 26 | | | | [Leo-Daily-Noche-2026-09-21.md](Frontend/Leo/Leo-Daily-Noche-2026-09-21.md) |
| Marcelo | 0 / 31 | | | | [Marcelo-Daily-Noche-2026-09-21.md](Frontend/Marcelo/Marcelo-Daily-Noche-2026-09-21.md) |
| Pablo | 0 / 38 | | | | [Pablo-Daily-Noche-2026-09-21.md](Frontend/Pablo/Pablo-Daily-Noche-2026-09-21.md) |

### Bloque C — frontend · AportaYa

| Persona | HECHO / total | Hitos cerrados | `A MEDIAS` | `BLOQUEADO` | Su daily |
|---|---|---|---|---|---|
| Richard | 0 / 51 | | | | [Richard-Daily-Noche-2026-09-21.md](Frontend/Richard/Richard-Daily-Noche-2026-09-21.md) |
| Justin | 0 / 36 | | | | [Justin-Daily-Noche-2026-09-21.md](Frontend/Justin/Justin-Daily-Noche-2026-09-21.md) |
| Leo | 0 / 52 | | | | [Leo-Daily-Noche-2026-09-21.md](Frontend/Leo/Leo-Daily-Noche-2026-09-21.md) |
| Marcelo | 0 / 59 | | | | [Marcelo-Daily-Noche-2026-09-21.md](Frontend/Marcelo/Marcelo-Daily-Noche-2026-09-21.md) |
| Pablo | 0 / 58 | | | | [Pablo-Daily-Noche-2026-09-21.md](Frontend/Pablo/Pablo-Daily-Noche-2026-09-21.md) |

> El total del bloque C es **256**. Un `BLOQUEADO` acá solo vale si es una
> decisión de negocio sin tomar o una acción destructiva sobre algo compartido: esperar la entrega
> de otro carril **no** es un bloqueo, se simula el contrato en tres niveles y se cierra contra el
> doble, declarándolo (regla 65).

### Consolidación del área frontend — la completa Pablo (PR10 · H5.S3.M3)

Cada número sale de un conteo, con su **denominador declarado**. Si el denominador cambia, se
explica por qué; achicarlo para que el número quede mejor está prohibido.

| Medida | Valor | Denominador |
|---|---|---|
| Componentes inspeccionados | | total del alcance |
| Consumidores migrados | | comprometidos en §4 |
| Familias verificadas | | detectadas |
| Escenarios del catálogo acreditados | | descubiertos |
| Rutas comprobadas en navegador | | afectadas |

### Qué NO se puede escribir en este documento

- Un `PASS` sin comando y exit code pegados. **Leer el diff no es verificar; compilar no es verificar.**
- «Listo», «funciona» o «implementado» sobre algo que no se ejecutó.
- Un porcentaje que no salga de `HECHO / total`.
- Un `BLOQUEADO` disfrazado de `PASS` porque «igual compila», ni un `BLOQUEADO` por un contrato
  ajeno que se podía simular.
- `READY` en `FINAL_REPORT.md` con un P0 sin evidencia.
- Datos reales de participantes, cuentas bancarias, documentos, OTP o tokens en cualquier salida pegada.
- **En el área frontend, además:** un snapshot actualizado o una tolerancia ampliada para tapar una
  regresión visual; una ficha del catálogo montada vacía para no probar sus contratos; un doble
  presentado como integración terminada; un componente marcado como verificado que solo se
  inspeccionó estáticamente; una ruta del documento antecedente escrita como hecho sin haberla
  confirmado en el código; y datos clínicos o identificatorios reales en fixtures, capturas,
  mensajes entre ventanas o URLs.

## 7. Orden de los bloques y un solo trabajo activo (regla 70.1)

Cada persona tiene **tres** bloques en este turno. **No se trabajan en paralelo.** El orden es
**A (backend) → B (mantra) → C (AportaYa)**, y cada bloque se cierra —o se declara `A MEDIAS` con
las cuatro respuestas: qué anda, qué no anda, qué falta exactamente y dónde quedó— **antes** de
abrir el siguiente. Repartir tres carriles no autoriza a abrirlos juntos.

**615 microtareas repartidas entre cinco personas no entran en un turno, y eso está
declarado a propósito** (README de `repartos/`): el encargo se escribe completo y ordenado por
dependencia aunque sobre. Lo que no se cierre va `A MEDIAS`. **Recortar alcance es decisión de
coordinación y se registra**, no se resuelve marcando `HECHO` lo que no se verificó.

Dentro del bloque C hay un orden propio: **Pablo primero** (su H2 entrega la línea base, los
clientes versionados y los contratos que los otros cuatro necesitan) y **Pablo último** (su H5 es
el cierre, y solo se puede escribir cuando los demás terminaron). Entre medio, los otros cuatro
carriles son independientes entre sí.
