# Evidencia local — declaración PEP sin titular verificable

- Frontend: `f0ccfb0`, PR #15. Flutter 3.44.8 en Windows, datos sintéticos.
- Prueba roja previa: la pantalla pedía la declaración y desbordaba 90 px con 320×760/texto 200 %; no había aviso de indisponibilidad. Después: no hay `Campo`, selector ni “Continuar”; el CTA vuelve a Perfil. La ausencia de POST no prueba que el backend rechace/autorice correctamente: eso queda pendiente.

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:28 +466: All tests passed!

flutter analyze --fatal-infos --no-pub
No issues found! (ran in 5.3s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

## Capturas inspeccionadas

En `PasanakuFrontend/apps/movil/test/goldens/imagenes/`. Se abrieron las tres nuevas y las siete recapturas que cambiaron al alinear el título del componente compartido. `perfil_*` no cambió porque usa otra pantalla. No hay fotos ni datos personales reales.

| Celda | PNG | Resultado de inspección |
|---|---|---|
| PEP, 320×760/200 %, claro | `pep_sin_titular_320_texto_200_light.png` | OK: aviso y CTA completos |
| PEP, 320×760/200 %, oscuro | `pep_sin_titular_320_texto_200_dark.png` | OK: contraste, aviso y CTA completos |
| PEP, 768×1024, claro | `pep_sin_titular_768_light.png` | OK: título, alerta y CTA alineados al ancho máximo |
| Dispositivos, 320×760/200 %, claro/oscuro | `dispositivos_sin_gestion_320_texto_200_{light,dark}.png` | OK ambos: contenido completo, sin corte |
| Contraseña, 320×760/200 %, claro/oscuro | `contrasena_sin_gestion_320_texto_200_{light,dark}.png` | OK ambos: aviso y CTA completos |
| Baja, 320×760/200 %, claro/oscuro | `baja_sin_gestion_320_texto_200_{light,dark}.png` | OK ambos: aviso y CTA completos |
| Baja, 768×1024, oscuro | `baja_sin_gestion_768_dark.png` | OK: título alineado con alerta y CTA |

Rúbrica local del estado PEP: jerarquía 2, alineación 2, espaciado 2, sistema 2, contraste 2, densidad tablet 1, estados 2 y pulido 2 = **15/16**. No hubo excepciones Flutter en las celdas. Son goldens Windows, no consola/red de dispositivo; faltan Android/iOS, TalkBack/VoiceOver y backend TEST. [Decisión contractual](../DECISION-PEP-TITULAR-PENDIENTE.md). El [CI de `f0ccfb0`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37746667724) volvió a fallar con **0 pasos ejecutados** por job; PR #15 no se fusionó.
