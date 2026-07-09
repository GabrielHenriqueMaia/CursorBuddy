# Project Sentinel - Documentação da Arquitetura

## Visão Geral

Project Sentinel é construído ao redor de um **Loop Agêntico em 6 Fases** que roda continuamente para supervisionar e interagir com o desktop Windows.

```
     ┌─────────────────────────────────────┐
     │  LOOP AGÊNTICO - EXECUÇÃO CONTÍNUA  │
     └─────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 1. PERCEPÇÃO - Capturar Estado       │
     │    └─ Screenshot, OCR, UI Elements   │
     └──────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 2. CONTEXTO - Processar/Entender     │
     │    └─ LLM Analysis, Memória          │
     └──────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 3. PLANEJAMENTO - Definir Ações      │
     │    └─ LLM Planning, Decomposição     │
     └──────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 4. EXECUÇÃO - Implementar Ações      │
     │    └─ Clicks, Typing, Automation     │
     └──────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 5. REFLEXÃO - Analisar Resultados    │
     │    └─ LLM Analysis, Lessons          │
     └──────────────────────────────────────┘
                      ↓
     ┌──────────────────────────────────────┐
     │ 6. MEMÓRIA - Armazenar Aprendizados  │
     │    └─ Database, Indexação            │
     └──────────────────────────────────────┘
                      ↓
              [Loop volta ao 1]
```

## Estrutura de Pacotes

### `sentinel.core`
**Núcleo da arquitetura**

- **`types.py`** - Definições de tipos de dados que fluem pelo loop
  - `PerceptionData` - Output da fase 1
  - `ContextData` - Output da fase 2
  - `PlanData` - Output da fase 3
  - `ExecutionResult` - Output da fase 4
  - `ReflectionData` - Output da fase 5
  - `MemoryEntry` - Dados armazenados na fase 6

- **`base.py`** - Classes abstratas base para todos os módulos
  - `SentinelModule` - Base comum
  - `PerceptionModule` - Abstração fase 1
  - `ContextModule` - Abstração fase 2
  - `PlanningModule` - Abstração fase 3
  - `ExecutionModule` - Abstração fase 4
  - `ReflectionModule` - Abstração fase 5
  - `MemoryModule` - Abstração fase 6

- **`loop.py`** - Orquestrador principal
  - `AgenticLoop` - Coordena todas as fases
  - `run_iteration()` - Executa um ciclo completo
  - `run()` - Loop contínuo

### `sentinel.modules`
**Implementações dos módulos** (prototypes iniciais)

- **`perception.py`** - Captura do Windows
  - `WindowsPerceptionModule`
  - Responsável por: screenshots, OCR, UI elements, cursor

- **`context.py`** - Análise com LLM
  - `LLMContextModule`
  - Responsável por: intenção do usuário, memória, análise

- **`planning.py`** - Planejamento com LLM
  - `LLMPlanningModule`
  - Responsável por: decomposição, confidence scores

- **`execution.py`** - Execução no Windows
  - `WindowsExecutionModule`
  - Responsável por: clicks, typing, automação

- **`reflection.py`** - Análise com LLM
  - `LLMReflectionModule`
  - Responsável por: lessons, anomalias, recomendações

- **`memory.py`** - Armazenamento
  - `SQLiteMemoryModule`
  - Responsável por: store, retrieve, lifecycle

### `sentinel.llm`
**Agnósticismo de LLM Provider**

- **`provider.py`** - Abstrações e implementações
  - `LLMProvider` - Interface abstrata
  - `LLMMessage` - Estrutura de mensagem
  - `LLMResponse` - Estrutura de resposta
  - Implementations: `OpenAIProvider`, `AnthropicProvider`, `GoogleProvider`
  - Factory: `get_llm_provider()`

**Por que abstrair LLM?**
- Trocar providers sem mudar código dos módulos
- Suportar múltiplos providers simultaneamente
- Facilitar testes com mock LLMs
- Garantir portabilidade

### `sentinel.memory`
**Sistema de memória** (a ser implementado)

- Armazenamento persistente
- Indexação e busca
- Limpeza de memória
- Scoring de relevância

## Fluxo de Dados

### Entrada (User/System)
```
User Input / System State
         ↓
   [Perception]
```

