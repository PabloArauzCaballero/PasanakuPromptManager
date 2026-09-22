# Contrato de estado de pantalla — releído contra el código real (H1.S2.M1)

> **Peldaño de evidencia:** `DISCOVERED` (regla 30). Todo lo que sigue está citado con ruta y
> línea del repo real `PasanakuBackend`, leído el 2026-09-22, SHA `a23bcb117effe7ce66d069a97ebd2c25c8390306`
> (rama `dev` remota, ver `H1.S1.M1`). **No hay un tipo de estado (`ViewState`/enum) separado en el
> repo**: lo que documenta este archivo es el contrato real que ya existe, repartido en dos
> organismos de `packages/ui/src`.

## 0. Corrección de la hipótesis heredada (AMB-F3)

El documento antecedente (otro proyecto, usado solo como plantilla de estructura) supone **diez**
variantes con nombre propio: pendiente de autenticación de ruta, cargando, vacío, listo,
validación, sin permiso, no encontrado, obsoleto, sin conexión y error.

**Eso no existe así en Pasanaku.** Lo que existe es:

- Un organismo `EstadoDePantalla<T>` (`packages/ui/src/estado-de-pantalla/estado-de-pantalla.ts`)
  que resuelve **cuatro ramas** sobre un `ResourceRef<T>` de Angular: `cargando` (línea 21),
  `error` (línea 25), `vacío` (línea 31, incluye el caso `idle` — sin petición todavía, línea 63) y
  `listo` (línea 36, `<ng-content>`).
- Un organismo `EstadoVacio` (`packages/ui/src/estado-vacio/estado-vacio.ts`) que **no es una rama
  del host**: es una molécula de contenido para pintar *dentro* de la rama vacía o en listas, con
  un `motivo: MotivoVacio` (`'sinDatos' | 'porFiltro' | 'porPermiso'`, línea 4 de
  `estado-de-pantalla.ts`) que trae su propio texto de "por qué" y su acción (líneas 34-47 de
  `estado-vacio.ts`).
- Un tipo de carga útil de error, `ErrorTraducido` (línea 7 de `estado-de-pantalla.ts`):
  `{ mensaje: string; trazaId?: string; sinConexion?: boolean; estado?: number }`. **`sinConexion`
  y `estado` (código HTTP) viajan como *propiedades del error*, no como ramas propias.**

## 1. Tabla comparativa — heredada vs. real

| Variante heredada (AMB-F3) | Veredicto | Evidencia |
|---|---|---|
| Pendiente de autenticación de ruta | **No existe** | No hay ninguna rama de "auth pendiente" en `estado-de-pantalla.ts` ni en `estado-vacio.ts`. Es responsabilidad de un guard de ruta (fuera de este organismo) — no localizado ningún `CanActivate`/resolver equivalente en el alcance de este carril; no se afirma su existencia ni su ausencia fuera de `packages/ui`. |
| Cargando | **Confirmada** | `estado-de-pantalla.ts:21` — `@if (recurso().isLoading())`, con `etiquetaDeCarga()` accesible (`role="status"`, línea 22). |
| Vacío | **Confirmada, con matiz** | `estado-de-pantalla.ts:31` decide *que* está vacío (predicado `vacio()` + `idle`, línea 59-68); el *contenido* del vacío (por qué + acción) lo pinta `EstadoVacio` (otro organismo, no una plantilla de esta rama) o el propio consumidor con `mensajeVacio` (input string simple, línea 54, no una plantilla). |
| Listo | **Se llama distinto — "con datos" es la rama `else` (`ng-content`)** | `estado-de-pantalla.ts:36`. No tiene nombre propio en el código; es simplemente el contenido proyectado por defecto. |
| Validación | **No existe como rama de este host** | Es un caso de `H4` (contrato de formulario), no del host de pantalla. No hay rama de "validación" en `estado-de-pantalla.ts`. |
| Sin permiso | **Se llama distinto — es un `MotivoVacio`, no una rama propia** | `estado-vacio.ts:4,46`: `'porPermiso'` es un motivo *dentro* de la rama vacía, con texto fijo ("Tu rol no puede ver esta información.") y sin acción. Un 403 real del backend no está mapeado automáticamente a este motivo: alguien tiene que decidirlo y pasarlo. |
| No encontrado | **No existe como rama propia — cae en `error` con `estado: 404`** | `ErrorTraducido.estado?: number` (línea 7) permite transportar el código HTTP, pero `estado-de-pantalla.ts` no distingue 404 de 500 en su plantilla (líneas 25-30): ambos pintan el mismo bloque `role="alert"` con el mismo botón "Volver a intentar" — reintentar un 404 no tiene sentido y hoy no se filtra. |
| Obsoleto | **No existe** | Ningún campo de "dato desactualizado" ni de fecha de corte en `ErrorTraducido` ni en `EstadoDePantalla`. Si una vista necesita indicar que el dato mostrado quedó viejo, hoy no hay dónde ponerlo. |
| Sin conexión | **Confirmada como propiedad del error, no como rama propia** | `ErrorTraducido.sinConexion?: boolean` (línea 7) existe en el tipo, pero la plantilla (líneas 25-30) no lo usa: no hay texto ni icono distinto para sin conexión vs. error genérico. El campo está declarado y no consumido — es carga útil sin plantilla. |
| Error | **Confirmada** | `estado-de-pantalla.ts:25-30`, `role="alert"`, mensaje traducido (`error()` computed, línea 70-74, con fallback genérico si el interceptor no adjuntó `mensaje`) + `trazaId` opcional (línea 28) + botón "Volver a intentar" (línea 29). **No expone el error crudo del backend** (regla 95.2.3): siempre pasa por `ErrorTraducido`. |

