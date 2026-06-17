# Registro: Detalhamento dos Testes Unitários

Este documento especifica o objetivo de cada arquivo e suíte de testes desenvolvidos para o sistema de geração musical (Backend).

## 1. Testes de Modelos (`test_modelos.py`)
Valida as classes que armazenam dados de estado do sistema e do escopo musical.
- **Contexto Global:** `test_contexto_global_acelerar`, `test_contexto_global_desacelerar`, `test_contexto_global_desacelerar_limite` testam a alteração de Beats Per Minute (BPM) global, garantindo que o BPM não passe do teto mínimo e que incremente/reduza de 10 em 10.
- **Estado Musical:** `test_estado_musical_inicializacao`, `test_estado_musical_mutacoes` provam que os eventos que alteram parâmetros locais de uma voz (como mudança de Oitava entre 0-9 e limites, mudança de Volume com máximo 127 e trocas de instrumento modularizando até 127) sejam validadas em memória sem lançar exceções.
- **Voz:** `test_voz_atraso_invalido`, `test_voz_sem_fechar_colchete` protegem a inicialização segura do texto de uma voz com defasagem (delay) mal formatado.

## 2. Testes de Regras (`test_regras.py`)
As regras definem o comportamento musical ou as alterações de setup da performance em tempo real de acordo com as especificações.
- **Regra de Notas:** Confere que as letras de A a H, incluindo "Mb", sejam corretamente traduzidas em "TOCAR_NOTA" e sinaliza que a letra processada era uma nota.
- **Regra de Pausas:** Valida as letras minúsculas (a, b, c) designando apenas "PAUSA" como tipo de evento.
- **Regra de Volume:** Confere a duplicação do volume através da simulação do caractere ` ` (Espaço).
- **Regras de Instrumentos e Dígitos:** Garante a alteração correta dos bancos General MIDI (ex: `!` para o banco #22). Além da verificação algorítmica de que dígitos pares somam o valor ao instrumento atual e ímpares mudam direto para Tubular Bells (15).
- **Regra de Oitava e Bpm:** Valida o incremento/decremento com os sinais (`?`, `.`, `V` para oitavas e `>`, `<` para BPM global).
- **Regra Padrão (Default):** Garante a reprodução contínua da última nota quando recebidas consoantes genéricas ou repouso silencioso caso não houvesse nota.

## 3. Testes de Serviços (`test_services.py`)
Foca no orquestrador da lógica de conversão do texto para eventos atômicos (`PolifoniaService`).
- **Timeline de Vozes:** `test_gerar_timeline_uma_voz`, `test_gerar_timeline_duas_vozes` verificam o processamento assíncrono de múltiplas linhas de texto para tracks independentes e atestam que os "delays" (`[4]`) sejam transformados corretamente em beats iniciais absolutos dentro da timeline contínua.
- **Alterações de Metadados:** `test_gerar_timeline_bpm`, `test_gerar_timeline_mb` checam a sincronia das trocas de andamento em relação às notas da timeline, e o encadeamento léxico da regra dupla Mi Bemol (Mb -> Eb).

## 4. Testes de Exportação MIDI (`test_midi_exporter.py`)
Foca em validar a biblioteca `MidiUtil` criando buffers válidos e em canais apropriados.
- `test_calcular_nota_midi`: Verifica se a matemática Oitava -> Frequência Midi está correta, resultando em C4 como 60.
- `test_gerar_base64_vazio` e `test_gerar_base64_com_notas_e_bpm`: Testam a injeção da timeline de dicionários, garantindo que mesmo timelines com pulos entre vozes (IDs distantes) ou trilhas diferentes ignorem percussão indevida (canal 9 mapeado para banco sonoro 10) produzam um binário Base64 autêntico.

## 5. Testes de Controladores (`test_controllers.py`)
Responsável pela validação pura da resposta padronizada (JSON).
- `test_processar_dados_sucesso` e `test_processar_dados_texto_vazio` simulam o modelo de envio (DTO) e validam as propriedades calculadas (número total de eventos, BPM final, tamanho final da base64 gerada) sem necessidade de inicializar rotas ou webservers.

## 6. Testes de Roteamento API (`test_routes.py`)
Com a instância de um cliente virtual de testes do pacote FastAPI, faz injeções HTTP em tempo real.
- Dispara requisições do tipo POST em `/enviar-form` checando o protocolo HTTP (status) das respostas. Aborda tanto caminhos de `Status 200 OK` quanto `400 Bad Request` e simulação (Mocks via unittest.mock.patch) de retornos de erro do sistema computando `500 Internal Server Error`.