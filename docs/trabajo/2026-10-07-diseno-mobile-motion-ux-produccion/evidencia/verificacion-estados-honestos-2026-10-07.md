# Estados y textos verificables — `d1aa8a5`

Se comparó el inicio con las respuestas reales disponibles: `GET /billetera/{cuentaId}/saldo` entrega saldo disponible/retenido, pero no lista de grupos ni movimientos. El contrato de `grupos` no ofrece un listado de participaciones de la persona. El extracto actual entrega período, saldo final y cantidad de movimientos, no una lista. Por eso se retiraron del inicio los mensajes absolutos «Todavía no estás en ningún pasanaku» y «Todavía no tenés movimientos», que aparecían incluso ante cuentas activas. El inicio ahora indica que no puede mostrar el detalle de pasanakus y enlaza a la consulta de extracto con lo que realmente devuelve.

La copia visible de portada, ingreso y billetera nombraba Banco Unión como custodio. El contrato de adhesión integrado (`apps/movil/lib/pantallas/identidad/texto_del_contrato.dart`) describe una cuenta de custodia separada del patrimonio de AportaYa, pero no identifica una entidad concreta. La copia de UI ahora usa esa formulación genérica. Esto elimina una afirmación no respaldada por el contrato consultado; **no equivale a aprobación de Cumplimiento** ni verifica situación bancaria real.

`/pasanaku/mi-estado` se abre desde la pestaña Grupos y el botón «Aportar» sin `participanteId`/`usuarioId`. Antes se intentaban peticiones con rutas vacías; ahora la pantalla muestra una explicación y un botón «Ir a ayuda» antes de leer providers. Cuatro pruebas (ID faltante de cada tipo × claro/oscuro) a 360×760 y texto 200 % verifican **cero peticiones**, acción visible y sin overflow. Otra prueba usa el enrutador real y confirma que «Ir a ayuda» llega a `/soporte/ayuda`. La acción «Aportar» sigue sin llevar a una obligación: este es un bloqueo P0, no un flujo completo.

| Flutter 3.44.8 / Dart 3.12.2 | Resultado |
|---|---|
| `flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact` | **258 PASS, 0 FAIL** |
| `flutter analyze --no-pub --fatal-infos` | `No issues found!` |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK` |
| `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` | APK debug construido |
| `flutter test --no-pub test/goldens --reporter expanded` | **4 PASS, 3 FAIL** en Windows |

Los goldens de saldo claro/oscuro tienen diferencias deliberadas de layout y texto (el claro reportó 45,13 %); el test de transición de marca incluye el nuevo texto de ingreso (el cuadro `llega` reportó 2,11 %). Se abrieron las imágenes de resultado de saldo claro/oscuro y del cuadro `llega`: no se observó recorte geométrico, pero la fuente Ahem impide validar la tipografía real. No se actualizaron snapshots. [Actions 37716292682](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37716292682) no inició jobs por pagos fallidos o límite de gasto de la cuenta; macOS/iOS/Flutter fueron omitidos. PR #15 sigue sin fusionar.

**Para cerrar:** backend/Producto deben definir y probar GET autorizados de participaciones y obligaciones elegibles de la persona autenticada; la app debe usar esos IDs y un monto autoritativo, no query vacía/positiva. Cumplimiento debe aprobar la copia de custodia. QA debe inspeccionar capturas con fuente real en Android/iOS, claro/oscuro y texto grande, y luego decidir goldens macOS. Sin esos pasos no se marca H6.S1.M5, H7.S1.M3, H7.S1.M4 ni H8.S1.M4 como HECHO.
