# Baseline real — H1.S1 (bloque B, `PR10-CatalogoYGates.Frontend`)

Ejecutado 2026-09-21 contra el clon real `Pasanaku/PasanakuFrontend`, rama `pablo/frontend/catalogo-ui`
creada desde `origin/dev`.

## H1.S1.M1 — Remoto, rama, SHA, estado del árbol

```text
$ git remote -v
origin  https://github.com/PabloArauzCaballero/PasanakuFrontend.git (fetch)
origin  https://github.com/PabloArauzCaballero/PasanakuFrontend.git (push)

$ git rev-parse HEAD
a23bcb117effe7ce66d069a97ebd2c25c8390306

$ git status --short
?? .claude/hooks/
?? .claude/rules/
```

Sin cambios ajenos en el árbol salvo la instalación del estándar (esperada, sin commitear).

## H1.S1.M2 — Comandos reales (confirmados, no candidatos)

```text
$ grep -A15 '"scripts"' package.json
  "lint": "turbo run lint",
  "typecheck": "turbo run typecheck",
  "test:front": "turbo run test:front",
  "test:a11y": "turbo run test:a11y",
  "build": "turbo run build",
```

`CMD_UI_TEST` real: `yarn workspace @aportaya/ui test:front` (no existe `test` a secas, confirmado
en `packages/ui/package.json`).

## H1.S1.M3 — Rojo previo (baseline de fallos), scope `packages/ui`

```text
$ yarn install --immutable
✔ Done with warnings in 19s 487ms (peer deps de @angular/forms y @angular/platform-browser
  incorrectamente resueltos en @aportaya/ui y @aportaya/tutoriales — preexistente, no lo causa este carril)

$ yarn workspace @aportaya/ui lint
exit=1
packages/ui/src/foco-de-tutorial/foco-de-tutorial.ts
  26:7  error  click must be accompanied by either keyup, keydown or keypress event for accessibility
  26:7  error  Elements with interaction handlers must be focusable
✖ 2 problems (2 errors, 0 warnings)
→ PREEXISTENTE. No es del catálogo (`foco-de-tutorial` está fuera del alcance de este carril).

$ yarn workspace @aportaya/ui typecheck
exit=0

$ yarn workspace @aportaya/ui test:front
exit=1
Test Files  1 failed | 13 passed (14)
Tests  1 failed | 46 passed (47)
FAIL src/monto/monto.spec.ts > ap-monto > pasa los mismos vectores que el Monto de Flutter
Error: Test timed out in 5000ms.
→ PREEXISTENTE. `monto.spec.ts` no es del catálogo (compara paridad con Flutter); no se tocó
  ningún archivo antes de correr este baseline.

$ yarn workspace @aportaya/ui build
exit=0
"ui: se consume por alias de tsconfig; `ng build` empaqueta con ng-packagr cuando haga falta publicar"
→ No produce un bundle medible por sí solo: el bundle real de `packages/ui` se mide desde
  `apps/web`/`apps/backoffice`, que lo consumen por alias de tsconfig. Pendiente (no se corrió el
  build completo de una app por tiempo — build de monorepo completo no ejecutado en esta sesión).
```

**Conclusión del baseline:** `packages/ui` tiene dos fallos preexistentes (1 de lint en
`foco-de-tutorial`, 1 de test en `monto.spec.ts`), ninguno de los dos dentro del alcance de este
carril (`packages/ui/src/catalogo/**`). Se registran como hallazgo (regla 00 §3: no se arreglan,
se avisa al dueño), no se tocan.

## No cubierto de este baseline

- Bundle size real (H1.S1.M4 del encargo): pendiente, requiere build de `apps/web` o
  `apps/backoffice` completo, no ejecutado por tiempo en esta sesión.
- `packages/diseno_flutter` (equivalente Flutter del catálogo): no se corrió ningún comando —
  Flutter no está en el PATH de esta máquina (confirmado en sesión anterior, ver memoria del
  proyecto). Bloqueado hasta que se instale, o se declara `BLOQUEADO` con esa causa si el turno
  real lo requiere.
