# Decisión pendiente — titular autorizado para declaración PEP

- Fecha: 2026-10-08. Contención frontend: `f0ccfb0` en PR #15.
- Responsables: Identidad, Cumplimiento, Seguridad y Producto.
- Estado: **flujo real pendiente de identidad/autorización y backend TEST**.

## Contratos y defecto observado

El contrato de Cumplimiento sí define `POST /cumplimiento/usuarios/{usuarioId}/pep` (`declararPep`, CU-03), con `EntradaPep` y respuesta que informa la recalificación. Requiere un `usuarioId` UUID y una sesión autorizada. La respuesta de `POST /sesiones` (`SalidaAutenticacion` en Identidad) entrega sesión/token/factor, pero **no** el identificador de usuario. La app móvil no dispone de un vínculo autenticado y verificable entre sesión y `usuarioId` para construir la ruta.

La antigua pantalla `/identidad/verificacion-profunda` pedía la declaración y “Continuar” solo escribía `PepNotifier` en memoria; no llamaba a Cumplimiento ni persistía. A 320 px/texto 200 % también desbordaba. La consulta `GET /usuarios/por-telefono` no es una solución de identidad del titular: está definida para invitaciones, exige permiso, expone teléfono en query y puede permitir enumeración. Tampoco un UUID de enlace demuestra titularidad. No se conectó el endpoint con ninguno de esos atajos.

## Contención y desbloqueo

La ruta conserva un aviso claro y salida a Perfil, sin pedir datos ni afirmar que se presentó una declaración. Se retiró el estado local PEP sin consumidor. Esto evita una confirmación falsa; **no implementa CU-03**.

Para habilitarlo, Identidad/Seguridad deben definir cómo obtiene la app el `usuarioId` propio desde una sesión autenticada y cómo Cumplimiento verifica esa titularidad/rol en el endpoint. Cumplimiento/Producto deben aprobar el formulario completo de `EntradaPep` (incluidos beneficiarios finales), el copy y el tratamiento de reenvíos/errores. Luego hay que probar 200/401/403/422, persistencia/relectura, cambios de riesgo y datos sintéticos en backend TEST, además del recorrido Android/iOS y accesibilidad manual. Hasta contar con esas pruebas, no exponer el formulario como operativo.
