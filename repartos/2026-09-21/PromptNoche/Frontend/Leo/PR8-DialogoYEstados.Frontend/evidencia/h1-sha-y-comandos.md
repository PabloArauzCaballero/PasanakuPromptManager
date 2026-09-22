# H1.S1.M1 y H1.S1.M2 — evidencia literal

## H1.S1.M1 — SHA, rama base, estado del árbol

`git status`/`git rev-parse` local están bloqueados para esta sesión contra el checkout
compartido de `PasanakuBackend` (ver bloqueo de entorno en `PR8-carril.md`). Evidencia obtenida
por las dos vías que sí funcionaron:

```text
$ cat .git/HEAD   # (dentro del checkout compartido de PasanakuBackend, vía Read, sin git)
ref: refs/heads/leo/feature/carril-PR3-plataforma

$ cat .git/refs/heads/leo/feature/carril-PR3-plataforma
a23bcb117effe7ce66d069a97ebd2c25c8390306

$ gh api repos/PabloArauzCaballero/PasanakuBackend/git/ref/heads/dev
{"ref":"refs/heads/dev", ... "object":{"sha":"a23bcb117effe7ce66d069a97ebd2c25c8390306", ...}}
```

**SHA base = `a23bcb117effe7ce66d069a97ebd2c25c8390306`** (idéntico en el checkout local y en
`origin/dev`, confirmado por dos fuentes independientes). `git status --short` **no se pudo
correr** en esta sesión — queda `A MEDIAS`, ver `PR8-carril.md`.

## H1.S1.M2 — tabla de comandos reales

Fuente: `package.json` raíz, `turbo.json`, `packages/ui/package.json`, `apps/web/package.json`,
`apps/backoffice/package.json` (leídos completos, no resumidos).

| Alias del encargo | Comando real confirmado | Existe |
|---|---|---|
| `CMD_LINT` | `turbo run lint` (root) / `yarn workspace @aportaya/ui lint` (scoped: `ng lint && python3 ../../scripts/verificar_frontend.py ui`) | Sí |
| `CMD_TYPECHECK` | `turbo run typecheck` (root) / `yarn workspace @aportaya/ui typecheck` (scoped: `tsc -p tsconfig.lib.json --noEmit && tsc -p tsconfig.spec.json --noEmit`) | Sí |
| `CMD_TEST` | `turbo run test:front` (root) | Sí |
| `CMD_UI_TEST` | `yarn workspace @aportaya/ui test:front` → `ng test --include='src/**/*.spec.ts' --exclude='src/**/*.a11y.spec.ts'` | Sí, confirmado literal (no había alias `test` a secas, tal como anticipaba el encargo) |
| `CMD_BUILD` | `turbo run build` | Sí |
| `CMD_E2E` | `yarn workspace @aportaya/backoffice test:e2e` → `playwright test` (los dos modales elegidos en H3.S2.M1 están en `apps/backoffice`) | Sí, script existe; no se ejecutó en esta sesión (bloqueo de entorno, no hay navegador orquestado) |

**Hallazgo real:** `turbo run <lo que sea>` sin `--filter` en la raíz **siempre falla** en este
entorno porque `@aportaya/movil` y `@aportaya/diseno-flutter` (Flutter) requieren los binarios
`dart`/`flutter`, que no están instalados en esta máquina — no es un defecto de código, es un
binario ausente del entorno de esta sesión, fuera de mi alcance (`apps/movil` no es IN de este
carril). Se usó `--filter=@aportaya/ui --filter=@aportaya/web --filter=@aportaya/backoffice
--continue` para acotar el comando a mi alcance real, y se registra acá como desvío del literal
del encargo (regla 00 §1.5: no hay patrón previo distinto, se documenta la decisión).
