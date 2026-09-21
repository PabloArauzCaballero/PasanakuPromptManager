# Daily — turno <día|noche> — <AAAA-MM-DD>

> **AVANCE DEL TURNO: <HECHO> / <total> — <%>.**
> **Estado:** `IN_PROGRESS`. Escrito **al repartir**, antes del turno: todo resultado está en
> `NOT_RUN` a propósito, porque nadie ejecutó nada todavía.

- **Turno:** <día|noche> · **Fecha:** <AAAA-MM-DD>
- **Modelo de datos de referencia:** `Pasanaco_backendBO/docs/Index.md`

## 1. Quién tiene qué

| Persona | Servicio | Encargo | Hitos | Subtareas | Microtareas | Estado |
|---|---|---|---:|---:|---:|---|
| **Richard** | `identidad` | [<título>](Richard/<Lote>.<Modulo>/<Tarea>.md) | | | | `NOT_RUN` |
| **Pablo** | `grupos` | [<título>](Pablo/<Lote>.<Modulo>/<Tarea>.md) | | | | `NOT_RUN` |
| **Marcelo** | `pagos` | [<título>](Marcelo/<Lote>.<Modulo>/<Tarea>.md) | | | | `NOT_RUN` |
| **Justin** | `entregas` + `contabilidad` | [<título>](Justin/<Lote>.<Modulo>/<Tarea>.md) | | | | `NOT_RUN` |
| **Leo** | plataforma | [<título>](Leo/<Lote>.<Modulo>/<Tarea>.md) | | | | `NOT_RUN` |
| | | | **<N>** | **<N>** | **<N>** | |

## 2. Lo primero, para todos

Antes de la primera microtarea: instalar el estándar (sección 1 del encargo) y **pegar la salida
de los dos comandos** en el daily personal.

## 3. Orden de dependencia — quién espera a quién

| Quien espera | De quién | Qué exactamente | Qué hace mientras tanto |
|---|---|---|---|

> **Nadie se queda esperando (regla 65).** Si el contrato de lo que falta se puede nombrar, se
> simula en tres niveles —correcto, límite, inválido— y se cierra contra el doble, declarándolo.

## 4. Reservas de archivos y servicios — para que nadie se pise

| Servicio / área | Reservado para |
|---|---|

**Dos personas escribiendo el mismo archivo es un defecto del reparto, no un accidente.**

## 5. Ambigüedades abiertas — se arrastran, no se resuelven

| ID | Qué | Quién la cierra | Estado |
|---|---|---|---|

## 6. Cierre del turno — completar acá

| Persona | HECHO / total | Hitos cerrados | `A MEDIAS` | `BLOQUEADO` | Su daily |
|---|---|---|---|---|---|

### Qué NO se puede escribir en este documento

- Un `PASS` sin comando y exit code pegados.
- «Listo», «funciona» o «implementado» sobre algo que no se ejecutó.
- Un porcentaje que no salga de `HECHO / total`.
- Un `BLOQUEADO` disfrazado de `PASS` porque «igual compila».
- Datos reales de participantes, cuentas bancarias o documentos en cualquier salida pegada.
