# UFRGS - Desenvolvimento de Software (INF01120)
**Alunos:** Guilherme Souza da Roza Lobato e Cristiano Zandoná Parnoff

# Arquitetura e Fluxo do Sistema (Fases 1 e 2)

Este documento detalha exaustivamente a arquitetura, a lógica e o fluxo de dados do nosso gerador de música, contemplando desde a inserção do texto até a exportação do arquivo MIDI e reprodução sonora, passando pelas modificações arquiteturais da Fase 2 (Polifonia/Fuga).

## 1. Visão Geral da Arquitetura

Optamos por uma arquitetura cliente-servidor para isolar a complexidade de regras de negócio:
- **Backend (Python com FastAPI):** Responsável por interpretar o texto, extrair as intenções musicais utilizando regras de negócio (Padrão Strategy), orquestrar as vozes da Fuga e exportar o modelo para MIDI.
- **Frontend (React com TypeScript e Vite):** Responsável pela interface com o usuário, submissão de dados, reprodução sonora em tempo real (utilizando `Tone.js`) e download de arquivos locais.

## 2. Fluxo Passo a Passo: Da Entrada à Resposta

Quando o usuário insere um texto na área de texto (seja digitando ou carregando via `.txt`) e clica em **Gerar e Tocar**, o fluxo segue os seguintes passos:

### 2.1. Frontend: Preparação e Requisição
1. **Coleta de Dados:** O componente `App.tsx` junta o texto digitado e as configurações globais numéricas (BPM, Instrumento Inicial, Oitava e Volume).
2. **Chamada de API:** A função `gerarSequencia` no arquivo `services/api.ts` cria uma requisição HTTP POST para o endpoint `/enviar-form` do Backend, empacotando os dados num objeto JSON (conforme contrato da interface `ApiConfig`).

### 2.2. Backend: Recebimento e Validação
1. **Rota e DTO:** O endpoint `/enviar-form` (no arquivo `routes/interface_route.py`) intercepta a requisição. Ele utiliza a classe `InterfaceDTO` (em `dtos/interface_dto.py`) para validar automaticamente se os tipos de dados enviados estão corretos.
2. **Controlador:** Os dados passam para o `InterfaceController.processar_dados()`. Este método valida regras superficiais (como impedir texto vazio) e despacha a requisição para a camada de serviços.

### 2.3. Backend: Separação de Vozes e Timeline (O Maestro)
O texto então entra no `PolifoniaService`, que atua como nosso maestro virtual (em `services/polifonia_service.py`).
1. **Separação por Linhas (Fase 2):** O serviço corta o texto onde há quebras de linha (`\n`). Cada linha se torna uma instância da classe `Voz` (em `models/voz.py`).
2. **Atributos por Voz:** Ao instanciar a `Voz`, o construtor confere o ID da linha (0, 1, 2...) e atribui a ela sua própria Oitava, Volume e Instrumento "base" únicos. Isso gera a distinção de naipes da orquestra barroca. Além disso, lê e remove atrasos de entrada, como `[4]`.
3. **Iteração de Caracteres:** Para cada `Voz`, o serviço itera caractere por caractere (com suporte a *lookahead* para encontrar notas conjuntas como `Mb` (Mi Bemol)).
4. **Aplicação das Regras (Padrão de Projeto):** Cada caractere é testado contra uma lista de classes que herdam de `RegraBase` (ex: `RegraNotas`, `RegraBpm`, `RegraVolume`, localizadas na pasta `regras`).
    - *Exemplo:* Se for `C`, a `RegraNotas` atende, altera o `EstadoMusical` interno daquela `Voz` específica e devolve um `EventoMusical` contendo a nota 'C'.
5. **Composição da Timeline Global:** Todos os `EventosMusicais` de todas as vozes são inseridos em uma lista única e recebem um marcador absoluto temporal (`beat_absoluto`). O maestro os organiza cronologicamente.
6. **Resolução de BPM Global:** Como o BPM (afetado por `<` e `>`) altera o andamento de toda a música, uma classe chamada `ContextoGlobal` repassa a timeline para propagar a variável de BPM em tempo real a todos os eventos relevantes.

### 2.4. Backend: Exportação para MIDI
Após a timeline estar pronta e ordenada, o `InterfaceController` invoca o `MidiExporter` (em `services/midi_exporter.py`).
1. A biblioteca `midiutil` é instanciada criando um arquivo de múltiplas trilhas (tracks).
2. O sistema itera nossa timeline, convertendo strings textuais ("C", oitava 4) no identificador pitch numérico do padrão GM (ex: Dó 4 = 60).
3. Configura a atribuição de vozes aos canais, evitando o canal 9 que é de percussão.
4. Gera um arquivo binário em memória e o converte para `Base64`.

### 2.5. Resposta HTTP
O `InterfaceController` empacota a lista de `EventoMusical` (sequência) e a string Base64 do MIDI e os devolve como uma resposta JSON de Sucesso 200 ao Frontend.

### 2.6. Frontend: Interpretação Visual e Sonora
O React intercepta o retorno na função do `App.tsx`:
1. **Disponibilização do MIDI:** O `Base64` do arquivo MIDI gerado é salvo no estado do componente, ativando o botão "Baixar MIDI" do usuário. Quando acionado, ele converte a string de volta em um arquivo de bytes descarregável (fuga_bach.mid).
2. **Reprodução Sonora (`AudioPlayer`):**
    - Enviamos a lista de eventos para a classe `AudioPlayer` (em `services/audio.ts`).
    - O player aloca um sintetizador (`Tone.PolySynth`) específico e diferente para cada `voz_id` existente.
    - Utilizando o agendador global (`Tone.Transport.schedule`), percorremos a timeline. A fórmula matemática simples baseada em `beat_absoluto` e `bpm` calcula exatamente em qual milissegundo as notas de diferentes vozes devem tocar.
    - O relógio começa a rodar, e sempre que a nota toca, a função `onIndex` emite uma requisição ao estado do React para alterar a cor visual do caractere exato, produzindo o efeito visual simultâneo.

## 3. Considerações Finais sobre a Lógica

O projeto segue os princípios **SOLID**, principalmente pelo baixo acoplamento. Cada regra musical é independente das demais. Se uma nova regra for solicitada na próxima fase, bastará criar um arquivo `regra_nova.py` e herdá-la de `RegraBase`, sem quebrar a timeline temporal, as vozes, nem a exportação MIDI.
