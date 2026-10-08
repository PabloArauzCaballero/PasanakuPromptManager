# Verificación: alta reanudada con texto ampliado

Frontend [`ea54e17`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/ea54e176794689b04b218e6b56e7e8df50be77fe) · Flutter 3.44.8 en Windows · datos sintéticos «Demo Prueba». H7.S1.M2 sigue A MEDIAS: esta prueba simula cierre/reapertura en widget tests, no app-kill ni teclado/dispositivo real.

## Hallazgo → cambio

Una prueba nueva montó `PantallaDeRegistro`, avanzó hasta captura, persistió el borrador, desmontó la app y creó otro contenedor Riverpod con el mismo almacén. Al reabrir a 360×760 y texto 200 %, recuperaba los datos permitidos y volvía a pedir verificación/fotos, pero la columna de la pantalla desbordaba **100 px**: el aviso de recuperación quedaba fijo por encima del único scroll. Ahora encabezado, aviso y paso forman una sola superficie desplazable. El mismo almacén nunca contiene contraseña, OTP ni ruta de foto; al reabrir vuelven vacíos. La prueba verifica que «Continuar» se alcanza incluso con un inset de teclado simulado de 300 px.

En la pasada visual, el selector SMS/correo cortaba ambas etiquetas a 200 %. `SelectorSegmentado` ahora usa opciones verticales con altura táctil mínima y texto completo al crecer la escala, sin cambiar el valor seleccionado; la transición respeta `disableAnimations`. Se acortaron el aviso de recuperación y la ayuda de mayoría de edad, sin alterar la condición.

## Capturas abiertas e inspeccionadas

| Celda | Captura | Inspección |
|---|---|---|
| Celular recuperado · 360×760 · 200 % · claro | [PNG](./alta_reanudada_celular_claro-2026-10-08.png) | Aviso, instrucción y seis celdas visibles; CTA deshabilitado visible, sin recorte. |
| Celular recuperado · 360×760 · 200 % · oscuro | [PNG](./alta_reanudada_celular_oscuro-2026-10-08.png) | Igual; contraste de aviso y celdas legible. |
| Datos recuperados · 360×760 · 200 % · claro | [PNG](./alta_reanudada_datos_claro-2026-10-08.png) | Encabezado, aviso y primer campo accesibles mediante scroll único; no se promete acción completada. |
| Datos recuperados · 360×760 · 200 % · oscuro | [PNG](./alta_reanudada_datos_oscuro-2026-10-08.png) | Igual; campo y aviso conservan límites visibles. |
| Datos, parte inferior · 360×760 · 200 % · claro | [PNG](./alta_reanudada_datos_accion_claro-2026-10-08.png) | Selector vertical y ayuda de edad completos; «Continuar» visible. |
| Datos, parte inferior · 360×760 · 200 % · oscuro | [PNG](./alta_reanudada_datos_accion_oscuro-2026-10-08.png) | Opciones completas y contraste de selección legible; CTA visible. |
| Datos, inset de teclado 300 px · 360×760 · 200 % · claro | [PNG](./alta_reanudada_datos_teclado_claro-2026-10-08.png) | «Continuar» permanece por encima del inset simulado; no es una captura de teclado del SO. |

Los iconos cuadrados son del rasterizador de widget tests Windows, no evidencia del icono real. No hubo consola/red de dispositivo ni capturas iOS/Android para este cambio. No se capturaron tablet/desktop porque el cambio corresponde al asistente nativo móvil; faltan anchuras de dispositivo y lector de pantalla.

## Comandos y resultados

```text
apps/movil: flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact
00:21 +314: All tests passed!
packages/diseno_flutter: flutter test --no-pub test/a11y test/unidad test/widget --reporter compact
00:03 +43: All tests passed!
apps/movil y packages/diseno_flutter: flutter analyze --no-pub --fatal-infos
No issues found!
python -X utf8 scripts/verificar_frontend.py movil
TODO OK
flutter build apk --debug --no-pub
Built build\app\outputs\flutter-apk\app-debug.apk
```

La suite de goldens Windows volvió a **10 PASS / 3 FAIL** (saldo claro/oscuro y transición), igual que antes. No se actualizaron referencias macOS. [CI de `ea54e17`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37727340213) no inició ningún paso: GitHub anota pagos fallidos/límite de gasto; Flutter/macOS/iOS quedaron omitidos. PR #15 sigue abierto y no debe forzarse.

## Bloqueo P0 descubierto: OTP previo al registro

La pantalla de contacto dice «Te enviamos un código» y `AltaNotifier.confirmarCelular()` solo marca un booleano local cuando se llenan seis celdas. La búsqueda en el contrato `servicios/identidad/src/main/resources/openapi/identidad.yaml` no encuentra una operación de emisión o validación de OTP previa a `POST /usuarios`; el `EntradaRegistro` tampoco incluye un comprobante de OTP. Por tanto **no está demostrado que se envíe ni valide ese código**. No se añadió una API ficticia ni se declaró verificación real. Producto/Identidad/Seguridad deben definir si la verificación sucede antes o después del registro, su contrato versionado, caducidad/reintentos y estados UX; luego probarlo contra backend TEST. Hasta entonces H7.S1.M2 no es HECHO ni el alta es release candidate.
