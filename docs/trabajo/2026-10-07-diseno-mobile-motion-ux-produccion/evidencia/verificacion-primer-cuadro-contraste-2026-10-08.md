# Primer cuadro reducido y contraste oscuro de marca — 2026-10-08

- Código: `PasanakuFrontend` [`7ffc6aa`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/7ffc6aa), [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Alcance: H7.S1.M8, H8.S1.M1 y evidencia parcial H8.S1.M4. Sin cambio en rutas, operación monetaria, backend ni duración normal de la marca.

## Defectos reproducidos antes de corregir

1. El test de movimiento reducido decía «primer cuadro», pero llamaba un `pump()` adicional. Al exigir la ausencia de `AperturaDeMarca` inmediatamente después de `pumpWidget`, falló: `Actual: Found 1 widget`. La portada quedaba cubierta durante un cuadro. `_ConApertura.didChangeDependencies` ahora lee la preferencia del sistema antes del primer `build`, omite el velo y cancela el respaldo; otro test activa la preferencia durante la apertura y comprueba que sale.
2. Las pastillas de garantías de la portada usaban `brandTexto` oscuro `#419F6E` sobre `brandBg` `#164A30`: contraste **3,1168:1**. La aserción nueva `>= 4.5` fue roja solo en oscuro. El token canónico ahora es `#8DD5A8`, contraste **5,9406:1**, sin cambiar el claro. Se actualizaron fuente JSON, bóveda CSS y maqueta heredada; Dart/CSS generados se reconstruyen desde JSON.

## Salidas locales

```text
# apps/movil · Flutter 3.44.8 · Windows
flutter test --no-pub test/widget/apertura_respaldo_test.dart test/goldens/apertura_respaldo_golden_test.dart --reporter expanded
00:01 +10: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget [goldens seleccionados] --reporter compact
00:36 +511: All tests passed!

flutter analyze --no-pub
No issues found!
flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
python -X utf8 scripts/verificar_frontend.py movil
TODO OK

# packages/diseno_flutter
flutter test --no-pub test/a11y test/unidad test/widget --reporter compact
00:08 +51: All tests passed!
flutter analyze --no-pub
No issues found!

# raíz frontend
corepack yarn workspace @aportaya/tokens test:front
Test Files 3 passed (3); Tests 16 passed (16)
corepack yarn workspace @aportaya/ui test:a11y
Test Files 1 passed (1); Tests 3 passed (3)
corepack yarn workspace @aportaya/web build
Application bundle generation complete; Prerendered 12 static routes.
corepack yarn workspace @aportaya/backoffice build
Application bundle generation complete.
```

El primer pase de Flutter con el nuevo token tuvo **9 fallos de golden oscuro**; eran diferencias de color en texto que consume `brandTexto`. Se abrieron las nueve imágenes nuevas y los nueve diffs aislados: no mostraron cambios de disposición, recorte ni contenido. Solo después se actualizaron esas nueve referencias y la suite completa volvió a pasar. El build de backoffice conserva una advertencia de presupuesto inicial excedido en 889 bytes; terminó con exit 0.

## Evidencia visual inspeccionada

Todas las capturas siguientes son Windows con datos sintéticos. `OK` se limita a la celda descrita, no a la pantalla completa en dispositivos reales.

| Celda | Captura en `7ffc6aa` | Inspección |
|---|---|---|
| 360×760, primer cuadro reducido, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/apertura_reducida_360_light.png) | OK: portada completa y ambas acciones visibles, sin velo ni recorte. |
| 360×760, primer cuadro reducido, oscuro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/apertura_reducida_360_dark.png) | OK: misma jerarquía, pastillas y acción secundaria legibles, sin velo. |
| Tour 320/texto 200 %, oscuro: inicio, scroll y última lámina | [inicio](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/tour_320_texto_200_dark.png), [scroll](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/tour_320_texto_200_scroll_dark.png), [última](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/tour_320_texto_200_ultima_dark.png) | OK en las tres: texto verde más legible, CTA y navegación conservados; diffs solo en texto verde. |
| Ingreso 320/texto 200 %, oscuro: teclado y recuperación | [teclado](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/ingreso_320_texto_200_teclado_dark.png), [recuperación](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/ingreso_320_texto_200_recuperacion_dark.png) | OK en ambas: cambio solo en enlace verde; el estado con teclado conserva scroll y acción fijada. |
| Saldo offline y turno sin confirmar, 360 oscuro | [saldo](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/saldo_offline_360_oscuro.png), [turno](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/turno_sin_confirmar_360_oscuro.png) | OK en ambas: diferencia limitada a acciones verdes, sin movimiento de layout. |
| Revisión de aporte offline, oscuro: 360/texto 200 % y 768 | [360](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/aporte_offline_revision_accion_360_texto_200_dark.png), [768](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/7ffc6aa/apps/movil/test/goldens/imagenes/aporte_offline_revision_768_dark.png) | OK en ambas: «Cambiar datos» más legible, confirmación deshabilitada preservada; diffs solo en texto verde. |

Inspección de calidad **parcial** del primer cuadro: jerarquía 2, alineación 2, espacio 2, sistema 2, contraste 2 para el par medido, densidad 2, estados 1 (no hay matriz completa), pulido 2 = **15/16**. No se emite aprobación global de portada o de otros componentes.

## Límites y gates restantes

- No hubo dispositivo Android/iOS, TalkBack/VoiceOver, backend TEST ni traza profile. H8.S1.M1 continúa **EN CURSO**, H8.S1.M4 **A MEDIAS**, H8.S1.M2 **TODO**. Las referencias Windows no se deben copiar a macOS sin inspección.
- La maqueta HTML heredada mostró el valor CSS nuevo con `getComputedStyle`, pero el navegador registró `Invalid or unexpected token` y un 404 de favicon; no cuenta como verificación visual web. Las builds de Angular y el test de paridad de tokens sí pasaron.
- Figma sigue sin acceso/paridad aprobada. El [CI de `7ffc6aa`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37760453508) terminó sin ejecutar pasos: GitHub anotó pagos fallidos o límite de gasto. Los jobs Flutter, goldens macOS e iOS fueron saltados; PR #15 sin merge y sin condición de release candidate.
