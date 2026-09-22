# La línea base que nadie discute, los contratos como frontera, y el cierre con hechos

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** Pablo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Bloque:** **C — AportaYa** (el bloque B, `PR10-CatalogoYGates.Frontend`, es de `mantra-core-health`: otro repo, otras reglas). **Un trabajo activo por vez** (regla 70.1): A backend → B mantra → C este.
- **Repo:** el monorepo de AportaYa — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2; `PasanakuFrontend` es su espejo) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `pablo/frontend/contratos`
- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 · te tocan **H0 (global), H11, H13 y H14**
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md)
- **5 hitos · 10 subtareas · 58 microtareas**

> **Tu carril es el primero y el último.** La línea base (H2) la necesitan los otros cuatro para
> arrancar, y el cierre (H5) solo se puede escribir cuando ellos terminaron. Entre medio, H3 y H4
> son tuyos y no dependen de nadie.

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
| `factual-discovery` | Separar hechos, desconocidos e hipótesis antes de que nadie toque código |
| `service-contracts-versioning` | Los clientes generados como frontera y qué significa romper un contrato |
| `api-openapi-docs` | Qué exige cada contrato y cómo se lee lo que el frontend consume |
| `authz-access-control` | Qué decide la interfaz y qué decide el servidor, y cómo se prueba la diferencia |
| `concurrency-and-locking` | Idempotencia de extremo a extremo: misma operación, misma clave |
| `e2e-playwright` | Los escenarios de autorización e idempotencia, con vigilancia de red |
| `microservices-testing` | Pruebas de contrato del lado consumidor contra los ejemplos |
| `technical-docs-and-adr` | Los ADR de clientes versionados y de fronteras de repositorio |
| `qa-evidence-reporting` | El informe de evidencia que consolida lo que cubrieron los cinco carriles |
| `work-report-md` | El reporte final con las tres secciones y el avance calculado |
| `secure-code-review` | La pasada final enfocada solo en seguridad |
| `evidence-and-verification` | El peldaño que podés declarar, por área, con la evidencia que haya |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **90** (autorización y datos expuestos) · **91** (toda pantalla que muestre un importe) · **98** (los contratos cruzan servicios)

> **Ojo con el bloque B.** En `mantra-core-health` las reglas 91 y 98 no aplican. **Acá sí.**
> Los escenarios de idempotencia que vas a escribir cubren formularios que mueven plata.

## 2. Resultado observable

Cualquiera clona el monorepo sin tener Java instalado y el frontend compila, porque los clientes
generados están versionados; un operador sin permiso que navega directo o al que el servidor le
responde que no puede ve un estado honesto en vez de una pantalla muda; un doble clic en un
formulario de dinero manda **una** operación; y al cerrar existe un documento que responde con
hechos qué partes del frontend son confiables y cuáles no.

**Kill-test:** clonar el repo en una máquina sin Java y correr la instalación y el chequeo de
tipos. Hoy falla: `clientes/angular` y `clientes/dart` están ignorados y solo existen después de
correr la tarea de generación, que necesita el entorno de Java. Si al cerrar sigue fallando, esto
NO está hecho. Segundo kill-test: entrar con permisos reducidos y navegar directo a una sección
que no corresponde. Hoy redirige al tablero **sin decir nada**, y quien lo ve cree que la pantalla
está rota.

## 3. Alcance

**IN:**
- `.gitignore`, `.gitattributes`, `clientes/**` (los generados, versionados).
- `docs/auditoria/**`: los ocho documentos del informe.
- `docs/Arquitectura/`: la enmienda al ADR de artefactos generados y el ADR de fronteras de repositorio.
- `scripts/verificar_remotos.sh`.
- Los escenarios `apps/backoffice/e2e/{autorizacion,idempotencia}.e2e.ts` y las pruebas de contrato
  del lado consumidor.
- Los tipos escritos a mano que dupliquen modelos generados, en el dominio de las tres apps.

