# Paso de CI: "regenerar los clientes no produce diferencia" — H2.S1.M5

**Entregado a Leo (`PR13-Ci.Frontend`, dueño de `.github/workflows/**`).**

Contexto: los 14 clientes Angular/Dart pasaron de ignorados (`.gitignore`) a versionados
(`ADR-044`, enmienda 2026-09-22). El CI ya tiene Java resuelto en los jobs `contratos` y
`frontend` (`.github/workflows/ci.yml:185-221`, `setup-java@v4` + `generateOpenApiClients`) —
lo que falta es que, además de generar, **compare contra lo versionado y falle si difieren**.
Sin este paso, un contrato que cambia sin que alguien regenere y commitee los clientes se
detecta recién cuando algo se rompe en runtime, no en el PR.

## Comando exacto

Agregar como paso nuevo dentro del job `contratos` (después de la línea 194 de `ci.yml`, que
ya corre `generateOpenApiClients`):

```yaml
      - name: 12b · los clientes versionados coinciden con los recién generados
        run: |
          git diff --exit-code -- clientes/ || {
            echo "::error::clientes/ quedó desactualizado. Corré ./gradlew generateOpenApiClients y commiteá el resultado."
            exit 1
          }
```

`git diff --exit-code` ya sale 1 si hay cualquier diferencia (incluida una nueva/borrada), sin
necesitar `git status --short` aparte. Como el paso anterior (línea 191-197) ya generó fresco
sobre el checkout, esto compara exactamente lo que hace falta: lo recién generado contra lo que
está commiteado.

## Por qué no lo hice yo

`.github/workflows/**` es reserva de Leo en este carril (`PR13-Ci.Frontend`) — no es mi archivo
para tocar (regla 00 §3). Esto es la nota completa y el comando listo, según pide el DoD.
