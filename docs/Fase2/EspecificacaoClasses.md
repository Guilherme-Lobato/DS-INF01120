# Especificação de Classes - Fase 2

Para dar suporte aos novos requisitos de polifonia (Fuga) e geração de arquivos, precisamos evoluir as classes da Fase 1, adotando princípios de modularidade (SOLID) para não quebrar o que já funcionava.

## Classe Voz (NOVA)
Encapsula os atributos e o estado temporal de uma única linha de texto do usuário.
- **Atributos:**
  - `id_voz (inteiro)`: Identificador único da voz (0, 1, 2...).
  - `texto_original (texto)`: A linha de texto que esta voz deve interpretar.
  - `atraso_beats (inteiro)`: O delay inicial da voz (extraído da sintaxe `[n]`).
  - `estado (EstadoMusical)`: Instância única do EstadoMusical pertencente exclusivamente a esta voz, com os valores base (oitava, instrumento, volume) inicializados conforme a regra do ID (Voz 0 = Oitava 6, Voz 1 = Oitava 5...).
- **Métodos:**
  - `inicializar_atributos_base()`: Define os valores iniciais da voz com base no `id_voz`.
  - `extrair_atraso()`: Lê a string e retira a formatação `[n]`, armazenando o atraso em `atraso_beats`.

## Classe EstadoMusical (Atualizada)
- Deixa de ser um estado global do sistema e passa a ser o **estado local de uma Voz**.
- **Novos Comandos Locais:** Passa a ter métodos para lidar com o comando `V` (diminuir oitava), e para garantir que alterações como `?` afetem apenas a sua instância atual, além do `!` (Harmônica - GM 22).

## Classe EventoMusical (Atualizada)
- Precisa de novos atributos para saber seu posicionamento exato na "linha do tempo" (timeline), pois as notas de diferentes vozes tocarão juntas.
- **Novos Atributos:**
  - `voz_id (inteiro)`: Identifica qual voz gerou este evento.
  - `beat_absoluto (flutuante)`: O momento exato, em "beats" (batidas), em que este evento vai ocorrer.

## Classe ContextoGlobal (NOVA)
- Responsável por armazenar e alterar estados que afetam todas as vozes, como o **BPM**.
- **Atributos:**
  - `bpm_atual (inteiro)`: Começa em 120 e pode ser modificado no meio do processamento por `>` ou `<`.
- **Métodos:**
  - `acelerar()`: Incrementa o BPM em 10.
  - `desacelerar()`: Decrementa o BPM em 10.

## Classe PolifoniaService (NOVA/Atualização da MusicService)
- Evolução do `MusicService`. Agora atua como o Maestro.
- **Atributos:** `lista_vozes (Lista de Voz)`
- **Métodos:**
  - `separar_linhas(texto_completo)`: Quebra o texto e gera instâncias da classe `Voz`.
  - `gerar_timeline()`: Itera paralelamente ou sequencialmente as vozes, calculando o `beat_absoluto` de cada `EventoMusical` baseado no `atraso_beats` e gerando uma lista cronológica contendo todos os eventos de todas as vozes para ser enviada ao frontend ou exportador.

## Classe MidiExporter (NOVA)
- Responsável por traduzir a lista cronológica de `EventoMusical` em trilhas e mensagens MIDI.
- **Métodos:**
  - `gerar_arquivo_midi(timeline, nome_arquivo)`: Utiliza uma biblioteca (ex: `midiutil` do Python) para instanciar um arquivo com múltiplas faixas (tracks) — uma para cada voz —, configurando os instrumentos corretos em canais separados (canais MIDI 0-15) e gravando as notas com seus respectivos tempos calculados.
