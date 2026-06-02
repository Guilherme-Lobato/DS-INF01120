# Lógica do Projeto - Fase 2

A lógica nesta fase aumenta significativamente a complexidade. O programa deixa de ser uma esteira simples (texto entra, som sai em fila indiana) para se tornar um simulador de linha do tempo multipistas (timeline), com gerenciamento de estado isolado por voz e um relógio global.

## Fluxo do Backend (Polifonia e Timeline)

1. **Upload e Parseamento do Arquivo:**
   - O backend recebe o texto completo (podendo vir do editor no frontend ou de um arquivo TXT enviado via requisição).

2. **Separação de Vozes (`PolifoniaService`):**
   - O sistema corta o texto pelo separador de quebra de linha. Cada linha válida vira uma classe `Voz` (Voz 0, Voz 1...).
   - Durante a inicialização de cada voz, o sistema procura pelo marcador `[n]` no começo da linha. Se achar, extrai o número `n`, que será o atraso (`atraso_beats`).

3. **Cálculo da Timeline (Linha do Tempo):**
   - Ao invés de apenas retornar um array flat, o `PolifoniaService` precisa calcular o momento (em "beats" ou tempos de compasso) de cada evento.
   - Cada voz começa seu "ponteiro de tempo" local no valor do seu atraso.
   - Se o BPM muda no meio da voz, isso afetará a velocidade das próximas batidas (se o cálculo do front for baseado em BPM em tempo real) ou recalcula o tempo absoluto das próximas notas.
   - O Backend processa o texto de cada voz aplicando as regras (via instâncias de `RegraBase`). Como as alterações (volume, oitava, instrumento) estão no `EstadoMusical` local da voz, um `?` na Voz 0 não afeta a Voz 1.

4. **Mesclagem dos Eventos:**
   - Todos os `EventoMusical` gerados ganham a propriedade `beat_absoluto`. O backend reúne tudo numa grande lista ou agrupa por trilha (Track) para enviar via JSON para o frontend.

## Fluxo de Geração MIDI
1. O backend aciona o `MidiExporter`.
2. O exportador cria um arquivo MIDI na memória.
3. Para cada voz, cria uma *Track* (trilha) diferente e atribui um Canal MIDI exclusivo.
4. Adiciona comandos de troca de instrumento (Program Change) e os eventos de *Note On* e *Note Off* nas marcações temporais calculadas.
5. Retorna o arquivo (como binário/base64) no mesmo endpoint ou em um dedicado para que o usuário baixe.

## Fluxo do Frontend (Visualização e Reprodução)
1. **Entrada e Salvamento TXT:** O usuário pode clicar num botão para importar um arquivo `.txt` do seu computador. O texto preenche o textarea. O usuário pode editar e clicar em "Salvar TXT", que fará o navegador baixar o conteúdo modificado como arquivo `.txt`.
2. **Novo Player Polifônico:**
   - A biblioteca de áudio do frontend (ex: Tone.js) precisa gerenciar múltiplas vozes.
   - Ao receber a "timeline" do backend, ele varre todos os eventos e usa a propriedade `beat_absoluto` ou `tempo` já convertido para programar as notas no relógio de transporte (`Transport` do Tone.js).
   - Assim, quando o botão "Play" for acionado, todas as vozes tocam sincronizadas, respeitando seus instrumentos e atrasos.
3. **Feedback Visual:** Agora pode ser necessário repensar o "highlight" do texto. Como várias linhas podem estar tocando ao mesmo tempo, a UI deverá aplicar a cor de destaque simultaneamente nas várias linhas em progresso.
4. **Baixar MIDI:** Um novo botão "Download MIDI" permitirá que o usuário obtenha o arquivo sonoro gerado pela classe `MidiExporter`.
