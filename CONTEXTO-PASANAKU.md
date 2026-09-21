# Contexto de Pasanaku — lo que hay que saber antes de tocar nada

Este archivo existe para que nadie —persona o agente— tenga que deducir el dominio leyendo
código. Es el resumen de **qué es el producto** y **cómo está partido**. El detalle vive en el
modelo de datos: [`Pasanaco_backendBO/docs/Index.md`](../Pasanaco_backendBO/docs/Index.md).

Si algo de acá contradice al `CLAUDE.md` del repo en el que estás trabajando, **gana el
`CLAUDE.md`** y la contradicción se registra (regla 00).

## 1. Qué es un pasanaku

Un grupo de personas aporta una cuota fija cada periodo, y en cada periodo **una** de ellas se
lleva el total. El orden de cobro se sortea. Al final, todos pusieron lo mismo y todos cobraron
una vez: no hay interés, hay **acceso a un monto grande antes de haberlo ahorrado**.

Lo que el software vende no es la plata: es **confianza**. Por eso tres cosas son el producto y
no un detalle técnico:

1. **El orden de cobro es verificable** (sorteo commit-reveal).
2. **Las cuentas del grupo son auditables** (panel calculado desde el mayor).
3. **Quien no paga tiene consecuencias con debido proceso**, y el que cumple cobra igual
   (fondo de garantía).

## 2. Las diez decisiones que atraviesan el modelo

Salen del README del modelo de datos y se reflejan en las reglas 91 y 98:

1. **Tokens como agregado propio.** Nunca se persiste el valor plano: solo su hash con *pepper*.
2. **El incumplimiento es un expediente, no una bandera.** Evidencia, descargo, plazo, estado
   `FIRME`, sanción proporcional y apelación. La reputación es *consecuencia* de ese expediente.
3. **El cupo está separado del participante.** Una persona puede tener dos manos o media mano;
   las obligaciones y los turnos cuelgan del cupo, no de la persona.
4. **Contabilidad de doble partida.** `SUM(debe) = SUM(haber)`, siempre. El panel se calcula
   desde el mayor. Nada se edita: se reversa.
5. **Idempotencia de extremo a extremo.** Webhooks, órdenes de cobro, desembolsos, tareas y
   notificaciones llevan `clave_idempotencia` única.
6. **Sorteo verificable.** Se publica el hash de la semilla antes de sortear y se revela después,
   para que cualquiera recompute el orden.
7. **Debido proceso en las sanciones.** Matriz `tipo × severidad × reincidencia`, plazo de
   descargo, estado `FIRME` antes de ejecutar, apelación en dos instancias.
8. **Auditoría encadenada por hash + outbox transaccional.** Bitácora *insert-only*, lectura
   auditada aparte de la escritura, y el evento de dominio escrito en la misma transacción.
9. **La entrega es una liquidación**, no una transferencia: bolsa bruta, deducciones línea a
   línea y neto contra cuenta verificada con periodo de enfriamiento.
10. **El organizador no cobra ni custodia** (RN-18). No hay comisión y el dinero del grupo no
    pasa por su cuenta.

## 3. Cómo está partido: el mapa de servicios

Cada servicio es **dueño de sus datos**. Nadie lee la base de otro (regla 98.1).

| Servicio | Módulo | Es dueño de |
|---|---|---|
| `identidad` | M1 | Usuario, credenciales, MFA, dispositivos, tokens, documento, KYC, consentimiento |
| `grupos` | M2 | Grupo, cupo, participante, periodo, turno, reglamento, acuerdos, sorteo |
| `pagos` | M3 | Obligación de aporte, orden de cobro, QR, pago, conciliación, extracto |
| `contabilidad` | M3 | Plan de cuentas, asiento, movimiento, cierre diario |
| `entregas` | M4 | Entrega de fondo, deducciones, cuenta bancaria del beneficiario, desembolso |
| `notificaciones` | M5 | Plantillas, canales, cola de envío, eventos de entrega |
| `confianza` | M6 | Transparencia, score y sus componentes, certificados |
| `organizador` | M7 | Contrato del organizador, tareas automatizadas, desempeño |
| `garantia` | M8 | Fondo, cobertura, incumplimiento, deuda, aval, sanción, apelación |
| `auditoria` | M9 | Bitácora encadenada, eventos de dominio, definición y ejecución de reportes |

Más el **gateway** en el borde y un **BFF por cliente** (web, app, WhatsApp).

## 4. Los tres flujos que hay que entender sí o sí

### Acreditar un aporte
`pagos` emite la orden y el QR → el participante paga → la pasarela manda el **webhook firmado**
→ `pagos` valida firma, ventana temporal, duplicado y monto contra la orden → crea el pago y
publica `aporte.acreditado` **por outbox** → `contabilidad` asienta, `grupos` marca la obligación
cumplida, `notificaciones` avisa, `confianza` puntúa.

### Entregar el fondo
`entregas` congela la bolsa bruta **leída del mayor** → pide deuda y deducciones a `garantia` →
asienta la liquidación → verifica cuenta bancaria y enfriamiento → **ordena el desembolso**
(punto de no retorno) → confirma recepción. Es una **saga con compensaciones**.

### Cubrir un incumplimiento
Obligación vencida → expediente en `garantia` con evidencia y plazo de descargo → `FIRME` →
verificación de política, límite y saldo del fondo → cobertura + **subrogación** (la deuda se
traslada, no se perdona) → asientos → cobranza escalonada → recuperación o castigo.

## 5. Lo que todavía no está decidido

No lo inventes: registralo como ambigüedad (regla 00.1.7) y seguí con el supuesto declarado.

- Qué pasa si **falta plata** para la entrega de un periodo: ¿cubre el fondo, se prorratea, se
  posterga? Es decisión de **negocio** y va en el reglamento, no en el código.
- Proveedor de pagos y de transferencias, y si soportan clave de idempotencia.
- Proveedor de verificación de identidad y qué devuelve.
- Broker de mensajería.
- Umbrales, plazos y formatos **regulatorios**: los define el oficial de cumplimiento, no este
  repo (`regulatory-compliance-mapping`, `aml-sanctions-screening`).

## 6. Por dónde entrar

| Querés… | Andá a |
|---|---|
| Saber qué skill cargar | [`skills-router`](.claude/skills/skills-router/SKILL.md) |
| Las obligaciones de trabajo | [`AGENTS.md`](AGENTS.md) y [`.claude/rules/`](.claude/rules/) |
| Lo que no se negocia con el dinero | [regla 91](.claude/rules/91-dinero-y-movimiento-de-fondos.md) |
| Lo que no se negocia entre servicios | [regla 98](.claude/rules/98-microservicios.md) |
| El modelo de datos, entidad por entidad | [`Pasanaco_backendBO/docs/Index.md`](../Pasanaco_backendBO/docs/Index.md) |
| El reparto del turno | [`repartos/`](repartos/README.md) |
