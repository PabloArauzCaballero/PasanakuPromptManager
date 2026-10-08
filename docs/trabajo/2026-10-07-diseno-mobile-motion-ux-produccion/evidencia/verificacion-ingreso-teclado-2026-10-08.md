# Ingreso: secuencia de teclado, texto 200 % y acción visible — 2026-10-08

- Código: `PasanakuFrontend` [`856a414`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/856a414), [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Antes: el campo de celular no declaraba `TextInputAction.next`, contraseña no declaraba `done` ni ejecutaba la acción, y la salida secundaria «Crear mi cuenta» seguía ocupando el pie con teclado abierto a 320 dp/texto 200 %.
- Ahora: «Siguiente» enfoca contraseña; «Listo» usa la misma validación y llamada de «Ingresar», con guarda ante envío duplicado. Al abrir el teclado solo se retira la salida secundaria; vuelve al cerrarlo. La recuperación sigue alcanzable por scroll. No cambian la autenticación, el servidor, el contrato de MFA ni las credenciales guardadas.

## Salidas literales

```text
# Desde apps/movil
flutter test --no-pub test/widget/ingreso_teclado_test.dart test/goldens/ingreso_teclado_golden_test.dart --reporter expanded
00:01 +8: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart test/goldens/tour_texto_grande_golden_test.dart test/goldens/ingreso_teclado_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:27 +499: All tests passed!

flutter analyze --no-pub
No issues found! (ran in 29.1s)

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk

# Desde packages/diseno_flutter
flutter test --no-pub test/widget test/a11y test/unidad --reporter expanded
00:02 +51: All tests passed!
flutter analyze --no-pub
No issues found! (ran in 8.0s)

# Desde la raíz de PasanakuFrontend
python -X utf8 scripts/verificar_frontend.py movil
TODO OK
python -X utf8 scripts/verificar_frontend.py diseno
TODO OK
```

La primera ejecución dirigida fue roja: `TextInputAction.next` era `null` y «Listo» no enviaba. Una captura intermedia mostró que la salida secundaria estrechaba el formulario; una prueba posterior fue roja porque «Crear mi cuenta» seguía visible con teclado. Se corrigieron ambos defectos y se volvieron a correr las pruebas. El test de respuesta 422 usa Dio simulado: prueba un solo POST y la guarda local, **no** autentica contra backend TEST.

## Inspección visual local

Las cuatro imágenes sintéticas de Windows se abrieron a resolución original. El rectángulo inferior de las capturas con teclado representa el `viewInsets` simulado, no un teclado real. Ninguna imagen contiene números de teléfono, contraseña ni datos de producción.

| Celda | Captura | Inspección |
|---|---|---|
| 320×760, texto 200 %, teclado, claro, contraseña enfocada | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/856a414/apps/movil/test/goldens/imagenes/ingreso_320_texto_200_teclado_light.png) | OK: etiqueta y campo legibles; «Ingresar» permanece sobre el inset; alta secundaria oculta. |
| 320×760, texto 200 %, teclado, oscuro, contraseña enfocada | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/856a414/apps/movil/test/goldens/imagenes/ingreso_320_texto_200_teclado_dark.png) | OK: sin fondo claro inesperado ni solapamiento del campo; CTA deshabilitado identificable. |
| 320×760, texto 200 %, teclado, oscuro, recuperación desplazada | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/856a414/apps/movil/test/goldens/imagenes/ingreso_320_texto_200_recuperacion_dark.png) | OK: «¿Olvidaste tu contraseña?» queda visible con scroll; CTA persistente. |
| 768×1024, claro, teclado cerrado | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/856a414/apps/movil/test/goldens/imagenes/ingreso_768_light.png) | OK: campos y salida secundaria presentes, sin desborde; densidad tablet aireada. |

Rúbrica del **slice de teclado**: jerarquía 2, alineación 2, espacio 2, sistema 2, contraste 2, densidad tablet 1, estados teclado abierto/cerrado 2 y pulido 2 = **15/16**, aprobado con nit de densidad tablet. No se observó un bloqueante anti-slop en estas cuatro celdas. La rúbrica no aprueba la pantalla completa: falta capturar aquí error de servidor, lector de pantalla y teclado real.

## Límites y gate

- Peldaño TESTED con inspección visual local, no VERIFIED en dispositivo. `tester.view.viewInsets` no reproduce el teclado del sistema, autocorrección ni VoiceOver/TalkBack.
- Las capturas golden son de Windows; inspeccionar y generar base propia en Mac. Android/iOS y backend TEST siguen pendientes para H7.S1.M2 (A MEDIAS) y H8.S1.M1/M4.
- [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37755208734) no inició jobs: GitHub anota pagos fallidos/límite de gasto. Flutter, goldens macOS e iOS quedaron saltados. PR #15 sin merge.
