# Registro: Implementação do Suporte a Arquivos MIDI e Eventos Globais de BPM

## O que foi feito?

Nesta etapa, adicionamos as novas funcionalidades exigidas pela Fase 2 relacionadas à polifonia e à exportação do resultado sonoro para um arquivo `.mid`.

### 1. Injeção de Eventos de BPM na Timeline
- **Detalhes da Correção:** O andamento musical global (BPM) não estava sendo adequadamente propagado para a lista de eventos absolutos da timeline. O caractere `>` e `<` geravam eventos isolados. 
- **Ação Realizada:**
  - Modificamos o método `gerar_timeline` do `PolifoniaService` para realizar uma segunda iteração cronológica na lista de eventos já ordenada.
  - Utilizamos a classe `ContextoGlobal` para rastrear as mudanças temporais e injetar a propriedade `bpm` exata em todos os eventos do tipo `CHANGE_BPM`, comunicando a alteração para a engine de áudio no momento correto.

### 2. Criação do Exportador MIDI (`MidiExporter`)
- **Detalhes da Correção:** O sistema precisava permitir que a "Fuga" pudesse ser baixada e executada localmente num player padrão do sistema operacional, requerendo o padrão General MIDI.
- **Ação Realizada:**
  - Instalamos a biblioteca `midiutil` no ambiente backend (`requirements.txt`).
  - Criamos a classe `MidiExporter`, que constrói um arquivo com `N` pistas de áudio (Tracks), onde cada `Voz` possui seu próprio instrumento num canal (Channel) exclusivo (ignorando o canal 9 para evitar percussão).
  - O método `gerar_base64` pega todos os eventos absolutos (pitch da nota, BPM real, momento exato, instrumento e volume da voz específica) e compõe a estrutura MIDI, retornando uma string encodada em Base64 para ser incorporada diretamente à resposta JSON da API.
  - Atualizamos a classe `InterfaceController` para orquestrar a chamada do serviço e adicionar o `midi_base64` ao retorno final.