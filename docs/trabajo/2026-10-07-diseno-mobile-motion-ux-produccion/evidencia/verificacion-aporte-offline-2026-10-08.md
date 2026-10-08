# Verificación local — aporte sin conexión y revisión adaptable (2026-10-08)

Código: [`9b7577f`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/9b7577f4c2e13eab36188dd1e58941d189c4d04e), PR [#15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). Windows, Flutter 3.44.8. Datos de obligación/referencia y red sintéticos; no se ejecutó un pago real.

## Resultado funcional

- En formulario y revisión, la pérdida de red muestra «Sin conexión» con una consecuencia explícita; el monto y la referencia permanecen. Revisar puede seguir siendo una acción local, pero **confirmar** y reintentar el POST se deshabilitan. `_enviar` comprueba de nuevo el estado: un callback obtenido antes de perder la red tampoco envía.
- Cuatro pruebas widget recorren 320/360×760, texto 200 %, claro/oscuro. Comprueban cero POST offline, datos conservados, recuperación y un solo POST al confirmar online; pasan guías de objetivos táctiles, etiquetas y contraste y no hay excepciones de layout.
- El formulario se extrajo a `FormularioAporte`, para mantener el archivo de pantalla bajo el gate de 200 líneas. La revisión usa columna centrada de ancho máximo 560 dp en tablet y mantiene el alto disponible para que el CTA normal no quede fuera de pantalla.

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
→ 388/388 PASS (359 no-golden + 29 goldens seleccionados)
flutter analyze --fatal-infos --no-pub → No issues found
dart format --output=none --set-exit-if-changed lib test → 0 changed
flutter build apk --debug --no-pub → PASS
python -X utf8 scripts/verificar_frontend.py movil → TODO OK
```

El primer ensayo de suite detectó dos fallos de test: el plugin nativo de conectividad no existe en `flutter test`. `conApp` ahora inyecta por defecto una conexión simulada online, y los casos offline inyectan la suya; la red HTTP sigue simulada independientemente. Se volvió a correr toda la suite y pasó 388/388.

## Matriz de ocho capturas finales inspeccionadas

Las imágenes son goldens de widget generados en Windows, no capturas Android/iOS. Cada enlace se abrió tras la recaptura final; el resultado de la inspección se limita a la celda indicada.

| Viewport / estado | Claro | Oscuro | Inspección |
| --- | --- | --- | --- |
| 360×760, texto 200 %, formulario | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_formulario_360_texto_200_light.png) | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_formulario_360_texto_200_dark.png) | OK: aviso legible y monto inicia bajo él; resto alcanzable con scroll. |
| 360×760, texto 200 %, revisión arriba | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_360_texto_200_light.png) | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_360_texto_200_dark.png) | OK: aviso y monto visibles sin desborde, contraste claro/oscuro. |
| 360×760, texto 200 %, revisión desplazada al CTA | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_accion_360_texto_200_light.png) | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_accion_360_texto_200_dark.png) | OK: referencia visible, Confirmar aporte inhabilitado y Cambiar datos accesible. El importe se corta arriba por el desplazamiento, no por overflow. |
| 768×1024, revisión | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_768_light.png) | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/9b7577f/apps/movil/test/goldens/imagenes/aporte_offline_revision_768_dark.png) | OK: título y contenido alineados a columna de 560 dp; CTA al pie, sin estirarse a todo el ancho. |

Defectos encontrados y recapturados: (1) el primer copy ocupaba demasiado alto al 200 % → se acortó en `textos.dart`; (2) en tablet la revisión y el CTA se extendían 736 dp → columna centrada y título alineado; (3) el primer centrado desplazó fuera de pantalla el CTA a escala normal → `LayoutBuilder` fijó altura de contenido al viewport; la prueba a11y normal volvió a pasar. Las ocho capturas finales reflejan las correcciones. No hay consola/red nativa observada: el ensayo de widget comprueba cero POST y ausencia de excepciones Flutter; el CI no ejecutó pasos.

## Gate visual y límites

Rúbrica visual **del estado offline**, no del recorrido P0 completo: jerarquía 2, alineación 2, espaciado 2, sistema 2, contraste 2, densidad 1 (vacío vertical en tablet por CTA al pie), estados 1 (solo offline y regreso online ensayados aquí), pulido 1 = **13/16**. Veredicto de **pantalla completa: NO APROBADA para producción**; la dimensión de estados no tiene todavía matriz real de permiso/error/éxito con backend y no hay prototipo Figma aprobado. No se detectaron señales de UI genérica como colores arbitrarios, emojis-icono o copy hueco en las celdas revisadas.

El monto del enlace sigue sin contrato GET autenticado de obligación y titularidad; la ruta de usuario continúa bloqueada por seguridad. No hubo backend TEST, app kill, pérdida/reconexión real de red en Android/iOS, teclado/lector de pantalla nativos ni goldens macOS. No copiar el baseline de Windows a Mac sin inspección. El [CI de `9b7577f`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37737414250) no empezó jobs (`steps: []`): la anotación de GitHub indica pagos fallidos o límite de gasto de Actions. Por eso H7.S1.M4 sigue A MEDIAS, H8.S1.M3 EN CURSO, H8.S1.M4 A MEDIAS y el DoD total **11/41 HECHO**; el frontend no se fusionó.
