"""Local LLM Provider implementations - Ollama, LM Studio, etc."""

import asyncio
import json
from typing import List, Optional, Dict, Any
import aiohttp
import structlog

from sentinel.llm.provider import LLMProvider, LLMMessage, LLMResponse

logger = structlog.get_logger(__name__)


class OllamaProvider(LLMProvider):
    """
    Ollama Local LLM Provider
    
    Supports any model available in Ollama:
    - qwen2.5-coder (1.5b, 7b)
    - llama3.1 (8b)
    - gemma3 (4b)
    - mistral
    - neural-chat
    - And many more...
    
    Make sure Ollama is running:
        ollama serve
    
    Then pull your desired model:
        ollama pull qwen2.5-coder:7b
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "qwen2.5-coder:7b",
        timeout: int = 300,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama server URL (default: localhost)
            model: Model name to use (default: qwen2.5-coder:7b)
            timeout: Request timeout in seconds
            config: Additional configuration options
        """
        super().__init__(api_key="local", config=config or {})
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def initialize(self) -> None:
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        logger.info(
            "Ollama provider initialized",
            base_url=self.base_url,
            model=self.model,
        )

    async def cleanup(self) -> None:
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            logger.info("Ollama provider cleaned up")

    async def _check_health(self) -> bool:
        """Check if Ollama server is running"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(
                f"{self.base_url}/api/tags",
                timeout=aiohttp.ClientTimeout(total=5),
            ) as response:
                return response.status == 200
        except Exception as e:
            logger.error("Ollama health check failed", error=str(e))
            return False

    async def _pull_model(self) -> bool:
        """Pull model if not available"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            logger.info("Pulling model", model=self.model)

            async with self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model, "stream": False},
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                return response.status in (200, 201)
        except Exception as e:
            logger.error("Failed to pull model", error=str(e))
            return False

    async def _convert_messages(self, messages: List[LLMMessage]) -> str:
        """Convert messages to Ollama chat format"""
        formatted_messages = []

        for msg in messages:
            formatted_messages.append({"role": msg.role, "content": msg.content})

        return json.dumps(formatted_messages)

    async def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 0.9,
        **kwargs,
    ) -> LLMResponse:
        """
        Chat with Ollama model.
        
        Args:
            messages: List of messages
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Max tokens to generate
            top_p: Top P sampling
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse with model output
        """
        if not self.session:
            await self.initialize()

        # Add system prompt if provided
        if system_prompt:
            messages = [
                LLMMessage(role="system", content=system_prompt),
                *messages,
            ]

        try:
            # Prepare request
            request_body = {
                "model": self.model,
                "messages": [
                    {"role": msg.role, "content": msg.content}
                    for msg in messages
                ],
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens,
                },
            }

            # Add any extra options
            for key, value in kwargs.items():
                if key not in ("system_prompt", "stream"):
                    request_body["options"][key] = value

            logger.info(
                "Ollama chat request",
                model=self.model,
                num_messages=len(messages),
                max_tokens=max_tokens,
            )

            # Make request
            async with self.session.post(
                f"{self.base_url}/api/chat",
                json=request_body,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama error: {error_text}")

                data = await response.json()

                response_text = data.get("message", {}).get("content", "")
                tokens_used = data.get("eval_count", 0)

                logger.info(
                    "Ollama response received",
                    tokens_used=tokens_used,
                    response_length=len(response_text),
                )

                return LLMResponse(
                    content=response_text,
                    model=self.model,
                    tokens_used=tokens_used,
                    raw_response=data,
                )

        except asyncio.TimeoutError:
            logger.error("Ollama request timeout", timeout=self.timeout)
            raise Exception(f"Ollama request timed out after {self.timeout}s")
        except Exception as e:
            logger.error("Ollama chat failed", error=str(e), exc_info=True)
            raise

    async def completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> LLMResponse:
        """
        Get completion from Ollama.
        
        Converts messages to a single prompt and generates completion.
        """
        # Convert messages to a single prompt
        prompt_parts = [msg.content for msg in messages]
        prompt = "\n".join(prompt_parts)

        if not self.session:
            await self.initialize()

        try:
            request_body = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            }

            logger.info(
                "Ollama completion request",
                model=self.model,
                prompt_length=len(prompt),
            )

            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=request_body,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama error: {error_text}")

                data = await response.json()

                response_text = data.get("response", "")
                tokens_used = data.get("eval_count", 0)

                return LLMResponse(
                    content=response_text,
                    model=self.model,
                    tokens_used=tokens_used,
                    raw_response=data,
                )

        except Exception as e:
            logger.error("Ollama completion failed", error=str(e))
            raise

    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models in Ollama"""
        if not self.session:
            await self.initialize()

        try:
            async with self.session.get(
                f"{self.base_url}/api/tags",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status != 200:
                    raise Exception("Failed to list models")

                data = await response.json()
                return data.get("models", [])

        except Exception as e:
            logger.error("Failed to list models", error=str(e))
            return []

    async def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific model"""
        if not self.session:
            await self.initialize()

        model = model_name or self.model

        try:
            async with self.session.post(
                f"{self.base_url}/api/show",
                json={"name": model},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status != 200:
                    raise Exception(f"Model not found: {model}")

                return await response.json()

        except Exception as e:
            logger.error("Failed to get model info", error=str(e), model=model)
            return {}
