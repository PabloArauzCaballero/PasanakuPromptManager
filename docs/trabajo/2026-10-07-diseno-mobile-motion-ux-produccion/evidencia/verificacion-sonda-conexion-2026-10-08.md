# Sonda inicial de conexión: acciones monetarias pausadas

- Código: `PasanakuFrontend` [`491cad4`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/491cad4ba12e7784ff097e9cea026f633e8f502c), PR [#15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Entorno local: Windows, Flutter 3.44.8, datos y red sintéticos. No es una prueba en backend TEST ni dispositivo físico.

## Hallazgo y corrección

Antes, varias pantallas bloqueaban dinero solo si `hayConexionProvider.value == false`; durante la primera sonda (`AsyncLoading`) y ante error del proveedor, `.value` no era `false` y el envío podía estar habilitado. Ahora `permiteOperar` requiere valor `true`, carga terminada y ausencia de error. Saldo, recarga, retiro, transferencia y revisión de aporte muestran estados diferenciados de comprobación, sin conexión y fallo de sonda. El fallo ofrece «Volver a comprobar»; los botones monetarios y sus callbacks vuelven a consultar la red antes del POST, incluso si el callback fue capturado cuando había conexión.

## Pruebas ejecutadas

| Gate | Resultado |
|---|---|
| App: `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget` más cinco archivos de golden seleccionados | 401/401 PASS, incluidos seis casos nuevos de sonda/callback y siete goldens nuevos |
| Diseño: `flutter test --no-pub test/a11y test/unidad test/widget` | 50/50 PASS; el aviso verifica estados, contraste y target de reintento en claro/oscuro a texto 200 % |
| `flutter analyze --fatal-infos --no-pub` en app y diseño | Sin problemas |
| `python -X utf8 scripts/verificar_frontend.py movil` y `... diseno` | Ambos PASS |
| `flutter build apk --debug --no-pub` | APK compilado; advertencia futura del plugin `patrol` sobre KGP, sin fallo actual |

Siete imágenes sintéticas de [`test/goldens/imagenes`](https://github.com/PabloArauzCaballero/PasanakuFrontend/tree/491cad4ba12e7784ff097e9cea026f633e8f502c/apps/movil/test/goldens/imagenes) se abrieron e inspeccionaron a resolución original: recarga pendiente y fallida en 360×760/200 % claro y oscuro (cuatro), revisión de aporte pendiente en 360×760/200 % claro y oscuro (dos), y saldo pendiente en 768×1024 claro (una). El texto, el mensaje de pausa y el reintento se leen sin recorte; el contenido inferior de los formularios se alcanza por scroll, cubierto además por las pruebas widget. No se observó overflow. La composición da una acción de recuperación única en el error, distingue información de advertencia y mantiene el dinero inactivo mientras la red es desconocida.

## Límite de evidencia y siguiente gate

Los goldens nuevos usan raster Windows y se comparan solo allí; no convertirlos en baseline macOS sin abrirlos y aprobarlos visualmente en Mac. Falta probar pérdida/recuperación de red y cierre real con backend TEST en Android/iOS, TalkBack/VoiceOver, y resolver contrato/titularidad de las rutas monetarias. Los checks de [GitHub Actions de este commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37739106464) terminaron sin pasos (`steps: []`) por la restricción de facturación ya registrada; PR #15 sigue `UNSTABLE` y sin merge. No se cambia el conteo formal: **11/41 HECHO**.
