# Guia Ollama - LLM Local para Project Sentinel

## 📋 O que é Ollama?

Ollama é uma ferramenta que permite rodar modelos de LLM localmente na sua máquina, sem depender de APIs em nuvem.

**Vantagens:**
- 💰 **Gratuito** - Sem custos por requisição
- 🚀 **Rápido** - Latência local, sem rede
- 🔒 **Privado** - Dados não saem do seu PC
- ♾️ **Ilimitado** - Sem rate limits ou throttling
- 🔧 **Flexível** - Múltiplos modelos, fácil trocar

**Desvantagens:**
- 💾 **RAM** - Precisa de espaço (4-16 GB depende do modelo)
- 🐢 **Velocidade** - Mais lento que GPT-4 cloud (mas ainda rápido)
- 🤖 **Qualidade** - Modelos open-source vs proprietary

---

## 🚀 Instalação Ollama

### Windows
1. Baixe [Ollama para Windows](https://ollama.ai)
2. Execute o instalador
3. Ollama estará disponível como app ou linha de comando

### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

### macOS
1. Baixe [Ollama para macOS](https://ollama.ai)
2. Execute o instalador

---

## 📦 Puxando Modelos

Modelos recomendados para Project Sentinel:

### Coding (Recomendado para seu caso)
```bash
# Qwen2.5-Coder 7B - MELHOR ESCOLHA
ollama pull qwen2.5-coder:7b
# Otimizado para código, rápido, bom reasoning

# Alternativa leve
ollama pull qwen2.5-coder:1.5b
# Mais rápido, menos VRAM, qualidade reduzida
```

### General Purpose
```bash
# Llama 3.1 8B - Versátil
ollama pull llama3.1:8b
# Bom para tudo, conversas, análise, criatividade

# Gemma 3 4B - Leve
ollama pull gemma3:4b
# Muito rápido, menos VRAM, bom pra tarefas simples

# Qwen 3 8B - Poderoso
ollama pull qwen3:8b
# Último modelo, mais poderoso, mais VRAM necessário
```

---

## 🎯 Requisitos de Sistema

| Modelo | VRAM | Speed | Quality | Recomendação |
|--------|------|-------|---------|--------------|
| qwen2.5-coder:1.5b | 2-4 GB | ⚡⚡⚡ Muito Rápido | Bom | Máquinas fracas |
| qwen2.5-coder:7b | 6-8 GB | ⚡⚡ Rápido | Excelente | ⭐ RECOMENDADO |
| gemma3:4b | 4-6 GB | ⚡⚡⚡ Muito Rápido | Bom | Máquinas com pouca RAM |
| llama3.1:8b | 6-8 GB | ⚡⚡ Rápido | Excelente | Versátil |
| qwen3:8b | 8-12 GB | ⚡ Rápido | Melhor | Máquinas poderosas |

---

## 🔧 Iniciando Ollama

### Terminal
```bash
# Inicie o servidor (fica rodando em background)
ollama serve

# Ou em outro terminal, teste o modelo
ollama run qwen2.5-coder:7b

# Digite sua mensagem
>>> Olá, qual é o seu nome?
```

### GUI (Windows)
- Ollama icon no system tray → Abra console
- Ou procure "Ollama" no menu iniciar

---

## 🧪 Testando com Project Sentinel

### 1. Verificar Conectividade

```bash
# No diretório do projeto
python test_ollama.py

# Deve listar seus modelos:
# ✅ Found 6 models:
#   1. qwen2.5-coder:7b              4.70 GB
#   2. llama3.1:8b                   4.90 GB
#   3. gemma3:4b                     3.30 GB
#   ...
```

### 2. Testar Chat
```bash
python test_ollama.py --model qwen2.5-coder:7b --chat-only

# Deve receber uma resposta e mostrar tokens usados
```

### 3. Listar Modelos Disponíveis
```bash
python -m sentinel.cli --list-models

# Mostra todos os modelos que você tem
```

---

## 💻 Usando em Project Sentinel

### Via CLI

```bash
# Usar modelo padrão (qwen2.5-coder:7b)
python -m sentinel.cli --debug

# Usar outro modelo
python -m sentinel.cli --model llama3.1:8b --debug

# Limitar iterações
python -m sentinel.cli --iterations 5 --debug
```

### Via Código

```python
import asyncio
from sentinel.llm.local import OllamaProvider
from sentinel.core.loop import AgenticLoop

async def main():
    # Criar provider
    llm = OllamaProvider(
        base_url="http://localhost:11434",  # URL do Ollama
        model="qwen2.5-coder:7b",           # Seu modelo
        timeout=300                          # Timeout em segundos
    )
    
    # Usar em loop agêntico
    loop = AgenticLoop(llm_provider=llm)
    await loop.run(max_iterations=10)

asyncio.run(main())
```

### Via Variáveis de Ambiente

```bash
# Configurar modelo padrão
export SENTINEL_LLM_PROVIDER=ollama
export SENTINEL_OLLAMA_MODEL=qwen2.5-coder:7b
export SENTINEL_OLLAMA_URL=http://localhost:11434

# Depois rodar normalmente
python -m sentinel.cli --debug
```

---

## 🎓 Dicas de Performance

### 1. GPU Acceleration
Ollama deteta automaticamente GPU disponível (NVIDIA, AMD, etc).

**Para NVIDIA com CUDA:**
```bash
# Instale NVIDIA CUDA Toolkit
# Ollama vai usar GPU automaticamente
```

**Para AMD:**
```bash
# Instale ROCm
# Ollama vai usar GPU automaticamente
```

### 2. Otimizando para seu Hardware

**Máquina fraca (2-4 GB RAM):**
```bash
ollama pull qwen2.5-coder:1.5b
python -m sentinel.cli --model qwen2.5-coder:1.5b
```

**Máquina média (8 GB RAM):**
```bash
ollama pull qwen2.5-coder:7b
python -m sentinel.cli --model qwen2.5-coder:7b  # ⭐ Recomendado
```

**Máquina potente (16+ GB RAM):**
```bash
ollama pull qwen3:8b
python -m sentinel.cli --model qwen3:8b
```

### 3. Monitorando Uso

**Ver processador/memória em uso:**
```bash
# Terminal separado enquanto Ollama roda
ollama list          # Lista modelos carregados
```

---

## ⚠️ Troubleshooting

### Erro: "Cannot connect to Ollama"
```
❌ Cannot connect to Ollama!
   Make sure Ollama is running: ollama serve
```

**Solução:**
```bash
# Terminal 1: Inicie Ollama
ollama serve

# Terminal 2: Rode seu código
python test_ollama.py
```

### Erro: "Model not found"
```
❌ Error: Model not found: qwen2.5-coder:7b
```

**Solução:**
```bash
# Puxe o modelo
ollama pull qwen2.5-coder:7b

# Verifique modelos disponíveis
ollama list
```

### Resposta muito lenta
**Causas:**
- Modelo é muito grande pra sua VRAM (swapping)
- Não tem GPU acceleration
- CPU fraca

**Soluções:**
1. Use modelo menor: `ollama pull qwen2.5-coder:1.5b`
2. Instale GPU drivers (CUDA/ROCm)
3. Feche outros programas para liberar RAM

### Erro de memória (OOM)
```
CUDA out of memory / OOM error
```

**Solução:**
```bash
# Use modelo menor
ollama pull gemma3:4b

# Ou aumente swap/RAM
```

---

## 🔄 Trocando Modelos

Fácil trocar entre modelos:

```bash
# Puxe novo modelo
ollama pull llama3.1:8b

# Use ele
python -m sentinel.cli --model llama3.1:8b --debug

# Ou na CLI:
python test_ollama.py --model llama3.1:8b --chat-only
```

Você pode ter múltiplos modelos instalados e trocar entre eles!

---

## 📚 Recursos Adicionais

- **Ollama Official**: https://ollama.ai
- **Model Library**: https://ollama.ai/library
- **GitHub**: https://github.com/jmorganca/ollama
- **Discord Community**: https://discord.gg/ollama

---

## 🎯 Próximas Etapas

1. ✅ Instale Ollama
2. ✅ Puxe qwen2.5-coder:7b
3. ✅ Rode `python test_ollama.py`
4. ✅ Teste com `python -m sentinel.cli --debug`
5. 📝 Implemente módulos (Perception, Context, etc)
6. 🚀 Rode loop agêntico completo

---

**Data**: 2026-07-09  
**Versão**: 1.0  
**Status**: Pronto para uso! 🚀
