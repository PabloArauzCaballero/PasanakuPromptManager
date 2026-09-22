# Reporte — Corregir el bloque B de Pablo (frontend) para que apunte a Pasanaku

> **AVANCE: 12 / 12 — 100 %.** ← `python .claude/hooks/plan_status.py --path PLAN.md` → `12/12 microtareas HECHO (100.0%)`

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` de este repo (sin commit; los
  cambios quedan en el árbol de trabajo)
- Peldaño de evidencia alcanzado: **`REGRESSION_VERIFIED`** para el artefacto documental corregido
  (los dos validadores del repo corridos después del cambio, con su código de salida pegado, y el
  `grep` de cierre que demuestra que no quedó ninguna referencia operativa a `mantra-core-health`).
  Sobre el **código del frontend de Pasanaku** nada cambió de peldaño: sigue en `DISCOVERED` — este
  trabajo corrigió documentos de reparto, no ejecutó ninguna microtarea de `PR10` ni de `PR15`.

## Completado

| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Cabecera de `PR10` corregida: repo `PasanakuBackend`/`PasanakuFrontend`, rama base `dev`, rama de trabajo `pablo/frontend/catalogo-ui` | `grep -n "Repo:" PR10-....md` | PASS — cita la URL real, ver `evidencia/verificacion.txt` |
| H1.S1.M2 | Tabla de comandos candidatos reemplazada por los reales de la raíz (`turbo run lint/typecheck/test:front/test:a11y/build`) y de los workspaces (`@aportaya/ui`, `@aportaya/backoffice`), verificados contra `package.json`/`turbo.json` reales, no inventados | `grep -c "turbo run" PR10-....md` | PASS — 5 líneas |
| H1.S1.M3 | Alcance IN/OUT y reservas retargeteados a `packages/ui/src/catalogo/**` (Angular) y `packages/diseno_flutter/lib/catalogo/**` (Flutter), confirmados como existentes en el árbol real | `grep -n "packages/ui/src/catalogo\|packages/diseno_flutter/lib/catalogo" PR10-....md` | PASS — aparecen en IN y en reservas |
| H1.S1.M4 | `AMB-F3` reescrita: ya no dice "hipótesis heredadas" sin más — aclara que son de `mantra-core-health` y que H1 del propio carril las redescubre contra Pasanaku antes de usarlas | lectura de la fila `AMB-F3` en `PR10` §5 | PASS |
| H1.S1.M5 | Reglas aplicables reevaluadas: 90 completa, 91 donde el catálogo cubra `campo-monto`/`desglose-de-cobro`/`cuenta-enmascarada`/`fila-de-movimiento` (confirmados en `packages/ui/src`), 98 condicionado a que una microtarea cruce un contrato de servicio | lectura de la sección 1 de `PR10` | PASS |
| H1.S2.M1 | Cabecera del bloque B en el daily de Pablo corregida al repo real, con nota de corrección fechada | `grep -n "Repo:" Pablo-Daily-....md` | PASS |
| H1.S2.M2 | `AMB-F2` actualizada en `docs/trabajo/2026-09-21-reparto-frontend-refactor/PLAN.md`: fila nueva que la marca resuelta para `PR10`, abierta para `PR6`–`PR9` | lectura de la fila añadida | PASS — no se borró la fila original, se agregó la actualización (regla 20 §6.7) |
| H1.S2.M3 | Riesgo residual de `docs/trabajo/2026-09-21-reparto-frontend-rescate/REPORTE.md` actualizado con la corrección y el alcance real | lectura de la sección de riesgos | PASS |
| H1.S2.M4 | Hallazgo registrado (ver "No cubierto" abajo): `PR6`–`PR9` con el mismo mismatch, sin corregir | — | PASS — este mismo documento |
| H1.S2 (extra, encontrado durante la verificación) | Dos referencias operativas más en el daily de Pablo (`mantra-core-health/` como carpeta a enlazar; "el bloque B es mantra-core-health" en la sección del bloque C) y una en `PR10` (carpeta de instalación del estándar) quedaron sin corregir en la primera pasada; se corrigieron al repetir el `grep` de cierre | `grep -n "mantra-core-health" Pablo-Daily-....md` antes/después | PASS — de 3 coincidencias operativas a 0; solo queda la línea explicativa de la corrección |
| H1.S3.M1 | `check_reparto.py` en verde tras el cambio | `python tools/check_reparto.py repartos/2026-09-21` | PASS — `exit=0`, `evidencia/verificacion.txt` |
| H1.S3.M2 | `check_skills_citadas.py` en verde tras el cambio | `python tools/check_skills_citadas.py` | PASS — `exit=0`, `evidencia/verificacion.txt` |
| H1.S3.M3 | Cero referencias operativas a `mantra-core-health`/`mdavila-2001` en los archivos de Pablo tocados (quedan solo las líneas que explican la corrección) | `grep -n "mantra-core-health\|mdavila-2001" repartos/.../Pablo/Pablo-Daily-....md` | PASS — 2 líneas, ambas explicativas; `grep "mockup" PR10` → vacío |

## A medias

ninguna.

## Pendiente

| ID | Estado | Qué lo destraba |
|---|---|---|
| Retargetear `PR6` (Richard), `PR7` (Justin), `PR8` (Leo) y `PR9` (Marcelo) al repo real de Pasanaku | `TODO` | Decisión del equipo/coordinación: son carriles de otras cuatro personas, fuera del alcance declarado de este trabajo (regla 00 §3). El mismo patrón de corrección aplicado acá a `PR10` es reutilizable. |
| Ejecutar de verdad las 38 microtareas de `PR10` contra `packages/ui/src/catalogo` y `packages/diseno_flutter/lib/catalogo` | `TODO` | Que se decida arrancar el bloque B como trabajo real (instalar Flutter si `CMD_FLUTTER_TEST` hace falta, correr H1 de auditoría, etc.). No se ejecutó ninguna microtarea real del carril en esta sesión: esto fue una corrección de documento, no la ejecución del turno. |

## Evidencia

Ver `evidencia/verificacion.txt` (comandos y salidas literales). Extracto:

```text
$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
exit=0

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 89 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)
exit=0

$ grep -n "mockup" .../PR10-CatalogoYGates.Frontend/CatalogoFielPreviewAisladoYGates.md
grep exit=1   # vacío = correcto
```

## No cubierto

- **`PR6`–`PR9` (Richard, Justin, Leo, Marcelo) siguen documentados contra `mdavila-2001/mantra-core-health`,
  un repo de salud ajeno a Pasanaku.** Es el mismo error que tenía `PR10` antes de esta corrección.
  No se tocaron porque el pedido de esta sesión fue específicamente "la sesión de Pablo" (regla 00
  §3, diff mínimo). El daily del equipo (`repartos/2026-09-21/PromptNoche/Daily-Noche-2026-09-21.md`)
  quedó con una nota que aclara que la excepción es solo la fila de Pablo.
- **Las rutas de microtarea dentro de `H2`–`H5` de `PR10`** (nombres de componentes, campos exactos
  de una ficha, estructura interna de `packages/ui/src/catalogo`) no se verificaron una por una
  contra el código real: eso es trabajo del propio `H1` del carril (auditoría), no de esta
  corrección de encabezado/alcance. Solo se confirmó que las dos carpetas raíz (`packages/ui/src/catalogo`,
  `packages/diseno_flutter/lib/catalogo`) existen.
- **No se ejecutó ninguna microtarea real de `PR10` ni de `PR15`** (no se clonó nada, no se corrió
  `turbo run lint`, no se instaló Flutter). Esta sesión corrigió documentos; la ejecución real del
  turno de Pablo (96 microtareas entre los dos bloques) es un trabajo aparte, mucho más grande, que
  no arrancó.
- **El toolchain de esta máquina no tiene Flutter/Dart en PATH** (confirmado en una sesión anterior,
  memoria del proyecto): `CMD_FLUTTER_TEST` de la tabla corregida no se pudo probar que funcione.

## Desvíos del plan

- El plan original preveía "0 referencias a mantra-core-health" como DoD de `H1.S1`. El primer
  `grep` de cierre encontró que quedaban 3 líneas operativas sin corregir (carpeta de instalación
  del estándar en `PR10` y en el daily de Pablo, y la frase "el bloque B es mantra-core-health" en
  la descripción del bloque C). Se corrigieron antes de cerrar — quedó registrado como microtarea
  extra en la sección "Completado" en vez de ocultarlo.
- Se afirmó una vez, sin verificar, que `PasanakuBackend` "trae su propio `AGENTS.md`". Se comprobó
  (`ls AGENTS.md CLAUDE.md` → no existen) y se corrigió el texto antes de cerrar, para no dejar una
  afirmación sin evidencia (regla 00 §1.3).

## Riesgos residuales

- Los cuatro carriles sin corregir (`PR6`–`PR9`) pueden ejecutarse tal cual están hoy contra
  `mantra-core-health` por error, si alguien no lee la nota agregada en el daily del equipo.
- Las citas de archivo de nivel de microtarea en `PR10` (`H2`–`H5`) siguen siendo, en su mayoría,
  descripciones genéricas heredadas de la plantilla — quedan sujetas a que H1 del propio carril las
  confirme antes de usarlas, tal como ya exigía la regla 00 antes de esta corrección.

## Decisiones y ambigüedades

- **Resuelta en esta sesión:** `AMB-F2`, solo para el carril de Pablo (`PR10`) — Pablo confirmó que
  el bloque B es trabajo de Pasanaku, no de `mantra-core-health`. Registrado como fila nueva en
  `docs/trabajo/2026-09-21-reparto-frontend-refactor/PLAN.md` sin borrar la fila original.
- **Sigue abierta:** si `PR6`–`PR9` se corrigen con el mismo criterio. A quién confirmársela:
  Pablo/coordinación, cuando decida si vale la pena para los otros cuatro carriles.
- **Supuesto tomado, no confirmado:** que el "documento antecedente" que originó `PR10` (mencionado
  en `AMB-F3`) es una plantilla de estructura y no contiene una decisión de negocio específica de
  Pasanaku que debiera preservarse literal. Se trató como plantilla, según lo dicho por Pablo en
  esta sesión ("alovida era simplemente guía... ajustado a este proyecto").
