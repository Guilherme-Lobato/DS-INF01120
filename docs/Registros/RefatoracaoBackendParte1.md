# Registro: Refatoração do Backend - Parte 1 (Remoção de Bad Smells)

**Data:** 01/06/2026

## O que foi feito?

Realizei a primeira parte da refatoração do código do Backend. O foco principal foi eliminar "bad smells" (códigos com más práticas) encontrados na lógica de processamento de caracteres da Fase 1, visando aumentar a robustez para a polifonia da Fase 2.

### 1. Correção do Processamento do Mi Bemol (`Mb`)
- **Problema Anterior:** Na classe `PolifoniaService`, o caractere "Mb" (Mi Bemol) estava sendo tratado com uma gambiarra utilizando `.replace("Mb", "M")` antes do laço de repetição. Isso destruía a originalidade da string e introduzia acoplamento indevido, pois a classe `RegraNotas` precisava ser adulterada para tratar a letra `M` como `Eb`, quebrando o mapeamento real.
- **Ação Realizada:** 
  - Altei o laço de repetição `for` do método `_processar_voz` na classe `PolifoniaService` para um laço `while`.
  - Implementei a técnica de **lookahead** (olhar a frente). Quando o iterador encontra a letra `M`, ele verifica se a próxima letra é `b`. Se for, processa ambas juntas como a string `"Mb"` e pula um índice no loop.
  - Atualizei a constante `_NOTAS` na classe `RegraNota` (arquivo `regra_notas.py`) para utilizar a chave `"Mb"` real, mapeando adequadamente para a nota musical `"Eb"`.
