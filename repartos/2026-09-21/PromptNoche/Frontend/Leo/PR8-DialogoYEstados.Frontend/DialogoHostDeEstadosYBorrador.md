# Diálogo, host de estados y borrador: la interacción compartida vive en un solo lugar

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Leo · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Leo-Daily-Noche-2026-09-21.md](../Leo-Daily-Noche-2026-09-21.md)
- **Corrección 2026-09-21 (Pablo, en sesión):** este carril se escribió originalmente contra
  `mdavila-2001/mantra-core-health` (otro proyecto, usado solo como plantilla de estructura —
  mismo caso que `PR10` y `PR6`). Confirmado: también es trabajo de Pasanaku. Repo, rama, comandos
  y alcance corregidos abajo. Ver [docs/trabajo/2026-09-21-correccion-bloques-leo/PLAN.md](../../../../../../docs/trabajo/2026-09-21-correccion-bloques-leo/PLAN.md).
- **Encargo madre:** prompt maestro de refactorización frontend (documento antecedente, escrito para
  `mantra-core-health`, usado como guía de estructura — no como fuente de hechos sobre Pasanaku).
  Este carril adapta el segundo piloto del §12.3 (el diálogo de contenido), el host de estados del
  §9, el §10.1 (contrato de formulario) y el §10.3 (guardado y cierre) al catálogo real de Pasanaku.
- **Repo:** el monorepo de Pasanaku — `https://github.com/PabloArauzCaballero/PasanakuBackend.git`
  (canónico) · espejo `https://github.com/PabloArauzCaballero/PasanakuFrontend.git` · rama base
  **`dev`** @ **el SHA que registres vos en H1.S1.M1** · **tu rama:** `leo/frontend/dialogo-estados`
- **4 hitos · 8 subtareas · 26 microtareas**

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
| `frontend-ux-states` | El contrato de estado y los cuatro estados obligatorios de una vista con red |
| `frontend-accessibility` | Modal: rol, nombre, foco inicial, foco atrapado, `Escape` y restauración |
| `angular-forms` | Controles tipados, validación, errores por campo, datos preservados |
| `frontend-forms-ux` | Cuándo validar, doble envío, y qué se siente al cancelar o cerrar |
| `atomic-design-components` | Proyección de contenido, API del organismo y reuso antes que creación |
| `angular-development` | Plantillas con contexto tipado, `input()`/`output()`, ciclo de vida |
| `angular-testing` | Probar foco, descarte y variantes por la interfaz del consumidor |
| `visual-proof` | La captura se mira, no solo se toma |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 60 · 65 · **95** (frontend) · **90** completa
(dato financiero e identificatorio real — Pasanaku, no un dato clínico de ejemplo como decía la
versión anterior de este carril). **91 aplica condicionalmente**: se determina en H3.S2.M1, al
elegir los dos modales reales — si alguno muestra un importe, una cuenta o un cobro, su borrador y
su apariencia se verifican con la misma exigencia que producción. **98 no aplica**: este carril es
frontend puro, salvo que termine tocando un contrato entre servicios.

## 2. Resultado observable

El contrato de estado de la aplicación queda **releído y publicado** en la primera hora, con todas
sus variantes y sus cargas útiles intactas; un host lo renderiza en un solo lugar; el diálogo de
contenido abre, atrapa el foco, cierra por botón, por `Escape` y por el fondo **con la misma
política de descarte**, y devuelve el foco al elemento que lo abrió; y dos modales reales del
producto ya lo usan sin perder el borrador ante un error de guardado.

**Kill-test:** abrir un modal con el formulario sucio y cerrarlo por `Escape`. Si se pierde lo
cargado, o si el botón protege y el `Escape` no, la política de descarte no es única: esto NO está
hecho. Y si el contrato de estado quedó reducido a cargando/error/éxito, se perdieron variantes:
tampoco está hecho.

## 3. Alcance

