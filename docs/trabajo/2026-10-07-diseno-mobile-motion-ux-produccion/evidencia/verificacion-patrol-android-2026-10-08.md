# Patrol Android nativo — 2026-10-08

## Defecto reproducido

El primer `patrol test` compiló y devolvió exit 0, pero su resumen fue `Total: 0 / Successful: 0`: el proyecto tenía tests Dart, pero no un runner Android que los expusiera a JUnit. `flutter test integration_test/arranque_y_registro_test.dart` tampoco es sustituto: falló al inicializar dos bindings (`IntegrationTestWidgetsFlutterBinding` y `PatrolBinding`).

Se añadió `MainActivityTest.java`, `PatrolJUnitRunner` y Android Test Orchestrator. El primer intento posterior no pudo instalar el APK por falta de espacio en el AVD habitual; el XML decía `Requested internal only, but not enough space`. Se usó una imagen de datos temporal separada para AtlasDemo con 4,9 GiB libres. No se borró Atlas; se desinstaló solo el APK sintético AportaYa del AVD habitual, recuperable al reinstalarlo.

## Salida observada

Con Flutter 3.44.8, JDK 21, Patrol CLI 3.11.0, Android 16/API 36 y `API=http://10.0.2.2:4010/api/v1`:

```text
patrol test -t integration_test/arranque_y_registro_test.dart -d emulator-5554 ...
Test summary:
Total: 1
Successful: 1
Failed: 0
Skipped: 0
```

El script real `corepack yarn workspace @aportaya/movil test:e2e:smoke --device emulator-5554 --dart-define=API=http://10.0.2.2:4010/api/v1` repitió **Total: 1 / Successful: 1 / exit 0**. El XML JUnit nombró `MainActivityTest` y `runDartTest[arranque_y_registro_test portada, tour y formulario de registro]`.

```text
patrol test -t integration_test/tour_completo_test.dart -d emulator-5554 ...
Test summary:
Total: 1
Successful: 1
Failed: 0
Skipped: 0
```

El segundo caso, aislado, verificó los cuatro párrafos del tour, tres toques «Siguiente» y la entrada al formulario. En una corrida de ambos casos juntos, el primero pasó y el segundo llegó al último toque, pero el AVD se desconectó; el XML marcó `tests="2" failures="1"` y `Test run failed to complete`. Esa corrida combinada **no** se cuenta como PASS. Android Test Orchestrator permitió iniciar el segundo caso después de que el runner sin aislamiento devolviera 500, pero no se ha demostrado estabilidad de la suite completa en este AVD.

El wrapper `scripts/ejecutar_patrol.dart` ahora devuelve error si el proceso Patrol falla, si no hay resumen o si dice `Total: 0`. `flutter test --no-pub test/unidad/ejecutar_patrol_test.dart` dio **4 PASS** para esos casos. En el último corte, la app dio **439/439** tests no-golden y `flutter analyze --no-pub --fatal-infos` informó `No issues found!`. `python -X utf8 scripts/verificar_frontend.py movil` dio `TODO OK` antes del refinamiento del wrapper, que no toca vistas.

## Alcance y límite

Los dos recorridos usan la app instalada y UI nativa, pero solo la zona pública: no envían el alta, no verifican OTP, no llaman al backend TEST ni prueban persistencia tras app kill, aporte financiero, iOS o dispositivo físico. La URL `10.0.2.2:4010` fue configuración de arranque; no se afirmó respuesta de un gateway real. H7.S1.M2 continúa **A MEDIAS**. Los goldens históricos y GitHub Actions siguen como gates separados.

Referencias de herramienta: [instalación de Patrol](https://patrol.leancode.co/documentation) y [Android Test Orchestrator](https://developer.android.com/training/testing/instrumented-tests/androidx-test-libraries/runner#using-android-test-orchestrator).
