# Cuenta de billetera: contención sin UUID inventado — `cbca157`

El login navega a `/billetera/inicio` sin `cuenta`; antes las rutas de inicio, recarga, retiro, transferencia y extracto asignaban el UUID fijo `11111111-1111-4111-8111-111111111111`. El contrato de autenticación devuelve sesión/token, no `cuentaId`, y el contrato financiero solo expone `GET /billetera/{cuentaId}/saldo`, no una consulta de cuentas de la persona autenticada. Usar un ID fijo para todas las personas no es un fallback seguro.

En `cbca157` esas cinco rutas validan la forma del ID; si falta o es malformado, muestran un estado con salida a Ayuda y no crean el provider financiero. Diez pruebas (cinco rutas × ausente/malformado) comprueban cero peticiones con Dio simulado; otras prueban navegación a Ayuda, conservación de la vista de saldo con UUID explícito y texto al 200 % en tema oscuro. **La validación de forma no autoriza una cuenta ajena**; la API debe comprobar titularidad. La cuenta explícita usada en la prueba es solo sintética.

| Verificación local en Windows / Flutter 3.44.8 | Resultado |
|---|---|
| Suite no-golden (`test/a11y`, `contrato`, `identidad`, `pasanaku`, `unidad`, `widget`) | **271 PASS, 0 FAIL** |
| `flutter analyze --no-pub --fatal-infos` | Sin issues |
| `python -X utf8 scripts/verificar_frontend.py movil` | `TODO OK` |
| `flutter build apk --debug --no-pub --dart-define=API=http://10.0.2.2:4010/api/v1` | APK construido |
| Goldens (`test/goldens`) | **4 PASS, 3 FAIL**: saldo claro/oscuro y transición; sin actualizar snapshots |

No hubo inspección visual en dispositivo de este estado, ni ejecución iOS, ni E2E contra backend TEST. La UI de billetera queda deliberadamente no operativa tras login hasta que backend/Producto definan y prueben un GET autorizado para resolver la cuenta de la sesión. Es un bloqueo P0 y **no** un release candidate. GitHub Actions continuó fallando en pocos segundos por el bloqueo de facturación de la cuenta, con Flutter/macOS/iOS omitidos; PR #15 permanece abierto.