**OUT:** `nucleo/sesion*` y `app.config.ts` (Richard), `gateway.ts` y `rutas/sistemas/**` (Justin),
`.github/workflows/**`, `apps/movil/lib/infraestructura/**` y `despliegue/**` (Leo), `packages/**`,
`eslint.config.js`, `server.ts` y `tsconfig.base.json` (Marcelo). Tampoco tocás `servicios/**` ni
ningún contrato: si al frontend le falta una operación, se registra como brecha.

**Reservas de archivos:** las seis rutas del IN son tuyas. El paso de CI que verifica que los
clientes están al día lo escribís vos en `entregables/` y lo **cablea Leo**, que es el dueño del
archivo de flujos de trabajo.

## 4. Plan

### H1 — La línea base de tu carril es un hecho registrado

**CA:** Dado el SHA de arranque, cuando alguien lee tu daily, entonces sabe en qué estado está el repositorio y qué falla hoy, sin haberlo corrido él.
**DoD:** las cuatro salidas pegadas en `evidencia/` con su `exit=`.
**Estado:** TODO

#### H1.S1 — Entorno, SHA y el estado del repositorio

**CA:** Dado tu clon, cuando registrás el SHA, el estado de los dos remotos y el kill-test de los clientes, entonces todo queda registrado tal cual es.
**DoD:** `evidencia/H1-S1-*.txt` con las salidas literales.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar el SHA de arranque y crear `pablo/frontend/contratos` desde `dev` | La rama existe sobre el SHA declarado | `git rev-parse HEAD` pegado en el daily; `git branch --show-current` → `pablo/frontend/contratos` | TODO |
| H1.S1.M2 | Instalar el estándar y verificarlo (sección 1) | Las dos salidas pegadas en el daily | `python .claude/hooks/plan_gate.py --self-test; echo exit=$?` → `0` | TODO |
| H1.S1.M3 | Registrar el estado de los dos remotos y en qué difieren hoy | Los dos SHA de la rama de trabajo quedan pegados | consulta de referencias remotas de ambos → `evidencia/H1-S1-M3.txt` | TODO |
| H1.S1.M4 | Correr el kill-test de los clientes: instalación y chequeo de tipos en un clon sin generar clientes | El fallo actual queda registrado con su salida | `yarn install --immutable && yarn typecheck; echo exit=$?` → pegado | TODO |

### H2 — La línea base que los otros cuatro necesitan (madre H0)

**CA:** Dado el SHA de arranque, cuando alguien lee la línea base, entonces encuentra para cada comando del pipeline su salida literal y su código de salida, la lista de hallazgos abiertos con su evidencia, y un repositorio donde el frontend compila sin necesidad del entorno de Java.
**DoD:** los ocho documentos creados con su esqueleto, la línea base escrita con la tabla de comandos, los clientes versionados y el clon limpio compilando sin Java.
**Estado:** TODO

#### H2.S1 — Los clientes generados pasan a estar versionados (decisión D-A1)

