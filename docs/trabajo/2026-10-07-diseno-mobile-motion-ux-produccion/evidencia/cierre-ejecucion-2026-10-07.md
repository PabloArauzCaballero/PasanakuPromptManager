# Cierre de ejecución local — 2026-10-07

Código: `PasanakuFrontend` `8308b9a` en PR #15, sobre `origin/dev` `da73387`. Esta evidencia actualiza la continuación anterior, sin sustituir sus límites externos.

## Verificaciones ejecutadas

| Prueba | Resultado |
|---|---|
| `flutter test test/a11y test/identidad test/unidad test/widget --reporter compact` | 178 PASS, 0 FAIL |
| `flutter analyze --fatal-infos` | `No issues found!` |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK`, incluido límite de 200 líneas y ausencia de `print` |
| `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` | `Built build\\app\\outputs\\flutter-apk\\app-debug.apk` después del último cambio |
| `git diff --cached --check` | Sin errores |

El SDK local era Flutter 3.47.5; la configuración de CI usa 3.44.8. La APK se instaló en un AVD Pixel_2 Android API 37. La demora inicial de Gradle fue descarga de artefactos, no bloqueo de compilación.

## Flujo comprobado

Una prueba HTTP simulada crea la cuenta y responde 500 al subir la foto: la cuenta permanece creada, el estado marca `fotosPendientes`, el error de alta es nulo y la copia temporal de la foto desaparece. Otra prueba exige aviso de advertencia en vez de éxito; la pantalla de ingreso a 360×760 con texto al 200 % conserva la acción dentro del viewport. No es E2E con backend real.

Se forzó la ruta `/ingreso?alta=lista&fotos=pendientes` en el AVD con datos sintéticos y se inspeccionaron ambas imágenes:

- [Claro](./android-alta-fotos-pendientes-claro.png): aviso amarillo distinguible, contenido completo, campos y acción visibles; sin recorte ni superposición.
- [Oscuro](./android-alta-fotos-pendientes-oscuro.png): mismo orden de lectura, aviso y contraste coherentes, sin recorte ni superposición.

El emulador con texto al 200 % mató la app por presión de memoria; las capturas posteriores mostraban el launcher y fueron descartadas. El 200 % Android real, TalkBack, VoiceOver, iOS y dispositivo físico continúan sin verificar.

## Riesgos / dependencias que impiden declarar producción

- PR #15 permanece abierto. En la cabeza `8308b9a`, [Actions 37711040763](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37711040763) falló en 3 s; el log del job no estuvo disponible y los jobs Flutter/iOS quedaron `skipping`. El bloqueo de facturación constaba en ejecuciones anteriores; esta nueva ejecución confirma CI rojo, no una causa nueva. No hay CI verde ni merge de código seguro.
- Sin Figma conectado, backend TEST, research con consentimiento, baseline de datos, aprobaciones de Producto/Seguridad/Cumplimiento ni cohorte de lanzamiento. Ninguno se sustituyó por mocks o capturas.
- Búsqueda estática acotada en Dart/Android/iOS sin `print`, `debugPrint`, `developer.log`, `Log.*` o SDKs de telemetría; no reemplaza revisión de payloads/logs en ejecución ni sign-off de privacidad.
- Mantener el conteo **11/41 HECHO**. El trabajo de código aumentó cobertura, pero no satisface por sí mismo los DoD de dispositivo, E2E real, Figma y lanzamiento.
