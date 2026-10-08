# Cada paso del alta abre desde arriba

H7.S1.M13. Frontend `92ce679` en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). AVD AtlasDemo con datos aislados, Android 16/API 36, 960×2280 px a 480 dpi = 320×760 dp, fuente del sistema al 200 %. APK debug final con `API=http://10.0.2.2:4010/api/v1`. Se usaron únicamente datos sintéticos; no se envió el alta ni se consultó backend TEST.

## Reproducción y cambio

El test nuevo desplazó el paso de datos hasta «Continuar» y luego avanzó. Antes del cambio, el paso de contraseña heredó **1287 dp** de desplazamiento (`Expected: 0; Actual: 1287.0`), dejando fuera de vista su inicio. Se asignó a `SingleChildScrollView` una clave dependiente del paso, de modo que cada transición inicia con posición de scroll nueva mientras el notifier conserva los campos. El mismo test desplaza el paso de contraseña, retrocede y comprueba posición cero y nombre «Demo» restaurado en el campo.

Verificación del código final: pruebas dirigidas de transición y reanudación **2/2 PASS**; `flutter test test/a11y test/identidad test/widget test/unidad test/pasanaku test/contrato` **443/443 PASS**; `flutter analyze` **No issues found**; `PYTHONUTF8=1 python scripts/verificar_frontend.py movil` **TODO OK**; formato de archivos cambiados sin diferencias; `flutter build apk --debug --dart-define=API=http://10.0.2.2:4010/api/v1` **Built app-debug.apk**. El aviso de compatibilidad futura del Kotlin Gradle Plugin de Patrol no impidió el build.

## Android real del APK final

Se instaló el APK final en el AVD temporal. Con el primer paso desplazado hasta su CTA, al avanzar se vio arriba «Paso 2 de 9 · Tu contraseña», su explicación y el primer campo tanto en claro como en oscuro. El aviso de borrador recuperado hace más exigente el espacio disponible; el primer campo aun así quedó visible. Al retroceder en el recorrido claro, el primer paso volvió arriba con el nombre sintético conservado. Las tres capturas se abrieron e inspeccionaron visualmente:

| Estado | Captura | Inspección |
| --- | --- | --- |
| Paso 1 desplazado a CTA | [paso1-abajo.png](./registro-scroll-android/paso1-abajo.png) | Punto de partida; CTA alcanzable por desplazamiento. |
| Paso 2 abierto arriba, claro | [paso2-arriba-claro.png](./registro-scroll-android/paso2-arriba-claro.png) | Encabezado, instrucción y primer campo visibles sin recorte. |
| Paso 2 abierto arriba, oscuro | [paso2-arriba-oscuro.png](./registro-scroll-android/paso2-arriba-oscuro.png) | Mismo contenido legible; sin solapamiento evidente. |

Filtro de los últimos 1500 renglones de `logcat` para `FATAL EXCEPTION|E/flutter|Unhandled Exception|RenderFlex overflow|DioException|Connection refused|No route to host`: **0 coincidencias**. Esto no equivale a certificar consola/red de todo el producto. Sin iOS, dispositivo físico, backend TEST, OTP, goldens macOS ni recorrido completo de los nueve pasos; esos gates siguen abiertos.
