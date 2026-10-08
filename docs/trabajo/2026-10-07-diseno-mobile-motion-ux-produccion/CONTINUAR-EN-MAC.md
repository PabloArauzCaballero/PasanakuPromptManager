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

Usar Flutter **3.44.8**, la version fijada en CI y ya verificada localmente en un SDK aislado de Windows: 297 pruebas no-golden, analisis y APK pasan. Revisar primero `flutter doctor -v` y tener Xcode instalado para el destino iOS.

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

- Cabeza actual de codigo `c2e0309` en PR #15: timeout y 5xx de recarga/retiro/transferencia ahora dicen que el resultado **no está confirmado**, sin afirmar que el dinero falló; 409 pide revisar el estado y deshabilita otro envío. Tests de 503 en retiro/transferencia a 360×640 con texto 200 %, más clasificación de timeout/500/409: **302/302** no-golden, análisis, verificador y APK debug OK. Se inspeccionaron capturas sintéticas de recarga en claro/oscuro, 360 y 600 px; usan Ahem y DEBUG, no sustituyen Android/iOS real. Goldens Windows **10 PASS/3 FAIL** siguen sin cambiar. La [evidencia ampliada](./evidencia/verificacion-idempotencia-billetera-2026-10-07.md) incluye el desajuste contrato/plan sobre el código HTTP del replay. [CI 37720766770](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37720766770) volvió a fallar antes de ejecutar jobs por facturación; PR #15 continúa sin merge.

- Cabeza de codigo `be2feeb` en PR #15: recarga, retiro y transferencia guardan la clave de idempotencia en almacen seguro **antes** del POST, la reutilizan tras reinicio y bloquean datos incompatibles. No se guarda el factor MFA. El boton de reintento ahora realiza el reenvio seguro y desaparece si una operacion pendiente exige consultar soporte. Recarga desplaza el formulario a 360 px y texto 200 %; antes desbordaba 513 px. Flutter **297/297** no-golden, analyzer, verificador y APK debug OK. Las pruebas son simuladas: faltan backend TEST y app-kill real en Android/iOS. [Evidencia](./evidencia/verificacion-idempotencia-billetera-2026-10-07.md). Los tres goldens previos de saldo/transicion siguen sin aprobarse en Windows; repetir en Mac y no actualizar referencias desde Windows. PR #15 sigue abierta porque GitHub Actions no ejecuta sus jobs por facturacion.

- Cabeza de codigo `79470be` en PR #15: el aporte exige revisar monto, medio y referencia antes del POST (`fd73088`); la revision y la edicion previa no envian dinero, el doble toque y reintento siguen usando la misma clave. Retiro/transferencia ahora desplazan el formulario cuando teclado y texto 200 % reducen el viewport (`79470be`); la prueba reprodujo desbordes de 219/209 px antes del arreglo. Flutter **289/289** no-golden, analyzer, verificador y APK debug OK. Los 6 goldens de aporte y 4 nuevos de formularios pasan; la suite global queda **10 PASS/3 FAIL** en Windows (saldo claro/oscuro, transicion). Se inspeccionaron las seis capturas nuevas/actualizadas de revision y formularios en claro/oscuro; son capturas Flutter locales, no Android/iOS real. [Evidencia y matriz](./evidencia/verificacion-revision-aporte-teclado-2026-10-07.md). El monto de aporte sigue viniendo de query sin GET autoritativo de obligacion: **no habilitar pagos en release**.

- En `9377256`: la validacion de la URL de gateway rechaza credenciales, query y fragmento, con tres pruebas nuevas. **274/274** pruebas no-golden, analyzer, verificador y APK debug pasan en ese corte. La revision estatica no encontro `print`, `debugPrint`, `LogInterceptor` ni SDK de analytics en la app movil; no equivale a auditoria formal. El borrador de alta retiene datos personales en Keychain/Keystore hasta 24 h y requiere aprobacion de Seguridad/Cumplimiento. La proteccion de captura iOS sigue no soportada y release iOS se bloquea deliberadamente. [Evidencia](./evidencia/verificacion-privacidad-gateway-2026-10-07.md).

