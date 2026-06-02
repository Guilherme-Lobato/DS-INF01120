# Definições de Classes - Fase 1

As classes abaixo foram projetadas para atender aos requisitos da Fase 1, utilizando princípios da Orientação a Objetos.

### Classe EstadoMusical
Representa o estado mutável durante a interpretação do texto.
- **Atributo instrumento (inteiro):** Número MIDI do instrumento atual.
- **Atributo oitava (inteiro):** Oitava atual (1 a 9).
- **Atributo volume (inteiro):** Volume atual (0 a 127).
- **Atributo ultima_nota (texto):** Última nota tocada.
- **Atributo anterior_era_nota (booleano):** Indica se o caractere anterior gerou uma nota.
- **Método dobrar_volume():** Dobra o volume ou seta o valor máximo.
- **Método subir_oitava():** Incrementa a oitava atual.
- **Método trocar_instrumento(novo):** Define um novo instrumento.
- **Método somar_instrumento(valor):** Soma um valor numérico ao instrumento atual.
- **Método registrar_nota(nota):** Atualiza o histórico para saber qual foi a última nota.

### Classe EventoMusical
Representa um único evento na sequência musical.
- **Atributo tipo:** O tipo da ação (tocar, pausar, mudar volume, etc.).
- **Atributo char (texto):** Caractere original do texto.
- **Atributo nota (texto):** Nome da nota gerada.
- **Atributo oitava (inteiro):** Oitava exata do evento.
- **Atributo volume (inteiro):** Volume exato do evento.
- **Atributo instrumento (inteiro):** Instrumento exato do evento.

### Classe RegraBase
Abstração para as regras de mapeamento de texto para som.
- **Método deve_processar(char, estado):** Retorna verdadeiro ou falso verificando se a regra se aplica àquele caractere.
- **Método processar(char, estado):** Aplica a regra musical e retorna o evento gerado.

### Classe PolifoniaService (antigo MusicService)
Orquestra a geração musical aplicando as regras ao texto.
- **Atributo regras (lista):** Lista contendo as instâncias das regras de mapeamento.
- **Método gerar_sequencia(texto, instr, oitava, vol):** Itera o texto completo e retorna a lista final de eventos.
