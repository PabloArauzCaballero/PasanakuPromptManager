# Reporte — Diseño mobile, motion y UX hacia producción

- Fecha: 2026-10-07 · Actualizado: 2026-10-08 · Plan: [PLAN.md](./PLAN.md) · Atlas actualizado: `dev` (`f4bb745`).
- Continuidad publicada: `PasanakuFrontend` en `codex/mobile-design-merge-2026-10-07` (`5fc734e`, PR #15); este reporte y evidencia en `PasanakuPromptManager`.
- Continuación Mac: [CONTINUAR-EN-MAC.md](./CONTINUAR-EN-MAC.md).
- Peldaño de evidencia: TESTED. El APK debug compiló e instaló en emulador Android; se inspeccionó el aviso de fotos pendientes en claro/oscuro con datos sintéticos. No se verificaron persistencia ni red contra backend real.
- Avance del roadmap: 18 / 49 microtareas HECHO (36,7 %), 11 EN CURSO, 4 A MEDIAS y 16 TODO. H7.S1.M11/M12 corrigen la visibilidad de errores sobre el teclado Android; M13 verifica el scroll en los nueve pasos bajo estado de contacto sintético y M14 armoniza Atrás del sistema en Android. No completan el E2E P0. H8.S1.M2 sigue EN CURSO por una traza diagnóstica profile en AtlasDemo, no por cumplir el presupuesto de rendimiento. H4.S1.M1 y H4.S1.M3 tienen borradores contrastados, no aprobación ni instrumentación real. El programa completo aún no es un release candidate.
- Bloqueo contractual P0 concretado: [decisión OTP del alta](./DECISION-OTP-ALTA-PENDIENTE.md). `dev` sigue sin prueba de contacto; existe una rama candidata de OTP de correo previo, no integrada ni aprobada. Producto, Identidad y Seguridad deben resolver secuencia/canal y validar en TEST antes de conectar el cliente.
- Bloqueo contractual del aporte concretado: [GET de obligación pendiente](./DECISION-OBLIGACION-APORTE-PENDIENTE.md). El GET agregado de participante no permite verificar un importe CU-21; faltan respuesta por obligación, titularidad autorizada y backend TEST. La ruta móvil continúa sin pago.
- Rendimiento sin gate válido: el primer [reintento profile sufrió ANR en Pixel_2](./evidencia/perfil-android-bloqueado-2026-10-08.md); [AtlasDemo produjo después una traza de arranque y una muestra de memoria](./evidencia/verificacion-profile-atlasdemo-2026-10-08.md). No hay p95 ni recorrido P0 medible en dispositivo de referencia; H8.S1.M2 sigue EN CURSO.

## Resultado de esta iteración

### Reintento de invitación sin error persistente ni doble consulta (`5fc734e`)

- El test rojo reprodujo que un timeout seguido de éxito dejaba visible el error anterior y que dos toques rápidos enviaban una consulta extra. Ahora el reintento muestra carga, evita consultas concurrentes y al resolver deja solo el estado nuevo. La invitación limita su contenido a 560 dp en tablet; [seis capturas sintéticas recapturadas e inspeccionadas](./evidencia/verificacion-reintento-invitacion-2026-10-08.md) cubren acceso sin sesión y enlace inválido en móvil claro/oscuro y tablet.
- Test dirigido **1/1**, suite no-golden completa, goldens **6/6**, analyzer, verificador y APK debug PASS en Windows. La secuencia error→carga→éxito tiene prueba funcional, no matriz visual propia ni backend TEST. H8.S1.M3 y H8.S1.M4 siguen sin cerrar; avance formal **18/49 HECHO**. Los jobs de [CI](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37791999547) no arrancaron por facturación/límite de gasto; PR #15 sin merge.

### Enlaces de invitación y retorno sin datos externos (`1c85b42`)

- Una prueba roja reprodujo que `%3Fdocumento%3D...` en el path de un enlace externo se convertía en query interna. El traductor ahora exige el código firmado, descarta la query externa y envía enlaces inválidos a una salida segura. La guardia de sesión solo preserva retornos de invitación válidos. El estado inválido indica pedir otro enlace y ofrece **Ir a portada**, no un reintento infinito. [Caso, pruebas, tres capturas sintéticas inspeccionadas y límites](./evidencia/verificacion-enlaces-profundos-privacidad-2026-10-08.md).
- Pruebas dirigidas **18/18**, suite no-golden completa, goldens nuevos **3/3**, analyzer, verificador y APK debug PASS en Windows. El enlace inválido y la salida se probaron además en el AVD AtlasDemo (API 36) con captura inspeccionada. Faltan enlace firmado válido, iOS/dispositivo físico, backend TEST, telemetría y revisión Seguridad/Cumplimiento; H8.S1.M6 sigue **EN CURSO**, el avance formal **18/49 HECHO** y PR #15 sin merge.

### Error de gateway distinto de teléfono offline (`b99d394`)

- `ConnectivityResult.none` sigue siendo offline; timeout/fallo de gateway ahora muestra «No pudimos comprobar la conexión» y pausa dinero sin afirmar que el teléfono perdió red. El `StreamProvider` mantiene la sonda periódica y se recupera sin reiniciar la pantalla. [Pruebas, siete imágenes inspeccionadas y límites](./evidencia/verificacion-sonda-error-vs-offline-2026-10-08.md).
- Sonda **10/10**, suite no-golden completa, goldens dirigidos **7/7**, analyzer, verificador y APK debug PASS en Windows. Android/iOS con backend TEST, matriz de fallos y CI remoto siguen pendientes; H8.S1.M3 continúa **EN CURSO** y el avance formal **18/49 HECHO**.

### Sonda de conexión que no queda pendiente indefinidamente (`ccce1a4`)

- La consulta al sistema y el GET del gateway tienen ahora un plazo total de 3 segundos. Si vence, se cancela HTTP y no sale una petición tardía cuando el plugin finalmente responde. [Defecto rojo→verde, pruebas y límite](./evidencia/verificacion-sonda-timeout-total-2026-10-08.md).
- Prueba dirigida **8/8**, suite no-golden completa, analyzer, verificador móvil y APK debug PASS. No hay prueba Android/iOS ni backend TEST para esta condición; H8.S1.M3 continúa **EN CURSO**. El avance formal permanece **18/49 HECHO** y el PR frontend #15 sigue sin merge por los gates remotos.

### Pruebas aisladas del candidato OTP (sin integración)

- La rama backend candidata `59370bbd` pasó **20/20 pruebas dirigidas**: 1 integración PostgreSQL/Testcontainers, 2 del adaptador Gmail con HTTP simulado y 17 del contrato web. [Comandos, resultados y límites](./evidencia/verificacion-candidato-otp-backend-2026-10-08.md).
- No se pudo validar Flutter en esa rama: además de un nombre de test incorrecto en el primer intento, `clientes/dart/identidad` es un doble temporal sin símbolos OpenAPI; generar tokens no reemplaza el cliente real. No hubo entrega Gmail real, SMS, backend TEST, aprobación contractual ni despliegue. El avance formal sigue **18/49 HECHO** y el PR frontend #15 continúa sin merge.

### Revisión de Atlas y de dependencias actuales

- [Auditoría de dependencias y acciones de desbloqueo](./evidencia/auditoria-dependencias-2026-10-08.md). Atlas avanzó a `f4bb745` con recarga de pestañas al volver; no se copió esa lógica en Pasanaku porque Inicio y las rutas monetarias actuales siguen apuntando a `PantallaCuentaNoDisponible` hasta tener titular/cuenta autenticados. Hacer refetch de un saldo inaccesible no resolvería el camino P0. La revisión de estados de red y las reglas de dinero impiden mostrar fondos pendientes como confirmados.
- `PasanakuBackend` sí tiene una propuesta de OTP de correo previo en la rama `pablo/feature/verificacion-correo-gmail-test` (`2f1101f3`), pero no está en `origin/dev`/`main` ni hay PR de esa rama. Se actualizó la [decisión OTP](./DECISION-OTP-ALTA-PENDIENTE.md) con esa evidencia; no se integró una API no aprobada. Figma sigue sin herramientas ni token en esta sesión, e iOS requiere Mac/Xcode. El avance formal permanece **18/49**.

### Atrás del sistema retrocede dentro del alta (`3bd3611`)

- Antes del cambio, `handlePopRoute()` desde el paso 2 cerraba toda la pantalla de registro. El test rojo→verde ahora recorre 3→2→1→tour y conserva el borrador. En Android real, tecla Atrás y gesto lateral desde el paso 2 regresaron al paso 1; otro Atrás abrió el tour. [Comandos, capturas publicables y límites](./evidencia/verificacion-registro-atras-sistema-2026-10-08.md).
- Pruebas dirigidas **3/3**, app no-golden **445/445**, analyzer, verificador y APK debug PASS. Se inspeccionaron claro/oscuro a 320×760 dp/texto 200 %, y `logcat` dirigido devolvió **0 errores inesperados**. H7.S1.M14 **HECHO** para Android; iOS y su gesto de borde siguen sin probar. La guía de UX móvil llevó a igualar la tecla/gesto del sistema con la flecha visible; la prueba visual impidió publicar capturas que mostraban contenidos del formulario.
- La auditoría del alcance de M13 encontró que el primer test solo cubría 1→2→1. Se amplió a los nueve pasos, ocho avances y ocho retrocesos bajo estado OTP **sintético de widget**, con scroll cero y encabezado visible en cada llegada. [Límite exacto de esa cobertura](./evidencia/verificacion-registro-scroll-2026-10-08.md). No equivale a completar el alta real.
- El [PR de frontend #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) sigue sin merge: los jobs remotos no arrancan por facturación/límite de GitHub Actions. No se saltearon los gates de Flutter, macOS/iOS, seguridad ni backend.

### Alta abre el nuevo paso arriba (`92ce679`)

- Una prueba a 320×760 dp/texto 200 % mostró que avanzar desde «Continuar» heredaba **1287 dp** de scroll y ocultaba el encabezado del paso 2. La clave de scroll por paso corrigió el avance y el retroceso sin perder los datos. [Prueba rojo→verde y tres capturas Android del APK final](./evidencia/verificacion-registro-scroll-2026-10-08.md).
- Código final: prueba dirigida y reanudación **2/2**, app no-golden **443/443**, analyzer, verificador y APK debug PASS. En el AVD temporal se inspeccionó el paso 2 arriba en claro/oscuro, con el primer campo visible pese al aviso de borrador recuperado. `logcat` dirigido: **0 errores inesperados**. H7.S1.M13 **HECHO**; iOS, dispositivos físicos y los nueve pasos con backend TEST siguen sin verificar.
- El frontend se publicó en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15), no se fusionó: los checks obligatorios siguen sin ejecutarse por el límite de facturación de GitHub Actions. El gate de goldens macOS y la decisión OTP también permanecen abiertos.

### Error de contraseña visible sobre teclado (`4dfddcf`)

- Las pruebas nuevas reprodujeron dos fallos: clave corta con campo a **-885 dp** y confirmación distinta a **-640 dp** tras tocar «Continuar». La corrección guía el foco al primer campo inválido y lo desplaza a una posición legible sin perder la contraseña. [Pruebas rojo→verde y cinco capturas Android del APK final](./evidencia/verificacion-contrasena-error-teclado-2026-10-08.md).
- En el código final: pruebas dirigidas **7/7**, app no-golden **442/442**, analyzer, verificador y APK debug PASS. Las capturas de ambos errores en claro/oscuro se abrieron e inspeccionaron con teclado real a 320×760 dp/texto 200 %; las claves sintéticas quedaron enmascaradas y el filtro de `logcat` devolvió **0 errores inesperados**. Las guías de UX móvil y prueba visual llevaron a verificar por separado cada error con teclado real. H7.S1.M12 **HECHO**; el flujo de alta completo, iOS y el gate visual general siguen parciales.
- No hay herramientas de Figma conectadas en esta sesión (la búsqueda del catálogo de herramientas por `figma`/`design_system` devolvió cero), ni archivo objetivo disponible para comparar. Por eso H5.S1.M1/M3/M4 y los prototipos Figma no se marcaron HECHO ni se sustituyeron por una maqueta local. La guía de biblioteca Figma exige descubrimiento del archivo y aprobación explícita de alcance antes de modificarlo.
- El [CI de `4dfddcf`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37779048397) volvió a anotar que los jobs no arrancaron por pagos fallidos o límite de gasto. El PR #15 sigue **UNSTABLE**, con Flutter y macOS/iOS saltados; no se hizo merge del frontend.

### Primer error del alta visible sobre el teclado (`c6b7dfb`)

- A 320×760 dp/texto 200 % con teclado real, «Continuar» validaba pero dejaba el primer error fuera de vista si su campo ya tenía foco. Una prueba widget falló antes del cambio (`Actual: -2539.0`) y pasó después. El formulario ahora desplaza el primer campo inválido y su mensaje a la zona visible sin borrar el valor. [Capturas antes/después, claro/oscuro y límites](./evidencia/verificacion-primer-error-teclado-2026-10-08.md).
- En el código final: prueba dirigida **1/1**, app no-golden **440/440**, `flutter analyze` sin issues y APK debug compilado. Las capturas del APK final se abrieron e inspeccionaron; el teclado Android estaba visible y `logcat` no mostró errores inesperados en el filtro dirigido. La skill `mobile-ux-design` motivó comprobar el error sobre el teclado real y `visual-proof` exigió repetir las capturas tras el último cambio de código. H7.S1.M11 queda **HECHO**; H7.S1.M2 y el gate visual general siguen **A MEDIAS**.
- [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) tiene el commit publicado. Sus checks remotos siguen fallando antes de arrancar por facturación/límite de GitHub Actions; Flutter, goldens e iOS aparecen saltados. No se fusionó el frontend ni se certifica producción.

### Cierre de proceso y reanudación Android (`697bd23`)

- Un gate nuevo corre dos fases Patrol aisladas sobre una imagen temporal del AVD: guarda un dato sintético en Keystore, confirma PID vivo, ejecuta `force-stop` y confirma PID ausente, relanza y comprueba aviso y campo recuperado. La corrida final dio **1/1 + 1/1 PASS; gate 2/2 y exit 0**. [Salida literal, fallo inicial y límites](./evidencia/verificacion-force-stop-android-2026-10-08.md). El gate rechaza teléfonos físicos y argumentos que alterarían la secuencia. La skill de UX móvil exigió verificar la recuperación visible en el formulario, no solo la presencia de bytes en Keystore.
- El primer intento había fallado: Patrol desinstaló el APK entre fases, borrando el estado. Se verificó `--no-uninstall` en el CLI instalado, se corrigió el comando y se repitió completo tras el último cambio. App no-golden **439/439**, analyzer y verificador móvil PASS. H7.S1.M2 permanece **A MEDIAS** por OTP/backend TEST, iOS, permisos/KYC y dispositivo físico; el avance formal sigue **14/45**. El warning de Kotlin Gradle Plugin de Patrol no bloqueó este build, pero requiere seguimiento al actualizar Flutter.
- El [CI de `697bd23`](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) sigue **UNSTABLE**: la anotación del job «Formato, reglas propias y compilacion» dice que no inició por pagos recientes fallidos o límite de gasto de Actions. Flutter, goldens e iOS quedaron saltados. PR #15 sin merge.

### Borrador recuperado con Keystore Android real (`67d3dda`)

- La prueba widget previa ya demostraba que los controladores del formulario se remontan después de la restauración; la sospecha de pérdida de valores por su orden de montaje quedó descartada. La nueva prueba Patrol abre portada y alta, escribe un dato sintético en una clave de ensayo aislada, reconstruye el árbol Flutter y comprueba que Keystore y el campo devuelven el valor. [Comando, salida literal y límites](./evidencia/verificacion-borrador-keystore-android-2026-10-08.md): **1/1 PASS**, app no-golden **439/439**, análisis y verificador PASS.
- No se ejecutó `force-stop` ni relanzamiento del proceso, ni iOS/backend TEST; H7.S1.M2 sigue **A MEDIAS** y el total formal **14/45** no cambia. El frontend continúa en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15), sin merge hasta pasar CI y los gates de producción.

