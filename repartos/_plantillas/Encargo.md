# <Título del encargo>

> **Estado:** `NOT_RUN`. Escrito al repartir, antes del turno. Ningún resultado de acá se
> ejecutó todavía.

- **Persona:** <Richard|Pablo|Marcelo|Justin|Leo> · **Turno:** <día|noche> · **Fecha:** <AAAA-MM-DD>
- **Servicio(s):** `<servicio>` · **Daily del equipo:** [Daily-<Dia|Noche>-<fecha>.md](../../Daily-<Dia|Noche>-<fecha>.md)
- **<N> hitos · <N> subtareas · <N> microtareas**

## 1. Antes de escribir una línea — instalación OBLIGATORIA del estándar

Esto es lo primero del turno, no lo último. Un turno que arranca sin esto arranca en `BLOQUEADO`.

1. Copiá o enlazá `.claude/` del estándar dentro del repo en el que vas a trabajar.
2. Entrá por `skills-router` y cargá las skills que tu trabajo necesita. **No leas el catálogo
   entero.**
3. Verificá que el estándar quedó instalado y **pegá las dos salidas** en tu daily:

```bash
ls .claude/skills | wc -l
python .claude/hooks/plan_gate.py --self-test
```

**Skills obligatorias de este encargo.** Van en tabla, con el nombre entre backticks en la
primera celda: así `tools/check_skills_citadas.py` puede verificar que existen. Una skill citada
que no existe manda a la nada.

| Skill | Para qué en este encargo |
|---|---|
| `<skill>` | <por qué la necesita este encargo> |

**Reglas que aplican con prioridad:** 00 · 20 · 30 · 40 · 91 si toca dinero · 98 si cruza servicios

## 2. Resultado observable

<Una frase: quién ve o puede hacer qué, dónde, desde qué estado.>

**Kill-test:** <la comprobación más barata que demostraría que esto NO está hecho.>

## 3. Alcance

**IN:** <lista explícita de lo que se toca>

**OUT:** <lista explícita de lo que NO se toca aunque se vea roto>

**Reservas de archivos:** <qué archivos/servicios son tuyos en este turno>

## 4. Plan

### H1 — <hito: resultado observable y demostrable>

**CA:** Dado <estado>, cuando <acción>, entonces <resultado observable>.
**DoD:** <comandos + gates aplicables>, con salida pegada en `evidencia/`.
**Estado:** TODO

#### H1.S1 — <subtarea>

**CA:** Dado <estado>, cuando <acción>, entonces <resultado observable>.
**DoD:** <comando> → <salida esperada>.
**Estado:** TODO

| ID | Microtarea | Criterio de aceptación | Definition of Done | Estado |
|---|---|---|---|---|
| H1.S1.M1 | <un solo cambio verificable> | <binario> | `<comando>` → <salida esperada> | TODO |
| H1.S1.M2 | … | … | `<comando>` | TODO |

## 5. Ambigüedades registradas

Se arrastran, **no se resuelven por conveniencia** (regla 00).

| ID | Ambigüedad | Quién puede resolverla | Qué bloquea | Supuesto tomado |
|---|---|---|---|---|
| Q-01 | <pregunta abierta> | <negocio / coordinación / cumplimiento> | <qué queda trabado> | <lo que asumís mientras tanto> |

## 6. Definition of Done del hito

- [ ] Todas las microtareas en `HECHO`, `A MEDIAS` con las cuatro respuestas, o `BLOQUEADO` con
      evidencia.
- [ ] `PLAN.md` y `REPORTE.md` escritos, con el avance calculado en la primera línea.
- [ ] Evidencia literal pegada en `evidencia/`, sin datos reales de participantes.
- [ ] Gates aplicables pasados: `evidence-and-verification` siempre; `money-movement-safety` si
      toca importes; `microservices-testing` si cruza servicios; `data-privacy-financial` si toca
      datos de personas.
- [ ] Peldaño de evidencia declarado (regla 30).
