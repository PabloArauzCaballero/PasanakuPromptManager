# Plan — Conflictos y merges bloqueados en todos los repos

- Fecha: 2026-09-22 · Repos afectados: `PasanakuBackend`, `mantra-core-health`, `EcomicDataCenter`, `AtlasBackend` · Predecesor: `INVENTARIO-PENDIENTES-2026-09-21.md`
- Resultado observable: quien abra la lista de PRs de esos cuatro repos ya no ve ninguno en `CONFLICTING/DIRTY`, y los `BLOCKED` de AtlasBackend tienen su causa raíz demostrada y registrada.
- Kill-test: `gh pr list -R <repo> --json number,mergeable` sigue devolviendo `CONFLICTING` en algún PR ⇒ esto NO está hecho.
- Orden de ejecución: **de menor a mayor tamaño**, a pedido explícito del usuario. H1.S1 (2 archivos) → H1.S2 (1) → H1.S3 (3) → H3 (diagnóstico) → H2 (42 conflictos).

## Encuadre — hechos del descubrimiento (fase 1)

Barrido de **88 repos** bajo `Entrypoint-GitHUb` (`find -maxdepth 4 -name .git`) y de **52 remotos** únicos.

Hechos confirmados por comando, no supuestos:

1. **Cero conflictos locales.** Ningún repo tiene `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`,
   `rebase-merge`, `rebase-apply` ni archivos en `--diff-filter=U`.
2. **4 PRs en `CONFLICTING/DIRTY`** (tamaño medido con `git merge-tree --write-tree`).
3. **7 PRs en `BLOCKED` en AtlasBackend**: `mergeable=MERGEABLE`, o sea **no es conflicto**.
   Están bloqueados por checks requeridos en rojo.
4. `PabloArauzCaballero/aportayaDoc` **redirige** a `PabloArauzCaballero/PasanakuBackend`
   (`gh api repos/.../aportayaDoc --jq .full_name`). Los PR #5/#6 que aparecían dos veces en el
   barrido son **el mismo par**, no duplicados.
5. Otros 5 PRs están en `UNSTABLE`: mergeables, con checks en rojo o pendientes.
   Fuera de alcance (no son ni conflicto ni `BLOCKED`).

## Alcance

- **IN:**
  - Resolver el conflicto de merge de los 4 PRs `CONFLICTING` y **pushear a la rama del PR**.
  - Diagnosticar la causa raíz de los 7 `BLOCKED` de AtlasBackend y corregir lo que esté dentro
    del alcance de un arreglo demostrable.
- **OUT:**
  - **Mergear los PRs.** Decisión explícita del usuario: quedan `MERGEABLE` para que su autor
    revise y mergee. No se toca `dev` ni `main` de ningún repo.
  - Los PRs en `UNSTABLE` (`AtlasAdminPortal#20`, `EcomicDataCenter#110/#109/#106`,
    `PasanakuBackend#5`): no están bloqueados por conflicto.
  - Refactor, reformateo o mejora de cualquier código tocado al resolver. Solo se concilian las
    dos versiones en conflicto.
  - Las ramas locales atrasadas respecto de su upstream: estar atrasado no es un conflicto.
- **Ambigüedades registradas:**
  1. **`mantra-core-health#381` tiene borrados cruzados**: `dev` borró `features/consultation/*`
     y la rama borró `my-profile/work-history/*`. Cuál de los dos borrados es el deliberado es
     una **decisión de producto**, no técnica. Supuesto a tomar: *el borrado más reciente de cada
     lado gana*, verificado commit por commit contra el historial de cada archivo. A confirmar
     con el dueño del carril C antes de mergear.
  2. **`EcomicDataCenter#97` toca `macro-annual-sectors.json`**, un catálogo sembrado. Rige la
     regla 97.4: **prohibido inventar valores**. Supuesto: la resolución es unión de ambos
     conjuntos de indicadores sin alterar ni un valor; si las dos ramas dan valores distintos
     para el mismo indicador, se registra como bloqueo y no se elige por conveniencia.

## H1 — Los tres conflictos chicos quedan mergeables

**CA:** Dado los PRs `PasanakuBackend#6`, `mantra-core-health#435` y `EcomicDataCenter#97`, cuando
se consulta su estado en GitHub, entonces los tres reportan `mergeable=MERGEABLE` y ninguno
`CONFLICTING`.
**DoD:** `gh pr view <n> -R <repo> --json mergeable,mergeStateStatus` por cada uno, salida pegada
en `evidencia/`. Ningún marcador `<<<<<<<` en el árbol commiteado.
**Estado:** HECHO

