# Project Sentinel

**Assistente Inteligente para Automação de Desktop Windows**

Um framework open-source, modular e extensível para construir agentes de IA que entendem e interagem com o Windows desktop.

## 🎯 Visão

Criar uma **camada inteligente sobre o Windows** capaz de:
- 👁️ Entender o contexto (aplicações abertas, janelas, conteúdo da tela)
- 🧠 Processar informações através de OCR, UI Automation e Vision Models
- 🗣️ Interagir por texto e voz
- 🎯 Desenhar overlays e apontar elementos na tela
- 🧠 Aprender padrões de usuário e armazenar memória
- ⚙️ Automatizar tarefas e evoluir para Computer Use

## 🏗️ Arquitetura

O sistema implementa um **Loop Agêntico em 6 Fases**:

```
┌─────────────────────────────────────────────────┐
│         AGENTIC LOOP - CICLO CONTÍNUO            │
└─────────────────────────────────────────────────┘

1️⃣  PERCEPÇÃO
    └─ Captura de estado do sistema
    └─ Screenshots, OCR, UI elements
    └─ Posição do cursor, aplicação ativa

        ↓

2️⃣  CONTEXTO
    └─ Processamento da percepção
    └─ Inferência de intenção do usuário
    └─ Busca de memórias relevantes
    └─ Análise contextual com LLM

        ↓

3️⃣  PLANEJAMENTO
    └─ Definição de objetivos
    └─ Geração de plano de ação
    └─ Decomposição de tarefas
    └─ Scores de confiança

        ↓

4️⃣  EXECUÇÃO
    └─ Implementação de passos planejados
    └─ Tratamento de erros
    └─ Captura de efeitos colaterais
    └─ Registro de resultados

        ↓

5️⃣  REFLEXÃO
    └─ Análise de sucesso/falha
    └─ Extração de lições aprendidas
    └─ Identificação de anomalias
    └─ Recomendações

        ↓

6️⃣  MEMÓRIA
    └─ Armazenamento de aprendizados
    └─ Indexação para busca rápida
    └─ Atualização de relevância
    └─ Gestão do ciclo de vida
```

## 📦 Estrutura de Projeto

```
CursorBuddy/
├── src/
│   └── sentinel/
│       ├── core/
│       │   ├── base.py          # Abstrações base para módulos
│       │   ├── types.py         # Tipos de dados do loop
│       │   ├── loop.py          # Orquestrador do loop agêntico
│       │   └── __init__.py
│       ├── modules/             # Implementações dos módulos
│       │   ├── perception.py
│       │   ├── context.py
│       │   ├── planning.py
│       │   ├── execution.py
│       │   ├── reflection.py
│       │   ├── memory.py
│       │   └── __init__.py
│       ├── llm/
│       │   ├── provider.py      # Abstrações agnósticas de LLM
│       │   └── __init__.py
│       ├── memory/              # Sistema de memória
│       │   └── __init__.py
│       └── __init__.py
├── tests/                       # Testes unitários e integração
├── setup.py                     # Configuração do pacote
├── requirements.txt             # Dependências
├── pyproject.toml              # Configuração moderna Python
├── ideia.md                    # Visão original do projeto
└── README.md
```

## 🔑 Princípios

### 1. **Separação de Responsabilidades**
Cada fase (Percepção, Contexto, Planejamento, Execução, Reflexão, Memória) é completamente isolada com interfaces bem definidas.

### 2. **Agnósticismo de LLM**
O sistema funciona com qualquer provedor:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Providers customizados

Basta implementar a interface `LLMProvider`.

### 3. **Modularidade**
Cada módulo é um plugin:
- Pode ser substituído por alternativas
- Pode ser desativado
- Pode ser estendido

### 4. **Qualidade de Código**
- ✅ Type hints completos
- ✅ Logging estruturado
- ✅ Tratamento de erros
- ✅ Testes automatizados
- ✅ Documentação

### 5. **Extensibilidade**
- Plugins para novos módulos
- Interfaces para integração
- Hooks e eventos

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
cd CursorBuddy

# Crie um ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# ou
source venv/bin/activate      # Linux/Mac

# Instale dependências
pip install -e .
```

### Usando Ollama (LLM Local) - ⭐ Recomendado

**Porque usar Ollama?**
- 💰 Gratuito, roda localmente
- 🚀 Rápido, sem latência de rede
- 🔒 Privado, dados não saem da máquina
- ♾️ Ilimitado, sem throttling

**Setup:**

```bash
# 1. Instale Ollama
#    https://ollama.ai

# 2. Inicie o servidor
ollama serve

# 3. Em outro terminal, puxe um modelo
#    Para programação (RECOMENDADO):
ollama pull qwen2.5-coder:7b

#    Alternativas:
ollama pull llama3.1:8b       # Versátil
ollama pull gemma3:4b          # Rápido & leve
ollama pull qwen3:8b           # Mais poderoso
```

**Teste a conexão:**

```bash
# No diretório do projeto
python test_ollama.py           # Lista todos os modelos
python test_ollama.py --list    # Apenas lista
python test_ollama.py --chat-only  # Testa chat
python test_ollama.py --model llama3.1:8b  # Testa modelo específico
```

### Rodar o Sentinel com Ollama

```bash
# Usar modelo padrão (qwen2.5-coder:7b)
python -m sentinel.cli --debug

