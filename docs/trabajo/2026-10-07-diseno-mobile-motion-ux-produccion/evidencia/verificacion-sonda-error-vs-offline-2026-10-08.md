# Gateway no verificable no es teléfono offline — 2026-10-08

Código: [`PasanakuFrontend b99d394`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/b99d394), PR #15. Continuación del [plazo total de la sonda](./verificacion-sonda-timeout-total-2026-10-08.md). H8.S1.M3 sigue **EN CURSO**.

## Cambio de estado

Antes, `ConnectivityResult.none`, un fallo del gateway y un timeout de la sonda se convertían todos en `false`. La UI mostraba «Sin conexión» incluso cuando el teléfono podía tener red y el servidor no respondía.

Ahora solo `ConnectivityResult.none` produce `false`. Un GET fallido, una configuración de gateway ausente o un timeout producen `SondaNoComprobada`, que el `StreamProvider` expone como error recuperable. La UI existente dice «No pudimos comprobar la conexión», pausa operaciones y ofrece «Volver a comprobar». La sonda periódica sigue viva tras el error y puede emitir `true` al recuperarse el gateway. Ninguna operación monetaria se habilita hasta ese `true`; el mensaje no presenta el fallo del servidor como certeza sobre la red del teléfono.

## Pruebas ejecutadas en Windows

- `flutter test --no-pub test/unidad/conectividad_android_test.dart`: **10/10 PASS**. Cubre ausencia de red del sistema, conexión fallida, gateway que acepta sin responder, plugin tardío sin GET posterior, timeout seguido de recuperación, error periódico seguido de recuperación y `StreamProvider` que pasa de error a conexión confirmada.
- `flutter test --no-pub test/unidad/conectividad_android_test.dart test/unidad/comandos_dinero_conexion_test.dart test/widget/operaciones_conexion_pendiente_test.dart --reporter json`: `success:true`. Los cuatro comandos monetarios tienen prueba de error de sonda sin POST ni clave local, además de la guardia de sonda pendiente y caída de red.
- `flutter test --no-pub test/unidad test/widget test/contrato test/identidad test/pasanaku test/a11y --reporter json`: `success:true`, suite no-golden completa. `flutter analyze --no-pub`: sin issues. `PYTHONUTF8=1 python scripts/verificar_frontend.py movil`: TODO OK. `flutter build apk --debug --no-pub`: APK generado.
- `flutter test --no-pub test/goldens/conexion_operaciones_golden_test.dart`: **7/7 PASS** en Windows. Las respuestas de red de este test son simuladas, no backend TEST.

## Inspección visual dirigida

Se abrieron las siete referencias PNG después de que la renderización actual coincidiera píxel a píxel con ellas. No se rebaselinaron. Los archivos están en `PasanakuFrontend/apps/movil/test/goldens/imagenes/`.

| Celda | Archivo | Resultado |
| --- | --- | --- |
| Recarga · error · 360×760 · 200 % · claro | `recarga_sonda_fallida_360_texto_200_light.png` | Alerta legible, acción «Volver a comprobar» visible, sin solapamiento en el área capturada. |
| Recarga · error · 360×760 · 200 % · oscuro | `recarga_sonda_fallida_360_texto_200_dark.png` | Texto y acción distinguibles sobre fondo oscuro, sin recorte del aviso. |
| Recarga · pendiente · 360×760 · 200 % · claro | `recarga_sonda_pendiente_360_texto_200_light.png` | Estado de comprobación legible; el formulario continúa debajo mediante scroll. |
| Recarga · pendiente · 360×760 · 200 % · oscuro | `recarga_sonda_pendiente_360_texto_200_dark.png` | Jerarquía del aviso conservada y contraste visual legible. |
| Aporte · pendiente · 360×760 · 200 % · claro | `aporte_sonda_pendiente_360_texto_200_light.png` | Aviso y monto visibles, sin choque entre ambos. |
| Aporte · pendiente · 360×760 · 200 % · oscuro | `aporte_sonda_pendiente_360_texto_200_dark.png` | Aviso y monto visibles; no hay fondo blanco intruso. |
| Saldo · pendiente · 768×1024 · claro | `saldo_sonda_pendiente_768_light.png` | Aviso sobre el saldo; acciones visibles pero inhabilitadas según prueba widget. |

`tester.takeException()` fue nulo en las pruebas golden. No hubo captura ni inspección de dispositivo real, lector de pantalla, consola/red reales o tema oscuro de tablet. Esto es una inspección visual **dirigida**, no el gate visual completo de H8.S1.M4.

## Límite de producción

El gateway TEST, Android/iOS reales, las transiciones entre wifi y datos, el resultado financiero tras timeout/app kill y la aprobación de Seguridad/QA siguen pendientes. La rama del frontend permanece sin merge porque los jobs obligatorios de GitHub Actions no arrancan; el conteo formal no cambia: **18/49 HECHO**.
