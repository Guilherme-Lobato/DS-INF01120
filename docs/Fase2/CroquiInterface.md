# Croquis e Justificativa de Layout — Fase 2

Croqui da interface tal como implementada em `frontend/App.tsx` para a Fase 2
(polifonia + manipulação de arquivos). A tela mantém a filosofia da Fase 1
(entrada de texto em primeiro plano) e acrescenta os elementos exigidos pela
nova fase.

## Croqui (tela única)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ● Texto para Música            UFRGS — INF01120 — Fase 2   [⚡ Backend online]│
├──────────────────────────────────────────────────────────────────────────┤
│ ┌─ Coluna esquerda (8/12) ─────────────────┐ ┌─ Coluna direita (4/12) ───┐ │
│ │ [⤒ Importar TXT] [⤓ Salvar] [⤓ Salvar como]      [♫ Baixar MIDI] │ │ Sequência Musical          │ │
│ │                                          │ │ (Vozes Mescladas)          │ │
│ │ ┌── Entrada de Texto ─────────────────┐  │ │ ┌────────────────────────┐ │ │
│ │ │ linha 1 → Voz 0                     │  │ │ │ [C v0][D v0][G v1] ... │ │ │
│ │ │ linha 2 → Voz 1                  🗑  │  │ │ │ (bloco atual destacado)│ │ │
│ │ └─────────────────────────────────────┘  │ │ └────────────────────────┘ │ │
│ │                                          │ │                            │ │
│ │ ┌─ BPM ───┐                              │ │ ┌─ Evento atual ─────────┐ │ │
│ │ │  120    │                              │ │ │ Voz 0            C4    │ │ │
│ │ └─────────┘                              │ │ └────────────────────────┘ │ │
│ │                                          │ │                            │ │
│ │ [ ▶  GERAR E TOCAR  /  ■ PARAR ]         │ │                            │ │
│ │  status / erro                           │ │                            │ │
│ │                                          │ │                            │ │
│ │ ▸ Regras de Mapeamento (expansível)      │ │                            │ │
│ └──────────────────────────────────────────┘ └────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

## Justificativa de cada elemento

- **Cabeçalho:** identifica o sistema e a fase, e exibe o indicador de status do
  backend (online/offline). Dá feedback imediato sobre conectividade antes que o
  usuário tente gerar a música.
- **Barra de ações de arquivo (topo da coluna esquerda):**
  - **Importar TXT** — carrega um arquivo de texto para o campo de entrada.
    Quando o navegador suporta a File System Access API, guarda o *handle* do
    arquivo para permitir sobrescrita posterior.
  - **Salvar** — sobrescreve o arquivo original importado (atende ao requisito
    da Fase 2 de "salvar substituindo o original"). Fica desabilitado enquanto
    não houver um arquivo importado com handle de escrita.
  - **Salvar como** — grava em um novo arquivo (ou baixa `.txt` como fallback
    em navegadores sem suporte à API).
  - **Baixar MIDI** — alinhado à direita e destacado em laranja por ser a saída
    principal da fase; habilita-se apenas após a geração.
- **Área de Entrada de Texto:** campo amplo e central, pois é a ação primária.
  Na Fase 2 cada linha representa uma voz independente (Voz 0, 1, 2…), suportando
  a polifonia da fuga. Botão de limpar (🗑) no canto.
- **Campo BPM:** controle numérico do andamento global (padrão 120). Permite
  digitação livre, com validação aplicada apenas ao confirmar (blur/Enter).
- **Botão Gerar e Tocar / Parar:** botão de ação destacado que alterna estado
  visual durante a reprodução, dando feedback imediato.
- **Regras de Mapeamento (seção expansível):** referência rápida das regras de
  conversão (notas, pausas, controles, instrumentos) sem poluir a tela.
- **Painel de Sequência Musical (coluna direita):** mostra os caracteres já
  convertidos como blocos, agora **com as vozes mescladas** e identificando a
  voz de cada evento (`v0`, `v1`…). O bloco em reprodução é destacado em tempo
  real, permitindo acompanhar visualmente a polifonia.
- **Cartão de Evento Atual:** durante a reprodução, exibe de forma ampliada a
  voz e a nota/oitava do evento corrente, reforçando o feedback do que está
  tocando.
