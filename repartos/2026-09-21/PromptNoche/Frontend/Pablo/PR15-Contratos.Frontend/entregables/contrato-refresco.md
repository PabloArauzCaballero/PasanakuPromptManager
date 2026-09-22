# Contrato real del refresco de sesión — H2.S2.M2

**Entregado a Richard (PR11-Sesion.Frontend).**

Verificado contra `servicios/identidad/src/main/resources/openapi/identidad.yaml` (2026-09-22):

- **No existe `POST /sesion/refrescar` ni ninguna operación de refresco** en el contrato real.
  El único endpoint de sesión es `POST /sesiones` (`operationId: autenticar`, CU-04, línea 60),
  que abre sesión desde cero — no renueva una existente.
- **El token de acceso viaja en el cuerpo JSON de la respuesta** (`SalidaAutenticacion.tokenAcceso`,
  línea 410), como un JWT firmado RS256 — **no en una cookie HttpOnly**. Confirmado leyendo el
  esquema completo: no hay ningún header `Set-Cookie` documentado en la respuesta de `/sesiones`.
- **No hay token de refresco** en el esquema (`SalidaAutenticacion` no tiene ningún campo
  `tokenRefresco`/`refreshToken` ni equivalente) — no hay nada que "rotar".

**Veredicto sobre la cookie:** el mecanismo de refresco por cookie que `PR11-Sesion.Frontend`
(Richard) implementa hoy está construido contra un contrato que **todavía no existe en el
backend real**. No es un error del carril de Richard — está simulado contra un doble en tres
niveles, como exige la regla 65, y así lo declara su propio trabajo. Esto solo confirma con el
contrato real que el doble es necesario, no que sobra.

Consistente con el hallazgo independiente del carril de Richard (`servicios/identidad no tiene
POST /sesion/refrescar en su contrato real`, entregable de esa sesión) — verificado dos veces
por dos caminos distintos, mismo resultado.
