# Primer error del alta visible sobre el teclado Android

Microtarea H7.S1.M11. Probada en AVD AtlasDemo aislado (Android 16/API 36), ventana 960×2280 px a 480 dpi = 320×760 dp, escala de fuente Android 200 %, teclado del sistema abierto y APK debug construido desde el código final con `API=http://10.0.2.2:4010/api/v1`. El valor `A` es sintético.

## Defecto, corrección y prueba

Con «Nombres» ya enfocado, el formulario desplazado hasta «Continuar» y la pantalla ocupada por el teclado, pulsar el botón insertaba los errores pero dejaba el primer error fuera de la vista. La captura [antes, claro](./teclado-error-android/antes-error-claro.png) muestra el formulario abajo tras la validación. La prueba de widget nueva reprodujo primero `Expected: >= 80; Actual: -2539.0` para la posición del primer campo.

`PasoDatos` ahora solicita foco al primer campo inválido y, tras reconstruir los mensajes, desplaza ese campo a la zona visible aunque ya tuviera foco. No borra lo escrito. `flutter test test/identidad/registro_error_foco_test.dart` terminó **1/1 PASS**; `flutter analyze` terminó **sin issues**; la suite no-golden `flutter test test/a11y test/identidad test/widget test/unidad test/pasanaku test/contrato` terminó **440/440 PASS**. `flutter build apk --debug --dart-define=API=http://10.0.2.2:4010/api/v1` compiló correctamente. Persiste un aviso no bloqueante de compatibilidad futura del Kotlin Gradle Plugin de Patrol.

## Evidencia visual final

Las tres capturas del código final se abrieron e inspeccionaron en resolución original:

| Captura | Observación |
| --- | --- |
| [«Continuar» con teclado, claro](./teclado-error-android/despues-cta-claro.png) | La acción sigue alcanzable por desplazamiento, sin desbordamiento visible. |
| [Primer error, claro](./teclado-error-android/despues-error-claro.png) | «Nombres», `A` y «Escribí al menos dos letras.» quedan completos sobre el teclado. |
| [Primer error, oscuro](./teclado-error-android/despues-error-oscuro.png) | El mismo valor y mensaje permanecen visibles y legibles al cambiar de tema. |

`dumpsys input_method` confirmó `mInputShown=true` y `mIsInputViewShown=true`. En los últimos 1500 renglones de `logcat`, el filtro `FATAL EXCEPTION|E/flutter|Unhandled Exception|RenderFlex overflow|DioException|Connection refused|No route to host` devolvió **0 coincidencias**. Esto no equivale a una prueba de backend TEST ni a una auditoría de toda la red.

Límites: solo emulador Android y paso 1 con datos sintéticos; no hubo iOS, dispositivo físico, envío real de alta, OTP, Figma ni aprobación del gate visual general. H7.S1.M2 y H8.S1.M4 conservan sus estados parciales.