### H1.S1 — PasanakuBackend#6 (`leo/frontend/ci` → `dev`)

Dos archivos de configuración en `add/add`: `.github/CODEOWNERS` y `.github/dependabot.yml`.
**CA:** El PR pasa a `MERGEABLE` y los dos archivos contienen las reglas de ambas ramas sin perder
ninguna entrada.
**DoD:** `gh pr view 6 -R PabloArauzCaballero/PasanakuBackend --json mergeable` → `MERGEABLE`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Traer `dev` a la rama `leo/frontend/ci` y dejar el merge en conflicto | El índice reporta exactamente 2 rutas en `U` | `git diff --name-only --diff-filter=U` → 2 líneas | HECHO |
| H1.S1.M2 | Conciliar `.github/CODEOWNERS` uniendo las reglas de las dos ramas | Sin marcadores y conserva toda regla de cualquiera de los dos lados | `grep -c '<<<<<<<'` → 0 | HECHO |
| H1.S1.M3 | Conciliar `.github/dependabot.yml` uniendo los `updates` de las dos ramas | YAML válido y sin marcadores | `python -c "import yaml;yaml.safe_load(open(...))"` → sin excepción | HECHO |
| H1.S1.M4 | Commitear el merge y pushear a `leo/frontend/ci` | El remoto tiene el commit de merge | `gh pr view 6 --json mergeable` → `MERGEABLE` | HECHO |

### H1.S2 — mantra-core-health#435 (`claude/encuestas-surveymonkey` → `dev`)

Un solo archivo: `src/app/shared/components/organisms/content-dialog/content-dialog.ts`.
**CA:** El PR pasa a `MERGEABLE` conservando tanto el cambio de `dev` como el de la rama.
**DoD:** `gh pr view 435 -R mdavila-2001/mantra-core-health --json mergeable` → `MERGEABLE`.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S2.M1 | Traer `dev` a la rama y dejar el merge en conflicto | El índice reporta exactamente 1 ruta en `U` | `git diff --name-only --diff-filter=U` → 1 línea | HECHO |
| H1.S2.M2 | Conciliar `content-dialog.ts` conservando ambos comportamientos | Sin marcadores y el archivo compila en su contexto | typecheck del repo → exit 0 | HECHO |
| H1.S2.M3 | Commitear y pushear a `claude/encuestas-surveymonkey` | El PR deja de estar en conflicto | `gh pr view 435 --json mergeable` → `MERGEABLE` | HECHO |

### H1.S3 — EcomicDataCenter#97 (`feat/sector-indicators` → `main`)

Tres archivos, uno de ellos catálogo sembrado. **Rige la regla 97.4.**
**CA:** El PR pasa a `MERGEABLE` sin que ningún valor del catálogo haya sido inventado ni alterado.
**DoD:** `gh pr view 97 -R PabloArauzCaballero/EcomicDataCenter --json mergeable` → `MERGEABLE`,
más el conteo de indicadores antes y después de la unión.
**Estado:** HECHO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H1.S3.M1 | Traer `main` a la rama y dejar el merge en conflicto | El índice reporta exactamente 3 rutas en `U` | `git diff --name-only --diff-filter=U` → 3 líneas | HECHO |
| H1.S3.M2 | Comparar los dos lados de `macro-annual-sectors.json`: claves solo-main, solo-rama y divergentes | La lista de claves divergentes está escrita en `evidencia/` | script de diff de claves → salida pegada | HECHO |
| H1.S3.M3 | Conciliar el JSON como unión, **sin tocar ningún valor**; si hay clave divergente, no elegir y declarar `BLOQUEADO` | `claves(resultado) == claves(main) ∪ claves(rama)` y ningún valor difiere de su origen | script de verificación de unión → `OK` | HECHO |
| H1.S3.M4 | Conciliar `boot-seed.macro-annual-history.ts` y `macro-annual-history.schema.ts` | Sin marcadores y el typecheck pasa | typecheck del repo → exit 0 | HECHO |
| H1.S3.M5 | Commitear y pushear a `feat/sector-indicators` | El PR deja de estar en conflicto | `gh pr view 97 --json mergeable` → `MERGEABLE` | HECHO |

## H2 — mantra-core-health#381 queda mergeable con los supuestos registrados