### Patrol Android ejecuta casos reales y rechaza cero tests (`9a0cc77`)

- El CLI antes compilaba y devolvía éxito con **Total: 0**. Se añadió instrumentación nativa JUnit, Android Test Orchestrator, un segundo recorrido público y un wrapper que falla si Patrol termina sin casos. En una imagen temporal separada del AVD, el smoke de portada/tour/registro y el tour completo pasaron **1/1 cada uno** de forma aislada. El intento de suite conjunta se interrumpió por desconexión del AVD y **no** se cuenta como PASS. [Comandos, XML, causas y límites](./evidencia/verificacion-patrol-android-2026-10-08.md).
- En el último corte, app no-golden **439/439**, wrapper **4/4**, analyzer y verificador móvil PASS. H7.S1.M9 y H7.S1.M10 quedan **HECHO**; H7.S1.M2 sigue **A MEDIAS** sin alta/OTP real, backend TEST, app kill, iOS ni dispositivo físico. Se registraron M9/M10 en el plan después de detectar el hueco implementando, desvío de la regla de plan previo. No hubo cambio visual ni evidencia nueva de capturas; el gate visual continúa abierto.
- [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) en `9a0cc77` sigue **UNSTABLE**: Actions falló antes de ejecutar los jobs por facturación/límite de gasto y saltó Flutter, goldens e iOS. No se fusionó el frontend.

### TalkBack de portada en AVD AtlasDemo (`ddd85ff`)

- TalkBack activo expuso dos paradas «AportaYa» para isotipo y palabra en la bienvenida. El lockup ahora tiene una sola etiqueta de imagen. El árbol `uiautomator` pasó de **2** nodos `AportaYa` a **1**; [captura con foco real inspeccionada y límites](./evidencia/verificacion-talkback-portada-atlasdemo-2026-10-08.md).
- APK profile reconstruido e instalado; **39/39** pruebas `test/a11y`, análisis de los dos archivos y verificador móvil PASS. Esto no prueba lectura auditiva completa, todo P0, VoiceOver ni dispositivo físico: H8.S1.M1 sigue **EN CURSO** y el total formal **12/43 HECHO**.

### Profile de arranque en AVD AtlasDemo (`1850696`)

- `flutter run --profile --trace-startup` compiló, instaló y produjo `start_up_info.json`/timeline: 2,125 s hasta el primer frame y 4,409 s hasta rasterizar el primer frame útil; una muestra posterior fue 155 398 KB PSS. Se abrió la [captura del estado final y se documentaron los límites](./evidencia/verificacion-profile-atlasdemo-2026-10-08.md). SwiftShader, un solo arranque y ausencia de backend TEST impiden usarlo como p95 o baseline de gama baja. H8.S1.M2 pasa a **EN CURSO**, no HECHO.
- El golden de saldo «éxito» conserva un layout horizontal antiguo mientras la app actual apila las acciones; los otros fallos visuales detectados son diferencias pequeñas de rasterizado/texto. No se regeneraron referencias sin paridad Mac ni se relajaron aserciones. Los cuatro goldens siguen abiertos y PR #15 sin merge.

### Alta a 320 dp y texto 200 % en Android (`1850696`)

- En el AVD, la portada en dos temas y las cuatro láminas del tour permitieron leer el contenido y alcanzar sus acciones mediante scroll. El recorrido reveló que los campos de documento y expedición del alta conservaban una fila demasiado estrecha y cortaban las ayudas. Un test rojo reprodujo la disposición; se corrigió apilando por ancho/escala y ampliando el límite de líneas solo para texto grande. [Capturas antes/después y recorrido Android](./evidencia/verificacion-android-320-texto-200-2026-10-08.md).
- Formulario **6/6**, app no-golden **435/435**, diseño no visual **51/51**, golden dirigido de ingreso **4/4**, analyzers, verificador y APK debug PASS. La suite completa de app dio **525 PASS / 4 FAIL** por cuatro goldens que no se rebaselinaron sin inspección. La prueba visual sigue limitada a emulador Android y un formulario sin datos; OTP, backend TEST, iOS y CI continúan pendientes. H7.S1.M2 y H8.S1.M4 siguen **A MEDIAS**; total **12/43 HECHO**.
- [CI del nuevo commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37763311961): GitHub Actions rechazó los jobs antes de ejecutarlos por facturación/límite de gasto; Flutter, macOS e iOS quedaron saltados. PR #15 no se fusionó.

### Portada Android en dos temas (AVD AtlasDemo)

- El APK debug de `7ffc6aa` se reconstruyó con la URL de API local admitida para el emulador. El primer arranque, sin `API`, mostró el bloqueo seguro de configuración; no se contó como falla visual. Con la configuración válida, la portada abrió sin sesión y se capturó en [claro y oscuro](./evidencia/verificacion-portada-android-atlasdemo-2026-10-08.md). Ambas imágenes 1080×1920 fueron abiertas e inspeccionadas: marca, título, garantías y acciones están completas, sin recortes visibles.
- Esto amplía la evidencia de H8.S1.M4, pero es un AVD Android 16 con renderizado por software y una sola densidad. No hay iOS, dispositivo físico, texto 200 %, lector de pantalla, backend TEST ni perfilado válido. H8.S1.M4 sigue **A MEDIAS**, H8.S1.M2 **TODO** y el total formal **12/43 HECHO**. PR #15 sigue sin merge por los checks remotos bloqueados.

