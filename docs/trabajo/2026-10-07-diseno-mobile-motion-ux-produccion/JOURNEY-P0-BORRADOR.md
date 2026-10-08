# Journey P0 — borrador contrastado con código

Estado: **para revisión de Producto/UX/Cumplimiento**. No es research con personas ni una aprobación de H4.S1.M1. Fuente: `PasanakuFrontend` `94b44bf`, rutas y pantallas Flutter; las dudas de la columna «a validar» son hipótesis, no hallazgos de usuarios.

| Momento y acción primaria visible | Intención de la persona | Duda a validar con personas | Dato solicitado/mostrado | Riesgo y salida observable en código |
|---|---|---|---|---|
| Portada → crear cuenta o ingresar | Entender si AportaYa le sirve y elegir camino | ¿Comprende custodia y diferencia entre tour y alta? | Ningún dato personal | `pantalla_portada.dart` separa las dos salidas y permite texto grande; el tour es opcional. |
| Alta → datos y contraseña | Abrir cuenta sin perder progreso | ¿Sabe por qué se piden estos datos y cuánto tarda? | Identidad, contacto y contraseña | `pantalla_registro.dart` muestra progreso; el borrador cifrado expira a 24 h y excluye contraseña. Requiere aprobación de privacidad. |
| Confirmar celular | Demostrar control del número | ¿Entiende por qué al volver debe verificar de nuevo? | Teléfono y código temporal | `estado_alta.dart`/`borrador_de_alta.dart`: OTP no se persiste; el retorno vuelve a verificación. |
| Capturar documento y prueba de vida | Completar expediente sin quedar atrapado por permisos | ¿Distingue alternativa documental de prueba de vida obligatoria? | Fotos de documento y rostro | `paso_captura.dart`: denegación de cámara tiene alternativa para documento; no se inventa un bypass de prueba de vida. Las copias temporales se eliminan tras intento de subida. |
| Cotejo, actividad y contrato | Revisar datos y consentir condiciones reales | ¿Detecta un dato equivocado antes de enviar? | Datos cotejados, perfil transaccional, aceptación contractual | `pantalla_registro.dart`: pasos separados; contrato vigente llega de backend, no texto inventado. El alta aceptada borra borrador. |
| Resultado de alta → ingreso/MFA | Saber si la cuenta existe y qué falta | ¿Interpreta «fotos pendientes» sin volver a registrarse? | Estado del expediente; credenciales en ingreso | `aviso_alta.dart` distingue cuenta creada de fotos no enviadas y orienta a soporte. No hay reenvío automático verificado. |
| Portada de billetera | Saber saldo y siguiente acción | ¿Entiende diferencia entre saldo, movimientos y obligaciones? | Saldo/movimientos del servidor | `pantalla_de_saldo.dart` usa estados de carga/vacío/error; no existe aún una prueba de tarea con usuarios. |
| Aporte → revisar monto, canal y referencia | Pagar una vez el período correcto | ¿Sabe de dónde sale el monto y qué referencia copiar? | Monto, canal, referencia | `pantalla_aportar.dart` bloquea monto ausente, cero o inválido; un monto positivo sigue llegando por query en `rutas.dart` y el cliente no tiene GET contractual de obligación. **Bloqueo de producción:** el monto debe leerse/verificarse contra fuente backend antes de confirmar. |
| Enviando/reintentando aporte | Saber si puede volver a tocar sin duplicar | ¿Entiende el resultado si se corta la conexión o se cierra la app? | Clave de idempotencia y huella SHA-256 de los datos, en almacén seguro | `cu21_cobrar_aporte.dart`/`clave_persistida_de_aporte.dart`: clave guardada antes del POST, reutilizada tras reinicio; un payload cambiado no se reenvía. Falta E2E con backend TEST y consulta de estado de la operación. |
| Resultado del aporte | Distinguir registrado de confirmado por el medio de pago | ¿Puede verificar qué pasó después, sin llamar a soporte? | Respuesta `SalidaCobro` | `confirmacion_aporte.dart` explica que la obligación se actualizará cuando el medio confirme. Falta comprobante/estado consultable y prueba de comprensión. |
| Entrega/cobro de turno | Conocer bolsa, deducciones y neto antes de aceptar | ¿Detecta una deducción inesperada? | Bolsa, descuentos, neto, destino | `rutas.dart` declara que no hay GET contractual para la vista de entrega; no existe pantalla real conectada. **Bloqueo P0**, no se sustituye por mock. |

## Decisiones pendientes antes de aprobar H4.S1.M1

1. Producto y UX validan este orden y la acción primaria de cada momento mediante un recorrido moderado, no solo leyendo el código.
2. Backend publica y prueba un GET de obligación/monto autoritativo y el estado/recibo de un aporte; el cliente deja de confiar en el parámetro `monto` de la ruta.
3. Cumplimiento valida explicación de custodia, datos biométricos, contratos, fotos pendientes y diferencia entre «registrado» y «confirmado».
4. Research prepara participantes y consentimiento, registra comprensión, abandono y recuperación sin PII ni importes en telemetría; H4.S1.M2–M4 permanecen pendientes.

La skill de claridad UX motivó separar intención, acción única, feedback y recuperación en cada momento. Las dudas siguen siendo hipótesis hasta contrastarlas con personas.
