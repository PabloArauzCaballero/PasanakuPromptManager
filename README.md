# PasanakuPromptManager

Estándar de ingeniería, diseño y operación de Pasanaku, escrito como skills de Claude Code.

No es una colección de apuntes: es el manual de la casa. Cada skill dice **qué hacer**, **cómo
comprobarlo** y **qué evidencia hace falta** para poder afirmar que está hecho. Son reutilizables
entre proyectos, pero están escritas para lo que Pasanaku realmente es: una **fintech de grupos de
pasanaku**, construida como **microservicios**, que administra **dinero de terceros**.

## Empezá acá

**[`skills-router`](.claude/skills/skills-router/SKILL.md)** — el índice. Mapea la situación
concreta (arrancar una tarea, tocar un endpoint, mover dinero, cruzar un límite de servicio,
diseñar una pantalla, desplegar, cerrar un carril) a la skill que hay que cargar, y fija la
precedencia cuando dos se contradicen.

Con 194 skills, leer el catálogo entero no sirve. El router sí.

## Cómo se usa

Copiá o enlazá `.claude/skills/` dentro del repo donde estés trabajando. Claude Code las carga
sola cuando la `description` matchea la tarea; también podés invocarlas por nombre.

Los **hechos de cada proyecto** (comandos reales, invariantes del modelo, prohibiciones, rutas)
no viven acá: viven en el `CLAUDE.md` de ese repo, y **mandan sobre cualquier skill**. Cómo
escribir ese archivo está en `claude-md-authoring`.

El modelo de datos de referencia —nueve módulos, con una ficha por entidad— vive en el repo
[`Pasanaco_backendBO`](../Pasanaco_backendBO/docs/Index.md). Las skills de dominio citan esas
entidades por su nombre real (`obligacion_aporte`, `entrega_fondo`, `cobertura_incumplimiento`…).

## Qué hay adentro

| Área | Cant. | Qué cubre |
|---|---|---|
| **Disciplina del agente** | 12 | Evidencia, anti-alucinación, alcance, causa raíz, cierre de turno. Los gates que mandan sobre todo lo demás. |
| **Oficio del repo** | 8 | Escribir skills, prompts, evals, subagentes, hooks, gobernanza. El manual de su propio producto. |
| **Microservicios** | 12 | Límites de servicio, contratos y versionado, sagas, gateway/BFF, resiliencia, traza distribuida, consistencia eventual, testing, despliegue independiente, seguridad entre servicios, integridad distribuida. |
| **Dominio dinero** | 9 | Movimiento de dinero, partida doble, QR y pasarela, conciliación, desembolsos, fondo de garantía, cobranza, disputas, cierre y reportería. |
| **Dominio Pasanaku** | 6 | Ciclo del grupo y sorteo verificable, calendario de aportes, KYC, cumplimiento y listas, transparencia y reputación, descubrimiento y emparejamiento. |
| **Backend** | 17 | Arquitectura, NestJS, MikroORM, PostgreSQL, concurrencia, errores, auth, multi-tenancy, colas, jobs, caché, notificaciones, archivos, búsqueda, tiempo real, mapas, moderación. |
| **Datos y modelo** | 7 | Esquema dirigido por modelo, PlantUML, seeds con procedencia, calidad, auditoría, backups, tooling Python. |
| **Frontend web** | 26 | Angular 21 + SSR, signals, formularios, componentes, CSS, diseño visual, calidad UI, accesibilidad, responsive, performance, i18n, SEO, Astro. |
| **Mobile** | 7 | Flutter: desarrollo, estado, tema, tests, offline, release. |
| **QA** | 20 | Estrategia, orquestación, unitarios, API, integridad, E2E, triage, datos sintéticos, casos límite, exploratorio, UAT, evidencia. |
| **Seguridad** | 15 | Guardrails, privacidad financiera, authn/authz, threat modeling, revisión con lente de seguridad, evaluación sobre sistemas propios, reporte y remediación. |
| **Calidad de código** | 10 | Clean code, SOLID, eficiencia, gates, linting, complejidad, deuda, código muerto, auditoría, code review. |
| **Proceso y GitHub** | 21 | Carriles, requisitos, slicing, bugs, git multi-repo, PRs, issues, rulesets, releases, ADRs, dependencias, incidentes. |
| **Despliegue** | 11 | Coolify, Docker, CI/CD, release y rollback, secretos, hardening, entorno Windows. |

## Las reglas que atraviesan todo

1. **Verificar es observar el artefacto real corriendo.** Leer el código no cuenta. Compilar no
   cuenta. Toda afirmación va con la salida literal pegada, y con la sección "No cubierto".
2. **No inventar.** Antes de crear una entidad, endpoint, catálogo o API, localizar el equivalente
   existente. Las ambigüedades se registran, no se resuelven por conveniencia.
3. **Diff mínimo.** Nada de refactors, renombres ni "aprovechadas" fuera de lo pedido.
4. **El dinero manda (regla 91).** Importes exactos con su moneda, idempotencia de punta a punta,
   el mayor no se edita, y nada se promete antes de estar cobrado. Si el cambio toca un importe,
   `money-movement-safety` aplica aunque nadie lo haya pedido.
5. **El límite de servicio manda (regla 98).** Un servicio es dueño de sus datos, los contratos se
   versionan, no hay transacciones distribuidas, y un E2E verde con todo sano no prueba nada: el
   cierre exige haber roto algo a propósito.
6. **Los datos de personas mandan.** Documento, cuenta bancaria, deuda e importes atribuibles no
   van a logs, URLs, trazas ni reportes (`data-privacy-financial`).
7. **Datos reales con procedencia, o sintéticos declarados.** Nunca datos ficticios presentados
   como reales, ni datos de producción en entornos de prueba.

## Estado

Las skills heredadas fueron verificadas contra documentación oficial al momento de escribirlas
(`angular.dev`, `docs.nestjs.com`, MikroORM, PostgreSQL/PostGIS, Playwright, `docs.github.com`,
`coolify.io/docs`, OWASP, W3C/WCAG, `web.dev`, `docs.flutter.dev`). Las skills de dominio
financiero y de microservicios están escritas contra el **modelo de datos de Pasanaku** y contra
patrones de arquitectura, no contra una implementación existente: cuando el repo de código exista,
hay que reverificarlas contra él.

**Lo que no está verificado y hay que confirmar con quien corresponda** está dicho explícitamente
en cada skill: los plazos, formatos y umbrales regulatorios (`regulatory-compliance-mapping`,
`aml-sanctions-screening`) los define el oficial de cumplimiento, no este repo.

Esto envejece. Antes de editar una skill, leé `prompt-governance-versioning`; antes de publicar el
cambio, `prompt-evals`.
