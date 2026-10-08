# Verificación: ruta de aporte sin importe verificado

Commit frontend: [`7c12866`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/7c128667f5b49eafc18255ece77342eba1183628) · PR [#15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) · Flutter 3.44.8 en Windows.

## Cambio y alcance

La ruta `/pasanaku/obligaciones/:obligacionId/aportar` antes aceptaba `?monto=125.00` y se lo pasaba a la pantalla capaz de hacer un POST de pago. Ese importe no proviene de un GET autenticado de la obligación; también queda expuesto en historiales y registros de enlaces. Ahora la ruta quita toda la query y solo muestra «No podemos confirmar cuánto te toca aportar» con salida «Ir a ayuda». No se realiza ninguna solicitud HTTP al abrirla ni al ir a Ayuda. La pantalla de formulario sigue en el código para pruebas aisladas, pero no está conectada a esta ruta.

Esto es **contención**, no entrega del flujo financiero. Para habilitarlo hacen falta contrato GET autenticado del importe vigente, autorización de la obligación, cuenta autenticada y los cinco controles de regla 91.6 con backend TEST. H7.S1.M4 permanece A MEDIAS; H8.S1.M6 sigue TODO hasta revisión de Seguridad/Cumplimiento y escaneo de payloads.

## Pruebas locales

| Comprobación | Resultado |
|---|---|
| Ruta sin query y ruta con `?monto=125.00&referencia=secreta` sintéticos | Ambas muestran bloqueo; query eliminada; cero solicitudes; no aparece `PantallaAportar`. |
| «Ir a ayuda» | Navega a `/soporte/ayuda`; cero solicitudes. |
| 360×760, texto 200 %, claro y oscuro | Sin excepción/overflow; etiqueta «Movimientos» dentro de la barra inferior. |
| `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget` | **313/313 PASS**. |
| `flutter test --no-pub test/a11y test/unidad test/widget` en `packages/diseno_flutter` | **41/41 PASS**. |
| `flutter analyze --no-pub` en app y diseño; `python -X utf8 scripts/verificar_frontend.py movil` | Sin problemas; verificador TODO OK. |
| `flutter build apk --debug --no-pub` | APK debug compilado. Advierte de futura migración KGP de `patrol`, no bloquea este build. |

Las capturas sintéticas inspeccionadas son [claro](./aporte-bloqueado-claro-2026-10-08.png) y [oscuro](./aporte-bloqueado-oscuro-2026-10-08.png). Mensaje y CTA son visibles; la barra inferior ya no recorta etiquetas al 200 %. Los iconos cuadrados son un artefacto del rasterizador de widget tests de Windows: estas imágenes **no** sustituyen Android/iOS ni TalkBack/VoiceOver. No se modificaron goldens macOS. La última corrida Windows anterior de goldens fue 10 PASS/3 FAIL; esta iteración no los repitió.

## Gate remoto

Los [jobs CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37726134023) terminaron en FAILURE con lista de pasos vacía; los dependientes Flutter/macOS/iOS quedaron SKIPPED. Es el mismo bloqueo de facturación de GitHub Actions reportado en las corridas anteriores, no evidencia de un test ejecutado y fallido. PR #15 sigue abierto/UNSTABLE: **no forzar merge**. Repetir CI y goldens en Mac cuando se restablezca la cuenta, además de resolver el GET y la validación financiera de extremo a extremo.
