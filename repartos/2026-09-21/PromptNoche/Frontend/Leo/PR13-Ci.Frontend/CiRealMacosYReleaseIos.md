# El CI deja de mentir: E2E del backoffice, dos jobs macOS, release iOS de verdad y cero `|| true`

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** Leo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Bloque:** **C — AportaYa** (el bloque B, `PR8-DialogoYEstados.Frontend`, **es el mismo repo
  desde la corrección del 2026-09-21**: antes decía `mantra-core-health`, ya es Pasanaku). **Un
  trabajo activo por vez** (regla 70.1): A backend → B diálogo/estados → C este.
- **Repo:** el monorepo de AportaYa — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `leo/frontend/ci`
- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 · te tocan **H6, H7 y H8**, más el paso de clientes de H0.S1.M9
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md)
- **5 hitos · 12 subtareas · 52 microtareas**

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
| `github-actions-ci` | Los jobs, sus dependencias, los artefactos y cómo no esconder un fallo |
| `ci-cd-pipeline` | El orden de las etapas y qué bloquea el avance |
| `code-quality-gates` | Escaneo de secretos y dependencias como etapas obligatorias |
| `mobile-release-security` | Firma, distribución y qué no puede viajar en un build de release |
| `flutter-testing` | Pruebas de capability con plataforma forzada y el simulador iOS |
| `e2e-playwright` | El servidor de pruebas del backoffice y la vigilancia de consola y red |
| `server-hardening` | Las cabeceras del HTML servido y qué protege cada una |
| `frontend-security` | La política de contenido que no rompe la app y qué deuda deja |
| `dependency-management` | Triage de advisories: parche dentro del major o motivo escrito |
| `github-branch-protection-rulesets` | Los checks requeridos y por qué el plan del repo los limita |
| `regression-suite-management` | Cuarentena con dueño y fecha, nunca abandono |
| `evidence-and-verification` | El peldaño que podés declarar con la evidencia que tengas |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **70** (un build, una suite, un navegador por vez) · **80.5** (prohibiciones sobre tests) · **90.3** (secretos y configuración) · **90.4** (cadena de suministro)

> **Corrección 2026-09-21:** el bloque B (`PR8`) dejó de ser `mantra-core-health`; ahora la regla 91
> le aplica también, condicionada a los dos modales que elija (ver la nota de reglas de `PR8`). La
> 98 no le aplica (es frontend puro). Acá, en el bloque C, las dos **siempre** aplican.
> El CI que estás arreglando es el que deja pasar, o no, cambios que tocan dinero.

## 2. Resultado observable

Quien mira una corrida del CI ve lo que realmente se ejecutó: los E2E del backoffice corren, las
goldens y las pruebas de integración de la app corren en macOS, sale un IPA de release en cada
corrida, y una colección de humo rota **hace fallar** el comando en vez de salir con éxito.

**Kill-test:** romper a propósito una colección de humo obligatoria y correr `yarn humo`. Hoy sale
código 0 siempre, porque `package.json:21` termina cada iteración con `|| true`. Si al cerrar sigue
saliendo 0, esto NO está hecho. Segundo kill-test: buscar el paso de E2E del backoffice en el job
`frontend`. Hoy no existe: el paso `f5` corre solo los del sitio, y
`apps/backoffice/playwright.config.ts:17` dice que el servidor "se levanta a mano".

## 3. Alcance

**IN:**
- `.github/workflows/ci.yml` (sos el dueño único del archivo en este turno), `.github/CODEOWNERS`,
  `.github/dependabot.yml`.
- `package.json` de la raíz (el script de humo) y `scripts/humo.mjs`.
- `apps/movil/lib/infraestructura/**` (los siete puertos y sus adaptadores por plataforma),
  `apps/movil/ios/**`, `apps/movil/pubspec.yaml`, `apps/movil/package.json`.
- `apps/backoffice/playwright.config.ts` y `apps/web/playwright.config.ts`.
- `despliegue/nginx/**` y la configuración del servidor que emite las cabeceras del backoffice.

