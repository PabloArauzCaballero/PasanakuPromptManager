# Reanudación del borrador con Keystore Android — 2026-10-08

## Alcance

El test Patrol `integration_test/reanudacion_borrador_test.dart` usa la app real,
un `ProviderScope` con el adaptador Android real y un prefijo exclusivo de claves
de ensayo. Abre la portada y el alta, escribe un dato sintético, espera la
persistencia, desmonta el árbol Flutter, abre de nuevo portada y alta y comprueba
el aviso de reanudación y el valor recuperado en el campo. Borra solo la clave
prefijada al terminar; nunca lee ni sobrescribe un borrador de usuario.

## Salidas observadas

En AVD AtlasDemo Android 16/API 36 con imagen de datos temporal separada,
Flutter 3.44.8, JDK 21 y Patrol CLI 3.11.0:

```text
dart scripts/ejecutar_patrol.dart --target integration_test/reanudacion_borrador_test.dart --device emulator-5554 --dart-define=API=http://10.0.2.2:4010/api/v1
🧪 el borrador sobrevive a recrear la app con Keystore Android
✅ el borrador sobrevive a recrear la app con Keystore Android
Test summary:
Total: 1
Successful: 1
Failed: 0
Skipped: 0
exit code: 0
```

Además:

```text
flutter analyze --no-pub --fatal-infos
No issues found! (ran in 7.1s)

flutter test --no-pub test/identidad/registro_reanudacion_test.dart test/identidad/borrador_de_alta_test.dart --reporter compact
+6: All tests passed!

python -X utf8 scripts/verificar_frontend.py movil
TODO OK
```

## Límite y siguiente gate

La reconstrucción del árbol bajo el proceso de instrumentación usa Keystore real,
pero **no mata ni relanza el proceso**. Tampoco verifica OTP, backend TEST, iOS,
dispositivo físico ni que Android restaure el formulario tras `force-stop`. No
promover H7.S1.M2 de **A MEDIAS** por esta prueba. La suite Patrol completa ya
había perdido el AVD durante un intento combinado; esta corrida aislada no
repara ese gate. No se cambió layout, tema ni motion, por lo que no se atribuye
una nueva verificación visual.
