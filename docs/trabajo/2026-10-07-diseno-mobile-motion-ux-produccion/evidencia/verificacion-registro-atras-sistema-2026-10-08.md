# Atrás del sistema Android dentro del alta

H7.S1.M14. Frontend `3bd3611` en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). AVD AtlasDemo aislado, Android 16/API 36, 960×2280 px a 480 dpi = 320×760 dp, fuente del sistema al 200 %, APK debug final con `API=http://10.0.2.2:4010/api/v1`. Datos de formulario exclusivamente sintéticos, sin envío de alta ni backend TEST.

## Rojo → verde

En una ruta de ensayo con pantalla anterior, el test abrió el registro, avanzó y llamó `handlePopRoute()` para simular Atrás del sistema. Antes del cambio falló: `Expected: exactly one matching candidate; Actual: Found 0 widgets with type "PantallaDeRegistro"` — se había cerrado toda la ruta desde el paso 2. Ahora `PopScope` impide el pop de la ruta a partir del paso 2 y delega el intento al paso anterior del notifier; en el primero deja salir normalmente. El test final cubre 3→2→1→pantalla anterior y comprueba que «Demo» permanece en el estado. El test de scroll comprueba además que el paso al que se regresa abre arriba.

Código final: pruebas dirigidas de Atrás y scroll **3/3 PASS**; app no-golden **445/445 PASS**; `flutter analyze` **No issues found**; `PYTHONUTF8=1 python scripts/verificar_frontend.py movil` **TODO OK**; formato de los tres archivos cambiados sin diferencias; `flutter build apk --debug --dart-define=API=http://10.0.2.2:4010/api/v1` **Built app-debug.apk**. Gradle advirtió compatibilidad futura del Kotlin Gradle Plugin de Patrol; no fue un fallo de este build.

## Interacción Android inspeccionada

Con el APK final, se completó el primer paso con datos sintéticos en la imagen temporal del AVD. Se vio el paso 2 en claro; `adb shell input keyevent 4` volvió al paso 1 con los valores conservados y otro Atrás abrió el tour. Se repitió paso 2→1 en oscuro con tecla del sistema y también con gesto lateral desde el borde izquierdo. Se abrieron e inspeccionaron las capturas de antes y después: encabezado y primer campo visibles, sin recorte ni superposición evidente en ambas variantes. Solo se publican capturas **sin datos de formulario**:

| Estado | Captura conservada | Inspección |
| --- | --- | --- |
| Paso 2 antes de Atrás, claro | [paso2-antes-claro.png](./registro-atras-android/paso2-antes-claro.png) | Encabezado, explicación y primer campo visibles. |
| Paso 2 antes de Atrás, oscuro | [paso2-antes-oscuro.png](./registro-atras-android/paso2-antes-oscuro.png) | Contenido legible, sin fondo claro accidental. |
| Después del segundo Atrás desde paso 1 | [tour-despues-de-atras.png](./registro-atras-android/tour-despues-de-atras.png) | El tour anterior reaparece completo. |

Las capturas de paso 1 con valores sintéticos se inspeccionaron localmente, pero no se publican para evitar exponer contenidos de formulario. El filtro de los últimos 1500 renglones de `logcat` para `FATAL EXCEPTION|E/flutter|Unhandled Exception|RenderFlex overflow|DioException|Connection refused|No route to host` devolvió **0 coincidencias**. No se inspeccionó todo el tráfico de red. `PopScope.canPop=false` desactiva el gesto de borde propio de rutas Cupertino en iOS según el SDK instalado; sigue disponible la flecha visible, pero gesto/VoiceOver/iOS no están verificados y deben revisarse en Mac. Sin dispositivo físico, OTP real, backend TEST ni goldens macOS.
