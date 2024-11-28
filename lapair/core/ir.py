"""
Core IR components for the LaPair framework.

This module defines the fundamental building blocks of the IR system, including
basic blocks, instructions, functions, and modules.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, TypeVar
import attr

from lapair.core.types import Type, TypeSystem
from lapair.core.symbol import SymbolTable

T = TypeVar('T')


@attr.s(auto_attribs=True, frozen=True)
class Location:
    """Source code location information."""
    file: str
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None


@attr.s(auto_attribs=True)
class Value:
    """Base class for all IR values."""
    type: Type
    name: Optional[str] = None
    location: Optional[Location] = None


@attr.s(auto_attribs=True, eq=False)
class Instruction(Value):
    """Base class for IR instructions."""
    operands: List[Value] = attr.Factory(list)
    users: Set['Instruction'] = attr.Factory(set)
    parent: Optional['BasicBlock'] = attr.ib(default=None, repr=False)

    def __eq__(self, other: object) -> bool:
        """Check equality based on object identity."""
        return self is other

    def __hash__(self) -> int:
        """Hash based on object identity."""
        return id(self)

    def add_operand(self, operand: Value) -> None:
        """Add an operand to this instruction."""
        self.operands.append(operand)
        if isinstance(operand, Instruction):
            operand.users.add(self)

    def remove_operand(self, operand: Value) -> None:
        """Remove an operand from this instruction."""
        self.operands.remove(operand)
        if isinstance(operand, Instruction):
            operand.users.remove(self)


@attr.s(auto_attribs=True, eq=False)
class BasicBlock:
    """Container for IR instructions with control flow information."""
    name: str
    instructions: List[Instruction] = attr.Factory(list)
    predecessors: Set['BasicBlock'] = attr.Factory(set)
    successors: Set['BasicBlock'] = attr.Factory(set)
    parent: Optional['Function'] = attr.ib(default=None, repr=False)

    def __eq__(self, other: object) -> bool:
        """Check equality based on object identity."""
        return self is other

    def __hash__(self) -> int:
        """Hash based on object identity."""
        return id(self)

    def add_instruction(self, instruction: Instruction) -> None:
        """Add an instruction to this basic block."""
        instruction.parent = self
        self.instructions.append(instruction)

    def add_predecessor(self, block: 'BasicBlock') -> None:
        """Add a predecessor basic block."""
        self.predecessors.add(block)
        block.successors.add(self)

    def remove_predecessor(self, block: 'BasicBlock') -> None:
        """Remove a predecessor basic block."""
        self.predecessors.remove(block)
        block.successors.remove(self)


@attr.s(auto_attribs=True)
class Function:
    """IR representation of a function."""
    name: str
    return_type: Type
    parameters: List[Value]
    blocks: List[BasicBlock] = attr.Factory(list)
    symbol_table: SymbolTable = attr.Factory(SymbolTable)
    parent: Optional['Module'] = attr.ib(default=None, repr=False)

    def add_block(self, block: BasicBlock) -> None:
        """Add a basic block to this function."""
        block.parent = self
        self.blocks.append(block)


@attr.s(auto_attribs=True)
class Module:
    """Top-level container for IR components."""
    name: str
    functions: Dict[str, Function] = attr.Factory(dict)
    symbol_table: SymbolTable = attr.Factory(SymbolTable)
    type_system: TypeSystem = attr.Factory(TypeSystem)

    def add_function(self, function: Function) -> None:
        """Add a function to this module."""
        function.parent = self
        self.functions[function.name] = function


class IR:
    """Main interface for working with the IR."""
    def __init__(self) -> None:
        self.modules: Dict[str, Module] = {}
        self.global_symbol_table = SymbolTable()
        self.type_system = TypeSystem()

    def create_module(self, name: str) -> Module:
        """Create a new module."""
        module = Module(name=name, type_system=self.type_system)
        self.modules[name] = module
        return module

    def get_module(self, name: str) -> Optional[Module]:
        """Get a module by name."""
        return self.modules.get(name)
