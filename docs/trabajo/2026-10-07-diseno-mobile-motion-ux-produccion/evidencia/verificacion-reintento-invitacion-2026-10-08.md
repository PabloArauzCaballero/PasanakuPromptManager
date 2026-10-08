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

La vista de error, la espera y el éxito del reintento fueron comprobados funcionalmente con respuesta interceptada; no se capturó una matriz visual de esos tres estados ni se ejecutó una llamada a backend TEST. La suite no-golden completa devolvió `success: true`; `flutter analyze --no-pub`, `python scripts/verificar_frontend.py movil` y `flutter build apk --debug --no-pub` pasaron en Windows. No hubo errores inesperados en los tests dirigidos. La comparación macOS, iOS, dispositivo físico y el gate remoto siguen abiertos: [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37791999547) no inició jobs por facturación/límite de gasto. H8.S1.M3 continúa **EN CURSO** y el total formal **18/49 HECHO**.
