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

## Conclusión parcial

El catálogo de Pasanaku **ya cumple, por lectura, la dimensión de fuente** (importa lo canónico, no
copia) — el escenario más grave que el kill-test #1 buscaba no se encontró. La dimensión de
**aislamiento es la que más probablemente falla** hoy (es una ruta normal, no un entorno separado),
pero eso todavía no está demostrado con una prueba ejecutada — es el trabajo real que sigue.
