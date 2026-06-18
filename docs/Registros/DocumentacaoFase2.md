# Registro: Documentação da Fase 2 (Croqui e convenção GM)

## O que mudou?

- **`docs/Fase2/CroquiInterface.md` (novo):** croqui e justificativa de layout
  da interface da Fase 2, exigidos pela 3ª parte do enunciado. Descreve a tela
  tal como implementada em `frontend/App.tsx` (botões Importar TXT, Salvar,
  Salvar como, Baixar MIDI; campo BPM; painel de vozes mescladas; cartão de
  evento atual), com justificativa de cada elemento. Antes existia apenas
  `docs/Fase1/CroquiInterface.md`.
- **`docs/Fase2/ConvencaoInstrumentosGM.md` (novo):** nota explicitando que o
  grupo adota programas GM **indexados de 0 a 127** e listando o instrumento
  base por voz conforme implementado em `backend/models/voz.py` (Voz 0 Cravo
  GM6, Voz 1 Órgão GM20, Voz 2 Piano GM0, Voz 3 Fagote GM70).

## Por quê?

- O croqui da Fase 2 não existia, apesar de exigido pelo enunciado.
- O enunciado se contradiz sobre o instrumento base por voz e sobre o Fagote
  (GM 70 vs 71; indexação 0 vs 1). A nota resolve a ambiguidade documentando a
  convenção efetivamente usada. Mudança **somente documental** — sem alteração
  de código.
