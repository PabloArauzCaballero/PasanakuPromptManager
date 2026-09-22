# Fronteras que se hacen cumplir solas: exports explícitos, un núcleo compartido y un proxy que deja de ser accidental

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** Marcelo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Bloque:** **C — AportaYa** (el bloque B, `PR9-InventarioYFamilias.Frontend`, **es el mismo repo
  desde la corrección del 2026-09-21**: antes decía `mantra-core-health`, ya es Pasanaku). **Un
  trabajo activo por vez** (regla 70.1): A backend → B inventario → C este.
- **Repo:** el monorepo de AportaYa — `https://github.com/PabloArauzCaballero/PasanakuBackend.git` (canónico por D-A2) · rama base `dev` @ `19a621e666afdea5bdc40aced326d3f212a116f4` · **tu rama:** `marcelo/frontend/fronteras`
- **Plan madre:** [`docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md`](../../../../../../docs/trabajo/2026-09-21-frontend-rescate-hardening/PLAN.md) v2 · te tocan **H9, H10 y H12** (salvo H12.S4, que es de Justin)
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md)
- **5 hitos · 13 subtareas · 59 microtareas**

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
| `component-architecture-solid` | Las capas, quién puede depender de quién y por qué |
| `atomic-design-components` | La API pública de un package de interfaz y qué no se expone |
| `static-analysis-linting` | Convertir invariantes en reglas que fallan solas, en vez de barridos por texto |
| `dead-code-duplication` | Detectar la duplicación real y decidir qué se extrae y qué no |
| `refactoring-safely` | Tests de caracterización antes de mover una línea |
| `error-handling-contract` | Las categorías de error y qué nunca se le muestra a una persona |
| `backend-observability` | Qué se registra, con qué correlación y qué jamás entra en un registro |
| `frontend-error-monitoring` | El puerto de telemetría y por qué el dominio no conoce al proveedor |
| `api-gateway-bff` | Si el servidor de render es un intermediario, qué responsabilidades asume |
| `resilience-patterns` | Tiempos de espera, límites y degradación declarada del reenvío |
| `typescript-standards` | Una sola versión del compilador, o el motivo escrito de dos |
| `evidence-and-verification` | El peldaño que podés declarar con la evidencia que tengas |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · **90.2** (nada de datos de personas en registros) · **95** (reutilizar antes que crear, tokens en vez de literales) · **96.4** (contratos y compatibilidad)

> **Corrección 2026-09-21:** el bloque B (`PR9`) dejó de ser `mantra-core-health`, pero sus reglas
> siguen distintas de las de acá: 91 no le aplica (es un inventario, no muta componentes de
> producto) y 98 tampoco. Acá, en el bloque C, las dos **siempre** aplican.
> El reenvío que vas a revisar es por donde pasan las peticiones de dinero del sitio.

## 2. Resultado observable

Un import a las entrañas de un package deja de compilar, una pantalla que intenta hacer red falla
el lint, la traza y los errores existen **una** vez en lugar de dos, el servidor del sitio dice qué
es —intermediario con tiempos de espera y límites, o solo render— y ningún error del backend llega
crudo a la pantalla de una persona.

**Kill-test:** agregar un import a un archivo interno de un package de interfaz y compilar. Hoy
funciona: `packages/ui/package.json` expone `"./*": "./src/*"` y el mapeo de rutas del compilador
apunta a todo `src/*`, así que **todo** es API pública. Si al cerrar sigue compilando, esto NO está
hecho. Segundo kill-test: comparar los interceptores de traza de las dos apps. Hoy el archivo es
idéntico en las dos, y el de errores también: dos copias de la misma infraestructura esperando
divergir.

## 3. Alcance

**IN:**
- `packages/{ui,tutoriales}/package.json` (sus `exports`), el package nuevo de núcleo HTTP
  compartido y su `package.json`, y `tsconfig.base.json`.
- `apps/web/eslint.config.js` y `apps/backoffice/eslint.config.js`.
- `apps/movil/test/arquitectura/**` y `apps/movil/analysis_options.yaml`.
- `scripts/verificar_frontend.py`.
- `apps/web/src/server.ts` y `apps/web/src/app/app.routes.ts`.
- Los interceptores de traza y errores de las dos apps (los movés al package y borrás las copias).
- El formateador de dinero y el módulo de fechas compartidos, y sus vectores.

