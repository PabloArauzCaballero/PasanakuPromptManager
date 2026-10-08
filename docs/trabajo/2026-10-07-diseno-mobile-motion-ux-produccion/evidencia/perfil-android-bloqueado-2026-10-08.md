# Perfil Android: build x64 y arranque, medición aún no válida

H8.S1.M2 permanece **TODO**. El segundo intento sí arrancó la app en profile, pero el emulador sufrió un ANR del sistema y no produjo una traza de frames válida. Ninguno de los dos intentos demuestra el presupuesto de rendimiento.

## Primer intento: bloqueo del compilador

En Windows se inició el AVD `Pixel_2` (Android 17, x86_64, 2 GiB RAM, 4 núcleos virtuales) en modo headless; `adb shell getprop sys.boot_completed` devolvió `1`. Se intentó:

```text
flutter run --profile --trace-startup --trace-to-file=build\visual\perfil_inicio_pixel2.binpb -d emulator-5554 --dart-define=API=http://10.0.2.2:4010/api/v1 --no-pub
```

El build terminó **antes de instalar/ejecutar**:

```text
Target android_aot_profile_android-x64 failed:
ProcessException: Una directiva de Control de aplicaciones bloqueó este archivo
Command: ...\flutter-sdk-3.44.8\bin\cache\artifacts\engine\android-x64-profile\windows-x64\gen_snapshot.EXE ...
Execution failed for task ':app:compileFlutterBuildProfile'.
BUILD FAILED
```

No se modificaron políticas del sistema ni se intentó eludir ese control. El AVD se cerró con `adb emu kill`; `adb devices` quedó vacío. El APK **debug** sí compila, pero no sirve para demostrar los presupuestos p95 de `build`/`raster` ni frames lentos en profile.

## Reintento del 8 de octubre: profile x64 sin traza útil

- `gen_snapshot.EXE --version` del artefacto x64 funcionó. El build profile universal falló todavía al invocar el artefacto **ARM64** por Control de aplicaciones. Acotar `flutter build apk --profile --target-platform android-x64 --no-pub` compiló `app-profile.apk` (54,0 MB), sin cambiar la política del sistema.
- El AVD `Pixel_2` arrancó headless con `-memory 1024`; `adb` confirmó boot. `flutter run --profile --trace-startup -d emulator-5554 --no-pub` instaló el APK x64, lanzó AportaYa y guardó `build/start_up_info.json`: primer frame Flutter **2459 ms**, primer frame rasterizado **9066 ms**. Son datos de un arranque en emulador bajo presión, **no** p95 ni una medición de los flujos P0.
- La ruta relativa de `--trace-to-file` llegó al dispositivo sin separadores (`buildvisual...`) y el grabador no pudo abrirla. No existe timeline válido para calcular `build`/`raster` p95. En logs hubo `Skipped 177 frames`; Windows cayó a ~0,54 GiB libres y el sistema Android mostró [«System UI isn't responding»](./android-profile-system-ui-anr-2026-10-08.png) sobre la bienvenida. La captura sintética se abrió e inspeccionó: la app estaba visible debajo del diálogo, pero la sesión no era utilizable.
- Se cerró el AVD con `adb emu kill`; `adb devices` volvió a vacío. No se modificaron configuraciones permanentes del emulador ni se atribuyó el ANR a la app sin una prueba en equipo estable.

Desde el Mac, repetir en un dispositivo Android de referencia o runner autorizado con Flutter 3.44.8 y gateway TEST; registrar modelo/OS/RAM, ruta y commit, ejecutar `flutter run --profile`, recorrer activación → portada → aporte sin datos reales, exportar timeline de DevTools y memoria, y calcular `build`/`raster` p95 y porcentaje de frames lentos contra §7 del plan. La ruta de aporte y el alta están fail-closed por contratos faltantes: no declarar H8.S1.M2 HECHO hasta que esos recorridos sean ejecutables y la evidencia exista. iOS requiere perfilado propio en Mac.
