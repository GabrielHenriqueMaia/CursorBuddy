"""Type definitions for core data flowing through the agentic loop"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class ModuleType(str, Enum):
    """Types of modules in the sentinel architecture"""
    PERCEPTION = "perception"
    CONTEXT = "context"
    PLANNING = "planning"
    EXECUTION = "execution"
    REFLECTION = "reflection"
    MEMORY = "memory"


@dataclass
class PerceptionData:
    """Output from Perception module - raw system state capture"""
    timestamp: datetime = field(default_factory=datetime.now)
    active_window: Optional[str] = None
    active_application: Optional[str] = None
    screen_content: Optional[bytes] = None  # screenshot
    cursor_position: Optional[tuple[int, int]] = None
    ui_elements: List[Dict[str, Any]] = field(default_factory=list)
    ocr_text: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class ContextData:
    """Output from Context module - processed understanding"""
    perception: PerceptionData
    user_intent: Optional[str] = None
    contextual_information: Dict[str, Any] = field(default_factory=dict)
    relevant_memory: List['MemoryEntry'] = field(default_factory=list)
    analysis: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class PlanData:
    """Output from Planning module - action plan"""
    context: ContextData
    goal: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: Optional[str] = None
    confidence: float = 0.0  # 0.0 to 1.0
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class ExecutionResult:
    """Output from Execution module - action results"""
    plan: PlanData
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    executed_steps: List[Dict[str, Any]] = field(default_factory=list)
    side_effects: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class ReflectionData:
    """Output from Reflection module - analysis of execution"""
    execution: ExecutionResult
    success_analysis: str
    lessons_learned: List[str] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    next_steps: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class MemoryEntry:
    """A single entry in the memory system"""
    id: str
    timestamp: datetime = field(default_factory=datetime.now)
    category: str  # e.g., "workflow", "user_pattern", "success", "failure"
    content: Dict[str, Any] = field(default_factory=dict)
    relevance_score: float = 1.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
