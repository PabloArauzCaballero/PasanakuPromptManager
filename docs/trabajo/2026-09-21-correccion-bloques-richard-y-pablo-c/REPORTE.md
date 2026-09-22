# Reporte — Corregir el bloque B y C de Richard, y cerrar los rastros que quedaron en el C de Pablo

> **AVANCE: 15 / 15 — 100 %.** ← `python .claude/hooks/plan_status.py --path PLAN.md` → `15/15 microtareas HECHO (100.0%)`

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` de este repo (sin commit; los
  cambios quedan en el árbol de trabajo)
- Peldaño de evidencia alcanzado: **`REGRESSION_VERIFIED`** para el artefacto documental corregido
  (los dos validadores del repo corridos después del cambio, con su código de salida pegado, y el
  `grep` de cierre sobre los cuatro archivos tocados). Sobre el **código del frontend de Pasanaku**
  nada cambió de peldaño: sigue en `DISCOVERED` — no se ejecutó ninguna microtarea real de `PR6` ni
  de `PR11`.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Cabecera de `PR6` (bloque B de Richard) corregida: repo `PasanakuBackend`/`PasanakuFrontend`, rama `dev`, rama de trabajo `richard/frontend/pantalla-piloto` | `grep -n "Repo:" PR6-....md` | PASS |
| H1.S1.M2 | Tabla de comandos reemplazada por los reales (`turbo run lint/typecheck/test:front/build`; `CMD_E2E` con los dos `test:e2e` reales de `apps/web` y `apps/backoffice`, confirmados en sus `package.json`) | `grep -c "turbo run" PR6-....md` | PASS — 3 líneas |
| H1.S1.M3 | Ritual de entrega retargeteado a `dev` (branch base, rebase, PR) | `grep -n "mockup" PR6-....md` | PASS — vacío |
| H1.S1.M4 | Reglas reevaluadas: 90 completa, 91 condicionada a la pantalla piloto elegida, 98 fuera salvo contrato entre servicios | lectura de la sección 1 | PASS |
| H1.S1.M5 | `AMB-F3`/`AMB-F5` actualizadas: rutas marcadas como de `mantra-core-health` (no confirmadas), integración contra `dev` | lectura de la sección 5 | PASS |
| H1.S1.M6 | Sección de instalación del estándar corregida a `PasanakuBackend/`; encontradas y corregidas dos líneas extra (`mockup` en el kill del H1.S1.M1 y en "otro carril que todavía no está en mockup") que no estaban en el plan original | `grep -n "mantra-core-health\|mockup" PR6-....md` | PASS — solo quedan 4 líneas explicativas de la corrección, ninguna operativa |
| H2.S1.M1 | Cabecera del bloque B en el daily de Richard corregida, con nota de corrección fechada | `grep -n "Repo:" Richard-Daily-....md` | PASS |
| H2.S1.M2 | Línea "otro repo, otras reglas" del bloque C de Richard corregida | lectura de la línea | PASS |
| H3.S1.M1 | Las dos líneas de `PR11` (bloque C de Richard) que decían "el bloque B es mantra-core-health" corregidas | `grep -n "mantra-core-health" PR11-....md` | PASS — 0 operativas |
| H3.S1.M2 | Las dos líneas de `PR15` (bloque C de Pablo) con el mismo problema corregidas — esto es lo que Pablo señaló como "faltó" en la sesión anterior | `grep -n "mantra-core-health" PR15-....md` | PASS — 0 operativas |
| H4.S1.M1 | Nota de corrección del bloque B en el daily del equipo ampliada de "solo Pablo" a "Pablo y Richard" | lectura de la nota | PASS |
| H4.S1.M2 | Fila de Richard en la tabla del bloque B marcada como retargeteada | lectura de la fila | PASS |
| H5.S1.M1 | `check_reparto.py` en verde tras los cuatro archivos tocados | `python tools/check_reparto.py repartos/2026-09-21` | PASS — `exit=0` |
| H5.S1.M2 | `check_skills_citadas.py` en verde | `python tools/check_skills_citadas.py` | PASS — `exit=0` |
| H5.S1.M3 | Barrido final sobre los 4 archivos: cero referencias operativas a `mantra-core-health`/`mockup` | `grep -rn "mantra-core-health\|mdavila-2001\|mockup" <4 archivos>` | PASS — 10 líneas, todas explicativas/históricas, `evidencia/verificacion.txt` |

## A medias

ninguna.

## Pendiente

| ID | Estado | Qué lo destraca |
|---|---|---|
| Retargetear `PR7` (Justin), `PR8` (Leo) y `PR9` (Marcelo), y sus bloques C (`PR12`–`PR14`) | `TODO` | Decisión de coordinación. Mismo patrón de corrección ya usado dos veces (`PR10` y `PR6`), reutilizable directamente. |
| Ejecutar de verdad las 24 microtareas de `PR6` y las 51 de `PR11` (75 en total, bloque B+C de Richard) contra el código real de Pasanaku | `TODO` | Que se decida arrancar el turno real. No se tocó ni un archivo de `apps/`, `packages/` ni `servicios/`: esto fue una corrección de documentos, no la ejecución del carril. |

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
  Avance: 15/15 microtareas HECHO  (100.0%)
```