**OUT:** `apps/backoffice/src/app/nucleo/**` y `app.config.ts` (Richard), `gateway.ts` y
`rutas/sistemas/**` (Justin), `packages/**`, `eslint.config.js`, `server.ts` y `tsconfig.base.json`
(Marcelo), `clientes/**`, `.gitignore` y `docs/auditoria/**` (Pablo). Tampoco tocás `servicios/**`
ni el job `codigo` del CI, que es del área backend.

**Reservas de archivos:** las seis rutas del IN son tuyas. Sos el **único** que edita
`.github/workflows/ci.yml`: los demás carriles te dejan el comando exacto en sus `entregables/` y
vos lo cableás como microtarea tuya.

## 4. Plan

### H1 — La línea base de tu carril es un hecho registrado

**CA:** Dado el SHA de arranque, cuando alguien lee tu daily, entonces sabe qué jobs del CI corren hoy, cuáles quedan salteados y con qué salida, sin haber tenido que abrir GitHub.
**DoD:** las cuatro salidas pegadas en `evidencia/` con su `exit=`.
**Estado:** TODO

#### H1.S1 — Entorno, SHA y el CI tal como está hoy

**CA:** Dado el repositorio, cuando consultás la última corrida y corrés el humo, entonces el resultado queda registrado tal cual es, sin corregir nada.
**DoD:** `evidencia/H1-S1-*.txt` con las salidas literales.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar el SHA de arranque y crear `leo/frontend/ci` desde `dev` | La rama existe sobre el SHA declarado | `git rev-parse HEAD` pegado en el daily; `git branch --show-current` → `leo/frontend/ci` | TODO |
| H1.S1.M2 | Instalar el estándar y verificarlo (sección 1) | Las dos salidas pegadas en el daily | `python .claude/hooks/plan_gate.py --self-test; echo exit=$?` → `0` | TODO |
| H1.S1.M3 | Registrar el estado real de la última corrida del CI: qué job falla y cuáles quedan salteados | La lista de jobs con su conclusión queda pegada | `gh run list --limit 3` y `gh run view <id> --json jobs` → `evidencia/H1-S1-M3.txt` | TODO |
| H1.S1.M4 | Correr `yarn humo` tal como está y registrar su código de salida (el kill-test, antes de tocar nada) | El código de salida queda registrado | `yarn humo; echo exit=$?` → pegado | TODO |

### H2 — Ninguna capability de iOS finge soporte (madre H6.S1 y H6.S2)

**CA:** Dado un dispositivo iOS, cuando la app consulta sus capacidades, entonces cada uno de los siete puertos declara si está soportado, no soportado o degradado según la plataforma real, y las funciones cuyo puerto no está soportado quedan deshabilitadas con su explicación, en vez de llamar a un canal nativo que no existe.
**DoD:** las pruebas de capability con plataforma forzada en verde para iOS y Android; `dart analyze --fatal-infos` limpio; ninguna instanciación de adaptador iOS abre un canal nativo.
**Estado:** TODO

#### H2.S1 — Detectar, no suponer

**CA:** Dado un puerto que hoy cae en el adaptador de Android bajo iOS, cuando se lo pide en iOS, entonces se obtiene un adaptador que declara que no está soportado y devuelve el valor seguro, nunca el canal de Android.
**DoD:** catorce casos (siete puertos por dos plataformas) en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | (madre H6.S1.M1) Agregar el grado de soporte a los siete puertos, con los adaptadores de Android declarando soporte pleno | `dart analyze --fatal-infos` sin observaciones | comando → 0 issues | TODO |
| H2.S1.M2 | (madre H6.S1.M2) Adaptadores explícitos de "no soportado en iOS" para conectividad, biometría, avisos y protección de pantalla | Ninguno abre un canal nativo al instanciarse | test con mensajería de prueba que falla ante cualquier canal → passed | TODO |
| H2.S1.M3 | (madre H6.S1.M3) La resolución por plataforma elige esos adaptadores bajo iOS | Con plataforma forzada iOS salen los tipos no soportados; con Android, los de Android | `flutter test test/unidad/capacidades_test.dart` → 14 passed | TODO |
| H2.S1.M4 | (madre H6.S1.M4) Evaluar si el plugin de conectividad ya instalado es multiplataforma real y, si lo es, dejar un solo adaptador soportado en ambas | La decisión cita la documentación de la versión instalada | `entregables/decision-conectividad.md` con la cita y la versión | TODO |
| H2.S1.M5 | (madre H6.S1.M5) Biometría: solo si ya existe una dependencia que la resuelva en iOS; si no, queda no soportada y se anota como deuda | No se agrega una dependencia sin justificarla (regla 90.4.2) | `grep -n "local_auth" apps/movil/pubspec.yaml` → resultado citado en la decisión | TODO |

