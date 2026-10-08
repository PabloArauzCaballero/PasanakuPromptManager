# Tour de activación: texto 200 % y movimiento reducido — 2026-10-08

- Código: `PasanakuFrontend` `04a6733`–`0cb7015`, [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Antes: el test nuevo en 320×760/texto 200 % falló con `A RenderFlex overflowed by 927 pixels on the bottom`. El tour no tenía desplazamiento vertical. En la primera captura local previa a compactar el arte, la explicación quedaba totalmente fuera del primer encuadre.
- Ahora: cada lámina se desplaza verticalmente, sin mover la acción principal del pie; el arte se compacta a texto grande, pero el texto conserva el 200 %. «Siguiente» salta de página bajo `disableAnimations`; el pie evita `AnimatedSize` en ese modo. La prueba ampliada detectó que `AnimatedSize` con duración cero fallaba al llegar a la cuarta lámina y se corrigió. Una revisión posterior encontró que los puntos aún animaban 150 ms: `0cb7015` los vuelve instantáneos y añade prueba directa en el sistema de diseño.

## Salidas literales

```text
# Desde apps/movil
flutter test --no-pub test/a11y/tour_texto_grande_test.dart test/widget/tour_movimiento_reducido_test.dart test/goldens/tour_texto_grande_golden_test.dart --reporter expanded
00:01 +9: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart test/goldens/tour_texto_grande_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:29 +491: All tests passed!

flutter analyze --no-pub
No issues found! (ran in 29.0s)

# Desde packages/diseno_flutter
flutter test --no-pub test/widget --reporter compact
00:03 +28: All tests passed!
flutter test --no-pub test/widget test/a11y test/unidad --reporter compact
00:03 +51: All tests passed!
flutter analyze --no-pub
No issues found! (ran in 9.3s)

# Suite completa del sistema de diseño en Windows, incluye goldens macOS
flutter test --no-pub test --reporter compact
+60 -15: Some tests failed.

# Desde la raíz de PasanakuFrontend
python -X utf8 scripts/verificar_frontend.py movil
TODO OK

# Desde apps/movil
flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

La prueba de accesibilidad recorre las cuatro láminas a 320×760/texto 200 % en ambos temas, lleva el párrafo al área visible, comprueba que el CTA permanece dentro del viewport y pasa los gates de tamaño/etiqueta táctil en primera y última lámina. La prueba de motion recorre las tres transiciones por botón con `disableAnimations=true`, verifica página entera, contenido final y duración cero de los cuatro puntos después de un solo frame, sin excepción. No prueba un gesto real en iOS/Android.

La suite completa de diseño **no está verde en Windows**: fallan por comparación de píxeles los catorce goldens del catálogo (claro/oscuro) y el test de cuadros intermedios de la apertura de marca; los otros 60 tests pasan. El propio catálogo documenta que sus bases se generaron en macOS y que la comparación entre rasterizadores no es un gate confiable. La diferencia de `Organismos` llega al 37,47 %, así que no se atribuye toda discrepancia a rasterización ni se regeneran bases a ciegas. Repetir esa suite en macOS, inspeccionar los diffs y resolver las divergencias antes de usarla como evidencia de salida. Los 28 tests dirigidos de widgets y los seis goldens nuevos del tour sí pasaron en Windows.

## Inspección visual local

Se abrieron las seis imágenes a resolución original. Son fixtures sintéticos del rasterizador Windows fijados a `fe54619`; `0cb7015` solo cambia la duración en modo reducido y las comparaciones golden siguieron pasando sin actualizar las imágenes.

| Celda | Captura | Inspección |
|---|---|---|
| 320×760, 200 %, claro, primer encuadre | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_320_texto_200_light.png) | OK: arte compacto, título completo, inicio del párrafo y CTA visibles; sin overflow. |
| 320×760, 200 %, claro, párrafo desplazado | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_320_texto_200_scroll_light.png) | OK: párrafo completo, pie persistente; el título sale por arriba por el scroll, no por recorte. |
| 320×760, 200 %, oscuro, primer encuadre | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_320_texto_200_dark.png) | OK: texto y CTA legibles, sin superficie clara hardcodeada. |
| 320×760, 200 %, oscuro, párrafo desplazado | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_320_texto_200_scroll_dark.png) | OK: cuerpo alcanzable y pie visible; sin superposición. |
| 320×760, 200 %, oscuro, cuarta lámina | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_320_texto_200_ultima_dark.png) | OK: título completo, comienzo del cuerpo, Crear mi cuenta y Ya tengo cuenta visibles. |
| 768×1024, claro, texto normal | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/fe54619/apps/movil/test/goldens/imagenes/tour_768_light.png) | OK: composición centrada y acción clara; densidad baja en tablet, nit no bloqueante. |

Rúbrica local: 15/16 (jerarquía 2, alineación 2, espacio 2, sistema 2, contraste 2 por colores base de tokens, densidad 1, estados aplicables 2, pulido 2). Contraste calculado frente al fondo base: claro `text` 14,93:1, `text2` 8,91:1, `brandTexto` 7,41:1; oscuro 15,20:1, 10,18:1 y 5,25:1. El aura modifica algunos píxeles: queda pendiente comprobación en pantalla real. La captura previa al ajuste de arte se inspeccionó pero no se conservó como archivo versionado; el test rojo sí conserva el defecto de overflow.

## Límites

- Peldaño TESTED + inspección visual local, no VERIFIED de dispositivo: no hubo TalkBack/VoiceOver, Android/iOS estable, captura de red/consola real ni prueba con personas. No se usaron respuestas de backend porque el tour no consulta datos.
- No hay viewport desktop porque es la app Flutter nativa; la matriz cubre teléfono estrecho y tablet Windows. Goldens de macOS requieren baseline e inspección propia.
- [CI del corte](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37752117356) no inició jobs por pagos/límite de GitHub Actions; Flutter, goldens macOS e iOS quedaron `SKIPPED`. PR #15 sin merge.