### Primer cuadro sin velo y contraste oscuro AA (`7ffc6aa`)

- La prueba anterior de «primer cuadro» esperaba un `pump` extra. Al quitarlo, reprodujo que la apertura aún se montaba con `disableAnimations`; se corrigió antes del primer `build` y se probó también el cambio de preferencia durante la animación. Al inspeccionar las capturas apareció otro defecto: garantías de portada con contraste oscuro **3,1168:1**. El token de texto de marca quedó en **5,9406:1** sobre su superficie y se sincronizó con la bóveda CSS y la maqueta. [Pruebas, dos capturas nuevas, nueve diffs inspeccionados y límites](./evidencia/verificacion-primer-cuadro-contraste-2026-10-08.md).
- App **511/511** pruebas dirigidas, diseño Flutter **51/51**, tokens **16/16**, UI web a11y **3/3**, analyzers, verificador, builds web/backoffice y APK debug PASS. Los nueve goldens oscuros cambiaron solo donde se usa `brandTexto`; se inspeccionaron antes de actualizar referencias. H7.S1.M8 queda **HECHO** con DoD local; H8.S1.M1 **EN CURSO**, H8.S1.M4 **A MEDIAS** y total formal **12/43 HECHO**. La maqueta HTML heredada tiene un error de JavaScript y no se cuenta como verificación visual web.
- El [CI de `7ffc6aa`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37760453508) volvió a rechazar jobs antes de ejecutar pasos por facturación de Actions; Flutter/macOS/iOS quedaron saltados. PR #15 sin merge.

### Apertura accesible sin controles cubiertos (`f1505f6`)

- Un test rojo encontró que «Crear mi cuenta» y «Ya tengo cuenta» seguían en el árbol del lector mientras el velo de marca los tapaba; además, la marca se anunciaba dos veces. [Corrección y evidencia](./evidencia/verificacion-semantica-apertura-2026-10-08.md): la pantalla inferior queda excluida de semántica solo durante la apertura, y el velo expone una única etiqueta con acción para saltarlo.
- App **508/508** pruebas dirigidas, diseño no visual **51/51**, analyzers, verificador y APK debug PASS. Los dos goldens de salida del respaldo no cambiaron. H8.S1.M1 sigue **EN CURSO** porque faltan TalkBack/VoiceOver reales, Android/iOS y auditoría final; avance formal **12/43 HECHO**.
- El [CI de `f1505f6`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37758366875) volvió a rechazar los jobs antes del primer paso por facturación de Actions. Flutter, macOS e iOS quedaron saltados; PR #15 sin merge.

### Respaldo de apertura sin depender de otro frame (`4efabdb`–`ac837f8`)

- La apertura ya tenía un temporizador de dos segundos. Un test rojo mostró que, con el ticker detenido y sin otro frame pendiente, su callback esperaba un cuadro que no solicitaba: el velo podía permanecer sobre la portada. El cierre ahora solicita el cuadro cuando el scheduler está inactivo, conserva las guardas de ciclo de vida y cancela el temporizador tras toque/desmontaje. Una prueba posterior pulsa «Crear cuenta» y comprueba la navegación al tour después del respaldo.
- [Evidencia del defecto, corrección y dos capturas claro/oscuro inspeccionadas](./evidencia/verificacion-respaldo-apertura-2026-10-08.md): cuatro tests de widget nuevos y dos goldens PASS; suite de app **507/507**, analyzer, verificador y APK debug PASS. El APK corresponde a `4efabdb`; `ac837f8` solo agregó un test, y en ese HEAD se repitieron suite, analyzer y verificador. H7.S1.M8 **HECHO** localmente; avance formal **12/43 HECHO**. No hubo medición real de frames ni dispositivo Android/iOS.
- El [CI de `ac837f8`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37757197087) volvió a rechazar todos los jobs antes de ejecutar pasos por pagos/límite de GitHub Actions. Los gates Flutter, macOS e iOS no corrieron y PR #15 permanece sin merge.

### Ingreso P0 con teclado navegable y acción visible (`856a414`–`7b4a5cd`)

- Un test reprodujo que el campo de celular no ofrecía «Siguiente» y «Listo» en contraseña no enviaba. Se conectaron las acciones del teclado a foco y envío existentes, con la misma validación del botón y guarda de doble solicitud. A 320 dp/texto 200 % la salida secundaria se oculta solo mientras el teclado está abierto, liberando el pie para la acción primaria; la recuperación queda alcanzable por scroll. El comportamiento del backend no cambia.
- App **501/501** pruebas dirigidas (incluidas dos nuevas de objetivos táctiles, etiquetas y contraste), diseño no visual **51/51**, ambos analyzers, ambos verificadores y APK debug PASS. [Cuatro capturas Windows inspeccionadas, rúbrica del slice 15/16 y límites](./evidencia/verificacion-ingreso-teclado-2026-10-08.md). H7.S1.M2 continúa **A MEDIAS**: no hubo teclado real, Android/iOS, lector de pantalla ni backend TEST. Total formal **11/42 HECHO**.
- [CI del último commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37755671459) volvió a rechazar todos los jobs antes del primer paso por pagos/límite de GitHub Actions; Flutter/macOS/iOS quedaron saltados. PR #15 permanece sin merge.

### Tour legible al 200 % y movimiento reducido completo (`04a6733`–`0cb7015`)

- Un test nuevo reprodujo overflow vertical de **927 px** a 320×760/texto 200 %. Las cuatro láminas ahora se desplazan dentro del área de contenido, el pie permanece visible y el arte se compacta a texto grande sin achicar la tipografía. Bajo `disableAnimations`, «Siguiente» salta inmediatamente; la prueba ampliada descubrió y corrigió un error de `AnimatedSize` al llegar a la última lámina.
- **491/491** pruebas dirigidas de app, **51/51** pruebas no visuales de diseño (incluye 28 widgets), ambos analyzers, verificador y APK debug PASS. [Seis capturas Windows abiertas e inspeccionadas, rúbrica local 15/16 y límites](./evidencia/verificacion-tour-texto-200-motion-2026-10-08.md). Las pruebas cubren cuatro láminas claro/oscuro, scroll, CTA, targets y etiquetas; tres transiciones reducidas llegan al contenido final en un frame y los puntos no animan. H7.S1.M5 vuelve a HECHO; H7.S1.M2 sigue A MEDIAS, H8.S1.M1 EN CURSO y H8.S1.M4 A MEDIAS. Total formal **11/42 HECHO**.
- La suite **completa** de diseño en Windows quedó **60 PASS / 15 FAIL** por comparaciones pixel a pixel de catorce goldens históricos del catálogo y un golden de marca con base macOS. Hay una diferencia de hasta 37,47 % en `Organismos`, por lo que requiere inspección en Mac; no se regeneraron bases para ocultar el fallo. Esto no cambia los 28 widgets dirigidos en verde ni habilita el gate visual de producción.
- [CI del corte](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37752117356) no inició jobs por pagos/límite de Actions; Flutter/macOS/iOS quedaron saltados. PR #15 permanece sin merge. No se atribuye verificación de dispositivo ni aprobación de contenido legal a estas pruebas.

### Acciones personales desde enlaces contenidas (`6f8ecf0`)

- Crear grupo con `organizador` de query, retiro con `participante` de query y permuta con IDs de query ya no ofrecen formularios capaces de enviar operaciones con identidad no comprobada. Las rutas muestran explicación y salida a Ayuda; crear grupo sin query conserva su recorrido. No se afirma vulnerabilidad backend demostrada.
- App **482/482** pruebas dirigidas, analyzer, verificador y APK debug PASS (APK del corte `6f8ecf0`; `9145046` solo añadió comentario y test). [Seis tests de enlace sin peticiones, uno de autogestión y tres capturas Windows inspeccionadas](./evidencia/verificacion-acciones-personales-desde-enlace-2026-10-08.md). El contrato confirma que crear sin `organizador` es autogestión y exige `GRUPO_CREAR`; se corrigió un comentario que lo atribuía a la plataforma. Faltan identidad autenticada y contrato para reactivar las acciones personales, backend TEST, Android/iOS y autorización con dos usuarios. H8.S1.M7 queda A MEDIAS, total formal **11/42 HECHO**.
- El primer pase del verificador detectó `textos.dart` con 201 líneas; se separó el microcopy y el verificador pasó. Este hallazgo se agregó al plan después de detectar el hueco en código: desvío de secuencia respecto de la regla de plan previo, registrado aquí para no ocultarlo. [CI](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37748563391) sigue sin ejecutar pasos y PR #15 sin merge.

### Bienvenida heredada sin afirmar alta ni acceso (`a6cf052`)

- La ruta `/identidad/bienvenida` se podía abrir sin un alta previa y mostraba “nueva cuenta” más enlaces directos a Billetera y Perfil, aunque el flujo real aún no abre sesión. Ahora orienta a ingreso con una sola acción y no confirma cuenta ni bono. El resultado comprobado del alta permanece en `/ingreso?alta=lista`.
- App **472/472** pruebas dirigidas, analyzer, verificador y APK debug PASS. [Tres capturas Windows inspeccionadas, accesibilidad claro/oscuro y límites](./evidencia/verificacion-bienvenida-sin-sesion-2026-10-08.md). [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37747519674) falló antes de ejecutar pasos; PR #15 sigue sin merge. H7.S1.M2 continúa A MEDIAS; formal **11/41 HECHO**.

### Declaración PEP no simulada sin titular (`f0ccfb0`)

- La pantalla de verificación adicional pedía datos PEP y “Continuar” solo cambiaba estado local; a 320 px/texto 200 % desbordaba. Se retiró ese formulario sin efecto y su estado huérfano. La ruta muestra aviso honesto y salida a Perfil. El componente compartido ahora alinea título, aviso y CTA en tablet; diez capturas afectadas fueron recapturadas y abiertas.
- [Decisión de identidad/autorización pendiente](./DECISION-PEP-TITULAR-PENDIENTE.md): Cumplimiento define `POST /cumplimiento/usuarios/{usuarioId}/pep`, pero la sesión móvil no entrega `usuarioId`; no usar teléfono en query ni un ID de enlace para atribuir la declaración. La contención no implementa CU-03.
- App **466/466** pruebas dirigidas, analyzer, verificador y APK debug PASS. [Evidencia visual y límites](./evidencia/verificacion-pep-sin-titular-2026-10-08.md). CI del commit falló antes de ejecutar pasos; PR #15 sin merge. H8.S1.M6 sigue EN CURSO y total formal **11/41 HECHO**.

### Rutas previas a sesión fuera de las pestañas (`7fe0d91`)

