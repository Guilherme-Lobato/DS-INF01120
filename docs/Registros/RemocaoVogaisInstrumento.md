# Registro: Remoção das vogais O/I/U do mapa de instrumentos (Fase 2)

## O que mudou?

- **`backend/regras/regra_instrumentos.py`:** removidas as 6 entradas de vogais
  (`O`, `o`, `I`, `i`, `U`, `u` → GM 110, Gaita de Foles) do dicionário
  `_INSTRUMENTOS`. Restam apenas `!` (22), `;` (15) e `,` (20).
- **`frontend/App.tsx`:** removida a linha de ajuda "Vogais O, I, U: Gaita de
  Foles (GM 110)".
- **`backend/tests/test_regras.py`:** `test_regra_instrumentos` não verifica mais
  `deve_processar('I')`; adicionado `test_vogais_oiu_nao_trocam_instrumento`,
  cobrindo que as vogais não são processadas pela `RegraInstrumento` e caem na
  `RegraDefault` (repete nota anterior ou pausa).

## Por quê?

O enunciado da Fase 2 (mapeamento da fuga) determina: "Outras letras (vogais
O,I,U e consoantes não classificadas) seguem a regra original, ou seja, se o
caractere anterior era nota, repete a última nota; caso contrário, pausa." Ou
seja, na Fase 2 as vogais **não** trocam mais de instrumento (esse era o
comportamento da Fase 1). Com a remoção do mapa, esses caracteres caem
naturalmente na `RegraDefault`.

## Como reverter (caso o professor confirme o comportamento da Fase 1)

O enunciado é internamente inconsistente em outros pontos, então a mudança foi
**isolada**. Para reverter, basta readicionar as linhas das vogais ao
`_INSTRUMENTOS`:

```python
"O": 110, "o": 110, "I": 110, "i": 110, "U": 110, "u": 110,
```

e, opcionalmente, restaurar a linha de ajuda no `App.tsx` e o teste antigo.
