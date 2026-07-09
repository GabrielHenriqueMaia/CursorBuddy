"""Example: Running with Local Ollama LLM

This example shows how to use Project Sentinel with a local Ollama instance.

Prerequisites:
    1. Install Ollama: https://ollama.ai
    2. Start Ollama: ollama serve
    3. Pull a model: ollama pull qwen2.5-coder:7b

Available models for your use:
    - qwen2.5-coder:1.5b    (Smallest, fastest)
    - qwen2.5-coder:7b      (Recommended, good balance)
    - llama3.1:8b           (Versatile, good quality)
    - gemma3:4b             (Fast, good for simple tasks)
    - qwen3:8b              (Latest Qwen, powerful)
"""

import asyncio
import os
from sentinel.llm.local import OllamaProvider
from sentinel.core.loop import AgenticLoop


async def main():
    """
    Example 1: Using Ollama with default settings
    """
    print("=" * 60)
    print("Project Sentinel - Local Ollama Example")
    print("=" * 60)

    # Create Ollama provider (uses qwen2.5-coder:7b by default)
    ollama = OllamaProvider(
        base_url="http://localhost:11434",
        model="qwen2.5-coder:7b",
        timeout=300,
    )

    # Initialize the provider
    await ollama.initialize()

    # Test connection
    print("\n🔍 Checking Ollama connection...")
    models = await ollama.list_models()
    
    if models:
        print(f"✅ Found {len(models)} models in Ollama:\n")
        for model in models:
            name = model.get("name", "unknown")
            size_mb = model.get("size", 0) / (1024**2)
            print(f"   • {name:<35} ({size_mb:>8.1f} MB)")
    else:
        print("❌ No models found. Did you forget to run 'ollama serve'?")
        await ollama.cleanup()
        return

    # Test a simple chat
    print("\n💬 Testing chat with Ollama...")
    from sentinel.llm.provider import LLMMessage

    messages = [
        LLMMessage(role="user", content="Hello! What's your name and what can you do?"),
    ]

    try:
        response = await ollama.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=200,
        )

        print(f"\n📝 Response from {response.model}:")
        print(f"   {response.content}")
        print(f"\n📊 Tokens used: {response.tokens_used}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Cleanup
    await ollama.cleanup()
    print("\n✨ Done!")


async def example_with_loop():
    """
    Example 2: Creating an agentic loop with Ollama

    Note: The implementation modules are still TODOs,
    so this won't execute fully yet. But this shows how it will work.
    """
    from sentinel.modules import (
        WindowsPerceptionModule,
        LLMContextModule,
        LLMPlanningModule,
        WindowsExecutionModule,
        LLMReflectionModule,
        SQLiteMemoryModule,
    )

    print("\n" + "=" * 60)
    print("Creating Agentic Loop with Local Ollama")
    print("=" * 60)

    # Create Ollama provider
    llm = OllamaProvider(
        model="qwen2.5-coder:7b",
        timeout=300,
    )

    # Create modules (all stubs for now)
    perception = WindowsPerceptionModule("perception")
    context = LLMContextModule("context", {"llm": llm})
    planning = LLMPlanningModule("planning", {"llm": llm})
    execution = WindowsExecutionModule("execution")
    reflection = LLMReflectionModule("reflection", {"llm": llm})
    memory = SQLiteMemoryModule("memory")

    # Create loop
    loop = AgenticLoop(
        llm_provider=llm,
        perception=perception,
        context=context,
        planning=planning,
        execution=execution,
        reflection=reflection,
        memory=memory,
    )

    print("\n✅ Agentic loop created!")
    print("   - Using Ollama for LLM tasks (Context, Planning, Reflection)")
    print("   - Will use Windows automation for Perception & Execution")
    print("   - Will use SQLite for Memory storage")
    print("\n   Ready to run when modules are implemented!")


async def example_model_selection():
    """
    Example 3: How to select different models for different tasks
    """
    print("\n" + "=" * 60)
    print("Model Selection Guide")
    print("=" * 60)

    models = {
        "qwen2.5-coder:1.5b": {
            "size": "~986 MB",
            "speed": "⚡️ Very Fast",
            "quality": "Good for simple tasks",
            "use": "Fast inference, low VRAM"
        },
        "qwen2.5-coder:7b": {
            "size": "~4.7 GB",
            "speed": "⚡️ Fast",
            "quality": "Good for coding and reasoning",
            "use": "RECOMMENDED - Best balance"
        },
        "llama3.1:8b": {
            "size": "~4.9 GB",
            "speed": "⚡️ Fast",
            "quality": "Excellent for general tasks",
            "use": "Versatile, good for diverse tasks"
        },
        "gemma3:4b": {
            "size": "~3.3 GB",
            "speed": "⚡️⚡️ Very Fast",
            "quality": "Good for simple tasks",
            "use": "Lightweight, efficient"
        },
        "qwen3:8b": {
            "size": "~5.2 GB",
            "speed": "⚡️ Fast",
            "quality": "Latest, powerful",
            "use": "Best quality, higher VRAM"
        },
    }

    for model_name, info in models.items():
        print(f"\n📦 {model_name}")
        for key, value in info.items():
            print(f"   {key:<8}: {value}")


if __name__ == "__main__":
    # Run the basic example
    asyncio.run(main())

    # Uncomment to see loop example:
    # asyncio.run(example_with_loop())

    # Uncomment to see model selection guide:
    # asyncio.run(example_model_selection())
