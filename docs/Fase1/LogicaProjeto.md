# Lógica do Projeto - Fase 1

A arquitetura do projeto está dividida em duas partes principais: **Backend (Python)** e **Frontend (React/TypeScript)**. O fluxo de dados ocorre de forma clara, desde o recebimento do texto até a sua reprodução audível.

## Fluxo do Backend
O Backend atua como o processador central do texto. Ele não toca o som em si, mas traduz o texto em uma lista estruturada de eventos musicais (como notas e pausas) utilizando o conceito de "MusicService" e regras específicas ("RegraBase").

1. **Endpoint de Geração (`POST /api/music/generate`)**:
   - **Recebe:** Um JSON contendo o `texto` digitado pelo usuário e as configurações iniciais (`bpm`, `instrumento`, `oitava`, `volume`).
   - **Processamento:** O controlador repassa esses dados para a classe `MusicService`. O `MusicService` inicializa a classe `EstadoMusical` com as configurações.
   - **Iteração:** Para cada caractere no texto, o serviço consulta sua lista de regras (classes que implementam `RegraBase`, como `RegraNotas`, `RegraVolume`, etc.).
   - **Aplicação da Regra:** Quando uma regra se aplica ao caractere, ela atualiza o `EstadoMusical` (ex: aumenta o volume) e gera um objeto `EventoMusical` (ex: tocar a nota 'C' com volume X).
   - **Retorno:** Retorna ao frontend um array de objetos `EventoMusical`, garantindo que o cliente saiba exatamente o que tocar, quando tocar e com qual configuração.

## Fluxo do Frontend
O Frontend é responsável pela interação do usuário e por processar o array de eventos recebido do Backend para gerar os sons correspondentes, além de apresentar visualmente o progresso da música.

1. **Ação do Usuário**:
   - O usuário preenche o texto, ajusta as variáveis de BPM, Instrumento, Oitava e Volume na interface.
   - Ao clicar em "Gerar e Tocar", esses dados são enviados para o Backend via requisição POST.
   
2. **Reprodução (Audio Engine)**:
   - O array de eventos retornado é lido sequencialmente pelo Frontend.
   - Utilizando uma biblioteca de reprodução em ambiente Web (como Tone.js ou Soundfont-player), o frontend calcula os tempos baseados no BPM.
   - Para cada `EventoMusical` na lista:
     - Se for do tipo `"tocar"`, dispara o som correspondente à nota, no instrumento indicado, com a oitava e volume corretos.
     - Se for `"pausar"`, simplesmente avança o tempo equivalente a uma pausa.
     
3. **Feedback Visual**:
   - A interface renderiza cada evento gerado (ou cada caractere) na tela.
   - Conforme o som é reproduzido, a interface destaca visualmente qual bloco/caractere está sendo tocado naquele exato milissegundo, permitindo que o usuário acompanhe o ritmo e a música na tela.

## Conclusão do Ciclo
Com esta arquitetura, respeitamos os princípios de separação de conceitos: o backend traduz regras lógicas (garantindo modularidade), enquanto o frontend cuida estritamente da interface com o usuário e da execução de áudio.
