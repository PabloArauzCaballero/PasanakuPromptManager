# La sesión del backoffice deja de mentir: un refresh, una restauración, y una auditoría que no finge

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** Richard · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Bloque:** **C — AportaYa** (el bloque B, `PR6-SmartPresentational.Frontend`, es de `mantra-core-health`: otro repo, otras reglas). **Un trabajo activo por vez** (regla 70.1): A backend → B mantra → C este.
- **Repo:** el monorepo de AportaYa — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2; `PasanakuFrontend` es su espejo) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` para `apps/` · **tu rama:** `richard/frontend/sesion`
- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 · te tocan **H1, H2 y H3** de ese plan
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md)
- **4 hitos · 11 subtareas · 51 microtareas**

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
| `authn-identity` | Rotación de refresh tokens, dónde vive cada token y qué significa cerrar sesión |
| `angular-signals-state` | La máquina de estados de sesión con signals y por qué `effect` no va acá |
| `angular-testing` | `HttpTestingController`, `fakeAsync`/`tick`, `TestBed` standalone para los specs del interceptor |
| `concurrency-and-locking` | El patrón single-flight: una operación en vuelo, N esperando el mismo resultado |
| `flutter-testing` | `http_mock_adapter` y los tests de `_TrazaYSesion` en Dart |
| `e2e-playwright` | Los E2E de sesión expirada y restauración, con web-first assertions y sin esperas fijas |
| `audit-trail-history` | Por qué la auditoría de lectura no puede vivir en el navegador |
| `frontend-ux-states` | Los estados `RESTORING` y `ERROR` del arranque, accionables y distinguibles |
| `visual-proof` | Las capturas por viewport y tema de los estados nuevos |
| `evidence-and-verification` | El peldaño que podés declarar con la evidencia que tengas |
| `root-cause-debugging` | Si un spec queda en rojo: reproducir y demostrar la causa antes de tocar nada |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **90** (sesión, tokens, PII en URLs) · **98** (el refresh cruza al servicio `identidad`)

> **Ojo con el bloque B.** En `mantra-core-health` las reglas 91 y 98 no aplican. **Acá sí.**
> Esto es AportaYa: hay dinero detrás de la sesión que estás arreglando.

## 2. Resultado observable

Un operador del backoffice con diez peticiones en vuelo y el token vencido ve **una** llamada a
`/sesion/refrescar` y sus diez pantallas cargan; si recarga el navegador sobre una ruta protegida
vuelve a esa ruta en vez de al login; y si el registro de acceso a un expediente falla, alguien se
entera, porque ya no se traga el error.

**Kill-test:** con el backoffice servido, `page.route` fuerza `401` en la primera respuesta de tres
recursos y se cuentan los `POST /sesion/refrescar`. Hoy salen **tres** (uno por petición:
`sesion.interceptor.ts:28` hace el refresh con el mismo `HttpClient` interceptado y no hay nada que
comparta el vuelo). Si al cerrar sigue saliendo más de uno, esto NO está hecho. Segundo kill-test:
`F5` sobre `/operacion/reclamos` con cookie válida. Hoy cae en `/ingreso` siempre, porque
`permisos.ts:26` decide de forma síncrona y nadie intenta restaurar.

## 3. Alcance

**IN:**
- `apps/backoffice/src/app/nucleo/`: `sesion.ts`, `sesion.interceptor.ts`, `permisos.ts`,
  `registro-de-acceso.interceptor.ts`, y los nuevos `refresco-de-sesion.ts` y `auth-bootstrap.ts`.
- `apps/backoffice/src/app/app.config.ts` (sos el dueño del archivo en este turno).
- `apps/backoffice/src/app/rutas/ingreso/**` (el `volverA` tras el login).
- El componente `RestaurandoSesion` y la pantalla de error de restauración.
- `apps/movil/lib/dominio/cliente.dart` y `apps/movil/lib/proveedores/sesion.dart`.
- E2E nuevos: `apps/backoffice/e2e/{sesion-expirada,restaurar-sesion}.e2e.ts`.

**OUT:** todo lo demás del monorepo, y en particular: `gateway.ts` y `rutas/sistemas/**` (son de
Justin), `.github/workflows/**` y `apps/movil/lib/infraestructura/**` (Leo), `packages/**`,
`eslint.config.js` y `apps/web/src/server.ts` (Marcelo), `clientes/**` y `docs/auditoria/**`
(Pablo). Tampoco tocás `servicios/**` ni ningún `openapi/*.yaml`: si el contrato no alcanza, es
brecha y se registra, no se edita.

**Reservas de archivos:** las nueve rutas del IN son tuyas y de nadie más en este turno. Si
necesitás un paso de CI para tus E2E, lo dejás escrito en `entregables/` y lo cablea Leo.

## 4. Plan

### H1 — La línea base de tu carril es un hecho registrado, no un supuesto

**CA:** Dado el SHA de arranque, cuando alguien lee tu daily, entonces sabe qué comandos de tu área corren hoy, cuáles fallan y con qué salida, sin haber tenido que correrlos él.
**DoD:** las cuatro salidas pegadas en `evidencia/` con su `exit=`, y la tabla de comandos reales del daily completa.
**Estado:** TODO

#### H1.S1 — Entorno, SHA y estado real de los tests de sesión

**CA:** Dado tu clon, cuando corrés los tests del backoffice y de la app, entonces registrás el resultado tal cual es, sin corregir nada todavía.
**DoD:** `evidencia/H1-S1-*.txt` con las salidas literales.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar el SHA de arranque de tu rama y crear `richard/frontend/sesion` desde `dev` | La rama existe y su base es el SHA declarado | `git rev-parse HEAD` → pegado en el daily; `git branch --show-current` → `richard/frontend/sesion` | TODO |
| H1.S1.M2 | Instalar el estándar y verificarlo (sección 1) | Las dos salidas pegadas en el daily | `python .claude/hooks/plan_gate.py --self-test; echo exit=$?` → `0` | TODO |
| H1.S1.M3 | Correr `yarn workspace @aportaya/backoffice test:front` y registrar el conteo tal cual está hoy | Conteo `passed/failed` registrado, sin corregir nada | comando → `evidencia/H1-S1-M3.txt` con `exit=` | TODO |
| H1.S1.M4 | Correr `flutter test test/unidad test/widget` en `apps/movil` y registrar el conteo | Conteo registrado | comando → `evidencia/H1-S1-M4.txt` con `exit=` | TODO |

### H2 — Diez `401` simultáneos producen exactamente un refresh (madre H1)

**CA:** Dado un access token vencido y un refresh válido, cuando diez peticiones reciben `401` a la vez, entonces sale **una** llamada a `/sesion/refrescar`, las diez se reintentan una sola vez con el token nuevo y todas completan; si el refresh falla, la sesión se cierra **una** vez y las diez fallan con su error original, sin segundo refresh y sin bucle.
**DoD:** `sesion.interceptor.spec.ts` y `test/unidad/cliente_refresco_test.dart` con los cuatro casos en verde, salidas pegadas; `yarn lint && yarn typecheck` sin `eslint-disable` nuevos; E2E `sesion-expirada` PASS con trace.
**Estado:** TODO

#### H2.S1 — Caracterización: el defecto queda demostrado antes de tocarlo

**CA:** Dado el interceptor actual, cuando corre el caso de diez `401` concurrentes, entonces el spec **falla** mostrando diez refresh.
**DoD:** `evidencia/H2-S1-M2.txt` con `expected 1 … received 10`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | (madre H1.S1.M1) Crear `sesion.interceptor.spec.ts` con el caso "un `401` → un refresh → un reintento" | El spec **pasa** contra el código actual | `yarn workspace @aportaya/backoffice test:front --include='src/app/nucleo/sesion.interceptor.spec.ts'` → 1 passed | TODO |
| H2.S1.M2 | (madre H1.S1.M2) Agregar el caso "diez `401` concurrentes → exactamente un refresh" | El spec **falla** con conteo 10 | mismo comando → `1 failed` con el conteo pegado | TODO |

#### H2.S2 — Single-flight en el backoffice

**CA:** Dado el interceptor nuevo, cuando llegan N `401` con un refresh en vuelo, entonces todos esperan el mismo `Observable` y el `POST` de refresh no atraviesa la cadena de interceptores.
**DoD:** los cuatro casos del §4 del metaprompt en verde; commit `fix(auth): refresh single-flight en el backoffice`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | (madre H1.S2.M1) Extraer el refresh a `RefrescoDeSesion` con `HttpBackend` propio, `shareReplay(1)` y `finalize` que limpia el vuelo | El `POST` sale sin `Authorization` ni las cabeceras que agregan los interceptores | spec: `expectOne('/sesion/refrescar')` sin esas cabeceras → PASS | TODO |
| H2.S2.M2 | (madre H1.S2.M2) Reescribir `sesionInterceptor` para usar `RefrescoDeSesion` y reintentar una sola vez | El caso de H2.S1.M2 pasa | spec de H2.S1.M2 → PASS | TODO |
| H2.S2.M3 | (madre H1.S2.M3) Caso límite: refresh lento y cinco peticiones nuevas durante el vuelo | Cero refresh adicionales; las cinco se reintentan con el mismo resultado | spec `refresh en vuelo no dispara otro` → PASS | TODO |
| H2.S2.M4 | (madre H1.S2.M4) Caso error: el refresh responde `401`, `5xx` o falla la red | `sesion.cerrar()` se llama una vez; las N fallan con su error original; cero segundos refresh | spec con `expect(cerrar).toHaveBeenCalledTimes(1)` → PASS | TODO |
| H2.S2.M5 | (madre H1.S2.M5) Caso rotación: la respuesta trae acceso nuevo y el reintento usa solo ese | `Authorization` del reintento = `Bearer <nuevo>` | spec `reintento usa el token nuevo` → PASS | TODO |
| H2.S2.M6 | (madre H1.S2.M6) Protección de bucle: una petición ya reintentada que recibe `401` no vuelve a refrescar | Segundo `401` → error propagado, cero refresh | spec `401 tras reintento no refresca` → PASS | TODO |
| H2.S2.M7 | (madre H1.S2.M7) Registrar en `entregables/decision-httpbackend.md` por qué el refresh usa un cliente sin interceptores y qué alternativa se descartó | La nota tiene contexto, alternativa y consecuencia | `grep -c "HttpBackend" entregables/decision-httpbackend.md` → ≥ 1 | TODO |

#### H2.S3 — Single-flight en la app (Dart/Dio)

**CA:** Dado `_TrazaYSesion`, cuando N peticiones reciben `401`, entonces comparten un único `Future` de refresh, el refresh sale por un `Dio` sin el interceptor de sesión, y tras la rotación el siguiente refresh usa exclusivamente el par nuevo del `AlmacenSeguro`.
**DoD:** cuatro casos en `test/unidad/cliente_refresco_test.dart` en verde; `dart analyze --fatal-infos` limpio.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S3.M1 | (madre H1.S3.M1) Test de caracterización: diez `401` concurrentes con `DioAdapter` mock | El test falla mostrando diez `POST /sesion/refrescar` | `flutter test test/unidad/cliente_refresco_test.dart` → `expected 1, actual 10` pegado | TODO |
| H2.S3.M2 | (madre H1.S3.M2) Introducir `_Refrescador` con `Future` compartido y un `Dio` de refresh separado | Diez `401` → un refresh; el `Dio` de refresh no agrega `Authorization` | mismo test → PASS | TODO |
| H2.S3.M3 | (madre H1.S3.M3) Caso límite: las peticiones que llegan durante el refresh esperan el mismo `Future` | Cero refresh adicionales | test `en vuelo` → PASS | TODO |
| H2.S3.M4 | (madre H1.S3.M4) Caso error: el refresh falla → `cerrar()` una vez y las pendientes reciben `ErrorDeApi(401)` | `almacen.borrar` llamado exactamente dos veces (acceso y refresco) | test `falla → cerrar una vez` → PASS | TODO |
| H2.S3.M5 | (madre H1.S3.M5) Caso rotación: tras el refresh, `tokenDeRefresco()` devuelve el nuevo y el siguiente refresh lo manda | El segundo `POST` lleva el refresco nuevo | test `rotación` → PASS | TODO |

#### H2.S4 — La red lo demuestra de punta a punta

**CA:** Dado el backoffice contra el simulado con sesión, cuando el E2E expira el token y navega a tres secciones a la vez, entonces la red muestra un solo `POST /sesion/refrescar` y las tres pantallas cargan.
**DoD:** `sesion-expirada.e2e.ts` PASS con trace; consola sin errores nuevos.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S4.M1 | (madre H1.S4.M1) Escribir `sesion-expirada.e2e.ts` que fuerza `401` en tres recursos y cuenta los refresh | Conteo = 1 y las tres pantallas muestran datos | `yarn workspace @aportaya/backoffice test:e2e sesion-expirada` → 1 passed | TODO |
| H2.S4.M2 | (madre H1.S4.M2) Regresión dirigida: `test:front` del backoffice completo y `flutter test test/unidad` | Todo en verde con los conteos pegados | ambos comandos → 0 failed | TODO |
| H2.S4.M3 | (madre H1.S4.M3) Registrar el hallazgo del refresh (backoffice y app) como corregido en `entregables/hallazgos-sesion.md`, con evidencia, causa raíz y pruebas | Las dos entradas con las seis secciones del formato de hallazgo | `grep -c "^## F-" entregables/hallazgos-sesion.md` → 2 | TODO |

### H3 — Recargar el navegador ya no te echa del backoffice (madre H2)

**CA:** Dado un operador con cookie de refresh válida, cuando recarga sobre `/operacion/reclamos` o abre un deep link protegido, entonces ve un estado de restauración y después la pantalla pedida; con cookie inválida termina en `/ingreso`; con `identidad` caído ve un error accionable y **nunca** un login silencioso mientras el estado es desconocido.
**DoD:** `sesion.spec.ts` con la máquina de cinco estados, `auth-bootstrap.spec.ts` con cinco casos, `permisos.spec.ts` extendido, E2E `restaurar-sesion` con los cinco escenarios PASS y doce capturas inspeccionadas.
**Estado:** TODO

#### H3.S1 — La máquina de estados de la sesión

**CA:** Dado `Sesion`, cuando se consulta su estado, entonces devuelve exactamente uno de `UNKNOWN`, `RESTORING`, `AUTHENTICATED`, `ANONYMOUS` o `ERROR`, arranca en `UNKNOWN`, y `abierta()` solo es verdadero en `AUTHENTICATED`.
**DoD:** `sesion.spec.ts` con la tabla de transiciones en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | (madre H2.S1.M1) Agregar `estado` como signal y derivar `abierta` de `AUTHENTICATED` | Los specs existentes de `nucleo/` siguen pasando | `…test:front --include='src/app/nucleo/*.spec.ts'` → 0 failed | TODO |
| H3.S1.M2 | (madre H2.S1.M2) Métodos de transición (`restaurando`, `anonima`, `fallo`) con las transiciones permitidas | `UNKNOWN → ANONYMOUS` directo se rechaza | spec `no se puede pasar de UNKNOWN a ANONYMOUS sin restaurar` → PASS | TODO |
| H3.S1.M3 | (madre H2.S1.M3) `sesion.spec.ts` con la tabla de ocho transiciones | 8 passed | mismo comando → 8 passed | TODO |

#### H3.S2 — `AuthBootstrap`: nadie decide "no hay sesión" sin haber preguntado

**CA:** Dado el arranque, cuando se resuelve el inicializador, entonces ya se intentó el refresh con un timeout de cinco segundos y el estado quedó en `AUTHENTICATED`, `ANONYMOUS` o `ERROR`.
**DoD:** `auth-bootstrap.spec.ts` con cinco casos en verde; el arranque no bloquea más que el timeout.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | (madre H2.S2.M1) Crear `auth-bootstrap.ts` con `provideAppInitializer` que llama a `RefrescoDeSesion` y mapea el resultado al estado | Con refresh `200` → `AUTHENTICATED` y el token queda cargado | spec `cookie válida → AUTHENTICATED` → PASS | TODO |
| H3.S2.M2 | (madre H2.S2.M2) Caso cookie inválida (`401`) → `ANONYMOUS`, no `ERROR` | Estado final `ANONYMOUS` | spec → PASS | TODO |
| H3.S2.M3 | (madre H2.S2.M3) Caso `identidad` caído (`503` o error de red) → `ERROR` | Estado `ERROR` y ningún redirect a `/ingreso` | spec → PASS | TODO |
| H3.S2.M4 | (madre H2.S2.M4) Caso timeout con `fakeAsync`: el refresh no responde en cinco segundos → `ERROR` | Estado `ERROR` a los 5 s exactos | spec con `tick(5000)` → PASS | TODO |
| H3.S2.M5 | (madre H2.S2.M5) Caso concurrencia: un `401` de otra petición durante el bootstrap no dispara un segundo refresh | `expectOne('/sesion/refrescar')` | spec → PASS | TODO |
| H3.S2.M6 | (madre H2.S2.M6) Registrar el inicializador en `app.config.ts` | El backoffice compila | `yarn workspace @aportaya/backoffice build; echo $?` → 0 | TODO |

#### H3.S3 — El guard espera, y la pantalla lo cuenta

**CA:** Dado `requiereSesion()`, cuando el estado es desconocido o restaurando, entonces el guard espera al desenlace; en `ANONYMOUS` redirige preservando la ruta pedida; en `ERROR` muestra una pantalla accionable con "Reintentar".
**DoD:** `permisos.spec.ts` extendido, el componente con su spec de accesibilidad, y doce capturas inspeccionadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | (madre H2.S3.M1) `requiereSesion()` devuelve un `Observable` que espera a que el estado salga de desconocido/restaurando | Con `RESTORING` no emite hasta la transición | spec `espera mientras restaura` → PASS | TODO |
| H3.S3.M2 | (madre H2.S3.M2) En `ANONYMOUS` redirige a `/ingreso?volverA=<ruta>` | El `UrlTree` contiene `volverA` | spec → PASS | TODO |
| H3.S3.M3 | (madre H2.S3.M3) `pantalla-de-ingreso.ts` navega a `volverA` tras el login, solo si es ruta interna | Una ruta externa se ignora y va a `/tablero` | spec `volverA externo se ignora` → PASS | TODO |
| H3.S3.M4 | (madre H2.S3.M4) Componente `RestaurandoSesion` con `aria-busy` y texto explícito mientras restaura | Spec de accesibilidad sin violaciones | `…test:a11y --include='**/restaurando-sesion.a11y.spec.ts'` → 0 violations | TODO |
| H3.S3.M5 | (madre H2.S3.M5) Pantalla de `ERROR` con mensaje accionable y botón "Reintentar" que vuelve a intentar el refresh | El click dispara un `POST /sesion/refrescar` nuevo | spec → `expectOne` tras el click | TODO |
| H3.S3.M6 | (madre H2.S3.M6) Prueba visual de los dos estados en tres viewports y dos temas | Doce capturas **miradas**: sin recortes ni texto ilegible | `ls evidencia/H3-S3-M6-*.png` → 12 archivos + la nota de qué viste | TODO |

