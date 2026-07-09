"""
Project Sentinel - Modular Agentic Assistant for Windows

A desktop automation platform structured around a 6-phase loop:
  1. Perception - Capture system state
  2. Context - Process and understand
  3. Planning - Define actions
  4. Execution - Implement actions
  5. Reflection - Analyze results
  6. Memory - Store learnings

Designed for modularity, extensibility, and LLM-agnosticism.
"""

__version__ = "0.1.0"
__author__ = "Project Sentinel"

from sentinel.core.loop import AgenticLoop

__all__ = ["AgenticLoop"]
