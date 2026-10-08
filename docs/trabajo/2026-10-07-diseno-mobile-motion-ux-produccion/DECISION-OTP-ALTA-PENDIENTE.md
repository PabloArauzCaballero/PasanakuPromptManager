# Decisión pendiente: secuencia y contrato OTP del alta

Estado: **propuesta para Producto, Identidad y Seguridad; no aprobada**. Bloquea H7.S1.M2 y el merge de [frontend PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15). El cliente quedó fail-closed en [`c541551`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/c541551): no simula un envío ni permite avanzar con seis dígitos arbitrarios.

Actualización 2026-10-08: existe una **implementación candidata, no integrada ni aprobada**, en [`PasanakuBackend/pablo/feature/verificacion-correo-gmail-test` (`59370bbd`)](https://github.com/PabloArauzCaballero/PasanakuBackend/tree/pablo/feature/verificacion-correo-gmail-test), con el commit de OTP [`2f1101f3`](https://github.com/PabloArauzCaballero/PasanakuBackend/commit/2f1101f3e4970086505caae1ec460aba9c0e3373). Propone la opción A para **correo**: solicitar/confirmar un challenge antes del alta y enviar `verificacionCorreoId` en `POST /usuarios`. La verificación de refs mostró `otp_feature_in_dev=False` y `otp_feature_in_main=False`; `gh pr list --state all --head pablo/feature/verificacion-correo-gmail-test` no devolvió PR. Esto no demuestra despliegue TEST, aprobación de Producto/Seguridad ni cobertura SMS. [Auditoría de dependencias y límites](./evidencia/auditoria-dependencias-2026-10-08.md).

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

La rama candidata materializa A para correo, pero todavía no se aprobó ni se fusionó. No se debe elegir una opción solo por el costo técnico: la política de cuándo recopilar documento/contraseña/consentimientos y cuándo crear una cuenta corresponde a Producto, Identidad y Seguridad.

## Contrato mínimo que cualquiera de las dos opciones debe resolver

1. Destino y propósito vinculados: un OTP de correo no verifica teléfono; un cambio de destino invalida el challenge anterior.
2. Emisión y reenvío reales con estado honesto: respuesta con destino enmascarado, vencimiento y plazo de reenvío; nunca devolver el OTP en claro al cliente. Fracaso de proveedor de entrega no puede mostrarse como «enviado».
3. Validación en servidor, consumo único, expiración, límite de intentos, rate limit por destino/dispositivo/IP y respuesta resistente a enumeración de cuentas. Hash del token en reposo; sin OTP, destino completo ni prueba opaca en URL, logs, analytics o capturas.
4. Evidencia de verificación ligada a la **misma** persona/destino/operación idempotente de alta; no basta un booleano local ni seis dígitos con forma válida.
5. Semántica explícita para timeout, app kill, reenvío, código errado/vencido, canal no disponible y doble toque. En cada caso la UI debe poder preguntar al servidor si se confirmó antes de repetir una operación irreversible.
6. Estados separados en backend: contacto confirmado, KYC/diligencia, cuenta de billetera creada y habilitación para operar. `202 PENDIENTE_VERIFICACION` por sí solo no cubre los cuatro.
7. Pruebas contractuales y E2E en TEST de SMS/correo, expiración, reenvío, intentos agotados, replay, cambio de destino, duplicado idempotente, corte de red y reapertura de app. Verificar que el cliente generado y la UI muestran el estado **real** y no avanzan ante un 4xx/5xx.

## Siguiente implementación, después de la decisión

Revisar y aprobar o rechazar la rama candidata de correo; si se aprueba, integrarla en la rama canónica y desplegarla en TEST antes de basar el frontend de producción en ella. Generar cliente Dart desde el contrato integrado; integrar el paso de verificación con challenge/respuesta reales; adaptar borrador/reanudación sin persistir OTP ni pruebas sensibles; ejecutar tests con backend TEST y dispositivos Android/iOS. Si Producto exige SMS además de correo, definir su proveedor/contrato y pruebas antes de habilitarlo. Solo entonces reabrir la continuación y evaluar H7.S1.M2 como HECHO. Hasta esa evidencia, mantener el bloqueo actual y el PR frontend sin merge de producción.
