# Plan maestro — Diseño mobile, motion y UX listo para producción

- Fecha: 2026-10-07
- Repos afectados: `PasanakuFrontend`, `PasanakuPromptManager`
- Referencia auditada: `Atlas/AtlasFrontend/apps/consumer-app`
- Resultado observable: una persona puede registrarse, entender su situación, aportar y comprobar qué pasó sin adivinar, incluso con mala conexión, texto grande o movimiento reducido; el equipo puede demostrar esa calidad antes de publicar.
- Kill-test: si un flujo crítico no tiene prototipo de sus estados, contrato de contenido, especificación de motion reducido, prueba en dispositivo y métrica de éxito, no está listo para producción.
- Decisión central: **no copiar Atlas visualmente**. Conservar la identidad cálida verde/naranja de AportaYa y adoptar la disciplina de Atlas: tokens, motion con propósito, confianza contextual, pruebas reales y evidencia visual.

## 1. Alcance y supuestos

### IN

- App Flutter de participante: activación, inicio, aportes, grupos, turnos, transparencia y soporte.
- Sistema visual y de motion, componentes, contenido, estados de pantalla, accesibilidad y responsive móvil/tablet.
- Flujo Figma → tokens → Flutter → goldens → dispositivo → piloto.
- Instrumentación UX sin datos personales o financieros en analytics.
- Gates de producto, diseño, accesibilidad, rendimiento, seguridad y release.

### OUT

- Cambiar reglas de negocio, contratos de dinero o arquitectura de microservicios.
- Copiar código React Native de Atlas a Flutter.
- Rediseñar backoffice o sitio público en este carril.
- Publicar builds en tiendas durante esta planificación.
- Usar datos de producción en capturas, pruebas o herramientas externas.

### Ambigüedades registradas

| Pregunta | Supuesto para avanzar | Confirmar con |
|---|---|---|
| ¿Qué recorrido tiene prioridad comercial? | Activación → portada → primer aporte, por ser el camino más corto al valor y la confianza | Producto |
| ¿Android primero sigue vigente? | Sí, con paridad iOS obligatoria antes de release | Producto + Mobile |
| ¿Existe baseline confiable de conversión y abandono? | No se encontró en el alcance revisado; H4 instrumenta antes de fijar metas de mejora | Data + Producto |
| ¿La transición de marca actual es definitiva? | Es candidata, no dogma; debe superar prueba de comprensión, rendimiento y movimiento reducido | Marca + UX |

## 2. Skills instaladas y cómo se usarán

Las skills instaladas estarán disponibles para Codex a partir del siguiente turno.

### Suite oficial de Figma

| Skill | Uso en este plan |
|---|---|
| `figma` | Leer diseños y contexto del archivo |
| `figma-use` | Operar sobre componentes y variables |
| `figma-create-new-file` | Crear el archivo de diseño si no existe uno canónico |
| `figma-generate-library` | Construir la librería base |
| `figma-create-design-system-rules` | Mantener reglas Figma ↔ código |
| `figma-code-connect-components` | Vincular componentes diseñados con Flutter |
| `figma-generate-design` | Ensamblar pantallas con el sistema existente |
| `figma-implement-design` | Llevar pantallas aprobadas a producción con fidelidad |

### Suite especializada mobile, UX y motion

`mobile-ux-design`, `frontend-motion`, `ux-clarity-usability`, `visual-hierarchy-composition`,
`frontend-beautiful-ui`, `ui-quality-review`, `frontend-design-system`,
`frontend-accessibility`, `ux-writing-microcopy`, `flutter-theming`, `flutter-development`,
`visual-proof`, `frontend-ux-states` y `frontend-responsive-layout`.

La skill `motion-ref`, ya presente, fija el principio rector: cada animación resuelve una duda,
una espera, una jerarquía o una transición; no existe solo para “verse moderna”.

## 3. Diagnóstico verificable

### Pasanaku hoy

