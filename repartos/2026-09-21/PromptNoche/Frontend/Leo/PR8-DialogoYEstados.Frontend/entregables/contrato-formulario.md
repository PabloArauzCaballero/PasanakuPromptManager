# Contrato de formulario y borrador (H4.S1.M1)

> **Peldaño:** `DISCOVERED`. Fuente: los dos modales reales elegidos como candidatos H3.S2.M1 —
> `apps/backoffice/src/app/rutas/contabilidad/cobros/ficha-de-cobro.ts` y
> `apps/backoffice/src/app/rutas/contabilidad/compras/ficha-de-factura.ts` — leídos completos.

## 1. Dueño del borrador — declarado

**El contenedor (`FichaDeCobro` / `FichaDeFactura`) es el único dueño del borrador.** No hay dos
borradores autoritativos hoy: los `signal()` locales (`monto`, `forma`) viven exclusivamente en el
componente que envuelve `<ap-dialogo>`, y el `Dialogo` en sí **no tiene ningún estado de
formulario** — solo `abierto` (apertura) y `cargando` (para el spinner del botón de confirmar). El
diálogo es "tonto" respecto del formulario: proyecta el contenido, no lo conoce. Esto ya cumple la
regla del encargo ("nunca las dos cosas a la vez") **tal como está escrito hoy**, sin necesitar un
cambio de arquitectura — el trabajo de H4 no es *resolver* una duplicación de borrador (no la hay),
es *demostrar* y *blindar* que se mantiene así al migrar al diálogo con política de descarte.

## 2. Qué ya está resuelto en el código real (evidencia, no propuesta)

| Requisito | Estado real | Evidencia |
|---|---|---|
| Valores iniciales | `monto = signal('')`, `forma = signal('TRANSFERENCIA')` | `ficha-de-cobro.ts:39-40` |
| Validación | `errorDeMonto` computed, bloquea el excedente contra el saldo (regla de dominio `cobroExcedeElSaldo`, `AP-CU104-02` del backend queda de respaldo — comentario línea 12) | `ficha-de-cobro.ts:47-49` |
| Bloqueo de doble envío | `enviando` signal, gate en `confirmar()`: no hay guardia explícita contra reentrancia mientras `enviando()` es true en el propio método (**brecha real, ver §4**) | `ficha-de-cobro.ts:51,60-68` |
| Error remoto conserva el borrador | `error: () => this.enviando.set(false)` — no limpia `monto` ni `forma`, y no cierra el diálogo | `ficha-de-cobro.ts:67` |
| Cancelar | `cambiarApertura(false)` → emite `cerrada` | `ficha-de-cobro.ts:56-59` |

## 3. Campo tocado / modificado — no está resuelto

`CampoMonto` y `GrupoRadio` (moléculas de `packages/ui`) no fueron leídos en detalle en esta sesión
(fuera del foco de lectura priorizado); no se afirma si exponen estado "tocado" (`touched`) o
"modificado" (`dirty`) por campo. **Esto es exactamente lo que la política de descarte del diálogo
necesita como predicado** (`hay cambios sin guardar`): hoy el candidato más simple y honesto, sin
inventar un campo `dirty` que no existe, es comparar `monto() !== '' || forma() !== valorInicial`
contra los valores iniciales capturados al abrir. Se registra como decisión técnica mínima
(regla 00 §1.5), no como hallazgo de un campo ya existente.

## 4. Brecha real: doble envío

`confirmar()` (línea 71-85 de `ficha-de-cobro.ts`) no verifica `if (this.enviando()) return` antes
de disparar la petición: si alguien pulsa el botón dos veces rápido antes de que Angular repinte el
`[cargando]="enviando()"` del botón (que sí debería deshabilitarlo — no se leyó `Boton` para
confirmar si `cargando` deshabilita el `click` nativo), hay una ventana de doble envío no cerrada
por este archivo. **No verificado en runtime** (regla 95.3.4 exige bloqueo — no confirmado que
`ap-boton` lo dé gratis; queda como hallazgo para el equipo, fuera de reescribir `Boton`, que no
está en el alcance IN de este carril).

## 5. Política para entidad que cambia durante la edición (Q-L1)

**No definida por producto.** Se aplica la rama conservadora exigida por el encargo: si la entidad
(`cuenta: CuentaPorCobrar` / `factura: FacturaDeProveedor`, ambas `input.required`) cambia mientras
el diálogo está abierto con un borrador sucio, **no se pierde el borrador en silencio** y **no se
guarda contra la entidad vieja** — la implementación concreta de esa rama (por ejemplo, recongelar
el `input` al abrir con un snapshot local, y comparar el `input` corriente contra ese snapshot para
decidir si avisar) no se escribió en esta sesión (ver bloqueo de entorno). Se registra como
`A MEDIAS`: el supuesto está tomado y escrito, el código que lo aplica no.

