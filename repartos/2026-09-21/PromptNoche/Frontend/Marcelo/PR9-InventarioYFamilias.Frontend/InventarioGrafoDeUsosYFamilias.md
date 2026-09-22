# El mapa que no miente: inventario con procedencia, grafo de usos diferenciado y matriz de familias

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Marcelo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Marcelo-Daily-Noche-2026-09-21.md](../Marcelo-Daily-Noche-2026-09-21.md)
- **Encargo madre:** prompt maestro de refactorización frontend. Este carril cubre el §6 (inventario y mapa de usos), el §7 (repetición semántica independiente del CSS), la fase 4 del §14 (retirada) y los campos mínimos del §17.
- **Repo:** `https://github.com/mdavila-2001/mantra-core-health` · rama base **`mockup`** @ **el SHA que registres vos en H1.S1.M1** · **tu rama:** `marcelo/feature/carril-PR9-inventario-familias`
- **5 hitos · 9 subtareas · 31 microtareas**

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
| `dead-code-duplication` | Duplicación real vs parecido superficial; qué se puede retirar y qué no |
| `atomic-design-components` | El eje de composición: átomo, molécula, organismo, plantilla, página |
| `refactoring-safely` | Retirar sin romper: consumidores dinámicos, rutas y orden de los pasos |
| `factual-discovery` | Separar hechos con ruta de desconocidos y de hipótesis |
| `anti-hallucination-guard` | No convertir "seguramente ya existe" en un hecho del inventario |
| `code-quality-audit` | Cómo se audita sin confundir métrica con calidad |
| `technical-docs-and-adr` | La ficha de familia y la decisión registrada con sus alternativas |
| `context-thrift` | Leer por rango y por búsqueda; no volcar archivos enteros |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 60 · 65 · **95** (frontend) · 90.2 leída
como dato **clínico e identificatorio** (AMB-F2). **No aplican** la 91 ni la 98.

## 2. Resultado observable

Existe un inventario de componentes con procedencia (commit, ruta, símbolo, selector), clasificado
por responsabilidad, nivel de composición y ámbito; un grafo de usos que **distingue** estar
importado de estar instanciado, de aportar contenido a una región, de cargarse dinámicamente y de
ser solo una dependencia de tipos; y una matriz de familias donde cada familia declara sus
invariantes, sus diferencias, su pieza canónica, su **contraejemplo** y su decisión. Lo que el
análisis no pudo resolver aparece marcado como no resuelto, no rellenado.

**Kill-test:** tomar un componente que solo está **importado y no usado** en una pantalla y ver si
el grafo lo cuenta como consumidor de producto. Si lo cuenta, el mapa miente, y todas las
decisiones de retirada que se apoyen en él son inválidas: esto NO está hecho.

## 3. Alcance

**IN:** el generador del índice de componentes y sus artefactos; el esquema de los registros de
componente, uso y familia; la matriz de familias; la lista de duplicados retirables con su
verificación de consumidores; `entregables/` con inventario, grafo y matriz.

**OUT:** **no se refactoriza ningún componente de producto en este carril.** La pantalla piloto de
Richard (PR6), el organismo tabla y sus consumidores (Justin, PR7), el diálogo, el host de estados
y el contrato de borrador (Leo, PR8), `component-stock`, el preview y CI (Pablo, PR10). Los tokens
del sistema de diseño. El backend. Ninguna dependencia nueva: si el repo ya trae una herramienta
capaz de resolver TypeScript y plantillas, **se usa esa**. `main` y `dev` no se tocan.

**Reservas de archivos:** el generador del índice y sus artefactos generados; los documentos de
inventario, grafo y familias. Lo que encuentres roto en un componente ajeno **se anota como
hallazgo con ruta en tu daily §6 y se le avisa al dueño del carril; no se arregla** (regla 00 §3).

### Comandos del repo — candidatos heredados, se confirman en H1.S1.M2

| Alias | Candidato heredado | Cómo se confirma |
|---|---|---|
| `CMD_LINT` | `yarn lint` | `package.json` → `scripts` |
| `CMD_TYPECHECK` | `yarn typecheck` | `package.json` → `scripts` |
| `CMD_TEST` | `yarn test` (Vitest) | `package.json` + config del runner |
| `CMD_BUILD` | `yarn build` | `package.json` → `scripts` |
| `CMD_INDEX` | `yarn stock:generate` | `package.json` → `scripts` |
| `CMD_VISTAS` | `yarn audit:vistas` | `package.json` → `scripts` |

