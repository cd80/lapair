"""
LaPair - Language-agnostic Program Analysis IR Framework.

This package provides a robust and extensible Intermediate Representation (IR)
framework designed for comprehensive program analysis and vulnerability detection
across multiple programming languages.
"""

__version__ = "0.1.0"
__author__ = "cd80"

from typing import List, Optional, Dict, Any

# Core components
from lapair.core.ir import (
    IR,
    BasicBlock,
    Instruction,
    Function,
    Module,
)
from lapair.core.types import (
    Type,
    TypeSystem,
)
from lapair.core.symbol import (
    Symbol,
    SymbolTable,
)

__all__: List[str] = [
    "IR",
    "BasicBlock",
    "Instruction",
    "Function",
    "Module",
    "Type",
    "TypeSystem",
    "Symbol",
    "SymbolTable",
]
