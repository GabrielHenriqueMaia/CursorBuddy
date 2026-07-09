"""Placeholder for Planning module implementation"""

from sentinel.core.base import PlanningModule
from sentinel.core.types import ContextData, PlanData


class LLMPlanningModule(PlanningModule):
    """
    Planning implementation using LLM.
    
    Responsibilities:
    - Define goals based on context
    - Generate action plans
    - Break down complex tasks
    - Assign confidence scores
    """

    async def process(self, context: ContextData) -> PlanData:
        """Create action plan from context"""
        # TODO: Implement planning
        # - Send context to LLM for planning
        # - Break down goal into steps
        # - Assign confidence scores
        # - Generate alternatives
        pass
