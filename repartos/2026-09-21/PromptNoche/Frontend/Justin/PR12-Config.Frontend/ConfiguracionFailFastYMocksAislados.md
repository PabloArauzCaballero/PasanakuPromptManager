# Producción no muestra cifras inventadas ni llama a la máquina del usuario

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** Justin · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Bloque:** **C — AportaYa** (el bloque B, `PR7-DataTable.Frontend`, **es el mismo repo desde la
  corrección del 2026-09-21**: antes decía `mantra-core-health`, ya es Pasanaku). **Un trabajo
  activo por vez** (regla 70.1): A backend → B tabla de datos → C este.
- **Repo:** el monorepo de AportaYa — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `justin/frontend/config`
- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 · te tocan **H4, H5 y H12.S4**
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md)
- **4 hitos · 7 subtareas · 36 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar dentro del monorepo de AportaYa.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo:**

| Skill | Para qué en este encargo |
|---|---|
| `environment-secrets-config` | Configuración validada al arrancar y servicio que falla si falta o es inválida |
| `frontend-ux-states` | Los cuatro estados obligatorios de toda vista con red, y el vacío que orienta |
| `smart-dumb-components` | Separar el contenedor que trae datos de la pantalla que los dibuja |
| `seed-data-catalogs` | Por qué un dato inventado presentado como real contamina, y cómo se declara lo sintético |
| `synthetic-test-data-generation` | Datos de ejemplo declarados como tales, válidos e inválidos a propósito |
| `angular-testing` | `TestBed` con providers, specs de los adaptadores y de los cuatro estados |
| `e2e-playwright` | Los E2E de `sistemas` sin contrato y de configuración inválida |
| `flutter-testing` | El widget test de la pantalla de configuración inválida en la app |
| `visual-proof` | Capturas del banner de datos de ejemplo y del estado de error, por viewport y tema |
| `frontend-security` | Que la app no mande tráfico a un host que no es el suyo |
| `evidence-and-verification` | El peldaño que podés declarar con la evidencia que tengas |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **90** (configuración y hosts) · **95** (estados obligatorios de la interfaz) · **97.4** (datos de catálogo y su procedencia)

> **Corrección 2026-09-21:** el bloque B (`PR7`) dejó de ser `mantra-core-health`; ahora la regla 91
> le aplica también, condicionada a los dos consumidores que elija. La 98 no le aplica (es frontend
> puro). Acá, en el bloque C, las dos **siempre** aplican.
> Las pantallas que estás tocando muestran estado de servicios que mueven plata.

## 2. Resultado observable

Un operador que abre cualquier pantalla de `sistemas/` en producción ve un error honesto que dice
que la fuente no está disponible, en vez de un `99.95 %` inventado; y ninguna de las tres apps
arranca en producción apuntando a `localhost` o a un host que no es el suyo: falla antes, y lo dice.

**Kill-test:** `yarn workspace @aportaya/backoffice build` y después
`grep -r "99.95" apps/backoffice/dist/backoffice/browser/`. Hoy aparece: los nueve arrays de
`datos-simulados.ts` entran al bundle de producción porque nueve pantallas los importan directo.
Si al cerrar sigue apareciendo, esto NO está hecho. Segundo kill-test: servir el backoffice
compilado sin la etiqueta `<meta aportaya-gateway>`. Hoy cae a `http://localhost:4010/api/v1`
(`gateway.ts:9`), que en el navegador de un operador es **su propia máquina**.

## 3. Alcance

**IN:**
- `apps/backoffice/src/app/nucleo/gateway.ts` y `apps/web/src/app/nucleo/gateway.ts`.
- `apps/backoffice/src/app/rutas/sistemas/**` (las nueve pantallas, sus puertos y adaptadores).
- `packages/simulado/src/backoffice-sistemas/**` y el `exports` de ese package.
- `packages/dominio-cliente/src/configuracion.ts` y su `exports`.
- `apps/movil/lib/dominio/configuracion.dart` y la pantalla de configuración inválida de la app.
- El componente `ConfiguracionInvalida` y el banner de datos de ejemplo.
- E2E nuevos: `apps/backoffice/e2e/{sistemas-sin-contrato,config-invalida}.e2e.ts`.

