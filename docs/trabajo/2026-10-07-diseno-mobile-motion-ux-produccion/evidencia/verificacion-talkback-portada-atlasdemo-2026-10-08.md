# TalkBack de portada en AtlasDemo — 2026-10-08

## Hallazgo y corrección

Con TalkBack habilitado en el AVD Android 16 `AtlasDemo`, `uiautomator dump` mostró dos nodos enfocables consecutivos con `content-desc="AportaYa"`: el isotipo y la palabra del mismo lockup. La portada ahora los agrupa en un único nodo semántico de imagen con esa etiqueta; no cambia su dibujo ni la navegación.

## Evidencia literal

- Antes: `content-desc="AportaYa"` aparecía **2** veces en el árbol Android de la portada.
- Después de reconstruir e instalar el APK profile: aparece **1** vez. Le siguen el título, la explicación, las tres garantías y los botones «Crear mi cuenta» y «Ya tengo cuenta» con etiquetas propias.
- `flutter test --no-pub test/a11y --timeout 60s` → **39 PASS**; `portada_a11y_test.dart` exige una sola etiqueta de marca en claro y oscuro al 200 %.
- `dart analyze lib/pantallas/identidad/pantalla_portada.dart test/a11y/portada_a11y_test.dart` → **No issues found**.
- `flutter build apk --profile --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` → APK construido e instalado. La [captura con el foco de TalkBack en el lockup](./portada-talkback-atlasdemo-2026-10-08.png) fue abierta: el rectángulo de foco abarca isotipo y palabra, con título, garantías y botones completos, sin recortes visibles.

## Alcance y límite

Esta comprobación automatizada inspecciona el árbol accesible y un foco de TalkBack en emulador, no evalúa una lectura auditiva completa, gestos en todos los pasos P0 ni uso por personas. El AVD usa GPU por software; falta dispositivo físico, VoiceOver en iOS y recorrido con backend TEST. H8.S1.M1 permanece **EN CURSO**.
