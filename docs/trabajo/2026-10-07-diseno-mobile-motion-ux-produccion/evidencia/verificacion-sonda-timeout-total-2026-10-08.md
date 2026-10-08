# Sonda de conexión con plazo total — 2026-10-08

Alcance: `PasanakuFrontend` [`ccce1a4`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/ccce1a4), PR #15. H8.S1.M3 permanece **EN CURSO**.

## Defecto reproducido

La sonda tenía `connectTimeout` de 3 segundos para abrir el socket, pero no un plazo para toda la operación. Si el gateway aceptaba el socket y nunca respondía, o si `connectivity_plus` no completaba su consulta, `hayConexion()` podía permanecer pendiente y la UI seguir en «Comprobando conexión» sin fin.

Se añadieron dos pruebas que primero fallaron: la primera no compilaba sin el nuevo parámetro de plazo; la segunda terminaba por el timeout externo del test a los 2 segundos al bloquear la consulta al sistema. El arreglo limita a 3 segundos el ciclo completo de consulta al sistema + GET `/version`, cancela la petición HTTP al vencer y evita un GET tardío si el plugin responde después del límite. La sonda devuelve `false` y la guardia monetaria no habilita un POST sin una confirmación positiva.

## Verificación local final

- `flutter test --no-pub test/unidad/conectividad_android_test.dart --reporter expanded`: **8/8 PASS**, incluidos servidor HTTP local que acepta pero no responde y plugin simulado que responde tarde.
- `flutter test --no-pub test/unidad test/widget test/contrato test/identidad test/pasanaku test/a11y --reporter json`: `{"success":true,"type":"done"}`; suite no-golden completa en verde.
- `flutter analyze --no-pub`: sin issues. `PYTHONUTF8=1 python scripts/verificar_frontend.py movil`: TODO OK. `flutter build apk --debug --no-pub`: APK generado. El primer intento del verificador con Python 3.14/CP1252 falló al decodificar un archivo UTF-8; se repitió con `PYTHONUTF8=1` y pasó, sin cambiar el verificador.

## Límite

La prueba usa HTTP de loopback y un plugin simulado en Windows, no una caída real de gateway en Android/iOS ni backend TEST. El booleano del puerto actual considera «sin conexión útil» tanto una pérdida de red como una sonda sin respuesta; esta evidencia no demuestra que el banner distinga por sí solo un gateway saturado de un teléfono offline. La matriz de timeout/500/app kill/reintento en dispositivos y la observación de resultado financiero siguen pendientes.