#### H3.S4 — Los cinco escenarios, en el navegador

**CA:** Dado el backoffice contra el simulado, cuando corre `restaurar-sesion.e2e.ts`, entonces F5 en ruta protegida, deep link con cookie válida, cookie inválida, `identidad` caído y refresh concurrente durante el bootstrap se comportan como dice el CA del hito.
**DoD:** cinco tests PASS con trace.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S4.M1 | (madre H2.S4.M1) E2E "F5 sobre `/operacion/reclamos` con cookie válida" | Tras el reload la URL sigue siendo la misma y la tabla carga | `test:e2e restaurar-sesion -g F5` → passed | TODO |
| H3.S4.M2 | (madre H2.S4.M2) E2E "deep link a `/cumplimiento/verificaciones` en pestaña nueva" | Llega sin pasar por `/ingreso` | `-g "deep link"` → passed | TODO |
| H3.S4.M3 | (madre H2.S4.M3) E2E "cookie inválida" | Termina en `/ingreso` con `volverA` | `-g "inválida"` → passed | TODO |
| H3.S4.M4 | (madre H2.S4.M4) E2E "identidad no disponible" | Pantalla de error con "Reintentar" visible y sin redirect | `-g "no disponible"` → passed | TODO |
| H3.S4.M5 | (madre H2.S4.M5) E2E "refresh concurrente durante el bootstrap" | Un solo `POST /sesion/refrescar` contado en la red | `-g concurrente` → passed | TODO |
| H3.S4.M6 | (madre H2.S4.M6) Registrar el hallazgo de restauración como corregido y commitear `fix(auth): restauración de sesión al arrancar` | La entrada con evidencia, causa raíz, corrección y pruebas | `git log --oneline -1` → el commit | TODO |