- Flutter/Dart con 326 archivos Dart entre app y sistema de diseño.
- Sistema propio en `packages/diseno_flutter`, tokens generados, temas claro/oscuro, componentes
  atómicos, moleculares y organismos.
- Ya existen goldens, pruebas de accesibilidad, haptics, transición de marca, zoom de navegación,
  aparición escalonada, monto animado y respeto de `MediaQuery.disableAnimationsOf(context)`.
- La identidad actual es propia: verde profundo, verde de confianza y naranja como acento. No
  necesita convertirse en la paleta navy/teal de Atlas.
- El hueco principal no es “falta de animación”; es **cerrar el sistema**: gobernanza de motion,
  paridad Figma/código, prueba con personas, instrumentación y gates por flujo.

### Qué Atlas hace bien

- Centraliza movimiento en tokens: toque 140 ms, contenido 240 ms, recorridos 380 ms y stagger
  de 45 ms.
- Corre el motion de alta frecuencia fuera del hilo de lógica y anula movimiento con la preferencia
  del sistema.
- Usa feedback táctil, superficies que se hunden, entradas de 12 px y transiciones de marca con
  navegación durante cobertura total.
- Documenta fallos reales que solo aparecieron en iOS: safe area, teclado, errores fuera de vista.
- Acompaña capturas con videos y contact sheets; una imagen fija no se presenta como evidencia de
  movimiento.
- Explica confianza en el mismo lugar donde pide el dato y evita promesas que el backend no cumple.

### Matriz de transferencia Atlas → AportaYa

| Patrón de Atlas | Decisión | Aplicación en AportaYa |
|---|---|---|
| Tokens únicos de duración, easing, spring y presión | ADOPTAR | Crear `MovimientoAportaYa` generado desde tokens; prohibir duraciones sueltas |
| Movimiento reducido = cambio instantáneo completo | ADOPTAR | Ningún contenido depende de animarse; tests con animaciones desactivadas |
| Safe area, teclado y scroll al primer error | ADOPTAR | Plantilla única de formulario y prueba iOS/Android |
| Tarjeta contextual de confianza | ADAPTAR | Explicar custodia, uso de datos y por qué se pide cada permiso, en lenguaje de Pasanaku |
| Press feedback + háptico semántico | ADOPTAR | Ligero para selección; medio para éxito; alerta solo para fallo significativo |
| Cinemática de marca de 1,7 s | ADAPTAR | Máximo una vez por sesión; comparar con la actual de 1,45 s y una variante de 900 ms |
| Navegar cuando el velo ya cubrió | ADOPTAR | Montar destino detrás de la marca sin mostrar dos pantallas ni bloquear carga |
| Dark-first navy/teal | DESCARTAR | Mantener lenguaje visual AportaYa y validar contraste en ambos temas |
| Animar cifras al aparecer | DESCARTAR | Animar solo un valor que cambia frente a la persona, nunca un saldo inicial |
| Celebración intensa de una operación monetaria | DESCARTAR | Confirmación sobria, comprobante y estado persistente; nunca confetti |
| Copiar estructura de crédito/mora | DESCARTAR | Usar modelo mental de grupo, aporte, turno, custodia y debido proceso |

## 4. Norte de experiencia

### Promesa

**“Sé cuánto tengo, qué debo hacer ahora y qué pasará después.”**

Cada pantalla debe responder, en este orden:

1. ¿Dónde estoy y qué estado tengo?
2. ¿Qué significa para mí, en dinero y tiempo?
3. ¿Cuál es la acción principal segura?
4. ¿Qué pasa después y cómo lo compruebo?

### Principios no negociables