#### H2.S2 — La interfaz lo dice y el arranque lo protege

**CA:** Dado un puerto no soportado, cuando se abre la pantalla que lo usa, entonces la acción aparece deshabilitada con su motivo; y en un release de iOS donde una capability crítica de seguridad no está soportada, la app no arranca.
**DoD:** widget tests con plataforma forzada en verde; el ADR de "Android primero" enmendado con la tabla.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | (madre H6.S2.M1) Exponer el mapa de capacidades como proveedor consultable | En iOS devuelve los no soportados que correspondan | `flutter test test/unidad/capacidades_test.dart` → passed | TODO |
| H2.S2.M2 | (madre H6.S2.M2) Las pantallas que usan biometría, avisos o protección deshabilitan la acción con su motivo accesible | Widget test con plataforma iOS: el botón está deshabilitado y el motivo es legible por lector | `flutter test test/widget/capacidades_ui_test.dart` → passed | TODO |
| H2.S2.M3 | (madre H6.S2.M3) En release de iOS, si el almacén seguro o la protección de pantalla no están soportados, se muestra la pantalla de bloqueo y no se crea el cliente HTTP | Widget test con plataforma forzada → pantalla de bloqueo | `flutter test test/widget/bloqueo_plataforma_test.dart` → passed | TODO |
| H2.S2.M4 | (madre H6.S2.M4) Actualizar el comentario del archivo de plataforma y enmendar el ADR de "Android primero" con la tabla puerto × plataforma × soporte | La tabla está en el ADR | `grep -c "UNSUPPORTED" "docs/Arquitectura/ADR-036"*` → ≥ 1 | TODO |
| H2.S2.M5 | (madre H6.S2.M5) Registrar el hallazgo de iOS como corregido, con la nota de qué falta verificar en dispositivo físico, y commitear `fix(mobile): capabilities iOS declaradas, sin fallback Android` | La entrada distingue lo corregido de lo pendiente de dispositivo | `git log --oneline -1` → el commit | TODO |

### H3 — Hay release de iOS en macOS, sí o sí (madre H6.S3, decisión D-A5)

**CA:** Dado un push a la rama de trabajo, cuando corre el CI, entonces un job en macOS ejecuta el gate de capabilities y las pruebas en simulador iOS, construye el IPA de release con los defines de configuración y lo publica como artefacto; si existen los secretos de firma lo firma y lo sube, y si no existen el paso queda declaradamente salteado sin fingir que subió.
**DoD:** la corrida con el job en verde y el artefacto listado; el gate demostrado en rojo con una capability crítica rota y restaurado después.
**Estado:** TODO

#### H3.S1 — El job que compila, prueba y entrega

