# Decisión pendiente — gestiones de cuenta desde la app

- Fecha: 2026-10-08. Código de contención: `PasanakuFrontend` `5e2a544` (PR #15).
- Dueños de la decisión: Producto, Identidad/backend, Seguridad y Legal/Cumplimiento.
- Estado: **BLOQUEADO por contrato y servicio**, no implementado como gestión real.

## Hecho comprobado

El OpenAPI de Identidad (`servicios/identidad/src/main/resources/openapi/identidad.yaml`) define alta, sesión, verificaciones y consultas puntuales, pero no una operación para actualizar correo, cambiar contraseña, listar/confiar/revocar dispositivos ni solicitar/cerrar cuenta. Las pantallas anteriores cambiaban únicamente estado local o cerraban un diálogo: podían hacer creer que una solicitud se había ejecutado. La casilla de confianza tampoco viajaba en la autenticación.

La copia del contrato mostrada por la app (`apps/movil/lib/pantallas/identidad/texto_del_contrato.dart`, sección de cierre de cuenta) afirma que el titular puede cerrar su cuenta desde la app. Eso no coincide con la capacidad técnica actual. **No se cambió el texto legal sin aprobación**; Legal/Producto deben decidir su corrección y el canal operativo vigente. El catálogo `/soporte/ayuda` contiene tutoriales, no un canal demostrado para tramitar una baja. No se debe presentarlo como tal.

## Contención implementada

Perfil, contraseña, baja y dispositivos muestran indisponibilidad explícita; no solicitan datos, no confirman una operación falsa ni envían llamadas. Cerrar sesión sigue siendo funcional. El tutorial de cuidado de cuenta ya no promete gestiones ausentes. Al autenticar, el estado local borra teléfono, contraseña y código MFA; durante el desafío retiene temporalmente lo exigido por el contrato de `/sesiones`.

## Decisiones y pruebas para desbloquear

1. Producto/Legal: fijar qué puede prometerse y cuál es el canal real para ejercer derechos y cerrar cuenta mientras no exista autoservicio; aprobar la copia legal y de UX. No afirmar que el derecho desaparece porque la app carece de endpoint.
2. Identidad/Seguridad: versionar contratos autorizados para cada gestión, con reautenticación/MFA según riesgo, auditoría, idempotencia donde proceda y semántica clara de solicitudes frente a efectos completados.
3. Backend TEST: probar autorización de titular, errores, persistencia y relectura. Luego implementar cliente y UI; cubrir éxito, carga, error, offline, doble toque y continuidad.
4. QA: validar en Android e iOS reales, texto 200 %, lectores de pantalla, capturas sin datos personales y regresión de cierre de sesión.

Hasta entonces, estas gestiones **no son funciones terminadas** y bloquean el cierre del vertical slice de producción.