# Usar modelo específico
python -m sentinel.cli --model llama3.1:8b --debug

# Limitar iterações
python -m sentinel.cli --iterations 10

# Listar modelos disponíveis
python -m sentinel.cli --list-models
```

### Usar como Library com Ollama

```python
import asyncio
from sentinel.llm.local import OllamaProvider
from sentinel.core.loop import AgenticLoop

async def main():
    # Criar provider local
    llm = OllamaProvider(
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b",  # ou qualquer outro modelo
    )
    
    # Criar loop (módulos implementados depois)
    loop = AgenticLoop(llm_provider=llm)
    
    # Rodar
    await loop.run(max_iterations=5)

asyncio.run(main())
```

### Usando Cloud APIs (OpenAI, Claude, Gemini)

Se preferir usar cloud APIs:

```bash
# OpenAI
export SENTINEL_LLM_PROVIDER=openai
export SENTINEL_OPENAI_API_KEY=sk-...

# Claude (Anthropic)
export SENTINEL_LLM_PROVIDER=claude
export SENTINEL_CLAUDE_API_KEY=sk-ant-...

# Gemini
export SENTINEL_LLM_PROVIDER=gemini
export SENTINEL_GEMINI_API_KEY=...

# Rodar
python -m sentinel.cli --debug
```

## 📋 Roadmap

### Fase 1: Fundações ✅ Em Progresso
- [x] Arquitetura base do loop agêntico
- [x] Abstrações de tipos de dados
- [x] Interfaces de módulos
- [x] Abstração agnóstica de LLM
- [ ] Implementações iniciais dos módulos

### Fase 2: Percepção
- [ ] Captura de screenshots
- [ ] OCR com Tesseract
- [ ] UI Automation com pywinauto
- [ ] Extração de elementos
- [ ] Tracking de cursor

### Fase 3: Contexto
- [ ] Análise de intenção
- [ ] Busca em memória
- [ ] Integração com LLM
- [ ] Construção de prompt contextual

### Fase 4: Planejamento
- [ ] Geração de planos
- [ ] Decomposição de tarefas
- [ ] Scoring de confiança
- [ ] Geração de alternativas

### Fase 5: Execução
- [ ] Execução de ações
- [ ] Tratamento de erros
- [ ] Rollback de falhas
- [ ] Logging de resultados

### Fase 6: Reflexão
- [ ] Análise de resultados
- [ ] Extração de lições
- [ ] Detecção de anomalias
- [ ] Geração de recomendações

### Fase 7: Memória
- [ ] Sistema de armazenamento
- [ ] Indexação e busca
- [ ] Gestão de relevância
- [ ] Limpeza de memória

### Fase 8: UI e Interação
- [ ] Overlays na tela
- [ ] Interface de controle
- [ ] Apontadores
- [ ] Chat interface

## 🛠️ Tecnologias

### Agnóstico a LLM Provider ✨
- **Ollama** (Local, Gratuito) ← Recomendado
  - qwen2.5-coder (1.5b, 7b)
  - llama3.1 (8b)
  - gemma3 (4b)
  - qwen3 (8b)
  - E mais de 100 modelos disponíveis

- **OpenAI**
  - GPT-4
  - GPT-4 Turbo
  - GPT-3.5 Turbo

- **Anthropic (Claude)**
  - Claude 3 Opus
  - Claude 3 Sonnet
  - Claude 3 Haiku

- **Google (Gemini)**
  - Gemini Pro
  - Gemini Ultra

### Core
- **Python 3.10+** - Linguagem principal
- **Pydantic** - Validação de dados
- **structlog** - Logging estruturado
- **aiohttp** - Async HTTP client (para Ollama)

### Integrações
- **OpenAI SDK** - GPT integration
- **Anthropic SDK** - Claude integration
- **Google Generative AI** - Gemini integration
- **pywin32** - Windows API
- **pytesseract** - OCR
- **pytest** - Testes

## 📝 Princípios de Desenvolvimento

### Código
- Sempre refatorar antes de adicionar features
- Interfaces primeiro, implementação depois
- Type hints obrigatórios
- Logging estruturado em tudo

### Arquitetura
- Sempre pensar em composição antes de herança
- Manter dependências mínimas
- Usar dependency injection
- Documentar decisões arquiteturais

### Testes
- Testar comportamentos, não implementações
- Mocks para integrações externas
- Testes de integração para o loop
- CI/CD pipeline

## 📚 Documentação

- [Arquitetura Detalhada](docs/architecture.md) - Em construção
- [Software Design Document (SDD)](docs/SDD.md) - Template e decisões de design
- [Guia de Módulos](docs/modules.md) - Em construção
- [API Reference](docs/api.md) - Em construção
- [Exemplos](examples/) - Em construção

## 🤝 Contribuindo

Project Sentinel é open-source e aceita contribuições!

1. Faça um fork
2. Crie uma branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 👤 Autor

Project Sentinel - Uma iniciativa de IA para automação inteligente de desktop

---

**Status**: 🚧 Em Desenvolvimento Ativo

Última atualização: 2026-07-09
