# Novos Requisitos e Funcionalidades - Fase 2

Este documento estende os requisitos da Fase 1, incorporando as novas demandas exigidas para a Fase 2 (manipulação de arquivos, formato MIDI e polifonia/fuga). 

## Requisitos da Fase 1 (Mantidos)

*   **[FUNCIONAL] Ler texto de entrada:** O sistema deve permitir que o usuário digite ou cole um texto em um campo na interface.
*   **[FUNCIONAL] Interpretar caracteres:** O sistema deve percorrer o texto caractere por caractere, aplicando as regras de mapeamento do enunciado.
*   **[FUNCIONAL] Gerar saída sonora:** O resultado deve ser audível e reproduzido diretamente pelo sistema.
*   **[FUNCIONAL] Configurar parâmetros globais:** O usuário deve poder definir BPM inicial.
*   **[FUNCIONAL] Aplicar regras exigidas:** Mapear A-G para notas, H para Si Bemol, vogais/pontuações para instrumentos específicos, espaços para dobrar volume.
*   **[FUNCIONAL] Visualizar a sequência:** A interface deve exibir a sequência gerada, destacando o evento que está tocando no momento.
*   **[FUNCIONAL] Controles do usuário:** O usuário poderá parar a reprodução, limpar o texto e re-executar.

## Novos Requisitos (Fase 2)

### 1. Entrada e Manipulação de Arquivos
*   **[FUNCIONAL] Leitura de Arquivo Texto:** O sistema deve permitir o upload/leitura de um arquivo `.txt` contendo a composição musical.
*   **[FUNCIONAL] Edição e Salvamento:** O sistema deve permitir a modificação do texto na interface e o salvamento do arquivo texto editado (substituindo o original/download).

### 2. Geração de Arquivo MIDI
*   **[FUNCIONAL] Exportação de MIDI:** O sistema deve gerar e permitir o salvamento (download) de um arquivo MIDI (`.mid`) correspondente à música gerada.
*   **[FUNCIONAL] Configuração de Salvamento MIDI:** O usuário deve poder escolher o nome do arquivo gerado e o diretório de destino (comportamento padrão do navegador ao realizar o download).

### 3. Padrão General MIDI (GM)
*   **[FUNCIONAL] Seleção de Instrumentos:** O conjunto de instrumentos do software passa a ser obrigatoriamente os 128 instrumentos do padrão General MIDI. 

### 4. Fuga e Polifonia Musical
*   **[FUNCIONAL] Múltiplas Vozes (Polifonia):** O sistema deve processar o arquivo de texto linha por linha. Cada linha será tratada como uma voz independente (V0, V1, V2, etc.) que soará simultaneamente com as demais.
*   **[FUNCIONAL] Atraso de Entrada:** O sistema deve interpretar a sintaxe `[n]` no início de uma linha como um atraso (delay) de `n` beats para o início da reprodução daquela voz.
*   **[FUNCIONAL] Oitava Base por Voz:** Cada voz deve iniciar com uma oitava pré-definida: Voz 0 = Oitava 6, Voz 1 = Oitava 5, Voz 2 = Oitava 4, Voz 3 = Oitava 3. A partir da Voz 4, o ciclo se repete.
*   **[FUNCIONAL] Volume Base por Voz:** Cada voz deve iniciar com um volume pré-definido: Voz 0 = 100, Voz 1 = 80, Voz 2 = 60, Voz 3 = 40. O ciclo se repete.
*   **[FUNCIONAL] Instrumento Base por Voz:** Cada voz deve ser atribuída a um instrumento clássico específico no início: Voz 0 = Cravo (GM 6), Voz 1 = Órgão (GM 20), Voz 2 = Piano (GM 0), Voz 3 = Fagote (GM 70).
*   **[FUNCIONAL] Controle Local de Oitava:** Os caracteres `?` (aumentar) e `V` (diminuir) devem alterar a oitava da nota com relação à oitava base, mas apenas para a voz que contém o caractere.
*   **[FUNCIONAL] Controle Global de BPM:** Os caracteres `>` (acelerar em 10) e `<` (desacelerar em 10) devem afetar o andamento geral da peça em tempo real, aplicando-se apenas no momento em que a voz inicia (após seu delay).

## Requisitos Não-Funcionais
*   **[NAO-FUNCIONAL] Padrões de Projeto (SOLID e OOP):** O backend deve ser altamente modular e estruturado utilizando os princípios de Orientação a Objetos e os padrões SOLID (SRP, OCP), facilitando extensões sem quebrar lógicas anteriores.
*   **[NAO-FUNCIONAL] Eliminação de Bad Smells:** Refatorar códigos duplicados, classes muito grandes e variáveis com nomes pouco descritivos, mantendo clareza de fluxo.
*   **[NAO-FUNCIONAL] Padrão de Nomenclatura:** Adotar `PascalCase` para nomes de arquivos de documentação, classes e construtores e `snake_case` ou `camelCase` (de acordo com a linguagem/contexto, ex: Python `snake_case`, TS `camelCase`) para métodos e variáveis.
*   **[NAO-FUNCIONAL] Documentação Contínua:** Todas as mudanças e a lógica do projeto devem estar extensivamente detalhadas na pasta `/docs`.
