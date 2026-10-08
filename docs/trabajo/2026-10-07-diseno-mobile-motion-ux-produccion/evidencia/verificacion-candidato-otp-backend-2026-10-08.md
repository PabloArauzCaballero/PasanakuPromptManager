# Verificación aislada del candidato OTP de correo — 2026-10-08

Alcance: rama remota `PasanakuBackend/pablo/feature/verificacion-correo-gmail-test` en `59370bbd`, probada en un worktree temporal separado. No se integró, desplegó ni modificó el backend canónico. El commit de OTP `2f1101f3` no está en `origin/dev` ni `origin/main` y esta rama no tiene PR registrado.

| Prueba dirigida | Runner correcto | Resultado local |
| --- | --- | --- |
| `CU01VerificacionCorreoTest` con PostgreSQL 16 Testcontainers | `:servicios:identidad:integrationTest --tests bo.aportaya.identidad.CU01VerificacionCorreoTest` | 1/1, cero fallos |
| `GmailApiCorreoDeVerificacionTest` | `:servicios:identidad:test --tests bo.aportaya.identidad.GmailApiCorreoDeVerificacionTest` | 2/2, cero fallos; HTTP de Gmail simulado |
| `UsuariosControllerWebTest` y clases anidadas | `:servicios:identidad:webTest --tests bo.aportaya.identidad.web.UsuariosControllerWebTest` | 17/17, cero fallos |

Total dirigido: **20/20**, según XML de JUnit en `servicios/identidad/build/test-results/{integrationTest,test,webTest}`. El primer intento de ejecutar `CU01VerificacionCorreoTest` mediante `test` devolvió «No tests found»: el build lo clasifica en `integrationTest`; se repitió en su runner correcto y pasó. No se ejecutó la suite completa ni se entregó correo real mediante Gmail.

Los tres comandos se ejecutaron desde la raíz del worktree aislado, con `--no-daemon --max-workers=1 --console=plain`:

```text
.\gradlew.bat :servicios:identidad:integrationTest --tests bo.aportaya.identidad.CU01VerificacionCorreoTest
.\gradlew.bat :servicios:identidad:test --tests bo.aportaya.identidad.GmailApiCorreoDeVerificacionTest
.\gradlew.bat :servicios:identidad:webTest --tests bo.aportaya.identidad.web.UsuariosControllerWebTest
```

El intento de pruebas Flutter en esa misma rama **no es una señal de compilación del OTP móvil**. Incluía una ruta de test inexistente (`paso_celular_test.dart`) y el checkout carece de clientes Dart generados y tokens de diseño. `flutter pub get` resolvió dependencias pero la compilación encontró símbolos ausentes. Al inspeccionar `clientes/dart/identidad/pubspec.yaml`, ese paquete se declara explícitamente «DOBLE TEMPORAL» y no publica ningún símbolo del servicio; generar sus `.g.dart` no puede convertirlo en cliente OpenAPI real. Se generaron tokens locales para diagnosticarlo, sin publicarlos. Esta rama backend no sirve por sí sola como base de un test móvil integrado.

Conclusión limitada: el candidato tiene cobertura backend dirigida en verde, pero eso **no aprueba** secuencia, canal, seguridad, entrega real, SMS ni despliegue TEST. Producto, Identidad y Seguridad deben aprobar el contrato; después se integra en el troncal, se genera un cliente Dart real desde el OpenAPI integrado y se prueba el flujo completo con backend TEST y Android/iOS. Hasta entonces H7.S1.M2 permanece A MEDIAS y el frontend PR #15 no debe fusionarse por esta evidencia.
