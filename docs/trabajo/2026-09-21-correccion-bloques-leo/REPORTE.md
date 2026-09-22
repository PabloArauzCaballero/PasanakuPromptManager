# Reporte — Corregir el bloque B de Leo y cerrar los rastros que quedan en su bloque C

> **AVANCE: 14 / 14 — 100 %.** ← `python .claude/hooks/plan_status.py --path PLAN.md` → `14/14 microtareas HECHO (100.0%)`

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` de este repo (sin commit; los
  cambios quedan en el árbol de trabajo)
- Peldaño de evidencia alcanzado: **`REGRESSION_VERIFIED`** para el artefacto documental corregido
  (los dos validadores del repo, con su código de salida pegado, y el `grep` de cierre sobre los
  tres archivos de Leo). Sobre el **código del frontend de Pasanaku** nada cambió de peldaño: sigue
  en `DISCOVERED` — no se ejecutó ninguna microtarea real de `PR8` ni de `PR13`.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Cabecera de `PR8` (bloque B de Leo) corregida: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `leo/frontend/dialogo-estados` | `grep -n "Repo:" PR8-....md` | PASS |
| H1.S1.M2 | Alcance IN retargeteado a `packages/ui/src/estado-de-pantalla`, `packages/ui/src/estado-vacio` y `packages/ui/src/dialogo`, confirmados como existentes en el árbol real | `grep -n "packages/ui/src/dialogo\|packages/ui/src/estado" PR8-....md` | PASS |
| H1.S1.M3 | Tabla de comandos reemplazada por los reales (`turbo run lint/typecheck/test:front/build`, `yarn workspace @aportaya/ui test:front`, `test:e2e` de `apps/web`/`apps/backoffice`), verificados contra `package.json`/`turbo.json` | `grep -c "turbo run" PR8-....md` | PASS — 3 líneas |
| H1.S1.M4 | Ritual de entrega retargeteado a `dev`; barrido encontró **3 referencias extra a `mockup`** no listadas en el plan original (DoD de H1, tabla H1.S1.M1, tabla H1.S2.M2) — corregidas dentro de la misma microtarea | `grep -n "mockup" PR8-....md` | PASS — vacío tras la corrección |
| H1.S1.M5 | Reglas reevaluadas: 90 completa, 91 condicionada a los dos modales de H3.S2.M1, 98 fuera salvo contrato entre servicios | lectura de la sección 1 | PASS |
| H1.S1.M6 | `AMB-F3`/`AMB-F5` y la sección de instalación del estándar corregidas | lectura de las secciones 1 y 5 | PASS |
| H2.S1.M1 | Cabecera del bloque B en el daily de Leo corregida, con nota fechada | `grep -n "Repo:" Leo-Daily-....md` | PASS |
| H2.S1.M2 | Línea "otro repo, otras reglas" del bloque C y sección de instalación del estándar corregidas | lectura de las dos líneas | PASS |
| H3.S1.M1 | Las dos líneas de `PR13` (bloque C de Leo) que decían "el bloque B es mantra-core-health" corregidas | `grep -n "mantra-core-health" PR13-....md` | PASS — 0 operativas |
| H4.S1.M1 | Nota de corrección del bloque B en el daily del equipo ampliada de "Pablo y Richard" a "Pablo, Richard y Leo" | lectura de la nota | PASS |
| H4.S1.M2 | Fila de Leo en la tabla del bloque B marcada como retargeteada | lectura de la fila | PASS |
| H5.S1.M1 | `check_reparto.py` en verde | `python tools/check_reparto.py repartos/2026-09-21` | PASS — `exit=0` |
| H5.S1.M2 | `check_skills_citadas.py` en verde | `python tools/check_skills_citadas.py` | PASS — `exit=0` |
| H5.S1.M3 | Barrido final sobre los tres archivos de Leo: cero referencias operativas | `grep -rn "mantra-core-health\|mdavila-2001\|mockup" <3 archivos>` | PASS — 8 líneas, todas explicativas, `evidencia/verificacion.txt` |

## A medias

ninguna.

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| Retargetear `PR7` (Justin) y `PR9` (Marcelo), y sus bloques C (`PR12`, `PR14`) | `TODO` | Decisión de coordinación. Mismo patrón de corrección ya usado tres veces (`PR10`, `PR6`, `PR8`), reutilizable directamente. |
| Ejecutar de verdad las 26 microtareas de `PR8` y las 52 de `PR13` (78 en total, bloque B+C de Leo) contra el código real de Pasanaku | `TODO` | Que se decida arrancar el turno real. No se tocó ningún archivo de `apps/`, `packages/` ni `servicios/`. |

## Evidencia

Ver `evidencia/verificacion.txt`. Extracto:

```text
$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
exit=0

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 89 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)
exit=0