**OUT:** `nucleo/sesion*`, `permisos.ts`, `registro-de-acceso*` y `app.config.ts` (Richard),
`gateway.ts` y `rutas/sistemas/**` (Justin), `.github/workflows/**`, `apps/movil/lib/infraestructura/**`
y `despliegue/nginx/**` (Leo), `clientes/**` y `docs/auditoria/**` (Pablo). Tampoco cambiás el
contrato público de un package sin registrar la decisión.

**Reservas de archivos:** las ocho rutas del IN son tuyas. Cuando muevas la traza y los errores al
package, avisás a Richard y Justin en el daily: sus imports cambian, y la migración de esos imports
es **microtarea tuya**, no de ellos.

## 4. Plan

### H1 — La línea base de tu carril es un hecho registrado

**CA:** Dado el SHA de arranque, cuando alguien lee tu daily, entonces sabe qué expone hoy cada package, cuánta duplicación real hay y qué dice el lint, sin haberlo corrido él.
**DoD:** las cinco salidas pegadas en `evidencia/` con su `exit=`.
**Estado:** TODO

#### H1.S1 — Entorno, SHA y el estado real de las fronteras

**CA:** Dado tu clon, cuando inventariás exports, duplicación y reglas de lint vigentes, entonces el resultado queda registrado tal cual es.
**DoD:** `evidencia/H1-S1-*.txt` con las salidas literales.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar el SHA de arranque y crear `marcelo/frontend/fronteras` desde `dev` | La rama existe sobre el SHA declarado | `git rev-parse HEAD` pegado en el daily; `git branch --show-current` → `marcelo/frontend/fronteras` | TODO |
| H1.S1.M2 | Instalar el estándar y verificarlo (sección 1) | Las dos salidas pegadas en el daily | `python .claude/hooks/plan_gate.py --self-test; echo exit=$?` → `0` | TODO |
| H1.S1.M3 | Inventariar qué expone hoy cada package y qué mapea el compilador (el kill-test, antes de tocar nada) | La tabla package → entradas expuestas queda registrada | `node -e` sobre cada `package.json` y `grep -A12 '"paths"' tsconfig.base.json` → `evidencia/H1-S1-M3.txt` | TODO |
| H1.S1.M4 | Medir la duplicación real entre las dos apps: comparar los archivos de traza, errores y sus interceptores | El resultado de cada comparación queda registrado | comparaciones → `evidencia/H1-S1-M4.txt` con las diferencias y las coincidencias | TODO |
| H1.S1.M5 | Correr `yarn lint` completo y registrar qué reglas están activas hoy en cada app y qué reporta | La salida queda registrada con su código | `yarn lint; echo exit=$?` → pegado | TODO |

### H2 — Un import a las entrañas de un package deja de compilar (madre H9.S1)

**CA:** Dado un package de interfaz, cuando alguien importa un archivo que no está en su API pública, entonces el compilador falla; y cada package declara explícitamente qué expone.
**DoD:** los `exports` sin comodín, el mapeo del compilador acotado, `yarn typecheck` en verde, y el import prohibido de prueba fallando con su salida pegada.
**Estado:** TODO

#### H2.S1 — Exports explícitos por package

**CA:** Dados los packages de interfaz y tutoriales, cuando una app importa, entonces solo resuelve entradas declaradas.
**DoD:** `yarn typecheck` verde con el mapeo acotado y el error del import prohibido pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | (madre H9.S1.M1) Inventariar qué módulos de los dos packages importan hoy las apps | Tabla módulo → consumidores | barrido de imports → `entregables/api-publica-actual.md` | TODO |
| H2.S1.M2 | (madre H9.S1.M2) Declarar en el package de interfaz una entrada por módulo público usado y quitar el comodín | Solo los módulos de la tabla quedan expuestos | inspección del `package.json` → sin la entrada comodín | TODO |
| H2.S1.M3 | (madre H9.S1.M3) Lo mismo en el package de tutoriales | Sin comodín | misma inspección | TODO |
| H2.S1.M4 | (madre H9.S1.M4) Acotar el mapeo de rutas del compilador para que coincida con lo expuesto | El proyecto entero typechequea | `yarn typecheck; echo $?` → 0 | TODO |
| H2.S1.M5 | (madre H9.S1.M5) Test negativo: un import a un archivo interno deja de compilar; se retira después | El error del compilador queda pegado | `evidencia/H2-S1-M5.txt` con el error | TODO |
| H2.S1.M6 | (madre H9.S1.M6) Escribir en `entregables/` la API pública de cada package con su propósito y la regla de cuándo se crea uno nuevo | Una sección por package | `grep -c "^### @aportaya/" entregables/api-publica.md` → 6 | TODO |

