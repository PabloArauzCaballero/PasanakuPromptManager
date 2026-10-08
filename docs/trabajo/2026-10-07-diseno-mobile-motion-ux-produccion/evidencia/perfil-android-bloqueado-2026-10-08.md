# Perfil Android: intento bloqueado antes de ejecutar la app

H8.S1.M2 permanece **TODO**. No hay medición de frames, memoria ni trace válido. Este registro es evidencia de un impedimento local, no evidencia de rendimiento.

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

Desde el Mac, repetir en un dispositivo Android de referencia o runner autorizado con Flutter 3.44.8 y gateway TEST; registrar modelo/OS/RAM, ruta y commit, ejecutar `flutter run --profile`, recorrer activación → portada → aporte sin datos reales, exportar timeline de DevTools y memoria, y calcular `build`/`raster` p95 y porcentaje de frames lentos contra §7 del plan. La ruta de aporte y el alta están fail-closed por contratos faltantes: no declarar H8.S1.M2 HECHO hasta que esos recorridos sean ejecutables y la evidencia exista. iOS requiere perfilado propio en Mac.