1. Claridad antes que espectáculo; confianza antes que conversión.
2. Una acción primaria por momento. Las secundarias no compiten visualmente.
3. El servidor calcula; el cliente explica y confirma.
4. Ningún importe se oculta, se recalcula localmente o cambia durante una animación.
5. Error, vacío, carga, offline y éxito parcial son diseños, no excepciones.
6. La mora se informa con salida y debido proceso; no se gamifica ni avergüenza.
7. Movimiento, color y háptico refuerzan el significado, nunca son el único significado.
8. Los permisos se piden en contexto y solo cuando la persona dispara la función.
9. Un flujo puede retomarse después de interrupción, cierre o pérdida de red.
10. La evidencia de producción se obtiene en dispositivos y con datos sintéticos.

## 5. Arquitectura de experiencia prioritaria

| Prioridad | Flujo vertical | Resultado que debe sentir la persona | Riesgo principal |
|---:|---|---|---|
| P0 | Activación, identidad y contratos | “Entiendo por qué me piden esto y puedo continuar” | Abandono, privacidad, teclado, permisos |
| P0 | Portada | “Sé cómo voy y qué hago hoy” | Sobrecarga, números sin contexto |
| P0 | Aporte: revisar → confirmar → resultado → comprobante | “Pagué una vez y sé exactamente qué pasó” | Doble envío, estado ambiguo, red intermitente |
| P0 | Entrega/cobro de turno | “Veo bolsa, deducciones y neto antes de aceptar” | Sorpresa monetaria |
| P1 | Crear, pedir cupo e invitar | “Conozco el compromiso total y quién decide” | Consentimiento débil, cupo mal entendido |
| P1 | Calendario y estado del grupo | “Distingo vencido, exigible, futuro y pagado” | Dependencia del color, suma incorrecta |
| P1 | Sorteo y transparencia | “Puedo verificar por qué salió ese orden” | Complejidad técnica sin traducción humana |
| P1 | No puedo pagar, reclamo y soporte | “Tengo una salida, un plazo y un número de caso” | Callejón sin salida, lenguaje punitivo |

Todas las vistas que consultan datos diseñan cinco estados: carga, vacío, error, offline y éxito
parcial. Las operaciones monetarias añaden: listo, enviando, recibido por servidor, pendiente de
confirmación, confirmado y rechazado recuperable/no recuperable.

## 6. Sistema visual que se entregará

### Archivo Figma canónico

Páginas: `00 Foundations`, `01 Components`, `02 Patterns`, `03 Flows`, `04 Motion`,
`05 Accessibility`, `06 Research`, `07 Ready for Dev`, `99 Archive`.

### Variables y tokens

- Color semántico: superficie, contenido, marca, éxito, advertencia, peligro, información y dinero.
- Tipografía: roles, no tamaños sueltos; números financieros con cifras tabulares.
- Espacio, radio, elevación, borde, opacidad, área táctil y safe area.
- Motion: duración, curva, resorte, distancia, escala de presión y stagger.
- Temas claro/oscuro y densidad teléfono/tablet; sin duplicar componentes por tema.
- Nombre idéntico o mapeo explícito entre variable Figma, token fuente y símbolo Dart.

### Componentes mínimos con variantes completas

- Botón, icon button, campo, selector, checkbox, chip, tab y navigation bar.
- Tarjeta de saldo, cuota, grupo, turno, requisito, movimiento, confianza y estado.
- Banner offline, alerta persistente, snackbar, diálogo, bottom sheet y comprobante.
- Skeleton, vacío, error, bloqueado, permiso denegado y éxito parcial.
- Calendario, desglose de dinero, línea de tiempo, QR/código corto y stepper.

Cada variante incluye: default, pressed, focused, disabled, loading, error, selected, texto grande,
movimiento reducido, claro/oscuro y semántica accesible.

## 7. Sistema de motion de producción

### Escala propuesta

| Nivel | Duración | Uso | Regla |
|---|---:|---|---|
| Instantáneo | 0 ms | Movimiento reducido, datos críticos | Contenido completo desde el primer frame |
| Feedback | 120–160 ms | Press, selección, toggle | Responde al dedo; escala mínima 0,97 |
| Estado | 200–280 ms | Error→recuperado, selección, cambio de importe | Un cambio, una lectura |
| Estructura | 280–380 ms | Bottom sheet, detalle, navegación | Mantiene origen/destino y puede interrumpirse |
| Marca | 900–1450 ms | Entrada excepcional, una vez por sesión | Nunca tapa una espera ni una operación de dinero |

