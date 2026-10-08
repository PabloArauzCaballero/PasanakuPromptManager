# Revisión de aporte y teclado móvil — `fd73088` / `79470be`

En `PantallaAportar`, el botón inicial ahora abre una revisión de monto, medio y referencia sin enviar el POST. Solo «Confirmar aporte» llama al caso de uso. «Cambiar datos» conserva la referencia antes del primer envío; tras un fallo, no ofrece editar datos de un intento monetario incierto. El aviso distingue «todavía no enviamos» de «el intento anterior podría haber llegado». Pruebas widget: cero peticiones al revisar/editar, un POST con doble toque, misma clave en reintento y rechazo de huella distinta en almacén seguro. **El monto aún viene de query**, no de un GET de obligación autorizada: esta UI no habilita release financiero.

En retiro/transferencia, la prueba inicial con 360×760 lógicos, inset de teclado de 300 dp y texto al 200 % mostró `RenderFlex overflowed by 219 pixels` y `209 pixels`. Se sustituyó el `Column` fijo por `CustomScrollView` + `SliverFillRemaining`; seis combinaciones (recarga/retiro/transferencia × claro/oscuro) comprueban que campo enfocado y CTA quedan dentro de la zona no cubierta, sin excepción. Otras seis pasan las guías Flutter de objetivo táctil Android, etiqueta y contraste. Es un teclado **simulado por inset**, no un recorrido en dispositivo.

| Captura Flutter 360×760, datos sintéticos | Inspección |
|---|---|
| `test/goldens/imagenes/aporte_revision_claro.png` | Monto focal, medio/referencia legibles; confirmar y cambiar datos visibles. |
| `test/goldens/imagenes/aporte_revision_oscuro.png` | Misma jerarquía; sin fondo claro accidental ni recortes. |
| `test/goldens/imagenes/retirar_formulario_claro.png` | Tres campos alineados y CTA deshabilitado al pie; sin overflow. |
| `test/goldens/imagenes/retirar_formulario_oscuro.png` | Campos y bordes distinguibles; sin recorte. |
| `test/goldens/imagenes/transferir_formulario_claro.png` | Selector, campos y CTA alineados; sin solapamiento. |
| `test/goldens/imagenes/transferir_formulario_oscuro.png` | Variante oscura consistente; sin recorte. |

Las dos capturas de formulario de aporte se actualizaron **solo** tras inspeccionar el diff: cambiaba únicamente el texto del botón de «Aportar» a «Revisar aporte» (0,26 % de píxeles). No se regeneraron los snapshots de saldo/transición.

| Verificación local Windows / Flutter 3.44.8 | Resultado |
|---|---|
| Suite no-golden completa | **289 PASS, 0 FAIL** |
| `flutter analyze --no-pub --fatal-infos` | Sin issues |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK` |
| APK debug con API de Prism por `10.0.2.2` | Construido |
| Suite de goldens | **10 PASS, 3 FAIL**: saldo claro/oscuro y transición |

No se capturó esta iteración en Android/iOS real, ni se probó el pago contra backend TEST. La inspección visual es local de Flutter; no sustituye tipografía, teclado, safe area, lector de pantalla ni rendimiento en dispositivo. GitHub Actions sigue impidiendo arrancar jobs por facturación; PR #15 permanece abierta y no se forzó merge.
