# Verificación Flutter 3.44.8 — `67777ae`

Se creó un worktree aislado del SDK en Windows con la etiqueta exacta **Flutter 3.44.8 / Dart 3.12.2** fijada en CI; no se cambió el SDK 3.47.5 preexistente. `flutter pub get` ajustó cuatro transitivas del `pubspec.lock` para esa versión y `flutter pub get --enforce-lockfile` pasó. El lockfile corregido está en el PR #15.

| Comando desde `apps/movil` | Resultado |
|---|---|
| `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact` | **194 PASS, 0 FAIL** |
| `flutter analyze --fatal-infos` | `No issues found!` |
| `python -X utf8 scripts/verificar_frontend.py movil` desde raíz | `TODO OK` |
| `flutter pub get --enforce-lockfile` | PASS |
| `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` | `Built build\\app\\outputs\\flutter-apk\\app-debug.apk` |
| `flutter test --no-pub test/goldens --reporter compact` | **4 PASS, 3 FAIL** en Windows: saldo claro/oscuro y transición de marca |

En 3.47.5, los goldens daban 2 PASS/5 FAIL; con 3.44.8, los dos formularios de aporte vuelven a pasar. Las imágenes de diff de saldo/transición se abrieron: master y resultado tienen el mismo layout aparente, con diferencias de contorno/rasterización. No se actualizaron snapshots ni se concluye equivalencia macOS; repetir ahí antes de integrar.

## Reintento de aporte

Una prueba recrea el `ProviderContainer` conservando el mismo almacén seguro: tras 503 simulado, el segundo proceso envía la misma clave y la limpia solo después de una respuesta válida. Otra prueba impide enviar si falla el guardado seguro; otra mantiene el éxito visible si falla la limpieza; otra bloquea un payload distinto con un error presentable. La huella SHA-256 no guarda la referencia en claro. Un widget test a 360×760 y texto 200 % alcanza mensaje y reintento sin overflow. Son pruebas simuladas, no E2E de cobro real ni recuperación tras kill del sistema operativo.

## Gate remoto y huecos

[Actions 37712900487](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37712900487) falló en 2–4 s y omitió Flutter/macOS/iOS. PR #15 sigue `UNSTABLE` y no se fusionó. El monto de aporte llega hoy por query en `rutas.dart`; no hay GET contractual de obligación para verificarlo antes del POST, ni ruta real de entrega/cobro de turno. Figma, backend TEST, research/aprobaciones y dispositivos iOS/físicos siguen pendientes.
