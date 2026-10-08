# Reintento de consulta de invitación sin estados contradictorios

La consulta de una invitación ya no muestra a la vez datos recuperados y un error anterior. Un toque repetido en «Reintentar» mientras la consulta está en vuelo tampoco envía una segunda petición. El cambio de `PasanakuFrontend` está en `5fc734e`, publicado en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).

## Secuencia comprobada

Un test de widget con sesión y Dio simulados reprodujo dos fallas antes de la corrección: tras un timeout seguido de respuesta exitosa, «No pudimos verificar la invitación» seguía visible junto al nombre del grupo; dos toques rápidos producían **3 consultas** en lugar de **2** en toda la secuencia. Ahora el reintento borra el error anterior, muestra carga durante la espera y bloquea consultas concurrentes. Al llegar la respuesta, solo aparecen los datos nuevos y desaparecen carga, error y «Reintentar». El test final pasó **1/1** y `tester.takeException()` fue nulo.

El acceso sin sesión se extrajo a un widget propio para mantener `pantalla_unirse.dart` por debajo del límite de 200 líneas. El contenido de invitación quedó limitado a 560 dp en tablet, como otros formularios del proyecto; conserva scroll en teléfono.

## Evidencia visual sintética de Windows

Los seis goldens dirigidos pasaron sin actualizar baselines después de la recaptura e inspección. Rutas relativas a `PasanakuFrontend/apps/movil/test/goldens/imagenes/`:

| Celda | Imagen | Inspección |
|---|---|---|
| 320×760, claro, texto 200 %, enlace inválido | `enlace_invalido_320_light_texto_200.png` | Mensaje y salida legibles; sin recorte ni dato del enlace. |
| 320×760, oscuro, texto 200 %, enlace inválido | `enlace_invalido_320_dark_texto_200.png` | Contraste visual legible; sin recorte ni fondo claro accidental. |
| 768×1024, claro, enlace inválido | `enlace_invalido_768_light_texto_100.png` | Mensaje y salida centrados dentro del ancho máximo. |
| 320×760, claro, texto 200 %, sin sesión | `invitacion_ingreso_320_light_texto_200.png` | Ingreso y registro visibles; sin desbordamiento. |
| 320×760, oscuro, texto 200 %, sin sesión | `invitacion_ingreso_320_dark_texto_200.png` | Acciones y texto visibles sobre tema oscuro; sin desbordamiento. |
| 768×1024, claro, sin sesión | `invitacion_ingreso_768_light_texto_100.png` | Acción principal centrada, no estirada a todo el ancho. |

## Ampliación verificada en `b3ab6ea`

La respuesta de consulta se valida antes de mostrarla: `montoAporte` debe ser una cadena monetaria positiva conforme al contrato OpenAPI, con moneda, periodicidad y hash reconocidos. El aporte se presenta como «Aporte por período: Bs 25,00» y la frecuencia como «Mensual», sin exponer enum crudo ni dejar un separador huérfano a texto 200 %. Datos malformados producen un error seguro. Una invitación vencida/inválida (`AP-CU69-05`) o sin permiso (403) ofrece **Ir a portada**; timeout/500 conserva **Reintentar**, y 401 devuelve el acceso. No se muestra el mensaje crudo del servicio.

Se incorporaron **13 imágenes** de estados en `apps/movil/test/goldens/imagenes/`: `invitacion_error_*` (2), `invitacion_carga_*` (2), `invitacion_exito_*` (3), `invitacion_exito_abajo_*` (2) y `invitacion_rechazada_{422,403}_*` (4), en 320×760 claro/oscuro con texto 200 % y éxito adicional en tablet 768×1024. Se inspeccionaron la carga, los errores, el éxito y el botón final tras scroll; la acción completa permanece accesible. También se recapturaron las tres imágenes de enlace inválido. El texto de error utiliza `errTexto`: contraste calculado de aproximadamente **4,85:1** en claro y **7,24:1** en oscuro, frente a ~3,9:1 del rol anterior. Un test verifica el token real, AA y el objetivo táctil de 48 dp.

En el código final pasaron **13/13** casos golden dirigidos sin actualizar baselines, la suite no-golden completa (`success: true`), `flutter analyze --no-pub`, el verificador móvil (`PYTHONUTF8=1`) y el APK debug en Windows. La matriz usa respuestas simuladas: **no** demuestra backend TEST ni un enlace firmado real. Faltan comparación macOS/iOS, dispositivo físico y CI remoto. El [PR frontend #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) permanece sin merge hasta que corran los gates obligatorios. H8.S1.M3 **EN CURSO**, H8.S1.M4 **A MEDIAS**, total formal **18/49 HECHO**.

Antes de esta ampliación, la suite no-golden y seis goldens dirigidos ya pasaban en Windows; el [CI de `5fc734e`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37791999547) no inició jobs por facturación/límite de gasto.

## Aceptación sin falso éxito (`6c51c74`)

Una prueba rojo→verde reprodujo la respuesta HTTP 201 incompleta: el cliente eliminaba el detalle y cerraba la clave de idempotencia aun sin `grupoId`, dejando la vista sin confirmación útil. Ahora exige `grupoId` y `participanteId` UUID del contrato antes de anunciar membresía o cerrar la clave. Si la confirmación no es verificable, conserva detalle, consentimiento y clave para un reintento sin duplicar la operación; el texto admite incertidumbre y no afirma fallo definitivo. El éxito ya no promete «Ver mis grupos», porque esa ruta todavía abre sin titular autenticado; ofrece **Ir a portada**.

El test widget cubre respuesta incompleta→reintento confirmado con la **misma clave**, sin falso éxito; una prueba unitaria comprueba ambos identificadores. Cuatro goldens nuevos —`invitacion_aceptacion_{incierta,confirmada}_320_{light,dark}_texto_200.png`— fueron inspeccionados: error y CTA se leen tras scroll en 320×760/texto 200 %, y el éxito tiene salida visible en ambos temas. En el código `6c51c74` pasaron suite no-golden completa, **15/15** casos golden dirigidos sin actualizar baselines, analyzer, verificador y APK debug en Windows. Sin respuesta real de backend TEST, no se da por cerrada la resiliencia H8.S1.M3; CI/macos/iOS/dispositivo físico siguen pendientes y el total permanece **18/49 HECHO**.
