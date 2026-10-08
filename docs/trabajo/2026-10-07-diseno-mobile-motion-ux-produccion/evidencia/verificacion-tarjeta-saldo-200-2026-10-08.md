# Tarjeta de saldo con texto al 200 % — 2026-10-08

Codigo frontend: `c52a22c` quita el ID de cuenta de las URLs internas de recarga, retiro y extracto; `a630b86` adapta la tarjeta reutilizable de saldo. Ambos commits estan en el PR #15. Son mejoras del cliente, no una autorizacion de cuenta ni una prueba de pagos contra backend.

## Reproduccion y arreglo

La prueba nueva de `TarjetaSaldo` a 360 dp y texto al 200 % fallo antes del arreglo con `A RenderFlex overflowed by 6.0 pixels on the right` en claro y oscuro. El importe y sus dos acciones competian por el ancho. Ahora el desglose y las acciones se apilan cuando lo exige el ancho disponible y la escala del texto; en ancho suficiente conservan la disposicion horizontal. Un importe extremo se corta solamente entre grupos de miles; la semantica anuncia la cifra completa.

## Capturas finales abiertas e inspeccionadas

Son capturas de widget Flutter en Windows con fuentes cargadas, datos sinteticos y texto al 200 %. No son capturas Android/iOS ni prueban el flujo de saldo autenticado. Las referencias de pixeles nuevas solo se comparan en Windows; en Mac el test se omite hasta generar una linea base propia tras inspeccion.

| Celda | Evidencia | Inspeccion |
|---|---|---|
| 320 dp, claro, importe normal | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_320_claro.png) | OK: cifra completa, acciones apiladas, sin recorte. |
| 360 dp, oscuro, importe normal | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_360_oscuro.png) | OK: cifra completa, contraste y objetivos legibles. |
| 620 dp, claro, antes del cambio de disposicion | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_620_claro.png) | OK: acciones apiladas, sin salto de contenido. |
| 640 dp, claro, despues del cambio | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_640_claro.png) | OK: acciones en fila, etiquetas enteras. |
| 768 dp, oscuro, tablet | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_768_oscuro.png) | OK: cifra y acciones alineadas, sin superficie blanca inesperada. |
| 320 dp, claro, importe extremo | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a630b86/packages/diseno_flutter/test/goldens/imagenes/tarjeta_saldo_texto_grande_320_importe_largo.png) | OK: ningun grupo de digitos se parte; importe completo visible y anunciado. |

La prueba de widget verifica en 320/360 dp, claro/oscuro y 200 %: sin excepciones de layout, targets Android, etiquetas de controles y contraste de texto. El importe extremo conserva la etiqueta semantica exacta `Saldo disponible: Bs 999.999.999.999,99`. Las tres pruebas de navegacion verifican que las URIs de recarga, retiro y extracto no contienen el UUID de cuenta.

Verificacion local final: diseno Flutter `flutter analyze --no-pub` limpio y **54/54** pruebas dirigidas de a11y/unidad/widget y los seis goldens nuevos; app movil `flutter analyze --no-pub` limpio y **336/336** pruebas no-golden. `flutter build apk --debug --no-pub` compilo despues del ultimo ajuste (`Built build\app\outputs\flutter-apk\app-debug.apk`). No hubo peticiones de red en las capturas de componente. No se cubrieron dispositivo real, lector de pantalla ni Mac, y el CI del commit `a630b86` rechazo los jobs antes de ejecutarlos por facturacion. No se emite veredicto de pantalla completa ni se cierra H5.S1.M3/H8.S1.M4.
