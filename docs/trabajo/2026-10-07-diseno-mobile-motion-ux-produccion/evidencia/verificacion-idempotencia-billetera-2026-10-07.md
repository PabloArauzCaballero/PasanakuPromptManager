# Evidencia — reintentos monetarios persistidos (`be2feeb`)

Fecha: 2026-10-07. Código en `PasanakuFrontend`, rama `codex/mobile-design-merge-2026-10-07`, PR #15 contra `dev` (`da73387`). SDK local: Flutter 3.44.8 / Dart 3.12.2 en Windows.

## Cambio y prueba

- `CU-10`, `CU-11` y `CU-12` guardan `{version, clave, huella}` en `AlmacenSeguro` antes del POST. La huella vincula importe, destino/medio y concepto donde aplica. En retiro excluye el factor MFA: no se guarda ni se hashea el secreto. Respuesta confirmada limpia el registro; fallo o respuesta incierta lo conserva. Un registro corrupto o una huella distinta impiden el POST y exigen consultar el estado con soporte.
- Seis pruebas unitarias nuevas: 503 y recreación de `ProviderContainer` con clave idéntica para cada operación, datos distintos, registro corrupto y no persistencia del MFA. Dos pruebas widget nuevas: el reintento de recarga hace un segundo POST con la misma clave; datos pendientes diferentes hacen **cero POST** y ocultan el reintento. El formulario a 360×640 con texto 200 % reproducía overflow de 513 px; tras scroll, no hay excepción y el envío queda deshabilitado en conflicto.
- `flutter analyze --no-pub`: sin problemas. `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget`: **297 PASS, 0 FAIL**. `python -X utf8 scripts/verificar_frontend.py movil`: OK. `flutter build apk --debug --no-pub`: PASS después del último cambio. `git diff --check`: OK.

## Límites de la evidencia

- Las pruebas monetarias usan adaptador HTTP simulado y reinicio de contenedor, **no** backend TEST ni cierre real del proceso. La garantía del servidor sobre idempotencia, el estado después de timeout, las credenciales y la autorización de cuenta siguen sin validarse. El login tampoco resuelve una `cuentaId` autorizada para activar la billetera.
- La corrida global de goldens Windows mantiene **10 PASS/3 FAIL**: saldo claro/oscuro y transición de ingreso. Sus baselines se crearon en macOS; no se sustituyeron desde Windows. No se capturó este estado en Android/iOS real ni se hizo inspección visual completa de recarga tras el cambio. En Mac se deben repetir goldens, revisar capturas y teclado real en claro/oscuro y texto grande antes de aprobar UI.
- PR #15 continúa abierta. La [ejecución CI 37719806692](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37719806692) para `be2feeb` muestra la anotación exacta «The job was not started because recent account payments have failed or your spending limit needs to be increased»; Flutter/macOS/iOS quedaron omitidos. No hay CI verde ni merge seguro. El programa conserva **11/41 HECHO**; esta mejora reduce riesgo pero no satisface por sí sola los DoD de backend/dispositivo/release.