### H3 — Las capas se hacen cumplir solas, no por barrido de texto (madre H9.S2, H9.S3, H9.S4)

**CA:** Dado un archivo de presentación que intenta hacer red, o un archivo de dominio que importa el framework, cuando corre el lint o las pruebas de arquitectura, entonces falla nombrando la regla; y el barrido por texto queda reducido a lo que esas reglas todavía no cubren, con la lista escrita.
**DoD:** tres imports prohibidos de prueba fallando con su salida pegada; `yarn lint` en verde; las pruebas de arquitectura de la app en verde con sus casos negativos.
**Estado:** TODO

#### H3.S1 — Fronteras de capa en las apps web

**CA:** Dada la configuración de lint, cuando un archivo de pantalla importa infraestructura o cliente HTTP, entonces el lint falla con la regla de fronteras.
**DoD:** los tres casos prohibidos con su error pegado y el lint en verde después.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | (madre H9.S2.M1) Verificar la API real del plugin de fronteras ya instalado **antes** de escribir la configuración, contra la documentación de la versión presente | La versión y la forma de la configuración quedan citadas | `yarn why` del plugin → versión pegada en `entregables/decision-fronteras.md` | TODO |
| H3.S1.M2 | (madre H9.S2.M2) Declarar los elementos por carpeta en el backoffice: infraestructura, dominio de ruta, presentación y contrato | La configuración carga y el lint arranca | `yarn workspace @aportaya/backoffice lint; echo $?` → 0, o la lista de violaciones reales a corregir | TODO |
| H3.S1.M3 | (madre H9.S2.M3) Declarar las reglas de dependencia permitida entre esos elementos | Tres imports prohibidos de prueba fallan | `evidencia/H3-S1-M3.txt` con los tres errores de la regla | TODO |
| H3.S1.M4 | (madre H9.S2.M4) Corregir las violaciones reales que aparezcan, agregando cada una al plan como microtarea antes de tocarla | Cero violaciones al terminar | `yarn workspace @aportaya/backoffice lint` → 0 problemas | TODO |
| H3.S1.M5 | (madre H9.S2.M5) Misma configuración en el sitio, con sus propios elementos | El lint del sitio termina sin problemas | `yarn workspace @aportaya/web lint` → 0 problemas | TODO |
| H3.S1.M6 | (madre H9.S2.M6) Restringir el import de los clientes generados fuera del dominio y la infraestructura | Un import desde una pantalla falla | caso negativo → error pegado | TODO |

#### H3.S2 — Fronteras de capa en la app, con análisis real

**CA:** Dada la app, cuando una pantalla importa el cliente HTTP o el almacén seguro, o el dominio importa el framework de interfaz, entonces la prueba de arquitectura falla nombrando el archivo.
**DoD:** la prueba en verde sobre el árbol real y detectando las tres violaciones sintéticas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | (madre H9.S3.M1) Verificar si el analizador está disponible en el SDK instalado antes de usarlo; si hace falta declararlo, justificarlo | La decisión queda escrita con la versión | `dart pub deps` → pegado en la decisión | TODO |
| H3.S2.M2 | (madre H9.S3.M2) Escribir la prueba de arquitectura que recorre el código, parsea los imports y aplica la matriz de capas | El árbol real pasa | `flutter test test/arquitectura` → passed | TODO |
| H3.S2.M3 | (madre H9.S3.M3) Fixtures negativas: pantalla con cliente HTTP, dominio con framework de interfaz, y consulta de plataforma fuera de infraestructura | La prueba detecta las tres | `flutter test test/arquitectura/fixtures_test.dart` → passed | TODO |
| H3.S2.M4 | (madre H9.S3.M4) Incluir la carpeta de arquitectura en la tarea de pruebas de la app | Corre con las demás | inspección del `package.json` de la app → la carpeta listada | TODO |