$ python .claude/hooks/plan_status.py --path PLAN.md
  Avance: 14/14 microtareas HECHO  (100.0%)
```

## No cubierto

- **`PR7` (Justin) y `PR9` (Marcelo), y sus bloques C (`PR12`, `PR14`), siguen sin corregir.** Mismo
  patrón que tenían `PR6`, `PR8` y `PR10`. Fuera de alcance de este pedido (regla 00 §3).
- **No se verificó si `PR12` y `PR14` tienen la misma línea colgando** que tenían `PR11`, `PR13` y
  `PR15` antes de corregirse. Probable por el patrón (3 de 3 casos verificados la tuvieron), pero no
  comprobado — no se tocó ninguno de los dos archivos.
- **No se ejecutó ninguna microtarea real** de `PR8` ni de `PR13`: no se clonó nada, no se corrió
  `turbo run lint`, no se tocó ningún archivo de `apps/` ni de `packages/ui`.
- **Las rutas de nivel de microtarea de `PR8`** (qué modales exactos, qué variantes tiene el tipo de
  estado real) no se verificaron contra el código: esa es la propia H1 del carril.

## Desvíos del plan

- `H1.S1.M4` encontró, al correr su propio `grep` de verificación, **tres** referencias a `mockup`
  que no estaban en el plan original (el DoD del hito H1, la tabla de `H1.S1.M1` y la tabla de
  `H1.S2.M2`) — un patrón más grande que el de la corrección de Richard (que tuvo dos extra) y el de
  Pablo (que tuvo tres). Se corrigieron dentro de la misma microtarea, no como trabajo nuevo, porque
  son parte del mismo DoD ("cero referencias operativas a mockup").
- El plan usó desde el inicio IDs de tres capas (`H<n>.S1.M<n>`), aprendiendo del desvío detectado
  en el trabajo predecesor de Richard — no hizo falta corregirlo esta vez.

## Riesgos residuales

- Mismo riesgo que los dos trabajos predecesores: `PR7`, `PR9`, `PR12` y `PR14` pueden ejecutarse
  por error contra `mantra-core-health` si alguien no lee las notas agregadas.
- El patrón de "más referencias colgando de las previstas en el plan" se repitió en los tres
  carriles corregidos hasta ahora (3, luego 2, luego 3). Si se corrigen `PR7`/`PR9`, conviene un
  barrido `grep` completo del archivo **antes** de escribir el plan, no solo después.

## Decisiones y ambigüedades

- Se reutilizó el criterio ya sentado en los dos trabajos predecesores: la corrección aplica solo al
  carril pedido explícitamente (esta vez, Leo).
- **Ambigüedad que se arrastra** (ya registrada en el trabajo predecesor, sigue sin resolver): si
  `PR12` (Justin) y `PR14` (Marcelo) tienen el mismo tipo de línea colgando. Supuesto tomado:
  probablemente sí. A quién confirmársela: quien decida si se corrigen `PR7`/`PR9`.