- Tres tests rojos probaron que los alias de ingreso, verificación básica y MFA mostraban la barra de Inicio/Grupos/Perfil sin sesión. Sus paths y nombres se conservaron, pero ahora viven fuera del shell. El test de navegación pasa y [una captura de la ruta MFA real se abrió e inspeccionó](./evidencia/verificacion-mfa-estados-2026-10-08.md).
- App **460/460** pruebas dirigidas, analyzer, verificador y APK debug PASS. No equivale a E2E en teléfono ni a autorización del backend; H7.S1.M2 sigue A MEDIAS, DoD formal **11/41**.

### Ruta MFA con estado real y teclado (`e4623f8`)

- Una prueba roja mostró que `/identidad/mfa` pedía un código aun sin desafío. Ahora distingue desafío pendiente, sesión ya abierta y ausencia de desafío: sin el primero no hay casillas ni petición posible. El formulario pendiente es desplazable con teclado/texto 200 %, añade etiqueta visible del código y feedback durante el envío. No presupone SMS ni otro canal que el backend no confirme.
- App **456/456** pruebas dirigidas, analyzer, verificador y APK debug PASS. [Siete capturas Windows abiertas e inspeccionadas, claro/oscuro, error, carga y tablet](./evidencia/verificacion-mfa-estados-2026-10-08.md). Falta recorrerlo en Android/iOS, con lector de pantalla y backend TEST. H7.S1.M2 sigue A MEDIAS y el total formal **11/41 HECHO** no cambia.

### Gestiones de cuenta sin efecto retiradas (`5e2a544`)

- Perfil, dispositivos, contraseña y baja ya no presentan campos, casillas o confirmaciones que solo alteraban memoria o cerraban un diálogo. Hay avisos de indisponibilidad y regreso seguro al perfil; cerrar sesión sigue borrando los tokens. El tutorial dejó de prometer estas operaciones. El estado de autenticación limpia teléfono, contraseña y código MFA al completarse la sesión.
- Flutter **440/440** pruebas dirigidas, analyzer, verificador y APK debug PASS. Diez goldens Windows de estados bloqueados inspeccionados en claro/oscuro, 320×760/200 % y tablet; [evidencia y límites](./evidencia/verificacion-gestiones-cuenta-2026-10-08.md).
- [Brecha de contrato y texto legal](./DECISION-GESTIONES-CUENTA-PENDIENTE.md): el OpenAPI no ofrece estas gestiones y el contrato mostrado aún promete cierre desde la app. Requiere Producto/Legal/Identidad/Seguridad y backend TEST. La contención no satisface el derecho ni completa el vertical slice. **11/41 HECHO** se mantiene; [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37743797062) falló antes de ejecutar pasos y PR #15 sigue `UNSTABLE`, sin merge.

### Guardia en los comandos monetarios (`7b90b02`)

- Una prueba nueva demostró que los cuatro notifiers monetarios podían emitir POST directamente durante la sonda inicial, aun con botones bloqueados. Recarga, retiro, transferencia y aporte ahora exigen red confirmada al iniciar y de nuevo después de persistir la clave, justo antes del POST. Si la red cae durante ese intervalo, informan «no enviamos», conservan la clave y, al recuperar red, un solo POST reutiliza esa clave. No se alteró el tratamiento de un timeout/5xx que sí pudo llegar al servidor.
- App **410/410** pruebas dirigidas, analyzer, formato, verificador y APK debug PASS. [Prueba de las cuatro operaciones, ocho casos de bloqueo/caída y límites](./evidencia/verificacion-sonda-conexion-2026-10-08.md). [CI de `7b90b02`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37741702555) otra vez sin pasos por facturación; frontend PR #15 sin merge y DoD formal **11/41 HECHO**.

### Perfil Android local no concluyente

- El build profile x64 de Flutter 3.44.8 compiló e instaló; la app renderizó el primer frame. El build universal ARM64 aún fue bloqueado por Control de aplicaciones de Windows. La traza solicitada no se abrió por una ruta inválida en el dispositivo y el AVD `Pixel_2` presentó ANR de System UI con ~0,54 GiB libres. [Registro, captura inspeccionada y límites](./evidencia/perfil-android-bloqueado-2026-10-08.md). No usar estos tiempos de arranque como rendimiento P0 ni declarar p95. El emulador quedó cerrado.

### Sonda inicial de conexión: dinero pausado hasta confirmación (`491cad4`)

- Saldo, recarga, retiro, transferencia y aporte requieren una sonda positiva terminada; durante carga o error no muestran «sin conexión» por inferencia y no permiten enviar. El nuevo aviso del catálogo diferencia los tres estados y ofrece reintento de sonda. Los callbacks de envío vuelven a comprobar la red para no reutilizar una autorización visual anterior a la desconexión.
- Flutter 3.44.8: app **401/401** pruebas dirigidas, diseño **50/50**, ambos analyzers y verificadores PASS; APK debug compilado. [Siete capturas sintéticas Windows abiertas e inspeccionadas](./evidencia/verificacion-sonda-conexion-2026-10-08.md), con recarga y aporte al 200 % claro/oscuro más saldo tablet. Faltan dispositivos reales, backend TEST y Mac/iOS.
- El [CI de `491cad4`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37739106464) terminó con jobs fallidos sin pasos (`steps: []`) por la restricción de facturación; PR #15 **sin merge**. H5.S1.M3 y H8.S1.M3 siguen EN CURSO, H7.S1.M4 y H8.S1.M4 A MEDIAS. DoD formal **11/41 HECHO**.

### Aporte sin conexión y revisión adaptable (`9b7577f`)

- Formulario y revisión muestran el estado sin conexión; confirmar y reintentar el POST se pausan, mientras monto y referencia siguen visibles. El callback antiguo también comprueba la red antes de enviar; volver a conectarse rehabilita la confirmación sin duplicar el intento. El contenido se limita a 560 dp y el título se alinea en tablet. La separación en `FormularioAporte` mantiene la pantalla bajo el límite de 200 líneas del repositorio.
- Flutter 3.44.8: app **388/388** pruebas dirigidas (359 no-golden + 29 goldens seleccionados), analyzer, formato, verificador propio y APK debug PASS. Cuatro recorridos widget cubren 320/360×760 al 200 % en claro/oscuro, con cero POST offline, conservación de datos, reconexión y checks de targets, etiquetas y contraste. Ocho capturas Windows de formulario/revisión/acción y tablet fueron abiertas e inspeccionadas; [matriz, rúbrica y límites](./evidencia/verificacion-aporte-offline-2026-10-08.md).
- No se habilitó la ruta real de aporte: sigue sin contrato de obligación verificada ni backend TEST. El [CI de `9b7577f`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37737414250) no ejecutó pasos por facturación de Actions. H7.S1.M4 sigue A MEDIAS, H8.S1.M3 EN CURSO, H8.S1.M4 A MEDIAS; PR #15 sin merge y DoD **11/41 HECHO**.

### Billetera sin conexión: estado visible y envío pausado (`a3e7a31`–`7766dc9`)

- Saldo, recarga, retiro y transferencia muestran un banner persistente al confirmar que el gateway no responde. Los envíos y reintentos monetarios quedan inhabilitados sin borrar lo escrito; al volver la conexión, las acciones se habilitan. Una respuesta HTTP 500 cuenta como gateway alcanzable y conserva su tratamiento de error de servidor, no se confunde con teléfono offline. El adaptador repite la sonda cada 15 s: detecta recuperación del gateway sin que cambie el Wi-Fi. El banner reutilizable quedó en el catálogo Flutter.
- La suite dirigida de la app pasó **376/376** (355 no-golden y 21 goldens seleccionados), el sistema de diseño **54/54**, ambos analizadores, formato, verificador propio y APK debug. Once capturas sintéticas Windows (saldo en cinco combinaciones y tres formularios en claro/oscuro con texto al 200 %) fueron abiertas e inspeccionadas; hubo un overflow a 359 dp y se corrigió antes del corte. [Matriz, capturas y límites](./evidencia/verificacion-billetera-offline-2026-10-08.md).
- No hay aún prueba de desconexión/reconexión en dispositivo físico, backend TEST ni recorrido iOS. El [CI de `7766dc9`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37735591472) tampoco ejecutó pasos por facturación de Actions; PR #15 **sin merge**. H8.S1.M3 permanece EN CURSO y DoD **11/41 HECHO**.

### Rutas personales sin IDs de URL (`0a3191d`)

- «Mi estado» y «Mi puntaje» ya no usan IDs de participante/usuario suministrados por enlaces como identidad. Ambas rutas eliminan la query y no hacen consultas personales; muestran un estado explicativo y salida a Ayuda. Cuatro pruebas de ruta verifican cero peticiones y el CTA a 360×760/200 %, claro/oscuro. Se abrieron e inspeccionaron cinco capturas de puntaje; app **342/342** no-golden + **10/10** goldens nuevos, diseño **54/54**, analizadores y APK debug PASS. [Evidencia y límites](./evidencia/verificacion-rutas-personales-sin-ids-2026-10-08.md).
- La revisión estática encontró un **riesgo de titularidad backend pendiente de reproducir**: el GET de estado de participante recibe un UUID arbitrario, agrega obligaciones sin comprobación de sujeto visible y `obligacion_aporte` no entra en la función genérica de RLS por carecer de `usuario_id`/`cuenta_billetera_id`. No se declara explotabilidad confirmada ni cierre de seguridad: requiere prueba con dos usuarios y rol real de servicio, contrato seguro y aprobación. Frontend PR #15 sigue sin merge; DoD total **11/41**.

### Turno personal sin datos verificados (`20300cc`)

- La ruta de turno ya no toma `total`, `mio` ni `actual` de un enlace para dibujar una posición personal o hacer `int.parse`; descarta la query, muestra solo el paquete publicado y avisa que el turno personal no está verificado. Una semilla revelada ya no produce un veredicto «coincide» por inferencia. El botón lleva al verificador real con el nombre «Verificar el sorteo».
- Pruebas de enlace adulterado en claro/oscuro (200 % en oscuro), navegación al verificador y cinco capturas Windows abiertas e inspeccionadas: [matriz y límites](./evidencia/verificacion-turno-sin-datos-verificados-2026-10-08.md). App **338/338** no-golden + **5/5** goldens dirigidos, diseño **54/54**, ambos analizadores y APK debug PASS. Falta GET autenticado del turno personal, backend TEST, Android/iOS, Figma y aprobación; no es un flujo de turno terminado. [CI](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37733245911) no inició jobs por facturación, PR #15 sin merge y DoD total **11/41**.

### Red caída ≠ respuesta tardía (`046ef76`)

- El interceptor y la UI ya no presentan un timeout como teléfono offline ni afirman que muestran datos anteriores en la primera carga. En pagos, ambos casos siguen siendo resultado incierto, con idempotencia intacta. Matriz local de billetera en 360×760/200 %, claro/oscuro, con cuatro capturas inspeccionadas; **329/329** pruebas no-golden, analyzer, verificador y APK debug PASS. [Evidencia y límites](./evidencia/verificacion-estados-red-timeout-2026-10-08.md). H8.S1.M3 sigue EN CURSO por backend TEST/dispositivo; CI remoto sin pasos por facturación y PR frontend sin merge. DoD total **11/41**.

