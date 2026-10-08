# Verificación local — montos exactos y perfil transaccional

- Frontend: `d912427` (`7da4b87` + `d912427`), rama `codex/mobile-design-merge-2026-10-07`, PR #15.
- SDK: Flutter 3.44.8 en Windows. Datos de pruebas y capturas **sintéticos**.
- Peldaño: **TESTED**. No se ejercitó backend TEST, mayor contable, app-kill real ni dispositivo Android/iOS en este corte.

## Resultado

`montoDeAporteValido` y `montoValido` comprueban forma y positividad sin `double`. El monto mensual estimado del alta ahora es una cadena decimal exacta en estado y borrador cifrado: `125.05` vuelve como `125.05`, no redondeado. El campo opcional se puede vaciar. Un borrador legado que almacenó ese valor como JSON number conserva los demás datos reanudables y deja ese monto vacío para reingreso; no intenta recuperar precisión perdida. No cambió el contrato de registro ni se agregó un destino de datos.

## Comandos y salida literal

Desde `PasanakuFrontend/apps/movil` con Flutter 3.44.8:

```text
flutter test --no-pub test/pasanaku/monto_aporte_test.dart test/unidad/validacion_monto_test.dart test/identidad/borrador_de_alta_test.dart --reporter expanded
00:00 +9: All tests passed!

flutter test --no-pub test/identidad/perfil_transaccional_test.dart --reporter expanded
00:00 +2: All tests passed!

flutter analyze --no-pub --fatal-infos
No issues found! (ran in 2.4s)

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact
00:17 +308: All tests passed!

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

El primer intento de la prueba visual dejó un temporizador de guardado pendiente; se corrigió avanzando el reloj de test, **sin** subir el timeout. El primer `flutter analyze --fatal-infos` señaló un constructor sin `const` en la nueva prueba; se corrigió y la segunda corrida quedó limpia. El APK emitió una advertencia sobre el plugin Patrol/Kotlin para versiones futuras de Flutter; no se cambió esa dependencia.

## Capturas inspeccionadas

| Viewport/tema/estado | Archivo | Inspección |
|---|---|---|
| 360×760, texto 200 %, claro, perfil con dato | [perfil_light.png](./perfil_light.png) | `Bs 125.05` y CTA visibles; ayudas completas tras acortar el copy. Sin desborde horizontal. |
| 360×760, texto 200 %, oscuro, perfil con dato | [perfil_dark.png](./perfil_dark.png) | Monto, ayudas y CTA visibles; contraste visual coherente. Sin desborde horizontal. |

La captura sale de `flutter_test`, con tipografías de marca cargadas y datos sintéticos. Los iconos aparecen como cuadrados por la fuente de iconos del entorno de test; **no** sirve como aprobación de iconografía ni reemplaza una captura de dispositivo. La actividad seleccionada todavía se abrevia como «Empleo en rela…» a 200 %: queda como hallazgo de accesibilidad para H8.S1.M1. No se capturó el menú desplegado, tema en dispositivo, tablet, teclado real ni lector de pantalla. `tester.takeException()` fue `null`; no hubo petición de red en este widget, pero no se hizo auditoría de consola/red de la app real.

## Límites de cierre

H7.S1.M2 y H7.S1.M4 siguen **A MEDIAS**. H8.S1.M1/H8.S1.M4 siguen abiertos. No hay GET autenticado de obligación/monto; la ruta de aporte todavía lee `monto` desde la URL y por eso el flujo no es apto para producción. La regla 91.6 exige asientos, doble ejecución real, cuadre, reversa y redondeo en backend; ninguna de esas cinco evidencias existe en este corte. CI remoto de PR #15 sigue sin ejecutar sus jobs por facturación. No fusionar el frontend como release candidate.

[CI del commit `d912427`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37724303432): el job de formato tiene `steps: []` y la anotación de fallo dice literalmente: `The job was not started because recent account payments have failed or your spending limit needs to be increased.` Flutter y macOS/iOS quedaron `skipped`; no es un fallo atribuido al código de esta iteración.
