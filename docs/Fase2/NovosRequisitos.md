# Novos Requisitos - Fase 2

Esta documentação detalha as mudanças e os novos requisitos introduzidos na Fase 2, focando em manipulação de arquivos, formato MIDI e na complexidade musical da Fuga (polifonia).

## 1. Entrada e Manipulação de Arquivos
- **Leitura de Arquivo Texto:** O texto não precisa ser apenas digitado; o sistema deve permitir carregar um arquivo `.txt`.
- **Edição e Salvamento:** O texto carregado poderá ser modificado em tela e re-salvo (substituindo o original ou fazendo download do novo arquivo txt).

## 2. Geração de Arquivo MIDI
- **Exportação:** Além da reprodução sonora direta (no navegador), o sistema deverá gerar e permitir o salvamento/download de um arquivo MIDI `.mid`.
- **Customização:** O usuário poderá definir o nome do arquivo gerado e escolher em qual diretório ele será salvo.

## 3. Padrão General MIDI (GM)
- **Seleção Ampliada:** O sistema passará a utilizar os 128 instrumentos oficiais do padrão General MIDI. O usuário poderá configurar qualquer um deles como instrumento inicial (embora agora exista configuração automática por voz).

## 4. Fuga e Polifonia Musical
Esta é a maior mudança. O sistema deixará de ser monofônico para se tornar polifônico, inspirando-se nas composições de Johann Sebastian Bach.

- **Múltiplas Vozes por Linhas:** Cada linha do texto será tratada como uma voz independente (`V0`, `V1`, `V2`, etc.), que tocarão simultaneamente. Não se pode usar quebra de linha como espaçador numa mesma voz.
- **Atributos Base por Voz:** Cada voz iniciará com configurações próprias, criando um efeito de coral ou orquestra:
  - **Oitava:** Voz 0 = 6, Voz 1 = 5, Voz 2 = 4, Voz 3 = 3 (repete o ciclo na Voz 4 em diante).
  - **Volume:** Voz 0 = 100, Voz 1 = 80, Voz 2 = 60, Voz 3 = 40 (repete o ciclo).
  - **Instrumento (sugestão):** Voz 0 = Cravo (GM 6), Voz 1 = Órgão (GM 20), Voz 2 = Piano (GM 0), Voz 3 = Fagote (GM 70).
- **Atraso de Entrada:** No início de cada linha, a sintaxe `[n]` definirá quantos "beats" a voz deverá esperar para começar a tocar (ex: `[4] C D E` significa atraso de 4 tempos).
- **Alterações Locais à Voz:**
  - `?`: Aumenta a oitava da voz (agora local e relativo à oitava base da voz).
  - `V`: Diminui a oitava da voz.
  - `!`: Troca o instrumento da voz para Harmônica (GM 22).
- **Controle Global de Andamento (BPM):**
  - `>`: Acelera o andamento da música inteira (BPM aumenta em 10).
  - `<`: Desacelera a música inteira (BPM diminui em 10).
  *(Atenção: Esses comandos afetam a música como um todo, considerando que podem ocorrer independentemente em diferentes momentos temporais).*
