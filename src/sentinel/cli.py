"""CLI for Project Sentinel"""

import asyncio
import os
from typing import Optional
import structlog
import click

from sentinel.core.loop import AgenticLoop
from sentinel.llm.provider import get_llm_provider
from sentinel.llm.local import OllamaProvider
from sentinel.modules import (
    WindowsPerceptionModule,
    LLMContextModule,
    LLMPlanningModule,
    WindowsExecutionModule,
    LLMReflectionModule,
    SQLiteMemoryModule,
)

logger = structlog.get_logger(__name__)


def get_llm_from_env() -> tuple[str, dict]:
    """Get LLM provider configuration from environment"""
    provider = os.getenv("SENTINEL_LLM_PROVIDER", "ollama").lower()
    
    # Local Ollama provider
    if provider in ("ollama", "local"):
        model = os.getenv("SENTINEL_OLLAMA_MODEL", "qwen2.5-coder:7b")
        base_url = os.getenv("SENTINEL_OLLAMA_URL", "http://localhost:11434")
        return provider, {
            "base_url": base_url,
            "model": model,
        }
    
    # Cloud providers
    api_key = os.getenv(f"SENTINEL_{provider.upper()}_API_KEY")
    if not api_key:
        raise ValueError(
            f"API key not found for {provider}. "
            f"Set SENTINEL_{provider.upper()}_API_KEY environment variable"
        )

    return provider, {"api_key": api_key}


async def list_ollama_models() -> None:
    """List available models in local Ollama"""
    try:
        provider = OllamaProvider()
        await provider.initialize()
        models = await provider.list_models()
        await provider.cleanup()

        if not models:
            click.echo("No models found in Ollama")
            return

        click.echo("\n✨ Available Ollama Models:\n")
        for model in models:
            name = model.get("name", "unknown")
            size_gb = model.get("size", 0) / (1024**3)
            modified = model.get("modified_at", "unknown")
            click.echo(f"  • {name:<30} ({size_gb:.2f}GB)")
        
        click.echo()
    except Exception as e:
        logger.error("Failed to list models", error=str(e))
        click.echo(f"❌ Error: Could not connect to Ollama. Is it running?")


async def main(
    max_iterations: Optional[int] = None,
    debug: bool = False,
    use_ollama: bool = True,
    model: Optional[str] = None,
    list_models: bool = False,
):
    """
    Run the agentic loop.
    
    Args:
        max_iterations: Maximum number of iterations
        debug: Enable debug logging
        use_ollama: Use Ollama instead of cloud API
        model: Specific model to use
        list_models: List available models
    """
    # Configure logging
    if debug:
        structlog.configure(
            processors=[
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.PrintLoggerFactory(),
        )
    else:
        structlog.configure(
            processors=[
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.PrintLoggerFactory(),
        )

    if list_models:
        await list_ollama_models()
        return

    logger.info("Starting Project Sentinel")

    try:
        # Get LLM provider
        provider_name, provider_kwargs = get_llm_from_env()
        logger.info("Using LLM provider", provider=provider_name)

        # Override model if specified
        if model and provider_name in ("ollama", "local"):
            provider_kwargs["model"] = model
            logger.info("Using custom model", model=model)

        llm = get_llm_provider(provider_name, **provider_kwargs)

        # Initialize if it's a local provider
        if isinstance(llm, OllamaProvider):
            logger.info("Initializing Ollama provider")
            await llm.initialize()

        # Create modules
        perception = WindowsPerceptionModule("perception")
        context = LLMContextModule("context", {"llm": llm})
        planning = LLMPlanningModule("planning", {"llm": llm})
        execution = WindowsExecutionModule("execution")
        reflection = LLMReflectionModule("reflection", {"llm": llm})
        memory = SQLiteMemoryModule("memory")

        # Create and run loop
        loop = AgenticLoop(
            llm_provider=llm,
            perception=perception,
            context=context,
            planning=planning,
            execution=execution,
            reflection=reflection,
            memory=memory,
        )

        await loop.run(max_iterations=max_iterations)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error("Fatal error", error=str(e), exc_info=True)
        raise
    finally:
        if isinstance(llm, OllamaProvider):
            await llm.cleanup()


if __name__ == "__main__":

    @click.group()
    def cli():
        """Project Sentinel - Agentic Desktop Assistant"""

    @cli.command(name="start")
    @click.option(
        "--iterations",
        "-i",
        type=int,
        default=None,
        help="Maximum number of iterations",
    )
    @click.option("--debug", "-d", is_flag=True, help="Enable debug logging")
    @click.option(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Specify Ollama model (e.g., qwen2.5-coder:7b, llama3.1:8b)",
    )
    @click.option(
        "--list-models",
        is_flag=True,
        help="List available Ollama models",
    )
    def start(iterations: Optional[int], debug: bool, model: Optional[str], list_models: bool):
        """Start the agentic loop"""
        asyncio.run(main(
            max_iterations=iterations,
            debug=debug,
            model=model,
            list_models=list_models,
        ))

    @cli.command(name="format")
    def format_cmd():
        """Open formatting panel (reads clipboard or stdin)"""
        from sentinel.format_panel import main as format_main
        format_main()

    cli()
