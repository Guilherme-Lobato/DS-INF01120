# Especificação de Classes - Fase 1

Esta seção descreve as classes que compõem o sistema na Fase 1. O objetivo é manter o código modular e aderir aos princípios SOLID, como a Responsabilidade Única (SRP).

## Classe EstadoMusical
Representa o estado mutável do sistema durante a interpretação do texto. À medida que o texto é lido, o estado guarda as propriedades atuais da música (instrumento, oitava, volume, etc.).
- **Atributos:**
  - `instrumento (inteiro)`: Número MIDI do instrumento atual.
  - `oitava (inteiro)`: Oitava atual (1 a 9).
  - `volume (inteiro)`: Volume atual (0 a 127).
  - `ultima_nota (texto)`: Guarda a última nota tocada.
  - `anterior_era_nota (booleano)`: Indica se o caractere processado imediatamente antes resultou em uma nota.
- **Métodos:**
  - `dobrar_volume()`: Multiplica o volume atual por dois. Se exceder 127, define para 127 (máximo). Retorna ao volume base se não puder dobrar.
  - `subir_oitava()`: Incrementa a oitava atual em 1.
  - `trocar_instrumento(novo_instrumento)`: Substitui o instrumento atual por um novo valor MIDI.
  - `somar_instrumento(valor)`: Soma um valor numérico ao instrumento atual.
  - `registrar_nota(nota)`: Atualiza a `ultima_nota` com a nota tocada e define `anterior_era_nota` como verdadeiro.

## Classe EventoMusical
Representa um único evento musical ou de controle a ser enviado para o frontend.
- **Atributos:**
  - `tipo (texto)`: Define a ação, como `"tocar"`, `"pausar"`, ou alteração de contexto.
  - `char (texto)`: O caractere do texto original que gerou este evento.
  - `nota (texto)`: A nota musical (ex: "C", "D", "E").
  - `oitava (inteiro)`: A oitava em que a nota deve ser tocada.
  - `volume (inteiro)`: O volume da nota.
  - `instrumento (inteiro)`: O instrumento designado para esta nota.

## Classe RegraBase
É uma classe abstrata (ou interface) que dita o formato para todas as regras de mapeamento (A-G para notas, espaços para volume, etc.). Isso aplica o Princípio Aberto-Fechado (OCP), permitindo adicionar novas regras sem alterar as antigas.
- **Métodos:**
  - `deve_processar(char, estado)`: Retorna um valor booleano indicando se a regra deve ser aplicada para aquele caractere específico.
  - `processar(char, estado)`: Modifica o `EstadoMusical` e gera um `EventoMusical` correspondente à ação.

## Classe MusicService
Orquestra o fluxo de geração musical. É responsável por receber o texto, iterar sobre ele e invocar as regras.
- **Atributos:**
  - `regras (lista)`: Contém as instâncias de todas as classes filhas de `RegraBase`.
- **Métodos:**
  - `gerar_sequencia(texto, instrumento_inicial, oitava_inicial, volume_inicial)`: Inicializa o `EstadoMusical` com os parâmetros fornecidos e varre a string `texto`. Para cada caractere, procura uma `RegraBase` aplicável na lista de `regras` e guarda o `EventoMusical` resultante em uma lista de saída. Retorna esta lista de eventos.