**CA:** Dado el job de release, cuando una capability crítica no está soportada, entonces falla **antes** de compilar y no produce IPA.
**DoD:** las dos corridas (roja y verde) pegadas con su identificador.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | (madre H6.S3.M1) Crear el job de release iOS en macOS con la misma versión de Flutter del CI y el paso de gate de capabilities antes de compilar | El gate corre antes que cualquier paso de compilación | `gh run view <id> --log` → el paso de gate aparece antes del de build | TODO |
| H3.S1.M2 | (madre H6.S3.M2) Paso de simulador: arrancar un iPhone y correr las pruebas de integración de enlace profundo y doble envío | Las pruebas pasan en simulador iOS | `gh run view --log` → el paso con su conteo de pruebas | TODO |
| H3.S1.M3 | (madre H6.S3.M3) Paso de IPA: build de release con el número de corrida y los defines tomados de variables del repositorio, más la publicación del artefacto | El artefacto aparece en cada corrida | `gh run view <id> --json artifacts` → contiene el IPA | TODO |
| H3.S1.M4 | (madre H6.S3.M4) Firma y subida condicionadas a que existan los secretos; sin ellos, mensaje explícito y paso salteado | Nunca finge una subida | Sin secretos: `gh run view --log` → el paso salteado con su mensaje · `entregables/secretos-ios.md` lista los cinco y quién los carga | TODO |
| H3.S1.M5 | (madre H6.S3.M5) Kill-test del gate: forzar temporalmente que una capability crítica no esté soportada y comprobar que el job falla sin producir IPA; revertir | Rojo demostrado y verde posterior | `evidencia/H3-S1-M5.txt` con las dos corridas | TODO |
| H3.S1.M6 | (madre H6.S3.M6) Escribir en `entregables/` qué cubre el simulador y qué solo cubre un dispositivo físico, con la tabla capability × simulador × dispositivo | La tabla distingue los tres casos | `grep -c "dispositivo" entregables/ios-simulador-vs-dispositivo.md` → ≥ 1 | TODO |

### H4 — Una verificación obligatoria que falla, falla (madre H7)

**CA:** Dado el comando de humo, cuando una colección obligatoria falla, entonces termina con código distinto de cero y nombra la colección; las informativas avisan sin bloquear; y no queda en los gates obligatorios del frontend ningún patrón que convierta un fallo en éxito.
**DoD:** los dos escenarios del humo con su código de salida pegado; el barrido de patrones de test falso en cero o con justificación escrita al lado.
**Estado:** TODO

#### H4.S1 — El humo honesto

**CA:** Dada una colección obligatoria rota, cuando corre el humo, entonces el código de salida es 1 y el nombre de la colección aparece en la salida.
**DoD:** las dos corridas pegadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | (madre H7.S1.M1) Reemplazar el bucle con `\|\| true` por un script que separe colecciones obligatorias de informativas y devuelva el código correcto | Con una obligatoria rota sale 1 y la nombra; con todas sanas sale 0 | `yarn humo; echo exit=$?` en los dos escenarios → `1` y `0` pegados | TODO |
| H4.S1.M2 | (madre H7.S1.M2) Test del script con los tres niveles: todas bien, una informativa falla, una obligatoria falla | Tres casos en verde | `yarn vitest run scripts/humo.spec.mjs` → 3 passed | TODO |
| H4.S1.M3 | (madre H7.S1.M3) Alinear la invocación del humo en el CI con el código de salida del script, sin envolturas que lo anulen | La línea del CI usa el código del script | `grep -n "yarn humo" .github/workflows/ci.yml` → sin `\|\| true` | TODO |

#### H4.S2 — Ningún test que pase por no hacer nada

**CA:** Dado el árbol de pruebas del frontend, cuando se buscan patrones de test falso, entonces no queda ninguno sin una justificación escrita al lado con dueño.
**DoD:** el barrido en cero y las suites en verde después de los cambios.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | (madre H7.S2.M1) Inventariar aserciones vacías, tests exclusivos o salteados, esperas por tiempo fijo y capturas de error vacías en `apps/` y `packages/` | Tabla archivo:línea → clase → acción | el barrido → `evidencia/H4-S2-M1.txt` | TODO |
| H4.S2.M2 | (madre H7.S2.M2) Corregir cada hallazgo sin debilitar el requisito: espera por condición en vez de por tiempo, quitar exclusivos, dueño y fecha a toda cuarentena | El barrido vuelve a cero o cada resto tiene su justificación al lado | mismo barrido → 0 | TODO |
| H4.S2.M3 | (madre H7.S2.M3) El script de pruebas de punta a punta de la app deja de ser un mensaje de consola y pasa a ser el comando real, que falla sin simulador | El script no simula éxito | `yarn workspace @aportaya/movil test:e2e; echo $?` → distinto de 0 sin simulador, con mensaje claro | TODO |
| H4.S2.M4 | (madre H7.S2.M4) Registrar el hallazgo del humo como corregido y commitear `fix(ci): las verificaciones obligatorias del frontend ya no pueden pasar en falso` | La entrada con evidencia y pruebas | `git log --oneline -1` → el commit | TODO |

