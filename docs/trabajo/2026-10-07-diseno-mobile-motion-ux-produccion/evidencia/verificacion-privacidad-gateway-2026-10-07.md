# Revisión estática acotada de privacidad — `9377256`

Se revisaron `apps/movil/lib` y `packages/diseno_flutter/lib` buscando salidas a logs y SDK de analytics (`print`, `debugPrint`, `LogInterceptor`, Firebase Analytics, Sentry, Crashlytics). No aparecieron usos en el código de app. El verificador propio también confirma `sin print` en vistas. Esto no prueba que dependencias, sistema operativo o backend no registren datos: faltan escaneo dinámico de payloads y aprobación de Seguridad/Cumplimiento.

Hallazgo corregido: `validarGateway` aceptaba una URL base con credenciales, query o fragmento si el host era propio y la ruta versionada. Ahora devuelve `url-con-datos` sin conservar la URL. Tres pruebas comprueban `userinfo`, query y fragmento. El cambio no modifica contratos ni llamadas financieras.

| Verificación local Windows / Flutter 3.44.8 | Resultado |
|---|---|
| Suite no-golden completa | **274 PASS, 0 FAIL** |
| `flutter analyze --no-pub --fatal-infos` | Sin issues |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK` |
| APK debug con API de Prism por `10.0.2.2` | Construido |

Riesgos abiertos: el borrador de alta conserva datos personales en Keychain/Keystore por hasta 24 horas sin aprobación formal; `ProteccionPantallaIos` no implementa bloqueo de capturas y la app bloquea release iOS por esa capacidad crítica; no hay destino de analytics aprobado; los goldens y la validación real de dispositivo continúan pendientes. No se marca H8.S1.M6 como HECHO.
