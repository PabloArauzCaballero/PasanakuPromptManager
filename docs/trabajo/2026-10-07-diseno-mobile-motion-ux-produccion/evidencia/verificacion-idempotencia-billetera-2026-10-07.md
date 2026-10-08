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

## Continuación: resultado incierto (`c2e0309`)

- `ErrorDeResultadoIncierto` traduce timeout y 5xx sin afirmar que el POST falló; conserva la traza de API cuando existe. El reintento sigue siendo manual y visible con la misma clave. Un 409 se trata como operación pendiente: se pide consultar el estado, se ocultan los reintentos y se bloquea el botón principal.
- Pruebas nuevas: clasificación de timeout, 500 y 409; retiro y transferencia con 503 a 360×640 y texto 200 % sin overflow, con traza y reintento visibles. La prueba de recarga afirma el nuevo mensaje tras timeout. Suite no-golden **302 PASS, 0 FAIL**; `flutter analyze --no-pub`, verificador frontend y APK debug PASS. Golden suite Windows **10 PASS, 3 FAIL** en los mismos casos de saldo/transición; no se actualizaron referencias.
- [CI 37720766770](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37720766770) para `c2e0309` repite la anotación de facturación; Flutter/macOS/iOS omitidos. PR #15 sigue abierta, sin aprobación de release.
- Desajuste backend que requiere reconciliación contractual: el plan maestro prescribe replay idempotente con **200 y la respuesta original** (`planes/00 Plan maestro.md`), mientras el OpenAPI de `nucleo-financiero` declara **201** para CU-10/11/12 y `BilleteraController` construye 201 incluso si el caso de uso devuelve una orden existente. No se cambió backend en este alcance; confirmar semántica y demostrar efecto único con backend TEST antes de cerrar H8.S1.M3.

### Capturas sintéticas inspeccionadas

Se forzó un 503 con adaptador HTTP de prueba y datos ficticios. Son PNG de `flutter_test` en Windows con fuente Ahem y banner DEBUG; permiten revisar geometría/scroll/contraste aproximado, **no** legibilidad tipográfica final ni UI en Android/iOS. Todas se abrieron e inspeccionaron: no se observó corte horizontal ni superposición; en 360 px el error requiere scroll y el CTA de reintento aparece al desplazar; en 600 px cabe sin desplazamiento. No se capturó teclado real ni consola/red de una app ejecutada.

| Viewport · tema · posición | Captura | Inspección |
| --- | --- | --- |
| 360×640 · claro · arriba | [PNG](./recarga-503-360-claro-arriba.png) | Mensaje continúa bajo viewport; scroll disponible, sin overflow. |
| 360×640 · claro · reintento | [PNG](./recarga-503-360-claro-reintento.png) | Reintento y acción primaria alcanzables; sin superposición. |
| 360×640 · oscuro · arriba | [PNG](./recarga-503-360-oscuro-arriba.png) | Misma geometría; fondos y bordes presentes. |
| 360×640 · oscuro · reintento | [PNG](./recarga-503-360-oscuro-reintento.png) | Ambos controles visibles y separados. |
| 600×900 · claro · arriba | [PNG](./recarga-503-600-claro-arriba.png) | Error y CTA completos en viewport; espacio inferior amplio. |
| 600×900 · claro · reintento | [PNG](./recarga-503-600-claro-reintento.png) | Igual a arriba: no requiere scroll. |
| 600×900 · oscuro · arriba | [PNG](./recarga-503-600-oscuro-arriba.png) | Jerarquía y bordes visibles; sin recorte. |
| 600×900 · oscuro · reintento | [PNG](./recarga-503-600-oscuro-reintento.png) | Igual a arriba: no requiere scroll. |

No cubierto: un teléfono real, notch, teclado nativo, VoiceOver/TalkBack, fuente final, estados de éxito/carga en estas capturas y resultado contra backend TEST. El nivel es **verificación funcional más inspección visual parcial sintética**, no aprobación visual de producción.

## Continuación: aporte y conciliación (`faf75ea`)

- CU-21 comparte la traducción de timeout/5xx como resultado incierto con billetera. Un 409 o una huella de aporte pendiente con otros datos ya no ofrece «Volver a intentar»; requiere revisar el estado o consultar soporte. Se agregó prueba widget del 409 a 360×760 y texto 200 %, y la prueba de aporte pendiente verifica la ausencia de reenvío. Los reintentos 503 con la misma clave siguen probados.
- Flutter 3.44.8: **303 PASS, 0 FAIL** no-golden; `flutter analyze --no-pub`, verificador de frontend y APK debug PASS. La [ejecución CI 37721477629](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37721477629) para `faf75ea` repite la anotación de facturación y omite Flutter/macOS/iOS. PR #15 permanece abierta. Goldens Windows no se actualizaron; el último conteo verificado fue **10 PASS/3 FAIL** en `c2e0309`.
- Capturas sintéticas con adaptador 409 y referencia ficticia, abiertas e inspeccionadas: [360×760 claro](./aporte-409-360-claro.png) y [360×760 oscuro](./aporte-409-360-oscuro.png). El mensaje cabe sin corte visible ni CTA de reenvío; contraste solo aproximado por Ahem/DEBUG. No se registró consola/red de app real, ni se hizo prueba contra backend TEST, Android/iOS, lector de pantalla o tipografía final. Nivel: **funcional más inspección geométrica local**, no gate visual de producción.

Intento Android adicional: se inició el AVD `Pixel_2` sin ventana y con RAM virtual reducida a 768 MB. ADB llegó a mostrar `emulator-5554` como `device`, pero `sys.boot_completed` seguía vacío y la RAM libre del host cayó de ~2,2 GB a ~380 MB. Se apagó únicamente ese emulador con `adb -s emulator-5554 emu kill`; la RAM libre volvió a ~2,5 GB. **No hubo boot completo, instalación, recorrido ni captura Android**. Repetir el gate en Mac/dispositivo con recursos suficientes.

Se repitió una sola vez tras recuperar ~3,3 GB libres: `Pixel_2`/Android 17 volvió a aparecer en ADB, pero `sys.boot_completed` permaneció vacío y el host cayó a ~440 MB libres. Se apagó de nuevo solo ese AVD; la RAM se recuperó a ~3,2 GB. El límite de esta PC se considera confirmado para este AVD; no se ejecutaron recorridos de producto.