#### H3.S3 — El barrido por texto, reducido a lo complementario

**CA:** Dado el script de barrido, cuando se lo compara con las reglas nuevas, entonces cada regla redundante fue eliminada con la referencia a lo que la reemplaza, y quedan solo las complementarias.
**DoD:** la tabla de reemplazos escrita, el script más corto y su autoprueba en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S3.M1 | (madre H9.S4.M1) Escribir la tabla regla por texto → reemplazo → estado (reemplazada o complementaria) | Una fila por barrido existente | `entregables/barridos-reemplazados.md` con 15 filas o más | TODO |
| H3.S3.M2 | (madre H9.S4.M2) Mover la prohibición de registros por consola a la regla de lint correspondiente, y la de impresión en la app a sus opciones de análisis | Una violación sintética falla en cada lenguaje | `evidencia/H3-S3-M2.txt` con los dos errores provocados | TODO |
| H3.S3.M3 | (madre H9.S4.M3) Quitar del script los barridos reemplazados y dejar su autoprueba ejercitando los complementarios | La autoprueba termina bien | `python3 scripts/verificar_frontend.py --self-test; echo $?` → 0 | TODO |
| H3.S3.M4 | (madre H9.S4.M4) Registrar los hallazgos de fronteras, exports y barridos como corregidos y commitear `refactor(boundaries): fronteras de packages y capas con enforcement` | Las tres entradas completas | `git log --oneline -1` → el commit | TODO |

### H4 — La infraestructura compartida existe una vez, y el servidor dice qué es (madre H10)

**CA:** Dado el núcleo HTTP de las dos apps web, cuando se compara, entonces traza, errores y configuración viven una sola vez en un package con API explícita; el servidor del sitio o es un intermediario con tiempos de espera, límites, saneo de cabeceras y pruebas, o dejó de reenviar; ningún error crudo del backend llega a una pantalla; y existe un puerto de telemetría que el dominio no conoce por proveedor.
**DoD:** los archivos duplicados eliminados de las dos apps, las pruebas del package y del servidor en verde, y las categorías de error cubiertas en los dos lenguajes.
**Estado:** TODO

#### H4.S1 — El package de núcleo HTTP

**CA:** Dado el package nuevo, cuando las apps lo consumen, entonces ninguna conserva su copia local de traza, errores o configuración.
**DoD:** los archivos borrados de las dos apps y el proyecto typechequeando.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | (madre H10.S1.M1) Crear el package con su API explícita y mover la traza tal cual, con su prueba de caracterización | La prueba pasa y las dos apps lo importan | `yarn workspace @aportaya/http-nucleo test:front` → passed · los archivos locales ya no existen | TODO |
| H4.S1.M2 | (madre H10.S1.M2) Mover el interceptor de errores y el catálogo base; el backoffice extiende el catálogo con sus códigos propios en vez de duplicarlo | El catálogo extendido resuelve un código propio del backoffice | prueba del catálogo extendido → PASS | TODO |
| H4.S1.M3 | (madre H10.S1.M3) Mover la resolución del gateway y la validación de configuración al package, coordinando con Justin el punto de entrada | Ninguna app conserva su función local | barrido de la función antigua en las apps → 0 | TODO |
| H4.S1.M4 | (madre H10.S1.M4) Escribir el criterio de qué se comparte y qué no, nombrando explícitamente lo que **no** se extrajo y por qué | La sección nombra sesión, idempotencia y registro de acceso como no extraídos | `grep -c "no se extrajo" entregables/que-se-comparte.md` → ≥ 1 | TODO |

#### H4.S2 — El servidor del sitio: intermediario declarado o solo render