Base recomendada: `fast=140`, `base=240`, `slow=340–380`, `stagger=45`; la prueba A/B de marca
decide entre 900 y 1450 ms. El resultado se vuelve token, no número repetido.

### Catálogo funcional

| Momento | Motion | Háptico | Movimiento reducido |
|---|---|---|---|
| Toque aceptado | Hundimiento sobreamortiguado | selección ligera | cambio visual instantáneo |
| Contenido listo | Fade + 8–12 px, escalonado | ninguno | aparece completo |
| Lista cargada | Máximo seis entradas escalonadas; resto junto | ninguno | lista completa |
| Navegar a detalle | Transición direccional/zoom coherente con back | ninguno | corte instantáneo |
| Abrir acción contextual | Bottom sheet conducido | ligero al asentarse | hoja aparece sin recorrido |
| Importe cambia por entrada | Conteo corto desde valor anterior | ninguno | valor final inmediato |
| Envío de aporte | Botón bloqueado + progreso no bloqueante | ligero | indicador estático + texto |
| Confirmación del servidor | Estado persistente + check sobrio | éxito medio | check final inmediato |
| Rechazo | Mensaje inline y foco/scroll al error | alerta única | foco y mensaje, sin shake |
| Marca | Cubrir → montar destino → descubrir | opcional y una vez | se omite por completo |

### Prohibiciones

- Nada de confetti, rebote juguetón, parallax ornamental o partículas en dinero, mora o reclamos.
- No animar todos los números al abrir ni usar movimiento para esconder latencia.
- No bloquear input por una animación secundaria.
- No más de una animación dominante por pantalla.
- Publicidad sin animación, como ya exige el plan de producto.
- No capturar analytics por frame ni contenido sensible; solo eventos de estado con IDs técnicos.

### Presupuesto técnico

- Animar preferentemente `transform` y `opacity`; aislar pintura compleja con `RepaintBoundary`.
- Una sola fuente de reloj por secuencia de marca; cancelar controladores al desmontar.
- Primer contenido visible antes del motion decorativo.
- En equipo de referencia a 60 Hz: `build` y `raster` p95 ≤ 16,7 ms en los flujos críticos;
  frames lentos < 1 % por recorrido perfilado.
- Toda secuencia de marca tiene timeout de seguridad y deja navegar aunque falle audio/asset.
- Tests cubren valor inicial, valor final, interrupción y `disableAnimations=true`.

## 8. Contenido, confianza y accesibilidad

### Contrato de contenido por pantalla

- Título orientado a tarea, estado en lenguaje humano y siguiente acción concreta.
- Importes con moneda, costo total, impuestos/deducciones y neto antes de confirmar.
- Error con qué pasó, qué quedó seguro, qué puede hacer ahora y código solo si sirve a soporte.
- Confirmación con estado persistente, fecha/hora, identificador y acceso al comprobante.
- Promesas de privacidad verificadas contra comportamiento real; sin texto legal inventado.

### Gate accesible

- Objetivos táctiles ≥ 48×48 dp y separación suficiente.
- Contraste AA, foco visible, orden de lectura lógico y estado no dependiente solo de color.
- Texto al 200 % sin corte, solapamiento ni pérdida de acción.
- TalkBack y VoiceOver en los flujos P0; labels para controles, importes y progreso.
- Safe area, notch, home indicator, rotación soportada donde corresponda y teclado sin tapar acción.
- Movimiento reducido, contraste alto y lector de pantalla forman parte del Definition of Done,
  no una ronda opcional al final.

## 9. KPIs y plan de medición

