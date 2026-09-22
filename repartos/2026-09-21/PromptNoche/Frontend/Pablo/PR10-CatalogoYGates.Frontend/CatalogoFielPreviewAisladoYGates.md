# El catálogo que monta el componente real, el preview aislado de verdad, y los gates que no se pueden falsear

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Pablo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Pablo-Daily-Noche-2026-09-21.md](../Pablo-Daily-Noche-2026-09-21.md)
- **Encargo madre:** prompt maestro de refactorización frontend. Este carril cubre el §12 completo (catálogo fiel, escenarios, aislamiento, ciclo de vida y acreditación), el §16 (verificación) y el §17 (artefactos y trazabilidad), más la fase 5 del §14.
- **Repo:** `https://github.com/mdavila-2001/mantra-core-health` · rama base **`mockup`** @ **el SHA que registres vos en H1.S1.M1** · **tu rama:** `pablo/feature/carril-PR10-catalogo-gates`
- **5 hitos · 11 subtareas · 38 microtareas**

> **Este carril es el más largo del área y también el que cierra.** Está escrito completo y
> ordenado por dependencia a propósito (regla del reparto): lo que no entre en el turno va
> `A MEDIAS` con las cuatro respuestas. **Recortarlo es decisión de coordinación y se registra**,
> no se resuelve borrando microtareas.

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` de este repo estándar dentro de `mantra-core-health/`. Si ese repo
   trae su propio `AGENTS.md` o `CLAUDE.md`, **ese manda sobre estas reglas**: lo que choque se
   registra como ambigüedad, no se resuelve solo.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `visual-proof` | La captura se mira; qué acredita una prueba visual y qué no |
| `visual-regression-testing` | Baseline determinista, sin ampliar tolerancias ni enmascarar la región tocada |
| `accessibility-testing` | Automático más teclado; qué NO detecta la verificación automática |
| `e2e-playwright` | Escenarios aislados, esperas por condición, trace y captura en fallo |
| `frontend-security` | El preview no altera la sesión anfitriona; mensajes y URLs sin datos sensibles |
| `frontend-performance` | Comparar bundle y peticiones contra el baseline, sin presupuestos inventados |
| `synthetic-test-data-generation` | Datos sintéticos por escenario, válidos e inválidos a propósito |
| `qa-evidence-reporting` | Registro de ejecución con comando, commit, exit code y artefactos |
| `code-quality-gates` | Qué bloquea y qué avisa; gates que no se compensan entre sí |
| `work-report-md` | El documento de cierre escrito para alguien que no vio la sesión |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 60 · 65 · **95** (frontend) · 90.2 leída
como dato **clínico e identificatorio** (AMB-F2). **No aplican** la 91 ni la 98.

## 2. Resultado observable

Cada ficha del catálogo **importa la implementación canónica que usa el producto en ese build**,
la monta con sus hijos, directivas, ranuras y proveedores, con contratos válidos, y sus acciones
producen salidas observables; el preview corre en un documento propio, con su propio arranque y
sus propios proveedores, sin tocar la sesión ni los datos del anfitrión; y el cierre del alcance
sale de comandos con exit code pegado, distinguiendo lo verificado aislado, lo verificado
integrado, lo verificado visualmente y lo bloqueado.

**Kill-test:** abrir la ficha de un organismo en el catálogo y comprobar si el nodo montado
proviene del mismo archivo que usa el producto, o de una copia dentro del catálogo. Si es una
recreación parecida, el catálogo miente y esto NO está hecho. Segundo kill-test: iniciar sesión con
una cuenta sintética en el preview y mirar la pestaña del anfitrión. Si la sesión del anfitrión
cambió, no hay aislamiento.

## 3. Alcance

**IN:** el runtime del catálogo de componentes y su ficha; la entrada de preview y su arranque
propio; las factories y hosts tipados de escenario y su esquema; el generador de datos sintéticos
de props; los gates de verificación visual, accesibilidad, consola y red; el registro de ejecución;
y el documento de cierre del refactor.

**OUT:** la pantalla piloto de Richard (PR6). El organismo tabla y sus consumidores (Justin, PR7).
El diálogo, el host de estados y el contrato de borrador (Leo, PR8). El generador del índice, el
grafo de usos y la matriz de familias (Marcelo, PR9). Los tokens del sistema de diseño. El backend
y sus contratos. Ninguna dependencia nueva ni actualizada. `main` y `dev` no se tocan: la promoción
se **recomienda** por escrito, no se ejecuta.

**Reservas de archivos:** el runtime del catálogo y su ficha; la entrada de preview; el generador
de props sintéticas; los archivos de configuración de CI; el documento de cierre y el registro de
ejecución. Lo que encuentres roto en un componente ajeno **se anota como hallazgo con ruta y se le
avisa al dueño del carril; no se arregla**.

### Comandos del repo — candidatos heredados, los confirmás vos y los publicás para los cinco

Sos quien consolida la tabla de comandos del área (AMB-F6): publicala en el daily de equipo §2 en
la primera hora, para que los otros cuatro no la descubran cada uno por su cuenta.

| Alias | Candidato heredado | Cómo se confirma |
|---|---|---|
| `CMD_LINT` | `yarn lint` | `package.json` → `scripts` |
| `CMD_TYPECHECK` | `yarn typecheck` | `package.json` → `scripts` |
| `CMD_TEST` | `yarn test` (Vitest) | `package.json` + config del runner |
| `CMD_COV` | `yarn test:coverage` | `package.json` → `scripts` |
| `CMD_BUILD` | `yarn build` | `package.json` → `scripts` |
| `CMD_E2E` | `yarn pw` (Playwright) | `package.json` + config de Playwright |
| `CMD_STOCK` | `yarn stock:generate` | `package.json` → `scripts` |
| `CMD_VISTAS` | `yarn audit:vistas` | `package.json` → `scripts` |

**Distinguí los comandos que ya existen de los scripts que acabás de escribir**: un comando nuevo
no es evidencia del estado previo del repo. Si un alias no existe, no lo inventes: usá el binario
que el repo ya trae y anotá la diferencia.

### Ritual de entrega

```bash
git fetch origin && git checkout -b pablo/feature/carril-PR10-catalogo-gates origin/mockup
git fetch origin && git rebase origin/mockup
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base mockup --fill --title "chore(catalog): <subtarea>"
```

- **PR contra `mockup`.** A `main` y a `dev` no se toca (AMB-F5).
- **Jamás te detenés.** Los organismos de Justin y Leo llegan durante el turno. Mientras tanto
  acreditás el mecanismo con componentes que **ya existen** y dejás la microtarea de adopción
  diferida y declarada (regla 65). **Mejorar el catálogo no es condición para que los otros
  avancen, ni al revés.**
- Un test tuyo en rojo detiene esa microtarea: se corrige o va `A MEDIAS`. Nunca `skip`, nunca
  `only`, nunca ampliar una tolerancia para tapar una diferencia.

## 4. Plan

### H1 — La base y el runtime actual del catálogo están auditados, no supuestos

**CA:** Dado el runtime actual, cuando alguien lee tu auditoría, entonces sabe si el preview
comparte inyectores y servicios con el anfitrión — **demostrado con una comprobación, no afirmado
por lectura** — y qué contratos complejos se rellenan hoy con valores inválidos.
**DoD:** `evidencia/baseline.md` + la comprobación de aislamiento con su salida pegada.
**Estado:** TODO

#### H1.S1 — Entorno, comandos y baseline del repo

**CA:** Dada la tabla de comandos publicada, cuando los otros cuatro la leen, entonces ninguno
tiene que descubrir por su cuenta cómo se corre lint, typecheck, test o E2E.
**DoD:** la tabla publicada en el daily §2 en la primera hora + los exit codes previos pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar remoto, rama `mockup`, SHA, estado del árbol y cambios ajenos. **No se resetea nada** (AMB-F4) | El archivo trae el SHA real de hoy | `git rev-parse HEAD && git status --short` → salida pegada | TODO |
| H1.S1.M2 | Completar y **publicar** la tabla de comandos y las versiones resueltas en el daily de equipo §2, en la primera hora. **Prohibido actualizar una dependencia** para facilitar el refactor | La tabla está en el daily y cada alias tiene comando real o la marca "no existe" | el daily §2 trae la tabla; `cat package.json` → `scripts` pegado | TODO |
| H1.S1.M3 | Correr lint, typecheck, test, cobertura y build y registrar el **rojo previo** como baseline de fallos del repo | Los exit codes quedan escritos, verdes o rojos | `<CMD_LINT>; <CMD_TYPECHECK>; <CMD_TEST>; <CMD_BUILD>` → exit codes pegados | TODO |
| H1.S1.M4 | Registrar el baseline de rendimiento: tamaño del bundle por entrada y qué rutas están en carga diferida hoy | Los números previos quedan escritos | `<CMD_BUILD>` → salida con tamaños pegada | TODO |

#### H1.S2 — El runtime del catálogo y el generador de props, auditados

**CA:** Dado el iframe actual, cuando se comprueba si comparte inyectores o servicios del padre,
entonces la respuesta sale de una comprobación ejecutada, no de leer el código.
**DoD:** la comprobación con su salida pegada, cualquiera sea el resultado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Leer el runtime del catálogo y registrar cómo carga los componentes, cómo usa el iframe, de dónde toma los estilos y qué responsabilidades mezcla, citando línea | Cada afirmación cita archivo y línea | `entregables/auditoria-catalogo.md` con citas | TODO |
| H1.S2.M2 | **Demostrar** si el nodo del preview comparte inyectores o servicios con el anfitrión, con una comprobación ejecutada | El resultado queda pegado, comparta o no | spec de aislamiento → salida pegada con exit code | TODO |
| H1.S2.M3 | Leer el generador de props sintéticas y registrar qué contratos complejos rellena con valores inválidos (cadena vacía para un obligatorio, colección vacía como única prueba, función ausente) | La lista de contratos mal rellenados queda escrita | `entregables/auditoria-props.md` con los casos citados | TODO |

### H2 — Las cuatro pruebas de fidelidad se cumplen por separado

**CA:** Dada una ficha del catálogo, cuando se auditan sus cuatro dimensiones —fuente, composición,
interacción y apariencia—, entonces cada una se acredita por su cuenta y ninguna se da por buena
porque otra pasó.
**DoD:** las cuatro comprobaciones con salida pegada sobre al menos dos componentes reales.
**Estado:** TODO

#### H2.S1 — Fuente, composición, interacción y apariencia

**CA:** Dado el nodo montado por el catálogo, cuando se compara su origen con el que usa el
producto, entonces es **el mismo archivo**, no una copia.
**DoD:** comprobación de identidad de fuente → PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Fuente: la ficha importa la implementación canónica del producto en ese build. **Prohibido copiar HTML, TypeScript o CSS a una demo** o reemplazar una ficha rota por una reconstrucción parecida | Una copia dentro del catálogo hace fallar la comprobación | prueba de identidad de fuente → PASS; caso negativo documentado | TODO |
| H2.S1.M2 | Composición: la ficha monta hijos, directivas, ranuras y proveedores necesarios, no un contenedor vacío | Un montaje sin hijos obligatorios se detecta | `<CMD_TEST> --grep "composición"` → PASS | TODO |
| H2.S1.M3 | Interacción: contratos válidos y acciones que producen **salidas observables**; ninguna acción decorativa que aparente persistir | Cada acción de la ficha emite algo comprobable | `<CMD_TEST> --grep "interacción"` → PASS | TODO |
| H2.S1.M4 | Apariencia: tema, fuentes, viewport y contexto declarados y reproducidos. "Componente real con datos sintéticos" es correcto; **no acredita integración con una API real** | La ficha declara su contexto y lo aplica | capturas de la ficha en los contextos declarados, miradas | TODO |

#### H2.S2 — La ficha y su trazabilidad

**CA:** Dada una familia repetida, cuando se la abre en el catálogo, entonces se llega a sus
consumidores y a la pieza canónica sin buscar a mano en el código.
**DoD:** la navegación funciona sobre al menos una familia real.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | La ficha muestra fuente y commit, responsabilidad, nivel, composición, contratos, variantes, usos directos y transitivos, escenarios y estado de verificación | Ningún campo vacío sin una marca de "no resuelto" | ficha de un componente real revisada y capturada | TODO |
| H2.S2.M2 | Desde una familia se llega a sus consumidores y a la implementación canónica. **Usa el grafo de Marcelo (PR9) cuando esté; mientras tanto, la fuente que ya exista, declarada** | La navegación funciona en un caso real | E2E de navegación del catálogo → PASS | TODO |
| H2.S2.M3 | Estados distinguidos: descubierto, escenario disponible, montaje válido, interacción verificada, paridad visual verificada y bloqueado. **Prohibido reducir todas las dimensiones a un solo check verde** | Las seis dimensiones se ven por separado | captura de la ficha con las seis + conteo por estado pegado | TODO |

### H3 — Los escenarios son explícitos, no props adivinadas

**CA:** Dado un contrato complejo, cuando el catálogo lo monta, entonces los valores vienen de una
factory tipada con invariantes conocidas, y lo que no se puede construir queda marcado como no
verificado en vez de rellenarse con un valor vacío.
**DoD:** el esquema del escenario validado + los casos de relleno inválido eliminados o marcados.
**Estado:** TODO

#### H3.S1 — Factories y hosts tipados

**CA:** Dado un componente que necesita proyección, plantillas o formularios, cuando se lo monta,
entonces se lo monta desde un host escrito en el lenguaje del framework, no desde un JSON.
**DoD:** `<CMD_TYPECHECK>` en verde + un host real funcionando.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Host tipado para la composición que necesita referencias de plantilla, formularios o proyección compleja | Un componente con proyección se monta completo | `<CMD_TEST> --grep "host"` → PASS | TODO |
| H3.S1.M2 | Factory por escenario con sus invariantes; el generador aleatorio **solo completa dentro** de esas invariantes, no las decide | Un dato fuera de invariante hace fallar la factory | `<CMD_TEST> --grep "factory"` → PASS; caso negativo documentado | TODO |
| H3.S1.M3 | Prohibido usar una cadena vacía para un obligatorio desconocido, y una colección vacía como única prueba de una colección compleja: el fallback se marca **no verificado** | Los casos hallados en H1.S2.M3 quedan corregidos o marcados | lista de H1.S2.M3 revisada, cada caso con su estado | TODO |
| H3.S1.M4 | El manifiesto guarda **referencias** a factories y hosts, no funciones serializadas; su esquema está definido y validado | Un manifiesto inválido falla la validación | validación del esquema → exit 0; caso negativo documentado | TODO |

#### H3.S2 — Edición de inputs y ciclo de vida del montaje

**CA:** Dada una edición inválida de una entrada, cuando el catálogo la aplica, entonces muestra el
error y conserva el último escenario válido; nunca marca el montaje como exitoso tras silenciar el
fallo.
**DoD:** `<CMD_TEST> --grep "edición inválida"` → PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Validar la edición de entradas: error visible y último escenario válido conservado; **no se marca montaje exitoso tras silenciar una escritura fallida** | Una entrada inválida muestra error y no rompe la ficha | `<CMD_TEST> --grep "edición inválida"` → PASS | TODO |
| H3.S2.M2 | Una sola ejecución vigente: un montaje demorado **no** reemplaza la selección actual. Probar A → B → A con cargas demoradas | La secuencia A → B → A deja montado A, no B | `<CMD_E2E> --grep "montaje demorado"` → PASS | TODO |
| H3.S2.M3 | Limpieza de componentes, escuchas, observadores y temporizadores, **también cuando el montaje falla** | Cien montajes fallidos no acumulan recursos | test de ciclo de vida → PASS; conteo antes/después pegado | TODO |

### H4 — El preview está aislado de verdad, no solo dentro de un iframe

**CA:** Dada una operación hecha en el preview, cuando se mira el anfitrión, entonces su sesión, su
almacenamiento y sus datos quedaron intactos, y ninguna petición de negocio inesperada salió.
**DoD:** la comprobación de aislamiento en verde + el registro de peticiones bloqueadas.
**Estado:** TODO

#### H4.S1 — Entrada propia y contexto propio

**CA:** Dado el preview, cuando se lo inspecciona, entonces tiene su propio documento, su propio
arranque y sus propios proveedores, e importa **los mismos componentes canónicos** que el producto.
**DoD:** la entrada existe y la comprobación de H1.S2.M2 ahora da aislado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Entrada de preview en documento propio, con arranque y proveedores específicos, importando los componentes canónicos | La comprobación de H1.S2.M2 pasa de compartido a aislado | mismo spec de H1.S2.M2 → resultado pegado, comparado con el previo | TODO |
| H4.S1.M2 | Verificar documento, ventana, superposiciones, router, temas, estilos, fuentes, almacenamiento y destrucción en el contexto del preview | Cada uno queda comprobado, no supuesto | spec por cada uno → salida pegada | TODO |
| H4.S1.M3 | Las cuentas sintéticas **no cambian la sesión anfitriona**; el almacenamiento usa un adaptador de memoria o un ámbito explícito de preview. El mismo origen puede seguir compartiendo cookies: eso se comprueba, no se asume | Iniciar sesión sintética deja la sesión del anfitrión intacta | E2E del segundo kill-test → PASS | TODO |
| H4.S1.M4 | Bloquear peticiones de negocio inesperadas y demostrar que no hubo mutación real. **Cualquier comprobación contra un entorno compartido es un escenario aparte y requiere autorización** | Ninguna petición de negocio sale del preview sin estar declarada | registro de peticiones del E2E → pegado | TODO |

#### H4.S2 — Mensajería, viewport y separación del bundle

**CA:** Dado un mensaje entre ventanas, cuando llega, entonces se validan origen, ventana emisora,
tipo, carga útil e identidad de ejecución, y no transporta credenciales ni datos clínicos.
**DoD:** los casos de mensaje inválido rechazados, con su salida.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Validar origen, ventana emisora, tipo, carga útil e identidad en cada mensaje; **sin credenciales ni datos clínicos en mensajes ni en URLs** (regla 90.2 leída como dato clínico) | Un mensaje de otro origen se rechaza | `<CMD_TEST> --grep "mensajes"` → PASS con los casos negativos | TODO |
| H4.S2.M2 | Viewport real de navegador con el tamaño declarado. **Estrechar un contenedor o usar zoom no reproduce un viewport**: las media queries se prueban en contexto de navegador | Las media queries se disparan como en el dispositivo real | capturas por viewport real, miradas | TODO |
| H4.S2.M3 | El bundle de producto **no** incluye fixtures, credenciales de prueba ni infraestructura exclusiva del catálogo | La búsqueda de artefactos del catálogo en el bundle de producto no encuentra nada | `<CMD_BUILD>` + búsqueda en la salida → sin resultados, pegado | TODO |

### H5 — Los gates y el cierre del alcance no se pueden falsear

**CA:** Dado el documento de cierre, cuando alguien que no vio la sesión lo lee, entonces sabe qué
comando corrió, con qué commit, con qué exit code, qué artefacto quedó, y qué **no** se ejecutó.
**DoD:** el registro de ejecución completo + el documento de cierre escrito.
**Estado:** TODO

#### H5.S1 — Gates de visual, accesibilidad, consola y red

**CA:** Dado un gate en rojo, cuando se cierra el turno, entonces sigue en rojo en el informe: no se
lo tapa actualizando un baseline ni ampliando una tolerancia.
**DoD:** los cuatro gates corridos, con su resultado real pegado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | Gate visual determinista: mismo navegador, sistema, viewport, escala, fuente, tema, idioma, reloj y datos; esperar assets y fuentes; animaciones controladas para capturas estables | Dos corridas seguidas sin cambios dan el mismo resultado | el gate corrido dos veces → mismo resultado, pegado | TODO |
| H5.S1.M2 | **Prohibido** actualizar snapshots, ampliar tolerancias o enmascarar la región modificada para ocultar una regresión | Ninguna de las tres cosas aparece en el diff | revisión del diff de configuración del gate visual | TODO |
| H5.S1.M3 | Gate de accesibilidad: verificación automática **más** navegación por teclado; nombre accesible, etiqueta y error, foco, cierre, restauración de foco y estado deshabilitado. Lo automático no alcanza y se dice | El recorrido por teclado está documentado, no solo el informe automático | spec de accesibilidad → salida pegada + recorrido descrito | TODO |
| H5.S1.M4 | Gate de consola y red: un error de consola relevante o un 4xx/5xx inesperado **hace fallar** el test. Un observador de rendimiento por sí solo no demuestra ausencia de red | Un error inyectado a propósito hace fallar el gate | caso negativo ejecutado → el gate falla como se espera | TODO |

#### H5.S2 — Rendimiento, solo donde hay riesgo

**CA:** Dado un cambio en colecciones, carga dinámica o reactividad, cuando se compara contra el
baseline de H1.S1.M4, entonces la diferencia está medida, no supuesta.
**DoD:** la comparación con los dos números pegados.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S2.M1 | Comparar bundle y peticiones duplicadas contra el baseline, solo en las áreas tocadas | Los dos números quedan escritos, antes y después | `<CMD_BUILD>` → tamaños comparados con H1.S1.M4 | TODO |
| H5.S2.M2 | La carga diferida existente se conserva: ninguna ruta pasa a cargarse de entrada sin decisión registrada | Las rutas diferidas del baseline siguen diferidas | salida del build comparada, pegada | TODO |
| H5.S2.M3 | **Prohibido imponer porcentajes o presupuestos universales sin datos**: solo comparación contra el baseline propio | Ningún umbral inventado en la configuración | revisión del diff: sin umbrales nuevos sin dato que los respalde | TODO |

#### H5.S3 — Cierre del alcance y consolidación del área

**CA:** Dado el cierre, cuando se mira el avance del área frontend, entonces sale de un conteo de
microtareas, no de una impresión; y lo que quedó a medias trae las cuatro respuestas.
**DoD:** el documento de cierre + el registro de ejecución + la consolidación con denominador declarado.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S3.M1 | Documento de cierre del refactor: alcance, baseline, decisiones, oleadas, estado y **cómo reproducirlo** | Alguien que no vio la sesión puede repetir la verificación | el documento existe en el repo frontend y lo enlaza el daily de equipo | TODO |
| H5.S3.M2 | Registro de ejecución: comando exacto, directorio, commit, fecha, exit code, estado (`pasó`, `falló`, `no se corrió`, `bloqueado`) y artefactos. **Una prueba omitida queda visible; un fallo previo no se presenta como regresión nueva ni se borra del informe** | Ninguna fila sin exit code ni sin estado | el registro con todas las corridas del área, pegado | TODO |
| H5.S3.M3 | Consolidar el área: componentes inspeccionados sobre el total, consumidores migrados sobre los comprometidos, familias verificadas, escenarios acreditados y rutas comprobadas, **con el denominador declarado** y explicado si cambió | Los cinco números salen de un conteo | la consolidación en el daily de equipo §6, con los conteos pegados | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| AMB-F3 | Las rutas del runtime del catálogo y del generador de props son hipótesis | Tu baseline (H1.S2) | La auditoría | No se usa ninguna hasta confirmarla con archivo y línea |
| AMB-F5 | A qué rama se integra el trabajo | Dueño del repo frontend | La integración final | PR contra `mockup`; la promoción se **recomienda** por escrito, no se ejecuta |
| AMB-F6 | Cuál es el runner de cada capa, con Vitest, Playwright y Cypress coexistiendo | Vos, en H1.S1.M2 | La tabla de comandos de los cinco | Se usa el que ya está cableado; **no se instala nada nuevo** |
| Q-P1 | Si el mismo origen del preview sigue compartiendo cookies o almacenamiento con el anfitrión | Tu comprobación (H4.S1.M3) | La acreditación del aislamiento | Se comprueba, no se asume; si comparte, se usa adaptador de memoria o ámbito explícito |
| Q-P2 | Si se puede verificar algo contra un entorno compartido | Coordinación / dueño del entorno | Las comprobaciones contra datos reales | **No se hace sin autorización escrita**; queda como escenario separado y declarado |
| Q-P3 | Qué organismos de Justin y Leo llegan a tiempo para acreditar sus fichas | Justin y Leo, durante el turno | La acreditación de esas dos fichas | Se acredita el mecanismo con componentes existentes y la adopción queda diferida y declarada |
| Q-P4 | Si el repo frontend tiene CI y qué corre hoy | Tu baseline | El cableado de los gates | Los gates se dejan corriendo localmente con su registro; el cableado en CI se declara `A MEDIAS` si no llega |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia. Regla 65: si el contrato se puede nombrar, se simula en tres niveles y se cierra.
- [ ] Las cuatro pruebas de fidelidad acreditadas **por separado**, no una por otra.
- [ ] El preview no altera la sesión ni los datos del anfitrión, demostrado con una corrida.
- [ ] El bundle de producto sin fixtures, credenciales de prueba ni infraestructura del catálogo.
- [ ] Ningún gate tapado actualizando un baseline, ampliando una tolerancia o enmascarando una región.
- [ ] Registro de ejecución con comando, commit, exit code, estado y artefactos, incluidos los
      `no se corrió` y los `bloqueado`.
- [ ] Peldaño de evidencia declarado por área (regla 30). El peldaño del área frontend es **el más
      bajo** de los cinco carriles, no el tuyo.
- [ ] Sin datos clínicos ni identificatorios reales en fixtures, capturas, mensajes, URLs ni evidencia.

## 7. Revisión adversarial antes de cerrar

1. ¿La demo **recrea** la pantalla en vez de importar la fuente canónica?
2. ¿El iframe comparte sesión o servicios del padre de manera inadvertida?
3. ¿Un mock exitoso se presenta como integración terminada?
4. ¿La ficha de la tabla está vacía para evitar probar columnas o funciones requeridas?
5. ¿El producto todavía usa el duplicado mientras el catálogo muestra la pieza nueva?
6. ¿Se declara verificado algo que solo fue inspeccionado estáticamente?
7. ¿El informe oculta pendientes achicando el alcance o el denominador?
8. ¿Se actualizó un snapshot o se amplió una tolerancia para que pasara?
9. ¿Un `no se corrió` se convirtió en un `pasó` porque igual compila?
10. ¿Se presentó un comando recién escrito como evidencia del estado previo del repo?
