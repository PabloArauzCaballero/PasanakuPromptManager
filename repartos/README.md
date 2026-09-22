# Repartos

Un **reparto** es el encargo de un turno: qué hace cada persona, con qué alcance, con qué
criterio de aceptación y con qué Definition of Done. Se escribe **antes** del turno y se cierra
**después**, con el avance calculado, nunca estimado.

## Estructura obligatoria

```
repartos/<AAAA-MM-DD>/<PromptDia|PromptNoche>/
├── Daily-<Dia|Noche>-<AAAA-MM-DD>.md            ← daily del equipo
├── Richard/
│   ├── Richard-Daily-<Dia|Noche>-<AAAA-MM-DD>.md   ← daily personal
│   └── <NombreLote>.<Modulo>/                       ← el punto es obligatorio
│       ├── <NombreTarea>.md                         ← el encargo (prompt)
│       ├── entregables/
│       └── evidencia/
├── Pablo/ …
├── Marcelo/ …
├── Justin/ …
└── Leo/ …
```

### Turnos divididos por área

Cuando el mismo equipo trabaja los dos lados en el mismo turno, se admite **un nivel opcional de
área** entre el turno y la persona, para poder ver de un vistazo quién tiene qué en cada uno:

```
repartos/<AAAA-MM-DD>/<PromptDia|PromptNoche>/
├── Daily-<Dia|Noche>-<AAAA-MM-DD>.md            ← uno solo: consolida las DOS áreas
├── Backend/
│   ├── Richard/ … (misma estructura de arriba)
│   └── …
└── Frontend/
    ├── Richard/ …
    └── …
```

Reglas del nivel de área, que `check_reparto.py` verifica:

- Los únicos nombres permitidos son `Backend` y `Frontend`.
- **O están las carpetas de área, o no está ninguna.** Un turno mitad por área y mitad con personas
  sueltas esconde a quien quedó fuera del árbol, y se reporta como problema.
- **El daily del equipo sigue siendo uno solo**, a nivel de turno. Ahí va el avance del turno
  completo, que es la suma de las dos áreas. Cada persona tiene un daily personal **por área**.
- Una persona con carril en las dos áreas sigue teniendo **un trabajo activo por vez** (regla 70.1):
  el daily del equipo declara el orden de los bloques y qué se deja `A MEDIAS` antes de abrir el
  siguiente. Repartir dos carriles no autoriza a trabajarlos en paralelo.

Ejemplo vivo: [`2026-09-21/PromptNoche/`](2026-09-21/PromptNoche/).

**El equipo son cinco:** Richard, Pablo, Marcelo, Justin y Leo. La lista vive en
`tools/check_reparto.py`; agregar o sacar a alguien es tocar ese archivo, no improvisar una
carpeta.

## Validación

```bash
python tools/check_reparto.py repartos/2026-09-20      # sale 1 si falta algo
python tools/check_reparto.py --self-test              # prueba el propio validador
```

El validador comprueba **estructura y contenido mínimo**, no calidad. Exige que cada encargo
traiga:

- la sección de **instalación obligatoria del estándar** y la entrada por `skills-router`;
- el comando que verifica que el estándar quedó instalado (`plan_gate.py --self-test`);
- **kill-test**, **alcance OUT** y **tabla de ambigüedades registradas**;
- las **tres capas** de la regla 20 (`H1` → `H1.S1` → `H1.S1.M1`), cada capa con `**CA:**`,
  `**DoD:**` y `**Estado:**`, y los seis estados permitidos, nada inventado.

Y `tools/check_skills_citadas.py` verifica que **toda skill citada exista**. Para que pueda
hacerlo, las skills del encargo van en una tabla encabezada `| Skill |`, con el nombre entre
backticks en la primera celda — no sueltas en prosa.

Un encargo con las piezas presentes y mal escritas **pasa el chequeo**. Eso lo revisa una
persona.

## Plantillas

En [`_plantillas/`](_plantillas/): daily de equipo, daily personal y encargo. El encargo de la
plantilla ya pasa el validador: copialo y reemplazá el contenido, no la estructura.

## Reglas de honestidad del reparto

- El **avance va en la primera línea** del daily: `AVANCE: <HECHO> / <total> — <%>` (regla 40).
- El porcentaje sale de `microtareas HECHO / total`. `A MEDIAS` cuenta como **no hecha**.
- Un encargo se escribe **completo y ordenado por dependencia**, aunque sea más de lo que entra
  en un turno. Lo que no se cierre va `A MEDIAS` con qué anda, qué no anda y qué falta.
  **Recortar alcance es decisión de coordinación, y se registra.**
- **Dos personas escribiendo el mismo archivo es un defecto del reparto**, no un accidente: cada
  reparto declara las reservas de archivos y servicios.
- Nada de datos reales de participantes en ninguna salida pegada (regla 90.2).