Si un alias no existe, **no lo inventes ni lo crees**: usá el binario que el repo ya trae y anotá
la diferencia en tu daily.

### Ritual de entrega

```bash
git fetch origin && git checkout -b marcelo/feature/carril-PR9-inventario-familias origin/mockup
git fetch origin && git rebase origin/mockup
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base mockup --fill --title "chore(inventory): <subtarea>"
```

- **PR contra `mockup`.** A `main` y a `dev` no se toca (AMB-F5).
- **Jamás te detenés.** Si el inventario necesita una decisión de otro carril, la nombrás, seguís
  con el resto y la dejás declarada (regla 65).
- **No desarrolles un compilador completo antes del primer resultado.** Aprovechá lo que el repo ya
  tiene, priorizá el alcance y dejá las dependencias no resueltas claramente identificadas.

## 4. Plan

### H1 — La base y el generador actual están auditados, no supuestos

**CA:** Dado el generador de índice existente, cuando alguien lee tu auditoría, entonces sabe qué
resuelve leyendo el código de verdad y qué resuelve adivinando con expresiones regulares, y cuáles
de los siete casos trampa falla hoy.
**DoD:** `evidencia/baseline.md` + los siete casos construidos + la salida del generador actual
sobre ellos, pegada.
**Estado:** TODO

#### H1.S1 — Entorno y fuente verificados antes de decidir nada

**CA:** Dado el documento antecedente, cuando terminás esta subtarea, entonces el generador quedó
localizado con archivo y línea, o registrado como inexistente.
**DoD:** SHA y `git status` pegados, tabla de comandos completa, ruta confirmada o refutada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar remoto, rama `mockup`, SHA, estado del árbol y cambios ajenos. **No se resetea nada** (AMB-F4) | El archivo trae el SHA real de hoy | `git rev-parse HEAD && git status --short` → salida pegada | TODO |
| H1.S1.M2 | Completar la tabla de comandos desde `package.json` y el lockfile; registrar versiones resueltas y qué herramienta de análisis ya está instalada | Cada alias tiene su comando real o la marca "no existe" | `cat package.json` → `scripts` y dependencias de análisis pegadas | TODO |
| H1.S1.M3 | Correr lint, typecheck, test y build y registrar el **rojo previo** | Los cuatro exit codes quedan escritos | `<CMD_LINT>; <CMD_TYPECHECK>; <CMD_TEST>; <CMD_BUILD>` → exit codes pegados | TODO |
| H1.S1.M4 | Localizar el generador del índice y registrar su ruta real. Si no existe, decirlo: **no se afirma que no existe sin haberlo buscado** (regla 00) | Queda `confirmado en <ruta:línea>` o `no existe, buscado así` | comando de búsqueda + su salida pegada | TODO |

#### H1.S2 — Los siete casos que pueden falsear el mapa

**CA:** Dados los siete casos, cuando se corre el generador actual sobre ellos, entonces queda
escrito cuáles resuelve bien y cuáles no, con la salida pegada — **sin arreglarlo todavía**.
**DoD:** `entregables/casos-trampa.md` con los siete casos y el resultado actual de cada uno.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Leer el generador y registrar qué resuelve con expresiones regulares y qué resolviendo el código de verdad, citando línea | Cada mecanismo queda citado; nada afirmado sin línea | `entregables/auditoria-generador.md` con citas de línea | TODO |
| H1.S2.M2 | Construir los siete casos trampa: alias de ruta, barrel y reexportación, import no usado, selector de atributo, tipo genérico, contenido proyectado, y carga dinámica identificada | Los siete existen como archivos de prueba reales | `ls` del directorio de casos → 7 entradas | TODO |
| H1.S2.M3 | Correr el generador **actual** sobre los siete y registrar cuáles falla. Prohibido corregirlo en esta microtarea | El resultado por caso queda escrito, verde o rojo | `<CMD_INDEX>` sobre el directorio de casos → salida pegada, siete resultados | TODO |

### H2 — El inventario se resuelve con el compilador y declara lo que no pudo resolver