### Alta sin OTP contractual: contención segura (`c541551`)

- El cliente ya no dice que envió un código ni acepta seis dígitos locales como verificación. Muestra un aviso persistente y salida «Volver»; el notifier bloquea avance y POST sin contacto verificado. La única simulación de verificación vive en fixtures de test para conservar las pruebas del serializador y fotos. App **323/323** no-golden, analyzer, verificador y APK debug PASS. Se recapturó e inspeccionó el componente a 360×760/200 %, claro/oscuro. [Evidencia y límites](./evidencia/verificacion-otp-bloqueado-2026-10-08.md).
- Es contención, **no** un alta completa: falta contrato y backend TEST de emisión/validación OTP. H7.S1.M2 continúa A MEDIAS y el frontend PR #15 no se fusiona. El CI remoto del commit no arrancó por facturación; DoD total **11/41**.

### Accesibilidad automatizada P0 (`da439f9`–`ee91cb8`)

- Alta recuperada y aporte bloqueado tienen pruebas de objetivos táctiles, etiquetas semánticas y contraste a 360×760/200 %, claro/oscuro. La portada añade objetivos táctiles y etiquetas, más contraste calculado de título/cuerpo; la guía visual de píxeles confunde los dos colores del logotipo, exento como imagen de marca. App **321/321** no-golden y analyzer PASS. [Matriz y límites](./evidencia/verificacion-a11y-local-2026-10-08.md). No sustituye TalkBack/VoiceOver ni el recorrido en dispositivo; H8.S1.M1 sigue EN CURSO. El PR frontend permanece abierto mientras CI y gates de producción no se resuelvan.

### Privacidad del error de ruta (`637160d`)

- El error de ruta desconocida construía un `StateError` con la URI completa. Aunque `EstadoError` hoy muestra un mensaje genérico, un monitor futuro podría exportar ese objeto con una query sensible. Se quitó la URI; una prueba con documento e importe **sintéticos** comprueba que no aparecen en el error. App **315/315** pruebas no-golden, analyzer y verificador PASS. [Alcance y riesgos del escaneo parcial](./evidencia/verificacion-privacidad-rutas-2026-10-08.md). H8.S1.M6 pasa a EN CURSO, **no HECHO**: faltan revisión Seguridad/Cumplimiento, payloads TEST y protección/capturas iOS. CI remoto sigue sin arrancar por facturación.

### Reanudación del alta al 200 % (`ea54e17`)

- La prueba de cierre/reapertura sintética encontró 100 px de overflow al volver al paso de celular con aviso de recuperación. El encabezado, aviso y paso ahora se desplazan juntos. A 360×760/200 %, el selector SMS/correo usa opciones verticales completas, el aviso y la ayuda de edad se leen sin recorte, y «Continuar» queda al alcance con inset de teclado simulado. El selector desactiva su transición al pedir movimiento reducido. [Siete capturas inspeccionadas y límites](./evidencia/verificacion-alta-reanudada-2026-10-08.md).
- App **314/314** pruebas no-golden, sistema de diseño **43/43**, analyzers, verificador y APK debug PASS. Goldens Windows **10 PASS/3 FAIL**, sin tocar baselines Mac. El CI de `ea54e17` no arrancó jobs por facturación. **Hallazgo P0 nuevo:** la UI dice que envió un OTP, pero el cliente solo confirma seis dígitos localmente y el OpenAPI de identidad no publica emisión/validación pre-registro. Falta decisión contractual y backend TEST; H7.S1.M2 queda A MEDIAS, DoD total **11/41** y PR frontend sin merge.

### Ruta de aporte cerrada hasta verificar el importe (`7c12866`)

- La ruta ya no transforma `?monto=` en un pago: elimina todos los parámetros de la URL, presenta un estado explícito con Ayuda y no hace solicitudes ni POST. Es contención P0, **no** finalización del aporte: falta un GET autenticado que entregue el importe vigente y valide la obligación. La barra inferior gana altura al 200 % para mantener visibles sus etiquetas.
- Cinco pruebas dirigidas cubren enlace sin query, monto/referencia sintéticos por query, navegación a Ayuda y claro/oscuro a 360×760/200 %. Se inspeccionaron dos capturas sintéticas. Flutter 3.44.8: app **313/313** no-golden, sistema de diseño **41/41**, ambos analyzers, verificador propio y APK debug PASS. [Evidencia y límites](./evidencia/verificacion-ruta-aporte-bloqueada-2026-10-08.md). El CI de `7c12866` no inició ningún paso por facturación; macOS/iOS se omitieron. No se tocaron los tres goldens que fallan en Windows. DoD permanece **11/41** y PR #15 no se fusionó.

### Menú de selección legible con texto grande (`dea50ec`)

- El menú del selector de perfil muestra opciones completas en varias líneas cuando el texto escala al 150 % o más, sin agrandar la caja seleccionada ni empujar el CTA fuera del primer viewport. Se capturaron e inspeccionaron formulario y menú abierto en 360×760/200 %, claro y oscuro. La caja todavía abrevia el valor seleccionado; abrir el menú revela la opción completa. **No** se cierra H8.S1.M1 sin TalkBack/VoiceOver y dispositivo. Sistema de diseño: **41/41** pruebas y análisis PASS; app: **308/308**, análisis, verificadores y APK debug PASS. [Matriz, capturas y límites](./evidencia/verificacion-selector-texto-grande-2026-10-07.md). CI remoto vuelve a fallar antes de arrancar por facturación. Conteo DoD: **11/41**.

### Montos exactos en aporte y perfil de alta (`7da4b87`–`d912427`)

- La validación de importe dejó de usar `double`. El perfil transaccional conserva el monto mensual estimado como cadena decimal exacta en memoria y en el borrador cifrado, sin redondear centavos al regresar; permite limpiar el campo opcional. Borradores legados numéricos preservan el resto del progreso pero requieren reingresar el monto. Dos ayudas que se cortaban al 200 % se acortaron sin perder las condiciones «opcional» y «no es un límite».
- Flutter 3.44.8: **308/308** pruebas no-golden, análisis, verificador y APK debug PASS. Dos capturas sintéticas 360×760 al 200 %, claro/oscuro, se abrieron e inspeccionaron. La actividad elegida aún se trunca visualmente a ese tamaño; no hay aprobación visual integral ni prueba en dispositivo. La integración con backend y las cinco evidencias monetarias de regla 91.6 siguen ausentes. [Salida y límites](./evidencia/verificacion-montos-exactos-2026-10-07.md). El conteo DoD permanece **11/41**.

### Contrato candidato de medición P0

- [Taxonomía y fuentes necesarias](./TAXONOMIA-EVENTOS-P0-BORRADOR.md): evento UX anónimo de propiedades cerradas y cálculo de tres KPI solo desde agregados internos autorizados. El esquema de cliente por sí solo no permite calcular los KPI; faltan definiciones, dueños, retención, fuente, destino y revisión de Privacidad/Data.
- [Validador sintético](./validar-eventos-p0.ps1): acepta únicamente el payload propuesto y rechaza identificadores, importes, texto libre y campos adicionales. No se ha ejecutado contra payloads reales de TEST ni se añadió un SDK. H4.S1.M3 queda **EN CURSO**, H4.S1.M4 **TODO**.
- Evidencia literal local: `powershell -NoProfile -ExecutionPolicy Bypass -File docs/trabajo/2026-10-07-diseno-mobile-motion-ux-produccion/validar-eventos-p0.ps1` → `PASS: 8/8 casos sintéticos; no son payloads de TEST`; `git diff --check` → salida vacía. No cubierto: emisor real, payload real, fuente y tablero.

### Aporte con resultado incierto y 409 seguro (`faf75ea`)

- El mismo error de resultado incierto se aplica al cobro de aporte; ya no se afirma que un timeout o 5xx impidió el pago. En 409 o con una clave pendiente y datos diferentes se quita el reintento de la revisión y se indica consultar estado/soporte. Una prueba de 409 a 360×760 y texto 200 % cubre el caso; las pruebas previas de 503, doble toque y revisión siguen pasando. **303/303** no-golden, análisis, verificador y APK debug PASS. Dos capturas sintéticas claro/oscuro fueron inspeccionadas, sin recorte; la fuente Ahem y el banner DEBUG impiden aprobación tipográfica o de dispositivo. [Evidencia](./evidencia/verificacion-idempotencia-billetera-2026-10-07.md). CI vuelve a fallar por facturación; DoD permanece **11/41**.

### Resultado incierto en operaciones de billetera (`c2e0309`)

- Un timeout o 5xx ya no se presenta como una falla confirmada: recarga, retiro y transferencia muestran que el resultado es incierto y permiten reintento manual con la clave persistida. Un 409 pide consultar el estado y bloquea repetir la operación. Dos pruebas widget nuevas ejercitan 503 en retiro/transferencia a 360×640 y texto 200 %; tres pruebas unitarias adicionales cubren timeout, 500 y 409. Flutter 3.44.8: **302/302** no-golden, análisis, verificador y APK debug PASS. Capturas sintéticas de recarga inspeccionadas en 360/600 px y claro/oscuro, con límites Ahem/DEBUG. Goldens Windows **10 PASS/3 FAIL**. [Evidencia](./evidencia/verificacion-idempotencia-billetera-2026-10-07.md). CI sigue bloqueado por facturación; el conteo DoD permanece **11/41**.

### Reintentos monetarios persistidos en `be2feeb`

- Recarga, retiro y transferencia persisten la clave de idempotencia antes de enviar dinero; un reinicio simulado reutiliza la misma clave tras un 503. Datos incompatibles o registro corrupto fallan cerrado. El factor MFA no queda en el registro. El CTA «Volver a intentar» reenvía con la clave original; si los datos pendientes difieren, se oculta junto con el envío y se indica consultar soporte.
- Una prueba a 360×640 y texto 200 % detectó overflow de **513 px** en el error de recarga. La pantalla ahora desplaza contenido y el caso pasa sin excepción. Flutter 3.44.8: **297/297** pruebas no-golden, análisis, verificador y APK debug PASS. Los goldens Windows mantienen **10 PASS/3 FAIL** (saldo claro/oscuro y transición); no se actualizaron snapshots macOS desde Windows. No hay prueba real de app-kill, backend TEST, Android/iOS físico ni aprobación visual de este nuevo estado. [Evidencia](./evidencia/verificacion-idempotencia-billetera-2026-10-07.md). El conteo DoD sigue **11/41**.