- En `cbca157` se retiro el UUID de cuenta de ejemplo de las cinco rutas de billetera. Sin `cuenta` valida se muestra un estado explicito con salida a Ayuda, sin consulta de red ni operacion. Trece pruebas nuevas cubren rutas ausentes/malformadas, navegacion, cuenta explicita y texto al 200 % en oscuro. [Evidencia](./evidencia/verificacion-cuenta-billetera-2026-10-07.md): **271/271** no-golden, analyzer, verificador y APK debug pasan. Esto es una contencion, **no el flujo financiero completo**: el login no entrega `cuentaId` y no existe GET para resolver la cuenta de la persona autenticada. Backend/Producto deben definir el contrato autorizado antes de habilitar inicio, recarga, retiro, transferencia y extracto. Un UUID en la query no es prueba de titularidad: la API debe autorizarlo. Goldens Windows siguen 4 PASS/3 FAIL y no hay captura de esta pantalla en dispositivo.

- En `d1aa8a5`: aporte idempotente y guarda de monto invalido; saldo cero con acciones legibles; inicio sin afirmar grupos/movimientos no consultados ni un banco custodio no identificado por contrato; ruta de estado sin IDs bloqueada antes de red y con salida a Ayuda. [Verificacion de ese corte](./evidencia/verificacion-estados-honestos-2026-10-07.md): 258/258 no-golden, APK y analyzer OK. [Verificacion del saldo cero](./evidencia/verificacion-saldo-cero-2026-10-07.md) y [del aporte](./evidencia/verificacion-flutter-3448-2026-10-07.md). Goldens Windows 4 PASS/3 FAIL; saldo y transicion incluyen cambios deliberados de copy/layout. Repetir en Mac y capturar saldo cero/normal en dispositivo, claro/oscuro y texto 200 %, antes de decidir nuevas referencias. La pantalla de monto invalido solo tiene prueba widget con fuente Ahem: inspeccionar tipografia y layout reales antes de aprobarla.
- **Bloqueo P0 adicional:** `Aportar` y la pestaña Grupos llegan a `/pasanaku/mi-estado` sin IDs; la guarda nueva evita red mal formada, pero no entrega el estado ni un aporte. Backend/Producto deben definir GET de grupos/participaciones y obligaciones elegibles de la persona autenticada, con autorizacion, antes de activar el acceso real. El extracto actual entrega resumen de un periodo, no lista de movimientos. Cumplimiento debe revisar la copia de custodia, ahora sin banco nombrado.
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
- La corrida 3.47.5 (2 PASS/5 FAIL) es historica; con 3.44.8 en Windows hay **4 PASS/3 FAIL** (saldo claro/oscuro y transicion). En `d1aa8a5`, saldo y transicion incluyen cambios intencionales de copy/layout, ademas de la diferencia previa de raster; no atribuir todo al renderizador. Falta Mac/CI y capturas reales. No se actualizaron snapshots.
- El progreso registrado es 11/41 microtareas HECHO. No es un release candidate.
- El borrador almacena datos personales localmente en Keychain/Keystore por hasta 24 h; requiere aprobacion formal de Seguridad/Cumplimiento antes de habilitarse en produccion.

## Siguiente orden de trabajo

1. Repetir los goldens de saldo y transiciones en Mac; documentar el resultado, sin actualizar snapshots en bloque.
2. Completar H7.S1.M2: interrupcion/retorno del alta y validacion iOS; no persistir credenciales.
3. Cerrar activacion → portada → aporte con TalkBack/VoiceOver y evidencia por dispositivo.
4. Con backend TEST disponible, ejecutar los escenarios de idempotencia, offline, timeout, 500 y app-kill.
5. Resolver las dependencias externas de Figma, baseline de analytics y aprobaciones de Producto/Cumplimiento antes de congelar el sistema o abrir piloto.

El plan detallado, las decisiones pendientes y la evidencia estan en [PLAN.md](./PLAN.md) y [REPORTE.md](./REPORTE.md). El APK debug y el AVD de Windows no se transfieren: se reconstruyen en el Mac con los comandos anteriores.
