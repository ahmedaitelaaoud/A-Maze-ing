"""
Utility module for the A-Maze-ing project.

Contains configuration parsing and validation functions safely exposed
for the main orchestrator.
"""

from .config import parse_config, validate_config

__all__ = ["parse_config", "validate_config"]
