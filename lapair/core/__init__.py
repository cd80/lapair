"""
Core components of the LaPair framework.

This package contains the fundamental building blocks of the IR system:
- IR representation (basic blocks, instructions, functions, modules)
- Type system
- Symbol table
"""

from lapair.core.ir import (
    Location,
    Value,
    Instruction,
    BasicBlock,
    Function,
    Module,
    IR,
)
from lapair.core.types import (
    Type,
    VoidType,
    IntegerType,
    FloatType,
    PointerType,
    ArrayType,
    StructType,
    FunctionType,
    TypeSystem,
)
from lapair.core.symbol import (
    Symbol,
    Scope,
    SymbolTable,
)

__all__ = [
    # IR components
    'Location',
    'Value',
    'Instruction',
    'BasicBlock',
    'Function',
    'Module',
    'IR',
    
    # Type system
    'Type',
    'VoidType',
    'IntegerType',
    'FloatType',
    'PointerType',
    'ArrayType',
    'StructType',
    'FunctionType',
    'TypeSystem',
    
    # Symbol table
    'Symbol',
    'Scope',
    'SymbolTable',
]
