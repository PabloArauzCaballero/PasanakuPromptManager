# Portada en emulador Android AtlasDemo — 2026-10-08

## Alcance

Se probó el corte `7ffc6aa` de `PasanakuFrontend` en el AVD local `AtlasDemo` (`sdk_gphone64_x86_64`, Android 16/API 36, 1080×1920 px, 420 dpi). Es un emulador sin ventana con renderizado por software; no representa un dispositivo físico ni una medición de rendimiento.

El primer APK debug se compiló sin `API`. La app mostró su bloqueo de configuración antes de hacer peticiones, como está previsto. Se reconstruyó con `--dart-define=API=http://10.0.2.2:4010/api/v1`, host admitido por la configuración **solo en debug/profile** para el emulador. No se levantó backend TEST ni se enviaron datos personales. La comprobación es visual de la portada sin sesión, no E2E del alta ni de pagos.

## Evidencia inspeccionada

- [Portada clara](./portada-android-atlasdemo-2026-10-08.png): marca, título, explicación, tres garantías y las dos acciones visibles; sin recorte ni solapamiento en 1080×1920.
- [Portada oscura](./portada-android-atlasdemo-dark-2026-10-08.png): mismo contenido y geometría; texto de las garantías legible con el token `brandTexto` corregido en `7ffc6aa`.

Comandos representativos: `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1`, `adb install -r`, `adb shell monkey -p bo.aportaya.aportaya_movil 1`, `adb shell cmd uimode night yes` y `adb shell screencap -p`. El build, la instalación y el inicio terminaron correctamente. Las dos capturas fueron abiertas e inspeccionadas individualmente.

## Límite del gate

Estas capturas añaden evidencia Android para una sola pantalla y una sola densidad. No verifican 320 dp, texto al 200 %, teclado, lector de pantalla, iOS, gestos, latencia, frames, backend TEST ni Figma. H8.S1.M4 permanece **A MEDIAS**, H8.S1.M2 **TODO** y el total del plan **12/43 HECHO**. No fusionar PR #15 mientras falten los checks remotos y el resto del DoD.