### Revisión de aporte y formularios con teclado en `fd73088`–`79470be`

- El aporte ahora tiene secuencia formulario → revisión → confirmación → respuesta. Revisar y cambiar datos no envían el POST; una vez enviado, el copy no afirma que nada llegó durante un timeout. Las pruebas dirigidas conservan el único POST ante doble toque y la misma clave en reintento. El importe positivo sigue proveniendo de query sin GET contractual autoritativo: **no se cierra H6.S1.M3 ni H7.S1.M4**.
- Las pruebas a 360×760 con inset de teclado de 300 dp y texto al 200 % reprodujeron overflow de **219 px en retiro y 209 px en transferencia**. Tras cambiar a scroll con contenido que ocupa el espacio disponible, campo y CTA son alcanzables en claro/oscuro; recarga también pasa esa matriz. Gates de objetivo táctil, etiqueta y contraste pasan en los tres formularios.
- Flutter 3.44.8: **289/289** no-golden, analyzer, verificador y APK debug PASS. Se inspeccionaron seis imágenes locales de revisión, retiro y transferencia en claro/oscuro; 10 goldens PASS y 3 FAIL preexistentes de saldo/transición en Windows. Faltan teclado real, TalkBack/VoiceOver, backend TEST y Mac/iOS. [Evidencia](./evidencia/verificacion-revision-aporte-teclado-2026-10-07.md). El conteo de DoD completos permanece 11/41.

### URL de gateway sin secretos embebidos en `9377256`

- La configuración de arranque ahora rechaza `userInfo`, query o fragmento en la URL base, aun si el host y TLS son válidos. Tres pruebas cubren esos casos; el error expone solo el motivo `url-con-datos`, no el valor. Flutter 3.44.8: **274/274** pruebas no-golden, analyzer, verificador y APK debug PASS. [Evidencia](./evidencia/verificacion-privacidad-gateway-2026-10-07.md).
- La búsqueda estática en `apps/movil/lib` y `packages/diseno_flutter/lib` no halló `print`/`debugPrint`, `LogInterceptor` ni SDK de analytics. Se añadió una prueba de URI en error en `637160d`. Sigue pendiente la revisión formal de Seguridad/Cumplimiento, escaneo de payloads en entorno de prueba, tratamiento del borrador cifrado y capacidad de protección de captura iOS; por eso H8.S1.M6 continúa EN CURSO, no HECHO.

### Cuenta de billetera sin identificador inventado en `cbca157`

- Se eliminó el UUID fijo de las cinco rutas de billetera. El login y el contrato financiero aún no resuelven la cuenta autenticada; sin ID válido ahora se muestra un estado honesto y Ayuda, sin petición de red ni operación. Un ID de query solo habilita la pantalla: **la autorización de titularidad debe ocurrir en backend**. Enlace y 13 pruebas nuevas: [evidencia](./evidencia/verificacion-cuenta-billetera-2026-10-07.md).
- Flutter 3.44.8: **271/271** pruebas no-golden, analyzer, verificador y APK debug PASS. Goldens Windows **4 PASS/3 FAIL** sin snapshots actualizados. No se obtuvo captura de esta pantalla en dispositivo ni validación iOS.
- El flujo P0 de billetera sigue **bloqueado**, no cerrado. Hace falta un GET autenticado que resuelva cuentas/titularidad y pasar el ID autorizado por las rutas; esto amplía el contrato backend, fuera del alcance aprobado del plan. No se hizo merge forzado de PR #15 con checks remotos rojos.

### Estados y promesas comprobables en `d1aa8a5`

- El inicio de billetera ya no afirma que la persona no tiene pasanakus ni movimientos sin consultar esos datos. La sección de extracto describe exactamente lo que su contrato devuelve (saldo final y cantidad de movimientos). El texto visible de custodia deja de nombrar a Banco Unión: el contrato de adhesión incluido en la app define una cuenta de custodia, pero no identifica ese banco como socio de AportaYa. **Cumplimiento aún debe aprobar el texto final**.
- `/pasanaku/mi-estado` sin `participanteId` o `usuarioId` ya no envía una petición mal formada: muestra el dato faltante y enlaza a Ayuda. Se probaron las dos ausencias en claro/oscuro a 360×760 y texto 200 %, sin llamadas de red, además de la navegación real al centro de ayuda. No resuelve la navegación de «Aportar»: el shell no tiene fuente de esos IDs ni GET de obligaciones elegibles.
- Flutter 3.44.8: **258/258** pruebas no-golden, analyzer, verificador y APK debug PASS. Goldens Windows **4 PASS/3 FAIL**; saldo claro/oscuro cambian por layout/copy y la transición por copy, además de las diferencias previas de raster. No se actualizaron snapshots. [Evidencia](./evidencia/verificacion-estados-honestos-2026-10-07.md).

### Saldo cero y acciones legibles en `f128a33`

- Una cuenta con saldo cero ya no reemplaza el inicio por un estado vacío: muestra **Bs 0,00**, «Recargar» y el contexto de pasanakus/movimientos. Los botones se apilan cuando su ancho no alcanza, con umbral que crece según la escala de texto; el desglose «Retenido» envuelve sin desbordar.
- Con Flutter 3.44.8 pasaron **253/253** pruebas no-golden, `flutter analyze --no-pub --fatal-infos`, el verificador móvil y la compilación del APK debug. Los tests nuevos comprueban etiquetas sin elipsis ni overflow en claro/oscuro, 360–600 px y texto 100/140/200 %, incluidos ambos lados del breakpoint. [Evidencia detallada](./evidencia/verificacion-saldo-cero-2026-10-07.md).
- Los goldens siguen **4 PASS/3 FAIL en Windows**, pero los dos de saldo ahora tienen un diff intencional de layout del 44 %: botones apilados. Las imágenes claro/oscuro generadas se abrieron y se comprobó la composición, no la tipografía real (Ahem). No se actualizaron referencias: falta captura real y golden macOS antes de aprobar H7.S1.M3/H8.S1.M4. Actions continúa rechazando jobs por facturación.

### Paridad de SDK y guardas de aporte en `94b44bf`

- La suite completa no-golden de Flutter **3.44.8** —misma versión fijada en CI— pasó **197/197**, `flutter analyze` y el verificador local están limpios, y el APK debug compiló. El lockfile quedó resuelto para Dart 3.12.2. [Evidencia](./evidencia/verificacion-flutter-3448-2026-10-07.md).
- Los goldens en esa versión dieron **4 PASS/3 FAIL en Windows**: saldo claro/oscuro y transición. Aporte claro/oscuro pasó; los dos fallos extra en Flutter 3.47.5 no eran reproducibles con 3.44.8. No se actualizaron snapshots; falta Mac/CI.
- El aporte ahora guarda la clave de idempotencia antes del POST y una huella de sus datos en almacén seguro. Un reinicio simulado reutiliza la clave; un reintento con datos cambiados no llega a la red y explica qué hacer. Son pruebas simuladas, no E2E real ni prueba de app-kill en dispositivo.
- Un monto ausente, cero o inválido bloquea el POST y muestra un estado informativo sin CTA de pago, incluso con texto al 200 % en pruebas de widget claro/oscuro. **Un monto positivo aún proviene de la ruta, no del backend**: esto es contención, no cierre contractual ni autorización de release. La captura de widget usa la fuente de test Ahem y no sirve como aprobación visual de tipografía; falta inspección real en dispositivo.
- [Journey P0 contrastado con código](./JOURNEY-P0-BORRADOR.md): intención, acción, dato y riesgo por momento. Es borrador, no research aprobado. Revela dos bloqueos de contrato: monto de obligación por parámetro de ruta sin GET autoritativo y entrega/cobro de turno sin pantalla/GET real.
- Los gates remotos de PR #15 siguen fallando antes de Flutter/macOS/iOS porque GitHub Actions informa pagos fallidos o límite de gasto de la cuenta; no se fusionó el código.

### Cierre de evidencia en `8308b9a`

- El alta ya no oculta un fallo de subida de fotos como éxito pleno: conserva la cuenta creada, informa el expediente pendiente y dirige a ingreso/soporte sin repetir el alta. La copia temporal de cada foto se elimina incluso cuando falla su lectura o el envío.
- `flutter test test/a11y test/identidad test/unidad test/widget --reporter compact`: **178/178 PASS**. Incluye 500 simulado al subir documento y aviso en una pantalla de 360×760 con texto al 200 %. `flutter analyze --fatal-infos` y `python -X utf8 scripts/verificar_frontend.py movil`: PASS. APK debug construido después del último cambio.
- Dos capturas Android 1080×1920 de la ruta de aviso, con fixture sintético, abiertas e inspeccionadas: [claro](./evidencia/android-alta-fotos-pendientes-claro.png) y [oscuro](./evidencia/android-alta-fotos-pendientes-oscuro.png). Aviso, campos y acción de ingreso legibles sin recorte. El emulador mató el proceso al intentar escalar texto al 200 %; esa variante sólo tiene prueba de widget, no captura Android válida.
- En aquel cierre se usó Flutter **3.47.5**; posteriormente se instaló 3.44.8 de forma aislada y se repitió la verificación anterior.
- Repetición de `test/goldens` en ese entorno: **2 PASS, 5 FAIL** (aporte, saldo y transición); se inspeccionaron diffs de contornos/texto, sin actualizar referencias ni atribuir todavía la causa. La comprobación en Mac/Flutter 3.44.8 sigue siendo gate de integración.
- Alcance y conteo se mantienen en **11/41 HECHO**: H7.S1.M2/H8.S1.M3/H8.S1.M4 siguen sin cumplir sus DoD completos. Detalle y límites: [evidencia de este cierre](./evidencia/cierre-ejecucion-2026-10-07.md).

### Continuación ejecutada en `codex/mobile-design-merge-2026-10-07`

Esta continuación histórica amplió el código sin completar nuevas microtareas: H7.S1.M2 sigue A MEDIAS porque el DoD exige recorrido completo tras cierre de proceso y evidencia en Android/iOS; H7.S1.M4/H8.S1.M3 requieren backend TEST real. El cambio posterior H4.S1.M1 a EN CURSO consta arriba.

