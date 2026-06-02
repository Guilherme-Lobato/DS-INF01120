# UFRGS - Desenvolvimento de Software (INF01120)
Trabalho Prático — Fase 1

**Alunos:** Guilherme Souza da Roza Lobato (00584649) e Cristiano Zandoná Parnoff (00584548)

## LISTA DE REQUISITOS FUNCIONAIS

- **Ler texto de entrada:** O sistema deve permitir que o usuário digite ou cole um texto em um campo na interface.
- **Interpretar caracteres:** O sistema deve percorrer o texto caractere por caractere, aplicando as regras de mapeamento do enunciado.
- **Gerar saída sonora:** O resultado deve ser audível e reproduzido diretamente pelo sistema (via API/biblioteca de áudio no frontend).
- **Configurar parâmetros:** O usuário deve poder definir BPM (Batidas Por Minuto), instrumento inicial, oitava padrão e volume inicial antes da geração.
- **Aplicar regras exigidas:**
  - Mapear A-G para notas, H para Si Bemol.
  - Letras a-h minúsculas são pausas (silêncio).
  - Vogais 'O', 'I', 'U' para o instrumento Gaita de Foles (GM #110).
  - Consoantes restantes: repetir nota se anterior foi nota, senão pausa.
  - Caractere '!' para o instrumento Bandoneon (GM #24).
  - Espaço para dobrar volume (ou máximo de 127).
  - Dígito par: soma valor do dígito ao instrumento atual.
  - Dígito ímpar ou ';': instrumento Tubular Bells (GM #15).
  - Caractere ',' para Church Organ (GM #114).
  - Caracteres '?' ou '.' para aumentar uma oitava.
  - Nova linha ('\n') para Ondas do Mar (GM #123).
- **Visualizar a sequência:** A interface deve exibir a sequência gerada, destacando o evento que está tocando no momento.
- **Controles do usuário:** O usuário poderá parar a reprodução, limpar o texto e re-executar sem precisar atualizar a página.

## REQUISITOS NÃO-FUNCIONAIS (Ênfase na Qualidade do Código)

- **Modularidade:** O sistema deve ser dividido em módulos com responsabilidades bem definidas (módulo de leitura, módulo de interpretação, de geração e de saída).
- **Baixo Acoplamento e Alta Coesão:** As classes devem ter poucas dependências e representar conceitos únicos.
- **Princípios SOLID:**
  - S (Responsabilidade Única): Classes com apenas um motivo para mudar.
  - O (Aberto/Fechado): Extensível para novas regras sem mudar o existente.
  - L (Substituição de Liskov): Subclasses devem substituir classes base.
  - I (Segregação de Interfaces): Interfaces específicas em vez de genéricas.
  - D (Inversão de Dependência): Depender de abstrações e não de implementações.
- **Legibilidade:** Nomes significativos, formatação consistente, sem duplicação de código.
- **Testabilidade e Versionamento:** Utilizar Git para versionamento adequado do projeto.