**CA:** Dado cualquier registro del inventario, cuando se lo audita, entonces trae su procedencia
(commit, ruta, símbolo, selector), su terna de clasificación con la señal que la justifica, y su
estado de análisis; y lo no resuelto figura como no resuelto.
**DoD:** el esquema validado + el índice regenerado sin diff residual.
**Estado:** TODO

#### H2.S1 — Identidad, contratos y procedencia

**CA:** Dado el índice generado, cuando se regenera desde su fuente, entonces no queda diferencia:
el artefacto no se edita a mano.
**DoD:** regenerar y comparar → sin diff.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Definir y **validar** el esquema del registro de componente: versión de esquema, identificador, ruta, símbolo exportado, selector, commit, nivel atómico, responsabilidad, ámbito, contratos, dependencias, estado del análisis y evidencia no resuelta | Un registro al que le falte un campo obligatorio **falla** la validación | validación del esquema sobre el índice → exit 0; caso negativo documentado | TODO |
| H2.S1.M2 | Resolver TypeScript y plantillas con la herramienta que el repo ya trae. **No se certifica composición solo con expresiones regulares** | Los casos de plantilla del H1.S2 se resuelven leyendo el código | `<CMD_INDEX>` → los casos de plantilla en verde | TODO |
| H2.S1.M3 | Estado del análisis y evidencia no resuelta por registro: lo que no se pudo resolver se marca, **no se rellena con un valor plausible** | Ningún campo desconocido queda con un valor inventado | búsqueda de valores de relleno en el índice → sin resultados fuera de los declarados | TODO |
| H2.S1.M4 | El índice se regenera desde su fuente y no deja diferencia residual; el artefacto generado no se edita a mano | Regenerar dos veces da lo mismo | `<CMD_INDEX> && git diff --stat` → sin cambios | TODO |

#### H2.S2 — Clasificación por responsabilidad, composición y ámbito

**CA:** Dada la clasificación de un componente, cuando alguien la discute, entonces puede ver la
**señal concreta** que la justifica, no una opinión.
**DoD:** cada registro clasificado cita la señal; la cobertura queda declarada con su denominador.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Clasificar cada componente del alcance con la terna responsabilidad × composición × ámbito, citando la señal que la justifica | Ninguna terna sin señal citada | el inventario no tiene registros con clasificación sin evidencia | TODO |
| H2.S2.M2 | No marcar como contenedor a un componente de presentación por el solo hecho de inyectar algo: se inspecciona la **dependencia transitiva real** | Cada marca de contenedor cita la dependencia de negocio que lo justifica | lista de contenedores con su dependencia citada | TODO |
| H2.S2.M3 | Declarar la cobertura: componentes inspeccionados sobre el total del alcance, con el denominador fijado y explicado si cambia | El número sale de un conteo, no de una impresión | conteo pegado; el denominador aparece escrito | TODO |

### H3 — El grafo distingue relaciones y no confunde disponible con usado

**CA:** Dado un import no usado, un selector mencionado en un comentario y un componente citado
solo en un test, cuando se consulta el grafo, entonces ninguno figura como consumidor de producto.
**DoD:** los tres casos negativos en verde + los siete casos trampa re-corridos.
**Estado:** TODO

#### H3.S1 — Las relaciones del contrato

**CA:** Dado cualquier uso, cuando se lo mira en el grafo, entonces trae archivo, ubicación, tipo
de relación y condición de renderizado.
**DoD:** ninguna fila del grafo sin esas cuatro columnas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Implementar las relaciones diferenciadas: importado y disponible, instanciado por la plantilla, directiva aplicada, contenido proyectado, carga dinámica, carga por ruta, dependencia solo de tipos y uso observado en ejecución | Las ocho existen y son distinguibles en la salida | validación del esquema de uso → exit 0; una fila de ejemplo por relación | TODO |
| H3.S1.M2 | Cada uso con archivo, ubicación, tipo de relación y condición de renderizado; ruta de aplicación cuando se pueda verificar, y declarada como no verificada cuando no | Ninguna fila incompleta; ninguna URL inventada | búsqueda de filas sin ubicación → sin resultados | TODO |
| H3.S1.M3 | Separar consumidor de **producto** de consumidor de **catálogo** y de **prueba**, en campos distintos | Los tres se pueden contar por separado | conteo por tipo pegado | TODO |
| H3.S1.M4 | Una dependencia no resuelta se marca como no resuelta: **no es ausencia de dependencia** | Ningún no resuelto convertido en cero | lista de no resueltos, con su causa | TODO |

