# Evidencia local — bienvenida sin sesión

- Frontend: `a6cf052`, PR #15; Flutter 3.44.8 en Windows, sin datos reales.
- La ruta heredada `/identidad/bienvenida` se puede abrir directamente. Antes decía “Bienvenida, nueva cuenta” aun sin alta y enlazaba a Billetera y Perfil sin sesión. La prueba dirigida falló antes del cambio porque encontró ese texto. El alta real ya cierra en `/ingreso?alta=lista` tras el resultado del servidor; esta ruta no sustituye ese aviso.
- Ahora muestra un estado informativo sin confirmar cuenta ni bono, con una sola acción “Ir a ingresar”. No crea sesión, no consulta el backend y no habilita Billetera/Perfil. H7.S1.M2 sigue A MEDIAS: el alta/OTP y la bienvenida final no están validados en Android/iOS ni backend TEST.

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:26 +472: All tests passed!

flutter analyze --fatal-infos --no-pub
No issues found! (ran in 5.7s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

## Capturas inspeccionadas

| Estado | Viewport/tema | PNG en `PasanakuFrontend/apps/movil/test/goldens/imagenes/` | Inspección |
|---|---|---|---|
| Sin sesión | 320×760, texto 200 %, claro | `bienvenida_sin_sesion_320_texto_200_light.png` | OK: texto y CTA completos, sin desborde |
| Sin sesión | 320×760, texto 200 %, oscuro | `bienvenida_sin_sesion_320_texto_200_dark.png` | OK: contraste y CTA completos |
| Sin sesión | 768×1024, claro | `bienvenida_sin_sesion_768_light.png` | OK: título, alerta y CTA alineados al ancho máximo |

Las tres imágenes se abrieron e inspeccionaron. Rúbrica local: jerarquía 2, alineación 2, espaciado 2, sistema 2, contraste 2, densidad tablet 1, estados 2 y pulido 2 = **15/16**. No se vio un bloqueante anti-slop. La prueba de accesibilidad automatizada cubrió objetivos, etiquetas y contraste en ambos temas al 200 %; no hubo excepciones Flutter en las celdas. Las capturas son locales Windows: no equivalen a recorrido Android/iOS, lector de pantalla, red ni consola de dispositivo.

El [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37747519674) falló con **0 pasos ejecutados** en los jobs. PR #15 permanece `UNSTABLE`, sin merge.