**OUT:** `nucleo/sesion*`, `permisos.ts`, `registro-de-acceso*` y `app.config.ts` (son de Richard:
vos entregás los providers, él los cablea), `.github/workflows/**` y `apps/movil/lib/infraestructura/**`
(Leo), `packages/{ui,tutoriales,tokens}` y `eslint.config.js` y `server.ts` (Marcelo), `clientes/**`
(Pablo). Tampoco tocás `servicios/**` ni inventás el contrato de observabilidad que falta: se
declara como brecha.

**Reservas de archivos:** las siete rutas del IN son tuyas. `app.config.ts` **no** es tuyo: dejás
`provideFuentesDeSistemas()` y `provideGateway()` exportados y probados con `TestBed`, y el
cableado es microtarea de Richard.

## 4. Plan

### H1 — La línea base de tu carril es un hecho registrado

**CA:** Dado el SHA de arranque, cuando alguien lee tu daily, entonces sabe qué compila hoy, qué contiene el bundle de producción y qué pasa sin la etiqueta de gateway, sin haberlo corrido él.
**DoD:** las cuatro salidas pegadas en `evidencia/` con su `exit=`.
**Estado:** TODO

#### H1.S1 — Entorno, SHA y el bundle tal como está hoy

**CA:** Dado tu clon, cuando construís el backoffice y buscás los datos simulados en el bundle, entonces el resultado queda registrado tal cual es, sin corregir nada.
**DoD:** `evidencia/H1-S1-*.txt` con las salidas literales.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar el SHA de arranque y crear `justin/frontend/config` desde `dev` | La rama existe sobre el SHA declarado | `git rev-parse HEAD` pegado en el daily; `git branch --show-current` → `justin/frontend/config` | TODO |
| H1.S1.M2 | Instalar el estándar y verificarlo (sección 1) | Las dos salidas pegadas en el daily | `python .claude/hooks/plan_gate.py --self-test; echo exit=$?` → `0` | TODO |
| H1.S1.M3 | Construir el backoffice y buscar los datos simulados en el bundle (el kill-test, antes de tocar nada) | El conteo actual queda registrado | `yarn workspace @aportaya/backoffice build && grep -rc "99.95" apps/backoffice/dist/backoffice/browser/` → pegado | TODO |
| H1.S1.M4 | Listar las nueve pantallas que importan `datos-simulados` y con qué símbolo | Tabla pantalla → símbolos importados | `grep -rn "datos-simulados" apps/backoffice/src --include=*.ts` → tabla en `evidencia/H1-S1-M4.txt` | TODO |

### H2 — Producción no puede mostrar un número inventado (madre H4)

**CA:** Dado un build de producción del backoffice, cuando un operador abre cualquier pantalla de `sistemas/`, entonces ve un estado de error accionable que dice que la fuente no está disponible y **nunca** los valores de ejemplo; en modo demo ve los mismos datos con un banner persistente que dice que son de ejemplo.
**DoD:** el bundle de producción sin los strings de los mocks; specs de los cuatro estados en las nueve pantallas; E2E `sistemas-sin-contrato` PASS; capturas inspeccionadas.
**Estado:** TODO

#### H2.S1 — Un puerto por fuente, y el simulado afuera

**CA:** Dada cada pantalla de `sistemas/`, cuando pide datos, entonces lo hace a un puerto inyectado, y la implementación de ejemplo vive en el package de simulado con tipos marcados como tales, no en el dominio de la ruta.
**DoD:** `grep` de `datos-simulados` en `apps/backoffice/src` → 0 fuera de tests; `yarn typecheck` verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | (madre H4.S1.M1) Definir los nueve puertos en `rutas/sistemas/dominio/puertos.ts` con el patrón de datos que ya usa la pantalla de saldo | Los nueve tokens exportados y tipados | `yarn workspace @aportaya/backoffice typecheck` → 0 errores | TODO |
| H2.S1.M2 | (madre H4.S1.M2) Mover los arrays de ejemplo a `packages/simulado/src/backoffice-sistemas/` con los tipos renombrados, dejando en el dominio solo las dos funciones puras y su spec | El spec de las funciones puras sigue verde y el package exporta la nueva entrada | `yarn workspace @aportaya/simulado test:front` → passed · `grep -c "Simulados" apps/backoffice/src/app/rutas/sistemas/dominio/*.ts` → 0 | TODO |
| H2.S1.M3 | (madre H4.S1.M3) Adaptador de fuente simulada que implementa los nueve puertos con un retardo determinista | Spec: emite los datos y nunca falla | spec → PASS | TODO |
| H2.S1.M4 | (madre H4.S1.M4) Adaptador de fuente no disponible que devuelve un error de dominio para los nueve puertos | Spec: cada puerto emite el error tipado | spec → PASS | TODO |
| H2.S1.M5 | (madre H4.S1.M5) Reescribir las nueve pantallas para inyectar su puerto y resolver los cuatro estados con los componentes que ya existen | Cada pantalla tiene spec de sus cuatro estados | `…test:front --include='src/app/rutas/sistemas/**/*.spec.ts'` → 36 passed o más | TODO |

