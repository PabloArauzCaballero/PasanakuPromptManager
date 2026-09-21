# docs/trabajo

Acá vive **un directorio por trabajo**, con la estructura que exige la regla 20:

```
docs/trabajo/<AAAA-MM-DD>-<slug>/
├── PLAN.md        ← se crea PRIMERO; sin esto, el hook plan_gate.py bloquea escribir código
├── REPORTE.md     ← al cerrar, SIEMPRE, incluso con el trabajo incompleto
└── evidencia/     ← salidas literales, capturas, traces
```

- El **avance va en la primera línea** del `REPORTE.md`: `AVANCE: <HECHO> / <total> — <%>`.
- Las tres secciones del reporte —Completado, A medias, Pendiente— **existen siempre**. Una
  sección vacía se escribe con "ninguna": borrarla está prohibido.
- Ninguna salida pegada puede contener datos reales de participantes, documentos, cuentas
  bancarias ni importes atribuibles (regla 90.2). Si los tenía: se enmascara **y se aclara**.

Cuando el trabajo es un carril con estructura propia (`repartos/`), el plan vive dentro de esa
estructura y no se duplica acá — pero tiene que cumplir igual las tres capas, los CA y DoD y los
seis estados (regla 20 §1).

El avance se calcula, no se estima:

```bash
python .claude/hooks/plan_status.py
```