### H4 — El navegador deja de fingir que garantiza la auditoría (madre H3)

**CA:** Dado un operador que abre un expediente, cuando la lectura se completa, entonces ningún código del frontend afirma que la auditoría quedó registrada; si el registro falla, se reporta y se ve; y si el contrato del backend no existe, el frontend no manda nada y la brecha queda escrita.
**DoD:** `registro-de-acceso.interceptor.spec.ts` con los tres niveles en verde; ningún `catchError` que devuelva vacío sobre la llamada de auditoría; `grep` de la palabra "garantiza" en ese archivo → 0.
**Estado:** TODO

#### H4.S1 — Qué exige el backend, y qué no existe

**CA:** Dado el resultado del descubrimiento de Pablo, cuando leés su entrega, entonces sabés si `POST /extraccion/accesos` existe en algún contrato y con qué campos; si no existe, queda escrito como brecha con el control esperado del lado servidor.
**DoD:** `entregables/brecha-auditoria.md` con la cita al contrato o la declaración de inexistencia.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | (madre H3.S1.M1) Escribir `entregables/brecha-auditoria.md`: amenaza, control esperado del lado servidor, servicio dueño y contrato mínimo | La nota nombra el servicio dueño y el evento esperado | `grep -c "extraccion/accesos" entregables/brecha-auditoria.md` → ≥ 1 | TODO |
| H4.S1.M2 | (madre H3.S1.M2) Verificar que el `rutaId` que se manda hoy no lleve identificadores de persona en ninguna pantalla que marque acceso a datos (regla 90.2.2) | Tabla de pantallas con su URL de lectura; ninguna con documento o cuenta en path o query, o queda registrado el hallazgo | `grep -rn "ACCESO_A_DATOS" apps/backoffice/src --include=*.ts` → tabla en `entregables/` | TODO |
| H4.S1.M3 | (madre H3.S1.M3) Registrar la decisión: el frontend no es fuente de auditoría; qué metadata se conserva y qué garantía se elimina | La nota tiene las dos alternativas y la elegida | `grep -c "fuente de auditoría" entregables/brecha-auditoria.md` → ≥ 1 | TODO |