#### H3.S2 — Los siete casos trampa, ahora en verde

**CA:** Dados los siete casos de H1.S2.M2, cuando se corre el generador corregido, entonces cada
uno da el resultado esperado, y los que no se pueden resolver quedan declarados.
**DoD:** los siete resultados pegados, comparados contra los de H1.S2.M3.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Re-correr los siete casos contra el generador corregido y comparar contra el resultado previo | Cada caso mejora o se declara por qué no se puede resolver | `<CMD_INDEX>` sobre los casos → salida pegada junto a la de H1.S2.M3 | TODO |
| H3.S2.M2 | Casos negativos: un import no usado, un selector en un comentario y un uso solo en un test **no** cuentan como consumidor de producto | Los tres casos negativos pasan | prueba del generador → los tres en verde | TODO |
| H3.S2.M3 | Los alias, barrels, reexportaciones, selectores de atributo, plantillas en línea, plantillas en archivo externo y componentes homónimos quedan resueltos o declarados | Cada uno resuelto o con su causa escrita | tabla de resolución con las siete filas | TODO |

### H4 — La matriz de familias decide con evidencia y con contraejemplo

**CA:** Dada cualquier familia, cuando se lee su ficha, entonces trae miembros y ubicaciones,
invariantes de comportamiento y composición, diferencias visuales, diferencias de dominio, pieza
canónica, alternativas descartadas, consumidores a migrar, pruebas de equivalencia, riesgo y **un
contraejemplo**: el caso cercano que la abstracción no debe absorber.
**DoD:** `entregables/familias.md` con la ficha completa por familia; ninguna sin contraejemplo.
**Estado:** TODO

#### H4.S1 — Detección por las cinco dimensiones, no por texto

**CA:** Dados dos componentes parecidos, cuando se decide si son la misma familia, entonces la
decisión cita propósito, anatomía, contrato, comportamiento y apariencia — no un porcentaje de
similitud de texto.
**DoD:** cada familia con las cinco dimensiones comparadas por escrito.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Comparar candidatos por las cinco dimensiones. Las coincidencias de texto producen **candidatos**, no equivalencias | Ninguna familia declarada solo por parecido textual | cada ficha trae las cinco dimensiones comparadas | TODO |
| H4.S1.M2 | Clasificar cada clase CSS involucrada como decorativa, estructural o usada por código antes de ignorarla al normalizar | Ninguna clase descartada sin clasificar | tabla de clases con su función | TODO |
| H4.S1.M3 | Ficha por familia con miembros, invariantes, diferencias visuales, diferencias de dominio, pieza canónica existente o nueva, alternativas descartadas y consumidores a migrar | Ninguna ficha incompleta | validación del esquema de familia → exit 0 | TODO |
| H4.S1.M4 | **Contraejemplo obligatorio** por familia, y la frase que explica qué cambio se haría una sola vez después de extraer y dónde se duplicaba antes | Ninguna familia sin contraejemplo | búsqueda de fichas sin contraejemplo → sin resultados | TODO |

#### H4.S2 — Priorización honesta y estados visibles

**CA:** Dada la lista priorizada, cuando alguien pregunta por qué una familia está primera,
entonces la respuesta son criterios legibles, no un número de similitud.
**DoD:** la lista con sus criterios + los estados de familia visibles.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Priorizar por repetición de reglas, adopción real, estabilidad del contrato, impacto del cambio y facilidad de validación. **Prohibido presentar un porcentaje de similitud como verdad arquitectónica** | Cada prioridad tiene su motivo escrito | la lista priorizada con motivo por fila | TODO |
| H4.S2.M2 | Estados de familia: detectada, analizada, decisión tomada, extracción en curso, consumidores migrados, verificada, retirada o descartada; pendientes y exclusiones **visibles** | Ninguna familia sin estado; ninguna exclusión oculta | conteo por estado pegado | TODO |
| H4.S2.M3 | Ninguna familia aprobada sin consumidores objetivo nombrados; las no aprobadas también llevan motivo | Toda familia aprobada nombra a sus consumidores | revisión: aprobadas sin consumidores → ninguna | TODO |

### H5 — Se retira lo que de verdad quedó sin consumidores