**IN (retargeteado a Pasanaku):** el tipo de estado de la aplicación y su documento de contrato;
`packages/ui/src/estado-de-pantalla` y `packages/ui/src/estado-vacio` (host de estados, confirmados
en el árbol real — ver H1 para auditar qué contienen hoy); `packages/ui/src/dialogo` (el organismo
de diálogo de contenido con su foco, su apilamiento y su política de descarte); el contrato de
formulario y borrador; **dos** modales reales de `apps/web` o `apps/backoffice`, publicados en
H3.S2.M1.

**OUT:** el organismo tabla y sus consumidores (Justin, PR7). La pantalla piloto de Richard (PR6).
El generador del índice y el grafo de usos (Marcelo, PR9). `component-stock`, el preview y CI
(Pablo, PR10). Los tokens del sistema de diseño: **no se toca una variable de color, espaciado ni
tipografía**. Las reglas de negocio del formulario de dominio: el diálogo no valida reglas
clínicas ni decide qué se puede guardar. El backend y sus contratos. Ninguna dependencia nueva ni
actualizada, ninguna librería de UI nueva. `main` y `dev` no se tocan.

**Reservas de archivos:** el tipo de estado y su contrato; el host de estados; el organismo de
diálogo y sus estilos; los dos modales que publiques en H3.S2.M1. Si uno de ellos pertenece a la
pantalla piloto de Richard o a un consumidor de Justin, **elegís otro** (AMB-F7).

### Tu entrega de la primera hora — el contrato de estado

Justin (PR7) y Pablo (PR10) construyen contra este contrato. **Publicalo en `dev` dentro de la
primera hora** (H1.S2.M2), en un PR con solo eso, título `contrato(estado): …`. Es el equivalente
frontend del micro-PR al troncal: nadie edita lo ajeno, y después todos rebasean. Si no llega a
tiempo, ellos trabajan contra un doble en tres niveles y lo declaran; no se quedan esperando.

El documento antecedente menciona **diez** variantes: pendiente de autenticación de ruta, cargando,
vacío, listo, validación, sin permiso, no encontrado, obsoleto, sin conexión y error.
**Son una hipótesis heredada, no un hecho** (AMB-F3): leé el tipo real, confirmá o corregí la
lista, y conservá las cargas útiles que ya tiene. Prohibido sustituirlo por cargando/error/éxito.

### Comandos del repo — candidatos heredados, se confirman en H1.S1.M2

**Corrección 2026-09-21:** la tabla original traía comandos de `mantra-core-health`. Reemplazados
por los reales del monorepo de Pasanaku, verificados contra `package.json` y `turbo.json` — quedan
igual **candidatos a confirmar por H1.S1.M2**:

| Alias | Candidato real (Pasanaku) | Cómo se confirma |
|---|---|---|
| `CMD_LINT` | `turbo run lint` | `package.json` raíz → `scripts.lint` |
| `CMD_TYPECHECK` | `turbo run typecheck` | `package.json` raíz → `scripts.typecheck` |
| `CMD_TEST` | `turbo run test:front` | `package.json` raíz → `scripts["test:front"]` |
| `CMD_UI_TEST` | `yarn workspace @aportaya/ui test:front` (no existe un script `test` a secas) | `packages/ui/package.json` → `scripts["test:front"]` |
| `CMD_BUILD` | `turbo run build` | `package.json` raíz → `scripts.build` |
| `CMD_E2E` | `yarn workspace @aportaya/web test:e2e` o `yarn workspace @aportaya/backoffice test:e2e` (Playwright, según en qué app estén los dos modales elegidos en H3.S2.M1) | `apps/web/package.json` y `apps/backoffice/package.json` → `scripts["test:e2e"]` |

Si un alias no existe, **no lo inventes ni lo crees**: usá el binario que el repo ya trae y anotá
la diferencia en tu daily.

### Ritual de entrega

