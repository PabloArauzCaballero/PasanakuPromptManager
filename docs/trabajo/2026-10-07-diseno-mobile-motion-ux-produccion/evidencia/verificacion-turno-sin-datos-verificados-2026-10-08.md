# Turno personal sin datos verificados — 2026-10-08

Código frontend: [`20300cc`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/20300cc834b83aa543c1ed3803af5a1874c4889f), PR #15.

## Hallazgo y contención

La ruta `/pasanaku/sorteos/:sorteoId/turno` convertía `total`, `mio` y `actual` de la URL con `int.parse` y dibujaba el riel como si fuera un dato del servidor. Un enlace con `total=abc` podía romper la pantalla; uno con `mio=999` podía atribuir a la persona una posición inventada. También se pasaba `coincide: true` al panel por el solo hecho de que existiera una semilla revelada; eso no prueba que el orden reproducido coincida con el guardado.

Ahora la ruta descarta cualquier query y el widget solo consulta el paquete publicado. La pantalla muestra un aviso persistente de que el turno personal no está verificado, conserva los datos públicos del sorteo y enlaza a la verificación pública. El panel no emite un veredicto de coincidencia que no haya calculado el servicio verificador. La acción se llama «Verificar el sorteo», porque navega dentro de la app y no «afuera».

**Límite:** esto no completa la vista de turno personal. El OpenAPI de `grupos` solo publica el paquete del sorteo; falta un GET autenticado con la posición de la persona, el turno actual y autorización de titularidad. El código no debe reconstruir esos datos desde parámetros de URL ni inferirlos del orden público sin la identidad autenticada. La pantalla es una contención segura hasta que ese contrato exista y se pruebe en backend TEST.

## Evidencia visual inspeccionada

Capturas de widget Flutter en Windows con fuentes cargadas y datos sintéticos. No son capturas en dispositivo Android/iOS; estos goldens solo corren en Windows y se omiten en Mac hasta crear referencias propias.

| Celda | Captura | Inspección |
|---|---|---|
| Móvil 360×760, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/20300cc834b83aa543c1ed3803af5a1874c4889f/apps/movil/test/goldens/imagenes/turno_sin_confirmar_360_claro.png) | Aviso visible antes del paquete, CTA legible, sin turno ficticio. |
| Móvil 360×760, oscuro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/20300cc834b83aa543c1ed3803af5a1874c4889f/apps/movil/test/goldens/imagenes/turno_sin_confirmar_360_oscuro.png) | Contraste y jerarquía coherentes; no hay chip de coincidencia inventado. |
| Móvil 360×760, texto 200 %, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/20300cc834b83aa543c1ed3803af5a1874c4889f/apps/movil/test/goldens/imagenes/turno_sin_confirmar_360_texto_200_claro.png) | El aviso y el paquete continúan en scroll, sin overflow. |
| Móvil 360×760, texto 200 %, oscuro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/20300cc834b83aa543c1ed3803af5a1874c4889f/apps/movil/test/goldens/imagenes/turno_sin_confirmar_360_texto_200_oscuro.png) | Texto completo, sin recorte; el CTA queda más abajo y se alcanza desplazando. |
| Tablet 768×1024, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/20300cc834b83aa543c1ed3803af5a1874c4889f/apps/movil/test/goldens/imagenes/turno_sin_confirmar_768_claro.png) | Aviso y acción se distribuyen sin anomalías de layout. |

## Pruebas y gates

- Dos pruebas de ruta con `?total=abc&mio=999&actual=-1` en claro/oscuro, una de ellas con texto al 200 %, comprueban: query eliminada, paquete cargado, ausencia de «999» y de veredicto falso, navegación al verificador y ninguna excepción.
- App: **338/338** pruebas no-golden y **5/5** goldens dirigidos; sistema de diseño: **54/54** pruebas dirigidas; analizadores de ambos paquetes sin hallazgos. `flutter build apk --debug --no-pub` PASS.
- [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37733245911): los jobs fallaron con `steps: []`; anotación literal: “The job was not started because recent account payments have failed or your spending limit needs to be increased”. Los jobs Flutter/macOS/iOS fueron omitidos. PR frontend sin merge.

El avance del plan permanece **11/41 HECHO**. H8.S1.M4 y H8.S1.M6 reciben evidencia parcial, pero no satisfacen capturas multiplataforma, pruebas con backend ni aprobación de seguridad.
