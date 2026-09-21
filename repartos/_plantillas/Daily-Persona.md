# Daily de <Persona> — turno <día|noche> — <AAAA-MM-DD>

> **AVANCE: <HECHO> / <total> — <%>.** ← primera línea, siempre. Sale de `microtareas HECHO / total`.
> **Estado:** `IN_PROGRESS` | `COMPLETADO` | `BLOQUEADO`.

- **Persona:** <Persona> · **Turno:** <día|noche> · **Fecha:** <AAAA-MM-DD> · **Servicio:** `<servicio>`
- **Tu encargo:** [<Título>](<Lote>.<Modulo>/<Tarea>.md)
- **Daily del equipo:** [Daily-<Dia|Noche>-<fecha>.md](../Daily-<Dia|Noche>-<fecha>.md)

## 1. Instalación del estándar — lo primero

- [ ] `ls .claude/skills | wc -l` → salida pegada abajo.
- [ ] `python .claude/hooks/plan_gate.py --self-test` → salida pegada abajo.
- [ ] Skills cargadas: `<lista>`

```text
$ ls .claude/skills | wc -l
<salida>
$ python .claude/hooks/plan_gate.py --self-test
<salida>
```

## 2. Avance por hito

| Hito | Microtareas | HECHO | Estado |
|---|---:|---:|---|
| H1 — <nombre> | | | TODO |
| **TOTAL** | | | |

## 3. Qué quedó andando (con evidencia)

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|

## 4. A medias — las cuatro respuestas, obligatorias

### <ID> — <título>
- **Qué anda:**
- **Qué no anda:**
- **Qué falta exactamente:**
- **Dónde quedó:** <rama, archivos, si compila>

## 5. Bloqueado

| ID | Qué bloquea | Qué intenté | Qué lo destraba | De quién depende |
|---|---|---|---|---|

> Recordá la regla 65: si el contrato de lo que falta se puede nombrar, **se simula en tres
> niveles y se cierra**. Solo una decisión de negocio o una acción destructiva sobre algo
> compartido justifican dejarlo abierto.

## 6. Hallazgos para el equipo

| ID | Qué | A quién le pega | Estado |
|---|---|---|---|

## 7. No cubierto

<Lo que se hizo pero NO se probó. Distinto de pendiente.>

## 8. Ambigüedades que arrastro

| ID | Ambigüedad | Quién la cierra | Estado |
|---|---|---|---|
