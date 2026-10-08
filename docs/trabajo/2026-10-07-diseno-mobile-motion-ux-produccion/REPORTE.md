# Reporte — Diseño mobile, motion y UX hacia producción

- Fecha: 2026-10-07 · Actualizado: 2026-10-08 · Plan: [PLAN.md](./PLAN.md) · Atlas actualizado: `dev` (`1fd49c6`).
- Continuidad publicada: `PasanakuFrontend` en `codex/mobile-design-merge-2026-10-07` (`20300cc`, PR #15); este reporte y evidencia en `PasanakuPromptManager`.
- Continuación Mac: [CONTINUAR-EN-MAC.md](./CONTINUAR-EN-MAC.md).
- Peldaño de evidencia: TESTED. El APK debug compiló e instaló en emulador Android; se inspeccionó el aviso de fotos pendientes en claro/oscuro con datos sintéticos. No se verificaron persistencia ni red contra backend real.
- Avance del roadmap: 11 / 41 microtareas HECHO (26,8 %), 10 EN CURSO, 3 A MEDIAS y 17 TODO. H4.S1.M1 y H4.S1.M3 tienen borradores contrastados, no aprobación ni instrumentación real. El programa completo aún no es un release candidate.
- Bloqueo contractual P0 concretado: [decisión OTP del alta](./DECISION-OTP-ALTA-PENDIENTE.md). El backend actual crea usuario pendiente sin prueba de contacto; Producto, Identidad y Seguridad deben elegir verificación antes o después de `POST /usuarios`. Ninguna de las dos está aprobada ni implementada.
- Bloqueo contractual del aporte concretado: [GET de obligación pendiente](./DECISION-OBLIGACION-APORTE-PENDIENTE.md). El GET agregado de participante no permite verificar un importe CU-21; faltan respuesta por obligación, titularidad autorizada y backend TEST. La ruta móvil continúa sin pago.
- Rendimiento sin evidencia: [el intento de `flutter run --profile` en AVD Android quedó bloqueado por Control de aplicaciones de Windows](./evidencia/perfil-android-bloqueado-2026-10-08.md) antes de ejecutar la app. No hay trace ni medición; H8.S1.M2 sigue TODO.

## Resultado de esta iteración

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

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| H3.S1.M1 | EN CURSO | Acta de Producto con orden P0. |
| H3.S1.M2 | EN CURSO | Aprobación de Diseño y Cumplimiento. |
| H3.S1.M3 | TODO | Nombrar y documentar dispositivo físico de referencia. |
| H3.S1.M4 | TODO | Data confirma fuente, dueño y fecha del baseline. |
| H4.S1.M1 | EN CURSO | [Borrador contrastado con código](./JOURNEY-P0-BORRADOR.md); falta taller y aprobación Producto/UX. |
| H4.S1.M2 | TODO | Participantes, consentimiento y protocolo de research. |
| H4.S1.M3 | TODO | Aprobación de taxonomía sin PII/importes. |
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
| H8.S1.M1 | EN CURSO | TalkBack, VoiceOver y revisión manual en dispositivo. |
| H8.S1.M2 | TODO | Dispositivo de referencia y traza `flutter run --profile`. |
| H8.S1.M3 | EN CURSO | Backend TEST y matriz real de red/app kill/reintento. |
| H8.S1.M4 | A MEDIAS | Capturas equivalentes iOS/Android, temas y escalas. |
| H8.S1.M5 | TODO | Research moderado con muestra y métricas acordadas. |
| H8.S1.M6 | EN CURSO | Revisión Seguridad/Cumplimiento, escaneo de payloads TEST y captura iOS; el escaneo estático parcial está documentado. |
| H9.S1.M1 | TODO | Build candidato y cohorte dogfood. |
| H9.S1.M2 | TODO | Go/no-go del piloto y feature flag/rollback probado. |
| H9.S1.M3 | TODO | Guardrails del 5 % sanos y soporte preparado. |
| H9.S1.M4 | TODO | Decisión de expansión a 100 % con observabilidad. |
| H9.S1.M5 | TODO | Datos de operación a 7/30 días. |

## No cubierto / no se debe afirmar aún

- No hubo prueba con usuarios ni medición de task success.
- No hubo E2E con backend desplegado, persistencia tras app kill, timeout real o red intermitente de dispositivo.
- No hubo trace de frames/memoria en gama baja. En el arranque debug del emulador se observaron frames omitidos durante compilación/carga inicial; hace falta perfilado en modo profile para evaluar rendimiento.
- No hubo build firmado, publicación en tiendas, rollout ni rollback.
- No se creó ni editó Figma porque el plugin fue sugerido pero no está conectado.

## Desvíos del plan

- Se adelantó `AtlasFrontend` con `git merge --ff-only origin/dev` (de `2a2468a` a `a85dc80`), porque la rama de referencia estaba 82 commits detrás y limpia. `PasanakuFrontend` solo recibió `fetch`; no se integró nada sobre su árbol con cambios locales.
- Se añadió H7.S1.M6 después de encontrar en Android un overflow al 200 %; la microtarea ya tiene prueba, análisis y evidencia visual.
- Se añadió H7.S1.M7 al constatar que el comentario de `.gitignore` prometía ignorar generados, pero no cubría los `.g.dart`; regla validada con tres clientes.
- H7.S1.M4 se reclasificó de HECHO a A MEDIAS: las pruebas disponibles usan adaptador HTTP falso y no cumplen el DoD de E2E contra backend TEST.

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
