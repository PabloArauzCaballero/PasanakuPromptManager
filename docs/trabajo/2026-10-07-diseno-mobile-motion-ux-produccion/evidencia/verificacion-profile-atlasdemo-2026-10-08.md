# Arranque profile en AtlasDemo — diagnóstico, no gate

Código: `PasanakuFrontend` `1850696`. Fecha: 2026-10-08. Dispositivo: AVD `AtlasDemo`, Android 16/API 36, `sdk_gphone64_x86_64`, 1080×1920/420 dpi, GPU SwiftShader/Impeller OpenGLES. La URL `API=http://10.0.2.2:4010/api/v1` es la configuración local de depuración admitida en emulador; no se levantó backend TEST ni se enviaron datos personales.

Se ejecutó desde `apps/movil`:

```text
flutter run --profile --trace-startup -d emulator-5554 --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1
√ Built build\app\outputs\flutter-apk\app-profile.apk (54.6MB)
Tracing startup on sdk gphone64 x86 64.
Time to first frame: 2125ms.
Saved startup trace info in build\start_up_info.json.
Application finished.
```

El [JSON literal de `start_up_info.json`](./perfil-atlasdemo-inicio-2026-10-08.json) informa `timeToFrameworkInitMicros=1973481`, `timeToFirstFrameMicros=2125160` y `timeToFirstFrameRasterizedMicros=4408608`. Flutter produjo además `build/start_up_timeline.json` local (830 809 bytes): contiene cuatro eventos `Frame` de inicio, no una muestra suficiente para p95. El log Android mostró `Skipped 63 frames!` durante el arranque. Una lectura posterior de `adb shell dumpsys meminfo bo.aportaya.aportaya_movil` dio `TOTAL PSS: 155398 KB`, `TOTAL RSS: 237552 KB`, `TOTAL SWAP PSS: 943 KB`; es una sola muestra, sin pico ni tendencia.

La [captura de la portada tras el arranque profile](./perfil-atlasdemo-portada-2026-10-08.png) fue abierta e inspeccionada: marca, texto, garantías y dos acciones visibles, sin recortes aparentes. La captura solo prueba el estado final en este AVD; no mide la transición ni demuestra consola/red limpias. El renderizado por software y la carga del host invalidan estos tiempos como baseline de gama baja. No hay p95 de frames, memoria durante recorrido, comparación 900/1450 ms, backend TEST, iOS ni dispositivo físico de referencia.

Conclusión: `flutter run --profile --trace-startup` ya es ejecutable en este entorno, por lo que H8.S1.M2 pasa a **EN CURSO**. Su CA/DoD de rendimiento **no** está cumplido; repetir en dispositivo acordado, con recorrido P0 y trazas completas antes de fijar umbrales o aprobar producción.
