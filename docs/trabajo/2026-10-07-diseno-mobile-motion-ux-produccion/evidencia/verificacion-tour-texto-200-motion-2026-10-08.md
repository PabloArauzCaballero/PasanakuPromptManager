# Tour de activación: texto 200 % y movimiento reducido — 2026-10-08

- Código: `PasanakuFrontend` `04a6733`–`fe54619`, [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Antes: el test nuevo en 320×760/texto 200 % falló con `A RenderFlex overflowed by 927 pixels on the bottom`. El tour no tenía desplazamiento vertical. En la primera captura local previa a compactar el arte, la explicación quedaba totalmente fuera del primer encuadre.
- Ahora: cada lámina se desplaza verticalmente, sin mover la acción principal del pie; el arte se compacta a texto grande, pero el texto conserva el 200 %. «Siguiente» salta de página bajo `disableAnimations`; el pie evita `AnimatedSize` en ese modo. La prueba ampliada detectó que `AnimatedSize` con duración cero fallaba al llegar a la cuarta lámina y se corrigió.

## Salidas literales

```text
flutter test --no-pub test/a11y/tour_texto_grande_test.dart test/widget/tour_movimiento_reducido_test.dart test/goldens/tour_texto_grande_golden_test.dart --reporter expanded
00:01 +9: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart test/goldens/tour_texto_grande_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:27 +491: All tests passed!

flutter analyze --no-pub
No issues found! (ran in 4.4s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

La prueba de accesibilidad recorre las cuatro láminas a 320×760/texto 200 % en ambos temas, lleva el párrafo al área visible, comprueba que el CTA permanece dentro del viewport y pasa los gates de tamaño/etiqueta táctil en primera y última lámina. La prueba de motion recorre las tres transiciones por botón con `disableAnimations=true`, verifica página entera y contenido final después de un solo frame, sin excepción. No prueba un gesto real en iOS/Android.

## Inspección visual local

Se abrieron las seis imágenes a resolución original después de la última edición visual. Todas son fixtures sintéticos del rasterizador Windows; la URL de cada archivo está fijada al commit `fe54619`.

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
- [CI del corte](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37751067024) no inició jobs por pagos/límite de GitHub Actions; Flutter, goldens macOS e iOS quedaron `SKIPPED`. PR #15 sin merge.