42 conflictos, con borrados en ambos sentidos. Es el hito de mayor riesgo del trabajo.
**CA:** Dado el PR #381, cuando se consulta su estado, entonces reporta `MERGEABLE`, el typecheck
y los tests dirigidos del área tocada pasan, y cada decisión de borrado cruzado está registrada
con el commit que la respalda.
**DoD:** `gh pr view 381 --json mergeable` → `MERGEABLE` · typecheck exit 0 · suite del área en
verde, salida pegada · tabla de decisiones de borrado en el `REPORTE.md`.
**Estado:** TODO

### H2.S1 — Decidir los borrados cruzados con evidencia del historial

**CA:** Para cada archivo en `modify/delete`, está escrito qué lado borró, en qué commit, con qué
fecha y mensaje, y cuál gana.
**DoD:** Tabla completa en `evidencia/381-borrados-cruzados.md`, una fila por archivo.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Listar los archivos en `modify/delete` y de qué lado vino el borrado | La lista tiene las 7 rutas del `merge-tree` | `git merge-tree ... \| grep 'modify/delete'` → salida pegada | TODO |
| H2.S1.M2 | Fechar el borrado de `features/consultation/*` en `dev` | Commit, fecha y mensaje escritos | `git log --diff-filter=D --format='%h %ad %s' -- <ruta>` → salida pegada | TODO |
| H2.S1.M3 | Fechar el borrado de `my-profile/work-history/*` en la rama | Commit, fecha y mensaje escritos | `git log --diff-filter=D --format='%h %ad %s' -- <ruta>` → salida pegada | TODO |
| H2.S1.M4 | Escribir la tabla de decisión con el supuesto y a quién confirmárselo | Cada fila dice qué gana y por qué | el archivo existe y no tiene filas vacías | TODO |

### H2.S2 — Resolver los 42 conflictos

**CA:** El árbol commiteado no tiene ningún marcador de conflicto y el typecheck pasa.
**DoD:** `grep -rn '<<<<<<<' src/` → 0 · typecheck exit 0.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S2.M1 | Traer `dev` a la rama y dejar el merge en conflicto | El índice reporta las rutas en `U` esperadas | `git diff --name-only --diff-filter=U \| wc -l` → salida pegada | TODO |
| H2.S2.M2 | Aplicar las decisiones de borrado de H2.S1 | Ningún archivo en `modify/delete` queda sin resolver | `git diff --diff-filter=U --name-only \| grep -c 'work-history\|consultation'` → 0 | TODO |
| H2.S2.M3 | Conciliar los conflictos de configuración (`.claude/settings.json`, `.gitignore`, `icons.md`) | Sin marcadores y el JSON parsea | `python -c "import json;json.load(open(...))"` → sin excepción | TODO |
| H2.S2.M4 | Conciliar el árbol de accesos (`core/navigation/*`, `dashboard/access-tree/*`) | Sin marcadores en esas rutas | `grep -rc '<<<<<<<' <rutas>` → 0 | TODO |
| H2.S2.M5 | Conciliar `features/account/*` | Sin marcadores en esas rutas | `grep -rc '<<<<<<<' src/app/features/account` → 0 | TODO |
| H2.S2.M6 | Conciliar `features/agenda/*` y `shell-layout` | Sin marcadores en esas rutas | `grep -rc '<<<<<<<' <rutas>` → 0 | TODO |
| H2.S2.M7 | Typecheck del proyecto completo | Exit 0 | typecheck del repo → exit 0, salida pegada | TODO |

### H2.S3 — Verificar y publicar

**CA:** Los tests dirigidos del área tocada pasan y el PR queda `MERGEABLE`.
**DoD:** salida del runner pegada · `gh pr view 381 --json mergeable` → `MERGEABLE`.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H2.S3.M1 | Correr los specs de las áreas tocadas | Todos en verde, o el rojo clasificado según regla 80.4 | runner del repo sobre esas rutas → salida pegada | TODO |
| H2.S3.M2 | Commitear y pushear a `carril-c/motor-de-sintomas` | El PR deja de estar en conflicto | `gh pr view 381 --json mergeable` → `MERGEABLE` | TODO |

## H3 — Los 7 `BLOCKED` de AtlasBackend tienen causa raíz demostrada