```bash
git fetch origin && git checkout -b leo/frontend/dialogo-estados origin/dev
git fetch origin && git rebase origin/dev
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base dev --fill --title "refactor(dialog): <subtarea>"
```

- **PR contra `dev`.** `main` no se toca. `PasanakuFrontend` (espejo) se sincroniza por
  fast-forward después, no en cada PR (decisión D-A2 del plan madre).
- **Jamás te detenés.** Lo que dependa de otro carril se simula en **tres niveles** —correcto ·
  límite · inválido— y se cierra contra el doble, declarándolo (regla 65).
- Un test tuyo en rojo detiene esa microtarea: se corrige o va `A MEDIAS` con las cuatro
  respuestas. Nunca `skip`, nunca `only`, nunca debilitar una aserción.

## 4. Plan

### H1 — La base es un hecho y el contrato de estado está publicado

**CA:** Dado el contrato publicado, cuando Justin o Pablo lo leen, entonces saben todas las
variantes y sus cargas útiles sin abrir el código; y el tipo real del repo quedó confirmado o
corregido respecto de la hipótesis heredada.
**DoD:** `entregables/contrato-view-state.md` en `dev` + test de exhaustividad en verde.
**Estado:** TODO

#### H1.S1 — Entorno y fuente verificados antes de decidir nada

**CA:** Dado el documento antecedente, cuando terminás esta subtarea, entonces el tipo de estado y
el organismo de diálogo quedaron localizados con archivo y línea, o registrados como inexistentes.
**DoD:** SHA y `git status` pegados, tabla de comandos completa, dos rutas confirmadas o refutadas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar remoto, rama `dev`, SHA, estado del árbol y cambios ajenos. **No se resetea nada** (AMB-F4) | El archivo trae el SHA real de hoy | `git rev-parse HEAD && git status --short` → salida pegada | TODO |
| H1.S1.M2 | Completar la tabla de comandos desde `package.json` y el lockfile; registrar versiones resueltas. **Prohibido actualizar una dependencia** | Cada alias tiene su comando real o la marca "no existe" | `cat package.json` → sección `scripts` pegada | TODO |
| H1.S1.M3 | Correr lint, typecheck, test y build y registrar el **rojo previo** | Los cuatro exit codes quedan escritos | `<CMD_LINT>; <CMD_TYPECHECK>; <CMD_TEST>; <CMD_BUILD>` → exit codes pegados | TODO |
| H1.S1.M4 | Localizar el tipo de estado y el organismo de diálogo resolviendo imports con el compilador, **no con grep suelto**; decidir por escrito si se adopta, se extiende o se extrae | Queda escrito cuál de las tres, con su motivo | `<CMD_TYPECHECK>` sobre un archivo de sondeo que los importa → exit 0 o error citado | TODO |

#### H1.S2 — El contrato de estado, releído y publicado

**CA:** Dado el tipo real, cuando se compara con la lista heredada de diez variantes, entonces cada
una queda `confirmada`, `no existe` o `se llama distinto`, y ninguna carga útil se pierde.
**DoD:** el documento publicado + `<CMD_TEST> --grep "estado"` → PASS.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Releer el tipo real y listar sus variantes con su carga útil, comparándolas contra las diez heredadas | Cada variante heredada queda marcada `confirmada`, `no existe` o `se llama distinto` | la tabla comparativa en `entregables/contrato-view-state.md` | TODO |
| H1.S2.M2 | Publicar el contrato en `dev` en la **primera hora**, en un PR con solo eso | El PR está mergeado y avisado en el daily de equipo §3 | `gh pr view --json state` → `MERGED`; aviso escrito en el daily | TODO |
| H1.S2.M3 | Test de exhaustividad que **falla** si se agrega una variante y no se maneja, o si se elimina una existente | Quitar una variante rompe el test | `<CMD_TEST> --grep "exhaustividad"` → PASS; caso negativo documentado | TODO |