#### H2.S2 — La bandera de entorno y el bloqueo en producción

**CA:** Dado un build de producción, cuando se resuelven los puertos, entonces se obtiene la fuente no disponible; en demo se obtiene la simulada y el shell muestra el banner.
**DoD:** spec del proveedor en los dos modos; el bundle de producción sin los strings de los mocks; banner con spec de accesibilidad.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | (madre H4.S2.M1) `provideFuentesDeSistemas()` que elige el adaptador por modo explícito, no solo por `isDevMode()` | En producción sin modo demo → fuente no disponible | spec → PASS | TODO |
| H2.S2.M2 | (madre H4.S2.M2) Importar la fuente simulada solo por import dinámico en la rama no productiva | Cero coincidencias de los mocks en el bundle de producción | `yarn workspace @aportaya/backoffice build && grep -rc "99.95" apps/backoffice/dist/backoffice/browser/` → 0 | TODO |
| H2.S2.M3 | (madre H4.S2.M3) Banner de datos de ejemplo en el shell, visible en las nueve pantallas, solo con fuente simulada | Spec de accesibilidad sin violaciones y no se renderiza con la fuente no disponible | `…test:a11y --include='**/banner-datos-de-ejemplo.a11y.spec.ts'` → 0 violations | TODO |
| H2.S2.M4 | (madre H4.S2.M4) Test de arquitectura que falla si una pantalla de `sistemas/` importa del package de simulado | Cero imports detectados | spec `sin-simulado-en-pantallas.spec.ts` → PASS | TODO |
| H2.S2.M5 | (madre H4.S2.M5) Prueba visual: pantalla de servicios en error (producción) y con banner (demo), tres viewports y dos temas | Doce capturas **miradas**: el banner no tapa la navegación | `ls evidencia/H2-S2-M5-*.png` → 12 + la nota de qué viste | TODO |
| H2.S2.M6 | (madre H4.S2.M6) E2E `sistemas-sin-contrato.e2e.ts`: sin modo demo, las nueve rutas muestran el error accionable | Nueve aserciones sobre el rol de alerta | `test:e2e sistemas-sin-contrato` → passed | TODO |
| H2.S2.M7 | (madre H4.S2.M7) Escribir `entregables/brecha-observabilidad.md`: los nueve recursos con la forma que hoy espera la interfaz, marcados como **propuesta**, no como contrato | Nueve subsecciones y la nota de que no existe en ningún contrato | `grep -c "^### " entregables/brecha-observabilidad.md` → ≥ 9 | TODO |
| H2.S2.M8 | (madre H4.S2.M8) Registrar el hallazgo de los mocks como corregido y commitear `fix(security): datos simulados fuera del bundle de producción` | La entrada con evidencia, causa raíz, corrección y pruebas | `git log --oneline -1` → el commit | TODO |

### H3 — Ninguna app arranca en producción contra la máquina del usuario (madre H5)

**CA:** Dado un despliegue de producción, cuando falta la URL del gateway, no es del propio origen (web y backoffice) o su host no está en la lista compilada (app), entonces la app web no arranca y muestra "configuración inválida" sin hacer ninguna petición, el servidor de render sale con código 1, y el build de release de la app falla.
**DoD:** la matriz de casos válidos, límite e inválidos en verde en TypeScript y en Dart; los tres comandos de verificación con su código de salida pegado.
**Estado:** TODO

#### H3.S1 — La función que decide, pura y compartida

