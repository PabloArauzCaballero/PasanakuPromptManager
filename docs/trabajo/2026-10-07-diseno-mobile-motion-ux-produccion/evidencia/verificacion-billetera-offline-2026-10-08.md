# Verificación local — billetera sin conexión (2026-10-08)

Código: [`a3e7a31`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/a3e7a31fb9c9376a6d4db42ff149ae3363ba6415) y [`7766dc9`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/7766dc95cd4c45abf0cb688fa7513d8c5d10179d), PR [#15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). Entorno: Windows, Flutter 3.44.8. Datos de pantalla y red sintéticos; no hay dinero ni usuarios reales.

## Conducta cubierta

| Caso | Evidencia local | Resultado |
| --- | --- | --- |
| El sistema informa sin red | La sonda evita el GET sin interfaz y devuelve falso | PASS |
| Gateway responde 200, 404 o 500 | Los tres son respuesta HTTP: no se etiqueta al teléfono como offline | PASS |
| Error de conexión al gateway | Se muestra estado sin conexión | PASS |
| Gateway se recupera sin cambio de Wi-Fi | Una sonda periódica de 15 s actualiza el estado; prueba con intervalo corto y fuente de eventos inyectada | PASS en unidad |
| Saldo sin red y reconexión | Banner visible; Aportar, Recargar y Retirar inhabilitados; al reconectar se habilitan | PASS |
| Recargar, retirar y transferir | Banner, monto/formulario preservado y envío/reintento deshabilitado sin red; CTA accesible al desplazar a 360×760, texto 200 %, claro/oscuro | PASS en widget |
| Accesibilidad local | Etiquetas, tamaños táctiles, contraste de texto y ausencia de overflow en las variantes ensayadas | PASS en widget |

Se detectó primero un overflow de 359 dp en saldo al añadir el banner fuera del área desplazable; se corrigió colocándolo dentro del `ListView`. La captura final ya no desborda. El banner se usa como componente de catálogo; no se difundió un texto engañoso de «pago fallido» para un resultado monetario incierto.

## Comandos y salidas

Desde `apps/movil`:

```text
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
→ 376/376 PASS (355 no-golden + 21 goldens seleccionados)
flutter analyze --fatal-infos → PASS
dart format --output=none --set-exit-if-changed lib test → 0 archivos cambiados
flutter build apk --debug → PASS
python -X utf8 ../../scripts/verificar_frontend.py movil → PASS
```

Desde `packages/diseno_flutter`: 54/54 pruebas dirigidas, analyzer y formato PASS; `python -X utf8 ../../scripts/verificar_frontend.py diseno` PASS. El `-X utf8` evita un error de decodificación propio de la consola Windows al leer comentarios Unicode; no cambia la validación.

## Capturas inspeccionadas

Las once imágenes son goldens sintéticos del test de widget, no capturas de dispositivo. Se abrieron individualmente después de generar los artefactos finales y se revisaron banner, jerarquía, contraste aparente, recorte y disposición. El test verifica por separado los targets y el contraste de texto.

| Vista | Claro | Oscuro |
| --- | --- | --- |
| Saldo 360×760, texto normal | [claro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/saldo_offline_360_claro.png) | [oscuro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/saldo_offline_360_oscuro.png) |
| Saldo 360×760, texto 200 % | [claro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/saldo_offline_360_texto_200_claro.png) | [oscuro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/saldo_offline_360_texto_200_oscuro.png) |
| Saldo 768, claro | [captura](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/saldo_offline_768_claro.png) | — |
| Recargar 360×760, texto 200 % | [claro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/recargar_offline_360_texto_200_light.png) | [oscuro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/recargar_offline_360_texto_200_dark.png) |
| Retirar 360×760, texto 200 % | [claro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/retirar_offline_360_texto_200_light.png) | [oscuro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/retirar_offline_360_texto_200_dark.png) |
| Transferir 360×760, texto 200 % | [claro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/transferir_offline_360_texto_200_light.png) | [oscuro](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/a3e7a31/apps/movil/test/goldens/imagenes/transferir_offline_360_texto_200_dark.png) |

## Límites y siguiente gate

La recuperación periódica se comprobó con eventos y gateway falsos, **no** con Wi-Fi/dispositivo real. Tampoco se hizo desconexión real en Android/iOS, prueba con teclado o lector de pantalla nativo, app kill/reapertura, backend TEST ni matriz completa de 500/timeout/reintento financiero. Por eso H8.S1.M3 sigue EN CURSO y H8.S1.M4 A MEDIAS; las capturas Windows no aprueban paridad multiplataforma. Las comparaciones de píxeles de estos goldens están condicionadas a Windows: en Mac hay que inspeccionar y generar baseline específica, no copiar la de Windows a ciegas.

El [run CI del corte final](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37735591472) falló con `steps: []`; la anotación del job dice que no arrancó por pagos recientes fallidos o límite de gasto de GitHub Actions. Los jobs dependientes Flutter, goldens macOS e iOS quedaron omitidos. No es una falla detectada en el código ni una validación exitosa de CI. El PR frontend permanece sin fusionar; DoD formal 11/41 HECHO.
