"""The Agentic Loop - Main orchestration engine"""

import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
import structlog

from sentinel.core.base import (
    PerceptionModule,
    ContextModule,
    PlanningModule,
    ExecutionModule,
    ReflectionModule,
    MemoryModule,
)
from sentinel.core.types import (
    PerceptionData,
    ContextData,
    PlanData,
    ExecutionResult,
    ReflectionData,
)
from sentinel.llm.provider import LLMProvider

logger = structlog.get_logger(__name__)


class AgenticLoop:
    """
    The main agentic loop orchestrator.
    
    Implements the 6-phase cycle:
    1. Perception - Capture system state
    2. Context - Process and understand
    3. Planning - Define actions
    4. Execution - Implement actions
    5. Reflection - Analyze results
    6. Memory - Store learnings
    
    This loop runs continuously and drives all agent behavior.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        perception: Optional[PerceptionModule] = None,
        context: Optional[ContextModule] = None,
        planning: Optional[PlanningModule] = None,
        execution: Optional[ExecutionModule] = None,
        reflection: Optional[ReflectionModule] = None,
        memory: Optional[MemoryModule] = None,
    ):
        self.llm_provider = llm_provider
        self.perception = perception
        self.context = context
        self.planning = planning
        self.execution = execution
        self.reflection = reflection
        self.memory = memory

        self.logger = structlog.get_logger("sentinel.loop")
        self.is_running = False
        self.iteration_count = 0

    async def initialize(self) -> None:
        """Initialize all modules"""
        self.logger.info("Initializing agentic loop")

        modules = [
            self.perception,
            self.context,
            self.planning,
            self.execution,
            self.reflection,
            self.memory,
        ]

        for module in modules:
            if module:
                await module.initialize()

        self.logger.info("Agentic loop initialized")

    async def cleanup(self) -> None:
        """Cleanup all modules"""
        self.logger.info("Cleaning up agentic loop")

        modules = [
            self.perception,
            self.context,
            self.planning,
            self.execution,
            self.reflection,
            self.memory,
        ]

        for module in modules:
            if module:
                await module.cleanup()

        self.logger.info("Agentic loop cleaned up")

    async def _phase_perception(self) -> Optional[PerceptionData]:
        """Phase 1: Perception"""
        if not self.perception:
            return None

        try:
            self.logger.info("Phase 1: PERCEPTION", iteration=self.iteration_count)
            result = await self.perception.process()
            self.logger.info(
                "Perception phase complete",
                iteration=self.iteration_count,
                active_window=result.active_window,
            )
            return result
        except Exception as e:
            self.logger.error(
                "Perception phase failed", iteration=self.iteration_count, error=str(e)
            )
            return None

    async def _phase_context(self, perception: PerceptionData) -> Optional[ContextData]:
        """Phase 2: Context"""
        if not self.context:
            return None

        try:
            self.logger.info("Phase 2: CONTEXT", iteration=self.iteration_count)
            result = await self.context.process(perception)
            self.logger.info(
                "Context phase complete",
                iteration=self.iteration_count,
                user_intent=result.user_intent,
            )
            return result
        except Exception as e:
            self.logger.error(
                "Context phase failed", iteration=self.iteration_count, error=str(e)
            )
            return None

    async def _phase_planning(self, context: ContextData) -> Optional[PlanData]:
        """Phase 3: Planning"""
        if not self.planning:
            return None

        try:
            self.logger.info("Phase 3: PLANNING", iteration=self.iteration_count)
            result = await self.planning.process(context)
            self.logger.info(
                "Planning phase complete",
                iteration=self.iteration_count,
                goal=result.goal,
                num_steps=len(result.steps),
            )
            return result
        except Exception as e:
            self.logger.error(
                "Planning phase failed", iteration=self.iteration_count, error=str(e)
            )
            return None

    async def _phase_execution(self, plan: PlanData) -> Optional[ExecutionResult]:
        """Phase 4: Execution"""
        if not self.execution:
            return None

        try:
            self.logger.info("Phase 4: EXECUTION", iteration=self.iteration_count)
            result = await self.execution.process(plan)
            self.logger.info(
                "Execution phase complete",
                iteration=self.iteration_count,
                success=result.success,
            )
            return result
        except Exception as e:
            self.logger.error(
                "Execution phase failed", iteration=self.iteration_count, error=str(e)
            )
            return None

    async def _phase_reflection(self, execution: ExecutionResult) -> Optional[ReflectionData]:
        """Phase 5: Reflection"""
        if not self.reflection:
            return None

        try:
            self.logger.info("Phase 5: REFLECTION", iteration=self.iteration_count)
            result = await self.reflection.process(execution)
            self.logger.info(
                "Reflection phase complete",
                iteration=self.iteration_count,
                lessons=len(result.lessons_learned),
            )
            return result
        except Exception as e:
            self.logger.error(
                "Reflection phase failed", iteration=self.iteration_count, error=str(e)
            )
            return None

    async def _phase_memory(self, reflection: ReflectionData) -> None:
        """Phase 6: Memory"""
        if not self.memory:
            return

        try:
            self.logger.info("Phase 6: MEMORY", iteration=self.iteration_count)
            await self.memory.process(reflection)
            self.logger.info("Memory phase complete", iteration=self.iteration_count)
        except Exception as e:
            self.logger.error(
                "Memory phase failed", iteration=self.iteration_count, error=str(e)
            )

    async def run_iteration(self) -> Dict[str, Any]:
        """Run a single iteration of the agentic loop"""
        iteration_start = datetime.now()
        self.iteration_count += 1

        self.logger.info(
            "Starting iteration",
            iteration=self.iteration_count,
            timestamp=iteration_start.isoformat(),
        )

        # Phase 1: Perception
        perception = await self._phase_perception()
        if not perception:
            return {"success": False, "error": "Perception failed"}

        # Phase 2: Context
        context = await self._phase_context(perception)
        if not context:
            return {"success": False, "error": "Context failed"}

        # Phase 3: Planning
        plan = await self._phase_planning(context)
        if not plan:
            return {"success": False, "error": "Planning failed"}

        # Phase 4: Execution
        execution = await self._phase_execution(plan)
        if not execution:
            return {"success": False, "error": "Execution failed"}

        # Phase 5: Reflection
        reflection = await self._phase_reflection(execution)
        if not reflection:
            return {"success": False, "error": "Reflection failed"}

        # Phase 6: Memory
        await self._phase_memory(reflection)

        iteration_end = datetime.now()
        duration = (iteration_end - iteration_start).total_seconds()

        self.logger.info(
            "Iteration complete",
            iteration=self.iteration_count,
            duration_seconds=duration,
            execution_success=execution.success,
        )

        return {
            "success": True,
            "iteration": self.iteration_count,
            "duration": duration,
            "execution_success": execution.success,
        }

    async def run(self, max_iterations: Optional[int] = None) -> None:
        """
        Run the agentic loop continuously.
        
        Args:
            max_iterations: Maximum number of iterations. None for infinite.
        """
        await self.initialize()
        self.is_running = True

        try:
            iteration = 0
            while self.is_running:
                if max_iterations and iteration >= max_iterations:
                    break

                await self.run_iteration()
                iteration += 1

                # Small delay between iterations to prevent CPU spinning
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            self.logger.info("Loop interrupted by user")
        except Exception as e:
            self.logger.error("Agentic loop error", error=str(e), exc_info=True)
        finally:
            await self.cleanup()
            self.is_running = False

    def stop(self) -> None:
        """Stop the agentic loop"""
        self.is_running = False
        self.logger.info("Stop requested")