**CA:** Dada una URL y el modo, cuando se la valida, entonces devuelve el resultado o el motivo del rechazo, sin efectos y sin depender del framework.
**DoD:** catorce casos en verde en `@aportaya/dominio-cliente`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | (madre H5.S1.M1) `validarConfiguracion(url, {modo, origenPropio, hostsPermitidos})` con las reglas de D-A6: ruta relativa o mismo origen en producción, nunca `localhost` ni `127.0.0.1`, y la ruta versionada al final | Los casos válidos pasan: ruta relativa en producción, mismo origen con TLS, y el simulado solo en desarrollo | `yarn workspace @aportaya/dominio-cliente test:front` → casos válidos passed | TODO |
| H3.S1.M2 | (madre H5.S1.M2) Casos límite: puerto, barra final, mayúsculas en el host, origen propio con puerto, lista con espacios | Normaliza y decide igual en todos | spec → passed | TODO |
| H3.S1.M3 | (madre H5.S1.M3) Casos inválidos: vacío, esquema no soportado, sin TLS en producción, host ajeno, sin la ruta versionada, esquema de script, y la forma `//otro-host/...` | Cada uno rechazado con un motivo distinto y sin lanzar | spec → passed | TODO |
| H3.S1.M4 | (madre H5.S1.M4) Exportar la entrada `./configuracion` en el package (export explícito, no comodín) | Las dos apps la importan y compilan | `yarn typecheck` → 0 errores | TODO |

#### H3.S2 — Backoffice y sitio: arrancar o decir que no

**CA:** Dado el arranque de la app, cuando la configuración es inválida para el modo detectado, entonces se muestra la pantalla de configuración inválida sin revelar la URL y sin hacer ninguna petición.
**DoD:** specs; build de producción sin la etiqueta → pantalla de error con captura; el servidor de render sale con 1.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | (madre H5.S2.M1) Reescribir el `gateway.ts` del backoffice: lee las dos etiquetas y devuelve vacío en producción si falta, **nunca** `localhost` | Sin etiqueta y en modo producción devuelve vacío | spec → PASS | TODO |
| H3.S2.M2 | (madre H5.S2.M2) Ídem el del sitio, con la variable de entorno en el servidor y la etiqueta en el navegador, dando el mismo resultado en los dos lados | Spec con plataforma servidor y navegador → mismo valor | spec → PASS | TODO |
| H3.S2.M3 | (madre H5.S2.M3) Componente `ConfiguracionInvalida` con mensaje accionable para operaciones y sin mostrar la URL | Spec de accesibilidad sin violaciones | `…test:a11y` → 0 violations | TODO |
| H3.S2.M4 | (madre H5.S2.M4) Entregar `provideGateway(modo)` probado con `TestBed` y dejar en `entregables/` la línea exacta que Richard tiene que poner en `app.config.ts` | El provider pasa sus specs sin tocar `app.config.ts` | spec → PASS · `entregables/cableado-app-config.md` con la línea | TODO |
| H3.S2.M5 | (madre H5.S2.M4) E2E `config-invalida.e2e.ts`: build de producción servido sin la etiqueta → pantalla visible y cero peticiones a la API | El contador de peticiones a la API queda en 0 | `test:e2e config-invalida` → passed | TODO |
| H3.S2.M6 | (madre H5.S2.M5) El servidor de render valida su variable al arrancar y **sale con 1** en producción si es inválida | Arranque sin la variable en modo producción → código 1 con mensaje | `echo $?` → `1` pegado en `evidencia/` | TODO |
| H3.S2.M7 | (madre H5.S2.M6) Prueba visual de la pantalla de configuración inválida en tres viewports y dos temas | Seis capturas **miradas** | `ls evidencia/H3-S2-M7-*.png` → 6 + la nota | TODO |

#### H3.S3 — La app: sin defines, no hay release

**CA:** Dado un build de release de la app, cuando faltan los defines de API o el host no está en la lista compilada, entonces el build falla o la app aborta antes de crear el cliente HTTP; en depuración sigue el atajo al simulado, explícito.
**DoD:** la matriz en Dart en verde y los dos códigos de salida del build pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | (madre H5.S3.M1) `validarGateway(url, {release, hostsPermitidos})` pura en la app, con la misma matriz | Catorce casos, incluida la lista vacía en release → inválido | `flutter test test/unidad/configuracion_test.dart` → passed | TODO |
| H3.S3.M2 | (madre H5.S3.M2) La base del cliente deja de tener valor por omisión en release; si es inválida se muestra la pantalla de bloqueo y no se crea el cliente | Widget test: con URL inválida se renderiza la pantalla y no hay cliente | `flutter test test/widget/configuracion_invalida_test.dart` → passed | TODO |
| H3.S3.M3 | (madre H5.S3.M3) Verificación de build: sin defines falla, con los dos defines correctos sale 0, y con la URL fuera de la lista falla | Los tres códigos de salida pegados | `evidencia/H3-S3-M3.txt` con los tres `exit=` | TODO |
| H3.S3.M4 | (madre H5.S3.M4) Documentar en `entregables/defines-por-plataforma.md` los defines obligatorios por plataforma y modo, incluido el atajo del emulador | Tabla plataforma × modo × valor | `grep -c "10.0.2.2" entregables/defines-por-plataforma.md` → ≥ 1 | TODO |
| H3.S3.M5 | (madre H5.S3.M5) Registrar el hallazgo del atajo a `localhost` en las tres apps como corregido y commitear `fix(config): configuración del gateway fail-fast en web, backoffice y app` | La entrada nombra los tres archivos | `git log --oneline -1` → el commit | TODO |

