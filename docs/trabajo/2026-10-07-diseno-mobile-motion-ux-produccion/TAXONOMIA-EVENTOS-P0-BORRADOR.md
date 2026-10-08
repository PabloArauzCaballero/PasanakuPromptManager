# Taxonomía P0 de medición — propuesta, no instrumentada

Estado: **EN CURSO**, pendiente de Data, Producto, Seguridad y Cumplimiento. Esta propuesta no crea un SDK, un endpoint ni un envío de datos. La búsqueda en `apps/movil/lib`, `apps/movil/test` y `apps/movil/pubspec.yaml` no encontró analytics o telemetría UX móvil. No hay fuente, destino, retención ni dueño aprobados; por eso H4.S1.M3 y H4.S1.M4 no están cerradas.

## Límite de privacidad

El evento candidato es anónimo y de cardinalidad cerrada. Su payload contiene **exactamente** `event`, `schema`, `flow`, `step` y `outcome`. No admite ID de persona, cuenta, grupo, obligación, operación o sesión; tampoco importe, moneda, documento, teléfono, QR, token, mensaje, texto libre, URL, hora del dispositivo ni propiedades adicionales. No se deriva un identificador persistente en el cliente. La prueba sintética [validar-eventos-p0.ps1](./validar-eventos-p0.ps1) falla cerrado ante campos o valores ajenos a la lista.

| Campo | Valores permitidos |
|---|---|
| `event` | `ux_p0_step` |
| `schema` | número entero `1` |
| `flow` | `alta`, `inicio`, `aporte` |
| `step` en `alta` | `inicio`, `datos`, `otp`, `documento`, `vida`, `contrato`, `resultado` |
| `step` en `inicio` | `portada`, `saldo`, `mi_estado` |
| `step` en `aporte` | `revision`, `envio`, `resultado` |
| `outcome` | `viewed`, `completed`, `abandoned`, `error`, `offline`, `uncertain` |

Ejemplo **sintético** permitido: `{"event":"ux_p0_step","schema":1,"flow":"alta","step":"otp","outcome":"completed"}`. Un `completed` en el cliente expresa únicamente que la UI avanzó: **no** confirma un aporte, la creación de una cuenta ni el estado de una obligación. La matriz de pasos es candidata y necesita revisión de nombres/semántica antes de introducir un emisor.

## Cálculo de los KPI primarios

El evento anónimo solo sirve para agregados de paso y errores de interfaz. No permite seguir a una persona ni unir soporte con pagos; por diseño, **ninguno de los tres KPI primarios se calcula con este evento solo**. La unión necesaria ocurre dentro de los sistemas autorizados, por sus dueños, y hacia un tablero salen únicamente contadores agregados con un umbral de grupo mínimo aprobado por Cumplimiento.

| KPI del plan | Numerador / denominador y ventana que deben aprobarse | Fuente autoritativa faltante | Dueño por confirmar |
|---|---|---|---|
| Activación comprendida | Cuentas que completan activación **y** llegan a portada / cuentas que inician activación; cohorte y ventana de llegada por definir. La llegada a portada requiere señal de producto asociable de forma interna, no un ID en analytics. | Identidad + definición de activación y llegada a portada | Producto, Identidad, Data |
| Éxito del primer aporte | Primeros aportes confirmados una sola vez / intentos elegibles iniciados; cohorte y plazo de confirmación por definir. El cliente nunca decide `confirmado`. | Obligaciones/cobro, mayor y webhook verificado; regla de elegibilidad | Producto, Pagos, Data |
| Resolución sin ayuda | Operaciones críticas completadas sin reintento ambiguo ni contacto de soporte en 24 h / operaciones críticas iniciadas; catálogo de operaciones y ancla de 24 h por definir. | Estado de operación, reintentos y contacto de soporte; unión interna autorizada | Producto, Soporte, Data |

No se fija meta porcentual ni baseline sin datos reales aprobados. Para `primer aporte` y `resolución`, un POST aceptado, un 200, un timeout o una pantalla de éxito no sustituyen el estado financiero/operativo autoritativo. Los denominadores deben excluir pruebas, duplicados idempotentes y eventos de retry según reglas aprobadas. El tablero debe mostrar numerador, denominador, período, frescura, exclusiones y advertencia de muestra pequeña; sin umbral de privacidad y volumen suficiente no se publica una tasa.

## Decisiones que bloquean la instrumentación

1. Data y Seguridad designan fuente, destino propio o tercero aprobado, control de acceso, retención y dueño de cada contador. No se introduce SDK antes de esa aprobación.
2. Producto e Identidad fijan qué es inicio y fin de activación, y cómo constatar llegada a portada sin exportar identidad a analytics.
3. Pagos define intento elegible, confirmación autoritativa y ventana de primer aporte; Soporte define contacto y estado ambiguo de 24 h. La unión se hace dentro de sistemas autorizados, sin leer directamente bases ajenas.
4. Cumplimiento aprueba el umbral mínimo de agregación, la ausencia de identificadores y los eventos/valores candidatos; QA captura payloads **reales en TEST** y ejecuta el validador sobre ellos antes de H4.S1.M3=HECHO.
5. Data valida tablero y baseline con numeradores, denominadores, ventanas, exclusiones y fecha antes de H4.S1.M4=HECHO.

La prueba adjunta usa solo datos sintéticos: demuestra el contrato propuesto, no el funcionamiento de una integración ni la privacidad de un SDK futuro.