## 6. No cubierto (al cerrar la sesión que escribió este contrato)

- No se leyeron `CampoMonto`, `GrupoRadio`, `Boton` en profundidad (fuera del foco priorizado de
  esta sesión) — el comportamiento de "tocado"/"modificado" y de deshabilitado por `cargando` en
  `ap-boton` queda sin confirmar.
- Ningún test de `formulario`/`error de guardado` corrido (bloqueo de entorno).
- No se verificó si algún modal existente evita a propósito la protección de descarte por una razón
  de producto (Q-L3): con la lectura de código disponible, ninguno de los dos candidatos tiene hoy
  ninguna protección — no hay dato para sospechar que sea intencional, así que ante la duda se
  protegerá cuando se implemente (regla del encargo, Q-L3).

## 7. Sesión de continuación (2026-09-22) — H4.S2.M1 implementado, H4.S1.M2/M3 escritos, no ejecutados

Con `git` real, se cablearon los dos modales elegidos (`ficha-de-cobro.ts`, `ficha-de-factura.ts`)
contra el `Dialogo` ya reforzado (ver `contrato-dialogo.md` §6):

1. **`hayCambiosSinGuardar`** — computed mínimo, exactamente el candidato descrito en §3:
   `monto() !== '' || forma() !== 'TRANSFERENCIA'`, pasado como `[hayCambiosSinGuardar]` al
   `<ap-dialogo>`. Cierra la brecha central: ahora las tres rutas de cierre SÍ preguntan si hay un
   borrador sucio, en los dos modales reales, no solo en el organismo aislado.
2. **Doble envío (§4, brecha real)** — `confirmar()` ahora empieza con
   `if (this.enviando() || ...) return`, defensa explícita además de lo que ya daba gratis
   `[disabled]="cargando()"` de `ap-boton` (confirmado leyendo `boton.ts`: si ya deshabilita el
   click nativo, pero un `return` explícito no depende de que el repintado de Angular gane la
   carrera contra un segundo clic).
3. **Q-L1, rama conservadora (§5)** — implementada, no solo declarada: un snapshot de la entidad
   (`cuenta`/`factura`) se toma la primera vez que llega el `input()`; si cambia mientras
   `hayCambiosSinGuardar()` es `true`, se enciende `entidadCambioConBorradorSucio` — el borrador NO
   se toca (sigue en pantalla) y `confirmar()` se bloquea contra la entidad vieja, con un aviso
   `role="alert"` visible en el propio diálogo.
4. **H4.S1.M2 (la suite de casos)** — escrita en `ficha-de-cobro.spec.ts` /
   `ficha-de-factura.spec.ts`: valores iniciales, campo tocado/modificado, validación, envío, doble
   envío bloqueado, error remoto (conserva borrador, no cierra), cancelar (con y sin cambios),
   reapertura con borrador limpio, y el caso de Q-L1 de arriba.

**Peldaño real, sin inflar (regla 30):** `WRITTEN` + **typecheck limpio confirmado**, no `RUNS`.
`apps/backoffice` no compila como bundle completo en este entorno — no por estos dos archivos
(se confirmó leyendo la lista completa de errores de un build real: cero errores en
`ficha-de-cobro.ts`, `ficha-de-factura.ts` o sus specs, después de corregir dos accesos a miembros
`protected` desde el test), sino por el hallazgo H-2 ya registrado (`clientes/angular/*` generados
no existen en este checkout) más uno nuevo, más chico: `@aportaya/tokens/generado/tokens.css`
tampoco existe hasta correr `yarn workspace @aportaya/tokens build` (no commiteado: la carpeta
`generado/` está en `.gitignore`, es un artefacto de build, no código fuente). `ng lint` sobre los
cuatro archivos: limpio, cero hallazgos. Ver `evidencia/h4-fichas-typecheck.md`.

**Lo que sigue sin ejecutarse, honesto:** el `test:front` real de `apps/backoffice` para estos dos
specs (bloqueado por lo de arriba, no por el contenido de los tests) y el E2E de foco/teclado/
descarte + comparación visual sobre los dos modales reales (mismo bloqueo de login que
`contrato-dialogo.md` §6 — las rutas de `contabilidad` redirigen a `/tablero` sin sesión).
