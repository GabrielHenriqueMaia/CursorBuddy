# PROJETO
Codinome: Project Sentinel (nome temporário)

# CONTEXTO

Quero desenvolver um assistente de IA para Windows inspirado em projetos como HeyClicky, OpenClicky, DesktopCtl e Computer Use, porém NÃO quero criar apenas um clone.

O objetivo é construir uma plataforma open source, modular e extensível para assistentes desktop contextuais.

O projeto deverá ser pensado para evoluir durante meses, porém inicialmente será desenvolvido em pequenas entregas incrementais.

A IA deve atuar como arquiteta de software, pesquisadora, revisora e desenvolvedora durante todo o projeto.

Ela deve sempre priorizar:

- código limpo
- arquitetura desacoplada
- baixo acoplamento
- alta coesão
- extensibilidade
- plugins
- interfaces bem definidas
- documentação automática
- testes quando fizer sentido

Nunca produzir código "rápido" apenas para funcionar.

Sempre pensar na evolução futura.

------------------------------------------------------------

# VISÃO DO PRODUTO

O sistema será um assistente residente no Windows capaz de compreender o contexto do usuário.

Ele deverá conseguir:

• entender qual aplicação está aberta
• entender a janela ativa
• entender o que existe na tela
• compreender texto através de OCR
• compreender interfaces através de UI Automation
• compreender imagens através de Vision Models
• conversar por texto
• conversar por voz
• desenhar overlays sobre qualquer aplicação
• destacar elementos na tela
• apontar onde clicar
• aprender fluxos do usuário
• armazenar memória
• executar ferramentas
• automatizar tarefas
• evoluir para um agente Computer Use

O foco NÃO é ser um chatbot.

O foco é ser uma camada inteligente sobre o Windows.

------------------------------------------------------------

# PRINCÍPIOS

Sempre separar:

Percepção

↓

Contexto

↓

Planejamento

↓

Execução

↓

Reflexão

↓

Memória

Nunca misturar essas responsabilidades.

Toda comunicação entre módulos deve ocorrer através de interfaces.

Nada deve depender diretamente de uma implementação específica de LLM.

Todo provider deve poder ser substituído.

OpenAI

Claude

Gemini

OpenRouter

Ollama

LM Studio

etc.

------------------------------------------------------------

# DIFERENCIAIS

O sistema deverá possuir conceitos que normalmente não existem juntos.

## Contexto híbrido

Não depender apenas de screenshots.

Misturar:

- Screenshot
- OCR
- UI Automation
- Janela ativa
- Processo ativo
- Mouse
- Clipboard
- Keyboard
- Monitor
- Histórico recente

Tudo isso deve gerar um único objeto chamado Context.

------------------------------------------------------------

## Memória

O sistema deverá lembrar

- conversas
- aplicativos
- projetos
- documentos
- tarefas
- padrões
- workflows

------------------------------------------------------------

## Plugins

Cada software poderá possuir um plugin.

Exemplo

plugins/

    vscode/
    chrome/
    excel/
    genexus/
    sqlserver/

Cada plugin poderá fornecer

context()

knowledge()

actions()

prompt()

tools()

------------------------------------------------------------

## Overlay

O sistema deverá desenhar

setas

círculos

caixas

balões

tooltips

cursores

efeitos

sobre qualquer aplicação.

------------------------------------------------------------

## Ferramentas

Mouse

Keyboard

Clipboard

Browser

Filesystem

Terminal

HTTP

MCP

IA

------------------------------------------------------------

# STACK PREFERENCIAL

Windows

C#

.NET 9

WinUI 3

Windows App SDK

Windows Graphics Capture

Windows UI Automation

Windows OCR

SQLite

Semantic Kernel (opcional)

Ollama

OpenAI SDK

OpenCV (caso necessário)

Não utilizar Electron.

Não utilizar Tauri inicialmente.

O projeto deve ser nativo Windows.

------------------------------------------------------------

# ARQUITETURA

Sentinel

│

├── Core

│       Contracts

│       Events

│       Dependency Injection

│       Logging

│       Config

│

├── Context Engine

│       Screenshot

│       OCR

│       UI Automation

│       Clipboard

│       Active Window

│       Cursor

│       Keyboard

│

├── Overlay Engine

│       Highlight

│       Shapes

│       Tooltip

│       Pointer

│

├── AI Engine

│       Planner

│       Chat

│       Vision

│       Reflection

│       Tool Router

│

├── Tool Engine

│       Mouse

│       Keyboard

│       Shell

│       Browser

│       HTTP

│       Filesystem

│

├── Memory Engine

│       Sessions

│       Embeddings

│       Timeline

│       Workflows

│

├── Plugin Engine

│

└── Desktop App

------------------------------------------------------------

# ROADMAP

## Fase 0

Arquitetura

Objetivo

Definir toda arquitetura antes de escrever código.

Entregáveis

- estrutura das soluções
- projetos
- interfaces
- diagramas
- convenções
- eventos
- padrões

------------------------------------------------------------

## Fase 1

Desktop Host

Criar

- janela invisível
- tray icon
- atalhos globais
- configuração
- logging

------------------------------------------------------------

## Fase 2

Overlay Engine

Implementar

- janela transparente
- always on top
- clique transparente
- desenho vetorial
- highlight
- tooltip
- seta

------------------------------------------------------------

## Fase 3

Context Engine

Implementar

captura de tela

OCR

janela ativa

processo

mouse

clipboard

keyboard

UI Automation

Construir o objeto

Context

------------------------------------------------------------

## Fase 4

LLM Engine

Implementar providers

OpenAI

Ollama

Claude

Gemini

Interface única

ILLMProvider

------------------------------------------------------------

## Fase 5

Chat

Criar

assistente

histórico

streaming

tool calling

------------------------------------------------------------

## Fase 6

Overlay Inteligente

Permitir que o modelo responda

"aponte"

"circule"

"mostre"

O overlay interpreta essas ações.

------------------------------------------------------------

## Fase 7

Tools

Mouse

Keyboard

Clipboard

Filesystem

Shell

HTTP

Browser

------------------------------------------------------------

## Fase 8

Plugin SDK

Criar SDK

Cada plugin poderá registrar

prompts

ações

conhecimento

ferramentas

------------------------------------------------------------

## Fase 9

Memory

SQLite

Embeddings

Timeline

Workflows

Contextos

------------------------------------------------------------

## Fase 10

Voice

Whisper

TTS

Realtime

------------------------------------------------------------

## Fase 11

Computer Use

Loop

Observe

↓

Think

↓

Plan

↓

Act

↓

Verify

↓

Repeat

------------------------------------------------------------

# COMO VOCÊ (LLM) DEVE AGIR

Você será o arquiteto técnico principal deste projeto.

Sempre que eu pedir uma implementação:

1. Analise o impacto arquitetural.
2. Identifique dependências.
3. Sugira melhorias.
4. Explique decisões técnicas.
5. Só então proponha o código.

Sempre priorize componentes reutilizáveis e desacoplados.

Questione decisões quando houver alternativas melhores.

Mantenha uma visão de longo prazo para evitar retrabalho.

Ao final de cada implementação, atualize a documentação técnica e proponha os próximos passos do roadmap.

Nunca perca de vista a visão do produto: um assistente contextual para Windows, modular, extensível, orientado a eventos e preparado para evoluir para um agente de Computer Use completo.