**CA:** Dado un clon limpio en una máquina sin Java, cuando se instalan las dependencias y se chequean los tipos, entonces termina bien, porque los clientes ya están en el repositorio.
**DoD:** el clon limpio compilando y el gate de "clientes al día" entregado a Leo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | (madre H0.S1.M4) Generar los clientes de los catorce contratos con la tarea del proyecto | Las dos carpetas de clientes existen con sus catorce servicios | la tarea → termina bien, con el listado pegado | TODO |
| H2.S1.M2 | (madre H0.S1.M7) Enmendar el ADR de artefactos generados: los clientes se versionan y el gate pasa a ser "regenerar no produce diferencia"; quitar las dos líneas que los ignoran | El repositorio ya no ignora esas carpetas y el ADR tiene su enmienda fechada | comprobación de ignorado → ya no aplica · el ADR contiene la enmienda | TODO |
| H2.S1.M3 | (madre H0.S1.M8) Commitear los clientes generados y marcarlos como generados para que las revisiones no se llenen de ruido | Los archivos están versionados y marcados | `git ls-files clientes/ \| wc -l` → mayor que cero · el archivo de atributos los marca | TODO |
| H2.S1.M4 | (madre H0.S1.M8) Verificar el kill-test: clon limpio **sin Java**, instalación y chequeo de tipos | Termina bien | en el clon limpio: `yarn install --immutable && yarn typecheck; echo exit=$?` → `0` | TODO |
| H2.S1.M5 | (madre H0.S1.M9) Escribir para Leo el paso de CI que regenera y falla si queda diferencia, con el comando exacto | La nota tiene el comando listo para cablear | `entregables/paso-ci-clientes.md` con el comando | TODO |
| H2.S1.M6 | (madre H0.S1.M5) Dejar registrado que la instalación no modifica el archivo de bloqueo | Sin cambios en el archivo de bloqueo tras instalar | `git status --short yarn.lock` → vacío, pegado | TODO |
| H2.S1.M7 | (madre H0.S1.M1) Registrar cómo se clona el monorepo en Windows sin que falle por rutas largas | La nota tiene el ajuste necesario | `entregables/clonar-en-windows.md` con el comando | TODO |
| H2.S1.M8 | (madre H0.S1.M6) Crear los ocho documentos del informe con su esqueleto y copiar el plan madre como plan de remediación | Los ocho existen con encabezado y el plan copiado se parsea | `ls docs/auditoria` → ocho archivos · el contador de microtareas sobre el plan copiado → mayor que cero | TODO |

#### H2.S2 — Los desconocidos que traban a los demás, resueltos

**CA:** Dado el descubrimiento, cuando los otros cuatro leen tus entregas, entonces saben si el refresco acepta cookie, si existe el endpoint de registro de accesos, cómo llega la configuración del gateway al HTML desplegado y qué verifica el script de maqueta.
**DoD:** las cuatro respuestas escritas con su cita o su declaración de inexistencia, y los hallazgos abiertos.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | (madre H0.S3.M1) Localizar cómo se construye la imagen del backoffice y cómo se inyecta la configuración del gateway en su HTML | La ruta queda citada, o se declara que no está en el árbol | el barrido → pegado en la línea base; entregado a Justin y a Leo | TODO |
| H2.S2.M2 | (madre H0.S3.M2) Extraer del contrato de identidad la forma real del refresco: dónde viaja el token, qué devuelve y si rota | La tabla del contrato queda escrita con su veredicto sobre la cookie | `entregables/contrato-refresco.md` con la cita; entregado a Richard | TODO |
| H2.S2.M3 | (madre H0.S3.M3) Buscar el endpoint de registro de accesos en los catorce contratos | Existe con su contrato citado, o se declara inexistente | el barrido sobre los contratos → pegado; entregado a Richard | TODO |
| H2.S2.M4 | (madre H0.S3.M4) Leer el script de verificación de maqueta y registrar qué comprueba | El párrafo queda en la línea base con su entrada y su salida | el script → su código de salida pegado | TODO |
| H2.S2.M5 | (madre H0.S3.M5) Consultar si el repositorio admite reglas de protección pese al plan, y registrar la respuesta | La respuesta queda registrada tal cual, sin interpretarla | la consulta → `evidencia/H2-S2-M5.txt`; entregado a Leo | TODO |
| H2.S2.M6 | (madre H0.S3.M6) Escribir los hallazgos abiertos con el formato del informe: severidad, archivos, evidencia con ruta y línea, riesgo, causa raíz | Cada hallazgo tiene sus secciones y estado abierto | `grep -c "^## F-" docs/auditoria/hallazgos.md` → veinte o más | TODO |
| H2.S2.M7 | (madre H0.S3.M7) Escribir la línea base con la tabla comando → código de salida → duración → enlace a evidencia, consolidando lo que los cinco carriles midieron en su H1 | La tabla cubre los comandos del pipeline | `grep -c "exit=" docs/auditoria/frontend-baseline.md` → doce o más | TODO |

### H3 — La interfaz oculta, el servidor decide, y nada se ejecuta dos veces (madre H11)