No se fija una mejora porcentual final sin baseline. Primero se instrumenta una versión completa;
después Producto aprueba el objetivo con intervalo y fecha.

### KPIs primarios

| KPI | Fórmula | Decisión que habilita |
|---|---|---|
| Activación comprendida | usuarios que completan activación y llegan a portada / usuarios que la inician | Priorizar pasos, contenido o permisos |
| Éxito del primer aporte | aportes confirmados una sola vez / intentos elegibles iniciados | Saber si el flujo central es seguro y usable |
| Resolución sin ayuda | operaciones críticas completadas sin reintento ambiguo ni contacto de soporte en 24 h / operaciones iniciadas | Medir confianza operativa, no solo conversión |

### Drivers y guardrails

- Drivers: avance por paso, tiempo hasta valor, recuperación de error, retorno a flujo interrumpido.
- Guardrails: doble intento, abandono después de ver costo, crash/ANR, frame lento, error de lector,
  queja de privacidad y contacto de soporte por estado ambiguo.
- Analytics usa IDs técnicos y categorías; nunca importe, documento, teléfono, nombre, QR o mensaje.

### Umbrales provisionales de lanzamiento

- Éxito en prueba final: ≥ 95 % en aporte/entrega y ≥ 90 % en activación, con participantes
  representativos y sin ayuda del moderador.
- Cero problemas P0/P1 de usabilidad, accesibilidad, privacidad o dinero abiertos.
- Cero resultado monetario ambiguo y cero doble envío en recorridos de resiliencia.
- 100 % de pantallas P0 con cinco estados y operaciones P0 con estados transaccionales.
- Durante piloto: crash-free sessions ≥ 99,9 % y guardrails sin degradación material frente al
  baseline. Si no existe volumen suficiente, se reporta intervalo y no se finge certeza.

## 10. Plan de ejecución por gates

No se avanza por calendario sino por evidencia. Un hito no puede “compensar” la falla del anterior.

## H1 — Atlas y Pasanaku quedan auditados

**CA:** Dado ambos productos, cuando se revisan código, capturas y evidencia, entonces cada patrón
adoptado, adaptado o descartado tiene una razón vinculada a Pasanaku.
**DoD:** matriz de §3 completa y archivos reales inspeccionados.
**Estado:** HECHO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Inventariar stack y motion de Atlas | Tokens, componentes y reduced motion identificados | `rg -n "useReducedMotion|withTiming|withSpring" AtlasFrontend/apps/consumer-app` | HECHO |
| H1.S1.M2 | Revisar evidencia visual Atlas | Bienvenida, confianza, portada y calendario observados | capturas de `docs/evidence` abiertas | HECHO |
| H1.S1.M3 | Inventariar Flutter actual | Componentes, goldens, haptics y motion identificados | `rg -n "disableAnimations|AnimationController|Haptic" PasanakuFrontend` | HECHO |

## H2 — El kit de skills queda disponible

**CA:** Dado un nuevo turno de Codex, cuando se invoque diseño mobile, motion, UX o Figma, entonces
las skills especializadas están instaladas y descubribles.
**DoD:** cada directorio contiene `SKILL.md` y el catálogo oficial marca Figma como instalado.
**Estado:** HECHO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Instalar suite oficial Figma | Seis skills faltantes presentes | `list-skills.py --format json` | HECHO |
| H2.S1.M2 | Instalar suite mobile/UX/motion | Catorce `SKILL.md` presentes | comprobación de ruta y tamaño | HECHO |

## H3 — La dirección de diseño es aprobable

**CA:** Dado este documento, cuando Producto, Diseño, Mobile, QA y Cumplimiento lo revisan, entonces
pueden aprobar norte, prioridades, principios, métricas y gates sin decisiones críticas implícitas.
**DoD:** §§4–12 completas, revisión registrada y ambigüedades resueltas.
**Estado:** EN CURSO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Aprobar flujo P0 | Existe orden único de activación → portada → aporte | acta de Producto | EN CURSO |
| H3.S1.M2 | Aprobar principios y prohibiciones | Diseño y Cumplimiento aceptan las reglas | checklist firmado | EN CURSO |
| H3.S1.M3 | Nombrar dispositivo de referencia | Modelo/OS/RAM quedan versionados | ficha en `docs/qa/devices.md` | TODO |
| H3.S1.M4 | Confirmar baseline de analytics | Existe fuente, dueño y fecha | diccionario de eventos aprobado | TODO |