**CA:** Dado un duplicado retirado, cuando se compila y se buscan referencias, entonces no queda
ninguna activa inesperada, incluidas las de carga dinámica y las de rutas.
**DoD:** `<CMD_BUILD>` → exit 0 + búsqueda de referencias con su salida pegada.
**Estado:** TODO

#### H5.S1 — Retirada verificada, no a ciegas

**CA:** Dado lo que no se puede retirar, cuando se cierra el carril, entonces cada exclusión tiene
consumidor identificado y motivo escrito.
**DoD:** `entregables/retirada.md` con retirados y excluidos, cada uno con su verificación.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H5.S1.M1 | Lista de duplicados retirables: **solo** los que tienen todos sus consumidores migrados o excluidos con motivo. Los que dependan de carriles ajenos quedan diferidos, no forzados | Ningún retirable con un consumidor de producto vivo | la lista con el estado de cada consumidor | TODO |
| H5.S1.M2 | Revisar usos dinámicos y rutas **antes** de borrar; actualizar el índice desde su generador, nunca a mano | La compilación y las rutas siguen en pie | `<CMD_BUILD>` → exit 0; `<CMD_INDEX> && git diff --stat` → sin residuo | TODO |
| H5.S1.M3 | Lo que no se puede retirar queda con consumidor y motivo explícitos; los hallazgos sobre código ajeno van a tu daily §6 con ruta, **no se arreglan** | Ninguna retirada sin verificar; ningún arreglo fuera de alcance en el diff | revisión del diff: solo archivos de tu reserva | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| AMB-F3 | Que exista el generador del índice y en qué ruta | Tu baseline (H1.S1.M4) | La auditoría del generador | No se afirma que no existe sin haberlo buscado, y la búsqueda queda pegada |
| AMB-F5 | A qué rama se integra el trabajo | Dueño del repo frontend | La integración final | PR contra `mockup` |
| Q-M1 | Qué herramienta de análisis usar si el repo no trae ninguna capaz de resolver plantillas | Coordinación | La resolución de composición | **No se instala nada nuevo** sin decisión registrada: se declara la limitación y se marca lo no resuelto |
| Q-M2 | Cuál es el alcance del inventario: todo el frontend o un subconjunto | Coordinación | El denominador de la cobertura | Se inventaría todo el frontend y se migra por oleadas; el denominador se fija en H2.S2.M3 y no se achica para mejorar el número |
| Q-M3 | Si una diferencia entre dos componentes parecidos es de dominio y no decorativa | Producto | La decisión de la familia | Ante la duda **no se fusiona**; queda como familia con decisión pendiente y su contraejemplo |
| Q-M4 | Qué consumidores están comprometidos por los carriles PR6, PR7 y PR8 | Richard, Justin y Leo, primera hora | La lista de retirables de H5 | Se toma lo publicado en el daily §4; lo que llegue después queda diferido y declarado |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia. Regla 65: si el contrato se puede nombrar, se simula en tres niveles y se cierra.
- [ ] Ningún dato desconocido rellenado con un valor plausible: lo no resuelto figura como no resuelto.
- [ ] Ningún componente de producto refactorizado en este carril: los hallazgos se anotan, no se arreglan.
- [ ] Los artefactos generados concuerdan con sus fuentes y se regeneran sin diferencia residual.
- [ ] `<CMD_LINT>`, `<CMD_TYPECHECK>`, `<CMD_TEST>`, `<CMD_BUILD>` y `<CMD_INDEX>` corridos con
      exit code pegado — incluido el rojo.
- [ ] Peldaño de evidencia declarado por área (regla 30).
- [ ] Sin datos clínicos ni identificatorios reales en fixtures, capturas, logs ni evidencia.

## 7. Revisión adversarial antes de cerrar

1. ¿Un import no usado, un selector en un comentario o un test cuentan como consumidor de producto?
2. ¿Se convirtió un "no resuelto" en "no hay dependencia"?
3. ¿Hay un porcentaje de similitud presentado como verdad arquitectónica?
4. ¿Alguna familia borra una diferencia real de dominio porque dos piezas se parecían?
5. ¿Se retiró código sin revisar consumidores dinámicos y rutas?
6. ¿El informe oculta pendientes achicando el alcance o el denominador?
7. ¿Se certificó composición solo con expresiones regulares?
8. ¿Se arregló algo fuera de alcance "de paso" en vez de anotarlo?
