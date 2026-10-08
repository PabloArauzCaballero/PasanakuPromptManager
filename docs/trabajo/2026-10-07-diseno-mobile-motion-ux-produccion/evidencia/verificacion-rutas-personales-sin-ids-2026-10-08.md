# Rutas personales sin IDs de URL — 2026-10-08

Código frontend: [`0a3191d`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/0a3191daf45c77c8acd872bbcb66ae07f210251f), PR #15.

## Qué cambió

`/pasanaku/mi-estado` y `/pasanaku/mi-puntaje` aceptaban `participante` y `usuario` por query y pedían al servidor el estado de deuda/restricción o el puntaje de ese ID. La query no acredita que corresponda a la persona autenticada y expone IDs personales en historiales y registros de enlaces.

Ambas rutas ahora descartan toda query y no hacen consultas personales a partir de ella. «Mi estado» conserva el estado seguro de participación no identificada; «Mi puntaje» tiene un estado equivalente con texto claro y salida a Ayuda. Esta es una **contención**, no el flujo personal terminado. Para reactivarlos hace falta que la identidad autenticada determine la participación y el usuario mediante un contrato de lectura `me`/titularidad, sin confiar en la URL.

## Hallazgo backend que requiere validación prioritaria

Revisión estática en el corte `0a3191d`, **sin prueba de explotación contra PostgreSQL real**:

1. `AportesController.consultarEstadoDelParticipante` exige `BILLETERA_VER` y pasa el `participanteId` de la ruta a `ConsultarEstadoDelParticipante.ejecutar`; no se observa en esas dos capas una comparación con el sujeto de `SesionDeLaPeticion`.
2. `EstadoDelParticipanteRepositorio.de` agrega `aportes.obligacion_aporte` usando `WHERE o.participante_id = ?` y devuelve importes de deuda/aporte.
3. `obligacion_aporte.sql` no tiene `usuario_id` ni `cuenta_billetera_id`. La función genérica `fn_seg_aplicar_rls()` de `restricciones.sql` recorre solo tablas con una de esas columnas. La búsqueda de políticas explícitas para `obligacion_aporte` no encontró otra.

Esto hace **plausible** que una sesión con permiso `BILLETERA_VER` consulte importes de otra participación si conoce su UUID. No se debe declarar vulnerabilidad confirmada ni corregida solo con la contención móvil: hay que probar con dos usuarios, el rol de servicio y filas reales en PostgreSQL; luego imponer titularidad en el servicio y/o política de filas específica, con prueba positiva/negativa automatizada. La autorización de cambiar contratos/reglas backend y la decisión del vínculo usuario↔participante aún están pendientes.

## Pruebas de cliente y evidencia visual

- Cuatro pruebas de enlaces adulterados, dos rutas × claro/oscuro a 360×760 y texto al 200 %, verifican query eliminada, cero peticiones, aviso y navegación a Ayuda tras desplazar el CTA.
- App **342/342** pruebas no-golden y **10/10** goldens nuevos de pantalla (cinco de turno, cinco de puntaje); analizadores de app y diseño sin hallazgos, diseño **54/54** pruebas dirigidas, APK debug PASS.
- [CI del commit](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37733822065): jobs iniciales rechazados antes de ejecutarse por facturación de GitHub Actions; Flutter/macOS/iOS omitidos. PR frontend sin merge.
- Capturas de widget Flutter en Windows con datos sintéticos; los goldens nuevos solo se comparan allí. En Mac crear referencias propias tras inspección; no equivalen a capturas Android/iOS ni a prueba de lector de pantalla.

| Celda de puntaje | Captura | Inspección |
|---|---|---|
| Móvil 360×760, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/0a3191daf45c77c8acd872bbcb66ae07f210251f/apps/movil/test/goldens/imagenes/puntaje_sin_identidad_360_claro.png) | Mensaje y CTA visibles, sin puntaje ajeno. |
| Móvil 360×760, oscuro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/0a3191daf45c77c8acd872bbcb66ae07f210251f/apps/movil/test/goldens/imagenes/puntaje_sin_identidad_360_oscuro.png) | Jerarquía/contraste coherentes. |
| Móvil 360×760, texto 200 %, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/0a3191daf45c77c8acd872bbcb66ae07f210251f/apps/movil/test/goldens/imagenes/puntaje_sin_identidad_360_texto_200_claro.png) | Texto completo, CTA visible. |
| Móvil 360×760, texto 200 %, oscuro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/0a3191daf45c77c8acd872bbcb66ae07f210251f/apps/movil/test/goldens/imagenes/puntaje_sin_identidad_360_texto_200_oscuro.png) | Texto completo, sin overflow. |
| Tablet 768×1024, claro | [PNG](https://github.com/PabloArauzCaballero/PasanakuFrontend/blob/0a3191daf45c77c8acd872bbcb66ae07f210251f/apps/movil/test/goldens/imagenes/puntaje_sin_identidad_768_claro.png) | Estado centrado y legible. |

El conteo DoD permanece **11/41 HECHO**. H8.S1.M6 sigue EN CURSO: la superficie móvil ya no acepta esos IDs, pero faltan validación y corrección de servicio, payloads TEST, Android/iOS y aprobación de Seguridad/Cumplimiento.