**CA:** Dado el backoffice, cuando un operador sin permiso navega directo o el servidor le responde que no puede, entonces ve un estado honesto y accionable; y cuando hace doble clic, reintenta tras un refresco, o recarga un formulario ya enviado, la operación lógica no se duplica.
**DoD:** los escenarios de autorización e idempotencia en verde con el conteo de peticiones pegado; las pruebas de contrato del lado consumidor en verde; el inventario de modelos duplicados en cero o justificado.
**Estado:** TODO

#### H3.S1 — Autorización: lo que oculta la interfaz no es lo que protege

**CA:** Dado un operador con permisos reducidos, cuando navega directo, cuando el servidor rechaza, o cuando sus permisos cambian durante la sesión, entonces la interfaz se comporta de forma honesta y explicada en los tres casos.
**DoD:** tres escenarios en verde y la sección escrita que distingue lo que decide cada lado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | (madre H11.S1.M1) Escenario: con permisos reducidos, navegar directo a una sección ajena muestra un aviso, no un redirect mudo | El aviso es visible y anunciado por lector | el escenario → passed | TODO |
| H3.S1.M2 | (madre H11.S1.M2) Escenario: el servidor rechaza por permisos y la pantalla muestra el estado "sin permiso", no un error genérico | El texto de permiso aparece, no el de error | el escenario → passed | TODO |
| H3.S1.M3 | (madre H11.S1.M3) Escenario: los permisos cambian en el refresco, el menú se recalcula y la ruta que ya no alcanza redirige | El menú pierde la sección y la URL cambia | el escenario → passed | TODO |
| H3.S1.M4 | (madre H11.S1.M4) Prueba de que ocultar un botón no impide la petición: el servicio igual la manda y el rechazo se clasifica | La prueba documenta que la interfaz no protege | la prueba → passed | TODO |
| H3.S1.M5 | (madre H11.S1.M5) Escribir la sección que distingue lo que decide la interfaz de lo que decide el servidor, citando los archivos reales | La tabla está en la arquitectura objetivo | `grep -c "servidor" docs/auditoria/arquitectura-objetivo.md` → uno o más en esa sección | TODO |

#### H3.S2 — Idempotencia con semántica, no con buena intención

**CA:** Dada una operación con efecto, cuando se la dispara dos veces por doble clic, por reintento tras refresco o por vencimiento con reintento, entonces se usa la misma clave; y cuando se abre el formulario de nuevo, la clave es otra.
**DoD:** las pruebas del interceptor y los cuatro escenarios en verde con las claves comparadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | (madre H11.S2.M1) Prueba del interceptor: la clave del contexto llega como cabecera; sin contexto no se agrega ninguna | Dos casos en verde | la prueba → passed | TODO |
| H3.S2.M2 | (madre H11.S2.M2) Prueba: el reintento tras el refresco de sesión conserva la **misma** clave | Las dos peticiones llevan la misma cabecera | la prueba → PASS | TODO |
| H3.S2.M3 | (madre H11.S2.M3) Inventariar los formularios con efecto y si deshabilitan el botón mientras la operación está en curso | Tabla formulario → deshabilita sí o no | el barrido → tabla en `entregables/` | TODO |
| H3.S2.M4 | (madre H11.S2.M4) Escenario: doble clic en un formulario de dinero manda una sola petición con una sola clave | El contador de peticiones queda en uno | el escenario → passed | TODO |
| H3.S2.M5 | (madre H11.S2.M5) Escenario: recargar y reabrir el formulario genera clave nueva; ir y volver en el historial conserva la misma | Las dos aserciones pasan | los dos escenarios → passed | TODO |
| H3.S2.M6 | (madre H11.S2.M6) Escenario: vencimiento con respuesta desconocida, la interfaz ofrece reintentar y el reintento lleva la misma clave | Las dos peticiones con la misma clave | el escenario → passed | TODO |
| H3.S2.M7 | (madre H11.S2.M7) Revisar la prueba de integración de doble envío de la app: que verifique la cabecera, no solo el conteo | La prueba comprueba la clave | inspección de la prueba → la cabecera aparece en las aserciones | TODO |