| Área | Resultado comprobable |
|---|---|
| Alta reanudable | Borrador local cifrado (Keychain/Keystore), TTL de 24 h, excluye contraseña/OTP/contrato/rutas de fotos y vuelve a verificación de celular; 3 pruebas unitarias de omisiones, re-verificación y expiración. Requiere revisión formal de privacidad/seguridad antes de activarlo en producción. |
| Cierre por ciclo de vida | `inactive`/`paused` fuerza el guardado inmediato; las escrituras se serializan y un alta aceptada borra el borrador despues de las pendientes. Pruebas nuevas cubren pausa sin esperar debounce y borrado al crear la billetera. |
| Limpieza excepcional | Si el borrado seguro falla al crear la cuenta, se anuncia despues de navegar con un mensaje de accion clara, sin bloquear la cuenta ni ocultar el aviso en una pantalla que se cierra. |
| Alta y mantenibilidad | Se separó el notifier del estado y se dividieron formularios/pasos extensos; el verificador local confirma que no quedan archivos Dart sobre 200 líneas. |
| Configuración Android | Se corrigió el rechazo de `10.0.2.2` en modo debug; el mismo host sigue rechazado en release. La prueba de configuración cubre el límite. |
| Aporte e invitación | Aporte se partió en componentes pequeños. Invitación usa el campo real `invitacionId` del DTO y lo presenta como código, sin inventar URL. |
| Portabilidad web | El lector de contenido acepta delimitadores YAML con CRLF; corrigió el typecheck local en Windows. |
| Pruebas Flutter | `flutter analyze --fatal-infos`: limpio; suite no-golden: 175/175. `flutter build apk --debug --dart-define=API=http://10.0.2.2:4010/api/v1` compilo antes del cambio final de ciclo de vida; el intento posterior se quedo varios minutos sin avance en Gradle/Kotlin y se interrumpio. |
| Prueba de dispositivo | Patrol compiló el bundle pero reportó cero pruebas; el proceso fue terminado por presión de memoria del emulador. No se cuenta como E2E ni como prueba de reanudación tras cierre. La captura resultante no es evidencia visual válida. |
| Suites web | 709 pruebas JS reportadas PASS entre workspaces. Typecheck individual en 7 workspaces PASS; `@aportaya/web` pasa tras generar contenido. Simulado ahora genera sus contratos/ejemplos antes de probar. |
| Herramientas | GitHub Actions sigue sin ejecutar jobs por el bloqueo de facturación de la cuenta. `yarn lint` ejecuta ESLint pero su gate Python no corre en este Windows (falta `python3`); los verificadores Python invocados como `python -X utf8` pasan localmente. |

Evidencia detallada de comandos/resultados: [continuacion-ejecucion-2026-10-07.md](./evidencia/continuacion-ejecucion-2026-10-07.md).

| Área | Resultado comprobable |
|---|---|
| Motion | Escala de 12 duraciones por intención añadida a la bóveda, CSS y Dart; portada, tour, pestañas, navegación, marca, contadores y microinteracciones consumen tokens. |
| Movimiento reducido | Entrada escalonada y presión eliminan movimiento sin perder contenido. La prueba descubrió y permitió corregir una inicialización tardía durante `dispose`. |
| Aporte P0 | El monto reglamentario ya no parece editable; canal y referencia tienen jerarquía clara; éxito y reintento usan lenguaje humano. |
| Dinero seguro | Pruebas de widget con adaptador HTTP falso: doble toque genera una sola petición; un fallo reintenta con la misma clave de idempotencia; no se muestra el enum técnico `PENDIENTE`. El backend real no fue ejercitado. |
| Accesibilidad | Gates de objetivo táctil Android, etiquetas, contraste y texto al 200 % pasan en claro y oscuro. |
| Evidencia visual | Cuatro capturas inspeccionadas: formulario/confirmación × claro/oscuro a 360 × 760. |
| Android | `assembleDebug` compiló e instaló; recorrido manual de bienvenida → tour → alta, con campo enfocado y teclado visible en emulador Android 17/API 37. No se enviaron datos. |
| Texto grande en bienvenida | Se detectó overflow en garantías y CTA fijo; las etiquetas ahora parten línea y con escala ≥ 1,5 las acciones entran en el scroll. La regresión y la captura Android al 200 % pasan. |
| Generación local | Los serializadores `*.g.dart` de los clientes Dart ahora están excluidos con una regla específica; Git confirmó identidad, aportes y cumplimiento. |
| Contratos | Cliente Dart de `cumplimiento` regenerado desde OpenAPI; recupera `ContratoVigente` y desbloquea compilación/análisis de la app. |
| Portabilidad | Dos pruebas de arquitectura fueron corregidas para normalizar separadores Windows/Linux. |
| Activación y cámara | Denegación/excepción de cámara mantiene el flujo; alternativa manual solo para fotos de documento y selección de foto disponible en la prueba de vida. 3 pruebas nuevas pasan. |

## Completado

| ID | Qué se logró | DoD observado |
|---|---|---|
| H1.S1.M1–M3 | Auditoría de Atlas y del sistema Flutter | Inventario y matriz en PLAN.md §3; capturas de referencia inspeccionadas. |
| H2.S1.M1–M2 | 8 skills Figma y 14 skills mobile/UX/motion instaladas | [skills-instaladas.txt](./evidencia/skills-instaladas.txt) muestra `installed=true` y `Present=True`. |
| H5.S1.M2 | Tokens de motion en fuente JSON, CSS y Dart | `yarn workspace @aportaya/tokens test:front` → `16 pruebas · PASS` ([evidencia](./evidencia/verificacion-implementacion-2026-10-07.txt)). |
| H6.S1.M4 | Catálogo de motion con reduced motion | `flutter test test/widget/movimiento_test.dart` → `3 pruebas · PASS` ([evidencia](./evidencia/verificacion-implementacion-2026-10-07.txt)). |
| H7.S1.M1 | Foundations de diseño en Flutter | `flutter test test/unidad test/widget test/a11y` → `41 pruebas · PASS`. |
| H7.S1.M5 | Motion y movimiento reducido | `flutter test test/widget/movimiento_test.dart` → `3 pruebas · PASS`. |
| H7.S1.M6 | Bienvenida operable con texto al 200 % | `flutter test test/a11y/pantalla_portada_texto_grande_test.dart` → `All tests passed!`; captura Android inspeccionada. |
| H7.S1.M7 | Serializadores generados excluidos de Git | `git check-ignore -v` reconoce `.g.dart` de identidad, aportes y cumplimiento. |

## Verificación

- Integración Frontend sobre el `dev` vigente: PR #15 abierta; GitHub Actions no ejecutó jobs porque la cuenta alcanzó un bloqueo de facturación. Los jobs Flutter también quedaron omitidos, así que no se considera verificación de CI ni mergeable todavía.
- Tras `469cd38`, Actions volvió a lanzar workflows: los gates fallaron en 2–6 s; los dependientes, incluido Frontend — Flutter y Angular, quedaron `skipped`. Ver ejecuciones [37709135911](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37709135911) y [37709135155](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37709135155). El frontend no se ejecutó. El PR es `MERGEABLE` por git pero `UNSTABLE` por checks; no se fusionó.

La evidencia literal está en [verificacion-implementacion-2026-10-07.txt](./evidencia/verificacion-implementacion-2026-10-07.txt).

- Tokens: 16/16 pruebas.
- Sistema de diseño Flutter: 41/41 pruebas de unidad, widget y accesibilidad.
- App móvil: 127/127 pruebas funcionales y 7/7 pruebas de accesibilidad.
- Aporte: 3/3 pruebas de flujo y 4/4 capturas golden.
- Análisis: sistema de diseño limpio; app móvil limpia tras regenerar el cliente oficial y corregir un lint.
- `git diff --check`: sin errores.
- `flutter analyze --fatal-infos` → `No issues found! (ran in 10.6s)`.
- `flutter test test/widget/portada_test.dart test/a11y/pantalla_portada_texto_grande_test.dart test/pasanaku/pantalla_aportar_test.dart test/a11y/pantalla_aportar_a11y_test.dart test/goldens/pantalla_aportar_golden_test.dart --reporter expanded` → `All tests passed!` (18 tests).
- `flutter test test/identidad/paso_captura_test.dart --reporter expanded` → 3/3 PASS: denegación, alternativa por fotos/manual y excepción del plugin.
- `flutter test --reporter compact` → 142 PASS y 3 fallos de golden en vistas de saldo/transición, no relacionados directamente con captura. Se inspeccionaron los comparativos; las diferencias son píxeles aislados/bordes de rasterizador. No se actualizaron snapshots.
- `flutter analyze --fatal-infos` después del cambio de captura → `No issues found! (ran in 11.2s)`.
- `flutter build apk --debug` → `Built build\\app\\outputs\\flutter-apk\\app-debug.apk`; APK instalado y proceso Android activo en Pixel_2 AVD (API 36).
- `git check-ignore -v` para serializadores de identidad/aportes/cumplimiento → todos coinciden con `.gitignore`; [evidencia](./evidencia/verificacion-generados-2026-10-07.txt).
- Android: `flutter run -d emulator-5554` → `√ Built build\app\outputs\flutter-apk\app-debug.apk`; instalación y sincronización completadas. Extracto literal y dispositivo: [verificación Android](./evidencia/verificacion-android-smoke-2026-10-07.txt).
- La prueba nueva falló antes del arreglo con overflow horizontal y CTA inmóvil; tras el arreglo pasó. Salida: [regresión de portada](./evidencia/verificacion-portada-texto-grande-2026-10-07.txt).

## Evidencia

- [Pruebas y análisis anteriores](./evidencia/verificacion-implementacion-2026-10-07.txt)
- [Compilación e inicio Android](./evidencia/verificacion-android-smoke-2026-10-07.txt)
- [Regresión de texto grande](./evidencia/verificacion-portada-texto-grande-2026-10-07.txt)
- [Archivos generados ignorados](./evidencia/verificacion-generados-2026-10-07.txt)
- [Ejecución adicional: activación/cámara y suite](./evidencia/verificacion-activacion-captura-2026-10-07.txt)
- Capturas de bienvenida, tour, alta, teclado y 200 % listadas arriba.

## Evidencia visual inspeccionada

- `apps/movil/test/goldens/imagenes/aporte_formulario_claro.png`
- `apps/movil/test/goldens/imagenes/aporte_formulario_oscuro.png`
- `apps/movil/test/goldens/imagenes/aporte_confirmado_claro.png`
- `apps/movil/test/goldens/imagenes/aporte_confirmado_oscuro.png`
- [Bienvenida Android](./evidencia/android-inicial.png)
- [Tour Android](./evidencia/android-tour.png)
- [Alta Android](./evidencia/android-crear-cuenta.png)
- [Alta Android con teclado](./evidencia/android-teclado.png)
- [Portada del APK actualizado](./evidencia/android-portada-ejecucion-final.png)
- [Tour del APK actualizado](./evidencia/android-tour-ejecucion-final.png)
- [Alta del APK actualizado](./evidencia/android-alta-ejecucion-final.png)
- [Alta con teclado del APK actualizado](./evidencia/android-alta-teclado-final.png)
- [Bienvenida al 200 % antes del arreglo](./evidencia/android-texto-200.png)
- [Bienvenida al 200 % después, inicio](./evidencia/android-texto-200-corregido.png)
- [Bienvenida al 200 % después, scroll hasta las acciones](./evidencia/android-texto-200-corregido-scroll.png)

