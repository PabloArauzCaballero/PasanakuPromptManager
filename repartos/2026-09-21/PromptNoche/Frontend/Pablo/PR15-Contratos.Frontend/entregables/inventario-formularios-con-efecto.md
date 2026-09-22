# Inventario de formularios con efecto — H3.S2.M3

Barrido real sobre `apps/backoffice/src/app`, 2026-09-22: todo componente con un método de
envío (`confirmar`, `guardar`, `habilitar`, `resolver`, `confirmarLiquidar`) que llama a una
operación con `Idempotency-Key` (vía `contextoConClave()`/`CLAVE_IDEMPOTENCIA`) o que dispara un
efecto de negocio. Se buscó `protected confirmar()`, `async \w+(): Promise<void>` y los usos de
`CLAVE_IDEMPOTENCIA`/`contextoConClave` y se revisó cada consumidor real, uno por uno.

| Formulario | Archivo | ¿Deshabilitaba el botón mientras la operación estaba en curso? | ¿Tenía guarda de reentrada sincrónica? | Acción |
|---|---|---|---|---|
| Cobrar cuenta por cobrar (CU-104) | `contabilidad/cobros/ficha-de-cobro.ts` | Sí (`[cargando]="enviando()"`) | **No** — bug real | Corregido: `if (this.enviando()) return`. Test nuevo: `ficha-de-cobro.spec.ts` |
| Pagar factura de proveedor (CU-103) | `contabilidad/compras/ficha-de-factura.ts` | Sí | **No** — bug real | Corregido: `if (this.enviando()) return`. Test nuevo: `ficha-de-factura.spec.ts` |
| Habilitar organizador (CU-90, con límite de monto) | `cumplimiento/organizadores/pantalla-de-habilitacion.ts` | Sí (`[cargando]="habilitando()"`) | **No** — bug real | Corregido: `if (this.habilitando()) return`. **Sin test nuevo** — no cubierto |
| Alta de anunciante/socio (con límite de gasto mensual) | `publicidad/anunciantes/pantalla-de-anunciantes.ts` | Sí, vía `guardando()` | **No** — bug real, agravado por ser `async`/`await` (ventana síncrona más ancha) | Corregido: `if (this.guardando()) return`. **Sin test nuevo** — no cubierto |
| Liquidar cuenta de publicidad (plata real) | `publicidad/liquidacion/pantalla-de-liquidacion.ts` | Sí, vía `liquidando()` | **No** — bug real, `async`/`await` | Corregido: `if (this.liquidando()) return`. **Sin test nuevo** — no cubierto |
| Resolver expediente de verificación (aprobar/rechazar KYC) | `cumplimiento/verificaciones/pantalla-de-expedientes.ts` | Sí, vía `resolviendo()` | **No** — bug real (no es plata, pero sí una decisión de cumplimiento que no debe duplicarse) | Corregido: `if (this.resolviendo()) return`. **Sin test nuevo** — no cubierto |
| Moderar campaña de publicidad | `publicidad/moderacion/cola-de-moderacion.ts` | Sí | **Sí**, ya tenía la guarda | Sin cambios |
| Aprobar campaña | `publicidad/campanas/panel-de-aprobacion.ts` | Sí | **Sí**, ya tenía la guarda | Sin cambios |
| Ingresar (login) | `ingreso/pantalla-de-ingreso.ts` | Sí | **Sí**, ya tenía la guarda | Sin cambios |
| Borrador de caso de cumplimiento | `cumplimiento/casos/pantalla-de-caso.ts` | N/A — no llama a un endpoint con efecto, solo guarda un borrador local | N/A | Sin cambios, no aplica |

## Resumen

**6 de 10 formularios con efecto real tenían el mismo bug** (sin guarda de reentrada síncrona,
pese a tener la señal `enviando`/equivalente y el botón deshabilitado en el DOM). Corregidos los
6. **Solo 2 de los 6 quedaron con test nuevo** que demuestre el arreglo (`ficha-de-cobro`,
`ficha-de-factura` — los dos casos de dinero explícito que motivaron el hallazgo). Los otros 4
(`habilitación`, `alta de anunciante`, `liquidación`, `resolución de expediente`) están
corregidos pero **sin prueba propia que falle si alguien revierte el fix** — queda en "No
cubierto" del reporte.

## Por qué pasaba desapercibido

El patrón `[cargando]="enviando()"` en el DOM SÍ deshabilita el botón — pero solo después de que
Angular re-renderiza. Dos clics (o dos invocaciones sincrónicas, como en un test o un doble evento
de teclado) que ocurren antes de ese repintado ejecutan el método de envío dos veces. En los
formularios `async`/`await` (anunciantes, liquidación) la ventaja es todavía más ancha: cualquier
código síncrono antes del primer `await` corre completo en la segunda llamada también. El
interceptor de idempotencia no protege acá porque la clave se firma **dentro** de cada llamada a
la función de dominio (`contextoConClave()` corre de nuevo en cada invocación), no una vez por
apertura de formulario.