#### H3.S3 — Los clientes generados como frontera contractual

**CA:** Dado el código de dominio de las tres apps, cuando se inventarían los tipos y rutas escritos a mano, entonces ninguno duplica un modelo o una operación del cliente generado sin justificación, y generar dos veces produce exactamente lo mismo.
**DoD:** el inventario en cero o justificado, la comparación de dos generaciones vacía, y las pruebas de contrato en verde en los dos lenguajes.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | (madre H11.S3.M1) Inventariar los tipos y enumeraciones escritos a mano que coincidan con modelos generados | Tabla tipo manual → tipo generado → acción | el inventario → `evidencia/H3-S3-M1.txt` | TODO |
| H3.S3.M2 | (madre H11.S3.M2) Reemplazar los duplicados por el tipo generado; los que no tengan equivalente quedan con la nota de que no hay contrato | El proyecto typechequea y no quedan duplicados sin justificar | `yarn typecheck; echo $?` → 0 | TODO |
| H3.S3.M3 | (madre H11.S3.M3) Revisar las rutas escritas a mano fuera de la infraestructura: cada una migra al método del cliente o se justifica | La lista queda en cero o con su justificación | el barrido → pegado | TODO |
| H3.S3.M4 | (madre H11.S3.M4) Comprobar el determinismo: generar dos veces y comparar; sin diferencias | La comparación no arroja diferencias | la comparación → termina bien, pegado | TODO |
| H3.S3.M5 | (madre H11.S3.M5) Pruebas de contrato del lado consumidor en la web: validar los ejemplos del simulado contra los tipos generados para tres operaciones críticas | Tres pruebas en verde | las pruebas → passed | TODO |
| H3.S3.M6 | (madre H11.S3.M6) Pruebas de contrato en la app: pasar de una a cuatro, usando los mismos ejemplos | Cuatro o más en verde | `flutter test test/contrato` → passed | TODO |
| H3.S3.M7 | (madre H11.S3.M7) Registrar los hallazgos de autorización, idempotencia y contratos como corregidos, con un commit por tema | Las tres entradas completas | `git log --oneline -3` → los tres commits | TODO |

### H4 — Un solo árbol, un remoto canónico, y el espejo sincronizado (madre H13, decisión D-A2)

**CA:** Dado quien lee la arquitectura objetivo y el ADR de fronteras, entonces encuentra los hechos medidos, la alternativa descartada con su motivo, la decisión tomada, y los dos remotos apuntando al mismo commit; el archivado del remoto espejo queda escrito para que lo ejecute su dueño, no ejecutado.
**DoD:** la sección y el ADR escritos, los dos remotos en el mismo commit, y el script de verificación con sus dos salidas.
**Estado:** TODO

#### H4.S1 — Los hechos, la decisión y la sincronización

**CA:** Dado el acoplamiento medido, cuando se lee la recomendación, entonces está justificada con números del propio código, no con preferencia.
**DoD:** los números pegados, el ADR aceptado y la comparación de remotos coincidiendo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | (madre H13.S1.M1) Medir cuántos archivos del frontend dependen de los clientes generados y cuántos pasos del CI del frontend dependen del entorno de Java | Los dos números quedan pegados | los dos barridos → pegados | TODO |
| H4.S1.M2 | (madre H13.S1.M2) Registrar la divergencia actual entre los dos remotos, en las dos direcciones | La lista de commits de cada lado queda pegada | la comparación → `evidencia/H4-S1-M2.txt` | TODO |
| H4.S1.M3 | (madre H13.S1.M3) Escribir las dos alternativas con sus costos y la decisión tomada, justificada con los números de M1 | La sección tiene el criterio explícito y la decisión | `grep -c "Decisión" docs/auditoria/arquitectura-objetivo.md` → uno o más | TODO |
| H4.S1.M4 | (madre H13.S1.M4) Escribir el ADR de fronteras de repositorio en estado aceptado, con los comandos de archivado marcados como **no ejecutados** | El ADR existe y el remoto espejo sigue sin archivar | el ADR existe · la consulta del repositorio → no archivado | TODO |
| H4.S1.M5 | (madre H13.S1.M5) Escribir el script que compara la rama de trabajo de los dos remotos y falla si difieren | Falla hoy y termina bien después de sincronizar | las dos salidas con su código pegadas | TODO |
| H4.S1.M6 | (madre H13.S1.M6) Sincronizar el espejo con un avance directo, sin forzar, y configurar el clon para que cada envío llegue a los dos | Los dos remotos muestran el mismo commit y el envío no fue forzado | la comparación de referencias remotas → el mismo identificador en ambos | TODO |

