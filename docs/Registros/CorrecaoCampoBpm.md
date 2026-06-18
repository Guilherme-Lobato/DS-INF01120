# Registro: Correção do campo BPM (digitação livre) e limites

## O que mudou?

- **`frontend/App.tsx` — componente `ConfigCard`:** o `<input type="number">`
  deixou de aplicar `clamp` a cada tecla. Agora usa um **estado de rascunho**
  (`draft: string`) sincronizado com a prop `value` via `useEffect`. O `clamp`
  (mín/máx) é aplicado **somente** ao confirmar — `onBlur` e tecla **Enter**. O
  campo pode ficar temporariamente vazio durante a edição; se o valor confirmado
  for inválido (vazio/`NaN`), reverte ao último valor válido.
- **Limites do BPM:** valor padrão **120**; mínimo **10** (alinhado ao piso do
  backend em `models/contexto_global.py`, `desacelerar` usa `max(10, …)`).
- **Teto de UI:** o enunciado **não** define teto de BPM. Adotamos **300** como
  teto de interface (suposição). Caso se queira remover o teto, basta elevar/
  retirar o `max` na chamada do `ConfigCard`.

## Por quê?

O `onChange` antigo fazia
`Math.max(min, Math.min(max, parseInt(...) || min))` a cada tecla, impedindo
estados intermediários e jogando o valor para o mínimo quando o campo ficava
vazio (`parseInt('') → NaN → min`). Isso causava o sintoma de "os dígitos não
entram e o valor pula". A digitação livre com validação no `blur`/Enter resolve
o problema preservando a validação final.