### H2 — El contrato de estado se renderiza en un solo lugar

**CA:** Dadas dos vistas que hoy repiten las mismas ramas de estado, cuando adoptan el host,
entonces la rama se implementa una vez y cambiarla se hace en un solo archivo.
**DoD:** las dos vistas migradas + `<CMD_TEST>` de las variantes en verde.
**Estado:** TODO

#### H2.S1 — El host de estados

**CA:** Dado el host, cuando recibe una variante que no sabe renderizar, entonces falla de forma
visible en desarrollo, no la ignora en silencio.
**DoD:** `<CMD_TEST> --grep "host de estados"` → PASS incluido el caso de variante no manejada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | El host renderiza el contrato completo; el contenido de cada rama lo aporta el consumidor por plantilla con contexto tipado | Ninguna variante queda sin rama; el contexto de cada plantilla está tipado | `<CMD_TYPECHECK>` → exit 0; `<CMD_TEST> --grep "host de estados"` → PASS | TODO |
| H2.S1.M2 | Cuando el contrato las trae: la acción de siguiente paso del estado vacío, la marca de fecha del estado obsoleto y el identificador de petición del error | Las tres aparecen cuando el contrato las define, y no se inventan cuando no | test por variante → PASS | TODO |
| H2.S1.M3 | El host **no** traduce errores de transporte, no decide autorización y no elige endpoints: eso queda afuera | Ninguna dependencia de red, sesión ni políticas en el host | test de dependencias del host → PASS | TODO |

#### H2.S2 — Adopción y accesibilidad del estado

**CA:** Dadas dos ramas repetidas reales, cuando se reemplazan por el host, entonces su apariencia
no cambia sin explicación y el estado se **anuncia**, no solo se dibuja.
**DoD:** comparación visual de las dos vistas + spec de accesibilidad sin infracciones nuevas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Reemplazar dos ramas de estado repetidas reales por el host, conservando su apariencia | Las dos vistas compilan y sus tests pasan | `<CMD_TEST> --grep "<vista 1>|<vista 2>"` → PASS | TODO |
| H2.S2.M2 | Tests de las variantes en las dos vistas adoptantes, incluidos vacío y error | Cada variante tiene su caso | `<CMD_TEST> --grep "variantes"` → PASS con el conteo pegado | TODO |
| H2.S2.M3 | El cambio de estado se anuncia por región viva; el estado vacío **orienta** (dice por qué está vacío y qué hacer) y el de error es **accionable**, sin mostrar el error crudo del backend | Ningún estado mudo, ningún error crudo | spec de accesibilidad → PASS; capturas de vacío y error en `evidencia/` | TODO |

### H3 — El diálogo tiene anatomía, foco y una sola política de descarte

**CA:** Dado el diálogo abierto, cuando se cierra por botón, por `Escape` o por el fondo, entonces
las tres rutas pasan por la misma política de descarte y el foco vuelve al elemento que lo abrió.
**DoD:** E2E de las tres salidas con borrador sucio → PASS, salida pegada.
**Estado:** TODO

#### H3.S1 — Anatomía, foco y ciclo de vida

**CA:** Dado el diálogo, cuando está abierto, entonces el foco no puede salir a la página de atrás
y el overlay no recorta ni empuja a los elementos vecinos.
**DoD:** E2E de foco atrapado + capturas del apilamiento en los tres viewports.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Contrato del diálogo: título, contenido proyectado, acciones proyectadas, partes obligatorias y opcionales, cardinalidad y orden visual y accesible. **No se exponen todos los nodos internos como ranuras** | Un uso sin título o sin acciones se detecta por tipo o por test | `entregables/contrato-dialogo.md` + `<CMD_TYPECHECK>` → exit 0 | TODO |
| H3.S1.M2 | Foco: inicial dentro del diálogo, atrapado mientras está abierto, `Escape` cierra, y **restauración** al elemento que lo abrió | Recorrer con tabulador no sale del diálogo; al cerrar el foco vuelve | `<CMD_E2E> --grep "foco"` → PASS | TODO |
| H3.S1.M3 | Capa y apilamiento coherentes: sin recorte por contenedores con recorte, sin empujar a los vecinos cuando el requisito pide superposición | El diálogo se ve completo en los tres viewports | capturas en `evidencia/` miradas, con el caso del contenedor con recorte | TODO |
| H3.S1.M4 | Limpieza: componentes, escuchas, observadores y temporizadores se destruyen al cerrar, **también cuando el montaje falla** | Abrir y cerrar cien veces no deja escuchas acumuladas | test de ciclo de vida → PASS; conteo antes/después pegado | TODO |

