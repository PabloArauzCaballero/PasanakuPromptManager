# Sonda inicial de conexión: acciones monetarias pausadas

- Código: `PasanakuFrontend` [`491cad4`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/491cad4ba12e7784ff097e9cea026f633e8f502c) (UI) y [`7b90b02`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/7b90b0228228562d1d8edb37765acea78470dd43) (límite del comando), PR [#15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Entorno local: Windows, Flutter 3.44.8, datos y red sintéticos. No es una prueba en backend TEST ni dispositivo físico.

## Hallazgo y corrección

Antes, varias pantallas bloqueaban dinero solo si `hayConexionProvider.value == false`; durante la primera sonda (`AsyncLoading`) y ante error del proveedor, `.value` no era `false` y el envío podía estar habilitado. Ahora `permiteOperar` requiere valor `true`, carga terminada y ausencia de error. Saldo, recarga, retiro, transferencia y revisión de aporte muestran estados diferenciados de comprobación, sin conexión y fallo de sonda. El fallo ofrece «Volver a comprobar»; los botones monetarios y sus callbacks vuelven a consultar la red antes del POST, incluso si el callback fue capturado cuando había conexión.

El test de comandos reveló un hueco adicional: llamar directamente a los notifiers de recarga, retiro, transferencia o aporte durante la primera sonda sí producía un POST. `7b90b02` exige conexión confirmada en el caso de uso al iniciar y otra vez justo después de persistir la clave idempotente, antes del POST. Si la red cae entre ambos puntos, informa que **no se envió** la operación; no lo confunde con un resultado remoto incierto. La clave queda conservada y el reintento al recuperar red la reutiliza.

## Pruebas ejecutadas

| Gate | Resultado |
|---|---|
| App: `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget` más cinco archivos de golden seleccionados | 401/401 PASS, incluidos seis casos nuevos de sonda/callback y siete goldens nuevos |
| Diseño: `flutter test --no-pub test/a11y test/unidad test/widget` | 50/50 PASS; el aviso verifica estados, contraste y target de reintento en claro/oscuro a texto 200 % |
| `flutter analyze --fatal-infos --no-pub` en app y diseño | Sin problemas |
| `python -X utf8 scripts/verificar_frontend.py movil` y `... diseno` | Ambos PASS |
| `flutter build apk --debug --no-pub` | APK compilado; advertencia futura del plugin `patrol` sobre KGP, sin fallo actual |

Tras `7b90b02`, la suite de app subió a **410/410 PASS** (nueve casos nuevos del comando: prueba de sonda, cuatro bloqueos iniciales y cuatro caídas entre persistencia y POST). En cada caída se verificó cero POST; tras recuperar red, exactamente un POST con la clave ya persistida. Analyzer, formato, verificador y APK debug volvieron a pasar. Los casos de 503, reinicio, MFA excluido de almacenamiento e importe inválido siguieron pasando.

Siete imágenes sintéticas de [`test/goldens/imagenes`](https://github.com/PabloArauzCaballero/PasanakuFrontend/tree/491cad4ba12e7784ff097e9cea026f633e8f502c/apps/movil/test/goldens/imagenes) se abrieron e inspeccionaron a resolución original: recarga pendiente y fallida en 360×760/200 % claro y oscuro (cuatro), revisión de aporte pendiente en 360×760/200 % claro y oscuro (dos), y saldo pendiente en 768×1024 claro (una). El texto, el mensaje de pausa y el reintento se leen sin recorte; el contenido inferior de los formularios se alcanza por scroll, cubierto además por las pruebas widget. No se observó overflow. La composición da una acción de recuperación única en el error, distingue información de advertencia y mantiene el dinero inactivo mientras la red es desconocida.

## Límite de evidencia y siguiente gate

Los goldens nuevos usan raster Windows y se comparan solo allí; no convertirlos en baseline macOS sin abrirlos y aprobarlos visualmente en Mac. Falta probar pérdida/recuperación de red y cierre real con backend TEST en Android/iOS, TalkBack/VoiceOver, y resolver contrato/titularidad de las rutas monetarias. Los checks de [GitHub Actions de `7b90b02`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37741702555) terminaron sin pasos (`steps: []`) por la restricción de facturación ya registrada; PR #15 sigue `UNSTABLE` y sin merge. No se cambia el conteo formal: **11/41 HECHO**.
