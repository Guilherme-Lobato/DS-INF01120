# Registro: Modificações no Frontend (Polifonia e Manipulação de Arquivos)

## O que foi feito?

Nesta etapa, o Frontend (React/TypeScript) foi atualizado para suportar os novos requisitos da Fase 2, focando em polifonia e na entrada/saída de arquivos.

### 1. Manipulação de Arquivos (`App.tsx`)
- **Upload de TXT:** Adicionado um campo de input de arquivo oculto e um botão "Importar TXT". Ao selecionar um arquivo, a API `FileReader` lê o conteúdo e preenche o campo de texto principal automaticamente.
- **Download de TXT:** Criado o botão "Salvar TXT", que gera um `Blob` com o conteúdo atual do campo de texto e força o download sob o nome `composicao.txt`.
- **Download de MIDI:** Adicionado o botão "Baixar MIDI", habilitado apenas após a geração da música. Ele decodifica a string Base64 retornada pela API e gera um arquivo binário `.mid` (fuga_bach.mid).

### 2. Adaptação da Timeline e Polifonia (`audio.ts` e `api.ts`)
- **Novas Propriedades na API:** O modelo `ApiEvento` foi estendido para receber as propriedades `voz_id`, `beat_absoluto` e `bpm`, necessárias para o mapeamento da "Fuga".
- **Refatoração do `AudioPlayer`:** 
  - A instância única do `Tone.PolySynth` foi substituída por um dicionário de instâncias (`Record<number, Tone.PolySynth>`), permitindo que cada voz (track) tenha seu próprio timbre e volume isolado e que sejam tocados simultaneamente.
  - A lógica de agendamento sequencial (com base no index do evento) foi substituída pelo agendamento temporal absoluto (`beat_absoluto * 60 / bpm`), injetado no relógio global (`Tone.Transport.schedule`).
  - O visualizador na interface agora mostra as vozes mescladas e identifica qual voz está tocando o evento destacado.