#### H3.S2 — Una sola política de descarte, y dos modales reales

**CA:** Dado un borrador sucio, cuando se intenta cerrar por cualquiera de las tres rutas, entonces
aparece la misma protección; y ninguna ruta interna del diálogo la elude.
**DoD:** `<CMD_E2E> --grep "descarte"` → PASS con las tres rutas.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Elegir los **dos** modales reales a migrar y publicarlos en el daily de equipo §4 en la primera hora, sin chocar con las reservas de Richard ni de Justin | Los dos quedan escritos y confirmados por los otros dos carriles | el daily §4 nombra los dos archivos | TODO |
| H3.S2.M2 | Botón, `Escape` y clic en el fondo pasan por la **misma** política de descarte; ninguna ruta interna la saltea | Las tres rutas se comportan igual con el borrador sucio | `<CMD_E2E> --grep "descarte"` → PASS | TODO |
| H3.S2.M3 | Guardar es una **intención**: un error de guardado conserva el borrador y muestra el error asociado a su campo cuando el servidor lo identifica | Tras un error, lo cargado sigue ahí | `<CMD_TEST> --grep "error de guardado"` → PASS | TODO |

### H4 — El formulario tiene un dueño y dos modales lo demuestran

**CA:** Dado el formulario dentro del diálogo, cuando se pregunta quién es su dueño, entonces la
respuesta es una sola: o el contenedor pasa los controles tipados, o la vista mantiene el borrador
con un contrato explícito — **nunca las dos cosas a la vez**.
**DoD:** el contrato de formulario escrito + los dos modales migrados con sus E2E en verde.
**Estado:** TODO

#### H4.S1 — El contrato de borrador

**CA:** Dado un cambio externo de la entidad mientras alguien la está editando, cuando se resuelve,
entonces se aplica la política **escrita**, no una elegida en silencio.
**DoD:** `entregables/contrato-formulario.md` + test del caso de entidad cambiada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Declarar el dueño del formulario y dejar **uno solo** con el borrador autoritativo | No hay dos borradores compitiendo | `entregables/contrato-formulario.md` + revisión del diff | TODO |
| H4.S1.M2 | Preservar valores iniciales, campo tocado, campo modificado, validación, envío, bloqueo del doble envío, error remoto, cancelar, restablecer y reapertura | Cada uno tiene su caso de prueba | `<CMD_TEST> --grep "formulario"` → PASS con el conteo pegado | TODO |
| H4.S1.M3 | Política explícita para la entidad que cambia durante la edición: ni se pierde el borrador en silencio ni se guarda contra la entidad equivocada. **Si la política no está definida por producto, se registra como ambigüedad y se implementa la rama conservadora** | La política está escrita antes del código | test del caso → PASS o ambigüedad registrada con el supuesto | TODO |

#### H4.S2 — Adopción y verificación del carril

