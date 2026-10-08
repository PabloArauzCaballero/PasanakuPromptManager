# Errores de contraseña visibles sobre teclado Android

H7.S1.M12. AVD AtlasDemo aislado, Android 16/API 36, pantalla 960×2280 px a 480 dpi = 320×760 dp, fuente del sistema al 200 %, APK debug del commit `4dfddcf` con `API=http://10.0.2.2:4010/api/v1`. Se recorrió el primer paso con datos sintéticos para llegar al paso 2; no se envió el alta ni se usó backend TEST. Las contraseñas sintéticas permanecen enmascaradas en todas las capturas publicadas.

## Reproducción y corrección

Antes del cambio, con el teclado abierto y «Continuar» al alcance por desplazamiento, las dos pruebas nuevas fallaron porque el campo inválido quedó por encima del viewport: clave corta `Actual: -885.0` y confirmación distinta `Actual: -640.0`, frente a la posición mínima esperada de 80 dp. `PasoContrasena` ahora conserva un nodo de foco por campo, lo libera en `dispose` y, tras mostrar los errores, lleva el primero a la zona visible. La alineación de 0,3 deja legibles la etiqueta, el campo enmascarado y el mensaje; el helper anterior conserva 0,15 para el primer paso.

Comprobación final: `flutter test test/identidad/paso_contrasena_error_foco_test.dart test/identidad/paso_contrasena_test.dart test/identidad/registro_error_foco_test.dart` → **7/7 PASS**; `flutter test test/a11y test/identidad test/widget test/unidad test/pasanaku test/contrato` → **442/442 PASS**; `flutter analyze` → **No issues found**; `PYTHONUTF8=1 python scripts/verificar_frontend.py movil` → **TODO OK**; `flutter build apk --debug --dart-define=API=http://10.0.2.2:4010/api/v1` → **Built app-debug.apk**. El build emitió un aviso de compatibilidad futura del Kotlin Gradle Plugin de Patrol, no un fallo actual.

## Capturas finales inspeccionadas

| Celda | Evidencia | Inspección |
| --- | --- | --- |
| CTA con teclado · claro | [cta-claro.png](./contrasena-error-android/cta-claro.png) | «Continuar» alcanzable por scroll encima del teclado, sin solapamiento. |
| Clave corta · claro | [clave-corta-claro.png](./contrasena-error-android/clave-corta-claro.png) | Etiqueta, campo y mensaje completos; contraseña enmascarada. |
| Clave corta · oscuro | [clave-corta-oscuro.png](./contrasena-error-android/clave-corta-oscuro.png) | Mismo error legible sobre teclado oscuro; sin recorte del mensaje. |
| Confirmación distinta · claro | [confirmacion-distinta-claro.png](./contrasena-error-android/confirmacion-distinta-claro.png) | «Repetila» y mensaje completos; foco y máscara visibles. |
| Confirmación distinta · oscuro | [confirmacion-distinta-oscuro.png](./contrasena-error-android/confirmacion-distinta-oscuro.png) | Mismo campo/error completos sobre teclado oscuro. |

En el último recorrido `dumpsys input_method` devolvió `mInputShown=true` y `mIsInputViewShown=true`; el filtro de los últimos 1500 renglones de `logcat` para `FATAL EXCEPTION|E/flutter|Unhandled Exception|RenderFlex overflow|DioException|Connection refused|No route to host` devolvió **0 coincidencias**. No se capturó ni verificó tráfico de backend TEST.

No cubierto: iOS/VoiceOver, dispositivo físico, backend TEST, OTP, matrices completas de tablet y goldens macOS. H7.S1.M2 y H8.S1.M4 siguen parciales.
