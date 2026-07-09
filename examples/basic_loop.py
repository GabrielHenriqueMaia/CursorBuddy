"""Example: Running a basic agentic loop"""

import asyncio
from sentinel.core.loop import AgenticLoop
from sentinel.llm.provider import get_llm_provider


async def main():
    """
    Example of running the agentic loop.
    
    This is a minimal example showing how to:
    1. Create an LLM provider
    2. Create an agentic loop
    3. Run iterations
    """

    # Step 1: Create LLM provider (using OpenAI in this example)
    llm = get_llm_provider(
        "openai",
        api_key="sk-...",  # Replace with your actual API key
    )

    # Step 2: Create agentic loop
    # (modules will be added once implementations are complete)
    loop = AgenticLoop(llm_provider=llm)

    # Step 3: Run a few iterations
    await loop.run(max_iterations=5)


if __name__ == "__main__":
    asyncio.run(main())