### H5 — El cierre: todo corrido, todo revisado, y un informe con hechos (madre H14)

**CA:** Dado el estado final de la rama, cuando se corre el pipeline completo más los gates nuevos, entonces todo está en verde con su salida pegada o declarado bloqueado con su causa; una segunda pasada que no confía en la primera solución y una tercera enfocada solo en seguridad no dejan nada sin veredicto; y el informe final responde, con hechos, qué partes del frontend son confiables y cuáles siguen bloqueadas.
**DoD:** los ocho documentos completos, el CI del canónico en verde, y el reporte con las tres secciones y el avance calculado en la primera línea.
**Estado:** TODO

#### H5.S1 — La corrida completa

**CA:** Dado el SHA final, cuando se corre todo en serie, entonces cada comando termina bien o su fallo queda declarado con causa.
**DoD:** la tabla comando → código de salida completa y el CI en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | (madre H14.S1.M1) Repetir en serie todos los comandos del pipeline sobre el SHA final, con sus salidas en evidencia | Cada comando con su código, sin excepción no declarada | la tabla en el informe de verificación final | TODO |
| H5.S1.M2 | (madre H14.S1.M2) Correr todos los escenarios del backoffice, los existentes y los que sumaron los cinco carriles, con un solo trabajador | Cero fallidos | los escenarios → salida pegada | TODO |
| H5.S1.M3 | (madre H14.S1.M3) Demostrar los dos kill-tests del plan madre: el refresco único y el humo que falla cuando debe | Los dos demostrados con su salida | las dos salidas en el informe | TODO |
| H5.S1.M4 | (madre H14.S1.M4) Demostrar que una configuración de producción incompleta falla en las tres apps | Tres fallos controlados pegados | las tres salidas en el informe | TODO |
| H5.S1.M5 | (madre H14.S1.M5) Enviar al remoto canónico, sincronizar el espejo y observar la corrida hasta el final | Todos los jobs en verde y los dos remotos iguales | la conclusión de la corrida → exitosa · el script de remotos → termina bien | TODO |

#### H5.S2 — La revisión que no se cree la primera solución

**CA:** Dado el cambio completo del turno, cuando lo revisa un segundo rol y después un tercero enfocado solo en seguridad, entonces cada categoría tiene veredicto con evidencia y lo encontrado está corregido o declarado.
**DoD:** las dos tablas de veredictos y los hallazgos nuevos cerrados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S2.M1 | (madre H14.S2.M1) Segunda pasada sobre el cambio completo buscando atajos, pruebas débiles, carreras, suscripciones sin ciclo de vida, peticiones duplicadas, bucles de sesión, estados imposibles, código muerto, datos de ejemplo en producción, imports internos y configuración ambigua | Las doce categorías con hallazgo o con "ninguno" | la tabla de doce categorías en el informe | TODO |
| H5.S2.M2 | (madre H14.S2.M2) Corregir cada hallazgo nuevo como microtarea agregada al plan antes de tocarlo | Ninguno queda en curso al cerrar | el contador de estados → sin microtareas en curso | TODO |
| H5.S2.M3 | (madre H14.S2.M3) Tercera pasada solo de seguridad, con la lista de riesgos vigente aplicada al frontend | Cada categoría con control, archivo y estado | la tabla de diez filas en el informe | TODO |
| H5.S2.M4 | (madre H14.S2.M4) Barrido final de prohibiciones: tipos permisivos nuevos, supresiones de lint sin justificar, tokens en almacenamiento del navegador, continuaciones ante error en gates y pruebas exclusivas o salteadas | Todos en cero o justificados en la misma línea | los conteos pegados en el informe | TODO |

