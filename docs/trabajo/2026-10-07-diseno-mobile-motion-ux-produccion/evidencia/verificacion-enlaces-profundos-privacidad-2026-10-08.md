# Enlaces de invitación sin datos externos en la ruta interna

El traductor de enlaces `aportaya://` ya no convierte segmentos decodificados sin validarlos en una ruta de navegación. Esto evita que texto de un enlace externo, incluida una secuencia codificada como `%3F`, termine interpretándose como parámetros internos. El cambio está en `PasanakuFrontend` `1c85b42`, publicado en [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).

## Defecto y corrección

La prueba roja reprodujo que `aportaya://unirse/ABC%3Fdocumento%3DCI_FICTICIA` producía `/pasanaku/unirse/ABC?documento=CI_FICTICIA`: `Uri.pathSegments` ya había decodificado `%3F` y el traductor reunía los segmentos sin validar. Ahora el enlace de invitación solo admite un segmento con el identificador y secreto firmados en el formato compartido con el retorno posterior al ingreso. Un enlace de invitación malformado lleva a `/pasanaku/unirse/invalida`; su pantalla explica el problema y ofrece **Ir a portada**. Otros hosts/rutas inesperados llevan a `/enlace-no-valido`. La query externa no se copia. La guardia de sesión conserva en `volver` solo una invitación válida; para cualquier otra ruta usa `/ingreso` sin retorno arbitrario.

## Verificación local del corte

- Tests unitarios y de widget dirigidos: **18/18 PASS**, incluidos parámetros codificados, host/ruta inesperados, retorno de ingreso y salida de enlace inválido.
- Suite no-golden de `apps/movil` (`test/unidad`, `test/widget`, `test/contrato`, `test/identidad`, `test/pasanaku`, `test/a11y`): `success: true` en Windows con Flutter 3.44.8.
- Goldens nuevos de enlace inválido: **3/3 PASS** a 320×760 en claro y oscuro con texto 200 %, y 768×1024 claro con texto 100 %. Las tres imágenes se inspeccionaron: mensaje y acción visibles, sin desbordamiento ni datos personales. Están versionadas bajo `apps/movil/test/goldens/imagenes/`.
- `flutter analyze --no-pub`, `python scripts/verificar_frontend.py movil`, `git diff --check` y `flutter build apk --debug --no-pub`: **PASS**. El verificador exigió extraer la acción de error a un widget para mantener la pantalla en 200 líneas.

## Límite de la evidencia y siguiente gate

La matriz visual es sintética de Windows, no una prueba de enlace entrante en Android/iOS ni una auditoría de logs, analytics o capturas reales. En Mac, repetir los tests y comparar los goldens con el rasterizado macOS; después abrir un enlace válido e inválido en ambos sistemas y revisar la ruta, el retorno y la telemetría. Seguridad/Cumplimiento debe revisar los payloads y los datos observables en backend TEST antes de cerrar H8.S1.M6. El avance formal continúa **18/49 HECHO**. El PR frontend no se fusiona mientras sus checks obligatorios sigan sin ejecutarse por el bloqueo de GitHub Actions.
