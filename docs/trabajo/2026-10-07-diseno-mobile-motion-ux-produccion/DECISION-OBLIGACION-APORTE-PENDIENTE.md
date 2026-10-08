# Contrato pendiente: importe vigente de una obligación de aporte

Estado: **propuesta no aprobada** para Aportes, Seguridad, Producto y Mobile. Bloquea H7.S1.M4 y el merge de [frontend PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). La ruta móvil falla cerrada desde [`7c12866`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/7c12866): descarta `?monto=` y no permite iniciar un POST de pago con un importe de URL.

## Evidencia del contrato actual

- [`aportes.yaml`](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/dev/servicios/aportes/src/main/resources/openapi/aportes.yaml) publica `POST /aportes/obligaciones/{obligacionId}/pagos`, pero ningún GET de **esa obligación**. `GET /aportes/participantes/{participanteId}/estado` devuelve un agregado (`porAportar`, `obligacionesAbiertas`), no el importe ni estado de una obligación identificada; no es fuente válida para el formulario CU-21.
- [`ObligacionRepositorio.ver`](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/dev/servicios/aportes/src/main/java/bo/aportaya/aportes/infraestructura/ObligacionRepositorio.java) sí lee internamente esperado, pagado, condonado, garantía, moneda, estado, vencimiento y versión. No expone esos datos al cliente ni demuestra autorización del titular para una consulta pública.
- [`CU21CobrarAporte`](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/dev/servicios/aportes/src/main/java/bo/aportaya/aportes/aplicacion/CU21CobrarAporte.java) bloquea la fila y rechaza exceso y estados PAGADO/ANULADO en el POST. Esa validación final es necesaria, pero no reemplaza mostrar un importe vigente y verificable **antes** de confirmar.
- `PantallaAportar` conserva monto fijo, revisión e idempotencia para pruebas aisladas; no está conectada a la ruta de producción mientras falta la consulta.

## Contrato candidato para aprobación

`GET /aportes/obligaciones/{obligacionId}` autenticado, sin importe ni identificadores personales en query. Respuesta acotada al titular autorizado, con al menos `obligacionId`, `estado`, `montoPendiente` como `Dinero` decimal **cadena + moneda**, `fechaVencimiento`, y una versión/ETag o marca de lectura para explicar cambios entre revisión y POST. Definir expresamente si recargo, comisión y monto a pagar son campos separados o parte de `montoPendiente`; no sumarlos en Flutter. El cliente no debe inferir el importe a partir de `porAportar` agregado ni de una query.

Decisiones pendientes de Aportes/Seguridad:

1. Titularidad exacta: cómo se vinculan sesión, usuario, participante y obligación. `@Permiso("BILLETERA_VER")` por sí solo no prueba pertenencia a la obligación. Un ID ajeno no puede filtrar saldo, grupo ni existencia de la obligación; definir 403/404 según política anti-enumeración.
2. Estados pagables: qué hacer con pendiente parcial, mora/recargo, período cerrado, PAGADO, ANULADO y pago en vuelo. La respuesta debe explicar si «Aportar» está disponible y por qué no, sin confiar únicamente en lógica móvil.
3. Concurrencia: GET puede quedar obsoleto. El POST debe seguir validando importe, estado y versión **en transacción**, con la misma clave de idempotencia ante timeout/doble toque/app kill. Definir la respuesta cuando cambió la obligación y un GET de reconsulta antes de intentar otra vez.
4. Resultado: `201`/`200` idempotente, 409/422 y 5xx/timeout no deben mostrarse como éxito falso; la app necesita consulta de estado para una operación de resultado incierto antes de generar otra intención de pago.
5. Límites de privacidad: no poner importes, referencias ni datos de participantes en enlaces, analytics o logs de cliente. Capturas de QA solo con datos sintéticos.

## Pruebas que habilitan el flujo

- Contrato OpenAPI + cliente Dart generado: misma obligación/moneda/decimal del servidor, 401/403/404 y estados no pagables.
- Backend TEST con titular, participante ajeno y obligación inexistente; confirmar autorización sin filtración de datos. Comparar GET con el POST bajo cambio concurrente y mora.
- E2E de CU-21 en Android/iOS: abrir enlace solo con `obligacionId`, mostrar importe exacto, revisión, doble toque, 409/422, timeout/503, reabrir la app y reintentar con clave conservada. Probar asientos, cuadre, reversa y redondeo de regla 91.6 antes de liberar dinero real.
- Accesibilidad, estados de carga/error/offline, texto 200 %, TalkBack/VoiceOver y capturas claro/oscuro en dispositivo. Sin esa evidencia H7.S1.M4 continúa **A MEDIAS**.

Hasta aprobar e implementar el contrato, mantener `PantallaAporteNoDisponible` en la ruta. La existencia de un GET agregado o del repositorio interno **no** justifica reactivar el pago.
