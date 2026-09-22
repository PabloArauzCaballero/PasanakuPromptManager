# Auditoría del catálogo real — H1.S2 (bloque B, `PR10-CatalogoYGates.Frontend`)

Auditado 2026-09-21 contra `Pasanaku/PasanakuFrontend` @ `a23bcb1`. Cada afirmación cita archivo y
línea, tal como exige H1.S2.M1. **Peldaño: `DISCOVERED`/lectura de código, salvo donde se indica una
comprobación ejecutada.**

## H1.S2.M1 — Cómo carga hoy el catálogo, de dónde toma los estilos, qué responsabilidades mezcla

- **Entrada:** `packages/ui/src/catalogo/catalogo.ts:10-30` — componente `Catalogo`, standalone,
  `OnPush`, importa `CatalogoAtomos`, `CatalogoMoleculas`, `CatalogoOrganismos` (tres sub-secciones).
- **Montaje en el producto:** `apps/web/src/app/app.routes.ts:180` — ruta `catalogo` con
  `loadComponent` (carga diferida) dentro de las rutas normales de `apps/web`, marcada como no
  indexable (`app.routes.ts:11`, `ADR-042`), **pero sin ningún mecanismo de aislamiento**: es una
  ruta más del árbol de rutas del sitio.
- **Fuente de los componentes:** `packages/ui/src/catalogo/catalogo-atomos.ts:2-24` — importa
  directamente `Boton` de `../boton/boton`, `Campo` de `../campo/campo`, `CampoMonto` de
  `../campo-monto/campo-monto`, etc. **Es la implementación canónica, no una copia**: no hay HTML,
  TypeScript ni CSS duplicado dentro de `catalogo/`. Esto contradice la hipótesis heredada del
  documento antecedente (que asumía una demo con recreaciones) — el catálogo de Pasanaku ya nace
  bien en este punto.
- **Datos:** `catalogo-atomos.ts:34-55` usa strings realistas del dominio ("Confirmar aporte de Bs
  250", "Cancelar", "Ver el grupo"), no lorem ipsum ni colecciones vacías — coincide con lo que pide
  el kill-test de H2.S1.M1.
- **Responsabilidades mezcladas:** el componente `Catalogo` mezcla navegación (`<nav>` con anclas),
  composición de secciones y estilos inline (`catalogo.ts:23-28`) en un solo archivo. No es una capa
  de arranque separada de la de contenido — punto a revisar en H3/H4 del carril, no corregido acá.

## H1.S2.M2 — ¿El nodo del preview comparte inyectores o servicios con el anfitrión?

**No ejecutado todavía como comprobación E2E — esto es lectura de código, no la comprobación que
exige el DoD.** Lo que la lectura muestra:

- El catálogo se monta con `loadComponent` **dentro** de `apps/web/src/app/app.routes.ts`, en el
  mismo árbol de rutas que el resto del sitio (login, panel, formularios reales). No hay una entrada
  HTML separada, ni un `bootstrapApplication` propio, ni un iframe.
- Consecuencia esperable (a confirmar con una prueba real, no asumida como hecho): el catálogo
  **comparte** el mismo `ApplicationRef`, el mismo inyector raíz, el mismo router y — si la sesión
  vive en un servicio Angular o en `localStorage` del mismo origen — la misma sesión que el resto
  del sitio. Esto **fallaría** el segundo kill-test del encargo ("iniciar sesión sintética en el
  preview y mirar la pestaña del anfitrión").
- **Pendiente real:** escribir y correr la comprobación ejecutable (spec de aislamiento) que exige
  el DoD de H1.S2.M2 antes de afirmar esto como demostrado. Lo de arriba es una hipótesis fundada en
  lectura de código, marcada explícitamente como tal — no se presenta como verificado (regla 30).

## H1.S2.M3 — Generador de props sintéticas: contratos mal rellenados

No localizado todavía. `catalogo-atomos.ts` no usa un generador de props: las props están escritas
a mano en el template (ver ejemplo arriba). Si existe un generador de datos sintéticos en otro lado
del árbol (`packages/simulado`, por ejemplo), no se buscó todavía — pendiente de H1.S2.M3 real.

## Hallazgo estructural (2026-09-22): el catálogo real no es un playground editable

Al intentar avanzar H3 (factories/hosts tipados, edición de inputs, ciclo de vida del montaje) y
H4 (preview aislado, mensajería entre ventanas), encontré que **el catálogo real de Pasanaku no es
un Storybook con controles editables ni un preview en iframe**: es una página estática
(`packages/ui/src/catalogo/catalogo-atomos.ts` y hermanos) que monta cada pieza **una vez**, con
props fijas escritas en el template. No hay:

- un panel para editar props en vivo (H3.S2 asume que sí — "dada una edición inválida de una
  entrada, cuando el catálogo la aplica" no tiene sentido si no hay edición);
- una entrada de preview separada, iframe, ni arranque propio (H4 completo asume esto);
- un manifiesto de escenarios con factories tipadas (H3.S1 asume esto — no existe tal manifiesto,
  las props están escritas a mano directamente en `catalogo-atomos.ts`/`-moleculas.ts`/`-organismos.ts`).

**Esto no es un defecto para arreglar dentro de este carril**: construir un playground editable con
preview aislado es una **funcionalidad nueva**, no una auditoría ni una corrección — semanas de
trabajo real (nuevo bootstrap, nuevo build target, mensajería entre ventanas, edición de props con
validación), no algo que se decide solo (regla 00 §1.5: "si no existe patrón previo, registrá la
decisión técnica"). El documento antecedente (`mantra-core-health`) sí tenía ese tipo de
arquitectura — de ahí que `H3`/`H4` la asuman —, pero Pasanaku no la construyó así.

**Microtareas de `H3` y `H4` afectadas (14 de las 38):** todas menos las que ya se resolvieron por
lectura/prueba directa (fuente, composición, interacción, el "no hay iframe"). Quedan `BLOQUEADO`
con esta causa, no `TODO`: no es que falte ejecutarlas, es que su premisa no aplica al catálogo real
sin construir la funcionalidad que asumen.

## Conclusión parcial

El catálogo de Pasanaku **ya cumple, por lectura, la dimensión de fuente** (importa lo canónico, no
copia) — el escenario más grave que el kill-test #1 buscaba no se encontró. La dimensión de
**aislamiento es la que más probablemente falla** hoy (es una ruta normal, no un entorno separado),
pero eso todavía no está demostrado con una prueba ejecutada — es el trabajo real que sigue.