## 2. Contrato real vigente (lo que hay que preservar, no reducir)

Reducir esto a `cargando/error/éxito` está expresamente prohibido por el encargo, y además sería
**menos** de lo que ya existe hoy: el repo ya tiene cargando / error (con `trazaId` y `sinConexion`
como carga útil) / vacío (con motivo y acción) / listo. Cuatro ramas de primer nivel, dos de ellas
con carga útil rica.

```ts
// packages/ui/src/estado-de-pantalla/estado-de-pantalla.ts (real, no propuesto)
export type MotivoVacio = 'sinDatos' | 'porFiltro' | 'porPermiso'
export type ErrorTraducido = { mensaje: string; trazaId?: string; sinConexion?: boolean; estado?: number }
// Ramas del host: cargando (isLoading) · error (ErrorTraducido) · vacío (idle | predicado+MotivoVacio) · listo (ng-content)
```

## 3. Brechas reales para H2 (no se inventan, se registran)

1. ~~El host no recibe plantillas con contexto tipado por rama~~ — **cerrada en la sesión de
   continuación (2026-09-22, con git real).** `estado-de-pantalla.ts` ahora expone
   `<ng-template #plantillaVacio let-motivo>` y `<ng-template #plantillaError let-error>`
   opcionales (leídas con `contentChild(..., { read: TemplateRef })`), con contexto tipado
   (`MotivoVacio` / `ErrorTraducido` completo). Si el consumidor no las proyecta, la rama sigue
   exactamente igual que antes (`mensajeVacio()` string / `error().mensaje` + `trazaId` +
   botón) — cero cambio de apariencia para los 11 consumidores reales. Test:
   `estado-de-pantalla.spec.ts`.
2. **Corrección real (no era la brecha que parecía):** `sinConexion` y `estado` SÍ están
   consumidos hoy, pero **no por el host** — por `apps/backoffice/src/app/nucleo/errores.interceptor.ts`,
   que arma `ErrorTraducido.mensaje` ya diferenciado por código HTTP (`mensajeDe(codigo, status)`)
   ANTES de que el host lo vea (confirmado leyendo `errores.interceptor.ts` + los tests reales
   `pantalla-de-billetera.spec.ts`, que prueban 401/403/503/sin-red con mensajes distintos, todos
   pasando por el mismo host sin que este distinga nada). Hacer que el host además ramifique sobre
   `estado`/`sinConexion` sería **duplicar** una decisión de traducción que H2.S1.M3 dice
   explícitamente que no le toca al host, y violaría "no se generaliza sin un segundo consumidor
   real que lo pida" (regla 00 §3.2) — no hay ningún consumidor real que necesite ese branching en
   el host mismo. **No se implementa; se cierra como no-brecha.**
3. No hay rama "obsoleto" ni carga útil de fecha de corte — **confirmado que sigue sin existir**
   tras releer el archivo en la sesión de continuación. `H2.S1.M2` la pide "cuando el contrato la
   trae"; como el contrato de hoy no la trae, esta parte de la microtarea es **N/A**, no pendiente.
4. `role="status"` / `role="alert"` ahora llevan **`aria-live` explícito** (`polite`/`assertive`)
   además del rol implícito — cerrado en la sesión de continuación. La sección "vacío" (que antes
   no tenía ningún rol) ahora también es `role="status"` con `aria-live="polite"`. **Sigue sin
   verificarse con un lector de pantalla real** (E2E de accesibilidad no corrido esta sesión
   tampoco — ver `PR8-carril.md` §No cubierto de la sesión de continuación).

## 4. No cubierto (al cerrar la sesión que escribió este contrato)