### H5 — El CI refleja la realidad y el HTML sale endurecido (madre H8)

**CA:** Dado un push a la rama de trabajo, cuando corre el CI, entonces web y backoffice pasan lint, tipos, unidad, accesibilidad, build **y pruebas de punta a punta** cada una; la app pasa formato, análisis, unidad, widget, contrato y accesibilidad, con goldens e integración en macOS; cada package tiene sus tareas reales; y el HTML del backoffice responde con sus cabeceras de seguridad.
**DoD:** la corrida con todos los jobs en verde y la lista de cabeceras pegada.
**Estado:** TODO

#### H5.S1 — Las pruebas de punta a punta del backoffice corren en el CI

**CA:** Dado el job del frontend, cuando llega al paso de punta a punta, entonces levanta el simulado y el servidor del backoffice por configuración, no a mano, y corre los escenarios con un solo trabajador.
**DoD:** el paso en verde en la corrida, con el reporte publicado si falla.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | (madre H8.S1.M1) Configurar el servidor de pruebas del backoffice igual que el del sitio, sin reutilizar procesos en el CI | En local levanta y baja los dos procesos; en CI nunca reutiliza | `yarn workspace @aportaya/backoffice test:e2e; echo $?` → 0 · sin procesos escuchando después | TODO |
| H5.S1.M2 | (madre H8.S1.M2) Sesión de operador para los escenarios: una utilidad que autentica contra el simulado en vez de inyectar el token a mano | Los escenarios existentes y los nuevos la usan | `grep -c "sesionDeOperador" apps/backoffice/e2e/*.ts` → ≥ 6 | TODO |
| H5.S1.M3 | (madre H8.S1.M3) Paso nuevo en el job del frontend con la instalación del navegador, la corrida y la publicación del reporte ante fallo | El paso existe y depende del build | `gh run view <id> --log` → el paso con su marca de éxito | TODO |
| H5.S1.M4 | (madre H8.S1.M4) Los escenarios fallan ante un error de consola o una respuesta inesperada del servidor | Un error provocado hace fallar el escenario; se retira después | `evidencia/H5-S1-M4.txt` con el fallo provocado y el verde posterior | TODO |

#### H5.S2 — La app en el CI, y los dos jobs de macOS (D-A4)

**CA:** Dado el job del frontend, cuando corre la etapa de la app, entonces formato, análisis y las cinco carpetas de pruebas tienen cada uno su paso con su propio resultado; y las goldens y las pruebas de integración corren en jobs de macOS propios.
**DoD:** los pasos y los dos jobs visibles y verdes en la corrida.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S2.M1 | (madre H8.S2.M1) Separar los pasos de la app con nombre propio en vez de embeberlos en la tarea general | Cada paso informa su propio resultado | `gh run view --log` → cuatro pasos listados | TODO |
| H5.S2.M2 | (madre H8.S2.M2) Job de goldens en macOS en cada push, con la línea base actual; actualizar el comentario del orquestador, que hoy dice que no corren | Una golden alterada a propósito lo pone en rojo | `evidencia/H5-S2-M2.txt` con el rojo provocado y revertido | TODO |
| H5.S2.M3 | (madre H8.S2.M3) Job de integración de la app en macOS con simulador, corriendo las siete pruebas de integración | Siete pruebas en verde en simulador | `gh run view --log` → el job con `7 passed` | TODO |

#### H5.S3 — Cada package con tareas reales

