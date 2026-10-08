# Privacidad móvil: escaneo parcial de rutas, logs y capturas

Frontend [`637160d`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/637160d84f4c720750c6b6192b14da22eee66ae5) · H8.S1.M6 **EN CURSO**, no cerrado. Esta es revisión estática del código local, no auditoría formal ni prueba de payloads reales.

## Amenaza, control y prueba

- **Amenaza:** un deep link externo con documento o importe en query podía quedar copiado dentro del `StateError` de ruta desconocida. `EstadoError` hoy muestra un mensaje genérico, pero un monitor de errores futuro podría exportar el objeto original. Una URL con datos identificatorios/financieros ya es indebida; repetirla en un error agrava la exposición.
- **Control:** `apps/movil/lib/navegacion/rutas.dart` ya crea `StateError('Ruta no encontrada')` sin interpolar `state.uri`. No se añadieron logs ni SDKs.
- **Prueba negativa:** `apps/movil/test/widget/deep_link_test.dart` abre una ruta inexistente con `documento=CI_FICTICIA&monto=125.00` **sintéticos** y comprueba que ninguna de esas cadenas entra al error. No se copió información de producción; no hubo datos enmascarados en la salida de prueba.
- **Resultado literal:** `flutter test --no-pub test/widget/deep_link_test.dart` → `+4: All tests passed!`; suite móvil sin goldens → `+315: All tests passed!`; `flutter analyze --no-pub --fatal-infos` → `No issues found!`; `python -X utf8 scripts/verificar_frontend.py movil` → `TODO OK`; `flutter build apk --debug --no-pub` → `Built build\app\outputs\flutter-apk\app-debug.apk`.

## Superficies revisadas

| Búsqueda | Resultado y límite |
|---|---|
| `rg` de `print`, `debugPrint`, `developer.log`, `LogInterceptor`, Sentry y analytics en `apps/movil/lib` y `packages/diseno_flutter/lib` | 0 coincidencias. No prueba que SDK nativos o servicios externos estén limpios. |
| `rg` de `Log.`, `println`, `NSLog`, `print(` en `apps/movil/android/app/src/main` y `apps/movil/ios/Runner` | 0 coincidencias en ese alcance. |
| `rg` de `queryParameters` en `apps/movil/lib` | 22 usos inspeccionados: IDs internos, flags de navegación y `volver`; el importe de aporte fue retirado de la ruta en `7c12866`. `volver` se filtra a la forma de invitación interna por `retornoDeInvitacion`, pero ese flujo de token en URL requiere revisión específica de Seguridad. |
| Protección de captura | Android registra `FLAG_SECURE`; iOS declara `ProteccionPantallaIos` no soportada y el release iOS sigue bloqueado. No se probó el comportamiento en dispositivo en este corte. |

## Riesgo residual / gate faltante

No hubo backend TEST, inspección de peticiones/respuestas reales, logs de gateway/servicios, trazas, métricas, SDK de crash, auditoría de lecturas, ni revisión Seguridad/Cumplimiento. Las capturas de diseño versionadas son sintéticas; no certifican que la app real nunca capture datos sensibles. El borrador cifrado de alta conserva datos personales hasta 24 h y aún requiere aprobación de retención. La ruta de invitación lleva un token de acción en URL por diseño: verificar propósito único, vencimiento, revocación y no exposición en logs antes del piloto. No se declara H8.S1.M6 HECHO.

El [CI remoto de este commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37727729344) volvió a terminar antes de ejecutar pasos por facturación de GitHub; Flutter/macOS/iOS se omitieron. PR #15 sigue abierto/UNSTABLE.
