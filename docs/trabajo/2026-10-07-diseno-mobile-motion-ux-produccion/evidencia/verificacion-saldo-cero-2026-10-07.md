# Saldo cero y legibilidad móvil — `f128a33`

El `saldoProvider` ya devolvía un saldo real de `0.00`, pero `PantallaDeSaldo` lo trataba como pantalla vacía y ocultaba el importe, «Recargar» y el contexto. Ahora se usa el cuerpo normal, que conserva el saldo cero y muestra «Todavía no tenés movimientos» en su sección. No se suma dinero en memoria ni se sustituye la respuesta del servidor.

La prueba a 360×760 y texto al 200 % encontró primero un desborde horizontal de 88 px en el desglose «Retenido». Se cambió la fila por un `Wrap`. Una aserción de `RenderParagraph.didExceedMaxLines` detectó después que la fila de tres acciones cortaba «Aportar» incluso al 100 %, y que una fila de dos cortaba «Recargar». El layout final apila las tres acciones cuando el ancho interno es menor que 520 dp multiplicados por la escala de texto. En pantallas amplias conserva la fila de tres.

| Comprobación con Flutter 3.44.8 / Dart 3.12.2 | Resultado |
|---|---|
| `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact` | **253 PASS, 0 FAIL** |
| `flutter analyze --no-pub --fatal-infos` | `No issues found!` |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK` |
| `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` | APK debug construido |
| `flutter test --no-pub test/goldens --reporter expanded` | **4 PASS, 3 FAIL** en Windows |

Los 54 casos de saldo cero cruzan 9 anchos (360, 390, 430, 480, 520, 550, 552, 554 y 600 px), temas claro/oscuro y escalas de texto 100/140/200 %. Incluyen anchos a ambos lados del breakpoint. Exigen importe cero anunciado, botón «Recargar» alcanzable, las tres etiquetas sin elipsis y ausencia de excepciones de layout. Dos casos adicionales prueban saldo con fondos a 360×760/200 % en ambos temas. Son pruebas de widget con red simulada; no prueban backend ni dispositivo.

Las imágenes de resultado del golden de saldo en claro y oscuro se abrieron e inspeccionaron: no se observó recorte geométrico, y la nueva columna de acciones explica el **44 % de diferencia de píxeles** frente al snapshot anterior. Esas imágenes usan tipografía Ahem del entorno de test, por lo que no validan legibilidad real, contraste percibido ni fidelidad macOS. No se actualizó ningún snapshot. Los otros fallos son los cuatro cuadros agrupados en el test de transición. En [Actions 37715305633](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37715305633), GitHub no inició los jobs por pagos fallidos o límite de gasto; Flutter/macOS/iOS fueron omitidos. PR #15 continúa abierto.

Pendiente para H7.S1.M3/H8.S1.M4: captura real de saldo cero y normal en Android/iOS o simulador Mac con tipografía real, claro/oscuro y texto 200 %; inspección de cada imagen, golden macOS actualizado solo tras revisión, y prueba de navegación «Recargar» con cuenta real de TEST. No declarar la portada verificada visualmente ni lista para release hasta entonces.