#### H5.S3 — Los documentos y el cierre

**CA:** Dado alguien que no vio el turno, cuando lee el informe final, entonces sabe qué quedó confiable, qué bloqueado y por qué, con el avance calculado y sin tener que preguntar nada.
**DoD:** los ocho documentos completos, el reporte escrito y ningún proceso corriendo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S3.M1 | (madre H14.S3.M1) Escribir los riesgos residuales con impacto, mitigación y dueño, incluyendo todo lo que quedó bloqueado | Cada riesgo con dueño | `grep -c "^## R-" docs/auditoria/riesgos.md` → seis o más | TODO |
| H5.S3.M2 | (madre H14.S3.M2) Escribir el informe de verificación final con su estructura completa y la respuesta por área: confiable, bloqueado y por qué | Ocho áreas con veredicto y evidencia enlazada | la tabla del informe → ocho filas | TODO |
| H5.S3.M3 | (madre H14.S3.M3) Consolidar los hallazgos de los cinco carriles: ninguno queda sin estado y el conteo de la cabecera coincide con el real | El conteo declarado coincide con el contado | el conteo por estado → igual al declarado | TODO |
| H5.S3.M4 | (madre H14.S3.M4) Escribir el reporte del trabajo con las tres secciones y el avance calculado en la primera línea | El candado de reporte no bloquea | la autoprueba del candado → termina bien y el reporte tiene las tres secciones | TODO |
| H5.S3.M5 | (madre H14.S3.M5) Commit final, envío, corrida en verde y nada corriendo en la máquina | Ningún puerto de desarrollo escuchando al terminar | la consulta de puertos → vacía, pegada en el daily | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-P1 | ¿Versionar los clientes generados contradice el ADR vigente de artefactos generados? | Vos mismo, con la enmienda escrita | Nada: es la decisión D-A1 ya tomada | Se enmienda el ADR en la misma microtarea en que se cambia el comportamiento; nunca se cambia el comportamiento dejando el ADR mintiendo |
| Q-P2 | ¿Cuándo se archiva el remoto espejo? | Vos, como dueño de la cuenta | Nada del turno | Se sincroniza y se deja escrito el comando; archivar es acción sobre algo compartido y se ejecuta fuera del turno |
| Q-P3 | ¿El endpoint de registro de accesos existe en algún contrato? | El descubrimiento de H2.S2.M3 | El carril de Richard | No existe hasta que se demuestre; se entrega el resultado a Richard apenas se sepa, no al final del turno |
| Q-P4 | ¿Los ejemplos del simulado alcanzan para probar contratos, o hay que extenderlos? | Verificable al escribir las pruebas | Las pruebas de contrato de H3.S3 | Alcanzan; si falta un ejemplo, se extiende el simulado (es su propósito) y **no** se inventa una respuesta que el contrato no declara |
| Q-P5 | ¿La revisión de la segunda pasada la hace otra persona o vos mismo con otro rol? | Coordinación | Nada, pero cambia el valor de la revisión | La hace un rol independiente del que escribió el código de cada carril; delegar la verificación a quien hizo el trabajo no cuenta como revisión independiente (regla 70.4.8) |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` del trabajo escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin datos de personas ni identificadores en las
      URLs pegadas (regla 90.2: si una salida los tenía, se enmascara **y se aclara**).
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `authz-access-control` por la
      matriz de autorización; `money-movement-safety` por los formularios de dinero de la prueba de
      idempotencia; `secure-code-review` por la tercera pasada.
- [ ] Peldaño de evidencia declarado **por área** (regla 30), y el del trabajo es el **más bajo**
      de sus áreas en alcance: no se promedia ni se redondea hacia arriba.
- [ ] El informe final no usa una palabra de finalización más fuerte que la evidencia pegada, y lo
      que quedó sin cubrir aparece **arriba**, no enterrado en un anexo.
