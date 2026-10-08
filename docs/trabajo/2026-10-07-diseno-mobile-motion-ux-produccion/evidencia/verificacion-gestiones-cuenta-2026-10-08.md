# Evidencia local — contención de gestiones de cuenta

- Frontend: `5e2a544`, PR #15. Flutter 3.44.8, Windows. Datos de prueba sintéticos.
- Cobertura: perfil, dispositivos, contraseña y baja; claro/oscuro a 320×760 con texto al 200 %, perfil a 768 claro y baja a 768 oscuro. Diez goldens nuevos abiertos e inspeccionados individualmente. Se detectó y corrigió un título truncado y avisos fuera del primer viewport; se regeneraron y volvieron a inspeccionar las capturas afectadas.
- Rúbrica visual local: jerarquía 2/2, alineación 2/2, espaciado 2/2, sistema 2/2, contraste 2/2, estados 2/2, pulido 2/2, densidad tablet 1/2 = **15/16**. La amplitud de tablet es deliberada para una única alerta; no se observó corte de texto ni CTA inaccesible en las diez capturas. Esto no es una prueba en dispositivo.

## Resultados literales recortados

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter expanded
00:23 +440: All tests passed!

flutter analyze --fatal-infos --no-pub
No issues found! (ran in 5.4s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

Las pruebas nuevas verifican ausencia de entradas/confirmaciones sin servicio, navegación y cierre de sesión real, objetivos táctiles/etiquetas/contraste, además de limpiar secretos tras autenticar. Los goldens son Windows y no sustituyen rasterización de macOS, Android/iOS, lectura de pantalla ni backend TEST. El APK se compiló de nuevo después de la limpieza final de secretos; Gradle avisó que una versión futura de Flutter requerirá migrar el plugin `patrol` a Kotlin integrado.

## Capturas versionadas

En `PasanakuFrontend/apps/movil/test/goldens/imagenes/`: `dispositivos`, `contrasena`, `baja`, `perfil` con sufijos `_sin_gestion_320_texto_200_light.png` y `_dark.png`; adicionalmente `perfil_sin_gestion_768_light.png` y `baja_sin_gestion_768_dark.png`. Inspección visual local: avisos completos, salida visible y sin textos solapados. No contienen datos personales reales.

## Límite de cierre

No hay API para estas gestiones; el contrato legal promete baja desde la app. [Decisión pendiente](../DECISION-GESTIONES-CUENTA-PENDIENTE.md). El [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37743797062) terminó en failure con **0 pasos ejecutados** en sus jobs; el problema de facturación ya estaba documentado en cortes anteriores. PR #15 queda `UNSTABLE`. **No se declara release candidate ni merge de frontend.**
