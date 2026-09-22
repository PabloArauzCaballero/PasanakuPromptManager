# Reporte — repartir el rescate del frontend de AportaYa en los cinco carriles del turno noche

> **AVANCE: 18 / 18 — 100 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` de este repo (sin commit; los cambios quedan en el árbol de trabajo)
- Peldaño de evidencia alcanzado: **`REGRESSION_VERIFIED`** para el artefacto documental — los dos validadores del repo corridos sobre el turno, el verificador de reservas escrito con su autoprueba, la no regresión sobre el reparto anterior, y los conteos hechos por script sobre los archivos reales, todos con su código de salida pegado. Sobre el **código del frontend** nada cambia de peldaño: sigue en `DISCOVERED`, porque este trabajo reparte el plan, no lo ejecuta.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Tabla de reparto por tema con dueño único por hito del plan madre | revisión de §2.2 contra los 15 hitos del plan madre | PASS — los 15 hitos tienen dueño, ninguno dos |
| H1.S1.M2 | Tabla de entregas entre carriles, cada una con su vía de cierre sin esperar (regla 65) | revisión de §2.2 | PASS — 5 filas completas |
| H1.S1.M3 | `evidencia/check_reservas.py` escrito con autoprueba | `python …/check_reservas.py --self-test` | PASS — `6 PASS, 0 FAIL` |
| H1.S2.M1 | Encargo de Richard (`PR11-Sesion.Frontend`) | conteo por script | PASS — 4 hitos · 11 subtareas · **51** microtareas |
| H1.S2.M2 | Encargo de Justin (`PR12-Config.Frontend`) | conteo por script | PASS — 4 · 7 · **36** |
| H1.S2.M3 | Encargo de Leo (`PR13-Ci.Frontend`) | conteo por script | PASS — 5 · 12 · **52** |
| H1.S2.M4 | Encargo de Marcelo (`PR14-Fronteras.Frontend`) | conteo por script | PASS — 5 · 13 · **59** |
| H1.S2.M5 | Encargo de Pablo (`PR15-Contratos.Frontend`) | conteo por script | PASS — 5 · 10 · **58** |
| H1.S2.M6 | `entregables/` y `evidencia/` en los cinco lotes | `find … -type d` | PASS — 10 carpetas |
| H1.S2.M7 | Validador de estructura sobre el turno | `python tools/check_reparto.py repartos/2026-09-21` | PASS — `OK, 2026-09-21 cumple la estructura obligatoria`, `exit=0` |
| H1.S2.M8 | Validador de skills citadas | `python tools/check_skills_citadas.py` | PASS — `89 skill(s) distinta(s) citada(s), 0 inexistentes`, `exit=0` |
| H1.S3.M1 | Bloque C en el daily del equipo, con tabla de las cinco personas | `grep -cE "^### Bloque [ABC]"` en §1 | PASS — 3 bloques (A, B, C) |
| H1.S3.M2 | Primera línea del daily del equipo y advertencia de los dos repos | `sed -n '3p'` | PASS — `AVANCE DEL TURNO: 0 / 615 — 0 %.` + advertencia de que 91 y 98 aplican solo al bloque C |
| H1.S3.M3 | Los cinco dailies personales con su segundo lote, el orden A→B→C y sus reservas | `grep -l "PR1[1-5]" … \| wc -l` | PASS — 5 de 5 |
| H1.S3.M4 | Aritmética verificada por script sobre los archivos reales | conteo de microtareas | PASS — `BLOQUE C = 256` · `TURNO = 359 + 256 = 615` |
| H1.S4.M1 | Evidencia literal en `evidencia/` | `ls evidencia/*.txt` | PASS — 4 archivos con su `exit=` |
| H1.S4.M2 | No regresión del reparto anterior | `python tools/check_reparto.py repartos/2026-09-20` | PASS — `OK`, `exit=0` |
| H1.S4.M3 | Este reporte, con las tres secciones y el avance calculado | `python .claude/hooks/report_gate.py --self-test < /dev/null` | PASS — `14 PASS, 0 FAIL` |

## A medias

ninguna.

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| Las 256 microtareas del bloque C | `TODO` | Que arranque el turno. El plan madre sigue en `0/247` y nada del código del frontend se tocó: este trabajo produce los encargos, no los ejecuta. |
| El orden interno del bloque C | `TODO` | Pablo primero (su H2 entrega la línea base, los clientes versionados y los contratos que los otros cuatro necesitan) y Pablo último (su H5 es el cierre). Los otros cuatro carriles son independientes entre sí. |

## Evidencia

```text
$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
exit=0

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 89 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)
exit=0

$ python tools/check_reparto.py repartos/2026-09-20        # no regresión
check_reparto: OK, 2026-09-20 cumple la estructura obligatoria
exit=0

$ python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py
rutas reclamadas: 37
0 colisiones
exit=0

$ python docs/trabajo/2026-09-21-reparto-frontend-rescate/evidencia/check_reservas.py --self-test
check_reservas self-test: 6 PASS, 0 FAIL

$ conteo de microtareas sobre los cinco encargos
persona   lote                        H   S   M  CA/DoD/Est
Richard   PR11-Sesion.Frontend        4  11  51  15/15/15 OK
Justin    PR12-Config.Frontend        4   7  36  11/11/11 OK
Leo       PR13-Ci.Frontend            5  12  52  17/17/17 OK
Marcelo   PR14-Fronteras.Frontend     5  13  59  18/18/18 OK
Pablo     PR15-Contratos.Frontend     5  10  58  15/15/15 OK

BLOQUE C = 23 hitos, 53 subtareas, 256 microtareas
TURNO = 359 (bloques A+B) + 256 = 615

$ sed -n '3p' repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md
> **AVANCE DEL TURNO: 0 / 615 — 0 %.**
```

Índice de `evidencia/`: `check_reparto.txt`, `check_skills_citadas.txt`, `no-regresion-2026-09-20.txt`,
`check_reservas.txt`, `conteo-microtareas.txt` y el script `check_reservas.py` con su autoprueba.

## No cubierto

- **La calidad de los encargos no está verificada por nadie más que quien los escribió.** Los dos
  validadores comprueban estructura y contenido mínimo, no si el corte es el correcto ni si un CA
  está bien redactado; el README de `repartos/` lo dice explícitamente: "un encargo con las piezas
  presentes y mal escritas pasa el chequeo. Eso lo revisa una persona". **Nadie lo revisó todavía.**
- **Las reservas se verificaron sobre la sección IN de cada encargo, no sobre el código.** El
  script compara rutas declaradas; si alguien escribió mal una ruta, la colisión aparecería recién
  al ejecutar. Son 37 rutas declaradas, no un análisis del grafo de imports real.
- **Los totales por carril salen de contar filas de tabla**, no de estimar esfuerzo: 59 microtareas
  no significa que el carril de Marcelo sea más largo en horas que el de Justin con 36.
- **No se verificó que las microtareas de los encargos cubran las 247 del plan madre una a una.**
  Cada microtarea cita su ID de origen entre paréntesis, pero no se corrió un cruce automático que
  demuestre que ninguna quedó afuera. El bloque C suma 256 porque cada carril agrega su propia
  línea base (H1.S1 de cada encargo, 4 o 5 microtareas), y H0 del plan madre se repartió entre esas
  líneas base y el carril de Pablo — ese reparto es una decisión de diseño, no un mapeo uno a uno
  verificado.
- Los dailies personales del área `Backend/` y los del bloque B no se tocaron: sus totales siguen
  siendo los de antes, y eso es correcto.

## Desvíos del plan

- **Dos conteos del plan resultaron equivocados y se corrigieron con el número medido**, no al
  revés: Marcelo quedó en **59** microtareas (el plan decía 58) y Pablo en **58** (el plan decía
  51, porque al escribir el encargo quedó claro que H0 global más H11, H13 y H14 no entraban en 51).
  Se actualizaron las dos tablas del plan, los DoD de `H1.S2.M4` y `H1.S2.M5`, y todos los totales
  derivados: bloque C de 248 a **256**, turno de 607 a **615**.
- **`check_totales.py` no se escribió como archivo aparte**: el conteo quedó como script embebido
  cuya salida está pegada en `evidencia/conteo-microtareas.txt`. El DoD de `H1.S3.M4` se corrigió
  para decir eso en vez de nombrar un archivo que no existe.
- El script `check_reservas.py` necesitó una corrección: imprimía una flecha Unicode que rompe en
  la consola de Windows (cp1252) y hacía morir el script **justo cuando encontraba una colisión**.
  Se reemplazó por ASCII y se agregó el caso a la autoprueba.

## Riesgos residuales

- **615 microtareas entre cinco personas no entran en un turno.** Está declarado a propósito en el
  daily del equipo (§7) y es lo que manda el README de `repartos/`: el encargo se escribe completo
  y ordenado por dependencia aunque sobre, y lo que no se cierre va `A MEDIAS`. El riesgo real es
  que alguien marque `HECHO` sin ejecutar el DoD para que el número quede mejor.
- **Tres bloques por persona y un solo trabajo activo (regla 70.1.1).** El orden A → B → C está en
  los seis dailies, pero nada lo hace cumplir automáticamente.
- **El área frontend tiene dos repos con reglas distintas — riesgo confirmado, no solo previsto.**
  Confundir `mantra-core-health` (sin reglas 91 y 98) con AportaYa/Pasanaku (con las dos) generó
  exactamente la confusión anticipada: Pablo, dueño de la decisión, leyó el turno y entendió que
  ambos bloques eran de Pasanaku. **Corrección 2026-09-21:** el bloque B de Pablo (`PR10`) se
  retargeteó al repo real de Pasanaku — ver `docs/trabajo/2026-09-21-correccion-bloque-b-pablo-pasanaku/`.
  Los bloques B de Richard, Justin, Leo y Marcelo (`PR6`–`PR9`) **siguen sin corregir** y tienen el
  mismo riesgo de lectura apurada; queda pendiente que el equipo decida si se corrigen igual.
- **El carril de Pablo es cuello de botella en los dos extremos**: su H2 entrega la línea base y los
  contratos que los otros necesitan, y su H5 es el cierre. Si su bloque A (backend, 54 microtareas)
  se come el turno, el bloque C de los otros cuatro arranca sin línea base.
- **Las entregas entre carriles pueden volverse espera.** Cada una trae su vía de cierre contra un
  doble (regla 65) y está escrito que ningún carril puede declararse `BLOQUEADO` por esperar a
  otro, pero eso depende de que lo apliquen.

## Decisiones y ambigüedades

**Decididas por Pablo en esta sesión:**

- **D-R1 · Lote extra, no turno nuevo.** Los cinco encargos van como segundo lote dentro de los
  carriles `Frontend/` existentes del turno noche del 2026-09-21, en vez de abrir
  `repartos/2026-09-22/`. Consecuencia asumida y declarada: el área frontend pasa a tener dos
  repositorios distintos y el turno pasa de 359 a 615 microtareas.
- **D-R2 · Corte por tema técnico** (sesión/auth · configuración y mocks · CI, macOS y release iOS ·
  fronteras y duplicación · contratos, autorización e idempotencia). Es el único corte que deja las
  reservas disjuntas: por app, el refresh y la configuración tocan las tres apps a la vez y dos
  personas se pisarían dentro del mismo hito; por fase, los carriles quedan encadenados.

**Ambigüedades que se arrastran:**

| ID | Ambigüedad | A quién confirmársela | Supuesto tomado |
|---|---|---|---|
| Q-R1 | Cada persona tiene ahora tres bloques y la regla 70.1.1 exige un trabajo activo por vez | Pablo | Orden A (backend) → B (mantra) → C (AportaYa); cada bloque se cierra o queda `A MEDIAS` con las cuatro respuestas antes de abrir el siguiente. Está escrito en los seis dailies |
| Q-R2 | 615 microtareas no entran en un turno | Pablo | El encargo se escribe completo y ordenado por dependencia; recortar alcance es decisión de coordinación **y se registra**, no se resuelve marcando `HECHO` lo no verificado |

Además, cada encargo arrastra sus propias ambigüedades hacia quien puede cerrarlas: Richard 4
(contrato del refresco por cookie, existencia del endpoint de auditoría, rotación del token,
cableado de providers), Justin 4 (origen propio en producción, contrato de observabilidad, qué es
"modo demo", quién carga los valores del despliegue), Leo 5 (minutos de macOS, secretos de firma
iOS, host del backoffice, soporte de la herramienta de integración, estrictez de la política de
contenido), Marcelo 5 (si el servidor sigue reenviando, nombre del package compartido, API del
plugin de fronteras, coordinación al mover imports, subir la versión del compilador) y Pablo 5
(enmienda del ADR, cuándo archivar el espejo, endpoint de auditoría, ejemplos del simulado, quién
hace la revisión independiente). Ninguna se resolvió por conveniencia: todas quedaron escritas con
su supuesto y su destinatario.
