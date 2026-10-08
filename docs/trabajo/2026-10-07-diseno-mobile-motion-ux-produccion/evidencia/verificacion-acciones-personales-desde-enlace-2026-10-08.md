# Acciones personales no autorizadas por un enlace — 2026-10-08

- Código: `PasanakuFrontend` `6f8ecf0`, [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15).
- Riesgo observado: las rutas de crear grupo con `organizador`, retiro con `participante` y permuta con IDs de turnos/contraparte recibían estos IDs de la URL y ofrecían operaciones sin que el cliente pudiera derivar la titularidad de la sesión. Un UUID en un enlace no es autorización; tampoco se concluye con esto que el backend sea explotable.
- Contención: las tres entradas muestran estado persistente y Ayuda sin formulario ni petición. Crear grupo sin query sigue con su recorrido anterior. No se inventó endpoint ni identidad de sesión.

## Evidencia literal

```text
flutter test --no-pub test/pasanaku/rutas_acciones_personales_sin_titular_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart
00:01 +9: All tests passed!

flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget test/goldens/bienvenida_sin_sesion_golden_test.dart test/goldens/accion_personal_no_disponible_golden_test.dart test/goldens/conexion_operaciones_golden_test.dart test/goldens/gestiones_cuenta_no_disponibles_golden_test.dart test/goldens/verificacion_profunda_sin_usuario_golden_test.dart test/goldens/mfa_estados_golden_test.dart test/goldens/aporte_offline_golden_test.dart test/goldens/billetera_offline_golden_test.dart test/goldens/turno_sin_confirmar_golden_test.dart test/goldens/puntaje_sin_identidad_golden_test.dart --reporter compact
00:27 +481: All tests passed!

flutter analyze --no-pub
No issues found! (ran in 2.1s)

python -X utf8 scripts/verificar_frontend.py movil
TODO OK

flutter build apk --debug --no-pub
√ Built build\app\outputs\flutter-apk\app-debug.apk
```

Los seis tests de rutas corren a 320×760, texto 200 %, claro/oscuro y comprueban cero peticiones incluso después de tocar Ayuda. Tres goldens Windows (`accion_personal_bloqueada_*`) se abrieron e inspeccionaron a resolución original: título, explicación y CTA visibles sin recorte; en tablet el contenido queda limitado a 560 dp. Rúbrica visual local: 15/16 (tablet deliberadamente sobria). Las capturas y los IDs de los tests son sintéticos.

## Límites y continuación

- Esto es contención del cliente, no habilitación de CU-20/62/65 ni prueba de autorización del servidor. Falta un origen de organizador/participación/turnos autenticado y un E2E con dos usuarios, backend TEST y permisos reales. Es responsabilidad de backend autorizar cada petición independientemente del cliente.
- No hubo Android/iOS estable, TalkBack/VoiceOver ni trazas de red de un dispositivo. Los goldens Windows no son baseline de macOS.
- [CI de `6f8ecf0`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37748563391): jobs fallidos con `steps: []`; Flutter, goldens e iOS quedaron `SKIPPED`. [PR #15](https://github.com/PabloArauzCaballero/PasanakuFrontend/pull/15) continúa `UNSTABLE` y sin merge. No se declara listo para producción.