## No cubierto

- **`PR7`–`PR9` (Justin, Leo, Marcelo) y sus bloques C (`PR12`–`PR14`) siguen sin corregir.** Mismo
  patrón que `PR6`/`PR10` tenían: repo `mdavila-2001/mantra-core-health`, rama `mockup`. Fuera de
  alcance de este pedido (regla 00 §3): nadie pidió esos tres carriles todavía.
- **No se verificó si `PR12`–`PR14` (los bloques C de Justin, Leo y Marcelo) tienen el mismo tipo de
  línea colgando que tenían `PR11` y `PR15`** ("el bloque B es mantra-core-health"). Es probable,
  por el patrón, pero no se comprobó con `grep` — no se tocó ninguno de esos tres archivos.
- **No se ejecutó ninguna microtarea real** de `PR6` ni de `PR11`: no se clonó nada, no se corrió
  `turbo run lint`, no se tocó ningún archivo de `apps/web`, `apps/backoffice` ni `nucleo/sesion*`.
- **Las rutas de nivel de microtarea de `PR6`** (qué pantalla piloto, qué componente, qué archivo
  exacto) no se verificaron contra el código real: esa es la propia H1 del carril (auditoría), tal
  como ya pasaba con `PR10`.

## Desvíos del plan

- El plan original usaba IDs de dos capas (`H1.M1`) en vez de las tres que exige la regla 20
  (`H<n>.S<n>.M<n>`). Lo detectó `python .claude/hooks/plan_status.py` al primer intento de cierre
  (`0/0 microtareas — 15 fila(s) sin contar`). Se corrigieron los 15 IDs a `H<n>.S1.M<n>` antes de
  marcar nada como `HECHO`, no después.
- `H1.S1.M6` encontró, al correr su propio `grep` de verificación, dos líneas más de `mockup` en
  `PR6` que no estaban listadas en el plan original (el kill-test implícito de `H1.S1.M1` y la
  frase "otro carril que todavía no está en mockup"). Se corrigieron dentro de la misma microtarea
  en vez de abrir una nueva, porque son parte del mismo DoD ("cero referencias operativas").

## Riesgos residuales

- Mismo riesgo que el trabajo predecesor: los carriles sin corregir (`PR7`–`PR9`, `PR12`–`PR14`)
  pueden ejecutarse por error contra `mantra-core-health` si alguien no lee las notas agregadas.
- La corrección de `PR6` es más genérica que la de `PR10`: no se ancló a un paquete real específico
  (como sí se hizo con `packages/ui/src/catalogo`) porque `PR6` no lo necesita — su propia H1.S2.M1
  es la que elige la pantalla piloto real. Si esa elección nunca se hace, el carril queda correcto
  en la forma pero sin ejecutar.

## Decisiones y ambigüedades

- Se reutilizó el criterio de `AMB-F2` ya sentado en el trabajo predecesor: la corrección aplica
  solo al carril pedido explícitamente (esta vez, Richard), no a los tres restantes.
- **Ambigüedad nueva, no resuelta:** si `PR12` (Justin), `PR13` (Leo) y `PR14` (Marcelo) —los
  bloques C de los otros tres— tienen el mismo tipo de línea colgona sobre "el bloque B es
  mantra-core-health" que tenían `PR11` y `PR15`. Supuesto tomado: probablemente sí, por el patrón
  observado dos veces seguidas, pero no se verificó. A quién confirmársela: quien decida si se
  corrigen `PR7`–`PR9`.