**CA:** Dado el servidor del sitio, cuando recibe una petición hacia la API, entonces la reenvía con tiempo de espera, límite de cuerpo, cabeceras salto a salto removidas y registro estructurado sin contenido sensible; o no la reenvía en absoluto y el enrutamiento lo hace la capa de despliegue.
**DoD:** la decisión registrada como ADR y, según el camino elegido, las pruebas del reenvío en verde o el reenvío eliminado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | (madre H10.S2.M1) Escribir el ADR con la decisión, usando lo que Pablo descubra sobre cómo enruta hoy el despliegue | El ADR tiene contexto, decisión y consecuencias | el archivo del ADR existe | TODO |
| H4.S2.M2 | (madre H10.S2.M2) Si sigue reenviando: tiempo de espera explícito y traducción del vencimiento a una respuesta de error del contrato | Con un destino que no responde, contesta el error en menos del doble del tiempo de espera | prueba dirigida → passed | TODO |
| H4.S2.M3 | (madre H10.S2.M3) Lista completa de cabeceras salto a salto removidas, y no reenviar credenciales de sesión salvo lista declarada | Prueba de cabeceras filtradas | prueba → passed | TODO |
| H4.S2.M4 | (madre H10.S2.M4) Límite de cuerpo con su respuesta de error, y redirecciones que no se reenvían crudas | Las dos pruebas pasan | pruebas → passed | TODO |
| H4.S2.M5 | (madre H10.S2.M5) Identificador de correlación generado si falta y registro estructurado sin consulta ni cuerpo; reemplazar el registro por consola que quedó de la plantilla | El registro no contiene la cadena de consulta | prueba → passed · barrido de registros por consola en el servidor → 0 | TODO |
| H4.S2.M6 | (madre H10.S2.M6) Si se decide no reenviar: eliminar el bloque y documentar el enrutamiento en la capa de despliegue, coordinando con Leo | El servidor ya no hace peticiones salientes | barrido de la llamada saliente en el servidor → 0 | TODO |
| H4.S2.M7 | (madre H10.S2.M7) Quitar los comentarios de plantilla del generador y dejar solo lo que explica una invariante | Sin los comentarios de ejemplo del andamiaje | barrido de la cadena de ejemplo → 0 | TODO |

#### H4.S3 — Errores por categoría, sin fugas

**CA:** Dado cualquier error de red o de API, cuando llega a la interfaz, entonces está clasificado en una de las diez categorías, conserva su código y su correlación, y el texto mostrado sale del catálogo.
**DoD:** las pruebas de clasificación en los dos lenguajes y el barrido de fugas en cero.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S3.M1 | (madre H10.S3.M1) Función de clasificación con las diez categorías, más red y vencimiento, conservando código y correlación | Doce casos cubiertos | prueba → 12 passed | TODO |
| H4.S3.M2 | (madre H10.S3.M2) El interceptor entrega el error ya clasificado a las pantallas; las que lo requieran se adaptan, cada una como microtarea propia si excede el cambio de tipo | El proyecto typechequea y los escenarios existentes siguen en verde | `yarn typecheck` y los escenarios del backoffice → 0 failed | TODO |
| H4.S3.M3 | (madre H10.S3.M3) Misma clasificación en la app, con el mismo conjunto de categorías | Doce casos en verde | `flutter test test/unidad/errores_test.dart` → passed | TODO |
| H4.S3.M4 | (madre H10.S3.M4) Prueba de fuga: ninguna plantilla muestra el mensaje crudo del error | El barrido da cero | barrido sobre plantillas y pantallas → 0 | TODO |

#### H4.S4 — El puerto de telemetría

**CA:** Dado un error inesperado o una respuesta de servidor fallida, cuando ocurre, entonces se emite un evento con ruta, versión, correlación, entorno y categoría, sin ningún dato de persona, a un puerto cuya implementación por defecto no depende de ningún proveedor.
**DoD:** las pruebas del puerto, del manejador global y del saneo, en los dos lenguajes.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S4.M1 | (madre H10.S4.M1) Definir el puerto de telemetría y sus dos implementaciones, nula y por consola | Las dos con su prueba | prueba del package → passed | TODO |
| H4.S4.M2 | (madre H10.S4.M2) Manejador global de errores que clasifica y emite con ruta, versión y correlación | Emite una vez por error con la forma esperada | prueba → PASS | TODO |
| H4.S4.M3 | (madre H10.S4.M3) Filtro que elimina claves prohibidas y recorta cadenas largas, con una prueba de carga envenenada | Cero claves prohibidas en la salida | prueba → PASS | TODO |
| H4.S4.M4 | (madre H10.S4.M4) Puerto equivalente en la app, con la captura de errores no atrapados y el mismo saneo | La prueba del saneo en la app pasa | `flutter test test/unidad/telemetria_test.dart` → passed | TODO |
| H4.S4.M5 | (madre H10.S4.M5) Registrar los hallazgos de duplicación, reenvío y errores como corregidos, con un commit por tema | Las tres entradas completas y tres commits separados | `git log --oneline -3` → los tres commits | TODO |