## H4 — Research e instrumentación establecen el baseline

**CA:** Dado el producto actual, cuando personas representativas recorren P0, entonces se conocen
errores, tiempos, comprensión y abandono sin exponer datos sensibles.
**DoD:** sesiones grabadas con consentimiento, síntesis, baseline y eventos validados en QA.
**Estado:** EN CURSO

El [journey P0 basado en pantallas reales](./JOURNEY-P0-BORRADOR.md) es insumo de H4.S1.M1, no investigación con personas ni aprobación. La fila queda EN CURSO hasta el taller con Producto/UX.

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H4.S1.M1 | Mapear journey y riesgos | Cada paso tiene intención, duda, dato y riesgo | journey aprobado | EN CURSO |
| H4.S1.M2 | Ejecutar test diagnóstico | Se prueban activación, portada y aporte con perfiles diversos | protocolo + hallazgos | TODO |
| H4.S1.M3 | Definir taxonomía de eventos | Cada KPI se calcula sin PII ni importes | prueba de payloads | TODO |
| H4.S1.M4 | Medir baseline | Hay numerador, denominador, ventana y dueño por KPI | tablero QA validado | TODO |

## H5 — Foundations y librería quedan conectados

**CA:** Dado Figma y Flutter, cuando cambia un token o componente aprobado, entonces el mapeo es
explícito y la divergencia se detecta antes del merge.
**DoD:** librería Figma publicada, tokens generados, catálogo Flutter y reglas de conexión.
**Estado:** TODO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H5.S1.M1 | Crear variables y modos | Claro/oscuro y teléfono/tablet comparten semántica | export de variables | TODO |
| H5.S1.M2 | Crear tokens de motion | No quedan duraciones sueltas en el alcance P0 | lint/`rg` con allowlist | HECHO |
| H5.S1.M3 | Completar componentes P0 | Cada variante de §6 existe en Figma y catálogo | checklist de paridad | EN CURSO |
| H5.S1.M4 | Conectar Figma con Flutter | Cada componente P0 apunta a símbolo real | Code Connect validado | TODO |
| H5.S1.M5 | Congelar v1 del sistema | Cambios posteriores requieren changelog y migración | tag + changelog | TODO |

## H6 — Los flujos P0 quedan prototipados y validados

**CA:** Dado un prototipo realista, cuando una persona completa P0, entonces entiende estado,
costo, acción y resultado sin ayuda.
**DoD:** prototipo navegable, contenido finalista, motion spec y dos rondas de prueba.
**Estado:** EN CURSO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H6.S1.M1 | Prototipar activación completa | Incluye permiso denegado, teclado, interrupción y retorno | recorrido grabado | TODO |
| H6.S1.M2 | Prototipar portada | Responde cuánto tengo, qué hago hoy y cómo van mis grupos | test de 5 segundos + tareas | TODO |
| H6.S1.M3 | Prototipar aporte | Costo, confirmación, pendiente, éxito, rechazo y comprobante visibles | task success ≥ umbral | EN CURSO |
| H6.S1.M4 | Especificar motion | Cada transición tiene trigger, valores, interrupción y reduce | tabla handoff completa | HECHO |
| H6.S1.M5 | Validar contenido legal | Ninguna promesa excede contrato o política | revisión Cumplimiento | TODO |

## H7 — Se implementa un vertical slice de producción

