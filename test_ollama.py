"""Quick test script for Ollama connectivity

Run this to test if your Ollama setup is working correctly.

Usage:
    python test_ollama.py
    python test_ollama.py --model llama3.1:8b
    python test_ollama.py --list
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentinel.llm.local import OllamaProvider
from sentinel.llm.provider import LLMMessage


async def test_list_models():
    """Test: List all available models"""
    print("\n📋 Listing Ollama Models")
    print("-" * 60)
    
    provider = OllamaProvider()
    await provider.initialize()
    
    try:
        models = await provider.list_models()
        
        if not models:
            print("❌ No models found!")
            await provider.cleanup()
            return False
        
        print(f"\n✅ Found {len(models)} models:\n")
        
        for i, model in enumerate(models, 1):
            name = model.get("name", "unknown")
            size_gb = model.get("size", 0) / (1024**3)
            modified = model.get("modified_at", "unknown")[:10]  # Date only
            print(f"  {i}. {name:<35} | {size_gb:>6.2f} GB | {modified}")
        
        await provider.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await provider.cleanup()
        return False


async def test_chat(model: str = "qwen2.5-coder:7b"):
    """Test: Chat with a model"""
    print(f"\n💬 Testing Chat with {model}")
    print("-" * 60)
    
    provider = OllamaProvider(model=model)
    await provider.initialize()
    
    try:
        messages = [
            LLMMessage(
                role="user",
                content="Describe yourself briefly in one sentence."
            ),
        ]
        
        print(f"\n📤 Sending message to {model}...")
        response = await provider.chat(messages, max_tokens=100)
        
        print(f"\n📥 Response:\n")
        print(f"   {response.content}")
        print(f"\n📊 Tokens used: {response.tokens_used}")
        print(f"   Model: {response.model}")
        
        await provider.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await provider.cleanup()
        return False


async def test_completion(model: str = "qwen2.5-coder:7b"):
    """Test: Get completion"""
    print(f"\n🔮 Testing Completion with {model}")
    print("-" * 60)
    
    provider = OllamaProvider(model=model)
    await provider.initialize()
    
    try:
        messages = [
            LLMMessage(role="user", content="Complete this code: def hello"),
        ]
        
        print(f"\n📤 Requesting completion from {model}...")
        response = await provider.completion(messages, max_tokens=50)
        
        print(f"\n📥 Completion:\n")
        print(f"   {response.content}")
        print(f"\n📊 Tokens used: {response.tokens_used}")
        
        await provider.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await provider.cleanup()
        return False


async def main():
    """Run all tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Ollama connectivity")
    parser.add_argument("--list", action="store_true", help="List models only")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Model to test")
    parser.add_argument("--chat-only", action="store_true", help="Test chat only")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("Project Sentinel - Ollama Connectivity Test")
    print("=" * 60)
    
    # Always list models first
    success = await test_list_models()
    
    if not success:
        print("\n❌ Cannot connect to Ollama!")
        print("   Make sure Ollama is running: ollama serve")
        return
    
    if args.list:
        return
    
    # Test chat
    print("\n" + "=" * 60)
    success_chat = await test_chat(args.model)
    
    if not args.chat_only and success_chat:
        # Test completion
        print("\n" + "=" * 60)
        await test_completion(args.model)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