### H5 — Dinero, fechas, rutas y herramientas dejan de ser una fuente de sorpresas (madre H12, salvo S4)

**CA:** Dado el frontend, cuando se audita, entonces todo importe pasa por el formateador único con sus bordes cubiertos, toda fecha se parsea con formato y zona explícitos, el archivo de rutas del sitio solo declara navegación, y hay una sola versión del compilador declarada o el motivo escrito de que haya dos.
**DoD:** los vectores de dinero y fechas en verde en los dos lenguajes; el archivo de rutas por debajo del tamaño acordado; la comprobación de versiones sin duplicados.
**Estado:** TODO

#### H5.S1 — Dinero: los bordes también

**CA:** Dado cualquier importe mostrado, cuando pasa por el formateador, entonces cero, negativos, valores grandes y el redondeo dan la misma salida en las dos plataformas, contra el mismo archivo de vectores.
**DoD:** los vectores ampliados en verde en los dos lenguajes y la regla estática activa.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | (madre H12.S1.M1) Ampliar los vectores con cero, negativo, valor grande, media unidad y otra moneda, y documentar el modo de redondeo | Cada vector con su salida esperada y el modo escrito | prueba del package de tokens → passed | TODO |
| H5.S1.M2 | (madre H12.S1.M2) Los mismos vectores en la app, contra el mismo archivo | Cero divergencias entre plataformas | `flutter test test/unidad/dinero_vectores_test.dart` → passed | TODO |
| H5.S1.M3 | (madre H12.S1.M3) Revisar el único parseo numérico permitido de la app: si el valor se usa después en un cálculo, pasa a decimal exacto; si solo valida forma, queda y se documenta | La decisión cita el uso real | el uso encontrado → pegado en la decisión | TODO |
| H5.S1.M4 | (madre H12.S1.M4) Regla estática que prohíbe formatear o parsear importes fuera del módulo autorizado | Una violación sintética falla | `evidencia/H5-S1-M4.txt` con el error provocado | TODO |

#### H5.S2 — Fechas con zona explícita

**CA:** Dada una fecha del contrato, cuando se la parsea o se la muestra, entonces se usa formato estricto y zona declarada, y ningún parseo ambiguo queda fuera del módulo de fechas.
**DoD:** los vectores en verde en los dos lenguajes y el barrido de parseos ambiguos en cero.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S2.M1 | (madre H12.S2.M1) Inventariar los parseos y formateos de fecha con su propósito | Tabla archivo:línea → propósito | barrido → `evidencia/H5-S2-M1.txt` | TODO |
| H5.S2.M2 | (madre H12.S2.M2) Módulo único de fechas en los dos lenguajes, con vectores compartidos que incluyan el cambio de día entre zonas | Los vectores pasan en los dos | ambas pruebas → passed | TODO |
| H5.S2.M3 | (madre H12.S2.M3) Migrar los usos del inventario y prohibir el parseo ambiguo con una regla estática | El barrido queda en cero fuera del módulo | mismo barrido → 0 | TODO |

#### H5.S3 — Rutas que solo declaran navegación

