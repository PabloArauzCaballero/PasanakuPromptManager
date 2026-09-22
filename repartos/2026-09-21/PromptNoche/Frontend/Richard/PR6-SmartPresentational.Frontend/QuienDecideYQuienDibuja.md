# Quién decide y quién dibuja: la pantalla piloto con su estado con dueño y su plantilla declarativa

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía: todo está en `TODO` a propósito.

- **Persona:** Richard · **Turno:** noche · **Área:** frontend · **Fecha:** 2026-09-21
- **Daily del equipo:** [Daily-Noche-2026-09-21.md](../../../Daily-Noche-2026-09-21.md) · **Tu daily:** [Richard-Daily-Noche-2026-09-21.md](../Richard-Daily-Noche-2026-09-21.md)
- **Encargo madre:** prompt maestro de refactorización frontend. Este carril cubre sus §3 (responsabilidad), §4 (propiedad del estado), §5 (código limpio y declarativo) y la fase 2 del §14, sobre **una** pantalla piloto.
- **Repo:** `https://github.com/mdavila-2001/mantra-core-health` · rama base **`mockup`** (no `dev`, no la rama por defecto) @ **el SHA que registres vos en H1.S1.M1** · **tu rama:** `richard/feature/carril-PR6-smart-presentational`
- **4 hitos · 7 subtareas · 24 microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` de este repo estándar dentro de `mantra-core-health/`. Si ese repo
   trae su propio `AGENTS.md` o `CLAUDE.md`, **ese manda sobre estas reglas** (jerarquía de
   `.claude/rules/README.md`): lo que choque se registra como ambigüedad, no se resuelve solo.
2. Entrá por `skills-router` y cargá **solo** las skills de la tabla. No leas el catálogo entero.
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Cargalas por nombre.

| Skill | Para qué en este encargo |
|---|---|
| `smart-dumb-components` | El eje del carril: qué decide el contenedor y qué dibuja la presentación |
| `angular-signals-state` | `computed` en vez de copias; cuándo NO usar `effect`; dónde vive cada dato |
| `component-architecture-solid` | Responsabilidad única y dependencias explícitas sin inventar capas |
| `frontend-ux-states` | Los cuatro estados obligatorios de una vista que depende de red |
| `angular-development` | Control flow, `input()`/`output()`, DI con `inject()`, OnPush |
| `angular-testing` | `setInput`, `whenStable`, harness: probar por la interfaz del consumidor |
| `visual-proof` | La captura se mira, no solo se toma |
| `scope-discipline` | Lo roto fuera de alcance se anota, no se arregla |
| `evidence-and-verification` | Qué podés afirmar con qué salida pegada |
| `finish-your-turn` | Cierre con avance calculado |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 60 · 65 · **95** (frontend) · 90.2 leída
como dato **clínico e identificatorio** (AMB-F2). **No aplican** la 91 (dinero) ni la 98
(microservicios): este repo no es Pasanaku.

## 2. Resultado observable

Una pantalla piloto del producto queda partida en un contenedor que conecta ruta, caso de uso y
efectos, y componentes de presentación que reciben un contrato tipado y emiten intenciones; su
plantilla se lee como una descripción de regiones y acciones; cada estado mutable tiene un dueño
escrito; y la pantalla se ve y se comporta **igual que antes** en tres viewports y en los dos
temas, demostrado contra el baseline capturado antes de tocarla.

**Kill-test:** buscar en el componente de presentación una dependencia que llegue —directa o
transitivamente— a un cliente HTTP de negocio, a la sesión o al almacenamiento. Si aparece una,
esto NO está hecho, por más carpetas `presentational/` que haya.

## 3. Alcance

**IN:** la pantalla piloto que elijas en H1.S2.M1 y los componentes que solo ella usa; su contrato
de vista; su spec; el baseline visual y funcional de su ruta; `entregables/estado-<pantalla>.md`.

**OUT:** el organismo tabla y sus consumidores (Justin, PR7). `ViewState`, `ContentDialog` y el
contrato de borrador (Leo, PR8). El generador del índice de componentes y el grafo de usos
(Marcelo, PR9). `component-stock`, el preview y los workflows de CI (Pablo, PR10). Los tokens del
sistema de diseño: **no se toca una variable de color, espaciado ni tipografía**. Ninguna
actualización de dependencias, ningún gestor de paquetes distinto del que declare el lockfile,
ninguna librería nueva. `main` y `dev` no se tocan.

**Reservas de archivos:** la pantalla piloto que publiques en H1.S2.M1 y los componentes privados
de esa pantalla. Esa pantalla **no puede ser** uno de los dos consumidores que migra Justin: el
que publique primero en el daily de equipo se la queda, y el otro elige otra (AMB-F7).

### Comandos del repo — candidatos heredados, se confirman en H1.S1.M2

El documento antecedente mencionaba estos scripts. **Son hipótesis**: leé `package.json` y usá el
alias real. Si un alias no existe, **no lo inventes ni lo crees**: usá el binario que el repo ya
trae y anotá la diferencia en tu daily.

| Alias | Candidato heredado | Cómo se confirma |
|---|---|---|
| `CMD_LINT` | `yarn lint` | `package.json` → `scripts` |
| `CMD_TYPECHECK` | `yarn typecheck` | `package.json` → `scripts` |
| `CMD_TEST` | `yarn test` (Vitest) | `package.json` + config del runner |
| `CMD_BUILD` | `yarn build` | `package.json` → `scripts` |
| `CMD_E2E` | `yarn pw` (Playwright) | `package.json` + config de Playwright |

### Ritual de entrega

```bash
git fetch origin && git checkout -b richard/feature/carril-PR6-smart-presentational origin/mockup
# por cada subtarea cerrada con su gate local en verde:
git fetch origin && git rebase origin/mockup
<CMD_LINT> && <CMD_TYPECHECK> && <CMD_TEST>
git push -u origin HEAD
gh pr create --base mockup --fill --title "refactor(<pantalla>): <subtarea>"
```

- **PR contra `mockup`.** A `main` y a `dev` no se toca (AMB-F5, `DECISION_REQUIRED`).
- **Jamás te detenés.** Si necesitás algo de otro carril que todavía no está en `mockup`, nombrás
  el contrato, construís el doble en **tres niveles** —correcto · límite · inválido—, cerrás contra
  el doble **declarándolo** en tu daily §4/§5 y dejás diferida la microtarea de integración
  (regla 65). Mientras el contrato de Leo no esté, consumís el tipo de estado **actual** del repo.
- Un fallo previo del repo, registrado en tu baseline, **no es una regresión tuya** ni te detiene:
  va a tu daily §6 como hallazgo con ruta.
- Un test tuyo en rojo sí detiene esa microtarea: se corrige o va `A MEDIAS` con las cuatro
  respuestas. Nunca `skip`, nunca `only`, nunca bajar una aserción.

## 4. Plan

### H1 — La base es un hecho registrado, no un recuerdo

**CA:** Dado el repo recién clonado, cuando alguien lee `evidencia/baseline.md`, entonces sabe el
SHA, las versiones resueltas, los comandos que de verdad existen, qué estaba rojo antes de que
tocaras nada, y cuál es la pantalla piloto con su apariencia y su comportamiento previos.
**DoD:** `evidencia/baseline.md` con las salidas literales de los cuatro comandos y las capturas
de la pantalla piloto en tres viewports × dos temas × tres estados, en `evidencia/`.
**Estado:** TODO

#### H1.S1 — Entorno y fuente verificados antes de decidir nada

**CA:** Dado el documento antecedente, cuando terminás esta subtarea, entonces cada ruta heredada
quedó confirmada con archivo y línea, o refutada por escrito.
**DoD:** `git rev-parse HEAD` y `git status --short` pegados, tabla de comandos reales completa, y
las cuatro rutas heredadas marcadas `confirmada` o `no existe`.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Registrar remoto, rama `mockup`, SHA, estado del árbol y cambios ajenos en `evidencia/baseline.md`. **No se resetea nada**: el SHA del documento original es referencia histórica (AMB-F4) | El archivo trae el SHA real de hoy, no el heredado | `git rev-parse HEAD && git status --short` → salida pegada | TODO |
| H1.S1.M2 | Completar la tabla de comandos leyendo `package.json` y el lockfile; registrar versiones resueltas de Angular, TypeScript y el gestor de paquetes. **Prohibido actualizar una dependencia para facilitar el refactor** | Cada alias tiene su comando real o la marca "no existe" | `cat package.json` → sección `scripts` pegada | TODO |
| H1.S1.M3 | Correr lint, typecheck, test y build y registrar el **rojo previo** como baseline de fallos | Los cuatro exit codes quedan escritos, verdes o rojos | `<CMD_LINT>; <CMD_TYPECHECK>; <CMD_TEST>; <CMD_BUILD>` → cuatro exit codes pegados | TODO |
| H1.S1.M4 | Confirmar o refutar las rutas heredadas que toca este carril (el contrato de estado, el componente de directorio y el de tabla) resolviendo imports con el compilador, **no con grep suelto** | Cada una queda `confirmada en <ruta:línea>` o `no existe` | `<CMD_TYPECHECK>` sobre un archivo de sondeo que las importa → exit 0 o error citado | TODO |

#### H1.S2 — La pantalla piloto, elegida y fotografiada antes de tocarla

**CA:** Dado el baseline, cuando se compare al final del carril, entonces existe una captura previa
por viewport, tema y estado, tomada con los mismos datos, reloj y locale.
**DoD:** capturas en `evidencia/baseline-visual/` + E2E dirigido de la ruta con su salida.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Elegir la pantalla piloto con criterio escrito (cantidad de consumidores de sus piezas y cantidad de reglas repetidas, no gusto) y **publicarla en el daily de equipo §4 dentro de la primera hora** | La pantalla queda escrita en el daily de equipo y no coincide con ningún consumidor de Justin | El daily de equipo §4 nombra la ruta y el archivo; Justin confirmó por escrito que no es suyo | TODO |
| H1.S2.M2 | Capturar el baseline visual: 3 viewports (móvil estrecho, tablet, escritorio) × tema claro y oscuro × estados carga, vacío y error | 18 capturas existen y **las miraste** | `<CMD_E2E>` del spec de capturas → exit 0; archivos listados en `evidencia/baseline-visual/` | TODO |
| H1.S2.M3 | Capturar el baseline funcional: E2E dirigido de la ruta con datos sintéticos deterministas. Si no existe uno, escribir el mínimo que ejercite entrar, ver datos y usar la acción principal | El E2E pasa **antes** de tocar código, o se registra su fallo previo | `<CMD_E2E> --grep "<ruta>"` → salida pegada con exit code | TODO |
| H1.S2.M4 | Registrar errores de consola y respuestas 4xx/5xx **previos** de esa ruta | La lista previa queda escrita; lo que ya estaba no se te imputa después | salida del spec con el recolector de consola y red → pegada | TODO |

### H2 — Cada estado mutable de la pantalla tiene un dueño escrito

**CA:** Dado `entregables/estado-<pantalla>.md`, cuando se lee cualquier fila, entonces responde
quién lo crea, quién puede cambiarlo, quién lo lee, qué lo invalida y cuándo se destruye; y ningún
hecho está representado dos veces con sincronización manual.
**DoD:** la tabla completa + los tests dirigidos de las derivaciones en verde, salida pegada.
**Estado:** TODO

#### H2.S1 — El inventario del estado, con las cinco preguntas respondidas

**CA:** Dado cada `signal`, campo de formulario, parámetro de ruta y dato derivado de la pantalla,
cuando se busca en la tabla, entonces está, con su dueño y su regla de sincronización.
**DoD:** la tabla no tiene celdas vacías; cada fila cita archivo y línea.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Listar todo estado mutable de la pantalla y responder las cinco preguntas por fila, citando archivo y línea | Ninguna celda vacía; toda fila con ruta | `entregables/estado-<pantalla>.md` existe y ninguna fila dice "no sé" | TODO |
| H2.S1.M2 | Marcar los hechos representados **dos veces** (contadores, visibilidad, selección visible, etiquetas calculadas) que hoy se sincronizan a mano en varios handlers | Cada copia queda citada con archivo y línea | la tabla trae una columna "copia manual" con al menos las ocurrencias halladas o la marca "ninguna" | TODO |
| H2.S1.M3 | Marcar los `effect` que copian un estado derivable y proponer, por escrito, la derivación que los reemplaza | Cada `effect` queda clasificado: derivable o sincronización necesaria con API imperativa | la tabla distingue los dos tipos; los necesarios declaran entrada, recurso y limpieza | TODO |

#### H2.S2 — Derivaciones en vez de copias, sin cambiar comportamiento

**CA:** Dado el mismo flujo de usuario, cuando se reemplaza una copia por una derivación, entonces
la pantalla se comporta igual y el test dirigido lo demuestra.
**DoD:** `<CMD_TEST>` del spec de la pantalla → PASS, salida pegada.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Reemplazar la primera copia manual por una derivación de solo lectura; test que falla si vuelve a existir la copia | El test dirigido pasa y el handler ya no asigna ese valor | `<CMD_TEST> --grep "<pantalla>"` → PASS | TODO |
| H2.S2.M2 | Reemplazar el `effect` de copia por la derivación; dejar solo los efectos con API imperativa real, cada uno con su limpieza | No queda ningún `effect` cuyo cuerpo solo escriba otro estado | mismo comando → PASS; revisión del diff sin `effect` de copia | TODO |
| H2.S2.M3 | Identidad estable en la iteración de la colección principal: clave por identidad, **no por índice**, donde los elementos cambian de posición | Reordenar la colección no pierde foco ni estado local de fila | test de reordenamiento → PASS | TODO |

### H3 — El contenedor decide y la presentación dibuja

**CA:** Dado el componente de presentación, cuando se resuelven sus dependencias directas y
transitivas, entonces no llega a ningún cliente de negocio, sesión ni almacenamiento; y sus salidas
se llaman como intenciones, no como resultados.
**DoD:** test de dependencias que falla si aparece una prohibida + `<CMD_TEST>` en verde.
**Estado:** TODO

#### H3.S1 — El contenedor: ruta, caso de uso, efectos y concurrencia

**CA:** Dado el contenedor, cuando dispara una operación asíncrona, entonces la semántica elegida
(reemplazar la anterior, serializar, o impedir el envío simultáneo) está declarada por escrito y
demostrada con un test.
**DoD:** `<CMD_TEST> --grep "<contenedor>"` → PASS con el caso de carrera incluido.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Definir el contrato de vista tipado que el contenedor entrega a la presentación: sin `any`, sin doble cast, sin aserción no nula sistemática | `<CMD_TYPECHECK>` en verde sin supresiones nuevas | `<CMD_TYPECHECK>` → exit 0; `grep` de supresiones nuevas en el diff → vacío | TODO |
| H3.S1.M2 | Mover al contenedor la navegación, la invocación del caso de uso y los efectos que hoy viven en la presentación | La presentación deja de importar esas piezas | `<CMD_TEST>` → PASS; el diff muestra los imports movidos | TODO |
| H3.S1.M3 | Declarar y aplicar la semántica de concurrencia de la operación de lectura principal (una búsqueda nueva reemplaza a la anterior) con un test de respuesta atrasada | Una respuesta vieja **no** reemplaza a la vigente | test de respuesta atrasada → PASS | TODO |
| H3.S1.M4 | Impedir el doble envío de la operación de escritura sin cancelar la petición en vuelo: cancelar la suscripción **no** cancela la operación en el servidor | Dos clics seguidos producen una sola operación | test de doble clic → PASS | TODO |

#### H3.S2 — La presentación: contrato adentro, intención afuera

**CA:** Dado un consumidor del componente de presentación, cuando lo usa, entonces no necesita
conocer clases CSS privadas, orden de llamadas internas ni inspeccionar el DOM del hijo.
**DoD:** los tests atraviesan la interfaz pública; `<CMD_TEST>` en verde.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Test de dependencias del componente de presentación: falla si un import directo o transitivo llega a un cliente de negocio, a la sesión o al almacenamiento | El test existe y pasa; si hoy falla, es el kill-test del carril y se corrige | `<CMD_TEST> --grep "dependencias"` → PASS | TODO |
| H3.S2.M2 | Renombrar las salidas a nombres de intención: lo que sale de la UI es una solicitud, nunca un resultado que todavía no ocurrió | Ninguna salida afirma un éxito que la UI no puede conocer | revisión del contrato + `<CMD_TYPECHECK>` → exit 0 | TODO |
| H3.S2.M3 | Test que demuestra que el componente **no muta** el objeto de entrada que recibe | Mutar la entrada hace fallar el test | `<CMD_TEST> --grep "no muta"` → PASS | TODO |

### H4 — La paridad está demostrada, no supuesta

**CA:** Dada la pantalla refactorizada, cuando se compara contra el baseline de H1.S2 con el mismo
navegador, viewport, tema, locale, reloj y datos, entonces no hay diferencia visual no explicada, y
la consola y la red no tienen errores nuevos.
**DoD:** comparación visual con artefactos + E2E dirigido PASS + lista de errores de consola igual
o menor que la del baseline.
**Estado:** TODO

#### H4.S1 — Verificación y cierre del carril

**CA:** Dado el reporte del carril, cuando alguien que no vio la sesión lo lee, entonces sabe qué
se verificó, con qué comando, y qué quedó **sin** ejercitar.
**DoD:** `entregables/PR6-carril.md` con peldaño de evidencia declarado y sección "No cubierto".
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Tests de contrato del presentational: entradas, cambios externos, eventos, estado local y limpieza | Los casos nuevos pasan y ninguno se acopla a nombres privados | `<CMD_TEST> --grep "<presentational>"` → PASS con el conteo pegado | TODO |
| H4.S1.M2 | E2E dirigido de la ruta + consola y red revisadas; los errores inesperados **hacen fallar** el test, no se ignoran | El E2E pasa y la lista de errores no creció respecto de H1.S2.M4 | `<CMD_E2E> --grep "<ruta>"` → PASS; lista de consola comparada y pegada | TODO |
| H4.S1.M3 | Comparación visual contra el baseline (3 viewports × 2 temas × 3 estados). **Prohibido actualizar el baseline o ampliar tolerancias** para tapar una diferencia | Cada diferencia está explicada o corregida; ninguna silenciada | reporte de comparación en `evidencia/` con las capturas antes/después | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| AMB-F3 | Las rutas del documento antecedente son hipótesis, no hechos | Tu propio baseline (H1.S1.M4) | Nada, si las confirmás primero | Ninguna se usa hasta estar confirmada con archivo y línea |
| AMB-F5 | A qué rama se integra el trabajo | Dueño del repo frontend | La integración final | PR contra `mockup`; `main` y `dev` no se tocan |
| AMB-F7 | Cuál es la pantalla piloto y que no choque con los consumidores de Justin | Coordinación, primera hora | La reserva de archivos | El primero que la publica en el daily §4 se la queda |
| Q-R1 | Si la pantalla piloto usa el organismo tabla que Justin va a reemplazar | Justin + coordinación | La migración final de esa pieza | Trabajás contra la tabla **actual**; la adopción de la nueva queda diferida y declarada, no forzada |
| Q-R2 | Si el repo tiene un contrato de estado con diez variantes o uno más pobre | Leo (PR8) publica el contrato en la primera hora | El tipado del contrato de vista | Consumís el tipo actual del repo; si Leo publica antes de que cierres H3, lo adoptás; si no, queda declarado |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia. Recordá la regla 65: si el contrato de lo que falta se puede nombrar, se simula en
      tres niveles y se cierra contra el doble.
- [ ] Baseline capturado **antes** de tocar y comparación hecha **después**, con las capturas miradas.
- [ ] Ningún componente de presentación con dependencia prohibida, directa o transitiva.
- [ ] Ningún hecho representado dos veces con sincronización manual dentro del alcance.
- [ ] `<CMD_LINT>`, `<CMD_TYPECHECK>`, `<CMD_TEST>` y `<CMD_E2E>` corridos, con exit code pegado
      — incluido el rojo.
- [ ] Peldaño de evidencia declarado por área (regla 30). Sin inspección visual, el techo es
      `VERIFIED_FUNCTIONAL_ONLY`.
- [ ] Sin datos clínicos ni identificatorios reales en fixtures, capturas, logs ni evidencia.

## 7. Revisión adversarial antes de cerrar

Respondé con evidencia; cualquier respuesta que deje un escape se corrige antes de cerrar:

1. ¿Se podría aprobar este cambio **moviendo archivos** sin cambiar responsabilidades?
2. ¿El componente gigante se convirtió en una fachada gigante?
3. ¿La presentación consigue negocio por una dependencia indirecta con nombre inocente?
4. ¿Hay dos estados que representan el mismo hecho y dependen de sincronización manual?
5. ¿El componente nuevo necesita saber **qué pantalla** lo usa para decidir su conducta?
6. ¿Una salida se llama éxito aunque solo se emitió una solicitud?
7. ¿Un cambio externo pierde un borrador, una selección o una respuesta vigente?
8. ¿Se declara verificado algo que solo fue inspeccionado estáticamente?
