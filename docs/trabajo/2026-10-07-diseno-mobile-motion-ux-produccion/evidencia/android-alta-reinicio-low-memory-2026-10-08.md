# Intento de reanudacion del alta en Android (2026-10-08)

Entorno: Windows, Flutter 3.44.8, AVD `Pixel_2` API 36 con 768 MB de RAM y ventana oculta. APK debug de la rama frontend `codex/mobile-design-merge-2026-10-07` en `c64e571`.

- `flutter build apk --debug --no-pub`: `Built build\app\outputs\flutter-apk\app-debug.apk`.
- `adb -s emulator-5554 install -r ...app-debug.apk`: `Success`.
- `adb shell am start -n bo.aportaya.aportaya_movil/.MainActivity`: inicio aceptado. En la captura transitoria solo aparecio el splash nativo; luego el proceso salio y el launcher volvio al frente. No se introdujeron datos ni se pudo recorrer el alta.
- `adb shell dumpsys activity exit-info bo.aportaya.aportaya_movil`:

```text
timestamp=2026-10-08 05:14:16.985 pid=8559 process=bo.aportaya.aportaya_movil reason=3 (LOW_MEMORY) importance=100 rss=317MB
timestamp=2026-10-08 05:13:36.464 pid=4316 process=bo.aportaya.aportaya_movil reason=3 (LOW_MEMORY) importance=100 rss=153MB
```

La memoria fisica libre de Windows bajo a menos de 1 GB durante el intento. Se apago el AVD con `adb emu kill` y se descarto la captura temporal del splash. **No es una prueba de reanudacion, ni evidencia de un crash funcional de Flutter.** Repetir desde el Mac con memoria suficiente: ingresar datos sinteticos no sensibles al primer paso del alta, mandar la app a background, forzar cierre, reabrir y comprobar que solo vuelven los campos permitidos; nunca contrasena, OTP ni fotos. Registrar capturas antes/despues y logs de dispositivo.