**CA:** Dado cada package, cuando corre el CI, entonces tiene lint, tipos y pruebas reales, no un mensaje de consola que simula una tarea.
**DoD:** la tabla de workspace por tarea completa y las tareas en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S3.M1 | (madre H8.S3.M1) El package de tutoriales se typechequea solo, en vez de delegarlo a quienes lo consumen | La tarea corre y termina bien | `yarn workspace @aportaya/tutoriales typecheck; echo $?` → 0 | TODO |
| H5.S3.M2 | (madre H8.S3.M2) El package de tutoriales tiene al menos una prueba real de su lógica | Una prueba o más, en verde | `yarn workspace @aportaya/tutoriales test:front` → passed | TODO |
| H5.S3.M3 | (madre H8.S3.M3) El package de diseño de la app tiene lint y pruebas propias si le faltan | Los dos comandos existen y terminan bien | ambos comandos → 0 | TODO |
| H5.S3.M4 | (madre H8.S3.M4) Escribir en `entregables/matriz-ci.md` la tabla workspace × tarea, marcando lo que no aplica y por qué | Nueve filas completas | `grep -c "^| @aportaya" entregables/matriz-ci.md` → 9 | TODO |

#### H5.S4 — Dueños de código y protección de rama, documentadas

**CA:** Dado el archivo de dueños de código, cuando alguien toca una carpeta sensible, entonces el dueño queda identificado; y la política de protección de rama está escrita con sus checks exactos, sin ejecutarse sobre el repositorio.
**DoD:** el archivo válido según GitHub y la sección escrita con los comandos marcados como no ejecutados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S4.M1 | (madre H8.S4.M1) Escribir el archivo de dueños de código para sesión, configuración del gateway, dinero, workflows y despliegue | El archivo es válido para GitHub | `gh api repos/.../codeowners/errors` tras el push → sin errores | TODO |
| H5.S4.M2 | (madre H8.S4.M2) Escribir la política de protección con los nombres exactos de los checks requeridos y la restricción real del plan del repositorio | Los comandos quedan marcados como **no ejecutados** | `grep -c "NO EJECUTADO" entregables/proteccion-de-rama.md` → ≥ 1 | TODO |
| H5.S4.M3 | (madre H8.S4.M3) Configurar actualizaciones automáticas de dependencias para el monorepo, la app y las acciones, semanales y agrupadas | El archivo es válido | validación del esquema local o la respuesta de GitHub tras el push → sin error de parseo | TODO |

#### H5.S5 — Las cabeceras del HTML del backoffice

**CA:** Dado el HTML del backoffice servido por su servidor, cuando se consultan sus cabeceras, entonces están la política de contenido, el transporte estricto, el tipo sin adivinar, la política de referencia, los permisos de funciones, el bloqueo de enmarcado, la ausencia de caché y la marca de no indexar.
**DoD:** la salida de la consulta de cabeceras pegada y los escenarios de punta a punta en verde con la política activa.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S5.M1 | (madre H8.S5.M1) Escribir la política de contenido del backoffice con el origen propio y el gateway, sin permitir scripts en línea, y registrar como deuda la excepción de estilos | La cabecera aparece en la respuesta | consulta de cabeceras → la línea pegada | TODO |
| H5.S5.M2 | (madre H8.S5.M2) Agregar transporte estricto, permisos de funciones, ausencia de caché para HTML y la marca de no indexar | Las cuatro cabeceras presentes | consulta → cuatro líneas pegadas | TODO |
| H5.S5.M3 | (madre H8.S5.M3) Correr los escenarios del backoffice contra el contenedor con la política activa | Cero violaciones de política en la consola | los escenarios → passed con el registro de consola pegado | TODO |
| H5.S5.M4 | (madre H8.S5.M4) Mismas cabeceras en el servidor de render del sitio, sin agregar dependencias nuevas sin justificar | La consulta al sitio muestra las cabeceras | consulta → pegada | TODO |
| H5.S5.M5 | (madre H8.S5.M5) Escribir en `entregables/` qué se espera del gateway respecto de la cookie de sesión y con qué comando se verifica | La nota tiene el comando de verificación | `grep -c "SameSite" entregables/cookies-esperadas.md` → ≥ 1 | TODO |
| H5.S5.M6 | (madre H8.S5.M6) Registrar el hallazgo de cabeceras como corregido y commitear `fix(security): cabeceras HTTP del backoffice y del sitio` | La entrada con evidencia y pruebas | `git log --oneline -1` → el commit | TODO |

#### H5.S6 — Dependencias y el paso de clientes al día