#### H4.S2 — El interceptor, con los tres niveles del contrato

**CA:** Dado el interceptor nuevo, cuando el registro falla, entonces se reporta con su identificador de correlación y se avisa sin bloquear; cuando el contrato no existe, no se manda nada y el archivo lo dice.
**DoD:** los tres niveles en verde; `yarn lint` limpio.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | (madre H3.S2.M1) Test de caracterización: hoy la lectura se muestra aunque el registro falle y el error desaparece | El spec documenta el comportamiento actual y pasa | `…test:front --include='**/registro-de-acceso.interceptor.spec.ts'` → passed | TODO |
| H4.S2.M2 | (madre H3.S2.M2) Nivel correcto: el registro sale después del éxito, con recurso, id y correlación, y **sin** la query en la ruta | Cuerpo exacto y sin `?` en el campo de ruta | spec → PASS | TODO |
| H4.S2.M3 | (madre H3.S2.M3) Nivel límite: lectura vacía no registra; dos lecturas iguales seguidas registran dos veces | Conteos exactos | spec → PASS | TODO |
| H4.S2.M4 | (madre H3.S2.M4) Nivel inválido: el registro falla → se emite el error a telemetría con la correlación y se avisa en pantalla; nada de tragarse el error | El doble de telemetría recibe exactamente una llamada | spec → PASS | TODO |
| H4.S2.M5 | (madre H3.S2.M5) Si el contrato no existe: el interceptor queda detrás de una bandera desactivada y no manda nada; el comentario del archivo se reescribe sin la palabra "garantiza" | Con la bandera apagada no sale ninguna petición de registro | spec `expectNone` → PASS · `grep -c garant <archivo>` → 0 | TODO |
| H4.S2.M6 | (madre H3.S2.M6) Registrar el hallazgo con su doble estado (corregido del lado cliente, bloqueado del lado backend) y commitear `fix(security): la auditoría de lectura no depende del navegador` | La entrada declara los dos estados | `git log --oneline -1` → el commit | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-R1 | ¿`POST /sesion/refrescar` acepta cookie HttpOnly sin cuerpo, como decidió D-A3? | Dueño de `identidad`; Pablo lo confirma en su H0.S3 | El caso de rotación contra el backend real | Sí acepta cookie. Si no, es brecha del backend: construís y verificás contra un doble que cumple el contrato con cookie (regla 65) y lo declarás |
| Q-R2 | ¿`POST /extraccion/accesos` existe en algún contrato? | Pablo (descubrimiento H0.S3) | El nivel correcto de H4.S2 | No existe hasta que se demuestre; el interceptor queda tras bandera desactivada y la brecha se escribe |
| Q-R3 | ¿El refresh rota el token en el backend? Si rota, N refresh concurrentes hoy revocan la familia entera | Dueño de `identidad` | La gravedad real del defecto que estás corrigiendo | Rota. Es la hipótesis que hace urgente el single-flight; se declara como hipótesis, no como hecho |
| Q-R4 | ¿El cableado de los providers de Justin en `app.config.ts` entra en tu turno? | Coordinación, primera hora | Nada: es una microtarea tuya cuando Justin entregue | Entra como microtarea nueva agregada al plan cuando llegue la entrega; no la hacés "de paso" |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` del trabajo escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin tokens, sin cookies y sin datos de personas
      (regla 90.2: si una salida los tenía, se enmascara **y se aclara que se enmascaró**).
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `data-privacy-financial`
      porque tocás el registro de acceso a expedientes; `security-guardrails` porque tocás sesión;
      `visual-proof` por los estados nuevos de H3.S3.
- [ ] Peldaño de evidencia declarado por área (regla 30). Recordá: un cambio posterior devuelve el
      área tocada a `WRITTEN` y hay que re-verificar.
- [ ] Ningún test borrado, saltado ni debilitado para cerrar (regla 80.5).
