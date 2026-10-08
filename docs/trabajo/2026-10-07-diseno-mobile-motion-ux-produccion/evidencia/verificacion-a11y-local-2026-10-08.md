# Accesibilidad automatizada P0: alta recuperada, aporte bloqueado y portada

Frontend [`da439f9`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/da439f9), [`78e2363`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/78e2363) y [`ee91cb8`](https://github.com/PabloArauzCaballero/PasanakuFrontend/commit/ee91cb8) · Flutter 3.44.8 en Windows. H8.S1.M1 permanece **EN CURSO**.

## Alcance y resultado

Se añadieron pruebas widget con pantalla de 360×760 y escala de texto 200 %, tanto en claro como en oscuro:

| Vista | Estados recorridos | Comprobaciones |
|---|---|---|
| Alta recuperada | Paso de celular tras restaurar borrador sintético; volver hasta datos y desplazar al selector SMS/correo. | `androidTapTargetGuideline`, `labeledTapTargetGuideline`, `textContrastGuideline`, sin excepción de layout. |
| Aporte bloqueado | Estado explícito sin importe verificado y salida a Ayuda. | Las mismas tres guías, sin excepción de layout. |
| Portada de bienvenida | Crear cuenta e ingresar, en claro/oscuro. | Objetivos táctiles y etiquetas; contraste WCAG AA calculado para título y cuerpo contra el fondo; sin excepción de layout. El logotipo se expone como imagen semántica y no se somete a la guía de contraste de texto. |

```text
flutter test --no-pub test/a11y/alta_reanudada_a11y_test.dart --reporter expanded
00:00 +2: All tests passed!
flutter test --no-pub test/a11y/aporte_bloqueado_a11y_test.dart --reporter expanded
00:00 +2: All tests passed!
flutter test --no-pub test/a11y/portada_a11y_test.dart --reporter expanded
00:00 +2: All tests passed!
flutter test --no-pub test/a11y test/contrato test/identidad test/pasanaku test/unidad test/widget --reporter compact
00:22 +321: All tests passed!
flutter analyze --no-pub
No issues found!
```

La guía de contraste de píxeles dio un falso positivo en oscuro al comparar entre sí los dos colores del logotipo, en vez de comparar cada uno con el fondo. El logotipo es una imagen con etiqueta «AportaYa»; WCAG 1.4.3 exime logos. La prueba no silencia ningún fallo de título/cuerpo: calcula sus ratios a partir de los tokens reales y exige ≥4,5:1 en ambos temas. Esto no reemplaza inspección visual en dispositivo.

Los datos del borrador son sintéticos («Demo Prueba»). Estas guías automatizadas no prueban orden de foco, anuncios, gestos ni comprensión con TalkBack/VoiceOver, y la prueba de aporte monta el estado UI con un adaptador HTTP simulado; tampoco prueba backend ni un cobro real. Las [capturas inspeccionadas del alta](./verificacion-alta-reanudada-2026-10-08.md) y del [aporte bloqueado](./verificacion-ruta-aporte-bloqueada-2026-10-08.md) son evidencia visual local separada. Falta recorrido manual en Android/iOS, permisos, teclado real y lector de pantalla antes de cerrar H8.S1.M1.

El [CI de `78e2363`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37728231974) no inició ningún paso: la anotación de GitHub vuelve a señalar facturación/límite de gasto; Flutter/macOS/iOS quedaron omitidos.

El [CI de `ee91cb8`](https://github.com/PabloArauzCaballero/PasanakuFrontend/actions/runs/37728565427) repitió el mismo bloqueo: el job terminó con cero pasos y la anotación literal «The job was not started because recent account payments have failed or your spending limit needs to be increased». No hay validación remota de este commit.
