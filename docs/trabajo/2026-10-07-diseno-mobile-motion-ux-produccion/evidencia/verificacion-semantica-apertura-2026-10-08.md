# Apertura: el lector no ve controles cubiertos — 2026-10-08

- Código: `PasanakuFrontend` [`f1505f6`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/f1505f6), [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Alcance: evidencia parcial de H8.S1.M1. No altera apariencia, rutas, tiempos ni contratos de red.

## Defecto reproducido y corrección

Antes de cambiar código, el test nuevo falló: el árbol de semántica contenía `label: "Crear mi cuenta"` y `label: "Ya tengo cuenta"` bajo la apertura, aunque la portada estaba tapada. La apertura también anunciaba dos veces `AportaYa` porque heredaba la etiqueta semántica del dibujo de marca. Un lector podía enfocar controles no visibles.

Mientras el velo está montado, `_ConApertura` excluye la pantalla inferior del árbol semántico; al retirarlo, los controles vuelven. `AperturaDeMarca` expone una sola etiqueta, una pista para saltar y la acción semántica de toque, sin heredar los nombres internos de la ilustración. La prueba verifica ambos estados del árbol y la etiqueta exacta, además de los cuatro casos anteriores de temporizador, toque, desmontaje y movimiento reducido.

## Verificación local

```text
# apps/movil, Flutter 3.44.8
flutter test --no-pub test/widget/apertura_respaldo_test.dart test/goldens/apertura_respaldo_golden_test.dart --reporter expanded
00:01 +7: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget [goldens seleccionados] --reporter compact
00:35 +508: All tests passed!

flutter analyze --no-pub
No issues found!
flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk

# packages/diseno_flutter
flutter test --no-pub test/a11y test/unidad test/widget --reporter compact
00:06 +51: All tests passed!
flutter analyze --no-pub
No issues found!

# raíz de frontend
python -X utf8 scripts/verificar_frontend.py movil
TODO OK
```

La suite completa de app corrió con el mismo código fuente de `f1505f6`; después solo se ajustó en el test la API para leer el árbol semántico sin un método deprecado. El test dirigido de 7 casos y analyzer se repitieron tras ese ajuste. Los dos goldens Windows de [salida del respaldo](./verificacion-respaldo-apertura-2026-10-08.md) pasaron sin cambiar imágenes; no se generó nueva captura porque el cambio es exclusivamente semántico.

## Límites

La prueba inspecciona el árbol de Flutter con reloj y red simulados; no reemplaza TalkBack/VoiceOver ni prueba de foco en Android/iOS reales. H8.S1.M1 continúa **EN CURSO** y H8.S1.M4 **A MEDIAS**. El [CI del último commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37758366875) rechazó todos los jobs antes del primer paso por pagos fallidos/límite de gasto en GitHub Actions; Flutter, goldens macOS e iOS quedaron saltados. PR #15 sin merge.
