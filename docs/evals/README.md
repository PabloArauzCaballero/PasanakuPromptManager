# Evals del catálogo

Infraestructura para probar que un cambio en una skill **no rompió el ruteo ni el
comportamiento** del catálogo. Se corre antes de publicar un cambio (`prompt-evals`).

- `catalogo.json` / `catalogo.md` — inventario de skills con su descripción, para detectar
  solapamientos y descripciones que no disparan.
- `score.py` — calcula el resultado de una corrida de evaluación.
- `escenarios/` — los casos. **Los escenarios heredados de otro producto no se portaron**: hay
  que escribir los de Pasanaku, empezando por los que más duelen si el ruteo falla:
  un cambio que toca un importe debe cargar `money-movement-safety`; uno que cruza servicios,
  la regla 98; uno que expone datos de una persona, `data-privacy-financial`.

Mientras no existan escenarios propios, esta carpeta es andamiaje: **no afirmes que el catálogo
está evaluado** (regla 30).