Veredicto de la pasada visual: jerarquía focal única en monto/resultado, CTA visible, sin overflow a 360 × 760, contraste coherente en ambos temas. Los íconos aparecen como glifos cuadrados en el rasterizador de widget tests de Windows; no se interpreta como evidencia del ícono real y debe revalidarse en dispositivo.

## A medias

- H3: la instrucción del propietario permite ejecutar el P0, pero faltan actas formales de Producto/Cumplimiento, dispositivo de referencia y baseline de analytics.
- H5/H6: código y tokens avanzaron; Figma sigue sin conexión, por lo que no hay variables publicadas, prototipo navegable ni Code Connect.
- H7: foundations, reduced motion y adaptación de bienvenida a texto grande están hechos. Alta solo se recorrió hasta el primer paso; aporte tiene pruebas de widget con HTTP falso, no E2E. Faltan completar el flujo, backend TEST, persistencia y evidencia iOS.
- H8: automatización y capturas locales pasan; se añadió inspección parcial del emulador. Faltan TalkBack, VoiceOver, perfilado y matriz completa de fallos.
- H8.S1.M7: qué anda: las tres rutas de acciones personales muestran contención y seis tests prueban cero peticiones; qué no anda: crear como organizador, retiro y permuta no pueden ejecutarse legítimamente desde esos enlaces; qué falta: titular autenticado en contrato, autorización backend con dos usuarios, TEST y dispositivo; dónde quedó: `6f8ecf0` en PR #15, [evidencia](./evidencia/verificacion-acciones-personales-desde-enlace-2026-10-08.md).

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| H3.S1.M1 | EN CURSO | Acta de Producto con orden P0. |
| H3.S1.M2 | EN CURSO | Aprobación de Diseño y Cumplimiento. |
| H3.S1.M3 | TODO | Nombrar y documentar dispositivo físico de referencia. |
| H3.S1.M4 | TODO | Data confirma fuente, dueño y fecha del baseline. |
| H4.S1.M1 | EN CURSO | [Borrador contrastado con código](./JOURNEY-P0-BORRADOR.md); falta taller y aprobación Producto/UX. |
| H4.S1.M2 | TODO | Participantes, consentimiento y protocolo de research. |
| H4.S1.M3 | EN CURSO | Aprobación de taxonomía sin PII/importes y payloads TEST. |
| H4.S1.M4 | TODO | Eventos QA y ventana de datos disponibles. |
| H5.S1.M1 | TODO | Conexión Figma para exportar variables. |
| H5.S1.M3 | EN CURSO | Inventario final de variantes P0 en Figma y Flutter. |
| H5.S1.M4 | TODO | Figma conectado para validar Code Connect. |
| H5.S1.M5 | TODO | Paridad Figma/código aprobada y changelog. |
| H6.S1.M1 | TODO | Figma conectado y validación del flujo completo. |
| H6.S1.M2 | TODO | Prototipo de portada y participantes de prueba. |
| H6.S1.M3 | EN CURSO | Backend de prueba y segunda ronda de usabilidad. |
| H6.S1.M5 | TODO | Revisión de Cumplimiento sobre contenido final. |
| H7.S1.M2 | A MEDIAS | Definir/implementar OTP real con Identidad/Seguridad; luego recorrer alta y reanudación en Android/iOS. |
| H7.S1.M3 | EN CURSO | Prototipo aprobado y captura de portada en dispositivos. |
| H7.S1.M4 | A MEDIAS | Backend TEST real para E2E idempotente, sin adaptador falso. |
| H8.S1.M1 | EN CURSO | Portada inspeccionada con TalkBack en AVD; faltan recorrido auditivo P0, VoiceOver y revisión en dispositivo físico. |
| H8.S1.M2 | EN CURSO | Arranque profile diagnóstico en AtlasDemo; faltan p95 del recorrido P0 y dispositivo de referencia. |
| H8.S1.M3 | EN CURSO | Backend TEST y matriz real de red/app kill/reintento. |
| H8.S1.M4 | A MEDIAS | Capturas equivalentes iOS/Android, temas y escalas. |
| H8.S1.M5 | TODO | Research moderado con muestra y métricas acordadas. |
| H8.S1.M6 | EN CURSO | Revisión Seguridad/Cumplimiento, escaneo de payloads TEST y captura iOS; el escaneo estático parcial está documentado. |
| H8.S1.M7 | A MEDIAS | Contrato de titular autenticado y prueba de autorización con dos usuarios en backend TEST; luego recorrido Android/iOS. |
| H9.S1.M1 | TODO | Build candidato y cohorte dogfood. |
| H9.S1.M2 | TODO | Go/no-go del piloto y feature flag/rollback probado. |
| H9.S1.M3 | TODO | Guardrails del 5 % sanos y soporte preparado. |
| H9.S1.M4 | TODO | Decisión de expansión a 100 % con observabilidad. |
| H9.S1.M5 | TODO | Datos de operación a 7/30 días. |

## No cubierto / no se debe afirmar aún

- No hubo prueba con usuarios ni medición de task success.
- No hubo E2E con backend desplegado, persistencia tras app kill, timeout real o red intermitente de dispositivo.
- AtlasDemo produjo traza de arranque profile y muestra puntual de memoria, pero no hubo medición p95 ni recorrido P0 en gama baja/dispositivo de referencia.
- No hubo build firmado, publicación en tiendas, rollout ni rollback.
- No se creó ni editó Figma porque el plugin fue sugerido pero no está conectado.

## Desvíos del plan

- Se adelantó `AtlasFrontend` con `git merge --ff-only origin/dev` (de `2a2468a` a `a85dc80`), porque la rama de referencia estaba 82 commits detrás y limpia. `PasanakuFrontend` solo recibió `fetch`; no se integró nada sobre su árbol con cambios locales.
- Se añadió H7.S1.M6 después de encontrar en Android un overflow al 200 %; la microtarea ya tiene prueba, análisis y evidencia visual.
- Se añadió H7.S1.M7 al constatar que el comentario de `.gitignore` prometía ignorar generados, pero no cubría los `.g.dart`; regla validada con tres clientes.
- H7.S1.M4 se reclasificó de HECHO a A MEDIAS: las pruebas disponibles usan adaptador HTTP falso y no cumplen el DoD de E2E contra backend TEST.
- H8.S1.M7 se incorporó después de encontrar rutas que aceptaban IDs personales de enlaces; el código empezó antes de registrar esta microtarea en el plan. La secuencia no cumplió la regla de plan previo y queda explicitada como desvío, sin convertir la contención en funcionalidad terminada.

## Decisiones y ambigüedades

- Sigue pendiente Producto/Cumplimiento: confirmación de prioridad comercial y aprobación de mensajes/custodia.
- Sigue pendiente Mobile/QA: dispositivo físico de referencia, validación iOS y pruebas TalkBack/VoiceOver.
- Sigue pendiente Figma: conexión del plugin y archivo canónico; no se inventó un prototipo ni se copiaron componentes de Atlas.

## Riesgos residuales

- La transición de marca conserva 1450 ms. Está tokenizada y tiene reduced motion, pero necesita comparación 900/1450 en dispositivo antes de congelarse.
- Los goldens de Flutter dependen del rasterizador; sirven para revisión local y regresión en la misma plataforma, no prueban paridad Android/iOS.
- El primer arranque falló porque faltaban `.g.dart`; al generarlos con `build_runner`, el APK compiló. Ahora esos serializadores quedan ignorados. La versión instalada avisó que `--delete-conflicting-outputs` ya no se reconoce y lo ignora. La ejecución del script Bash falla en esta máquina porque `bash` apunta a WSL no instalado; la ejecución CI Linux no fue alterada.
- El repositorio contenía cambios previos en capturas web, legal, vectores, reglas y simulados; se preservaron sin mezclarlos con esta implementación.

## Próximo gate

1. Conectar Figma y publicar foundations/componentes P0.
2. Ejecutar activación → portada → aporte en Android e iOS con TalkBack/VoiceOver.
3. Medir frame timing, memoria y transición 900/1450 en dispositivo de referencia.
4. Validar offline/timeout/500/app kill contra backend TEST.
5. Cerrar H3/H4 con research, analytics y aprobaciones; solo entonces preparar piloto.

## Actualizacion 2026-10-08: titularidad de billetera

En la revision de las rutas se detecto que un `?cuenta=<UUID>` valido habilitaba las cinco pantallas de billetera sin comprobar que la cuenta perteneciera a la sesion. El contrato de login no entrega la cuenta autenticada y el OpenAPI de nucleo-financiero no publica una ruta para resolverla. El frontend del PR #15 ahora ignora ese parametro y muestra el estado seguro con salida a Ayuda; un UUID de formato valido ya no provoca GET ni POST. Las pantallas de operacion siguen implementadas, pero no son accesibles por rutas de usuario hasta disponer del contrato de titularidad autenticada. Esto no convierte ninguna microtarea pendiente en HECHO ni sustituye la integracion backend.

Verificacion local de este cambio: 333/333 pruebas no-golden, analisis estatico limpio y cuatro goldens nuevos que pasan en Windows. Se abrio e inspecciono cada captura: movil 360x760 claro/oscuro, tablet 768x1024 claro y movil 360x760 oscuro al 200 %; mensaje, candado y CTA legibles, sin recortes visibles. En `c64e571` estas cuatro comparaciones se limitaron a Windows: en Mac se omiten hasta inspeccionar esa plataforma y crear referencias propias; no se cubrieron dispositivo real, VoiceOver/TalkBack ni backend TEST. GitHub Actions sigue sin iniciar por facturacion, asi que el PR #15 permanece sin merge.

Intento adicional de H7.S1.M2 en Android debug: APK compilado e instalado, pero el AVD `Pixel_2` cerro la app dos veces con `ApplicationExitInfo reason=3 (LOW_MEMORY)` antes de llegar a portada. Se apago el emulador; no se afirmo reanudacion del alta. [Comandos, salida y limite](./evidencia/android-alta-reinicio-low-memory-2026-10-08.md).

La continuacion del PR #15 en `c52a22c` quita el UUID de cuenta de la navegacion interna hacia recarga/retiro/extracto. En `a630b86`, una prueba que fallaba con overflow de 6 dp a texto 200 % llevo a adaptar la tarjeta de saldo: apilado de desglose/acciones y corte del importe extremo entre grupos de miles, con semantica completa. [Matriz de seis capturas inspeccionadas, pruebas y limites](./evidencia/verificacion-tarjeta-saldo-200-2026-10-08.md). Esto mejora el catalogo Flutter y la privacidad de navegacion, pero no sustituye paridad Figma, backend autorizado ni capturas iOS/Android; H5.S1.M3 sigue EN CURSO y H8.S1.M4 A MEDIAS. DoD total: **11/41 HECHO**.
