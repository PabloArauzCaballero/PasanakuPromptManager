# Reanudación tras `force-stop` Android — 2026-10-08

## Recorrido y aislamiento

En una imagen de datos temporal separada del AVD AtlasDemo (Android 16/API 36),
el gate `scripts/verificar_reinicio_android.dart` ejecutó dos tests Patrol sobre
la app instalada. El primero abrió portada y alta y persistió un nombre
**sintético** en Keystore con el prefijo exclusivo `e2e.reanudacion.`. El script
abrió el APK, comprobó un PID vivo, ejecutó `adb shell am force-stop` sobre
`bo.aportaya.aportaya_movil` y comprobó que el PID desapareció. El segundo test
abrió de nuevo portada y alta, comprobó el aviso de reanudación y el valor del
campo, y borró solo la clave de ensayo. No se leyó ni alteró un borrador normal.

El script rechaza dispositivos que no empiezan por `emulator-` y exige
`ro.boot.qemu=1` antes de actuar. También rechaza argumentos que podrían
reactivar la desinstalación o cambiar el destino de Patrol; solo admite
`--dart-define=CLAVE=VALOR` adicionales.

## Fallo inicial que cambió el comando

La primera corrida sembró el borrador (**Total: 1 / Successful: 1**) pero luego
`am start` devolvió `Error type 3: Activity class ... does not exist`. El CLI
Patrol 3.11.0 desinstala el APK antes y después de cada corrida por defecto;
desinstalar también elimina sus datos. Se verificó en el código de esa versión
que `--no-uninstall` desactiva ambos pasos y se añadió a cada fase. La primera
corrida completa quedó **FAIL**, no se contó como prueba de reanudación.

## Salida final observada

Flutter 3.44.8, JDK 21, Patrol CLI 3.11.0; desde `apps/movil`:

```text
dart scripts/verificar_reinicio_android.dart emulator-5554 --dart-define=API=http://10.0.2.2:4010/api/v1
01 guarda borrador sintético antes de force-stop Android
Total: 1
Successful: 1
Failed: 0
Proceso Android vivo antes de force-stop: sí
Proceso Android vivo después de force-stop: no
02 recupera borrador tras force-stop Android
Total: 1
Successful: 1
Failed: 0
Gate reinicio Android: 2/2 fases PASS.
exit code: 0
```

Después del último cambio del script se repitió el gate completo con la misma
salida final. El control de dispositivo físico rechazó `dispositivo-fisico`
con código **64**, y el argumento `--uninstall` también fue rechazado con **64**.
La suite no visual de app pasó **439/439**, `flutter analyze --no-pub
--fatal-infos` informó `No issues found!`, y el verificador móvil `TODO OK`.

## Límite

Esto sí demuestra cierre y relanzamiento del proceso **Android emulado** con
persistencia del primer dato del alta en Keystore. No demuestra la activación
completa: OTP sigue sin contrato/backend TEST; tampoco cubre KYC, permisos,
aporte, iOS, dispositivo físico, consola/red limpias ni todos los estados de
la pantalla. H7.S1.M2 continúa **A MEDIAS**. El APK queda instalado en el AVD
al usar `--no-uninstall`; la imagen temporal se retira al acabar la sesión.
