# Selector de perfil con texto 200 % — prueba local

- Frontend: `dea50ec`, PR #15. Flutter 3.44.8 en Windows; datos y capturas sintéticos.
- El `CampoDeSeleccion` conserva una caja compacta, pero cuando el sistema escala la letra al 150 % o más, el menú permite que cada opción ocupe las líneas necesarias. La opción seleccionada puede seguir abreviada en la caja; al abrir el menú se ve completa. No cambian los códigos del perfil ni el valor persistido.

## Salida literal

```text
dart analyze --fatal-infos                 [packages/diseno_flutter]
No issues found!

flutter test --no-pub test/unidad test/widget test/a11y --reporter compact
00:08 +41: All tests passed!

flutter analyze --no-pub --fatal-infos    [apps/movil]
No issues found! (ran in 15.6s)

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact
00:17 +308: All tests passed!

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk

python -X utf8 scripts/verificar_frontend.py movil
TODO OK
python -X utf8 scripts/verificar_frontend.py diseno
TODO OK
```

La prueba widget abre el selector a 360×760 con texto al 200 % en claro y oscuro y comprueba que la opción «Empleo en relación de dependencia» del menú no declara `TextOverflow.ellipsis`. No se afirmó nada sobre red o backend: esta vista no los consulta. El APK se compiló, **no** se ejecutó en dispositivo en este corte.

## Capturas inspeccionadas

| Estado | Claro | Oscuro | Observación |
|---|---|---|---|
| Perfil con dato | [imagen](./perfil-texto-grande/perfil_light.png) | [imagen](./perfil-texto-grande/perfil_dark.png) | Monto `Bs 125.05`, ayudas y CTA legibles; el valor de actividad se abrevia en la caja. Sin recorte horizontal. |
| Menú de actividad abierto | [imagen](./perfil-texto-grande/perfil_menu_light.png) | [imagen](./perfil-texto-grande/perfil_menu_dark.png) | Varias opciones largas se muestran completas en renglones múltiples; la lista continúa por scroll. Sin banner DEBUG tras la recaptura. |

Los íconos se ven como cuadros por la fuente de iconos del rasterizador de `flutter_test`; no es aprobación de iconografía Android/iOS. Tampoco cubre TalkBack, VoiceOver, teclado real, tablet ni el final de la lista tras scroll. Es evidencia visual **solo** de estas cuatro celdas sintéticas, no de la pantalla completa en producción.

El [CI remoto del mismo commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37725255564) terminó en rojo antes de ejecutar pasos: la anotación dice `The job was not started because recent account payments have failed or your spending limit needs to be increased.` Flutter/macOS/iOS siguen omitidos; no habilita merge del frontend.
