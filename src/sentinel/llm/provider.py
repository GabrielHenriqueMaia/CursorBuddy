"""LLM Provider Abstraction - agnóstico a provider"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from typing import Union


@dataclass
class LLMMessage:
    """Message in conversation"""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Dict[str, Any] = None


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    tokens_used: int
    raw_response: Dict[str, Any]


class LLMProvider(ABC):
    """Abstract base for LLM providers (OpenAI, Claude, Gemini, etc)"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key
        self.config = config or {}

    @abstractmethod
    async def completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Get completion from LLM"""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Chat with LLM"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI implementation"""

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, kwargs)
        self.model = model

    async def completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """OpenAI completion"""
        # Implementation will be added when OpenAI SDK is integrated
        pass

    async def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """OpenAI chat"""
        pass


class AnthropicProvider(LLMProvider):
    """Claude (Anthropic) implementation"""

    def __init__(self, api_key: str, model: str = "claude-3-opus", **kwargs):
        super().__init__(api_key, kwargs)
        self.model = model

    async def completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Claude completion"""
        pass

    async def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Claude chat"""
        pass


class GoogleProvider(LLMProvider):
    """Google Gemini implementation"""

    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(api_key, kwargs)
        self.model = model

    async def completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Gemini completion"""
        pass

    async def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Gemini chat"""
        pass


def get_llm_provider(provider: str, api_key: Optional[str] = None, **kwargs) -> LLMProvider:
    """Factory function to get LLM provider"""
    from sentinel.llm.local import OllamaProvider
    
    providers = {
        "openai": OpenAIProvider,
        "claude": AnthropicProvider,
        "anthropic": AnthropicProvider,
        "gemini": GoogleProvider,
        "google": GoogleProvider,
        "ollama": OllamaProvider,
        "local": OllamaProvider,
    }

    provider_class = providers.get(provider.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider}")

    # Ollama doesn't need API key
    if provider.lower() in ("ollama", "local"):
        return provider_class(**kwargs)
    
    if not api_key:
        raise ValueError(f"API key required for {provider}")
        
    return provider_class(api_key, **kwargs)
