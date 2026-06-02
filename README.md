# Desenvolvimento de Software (INF01120) - Trabalho Prático

Este repositório armazena e versiona o Trabalho Prático (Fase 1 e 2) realizado durante a disciplina de **Desenvolvimento de Software**, ministrada pelo professor **Marcelo Pimenta** na Universidade Federal do Rio Grande do Sul (UFRGS).

## 👥 Integrantes do Grupo
* **Cristiano Zandoná Parnoff** (00584548)
* **Guilherme Souza da Roza Lobato** (00584649)

## 📂 Objetivo do Projeto
O objetivo principal é a definição, implementação e testes de um **Gerador de Música a partir de Texto**. Na Fase 1 o projeto interpreta caracteres e gera sequências sonoras simples. Na Fase 2, o projeto evolui para simular uma **melodia em fuga (polifonia barroca)**, reproduzindo múltiplas vozes textuais simultaneamente e exportando arquivos MIDI reais.

O foco da disciplina e deste projeto é a aplicação prática de conceitos de engenharia de software: boas práticas (Clean Code), Orientação a Objetos, Design Patterns, modularidade e princípios SOLID.

## 🛠️ Arquitetura e Tecnologias
O projeto foi dividido em duas camadas (Cliente-Servidor) para respeitar a Responsabilidade Única (SRP):
* **Backend (API e Regras Musicais):** Python, FastAPI, MidiUtil.
* **Frontend (Interface e Reprodução de Áudio):** React, TypeScript, Vite, TailwindCSS, Tone.js.

## 📄 Documentação

A documentação detalhada (croquis, especificações de classes, e fluxo de lógica) está dividida em diretórios na pasta `/docs`:

- [Fluxo do Sistema (Backend e Frontend)](docs/FluxoDoSistema.md)
- [Requisitos Funcionais (Fase 1)](docs/Fase1/RequisitosFuncionais.md)
- [Novos Requisitos e Polifonia (Fase 2)](docs/Fase2/NovosRequisitosEFuncionalidades.md)
- [Registros de Refatoração e Modificações](docs/Registros/)

## 🚀 Como Rodar o Projeto

**1. Iniciando o Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

**2. Iniciando o Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---
*Instituto de Informática - UFRGS*
