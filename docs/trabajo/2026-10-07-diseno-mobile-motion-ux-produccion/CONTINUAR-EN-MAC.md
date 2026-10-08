# Continuar el trabajo de diseno mobile desde Mac

Este handoff separa el codigo de diseno de los cambios locales ajenos al plan y deja el siguiente arranque claro. El codigo fuente vive en `PasanakuFrontend`; el plan, reporte y evidencia viven en `PasanakuPromptManager`. El slice de frontend integrado sobre el `dev` mas reciente esta en `codex/mobile-design-merge-2026-10-07` (PR #15); este handoff/documentacion esta en `main` de PromptManager. La rama original `codex/mobile-design-handoff-2026-10-07` se conserva como evidencia del trabajo previo. Atlas ya esta actualizado en `origin/dev` (`1fd49c6`); no necesita cambios para continuar.

## Obtener las ramas

En cada clon local, usar la rama correspondiente:

```bash
git -C PasanakuFrontend fetch origin
git -C PasanakuFrontend switch --track origin/codex/mobile-design-merge-2026-10-07
git -C PasanakuPromptManager fetch origin
git -C PasanakuPromptManager switch main
```

Si ya existe la rama local de frontend, usar `git -C PasanakuFrontend switch codex/mobile-design-merge-2026-10-07`. La integracion espera CI: GitHub Actions no pudo arrancar por un problema de facturacion del repositorio; revisar y repetir los checks cuando se restablezca. No fusionar manualmente mientras los goldens de Flutter sigan en rojo.

No usar `git pull` sobre una rama con cambios locales sin guardar. El alcance publicado excluye los cambios locales ajenos al plan (capturas web, texto regulatorio, reglas/hooks de Claude y un fixture simulado).

## Preparar Flutter en macOS

Usar Flutter **3.44.8**, la version fijada en CI y ya verificada localmente en un SDK aislado de Windows: 197 pruebas no-golden, analisis y APK pasan. Revisar primero `flutter doctor -v` y tener Xcode instalado para el destino iOS.

Desde la raiz de `PasanakuFrontend` (Node/Yarn se declaran en `package.json`):

```bash
corepack yarn install
yarn workspace @aportaya/tokens build
bash apps/movil/scripts/generar-clientes.sh
cd apps/movil
flutter pub get
flutter analyze --fatal-infos
flutter test test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact
flutter test test/goldens --reporter expanded
flutter devices
flutter run -d <id-del-dispositivo>
```

El script genera serializadores `.g.dart` locales ignorados por Git. No versionarlos. Para iOS, elegir un simulador o dispositivo listado por `flutter devices`; la validacion iOS aun esta pendiente.

## Estado que recibes

- Cabeza de codigo `94b44bf` en PR #15: el aporte persiste clave idempotente y huella de datos antes del POST, reutiliza la clave tras reinicio simulado, bloquea reintento con datos distintos y no permite pagar si el monto falta, es cero o es invalido. [Verificacion Flutter 3.44.8](./evidencia/verificacion-flutter-3448-2026-10-07.md): 197/197 no-golden, APK y analyzer OK; goldens Windows 4 PASS/3 FAIL. Repetir los tres fallidos en Mac sin actualizar snapshots en bloque. La pantalla de monto invalido solo tiene prueba widget con fuente Ahem: inspeccionar tipografia y layout reales en dispositivo antes de aprobarla.
- [Journey P0](./JOURNEY-P0-BORRADOR.md) listo para revisar, pero no aprobado. Bloqueo de producto: el monto de aporte viene de query, sin GET contractual autoritativo de obligacion; entrega/cobro de turno tampoco tiene vista real/GET. No usar este slice como candidato de release.
- La nueva pantalla de monto invalido no tiene captura Android valida: se intento arrancar `Pixel_2` con 1024 MB y sin ventana, pero la memoria libre de Windows cayo de 2,16 GB a 0,74 GB antes de completar el arranque. Se apago el emulador mediante `adb emu kill`. En Mac, capturar e inspeccionar ese estado en claro/oscuro y texto al 200 %; no usar la imagen de widget con fuente Ahem como aprobacion visual.
- H4.S1.M3 (taxonomia de eventos) no esta cerrado: la busqueda en app, paquetes y docs no encontro una fuente ni un destino de analytics movil con dueno aprobado. No instrumentar un sink ficticio ni atribuir los KPI a datos inexistentes; primero definir destino, propiedad y politica de retencion.

- La continuacion local agrega borrador cifrado de alta con expiracion y pruebas, corrige `10.0.2.2` solo para debug, divide pantallas grandes, corrige el DTO de invitacion y hace tolerante a CRLF el parser de contenido web. Ver `evidencia/continuacion-ejecucion-2026-10-07.md`.
- En `8308b9a`, `flutter analyze --fatal-infos`: limpio; suite funcional no-golden: **178/178**. La APK debug con `API=http://10.0.2.2:4010/api/v1` se recompilo despues del ultimo cambio. El supuesto bloqueo anterior en Gradle era una descarga activa de artefactos Flutter.
- Un fallo 500 en la subida de fotos despues de crear la cuenta ahora deja visible el pendiente y la indicacion de contactar a soporte, sin inducir a registrar otra cuenta. Dos capturas Android en claro/oscuro fueron inspeccionadas; la prueba widget del aviso con texto al 200 % pasa. La captura Android al 200 % de esta pantalla sigue pendiente por falta de memoria del AVD.
- El borrador se guarda de inmediato al `inactive`/`paused`; al completar el alta, se espera la cola de escrituras y se elimina para evitar una carrera que lo restaure. Hay pruebas dirigidas para pausa y borrado.
- Pruebas web por workspace: 709 PASS; typecheck individual en siete workspaces pasa. Verificadores Python locales pasan con `python -X utf8`.
- Patrol no consiguio ejecutar pruebas (0 tests) y el emulador mato el proceso por memoria. No contar esto como prueba E2E ni visual.
- Handoff Android: `PasanakuFrontend` compila en debug; el flujo portada → tour → alta se recorrio en un AVD, con teclado abierto. No se introdujeron datos.
- `flutter analyze --fatal-infos`: limpio.
- Prueba dirigida de captura: 3/3 pasa (denegacion/excepcion, alternativa manual documental y selector de fotos en prueba de vida).
- La corrida 3.47.5 (2 PASS/5 FAIL) es historica; con 3.44.8 en Windows hay **4 PASS/3 FAIL** (saldo claro/oscuro y transicion). Los diffs fueron inspeccionados; falta Mac/CI para atribuir la causa. No se actualizaron snapshots.
- El progreso registrado es 11/41 microtareas HECHO. No es un release candidate.
- El borrador almacena datos personales localmente en Keychain/Keystore por hasta 24 h; requiere aprobacion formal de Seguridad/Cumplimiento antes de habilitarse en produccion.

## Siguiente orden de trabajo

1. Repetir los goldens de saldo y transiciones en Mac; documentar el resultado, sin actualizar snapshots en bloque.
2. Completar H7.S1.M2: interrupcion/retorno del alta y validacion iOS; no persistir credenciales.
3. Cerrar activacion → portada → aporte con TalkBack/VoiceOver y evidencia por dispositivo.
4. Con backend TEST disponible, ejecutar los escenarios de idempotencia, offline, timeout, 500 y app-kill.
5. Resolver las dependencias externas de Figma, baseline de analytics y aprobaciones de Producto/Cumplimiento antes de congelar el sistema o abrir piloto.

El plan detallado, las decisiones pendientes y la evidencia estan en [PLAN.md](./PLAN.md) y [REPORTE.md](./REPORTE.md). El APK debug y el AVD de Windows no se transfieren: se reconstruyen en el Mac con los comandos anteriores.
