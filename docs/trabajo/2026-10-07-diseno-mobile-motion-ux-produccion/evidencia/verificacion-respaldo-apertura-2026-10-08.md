# Apertura de marca: el respaldo retira el velo sin ticker — 2026-10-08

- Código: `PasanakuFrontend` [`4efabdb`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/4efabdb)–[`ac837f8`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/ac837f8), [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). El segundo commit solo añade la comprobación de navegación posterior; las imágenes son del primero.
- Alcance: H7.S1.M8, continuidad de motion sin bloquear la portada. No cambia curvas, duración normal, apariencia ni contratos de red.

## Hallazgo reproducido

La apertura ya tenía un `Timer` de dos segundos en `_ConApertura`; no faltaba el temporizador. El defecto era su cierre: `_ocultar()` siempre registraba un `addPostFrameCallback`, pero esa API **no solicita un frame**. Con `TickerMode(enabled: false)` y sin otro frame pendiente, vencían los dos segundos y el velo seguía montado. La prueba nueva fue roja antes del cambio:

```text
flutter test --no-pub test/widget/apertura_respaldo_test.dart --reporter expanded
Expected: true
Actual: <false>
el temporizador no puede esperar un cuadro que nadie pidió
```

Ahora, si Flutter está en `SchedulerPhase.idle`, el respaldo llama `setState` y programa el frame necesario. Si el cierre llega mientras se construye un frame, se difiere hasta su final; si llega durante callbacks post-frame, solicita el siguiente. El cierre conserva la guarda `mounted`/idempotente y cancela el temporizador al toque o al desmontar.

## Salidas literales

```text
# Desde apps/movil
flutter test --no-pub test/widget/apertura_respaldo_test.dart test/goldens/apertura_respaldo_golden_test.dart --reporter expanded
00:01 +6: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart test/goldens/tour_texto_grande_golden_test.dart test/goldens/ingreso_teclado_golden_test.dart test/goldens/apertura_respaldo_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:28 +507: All tests passed!

flutter analyze --no-pub
No issues found! (ran in 12.3s)

# Desde la raíz de PasanakuFrontend
python -X utf8 scripts/verificar_frontend.py movil
TODO OK

# Desde apps/movil
flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

Los cuatro tests nuevos prueban vencimiento sin cuadro pendiente, toque para saltar, desmontaje con temporizador cancelado y movimiento reducido en el primer cuadro. El test golden detiene el ticker, vence el respaldo, reanuda frames y comprueba que la portada aparece sin el velo en ambos temas; después pulsa «Crear cuenta» y verifica que se abre el tour. Son pruebas de widget con reloj y red simulados, no una medición de frames en Android/iOS. La suite dirigida de **507/507**, el analyzer y el verificador se repitieron en `ac837f8`; el APK debug se compiló en `4efabdb`, cuyo único cambio posterior fue el test.

## Inspección visual local

Se abrieron las dos capturas Windows a resolución original. Ambas usan datos de portada, sin datos de personas ni operaciones.

| Celda | Captura | Inspección |
|---|---|---|
| 360×760, claro, después del respaldo y reanudación | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/4efabdb/apps/movil/test/goldens/imagenes/apertura_respaldo_360_light.png) | OK: portada completa, texto y CTA visibles, sin velo ni superposición. |
| 360×760, oscuro, después del respaldo y reanudación | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/4efabdb/apps/movil/test/goldens/imagenes/apertura_respaldo_360_dark.png) | OK: portada completa, paleta oscura consistente, sin velo ni recorte. |

Rúbrica visual **parcial del estado de respaldo**: jerarquía 2, alineación 2, espacio 2, sistema 2, contraste 2, densidad 2, estados 1 (solo se capturó salida del respaldo), pulido 2 = **15/16**. No hay veredicto global de portada: faltan matriz completa de tamaños/estados, captura de dispositivo y prueba de lector. No se detectó señal anti-slop nueva; el cambio no modifica estilos.

## Límite de salida

- H7.S1.M8 cumple su CA local con una prueba que reprodujo y corrigió el defecto; H8.S1.M2 y H8.S1.M4 siguen pendientes/parciales. La prueba con `TickerMode` no equivale a un fallo real del renderizador del sistema operativo.
- Las imágenes tienen baseline Windows. En Mac, inspeccionar antes de regenerar goldens; Android/iOS, CI, perfil y backend TEST siguen siendo gates separados.
- [CI del último commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37757197087) terminó sin iniciar jobs: GitHub anota pagos fallidos/límite de gasto; Flutter, goldens macOS e iOS quedaron saltados. PR #15 sin merge.
