# La tabla canónica: un contrato, cero banderas por pantalla, y dos consumidores reales migrados

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Justin · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Justin-Daily-Noche-2026-09-21.md](../Justin-Daily-Noche-2026-09-21.md)
- **Corrección 2026-09-21 (Pablo, en sesión):** este carril se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura — mismo
  caso que `PR10`, `PR6` y `PR8`). Confirmado: también es trabajo de Pasanaku. Repo, rama, comandos
  y alcance corregidos abajo. Ver [docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md](../../../../../../docs/trabajo/2026-09-21-correccion-bloques-justin-y-marcelo/PLAN.md).
- **Encargo madre:** prompt maestro de refactorización frontend (documento antecedente, escrito para
  `mantra-core-health`, usado como guía de estructura — no como fuente de hechos sobre Pasanaku).
  Este carril adapta el primer piloto del §12.3 (la tabla de datos), el §8 (contrato de
  composición), el §10.2 (selección y paginación) y las fases 2 y 3 del §14 al catálogo real.
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `https://github.com/PabloArauzCaballero/PasanakuFrontend.git` · rama base
  **`dev`** @ **el SHA que registres vos en H1.S1.M1** · **tu rama:** `justin/frontend/tabla-datos`
- **4 hitos · 8 subtareas · 27 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` de este repo estándar dentro de `PasanakuBackend/` (ya hay una copia
   sin commitear ahí, de una sesión anterior — verificala antes de volver a copiar). Si ese repo
   trae su propio `AGENTS.md` o `CLAUDE.md` (no verificado todavía), **ese manda sobre estas
   reglas**: lo que choque se registra como ambigüedad, no se resuelve solo.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `frontend-data-tables` | El corazón del carril: columnas, identidad, orden, selección y colapso móvil |
| `atomic-design-components` | Reusar antes que crear; parametrizar en vez de copiar; API del organismo |
| `angular-development` | `input()`/`output()`/`model()`, plantillas tipadas, control flow, OnPush |
| `typescript-standards` | Contrato genérico sin `any`, sin doble cast, sin aserción no nula sistemática |
| `frontend-accessibility` | Nombre accesible, encabezados asociados, foco y orden anunciado |
| `frontend-responsive-layout` | La tabla que colapsa a tarjetas sin perder información ni acciones |
| `angular-testing` | `setInput`, harness y pruebas por la interfaz del consumidor |
| `visual-regression-testing` | Paridad visual contra el baseline, sin ampliar tolerancias |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 60 · 65 · **95** (frontend) · **90** completa
(dato financiero e identificatorio real — Pasanaku, no un dato clínico de ejemplo como decía la
versión anterior de este carril). **91 aplica condicionalmente**: se determina en H1.S2.M2, al
elegir los dos consumidores — si alguno muestra un importe, una cuenta o un cobro, sus datos
sintéticos se verifican con la misma exigencia que producción. **98 no aplica**: este carril es
frontend puro, salvo que termine tocando un contrato entre servicios.

## 2. Resultado observable

Existe **una** implementación de tabla de datos (`packages/ui/src/tabla-de-datos`, confirmada en el
árbol real) con contrato escrito —identidad de fila como función pura, columnas tipadas, estado,
orden, selección y paginación— y **dos pantallas reales del producto** la usan, conservando sus
diferencias legítimas de presentación por tokens y variantes, sin una sola bandera con nombre de
pantalla; la implementación anterior quedó sin referencias activas, o su excepción tiene consumidor
y motivo escritos.

**Kill-test:** abrir la ficha de la tabla en el catálogo. Si está montada **sin columnas**, sin
función de identidad o con una colección vacía como único escenario, la tabla no está probada: está
escondida. Y buscar en el organismo una condición que dependa del nombre de una pantalla: si
aparece una, esto NO está hecho.

## 3. Alcance

**IN:** el organismo de tabla de datos (el existente si lo hay; si no, el mínimo extraído), su
contrato, sus estilos encapsulados, sus specs, y **los dos consumidores** que publiques en
H1.S2.M2 con su baseline y su migración.

**OUT:** la pantalla piloto de Richard (PR6) y cualquier consumidor que él haya reservado primero.
`ViewState`, `ContentDialog` y el contrato de borrador (Leo, PR8). El generador del índice y el
grafo de usos (Marcelo, PR9). `component-stock`, el preview y CI (Pablo, PR10). Los tokens del
sistema de diseño: **no se toca una variable de color, espaciado ni tipografía**. El backend y sus
contratos: **no se toca un endpoint ni un DTO**. Ninguna dependencia nueva ni actualizada. `main` y
`dev` no se tocan.

**Reservas de archivos:** `packages/ui/src/tabla-de-datos` y sus estilos; los dos consumidores
publicados en H1.S2.M2. Si uno de ellos es la pantalla piloto de Richard, **elegís otro**: el que
publique primero en el daily de equipo se la queda (AMB-F7).

### Comandos del repo — candidatos reales (Pasanaku), se confirman en H1.S1.M2

**Corrección 2026-09-21:** la tabla original traía comandos de `mantra-core-health`. Reemplazados
por los reales, verificados contra `package.json`/`turbo.json`:

| Alias | Candidato real (Pasanaku) | Cómo se confirma |
|---|---|---|
| `CMD_LINT` | `turbo run lint` | `package.json` raíz → `scripts.lint` |
| `CMD_TYPECHECK` | `turbo run typecheck` | `package.json` raíz → `scripts.typecheck` |
| `CMD_TEST` | `turbo run test:front` | `package.json` raíz → `scripts["test:front"]` |
| `CMD_BUILD` | `turbo run build` | `package.json` raíz → `scripts.build` |
| `CMD_E2E` | `yarn workspace @aportaya/web test:e2e` o `yarn workspace @aportaya/backoffice test:e2e` (según en qué app estén los dos consumidores elegidos en H1.S2.M2) | `apps/web/package.json` y `apps/backoffice/package.json` → `scripts["test:e2e"]` |

Si un alias no existe, **no lo inventes ni lo crees**: usá el binario que el repo ya trae y anotá
la diferencia en tu daily.

### Ritual de entrega

```bash
git fetch origin && git checkout -b justin/frontend/tabla-datos origin/dev
git fetch origin && git rebase origin/dev
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base dev --fill --title "refactor(table): <subtarea>"
```

- **PR contra `dev`.** `main` no se toca. `PasanakuFrontend` (espejo) se sincroniza por
  fast-forward después, no en cada PR (decisión D-A2 del plan madre).
- **Jamás te detenés.** El contrato de estado es de Leo y se publica en la primera hora. Si no está,
  nombrás el contrato, construís el doble en **tres niveles** —correcto (colección con filas
  válidas) · límite (colección vacía; una sola fila; respuesta marcada como obsoleta) · inválido
  (error con su identificador de petición; sin permiso; no encontrado)— y cerrás contra el doble
  **declarándolo** (regla 65). La adopción del tipo real queda como microtarea diferida.
- Un test tuyo en rojo detiene esa microtarea: se corrige o va `A MEDIAS`. Nunca `skip`, nunca
  `only`, nunca debilitar una aserción, nunca borrar un test que molesta.

## 4. Plan

### H1 — La base y el mapa de usos de la tabla son hechos registrados

**CA:** Dado `evidencia/baseline.md`, cuando alguien lo lee, entonces sabe el SHA, los comandos
reales, qué estaba rojo antes, qué pantallas usan hoy una tabla y con qué tipo de relación, y
cuáles dos se van a migrar.
**DoD:** baseline con las salidas literales + tabla de consumidores con archivo, ubicación, tipo de
relación y condición de render + baseline visual de los dos elegidos.
**Estado:** TODO

#### H1.S1 — Entorno y fuente verificados antes de decidir nada

**CA:** Dado el documento antecedente, cuando terminás esta subtarea, entonces la implementación de
tabla existente quedó localizada con archivo y línea, o se registró que no existe.
**DoD:** SHA y `git status` pegados, tabla de comandos completa, y la pieza de tabla `confirmada en
<ruta:línea>` o `no existe`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar remoto, rama `dev`, SHA, estado del árbol y cambios ajenos. **No se resetea nada** (AMB-F4) | El archivo trae el SHA real de hoy | `git rev-parse HEAD && git status --short` → salida pegada | TODO |
| H1.S1.M2 | Completar la tabla de comandos desde `package.json` y el lockfile; registrar versiones resueltas. **Prohibido actualizar una dependencia** para facilitar el refactor | Cada alias tiene su comando real o la marca "no existe" | `cat package.json` → sección `scripts` pegada | TODO |
| H1.S1.M3 | Correr lint, typecheck, test y build y registrar el **rojo previo** | Los cuatro exit codes quedan escritos | `<CMD_LINT>; <CMD_TYPECHECK>; <CMD_TEST>; <CMD_BUILD>` → exit codes pegados | TODO |
| H1.S1.M4 | Localizar la implementación de tabla existente y su contrato actual resolviendo imports con el compilador, **no con grep suelto**. Si ya resuelve bien la separación, se **adopta y extiende**, no se reescribe | Queda escrito si se adopta, se extiende o se extrae | `<CMD_TYPECHECK>` sobre un archivo de sondeo que la importa → exit 0 o error citado | TODO |

#### H1.S2 — Quién la usa de verdad, y cuáles dos se migran

**CA:** Dada la lista de consumidores, cuando se mira una fila, entonces distingue si la plantilla
**instancia** el componente o solo lo tiene importado disponible, y en qué condición se renderiza.
**DoD:** la tabla de usos con las cuatro columnas + los dos elegidos publicados en el daily §4.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Listar los consumidores con relación diferenciada: instancia en plantilla, import disponible sin usar, dependencia solo de tipos, carga dinámica y carga por ruta. Un import no usado o un selector en un comentario **no** son consumidores | Cada fila tiene archivo, ubicación, tipo de relación y condición de render | `entregables/usos-tabla.md` con la tabla; ninguna fila sin ubicación | TODO |
| H1.S2.M2 | Elegir los **dos** consumidores a migrar (los de contrato más compatible, no los más fáciles) y publicarlos en el daily de equipo §4 en la primera hora | Los dos quedan escritos y ninguno choca con la reserva de Richard | el daily §4 nombra los dos archivos; Richard confirmó por escrito | TODO |
| H1.S2.M3 | Capturar el baseline visual y funcional de esos dos: 3 viewports × 2 temas × estados carga, vacío y error, con datos sintéticos deterministas | Las capturas existen y **las miraste**; el E2E dirigido corrió | `<CMD_E2E>` del spec de capturas → exit 0; archivos en `evidencia/baseline-visual/` | TODO |

### H2 — El contrato está escrito antes de tocar la implementación

**CA:** Dado `entregables/contrato-tabla.md`, cuando un consumidor lo lee, entonces sabe qué datos
debe pasar, qué intenciones recibe, qué estados existen, qué combinaciones son inválidas y qué
pasa cuando llega una respuesta atrasada — sin leer el código del organismo.
**DoD:** la ficha completa con las diez áreas del contrato + `<CMD_TYPECHECK>` en verde.
**Estado:** TODO

#### H2.S1 — Datos, identidad, columnas y estado

**CA:** Dado un conjunto de filas, cuando se reordenan o se reemplazan, entonces la identidad de
cada fila se mantiene estable y el estado de fila no salta de una a otra.
**DoD:** `<CMD_TEST> --grep "identidad"` → PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Escribir la ficha del contrato: identidad, entradas (nombre, tipo, obligatoriedad, nulabilidad, default, transformación), salidas con su intención, composición, estado, apariencia, errores y compatibilidad | Las diez áreas están; ninguna dice "según el caso" | `entregables/contrato-tabla.md` existe **antes** de la primera línea de implementación | TODO |
| H2.S1.M2 | Identidad de fila como **función pura tipada** provista por el consumidor. Prohibido el índice cuando los elementos cambian de posición | Reordenar no pierde selección ni foco de fila | `<CMD_TEST> --grep "identidad"` → PASS | TODO |
| H2.S1.M3 | Definición de columna tipada: acceso a celda como función pura y plantilla con contexto tipado para el contenido dependiente de la fila | Un acceso mal tipado no compila | `<CMD_TYPECHECK>` → exit 0; un caso negativo documentado que no compila | TODO |
| H2.S1.M4 | Estado de la colección con el tipo de estado **real del repo**, sin reducir sus variantes a cargando/error/éxito. Si el contrato de Leo no llegó, doble en tres niveles y microtarea de adopción diferida | Ninguna variante del tipo se pierde por el camino | test de exhaustividad de variantes → PASS | TODO |

#### H2.S2 — Selección y paginación, con sus casos feos

**CA:** Dado un cambio de filtro o una respuesta atrasada, cuando el usuario ya había seleccionado
filas, entonces la política declarada se cumple y no hay una selección fantasma.
**DoD:** `<CMD_TEST> --grep "selección"` → PASS con los casos de borde incluidos.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Especificar e implementar la selección: identidad, alcance por página o global, significado de "seleccionar todo", elementos deshabilitados, pérdida de un elemento y cambio de filtro | Cada caso tiene su respuesta escrita y su test | `<CMD_TEST> --grep "selección"` → PASS | TODO |
| H2.S2.M2 | Conservar la paginación existente tal cual es: si es por cursor, **sigue siendo por cursor**. Prohibido convertirla en paginación por índice para simplificar la demo | La paginación se comporta igual que en el baseline | E2E de paginación → PASS; comparación con el baseline funcional | TODO |
| H2.S2.M3 | Una respuesta atrasada **no** reemplaza a la vigente ni resucita una selección descartada | El test de respuesta atrasada falla si se reemplaza | `<CMD_TEST> --grep "atrasada"` → PASS | TODO |

### H3 — Una implementación, variantes con significado, cero banderas de pantalla

**CA:** Dadas dos apariencias distintas de la tabla, cuando se comparan sus plantillas, entonces
comparten anatomía y comportamiento y solo difieren por tokens y variantes semánticas; ninguna
condición menciona el nombre de una pantalla.
**DoD:** búsqueda de nombres de pantalla dentro del organismo → vacía; `<CMD_TEST>` en verde.
**Estado:** TODO

#### H3.S1 — Anatomía, variantes y estilos

**CA:** Dado el organismo, cuando un consumidor necesita una apariencia distinta, entonces la
consigue con un token o una variante acotada, sin tocar su plantilla.
**DoD:** las dos apariencias del baseline reproducidas desde una sola implementación.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Declarar anatomía: regiones obligatorias y opcionales, cardinalidad, orden visual y orden accesible; qué hijos crea el organismo y qué aporta el consumidor | Un uso sin una región obligatoria se detecta por tipo o por test | `<CMD_TYPECHECK>` → exit 0; test de uso inválido → falla como se espera | TODO |
| H3.S1.M2 | Representación móvil: colapso a tarjetas **sin perder información ni acciones**; la tabla sigue siendo legible en móvil estrecho | En móvil, toda columna y toda acción del escritorio siguen disponibles | capturas móviles comparadas con el baseline → sin pérdida | TODO |
| H3.S1.M3 | Variantes por token y densidad, con nombre semántico. **Prohibido** usar el nombre de una pantalla como variante | Búsqueda de nombres de pantalla dentro del organismo → vacía | `grep -rin "<nombres de pantalla>" <ruta del organismo>` → sin resultados | TODO |
| H3.S1.M4 | Estilos encapsulados: sin dependencias nuevas de selectores privados de hijos, sin perforar la encapsulación, sin cascadas globales y sin `!important` como solución por defecto | El diff no agrega ninguna de esas cuatro cosas; las excepciones indispensables quedan localizadas y explicadas | revisión del diff de estilos + `<CMD_LINT>` → exit 0 | TODO |

#### H3.S2 — Accesibilidad de la tabla

**CA:** Dada la tabla, cuando se recorre solo con teclado, entonces se puede ordenar, seleccionar y
paginar, y el lector anuncia el estado de orden y de selección.
**DoD:** recorrido por teclado registrado + verificación automática sin infracciones nuevas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Nombre accesible de la tabla, encabezados asociados a sus celdas y orden de foco coherente con el orden visual | La verificación automática no agrega infracciones y el recorrido tiene sentido | spec de accesibilidad → PASS; recorrido descrito en `evidencia/` | TODO |
| H3.S2.M2 | Ordenar por teclado, con el estado de orden anunciado (no solo dibujado con una flecha) | Se puede ordenar sin mouse y el estado se percibe sin ver | E2E de teclado → PASS | TODO |
| H3.S2.M3 | Ninguna información transmitida **solo por color** (fila seleccionada, fila deshabilitada, estado de la fila) | Cada señal de color tiene además texto, icono o atributo | revisión + captura en escala de grises en `evidencia/` | TODO |

### H4 — Dos consumidores reales la usan y la vieja se retira

**CA:** Dadas las dos pantallas migradas, cuando se comparan con su baseline, entonces se ven y se
comportan igual salvo las diferencias explicadas; y la implementación anterior no tiene
referencias activas inesperadas.
**DoD:** E2E dirigido de las dos pantallas PASS + comparación visual + búsqueda de referencias a la
pieza retirada.
**Estado:** TODO

#### H4.S1 — Migración de los dos consumidores

**CA:** Dado cada consumidor migrado, cuando conserva una diferencia de presentación, entonces esa
diferencia está expresada como token o variante, no como un caso especial dentro del organismo.
**DoD:** los dos consumidores compilan, pasan sus tests y no agregan una bandera al organismo.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Migrar el consumidor 1 al organismo canónico, conservando sus diferencias legítimas | Compila, sus tests pasan, su apariencia no cambió sin explicación | `<CMD_TEST> --grep "<consumidor 1>"` → PASS | TODO |
| H4.S1.M2 | Migrar el consumidor 2 | Compila y sus tests pasan | `<CMD_TEST> --grep "<consumidor 2>"` → PASS | TODO |
| H4.S1.M3 | Retirar la implementación duplicada **solo** si todos sus consumidores están migrados o excluidos con motivo; revisar usos dinámicos y rutas antes de borrar | Ninguna referencia activa inesperada; las exclusiones tienen consumidor y motivo | búsqueda de referencias al símbolo retirado → solo las declaradas; `<CMD_BUILD>` → exit 0 | TODO |

#### H4.S2 — Verificación del carril

**CA:** Dado el reporte del carril, cuando alguien que no vio la sesión lo lee, entonces sabe qué
se verificó aislado, qué se verificó integrado, qué quedó bloqueado y qué **no** se ejercitó.
**DoD:** `entregables/PR7-carril.md` con peldaño de evidencia y sección "No cubierto".
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Tests de contrato: entradas, cambios externos, salidas, selección, cardinalidad y que la tabla **no muta** las filas recibidas | Mutar la entrada hace fallar el test | `<CMD_TEST> --grep "<organismo>"` → PASS con el conteo pegado | TODO |
| H4.S2.M2 | E2E dirigido en los dos consumidores, con consola y red vigiladas: un error de consola relevante o un 4xx/5xx inesperado **hace fallar** el test | Los dos E2E pasan y la lista de errores no creció respecto del baseline | `<CMD_E2E> --grep "<consumidor 1>|<consumidor 2>"` → PASS; listas comparadas | TODO |
| H4.S2.M3 | Comparación visual contra el baseline en 3 viewports × 2 temas. **Prohibido** actualizar snapshots, ampliar tolerancias o enmascarar la región modificada | Cada diferencia está explicada o corregida | reporte de comparación con capturas antes/después en `evidencia/` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| AMB-F3 | Que `packages/ui/src/tabla-de-datos` sea la implementación real y su forma exacta — hipótesis heredada de `mantra-core-health`, ruta confirmada, contenido no | Tu baseline (H1.S1.M4) | La decisión entre adoptar, extender o extraer | No se toca código hasta confirmar el contenido con archivo y línea real de Pasanaku (corrección 2026-09-21) |
| AMB-F5 | A qué rama se integra el trabajo | Dueño del repo frontend | La integración final | **Resuelta 2026-09-21:** PR contra `dev` (rama real) |
| AMB-F7 | Que los dos consumidores no choquen con la pantalla piloto de Richard | Coordinación, primera hora | La reserva de archivos | El primero que publica se la queda |
| Q-J1 | Cuántas variantes tiene el tipo de estado real del repo | Leo (PR8), primera hora | El tipado del estado de la colección | Doble en tres niveles contra el tipo actual; adopción del contrato de Leo como microtarea diferida y declarada |
| Q-J2 | Si la paginación del repo es por cursor o por índice | Tu baseline (H1.S2.M1) | El contrato de paginación | Se conserva **tal cual está**; convertirla sería un cambio de comportamiento, y eso no entra en este carril |
| Q-J3 | Si alguna diferencia entre las dos pantallas es una regla de dominio y no decoración | Coordinación / producto | La decisión de fusionar | Ante la duda **no se fusiona**: se conservan composiciones separadas y se registra |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia. Regla 65: si el contrato se puede nombrar, se simula en tres niveles y se cierra.
- [ ] El contrato escrito **antes** de la implementación, no después.
- [ ] Dos consumidores reales migrados y verificados en contexto, no solo en el catálogo.
- [ ] Ninguna bandera con nombre de pantalla dentro del organismo.
- [ ] `<CMD_LINT>`, `<CMD_TYPECHECK>`, `<CMD_TEST>`, `<CMD_E2E>` y `<CMD_BUILD>` corridos con exit
      code pegado — incluido el rojo.
- [ ] Peldaño de evidencia declarado por área (regla 30).
- [ ] Sin datos clínicos ni identificatorios reales en fixtures, capturas, logs ni evidencia.

## 7. Revisión adversarial antes de cerrar

1. ¿La ficha del catálogo está **vacía** para evitar probar columnas o funciones requeridas?
2. ¿El producto todavía usa el duplicado mientras el catálogo muestra la pieza nueva?
3. ¿Una variación decorativa produjo otro organismo completo?
4. ¿El contrato proyectado permite usos inválidos que ningún chequeo detecta?
5. ¿La extracción borró una diferencia real de dominio porque dos tablas se parecían?
6. ¿Un cambio de filtro pierde una selección vigente sin que nadie lo haya decidido?
7. ¿Se retiró código sin revisar consumidores dinámicos y rutas?
8. ¿Se declara verificado algo que solo fue inspeccionado estáticamente?
