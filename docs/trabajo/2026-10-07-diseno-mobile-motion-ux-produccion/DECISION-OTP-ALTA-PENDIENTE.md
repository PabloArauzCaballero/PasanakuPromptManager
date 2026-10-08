# Decisión pendiente: secuencia y contrato OTP del alta

Estado: **propuesta para Producto, Identidad y Seguridad; no aprobada**. Bloquea H7.S1.M2 y el merge de [frontend PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). El cliente quedó fail-closed en [`c541551`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/c541551): no simula un envío ni permite avanzar con seis dígitos arbitrarios.

## Evidencia del contrato actual

- [`servicios/identidad/src/main/resources/openapi/identidad.yaml`](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/dev/servicios/identidad/src/main/resources/openapi/identidad.yaml) declara `POST /usuarios` público y `EntradaRegistro` sin código, challenge ID ni prueba de contacto. Responde `202 PENDIENTE_VERIFICACION`; no expone una ruta de emisión/validación OTP para este alta. Los endpoints de token publicados son de **invitación de grupo**, no de contacto de registro.
- [`CU01RegistrarUsuario.java`](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/dev/servicios/identidad/src/main/java/bo/aportaya/identidad/aplicacion/CU01RegistrarUsuario.java) crea usuario, credencial, documento y consentimientos y emite `identidad.usuario_registrado`. Comprueba que exista correo si se eligió ese canal, pero no emite ni valida el token del contacto.
- `CanalDeVerificacion` y las políticas sembradas `VERIFICACION_TELEFONO`/`VERIFICACION_CORREO` distinguen SMS de correo. `token_verificacion` tiene hash, expiración, intentos y reenvíos; la tabla y la política son **infraestructura posible**, no una prueba de que el flujo esté implementado.
- `PENDIENTE_VERIFICACION` en el alta no demuestra posesión del teléfono/correo: el código actual también espera diligencia y apertura asíncrona de billetera. No debe interpretarse como OTP validado.

## Decisión que falta

Producto/Identidad/Seguridad deben elegir una secuencia **antes de mover el paso móvil**:

| Opción | Contrato a aprobar | Trade-off principal |
|---|---|---|
| A · Verificar antes de `POST /usuarios` | Challenge público de propósito `VERIFICACION_TELEFONO` o `VERIFICACION_CORREO`; validación server-side; `POST /usuarios` acepta una prueba opaca, vinculada al destino y consumida una vez en la misma operación idempotente. | Evita crear cuentas sin contacto confirmado; exige un challenge previo sin usuario y cambio de `EntradaRegistro`. |
| B · Registrar en pendiente y verificar después | `POST /usuarios` mantiene el `202` actual; devuelve una capacidad de verificación de alcance limitado; operaciones posteriores envían/validan el OTP y solo entonces el servidor marca el contacto confirmado. La UI mueve el paso OTP después del alta y no promete billetera operable mientras siga pendiente. | Alinea la secuencia con el backend existente, pero exige retención/limpieza de cuentas pendientes y una capacidad segura para verificar sin sesión plena. |

La opción B parece requerir menos cambio en el orden transaccional existente; **es una inferencia técnica, no una aprobación de Producto ni Seguridad**. No se debe elegir solo por ese costo: la política de cuándo recopilar documento/contraseña/consentimientos y cuándo crear una cuenta puede decidir A.

## Contrato mínimo que cualquiera de las dos opciones debe resolver

1. Destino y propósito vinculados: un OTP de correo no verifica teléfono; un cambio de destino invalida el challenge anterior.
2. Emisión y reenvío reales con estado honesto: respuesta con destino enmascarado, vencimiento y plazo de reenvío; nunca devolver el OTP en claro al cliente. Fracaso de proveedor de entrega no puede mostrarse como «enviado».
3. Validación en servidor, consumo único, expiración, límite de intentos, rate limit por destino/dispositivo/IP y respuesta resistente a enumeración de cuentas. Hash del token en reposo; sin OTP, destino completo ni prueba opaca en URL, logs, analytics o capturas.
4. Evidencia de verificación ligada a la **misma** persona/destino/operación idempotente de alta; no basta un booleano local ni seis dígitos con forma válida.
5. Semántica explícita para timeout, app kill, reenvío, código errado/vencido, canal no disponible y doble toque. En cada caso la UI debe poder preguntar al servidor si se confirmó antes de repetir una operación irreversible.
6. Estados separados en backend: contacto confirmado, KYC/diligencia, cuenta de billetera creada y habilitación para operar. `202 PENDIENTE_VERIFICACION` por sí solo no cubre los cuatro.
7. Pruebas contractuales y E2E en TEST de SMS/correo, expiración, reenvío, intentos agotados, replay, cambio de destino, duplicado idempotente, corte de red y reapertura de app. Verificar que el cliente generado y la UI muestran el estado **real** y no avanzan ante un 4xx/5xx.

## Siguiente implementación, después de la decisión

Actualizar OpenAPI y backend de Identidad; generar cliente Dart; integrar `PasoCelular` con el challenge y la respuesta real; adaptar borrador/reanudación sin persistir OTP ni pruebas sensibles; ejecutar tests con backend TEST y dispositivos Android/iOS. Solo entonces reabrir el botón de continuación y evaluar H7.S1.M2 como HECHO. Hasta esa evidencia, mantener el bloqueo actual y el PR frontend sin merge de producción.