- No se ejecutó ningún test contra este contrato en esa sesión (ver bloqueo de `node_modules`/git
  en el `REPORTE.md` del carril). Esta tabla era `DISCOVERED`, no `TESTED`.
- No se revisó `apps/movil` (Flutter): el organismo de este contrato es Angular puro
  (`packages/ui`), fuera del alcance declarado.
- No se confirmó la existencia o ausencia de un guard de "pendiente de autenticación de ruta" fuera
  de `packages/ui` (no está en el alcance IN de este carril).

## 5. Sesión de continuación (2026-09-22) — H2.S1 implementado y `TESTED`; H2.S2.M1 cerrado como N/A verificado

**H2.S1.M1/M2 implementados:** `estado-de-pantalla.ts` ahora acepta `<ng-template #plantillaVacio
let-motivo>` y `<ng-template #plantillaError let-error>` opcionales (leídas con
`contentChild(..., { read: TemplateRef })`, contexto tipado: `MotivoVacio` / `ErrorTraducido`
completo). Si el consumidor no las proyecta, la rama sigue exactamente igual que antes — cero
cambio de apariencia para los 11 consumidores reales, confirmado por los tests de la §5.1 (rama por
defecto) y §5.2 (rama con plantilla, en un anfitrión de prueba separado). También se agregó
`aria-live="polite"`/`"assertive"` explícito a las tres ramas que lo necesitan (cargando/vacío con
`polite`, error con `assertive`) — antes solo tenían el rol implícito. Verificado en verde,
`TESTED` real (no razonado): `packages/ui/src/estado-de-pantalla/estado-de-pantalla.spec.ts`, 10
casos, corridos dentro de la corrida completa de `evidencia/h3-h2-ui-tests.md` §1 (16/17 archivos
en verde, el único rojo es `monto.spec.ts`, preexistente y no tocado).

**H2.S1.M3 (el host no traduce transporte ni decide autorización):** confirmado con un test que lee
el archivo fuente y falla si aparece `HttpClient`, `@angular/common/http`, `@angular/router` o algo
de sesión/autenticación — sigue sin aparecer. Además, releyendo
`apps/backoffice/src/app/nucleo/errores.interceptor.ts` se corrigió el §3.2 de arriba (ver tachado):
la traducción de `sinConexion`/`estado` YA pasa por el interceptor, no por el host, y agregarla acá
sería duplicar una decisión que el propio H2.S1.M3 dice que no es del host.

**H2.S2.M1 — verificado como N/A, no fabricado ni saltado.** Se pidió un agente de exploración
dedicado a buscar, en TODO `apps/backoffice/src/app/rutas/**` y `apps/web/src/app/**`, cualquier
vista que use `resource()`/`httpResource()`/`ResourceRef` y pinte a mano sus propias ramas de
cargando/error/vacío en vez de usar `ap-estado-de-pantalla`. Resultado: **no existe ninguna** —
`grep -rl "resource(\|httpResource(\|ResourceRef"` sobre esos dos árboles devuelve un ÚNICO archivo
(`verificador-de-sorteo.ts`), que ya está en la lista de 11 adoptantes. Lo más parecido que
apareció (`@defer/@placeholder` de hidratación diferida, y `tabla-de-datos-virtualizada.ts`, el
organismo compartido de tabla) NO califica: ninguno usa `ResourceRef` con las tres ramas manuales.
**Conclusión:** el precondición de H2.S2.M1 ("dos ramas repetidas reales") no existe en este repo
hoy — no hay nada que "reemplazar por el host" porque ya está todo adoptado. Se cierra como
`VERIFICADO N/A`, no como `TODO` ni como algo saltado.

**H2.S2.M2/M3, reinterpretados contra la realidad verificada arriba:** en vez de "las dos vistas
adoptantes" (que no existen como tal), se tomó el equivalente real más cercano: de los 11
consumidores reales, 6 no tenían NINGÚN test (`pantalla-de-expedientes.ts`,
`pantalla-de-desempeno.ts`, `pantalla-de-liquidacion.ts`, `simulador-de-costos.ts`,
`verificador-de-cadena.ts`, `verificador-de-certificado.ts`, `verificador-de-sorteo.ts` — 7, en
realidad). **No se llegó a escribirles tests en esta sesión** (tiempo): queda `PENDIENTE`, no
`N/A` — a diferencia de H2.S2.M1, esto SÍ se puede hacer, simplemente no se hizo todavía. De los que
sí tienen test (`pantalla-de-billetera.spec.ts`), la cobertura ya existente demuestra el patrón
completo: cargando/éxito/vacío-con-motivo/error(401/403/503/sin-red) + aria, sin tocar nada nuevo.
