# Plan — Actualizar el estado real de los carriles de Justin

- Fecha: 2026-09-22 · Repos afectados: `PasanakuPromptManager`, `PasanakuBackend`, `PasanakuFrontend` · Predecesor: `2026-09-21-correccion-bloques-justin-y-marcelo`
- Resultado observable: los dailies de Justin y el daily de equipo separan con precisión lo integrado, lo verificado en esta sesión, lo pendiente y los cambios que aún no están en `dev`.
- Kill-test: un hito aparece como `HECHO` sin commit integrado y salida de prueba reproducida.

## Alcance

- IN: auditar PR2, PR7 y PR12 contra `origin/dev`; ejecutar sus gates dirigidos; actualizar los tres dailies, sus porcentajes y el daily del equipo; documentar los commits de corrección de PR12 que se reconcilien en una rama nueva.
- OUT: reescribir historia Git, mergear ramas compartidas, alterar contratos de negocio sin prueba roja, y convertir el encargo histórico de 2026-09-20 en trabajo activo.
- Ambigüedades registradas: el prompt original de PR2 quedó en `NOT_RUN` aunque hay commits integrados; se usa la evidencia actual de Git y los gates ejecutados, nunca se infiere un porcentaje por el mensaje de un commit.

## H1 — Evidencia actual de producto recopilada

**CA:** Dado cada carril de Justin, cuando se revisa su estado, entonces hay commit/rama y salida de gate que sustentan cada afirmación.
**DoD:** `git log` y los gates dirigidos quedan resumidos literalmente en `REPORTE.md`.
**Estado:** A MEDIAS

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H1.S1.M1 | Auditar PR2 contra `origin/dev` y correr sus tests dirigidos H2/H3 | Sin deducir estado desde el prompt | `./gradlew :servicios:nucleo-financiero:integrationTest --tests '*CU11*'` → salida registrada | BLOQUEADO |
| H1.S1.M2 | Confirmar que la rama de PR7 no difiere de `origin/dev` | No queda cambio huérfano de tabla | `git diff --quiet origin/dev origin/justin/frontend/tabla-datos` → 0 | HECHO |
| H1.S1.M3 | Reproducir y reconciliar en rama limpia los fixes pendientes de PR12 | Los tests objetivo fallan antes y pasan después | gates de Angular/Flutter dirigidos → salida registrada | A MEDIAS |

## H2 — Dailies y reporte dicen la verdad operativa

**CA:** Dado que un integrante abre cualquier daily de Justin, cuando mira avance y pendiente, entonces puede retomar el trabajo sin confundir código integrado con documentación preparada.
**DoD:** `python tools/check_reparto.py repartos/2026-09-21` y `python tools/check_skills_citadas.py` finalizan con exit 0.
**Estado:** A MEDIAS

| ID | Microtarea | CA | DoD | Estado |
|---|---|---|---|---|
| H2.S1.M1 | Actualizar daily backend PR2 con hitos y riesgos demostrados | Todo estado cita evidencia o queda `A MEDIAS` | revisión + enlaces a evidencia | HECHO |
| H2.S1.M2 | Actualizar daily frontend PR7/PR12 y sus reservas | PR7 integrado y PR12 distingue `dev` de rama pendiente | revisión + hashes | HECHO |
| H2.S1.M3 | Actualizar la consolidación del equipo y crear reporte de este trabajo | El denominador y el avance son explícitos | ambos validadores → exit 0 | A MEDIAS |

## Riesgos y bloqueos previstos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Un gate falla por infraestructura compartida | No se puede declarar el carril cerrado | Registrar la salida y mantener la microtarea `A MEDIAS` |
| PR12 trae commits contra una base antigua | Un cherry-pick podría borrar trabajo ajeno | Aplicar únicamente los dos fixes en una rama nacida de `origin/dev`, revisar el diff y probar |
