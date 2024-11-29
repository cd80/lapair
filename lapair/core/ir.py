"""
Core IR definitions for the LaPair framework.

This module defines the core Intermediate Representation structures, including
Instructions, Values, BasicBlocks, Functions, Modules, Constants, and Location.
"""

from __future__ import annotations

from typing import List, Optional, Set, Dict, Any
import attr

from lapair.core.types import Type, TypeSystem


@attr.s(auto_attribs=True, eq=False)
class Location:
    """Represents source code location information."""
    file: str
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None


@attr.s(auto_attribs=True, eq=False)
class Value:
    """Base class for all IR values."""
    type: Type
    name: Optional[str] = None
    location: Optional[Location] = None
    users: Set[Instruction] = attr.Factory(set)

    def add_user(self, instr: Instruction):
        """Add an instruction that uses this value."""
        self.users.add(instr)


@attr.s(auto_attribs=True, eq=False)
class Constant(Value):
    """Represents an immutable constant value in the IR."""
    value: Any = None


@attr.s(auto_attribs=True, eq=False)
class Instruction(Value):
    """Base class for all IR instructions."""
    operands: List[Value] = attr.Factory(list)
    parent: Optional[BasicBlock] = None  # Reference to the containing basic block

    def add_operand(self, value: Value):
        """Add an operand to the instruction."""
        self.operands.append(value)
        value.add_user(self)

    def replace_operand(self, old_value: Value, new_value: Value):
        """Replace an operand with a new value."""
        for idx, operand in enumerate(self.operands):
            if operand is old_value:
                self.operands[idx] = new_value
                old_value.users.discard(self)
                new_value.add_user(self)

    def remove_operand(self, value: Value):
        """Remove an operand from the instruction."""
        self.operands.remove(value)
        value.users.discard(self)


@attr.s(auto_attribs=True, eq=False)
class BasicBlock:
    """Represents a basic block in the IR."""
    name: str
    instructions: List[Instruction] = attr.Factory(list)
    predecessors: Set[BasicBlock] = attr.Factory(set)
    successors: Set[BasicBlock] = attr.Factory(set)
    parent: Optional[Function] = None  # Reference to the containing function

    def add_instruction(self, instr: Instruction):
        """Add an instruction to the basic block."""
        instr.parent = self
        self.instructions.append(instr)

    def add_predecessor(self, pred: BasicBlock):
        """Add a predecessor to the basic block."""
        self.predecessors.add(pred)
        pred.successors.add(self)

    def add_successor(self, succ: BasicBlock):
        """Add a successor to the basic block."""
        self.successors.add(succ)
        succ.predecessors.add(self)

    def remove_predecessor(self, pred: BasicBlock):
        """Remove a predecessor from the basic block."""
        self.predecessors.discard(pred)
        pred.successors.discard(self)

    def remove_successor(self, succ: BasicBlock):
        """Remove a successor from the basic block."""
        self.successors.discard(succ)
        succ.predecessors.discard(self)


@attr.s(auto_attribs=True, eq=False)
class Function:
    """Represents a function in the IR."""
    name: str
    return_type: Type
    parameters: List[Value]
    blocks: List[BasicBlock] = attr.Factory(list)
    symbol_table: Dict[str, Value] = attr.Factory(dict)
    parent: Optional[Module] = None  # Reference to the containing module

    def add_block(self, block: BasicBlock):
        """Add a basic block to the function."""
        block.parent = self
        self.blocks.append(block)

    def add_parameter(self, param: Value):
        """Add a parameter to the function."""
        self.parameters.append(param)
        if param.name:
            self.symbol_table[param.name] = param

    def get_block(self, name: str) -> Optional[BasicBlock]:
        """Retrieve a basic block by name."""
        for block in self.blocks:
            if block.name == name:
                return block
        return None


@attr.s(auto_attribs=True, eq=False)
class Module:
    """Represents a module in the IR, containing functions and global variables."""
    name: str
    functions: Dict[str, Function] = attr.Factory(dict)
    global_variables: Dict[str, Value] = attr.Factory(dict)
    symbol_table: Dict[str, Value] = attr.Factory(dict)
    type_system: TypeSystem = attr.Factory(TypeSystem)
    parent: Optional[IR] = None  # Reference to the IR

    def add_function(self, function: Function):
        """Add a function to the module."""
        function.parent = self
        self.functions[function.name] = function

    def add_global(self, var: Value):
        """Add a global variable to the module."""
        if var.name:
            self.global_variables[var.name] = var
            self.symbol_table[var.name] = var

    def get_function(self, name: str) -> Optional[Function]:
        """Retrieve a function by name."""
        return self.functions.get(name)

    def get_global(self, name: str) -> Optional[Value]:
        """Retrieve a global variable by name."""
        return self.global_variables.get(name)


@attr.s(auto_attribs=True, eq=False)
class IR:
    """Represents the overall IR, containing one or more modules."""
    modules: Dict[str, Module] = attr.Factory(dict)
    global_symbol_table: Dict[str, Value] = attr.Factory(dict)
    type_system: TypeSystem = attr.Factory(TypeSystem)

    def add_module(self, module: Module):
        """Add a module to the IR."""
        module.parent = self
        self.modules[module.name] = module

    def get_module(self, name: str) -> Optional[Module]:
        """Retrieve a module by name."""
        return self.modules.get(name)

    def create_module(self, name: str) -> Module:
        """Create and add a new module to the IR."""
        module = Module(name=name)
        self.add_module(module)
        return module
