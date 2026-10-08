# Android 320 dp / texto 200 % — portada, tour y alta

Fecha: 2026-10-08. Código: `PasanakuFrontend` `1850696` (PR #15). AVD AtlasDemo, Android 16/API 36, tamaño emulado 1080×2400 px a 540 dpi (320×711 dp), `font_scale=2.0`, APK debug con `API=http://10.0.2.2:4010/api/v1`. No hubo backend TEST ni datos personales. Las imágenes muestran pantallas sin sesión y formulario vacío.

## Defecto y corrección

Antes, [el primer paso del alta](./alta-android-320-200-light-bottom-2026-10-08.png) mantenía «Número de documento» y «Expedido en» en dos columnas: las etiquetas se partían de forma torpe y las ayudas terminaban en puntos suspensivos. Un test nuevo falló con la segunda etiqueta comenzando a la misma altura que la primera (`698.0` frente al límite `818.0`).

En `1850696` ambos campos se apilan si el ancho disponible es menor de 400 dp o la escala de texto es al menos 1,5. La decoración admite cinco líneas de ayuda y seis de error con texto grande; en escala normal conserva sus límites previos. El test verifica posición, longitud de ayudas y selección de «La Paz» en 320 dp/200 %. La pantalla corregida fue abierta e inspeccionada en [claro](./alta-android-320-200-light-corregida-2026-10-08.png) y [oscuro](./alta-android-320-200-dark-corregida-2026-10-08.png): ambas etiquetas, ayudas y selector son legibles, sin solapamiento visible. El valor del departamento sigue guardándose en el estado del alta.

## Recorrido visual adicional

- Portada 320 dp/200 %: [inicio claro](./portada-android-320-200-light-2026-10-08.png), [acciones claras al desplazar](./portada-android-320-200-light-bottom-2026-10-08.png), [inicio oscuro](./portada-android-320-200-dark-2026-10-08.png) y [acciones oscuras al desplazar](./portada-android-320-200-dark-bottom-2026-10-08.png). Contenido y dos acciones alcanzables por scroll, sin recortes visibles.
- Tour a 320 dp/200 % en claro: [primera lámina arriba](./tour-android-320-200-light-2026-10-08.png) y [abajo](./tour-android-320-200-light-bottom-2026-10-08.png), [segunda](./tour-android-2-320-200-light-bottom-2026-10-08.png), [tercera](./tour-android-3-320-200-light-bottom-2026-10-08.png) y [cuarta](./tour-android-4-320-200-light-bottom-2026-10-08.png). Se desplazó el contenido y se pulsó «Siguiente» hasta la última. El CTA permaneció visible; los textos completos se pudieron leer tras desplazar.

## Pruebas y límites

- `flutter test --no-pub test/widget/paso_datos_test.dart` → 6/6 PASS; el nuevo caso estuvo rojo antes de la corrección.
- Seis directorios no-golden de app → **435/435 PASS**; diseño Flutter no visual → **51/51 PASS**; golden dirigido de ingreso/teclado → **4/4 PASS**; analyzers de app/diseño y verificador de arquitectura → PASS; APK debug compiló e instaló.
- `flutter test --no-pub test` completo terminó **525 PASS / 4 FAIL** en cuatro goldens (`aporte revisión oscuro`, `saldo éxito claro/oscuro`, `transición portada→ingreso`). No se actualizaron sus bases sin inspección y reconciliación con el estado actual. Por tanto, el gate de goldens completo no pasa.
- El [CI de `1850696`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37763311961) volvió a rechazar los jobs antes de ejecutarlos por pagos fallidos o límite de gasto de GitHub Actions; Flutter/macOS/iOS quedaron saltados. PR #15 permanece abierto.
- La primera reinstalación del APK corregido falló por espacio del AVD. Se desinstaló **solo** `bo.aportaya.aportaya_movil` con datos sintéticos y se instaló el APK nuevo; las capturas «corregida» son posteriores a esa instalación. Se retiraron tres capturas temporales redundantes del workspace; no se tocó información de usuario.

El emulador usa renderizado por software. Falta inspección equivalente en iOS/dispositivo físico, texto grande con teclado y lector de pantalla, validación con backend TEST y CI remoto. H7.S1.M2 permanece **A MEDIAS**, H8.S1.M4 **A MEDIAS** y el plan **12/43 HECHO**. No es prueba de un release candidate.
