"""Base abstract classes for all modules in the agentic loop"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import structlog

from sentinel.core.types import (
    PerceptionData,
    ContextData,
    PlanData,
    ExecutionResult,
    ReflectionData,
    MemoryEntry,
)

logger = structlog.get_logger(__name__)


class SentinelModule(ABC):
    """Base class for all Sentinel modules"""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = structlog.get_logger(f"sentinel.{name}")

    @abstractmethod
    async def process(self, *args, **kwargs) -> Any:
        """Process input and return output"""
        pass

    async def initialize(self) -> None:
        """Initialize module resources"""
        self.logger.info("Initializing module", module=self.name)

    async def cleanup(self) -> None:
        """Cleanup module resources"""
        self.logger.info("Cleaning up module", module=self.name)


class PerceptionModule(SentinelModule):
    """
    Perception: Capture and raw state extraction
    
    Responsibilities:
    - Capture active window/application
    - Screenshot capture
    - OCR processing
    - UI element extraction
    - Cursor position tracking
    """

    async def process(self) -> PerceptionData:
        """Capture current system state and return perception data"""
        pass


class ContextModule(SentinelModule):
    """
    Context: Processing and understanding raw perception
    
    Responsibilities:
    - Analyze perception data
    - Infer user intent
    - Retrieve relevant memories
    - Build contextual understanding
    - Call LLM for analysis if needed
    """

    async def process(self, perception: PerceptionData) -> ContextData:
        """Process perception data into contextual understanding"""
        pass


class PlanningModule(SentinelModule):
    """
    Planning: Define actions and strategy
    
    Responsibilities:
    - Define goals based on context
    - Generate action plans
    - Break down complex tasks
    - Assign confidence scores
    - Generate alternatives
    """

    async def process(self, context: ContextData) -> PlanData:
        """Create action plan based on context"""
        pass


class ExecutionModule(SentinelModule):
    """
    Execution: Implement planned actions
    
    Responsibilities:
    - Execute planned steps
    - Handle errors and recovery
    - Capture side effects
    - Return execution results
    """

    async def process(self, plan: PlanData) -> ExecutionResult:
        """Execute the planned actions"""
        pass


class ReflectionModule(SentinelModule):
    """
    Reflection: Analyze execution results
    
    Responsibilities:
    - Analyze success/failure
    - Extract lessons learned
    - Identify anomalies
    - Make recommendations
    - Plan next steps
    """

    async def process(self, execution: ExecutionResult) -> ReflectionData:
        """Analyze execution results and generate reflections"""
        pass


class MemoryModule(SentinelModule):
    """
    Memory: Store and retrieve learnings
    
    Responsibilities:
    - Store memory entries
    - Retrieve relevant memories
    - Update relevance scores
    - Manage memory lifecycle
    - Search and query capabilities
    """

    async def store(self, entry: MemoryEntry) -> str:
        """Store a memory entry and return its ID"""
        pass

    async def retrieve(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memories matching a query"""
        pass

    async def process(self, reflection: ReflectionData) -> List[MemoryEntry]:
        """Convert reflection data into memory entries"""
        pass