### Ciclo Completo
```
Perception Data
     ↓
Context Data
     ↓
Plan Data
     ↓
Execution Result
     ↓
Reflection Data
     ↓
Memory Entries
```

### Output (Ações)
```
   [Execution]
     ↓
Actions on Windows
(Clicks, Typing, etc)
```

## Princípios de Design

### 1. Separação Crítica
Nunca misturar responsabilidades entre fases. Cada módulo:
- Recebe entrada bem definida
- Processa de forma isolada
- Retorna output estruturado
- Sem efeitos colaterais

### 2. Agnósticismo de LLM
```python
# Qualquer módulo que use LLM faz assim:

async def process(self, data):
    response = await self.llm_provider.chat(
        messages=[...],
        temperature=0.7
    )
    return parsed_response
```

Isso funciona com OpenAI, Claude, Gemini sem modificação.

### 3. Composição sobre Herança
```python
# ✅ BOM - Injeção de dependência
loop = AgenticLoop(
    llm_provider=llm,
    perception=perception_module,
    context=context_module,
    # ... etc
)

# ❌ RUIM - Herança profunda
class MyLoop(AgenticLoop):
    pass
```

### 4. Logging Estruturado
```python
# Usando structlog para rastreabilidade
logger.info(
    "Perception phase complete",
    iteration=5,
    active_window="chrome",
    duration_ms=123
)
```

### 5. Type Safety
```python
# Type hints completos para evitar bugs

async def process(
    self,
    perception: PerceptionData  # ← tipo explícito
) -> ContextData:              # ← retorno explícito
    ...
```

## Integração LLM

### Exemplo 1: OpenAI
```python
from sentinel.llm.provider import get_llm_provider

llm = get_llm_provider(
    "openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4"
)

response = await llm.chat(
    messages=[LLMMessage(role="user", content="...")]
)
```

### Exemplo 2: Claude
```python
llm = get_llm_provider(
    "claude",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus"
)

response = await llm.chat(messages=[...])
```

### Exemplo 3: Custom Provider
```python
from sentinel.llm.provider import LLMProvider

class MyCustomLLM(LLMProvider):
    async def chat(self, messages, **kwargs):
        # Sua implementação
        pass

loop = AgenticLoop(llm_provider=MyCustomLLM(...))
```

## Testabilidade

### Estrutura favorece testes
```python
# Mocks são fáceis
mock_perception = AsyncMock()
mock_perception.process.return_value = PerceptionData(...)

loop = AgenticLoop(
    llm_provider=llm,
    perception=mock_perception,  # ← Mock injected
    # ... rest with mocks
)

await loop.run_iteration()  # Testa a orquestração sem I/O
```

## Extensibilidade

### Adicionar novo provedor de LLM
1. Herdar de `LLMProvider`
2. Implementar `chat()` e `completion()`
3. Registrar em `get_llm_provider()`

### Adicionar novo módulo
1. Herdar de `SentinelModule` (ou fase específica)
2. Implementar `process()`
3. Injetar em `AgenticLoop`

### Adicionar nova fonte de dados
1. Estender `PerceptionModule`
2. Adicionar capture de nova fonte
3. Incluir em `PerceptionData`

## Próximas Etapas

1. **Implementar Percepção**
   - Screenshots com PIL
   - OCR com pytesseract
   - UI Elements com pywinauto
   - Cursor tracking

2. **Implementar Context**
   - Integrar LLM de verdade
   - Memory retrieval
   - Intent extraction

3. **Implementar Planning**
   - LLM-based planning
   - Task decomposition
   - Confidence scoring

4. **Implementar Execution**
   - Mouse actions
   - Keyboard input
   - Window management

5. **Implementar Reflection**
   - Result analysis
   - Lesson extraction
   - Anomaly detection

6. **Implementar Memory**
   - SQLite storage
   - Search/retrieval
   - Relevance scoring

7. **Sistema de Plugins**
   - Plugin loader
   - Hook system
   - Plugin marketplace

8. **UI Desktop**
   - Overlay system
   - Visual feedback
   - User controls

---

**Versão**: 1.0  
**Data**: 2026-07-09  
**Status**: Em Desenvolvimento Ativo