**CA:** Dado el backend de prueba, cuando una persona recorre activación → portada → aporte, entonces
la app persiste, reintenta de forma idempotente y muestra el estado real.
**DoD:** build, tests dirigidos, E2E con backend real y evidencia en Android/iOS.
**Estado:** EN CURSO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H7.S1.M1 | Implementar foundations | Tokens/componentes P0 reemplazan estilos locales | `yarn workspace @aportaya/diseno-flutter typecheck` | HECHO |
| H7.S1.M2 | Implementar activación | Se retoma tras cierre y maneja permisos/teclado | test dirigido + video; cobertura nueva de denegación/excepción de cámara y teclado en Android | A MEDIAS |
| H7.S1.M3 | Implementar portada | Prioridad visual coincide con prototipo aprobado | golden + captura real | EN CURSO |
| H7.S1.M4 | Implementar aporte seguro | Doble toque/reintento conserva idempotencia | E2E de duplicado con backend TEST | A MEDIAS |
| H7.S1.M5 | Implementar motion/reduced motion | Ambos recorridos terminan con igual contenido | test con animación on/off | HECHO |
| H7.S1.M6 | Hacer bienvenida usable con texto al 200 % | Garantías sin overflow y acciones dentro del scroll cuando el texto crece | test de texto grande + captura en Android | HECHO |
| H7.S1.M7 | Excluir serializadores Dart generados del diff | `build_runner` no deja archivos generados como cambios locales | `git check-ignore` reconoce un `*.g.dart` de cada cliente | HECHO |

## H8 — Calidad de producción queda demostrada

**CA:** Dado el vertical slice, cuando se somete a accesibilidad, resiliencia, rendimiento y
regresión, entonces no quedan fallos P0/P1 y las métricas cumplen umbral.
**DoD:** scorecard §11 completo con enlaces a evidencia literal.
**Estado:** EN CURSO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H8.S1.M1 | Accesibilidad automatizada/manual | TalkBack, VoiceOver y texto 200 % completan P0 | informe a11y | EN CURSO |
| H8.S1.M2 | Performance | Frames y memoria cumplen presupuesto en gama baja | trace de `flutter run --profile` | TODO |
| H8.S1.M3 | Resiliencia | Offline, timeout, 500, app kill y reintento dan estado inequívoco | matriz de fallos | EN CURSO |
| H8.S1.M4 | Visual | Claro/oscuro, tamaños y plataformas no divergen | goldens + capturas | A MEDIAS |
| H8.S1.M5 | Usabilidad final | Éxito de tareas alcanza umbrales | reporte con muestra y método | TODO |
| H8.S1.M6 | Seguridad/privacidad | No hay PII en logs, analytics o capturas | revisión + escaneo | TODO |

## H9 — Piloto y despliegue progresivo cierran el circuito

**CA:** Dado un build candidato, cuando se despliega por cohortes, entonces cada expansión ocurre
solo si KPIs y guardrails permanecen sanos y existe rollback probado.
**DoD:** 5 % → 25 % → 100 %, observación por cohorte, decisión registrada y rollback ejercitado.
**Estado:** TODO

| ID | Microtarea | CA binario | DoD | Estado |
|---|---|---|---|---|
| H9.S1.M1 | Dogfood interno | No quedan bloqueos de recorrido | reporte de cohorte | TODO |
| H9.S1.M2 | Piloto 5 % | Guardrails dentro de umbral | tablero + decisión | TODO |
| H9.S1.M3 | Expandir a 25 % | KPIs no degradan y soporte está preparado | acta go/no-go | TODO |
| H9.S1.M4 | Generalizar | 100 % con observabilidad y rollback | release report | TODO |
| H9.S1.M5 | Revisar a 7/30 días | Backlog se reordena con evidencia | revisión KPI | TODO |

## 11. Scorecard binario de salida

