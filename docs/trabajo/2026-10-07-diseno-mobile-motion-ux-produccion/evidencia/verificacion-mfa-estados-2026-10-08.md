# Evidencia local — estados de verificación MFA

- Frontend: `e4623f8`, PR #15; Flutter 3.44.8 sobre Windows, sin datos reales.
- Kill-test antes del cambio: un enlace directo a `/identidad/mfa` mostraba `CampoOTP` aunque `PasoSesion` era `credenciales`. La prueba dirigida falló con `Expected: no matching candidates; Actual: Found 1 widget with type CampoOTP`.
- Corrección: sin desafío se muestra un aviso y CTA a ingreso; con sesión ya abierta, CTA a inicio. Solo con `PasoSesion.mfa` se acepta el factor. El formulario pendiente es desplazable con teclado y texto 200 %, tiene etiqueta visible de seis dígitos, muestra espera y bloquea nuevas entradas durante el POST. No se inventó un canal de entrega del código ni se cambió el contrato MFA del backend.

## Evidencia literal recortada

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:25 +456: All tests passed!

flutter analyze --fatal-infos --no-pub
No issues found! (ran in 4.6s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

El verificador falló una vez al ampliar `textos.dart` a 208 líneas; el copy exclusivo de MFA se separó a `textos_mfa.dart`, y el verificador volvió a pasar. El APK advierte que `patrol` deberá migrar de KGP en una versión futura de Flutter; el build actual pasó.

## Inspección visual

Todas las capturas siguientes se abrieron e inspeccionaron individualmente desde `PasanakuFrontend/apps/movil/test/goldens/imagenes/`. El primer pase de espera solo mostraba una barra tenue; se añadió “Verificando código”, se recapturó y se inspeccionó de nuevo.

| Estado | Viewport/tema | PNG | Inspección |
|---|---|---|---|
| Sin desafío | 320×760, 200 %, claro | `mfa_sin_desafio_320_texto_200_light.png` | OK: alerta y CTA completos |
| Sin desafío | 320×760, 200 %, oscuro | `mfa_sin_desafio_320_texto_200_dark.png` | OK: contraste y CTA visibles |
| Pendiente | 320×760, 200 %, claro | `mfa_pendiente_320_texto_200_light.png` | OK: título, etiqueta y seis celdas visibles |
| Pendiente | 320×760, 200 %, oscuro | `mfa_pendiente_320_texto_200_dark.png` | OK: bordes y etiqueta visibles |
| Sin desafío | 768×1024, claro | `mfa_sin_desafio_768_light.png` | OK: ancho de contenido y CTA limitados |
| Enviando | 320×760, 200 %, claro | `mfa_enviando_320_texto_200_light.png` | OK tras corrección: espera legible |
| Error | 320×760, 200 %, oscuro | `mfa_error_320_texto_200_dark.png` | OK: error completo, sin desborde |

Rúbrica local sobre estas capturas: jerarquía 2, alineación 2, espaciado 2, sistema 2, contraste 2, densidad 1 (tablet vacío por un único aviso), estados 2, pulido 2 = **15/16**. Sin señales anti-slop bloqueantes. La comparación de píxeles corre solo en Windows; las pruebas widget no registran tráfico real ni sustituyen capturas Android/iOS, lector de pantalla o backend TEST. No hubo excepciones de Flutter en las celdas; no se declara consola/red de dispositivo verificada.

El [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37745299748) terminó en failure con **0 pasos ejecutados** por job; el frontend PR #15 permanece `UNSTABLE`. No fusionar saltando esos checks.