**CA:** Dado el reporte del carril, cuando alguien que no vio la sesión lo lee, entonces sabe qué se
verificó aislado, qué integrado, qué quedó bloqueado y qué **no** se ejercitó.
**DoD:** `entregables/PR8-carril.md` con peldaño de evidencia y sección "No cubierto".
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S2.M1 | Migrar el modal 1 al diálogo canónico con su contrato de borrador | Compila, sus tests pasan, su apariencia no cambió sin explicación | `<CMD_TEST> --grep "<modal 1>"` → PASS | TODO |
| H4.S2.M2 | Migrar el modal 2 | Compila y sus tests pasan | `<CMD_TEST> --grep "<modal 2>"` → PASS | TODO |
| H4.S2.M3 | E2E de foco, teclado y descarte en los dos modales + comparación visual contra el baseline en 3 viewports × 2 temas, con consola y red vigiladas | Los E2E pasan y ninguna diferencia visual queda sin explicar | `<CMD_E2E> --grep "<modal 1>|<modal 2>"` → PASS; reporte de comparación en `evidencia/` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| AMB-F3 | Que el tipo de estado tenga diez variantes y esos nombres — hipótesis heredada de `mantra-core-health`, no confirmada en Pasanaku | Tu baseline (H1.S2.M1), contra el tipo real de `packages/ui` o del `nucleo` de las apps | El contrato que publican Justin y Pablo | Se lee el tipo real primero; la lista heredada se confirma o se corrige (corrección 2026-09-21: el documento antecedente es de otro proyecto, sirve solo de guía) |
| AMB-F5 | A qué rama se integra el trabajo | Dueño del repo frontend | La integración final | **Resuelta 2026-09-21:** PR contra `dev` (rama real). `PasanakuFrontend` (espejo) se sincroniza por fast-forward |
| AMB-F7 | Que los dos modales no choquen con las reservas de Richard y Justin | Coordinación, primera hora | La reserva de archivos | El primero que publica se la queda |
| Q-L1 | Qué debe pasar con un borrador cuando la entidad cambia mientras se edita | Producto | H4.S1.M3 | Se implementa la rama conservadora (no se pierde lo cargado, no se guarda contra la entidad vieja) y se registra como decisión pendiente |
| Q-L2 | Si la proyección de contenido alcanza o hace falta una plantilla diferida para el contenido del diálogo | Tu verificación en la versión instalada | La anatomía del diálogo | Se comprueba el comportamiento en **la versión instalada**, no se copia de una versión posterior |
| Q-L3 | Si algún modal existente evita a propósito la protección de descarte por una razón de producto | Producto | La política única | Ante la duda se protege y se registra; quitar una protección sería un cambio de comportamiento |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia. Regla 65: si el contrato se puede nombrar, se simula en tres niveles y se cierra.
- [ ] El contrato de estado publicado en la primera hora y avisado en el daily de equipo.
- [ ] Ninguna variante del contrato de estado perdida por el camino.
- [ ] Las tres rutas de cierre del diálogo pasan por la misma política de descarte, demostrado.
- [ ] `<CMD_LINT>`, `<CMD_TYPECHECK>`, `<CMD_TEST>`, `<CMD_E2E>` y `<CMD_BUILD>` corridos con exit
      code pegado — incluido el rojo.
- [ ] Peldaño de evidencia declarado por área (regla 30).
- [ ] Sin datos clínicos ni identificatorios reales en fixtures, capturas, logs ni evidencia.

## 7. Revisión adversarial antes de cerrar

1. ¿Un cierre evita la protección de cambios sin guardar por alguna ruta interna?
2. ¿Un cambio externo pierde un borrador o una respuesta vigente?
3. ¿Una salida se llama éxito aunque solo se emitió una solicitud?
4. ¿El contrato proyectado permite usos inválidos que ningún chequeo detecta?
5. ¿El contenedor vacío del diálogo se presentó como prueba del organismo?
6. ¿El host de estados se convirtió en un selector de veinte dominios para justificar un componente universal?
7. ¿Se mantienen dos borradores autoritativos, uno en el contenedor y otro en la vista?
8. ¿Se declara verificado algo que solo fue inspeccionado estáticamente?