| Gate | PASS exige | Evidencia |
|---|---|---|
| Producto | Flujos P0 completos y reglas de dinero respetadas | UAT + contratos |
| UX | Task success en umbral; cero P0/P1 | informe de investigación |
| Visual | Paridad Figma/código en claro/oscuro | goldens y capturas reales |
| Motion | Propósito, tokens, interrupción y reduced motion | video + tests |
| Accesibilidad | 48 dp, AA, texto 200 %, TalkBack/VoiceOver | auditoría manual/automática |
| Rendimiento | Presupuesto de frames en dispositivo referencia | DevTools trace |
| Resiliencia | Offline, timeout, duplicado y app kill cubiertos | E2E y matriz de fallos |
| Privacidad | Cero PII/datos financieros en evidencia o telemetry | payload review + logs |
| Seguridad | Authz, step-up y almacenamiento seguro verificados | test dirigido |
| Release | Observabilidad, feature flag y rollback probados | runbook + simulacro |

Comandos base, desde `PasanakuFrontend`:

```powershell
yarn workspace @aportaya/tokens build
yarn workspace @aportaya/diseno-flutter typecheck
yarn workspace @aportaya/diseno-flutter test:front
yarn workspace @aportaya/diseno-flutter test:goldens
yarn workspace @aportaya/diseno-flutter test:a11y
yarn workspace @aportaya/movil typecheck
yarn workspace @aportaya/movil test:front
yarn workspace @aportaya/movil test:goldens
yarn workspace @aportaya/movil test:a11y
```

El E2E no se declara cubierto por el placeholder actual: requiere Patrol y dispositivo/emulador
real, backend real de TEST y evidencia de red/consola/persistencia.

## 12. Roles y gobernanza

| Rol | Decide | Entrega |
|---|---|---|
| Producto | Prioridad, alcance, KPI y go/no-go | journey y aceptación |
| Product Design | Jerarquía, interacción, sistema visual | Figma y specs |
| Motion Design | Lenguaje, coreografía y reduced motion | motion spec y videos |
| Content Design | Nombres, errores, confirmaciones y confianza | content matrix |
| Flutter | Arquitectura, rendimiento y fidelidad | código y tests |
| QA/A11y | Estrategia, dispositivos y evidencia | scorecard y defectos |
| Data | Definiciones, eventos, baseline y guardrails | diccionario y tablero |
| Seguridad/Cumplimiento | Dinero, privacidad, consentimiento y promesas | sign-off trazable |

Una decisión de diseño cambia mediante ADR breve si afecta navegación, dinero, privacidad, motion
de marca o tokens. Figma no es fuente de lógica; código no es fuente de intención. El contrato es:
variable/componente enlazado + criterio de aceptación + evidencia.

## 13. Riesgos y mitigación

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Copiar Atlas sin adaptar el modelo mental | Alto | Transferir principios; probar vocabulario y jerarquía AportaYa |
| Motion ornamental en dinero | Alto | Catálogo permitido/prohibido y review de Motion + Cumplimiento |
| Figma y Flutter divergen | Alto | tokens, Code Connect, catálogo y golden gate |
| Baseline inexistente o contaminado | Medio | instrumentar primero; targets provisionales etiquetados |
| Jank en gama baja | Alto | dispositivo referencia, profile mode y presupuesto p95 |
| iOS se valida tarde | Alto | evidencia por hito, no al final; safe area/teclado obligatorios |
| Capturas filtran datos | Alto | fixtures sintéticos y revisión previa a versionar |
| “Casi listo” sin E2E real | Alto | scorecard binario; placeholder E2E no cuenta |

## Orden de arranque recomendado

1. Resolver las cuatro decisiones H3.
2. Ejecutar H4 y fijar baseline.
3. Construir H5 sin rediseñar aún toda la app.
4. Prototipar y probar H6.
5. Implementar solo el vertical slice H7.
6. Pasar H8 completo.
7. Recién entonces escalar los patrones al resto de P1 y abrir H9.

Este orden evita dos trampas: pulir decenas de pantallas antes de validar el flujo central y usar
motion para maquillar una arquitectura de experiencia que todavía no se entiende.