### H4 — Ninguna pantalla con red confunde "vacío" con "roto" (madre H12.S4)

**CA:** Dada cada pantalla que depende de una llamada de red, cuando la API devuelve datos, vacío, error o sin permiso, entonces se muestra el estado que corresponde, distinguible de los otros y accionable.
**DoD:** el inventario completo de pantallas con sus estados marcados, y cada estado faltante corregido con su spec, agregado al plan como microtarea nueva antes de tocarlo.
**Estado:** TODO

#### H4.S1 — El inventario que no miente

**CA:** Dado el inventario, cuando se lee, entonces cada pantalla con red tiene marcados sus estados resueltos y sus faltantes, sin "probablemente".
**DoD:** la tabla con tantas filas como pantallas con red haya.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | (madre H12.S4.M1) Inventariar cada pantalla del backoffice con red y marcar cargando, datos, vacío, error, sin permiso y sin conexión | La tabla tiene una fila por pantalla con red, sin celdas vacías | `find apps/backoffice/src -name 'pantalla-*.ts' \| wc -l` = filas de `entregables/inventario-estados.md` | TODO |
| H4.S1.M2 | (madre H12.S4.M2) Por cada estado faltante, agregar la microtarea al plan **antes** de tocar la pantalla, con su criterio en dado/cuando/entonces | Ninguna pantalla se toca sin su fila previa en el plan | `python .claude/hooks/plan_status.py` refleja el total actualizado | TODO |
| H4.S1.M3 | (madre H12.S4.M3) Verificar que la app distingue sin conexión de error del servidor; si no lo hace, spec de widget que lo demuestre | La distinción queda probada o registrada como faltante | `flutter test test/widget/estado_offline_test.dart` → passed | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-J1 | ¿Cuál es el origen propio real en producción y cómo llega la etiqueta de gateway al HTML del backoffice? | Leo (dueño del despliegue) y Pablo (descubrimiento H0.S3) | El caso "mismo origen" de H3.S1 | Same-origin: ruta relativa versionada, que es lo que ya inyecta el servidor del sitio. Si el backoffice se sirve desde otro host, es hallazgo y se registra |
| Q-J2 | ¿Existe o existirá un contrato de observabilidad para las nueve pantallas de `sistemas/`? | Negocio y el dueño de un futuro servicio de plataforma | Reemplazar los adaptadores de ejemplo por reales | No existe. Se escribe la propuesta en `entregables/brecha-observabilidad.md` y **no** se inventa el endpoint |
| Q-J3 | ¿Qué significa "modo demo" operativamente: una etiqueta en el HTML, una variable de build, o un rol? | Coordinación | La forma exacta de la bandera de H2.S2.M1 | Etiqueta explícita en el HTML más variable de entorno; nunca solo `isDevMode()`, porque eso deja la decisión en el compilador |
| Q-J4 | ¿Los valores de `API` y la lista de hosts en el despliegue quién los carga? | Leo (infra) | El build de release de la app | Los carga infra en el despliegue; vos entregás la tabla de defines y el build falla por diseño si faltan |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` del trabajo escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin URLs con datos de personas y sin secretos
      (regla 90.2: si una salida los tenía, se enmascara **y se aclara que se enmascaró**).
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `visual-proof` por el banner y
      los estados de error; `seed-data-catalogs` porque tocás datos presentados como reales;
      `security-guardrails` porque decidís a qué host sale el tráfico.
- [ ] Peldaño de evidencia declarado por área (regla 30).
- [ ] Ningún dato de ejemplo queda en el bundle de producción, y ningún fallback silencioso
      reemplaza un error real por una cifra inventada.