**CA:** Dado el informe de vulnerabilidades, cuando se lee, entonces cada aviso de severidad alta o crítica tiene parche aplicado dentro del mismo major o su motivo escrito; y el CI falla si alguien cambia un contrato sin regenerar los clientes.
**DoD:** el informe antes y después pegado, y el paso de clientes demostrado en rojo con un contrato cambiado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S6.M1 | (madre H8.S6.M1) Triage de los avisos: paquete, severidad, ruta de dependencia y acción | La tabla cubre todos los avisos del informe | `entregables/triage-dependencias.md` con una fila por aviso | TODO |
| H5.S6.M2 | (madre H8.S6.M2) Aplicar parches dentro del mismo major para los avisos altos y críticos, con la suite dirigida en verde | El informe queda sin altos ni críticos sin triage | informe de vulnerabilidades → pegado antes y después | TODO |
| H5.S6.M3 | (madre H8.S6.M3) Inventario de dependencias declaradas sin uso en las apps y los packages, quitando las que no se usan | La lista con uso y sin uso, y la instalación limpia después | `evidencia/H5-S6-M3.txt` con la tabla | TODO |
| H5.S6.M4 | (madre H8.S6.M4) Comprobar que no hay duplicados de major en el árbol de dependencias | La comprobación termina bien | comando de deduplicación en modo verificación → 0 | TODO |
| H5.S6.M5 | (madre H0.S1.M9) Paso de CI "clientes al día": regenerar y fallar si queda diferencia, igual que el gate del esquema | Un contrato cambiado sin regenerar pone el job en rojo | commit de prueba con un campo nuevo en un contrato sin regenerar → job en rojo pegado; revertido después | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-L1 | ¿Los minutos de macOS alcanzan para tres jobs por push (goldens, integración, release iOS)? | Pablo (dueño de la cuenta) | La cadencia de los jobs, no su existencia | Alcanzan. Medís la duración en las primeras corridas; si no alcanzan, el release iOS pasa a ejecución manual y por etiquetas, **nunca** se elimina, y la decisión se registra |
| Q-L2 | ¿Quién carga los cinco secretos de firma de iOS y cuándo? | Pablo | La subida a distribución, no el IPA | Los carga Pablo. Hasta entonces el IPA sale sin firmar y el paso de subida queda salteado, declarado, nunca fingido |
| Q-L3 | ¿El backoffice se sirve desde su propio host o detrás del mismo origen que el sitio? | Infra y Justin (que define el origen propio) | El valor exacto del origen en la política de contenido | Mismo origen, coherente con la decisión de configuración; si resulta otro host, es hallazgo y se registra antes de cambiar la política |
| Q-L4 | ¿La herramienta de pruebas de integración instalada soporta correr contra simulador iOS en el CI? | Verificable: se comprueba la versión instalada | La forma exacta del paso de simulador | Se verifica **antes** de escribir el paso (regla 00: no se inventa la API de un tercero); si no lo soporta, se usa el corredor estándar con el simulador ya arrancado |
| Q-L5 | ¿La política de contenido rompe algo del backoffice por estilos en línea del framework? | Verificable en la corrida | El nivel de estrictez de la política | Se permite estilos en línea y se registra como deuda con la alternativa (nonce); scripts en línea **no** se permiten |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` del trabajo escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, **sin secretos ni tokens** (regla 90.3): ninguna
      salida de CI pegada puede contener el valor de una variable secreta.
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `code-quality-gates` y
      `dependency-management` por el triage; `mobile-release-security` por el release iOS;
      `server-hardening` por las cabeceras.
- [ ] Peldaño de evidencia declarado por área (regla 30). Un CI verde con todo sano demuestra el
      camino feliz: para declarar más, hay que haber roto algo a propósito (H3.S1.M5, H5.S2.M2).
- [ ] Ningún test borrado, saltado ni debilitado, y ningún `|| true` ni continuación ante error en
      un gate obligatorio (regla 80.5).
- [ ] Nada quedó corriendo al cerrar el turno: servidores de prueba y contenedores bajados, y
      declarado en el daily (regla 70.2).
