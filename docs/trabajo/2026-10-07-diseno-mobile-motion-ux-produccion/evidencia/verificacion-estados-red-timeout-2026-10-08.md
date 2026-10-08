# Sin conexión y timeout son estados distintos

Frontend [`046ef76`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/046ef76), Flutter 3.44.8 en Windows. Es una mejora local de H8.S1.M3, que sigue **EN CURSO**.

Antes, todo error HTTP sin respuesta terminaba como `ErrorDeRed`: un timeout podía mostrar el icono de Wi-Fi caído, y una carga inicial decía «Te mostramos lo último que vimos» aunque no hubiese datos. Ahora el interceptor distingue espera agotada de fallo de conexión. La billetera muestra «La respuesta tardó demasiado. Intentá de nuevo» en el primero y «No pudimos conectarnos. Revisá tu conexión e intentá de nuevo» en el segundo. En operaciones de dinero ambos siguen siendo **resultado incierto**, no un fallo de cobro confirmado; solo una falla de conexión usa la variante visual offline. La clave de idempotencia no se cambió.

| Comprobación | Resultado |
|---|---|
| Pruebas de traducción y dominio | `receiveTimeout` → `ErrorDeTiempoDeEspera` no offline; `connectionTimeout` financiero → resultado incierto no offline; `connectionError` financiero → resultado incierto offline; 500 y 409 conservan su tratamiento previo. |
| Billetera, 360×760/200 %, claro/oscuro | 4 pruebas PASS: mensaje, icono correspondiente, reintento, objetivos táctiles, etiquetas, contraste y ausencia de excepción de layout. HTTP interceptado con fallos sintéticos. |
| Suite móvil no-golden | **329/329 PASS**. |
| `flutter analyze --no-pub` | Sin problemas. |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK`. |
| `flutter build apk --debug --no-pub` | PASS. |

## Capturas inspeccionadas

| Celda | Captura | Inspección |
|---|---|---|
| 360×760/200 %, claro, sin conexión | [PNG](./capturas/estados-red-saldo/saldo_connectionError_light.png) | Mensaje y botón completos; sin recorte, superposición ni fondo oscuro indebido. |
| 360×760/200 %, claro, timeout | [PNG](./capturas/estados-red-saldo/saldo_receiveTimeout_light.png) | Mensaje y botón completos; no se afirma falta de red. |
| 360×760/200 %, oscuro, sin conexión | [PNG](./capturas/estados-red-saldo/saldo_connectionError_dark.png) | Contraste y jerarquía legibles; sin recorte. |
| 360×760/200 %, oscuro, timeout | [PNG](./capturas/estados-red-saldo/saldo_receiveTimeout_dark.png) | Contraste y jerarquía legibles; no se afirma falta de red. |

Son capturas de `flutter_test` con fuente de marca y datos sintéticos. Los iconos se rasterizan como cuadrados en este entorno; la prueba comprueba el tipo de icono en el árbol, pero **no** aprueba la iconografía. No se verificaron tablet/desktop, dispositivo real, iOS, TalkBack/VoiceOver, teclado, consola/red de app real ni backend TEST. Los fallos de red son inyectados; la comprobación no prueba comportamiento de infraestructura. El [CI de `046ef76`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37729723735) tampoco inició pasos por facturación/límite de gasto. No fusionar frontend como release candidate.
