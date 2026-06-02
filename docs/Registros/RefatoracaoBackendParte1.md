# Registro: Refatoração do Backend - Parte 1 (Remoção de Bad Smells)

**Data:** 01/06/2026
**Responsável:** AI Agent

## O que foi feito?

Conforme solicitado e planejado, realizei a primeira parte da refatoração do código do Backend. O foco principal foi eliminar "bad smells" (códigos com más práticas) encontrados na lógica de processamento de caracteres da Fase 1, visando aumentar a robustez para a polifonia da Fase 2.

### 1. Correção do Processamento do Mi Bemol (`Mb`)
- **Problema Anterior:** Na classe `PolifoniaService`, o caractere "Mb" (Mi Bemol) estava sendo tratado com uma gambiarra utilizando `.replace("Mb", "M")` antes do laço de repetição. Isso destruía a originalidade da string e introduzia acoplamento indevido, pois a classe `RegraNotas` precisava ser adulterada para tratar a letra `M` como `Eb`, quebrando o mapeamento real.
- **Ação Realizada:** 
  - Altei o laço de repetição `for` do método `_processar_voz` na classe `PolifoniaService` para um laço `while`.
  - Implementei a técnica de **lookahead** (olhar a frente). Quando o iterador encontra a letra `M`, ele verifica se a próxima letra é `b`. Se for, processa ambas juntas como a string `"Mb"` e pula um índice no loop.
  - Atualizei a constante `_NOTAS` na classe `RegraNota` (arquivo `regra_notas.py`) para utilizar a chave `"Mb"` real, mapeando adequadamente para a nota musical `"Eb"`.

### 2. Por que isso é importante?
Ao aplicar o *lookahead*, respeitamos os princípios do **Clean Code** e a originalidade da string recebida do usuário. O serviço volta a ser estritamente um orquestrador e a responsabilidade de saber o que `"Mb"` significa recai puramente sobre a `RegraNota`, respeitando o **Princípio da Responsabilidade Única (SRP)** do SOLID.

## Próximos Passos
- Refatorar a emissão de eventos de BPM (`>` e `<`) para que sejam injetados corretamente na timeline global e consigam comunicar o frontend e o exportador de MIDI.
- Desenvolver a classe `MidiExporter` para geração de arquivo `.mid`.