# Registro: Salvar TXT substituindo o arquivo original

## O que mudou? (`frontend/App.tsx`)

- **Importar TXT:** quando o navegador suporta a **File System Access API**
  (`window.showOpenFilePicker`), a importação passa a guardar o *handle* do
  arquivo (`fileHandleRef`), habilitando a sobrescrita posterior. Sem suporte,
  mantém-se o `<input type="file">` + `FileReader` como fallback.
- **Salvar (novo botão):** sobrescreve o arquivo original importado via
  `handle.createWritable()`. Fica desabilitado enquanto não houver um arquivo
  importado com handle de escrita.
- **Salvar como (novo botão):** grava em um novo arquivo via
  `window.showSaveFilePicker`; em navegadores sem suporte, cai no **download**
  tradicional (`composicao.txt`), preservando o comportamento anterior.

## Por quê?

O enunciado pede que, ao editar o TXT, seja possível **salvá-lo substituindo o
arquivo original**. Antes, o botão "Salvar TXT" apenas baixava um novo arquivo,
sem sobrescrever o original. A File System Access API permite a sobrescrita real
quando disponível, e o download permanece como fallback para compatibilidade.
