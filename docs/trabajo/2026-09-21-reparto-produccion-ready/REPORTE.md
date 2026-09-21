# Reporte — Reparto en carriles del plan "dev → production ready"

> **AVANCE: 10 / 10 — 100 %.**

- Fecha: 2026-09-21 · Plan: [PLAN.md](./PLAN.md) · Rama(s): `main` de este repo (sin commit: no se pidió); el backend no se tocó
- Peldaño de evidencia alcanzado: `VERIFIED` para el artefacto documental (los dos validadores del repo ejecutados sobre el reparto, salida abajo). Sobre el backend, nada cambia de peldaño: sigue en `DISCOVERED`.

## Completado
| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | Árbol `repartos/2026-09-21/PromptNoche/{Richard,Justin,Leo,Marcelo,Pablo}/<Lote>.<Modulo>/{entregables,evidencia}` | `find repartos/2026-09-21 -type d \| wc -l` | `22` (≥ 16) |
| H1.S1.M2 | Encargo de Richard — `identidad`: challenge MFA con propósito, evidencia step-up, arranque seguro (3 H · 9 S · 28 M) | `python tools/check_reparto.py repartos/2026-09-21` | OK, no lo nombra |
| H1.S1.M3 | Encargo de Justin — `nucleo-financiero`: idempotencia con scope, MFA step-up con doble, doble aprobación, proveedor (4 H · 13 S · 42 M) | ídem | OK |
| H1.S1.M4 | Encargo de Leo — plataforma: helper `Idempotencia`, outbox que publica, guardas comunes, barridos (4 H · 13 S · 49 M) | ídem | OK |
| H1.S1.M5 | Encargo de Marcelo — transversal: inventario, `aportes`, ledger, base, PIT, código muerto (6 H · 11 S · 40 M) | ídem | OK |
| H1.S1.M6 | Encargo de Pablo — CI, supply chain, borde, carga, cierre (5 H · 17 S · 54 M) | ídem | OK |
| H1.S2.M1 | 5 dailies personales con enlace a su encargo y tabla de hitos con conteos reales | `ls repartos/2026-09-21/PromptNoche/*/*-Daily-Noche-2026-09-21.md \| wc -l` | `5` |
| H1.S2.M2 | Daily del equipo: §1 conteos (22 H · 63 S · 213 M), §2 orden de arranque (Spotless, plantilla de perfiles) y ritual `dev`→`test`, §3 esperas → dobles en tres niveles, §4 reservas disjuntas, §5 ambigüedades | revisión | Toda espera tiene doble o `DECISION_REQUIRED`; ninguna ruta con dos dueños |
| H1.S2.M3 | Validadores | `python tools/check_reparto.py repartos/2026-09-21 && python tools/check_skills_citadas.py` | exit 0 ×2 (salida abajo) |
| H1.S2.M4 | Este `REPORTE.md` | `python .claude/hooks/plan_status.py` | `10/10` |

## A medias
ninguna.

## Pendiente
| ID | Estado | Qué lo destraba |
|---|---|---|
| — | — | ninguna microtarea de este trabajo. Lo pendiente es el **turno en sí**: 213 microtareas en `NOT_RUN` repartidas en cinco carriles, que arrancan por el baseline de cada módulo |

## Evidencia
```text
$ python tools/check_reparto.py repartos/2026-09-21
check_reparto: OK, 2026-09-21 cumple la estructura obligatoria
exit=0

$ python tools/check_skills_citadas.py
check_skills_citadas: OK, 52 skill(s) distinta(s) citada(s), 0 inexistentes (de 194 en disco)
exit=0

$ for f in */*/*.md; do ... grep -cE "^\| *H[0-9]+\.S[0-9]+\.M[0-9]+ *\|" ...; done   (en repartos/2026-09-21/PromptNoche)
Richard : hitos=3 subtareas=9  micro=28
Justin  : hitos=4 subtareas=13 micro=42
Leo     : hitos=4 subtareas=13 micro=49
Marcelo : hitos=6 subtareas=11 micro=40
Pablo   : hitos=5 subtareas=17 micro=54
```

## No cubierto
- El validador comprueba **estructura y contenido mínimo, no calidad** (README de `repartos/`): que un DoD sea ejecutable de verdad en el backend solo se sabrá al correrlo en el turno.
- Las reservas de archivos se revisaron a mano cruzando los cinco encargos y el daily §4; no hay script que lo verifique.
- Ninguna microtarea del backend se ejecutó: el baseline real del SHA `19a621e6` sigue siendo desconocido (H1 de cada encargo lo produce).

## Desvíos del plan
- El plan madre tenía 210 microtareas; el reparto queda en 213: se agregó un baseline por módulo (5) y se fundieron dos filas al repartir por dueño de archivo (los IDOR de `identidad`/`nucleo` pasan al dueño del servicio en vez de a Marcelo). Trazabilidad ID a ID en la cabecera "Plan madre" de cada encargo.
- Se creó un plan propio para este trabajo (`docs/trabajo/2026-09-21-reparto-produccion-ready/`) en vez de extender el del backend: son dos trabajos con entregables distintos (regla 70.1.1, el anterior ya estaba cerrado con su reporte).

## Riesgos residuales
- **Carga desigual**: Pablo 54 y Leo 49 microtareas contra Richard 28. Es deliberado (plataforma y CI son ruta crítica y de un solo dueño por conflicto cero), pero si el turno se acorta, lo que no cierre va `A MEDIAS`; nadie toma archivos ajenos para "ayudar".
- **Archivos compartidos por micro-PR** (`sql/` generado, `libs.versions.toml`, `buildSrc/`, `_Arquitectura.md`, `docs/Seguridad.md`, `Entornos y despliegue.md`): cinco personas los tocan en la misma noche; el protocolo "un commit, merge en la hora, todos rebasean" depende de disciplina, no de un candado.
- **Merge sin CI verde**: como `dev` no tiene protección y el pedido es autonomía total, la condición de merge es el gate local del módulo. Un test ajeno roto en `dev` se detecta por el CI después del merge, no antes.
- **Windows**: el clon exige `core.longpaths=true` (rutas largas en `docs/Modelos/`); no está en los encargos porque no se sabe qué máquina usa cada uno — va como hallazgo en el daily del equipo si alguien lo sufre.

## Decisiones y ambigüedades
- **AMB-R1** — "pushear a dev y test": se interpretó `test` como **espejo de `dev`** (`git push origin origin/dev:test` tras cada merge), porque hoy ambas ramas apuntan al mismo SHA. Confirmar: Pablo. Si `test` tuviera vida propia, el ritual cambia en los cinco encargos (una línea).
- **Protección de ramas**: única microtarea `BLOQUEADO` del turno (Pablo H2.S5.M3, `DECISION_REQUIRED`). No se simula porque es una acción sobre algo compartido, no un contrato; el documento y los comandos quedan listos.
- **Contrato del JWT step-up** fijado por escrito e idéntico en los encargos de Richard y Justin para que ninguno espere al otro; cambiarlo durante el turno está prohibido en ambos.
- Las AMB-2…AMB-12 del plan madre se arrastran con su supuesto en el daily del equipo §5 y en cada encargo §5; ninguna se presentó como hecho.
