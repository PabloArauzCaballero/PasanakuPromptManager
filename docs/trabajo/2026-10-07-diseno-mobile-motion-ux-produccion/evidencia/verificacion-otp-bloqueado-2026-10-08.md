# Alta pausada sin verificación OTP real

Frontend [`c541551`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/c541551), Flutter 3.44.8 en Windows. Es una **contención P0**, no la implementación del OTP ni la finalización del alta.

El paso de contacto ya no afirma que envió un código ni acepta seis dígitos arbitrarios. Explica que no se envió ninguno y que el alta está pausada; permite volver al paso anterior. `AltaNotifier.siguiente()` no cruza el paso de contacto sin verificación y `enviarAlServidor()` no hace el POST sin ella. La app de producción no tiene un método que marque `codigoConfirmado`; solo un notifier de **test** simula esa condición para mantener las pruebas del serializador, contratos y subida de fotos. El backend aún no tiene contrato de emisión/validación OTP pre-registro ni prueba en TEST.

| Comprobación | Resultado |
|---|---|
| Prueba dirigida en claro/oscuro, 360×760/200 % | 2 PASS: aviso, sin `CampoOTP` ni «Continuar», objetivos táctiles, etiquetas, contraste, sin excepción, sin avance ni POST, «Volver» funciona. |
| Suite móvil no-golden | **323/323 PASS**. |
| `flutter analyze --no-pub` | Sin problemas. |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK`. |
| `flutter build apk --debug --no-pub` | PASS, `build/app/outputs/flutter-apk/app-debug.apk`. |

## Evidencia visual local

Capturas de componente con fuente de marca cargada y datos sintéticos, tomadas en el commit indicado e inspeccionadas una por una:

| Celda | Captura | Inspección |
|---|---|---|
| 360×760, claro, texto 200 %, aviso pausado | [PNG claro](./capturas/otp-bloqueado/contacto_bloqueado_light.png) | Sin recorte ni superposición; mensaje y botón «Volver» completos. |
| 360×760, oscuro, texto 200 %, aviso pausado | [PNG oscuro](./capturas/otp-bloqueado/contacto_bloqueado_dark.png) | Sin recorte ni superposición; texto y borde legibles. |

Primera captura exploratoria reveló que «Volver al paso anterior» en dos líneas tocaba el borde del botón a 200 %; se cambió a «Volver», se recapturaron **ambas** celdas y se reinspeccionaron. Los iconos del entorno de `flutter_test` aparecen como cuadrados: estas imágenes no aprueban iconografía ni reemplazan captura de dispositivo. No se capturaron tablet/desktop, iOS, teclado, foco, lector de pantalla ni un flujo backend real. La prueba usa un adaptador HTTP simulado y no ejecuta una auditoría de consola/red de la app real.

El [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37729275738) terminó sin ejecutar pasos; la anotación señala facturación/límite de gasto de GitHub. Flutter/macOS/iOS no quedaron validados remotamente. **H7.S1.M2 sigue A MEDIAS; H8.S1.M1 sigue EN CURSO; DoD total 11/41.** No fusionar el frontend ni presentar este bloqueo como alta terminada.