Cinco PRs de Dependabot (#40, #42, #43, #44, #45) fallan **los mismos tres checks**; #24 y #46
fallan otros. Hipótesis a falsar: la causa es común y vive en la base, no en cada bump.
**CA:** Dado cada uno de los 7 PRs, cuando se pregunta por qué está bloqueado, entonces hay una
causa demostrada con evidencia (log del check), clasificada según la regla 80.4, y las que se
pueden corregir dentro del alcance están corregidas y re-verificadas.
**DoD:** tabla PR × check × clase × causa en el `REPORTE.md`, con el enlace al log de cada fallo.
**Estado:** TODO

### H3.S1 — Reproducir y clasificar

**CA:** Cada check en rojo tiene su clase (`PRODUCT_BUG`, `TEST_BUG`, `ENVIRONMENT`, `DATA`,
`EXTERNAL`) respaldada por el log, no por intuición.
**DoD:** `evidencia/atlasbackend-checks.md` con una fila por (PR, check) en rojo.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H3.S1.M1 | Bajar el log del check `gitleaks` de un PR de Dependabot | El log está en `evidencia/` y nombra el hallazgo | `gh run view <id> --log-failed` → salida pegada | TODO |
| H3.S1.M2 | Bajar el log de `yarn audit (high/critical)` | El log nombra el paquete y el CVE | `gh run view <id> --log-failed` → salida pegada | TODO |
| H3.S1.M3 | Bajar el log de `migraciones + seeders + smoke` | El log nombra el paso que falla | `gh run view <id> --log-failed` → salida pegada | TODO |
| H3.S1.M4 | Comprobar si los mismos tres checks fallan en `main` sin ningún PR | Binario: fallan en main / no fallan | `gh run list --branch main --json conclusion,name` → salida pegada | TODO |
| H3.S1.M5 | Clasificar cada fallo según regla 80.4 con su evidencia | Ninguna fila sin clase ni sin log | el archivo existe, sin celdas vacías | TODO |
| H3.S1.M6 | Bajar y clasificar los fallos propios de #24 y #46 | Cada uno con su causa nombrada | `gh run view <id> --log-failed` → salida pegada | TODO |

### H3.S2 — Corregir lo que esté dentro de alcance

**CA:** Todo fallo clasificado como corregible tiene su arreglo aplicado y el check re-corrido en
verde; lo que no, queda `BLOQUEADO` con qué lo destraba y de quién depende.
**DoD:** `gh pr checks <n>` con los checks antes en rojo ahora en verde, salida pegada.
**Estado:** TODO

| ID | Microtarea | CA (binario) | DoD (comando de verificación) | Estado |
|---|---|---|---|---|
| H3.S2.M1 | Aplicar el arreglo de la causa común (se define al cerrar H3.S1; no se adivina antes) | El check antes en rojo pasa a verde en al menos un PR | `gh pr checks <n>` → salida pegada | TODO |
| H3.S2.M2 | Re-verificar los 5 PRs de Dependabot tras el arreglo | Cada uno reporta su `mergeStateStatus` actualizado | `gh pr view <n> --json mergeStateStatus` ×5 → salida pegada | TODO |
| H3.S2.M3 | Registrar como `BLOQUEADO` lo que exceda el alcance | Ningún fallo queda sin destino declarado | el `REPORTE.md` no tiene fallos huérfanos | TODO |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Resolver mal un borrado cruzado en #381 resucita código que el equipo borró a propósito | Alto — se reintroduce una feature retirada | H2.S1 fecha cada borrado contra el historial antes de decidir; la decisión queda escrita y se confirma con el dueño del carril antes de mergear |
| `macro-annual-sectors.json` tiene el mismo indicador con valores distintos en cada rama | Alto — elegir uno es inventar un dato (regla 97.4) | H1.S3.M3 detiene y declara `BLOQUEADO` en vez de elegir |
| No hay toolchain local (Node/yarn) para correr typecheck y tests de estos repos | Medio — el peldaño se queda en `WRITTEN` | Se verifica con lo que haya; si falta, se declara el peldaño real y se apoya en el CI del PR |
| Pushear a ramas de PR ajenas (`leo/`, `carril-c/`, `claude/`) pisa trabajo en curso de otro | Alto | Solo commit de merge, nunca `push --force`; se avisa en el PR qué se resolvió y con qué criterio |
| Los 7 `BLOCKED` de AtlasBackend dependen de secretos o infraestructura de CI | Medio | Regla 65: si el bloqueo es de otro, se aísla y se declara; no se detiene el resto del trabajo |