**CA:** Dado el archivo de rutas del sitio, cuando se lo lee, entonces solo declara navegación; los textos y metadatos viven en un catálogo tipado y el contenido regulatorio lleva versión, vigencia y fuente.
**DoD:** el archivo por debajo del tamaño acordado, los escenarios del sitio en verde y el generador de contenido fallando ante una ficha sin fuente.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S3.M1 | (madre H12.S3.M1) Mover los bloques de metadatos y datos estructurados a un catálogo tipado, dejando en las rutas solo la referencia | El archivo de rutas queda por debajo de 80 líneas y los escenarios del sitio siguen en verde | `wc -l` del archivo → < 80 · escenarios del sitio → passed | TODO |
| H5.S3.M2 | (madre H12.S3.M2) Inventariar los contenidos regulatorios y anotar versión, vigencia y fuente; los que no tengan fuente quedan marcados como decisión pendiente de cumplimiento | La lista de faltantes queda registrada, sin inventar ninguna fuente | barrido de fichas sin fuente → lista pegada | TODO |
| H5.S3.M3 | (madre H12.S3.M3) El generador de contenido falla si una ficha regulatoria no tiene fuente y vigencia | Con una ficha de prueba sin fuente el generador falla; sin ella, termina bien | los dos códigos de salida pegados | TODO |

#### H5.S4 — Comentarios y herramientas

**CA:** Dado el código y su configuración, cuando se los lee, entonces los comentarios explican qué invariante existe y por qué importa, la historia vive en las decisiones, y hay una sola versión del compilador o el motivo escrito de que haya dos.
**DoD:** el barrido de comentarios narrativos en cero en los archivos listados y la comprobación de versiones sin duplicados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S4.M1 | (madre H12.S5.M1) Recortar los comentarios narrativos de los archivos de configuración y del servidor, moviendo la historia a las decisiones con su enlace | El barrido de marcas narrativas en esos archivos da cero | barrido → 0 | TODO |
| H5.S4.M2 | (madre H12.S5.M2) Unificar la versión del compilador en los packages que van atrasados, si tipos y pruebas siguen en verde; si no, documentar por qué hay dos | Una sola versión, o el motivo escrito | comprobación de versiones → una entrada, o la decisión escrita | TODO |
| H5.S4.M3 | (madre H12.S5.M3) Confirmar una sola versión del linter y del framework en todo el árbol | La comprobación de duplicados termina bien | comprobación en modo verificación → 0 | TODO |
| H5.S4.M4 | (madre H12.S5.M4) Registrar los hallazgos de calidad como corregidos, con un commit por tema | Las entradas completas y los commits separados | `git log --oneline -3` → los commits | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-M1 | ¿El servidor del sitio debe seguir reenviando hacia la API, o el enrutamiento lo hace la capa de despliegue? | Leo (dueño del despliegue) y lo que Pablo descubra sobre el enrutamiento actual | El camino de H4.S2 (endurecer el reenvío o eliminarlo) | Si el despliegue ya puede enrutar, se elimina el reenvío: un intermediario accidental es peor que ninguno. Se decide con evidencia, no por preferencia |
| Q-M2 | ¿Qué nombre lleva el package de núcleo HTTP compartido? | Coordinación | Nada: es nombre, no diseño | Se registra el nombre elegido en las decisiones antes de crearlo, y no se cambia después para no romper imports de los otros carriles |
| Q-M3 | ¿La versión instalada del plugin de fronteras tiene la forma de configuración que se espera? | Verificable: la documentación de la versión presente | La configuración de H3.S1 | Se verifica **antes** de escribir la configuración (regla 00: prohibido inventar la API de un tercero) |
| Q-M4 | ¿Mover la traza y los errores rompe imports de Richard o de Justin a mitad de su trabajo? | Coordinación, primera hora | Nada, si se avisa | La migración de esos imports es **microtarea tuya**, no de ellos, y se anuncia en el daily antes de hacerla |
| Q-M5 | ¿Subir la versión del compilador en los packages atrasados rompe algo? | Verificable: tipos y pruebas | La unificación de H5.S4.M2 | Se intenta; si rompe, se documenta el motivo de las dos versiones en vez de forzar la unificación |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` del trabajo escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin datos de personas en ninguna salida de registro
      (regla 90.2: si una salida los tenía, se enmascara **y se aclara que se enmascaró**).
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `error-handling-contract` por
      las categorías; `frontend-security` si el servidor sigue reenviando; `data-privacy-financial`
      por el saneo de la telemetría.
- [ ] Peldaño de evidencia declarado por área (regla 30). Mover código no es verificarlo: cada
      package movido vuelve a `WRITTEN` hasta que su prueba corre.
- [ ] Ningún contrato público de package cambiado sin su decisión registrada, y ningún import de
      otro carril roto sin haberlo migrado vos y avisado en el daily.
