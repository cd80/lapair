"""
IR instruction definitions for the LaPair framework.

This module defines the concrete instruction types that can appear in the IR,
including arithmetic operations, control flow, memory operations, and more.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Set, Dict
import attr

from lapair.core.ir import Instruction, Value, BasicBlock
from lapair.core.types import Type, IntegerType, PointerType

class InstructionKind(Enum):
    """Kinds of IR instructions."""
    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    REM = auto()
    
    # Bitwise
    AND = auto()
    OR = auto()
    XOR = auto()
    SHL = auto()
    SHR = auto()
    
    # Memory
    ALLOCA = auto()
    LOAD = auto()
    STORE = auto()
    GEP = auto()  # Get Element Pointer
    
    # Control Flow
    BR = auto()      # Branch
    SWITCH = auto()
    RET = auto()     # Return
    CALL = auto()
    PHI = auto()
    
    # Comparison
    ICMP = auto()  # Integer comparison
    FCMP = auto()  # Float comparison
    
    # Conversion
    TRUNC = auto()    # Truncate
    ZEXT = auto()     # Zero extend
    SEXT = auto()     # Sign extend
    FPTRUNC = auto()  # Floating-point truncate
    FPEXT = auto()    # Floating-point extend
    BITCAST = auto()  # Bit pattern cast
    
    # Other
    SELECT = auto()   # Conditional select
    FREEZE = auto()   # Freeze value for optimization

class ComparisonKind(Enum):
    """Kinds of comparison operations."""
    # Integer comparisons
    EQ = auto()   # Equal
    NE = auto()   # Not equal
    LT = auto()   # Less than
    LE = auto()   # Less than or equal
    GT = auto()   # Greater than
    GE = auto()   # Greater than or equal
    
    # Float comparisons
    OEQ = auto()  # Ordered and equal
    ONE = auto()  # Ordered and not equal
    OLT = auto()  # Ordered and less than
    OLE = auto()  # Ordered and less than or equal
    OGT = auto()  # Ordered and greater than
    OGE = auto()  # Ordered and greater than or equal
    
    UEQ = auto()  # Unordered or equal
    UNE = auto()  # Unordered or not equal
    ULT = auto()  # Unordered or less than
    ULE = auto()  # Unordered or less than or equal
    UGT = auto()  # Unordered or greater than
    UGE = auto()  # Unordered or greater than or equal

@attr.s(kw_only=True, eq=False)
class BinaryInstruction(Instruction):
    """Base class for binary operations."""
    kind: InstructionKind = attr.ib()
    left: Value = attr.ib()
    right: Value = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.left)
        self.add_operand(self.right)

@attr.s(kw_only=True, eq=False)
class CompareInstruction(Instruction):
    """Base class for comparison operations."""
    kind: InstructionKind = attr.ib()
    comparison: ComparisonKind = attr.ib()
    left: Value = attr.ib()
    right: Value = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.left)
        self.add_operand(self.right)

@attr.s(kw_only=True, eq=False)
class AllocaInstruction(Instruction):
    """Allocate memory on the stack."""
    allocated_type: Type = attr.ib()
    array_size: Optional[Value] = attr.ib(default=None)

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        if self.array_size is not None:
            self.add_operand(self.array_size)

@attr.s(kw_only=True, eq=False)
class LoadInstruction(Instruction):
    """Load a value from memory."""
    pointer: Value = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.pointer)

@attr.s(kw_only=True, eq=False)
class StoreInstruction(Instruction):
    """Store a value to memory."""
    value: Value = attr.ib()
    pointer: Value = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.value)
        self.add_operand(self.pointer)

@attr.s(kw_only=True, eq=False)
class GetElementPtrInstruction(Instruction):
    """Get the address of a subelement of an aggregate data structure."""
    pointer: Value = attr.ib()
    indices: List[Value] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.pointer)
        for index in self.indices:
            self.add_operand(index)

@attr.s(kw_only=True, eq=False)
class BranchInstruction(Instruction):
    """Branch instruction for control flow."""
    true_block: BasicBlock = attr.ib()
    condition: Optional[Value] = attr.ib(default=None)
    false_block: Optional[BasicBlock] = attr.ib(default=None)

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        if self.condition is not None:
            self.add_operand(self.condition)

@attr.s(kw_only=True, eq=False)
class ReturnInstruction(Instruction):
    """Return instruction."""
    value: Optional[Value] = attr.ib(default=None)

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        if self.value is not None:
            self.add_operand(self.value)

@attr.s(kw_only=True, eq=False)
class CallInstruction(Instruction):
    """Function call instruction."""
    function: Value = attr.ib()
    arguments: List[Value] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.function)
        for arg in self.arguments:
            self.add_operand(arg)

@attr.s(kw_only=True, eq=False)
class PhiInstruction(Instruction):
    """Phi instruction for SSA form."""
    incoming_values: Dict[BasicBlock, Value] = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        for value in self.incoming_values.values():
            self.add_operand(value)

@attr.s(kw_only=True, eq=False)
class SelectInstruction(Instruction):
    """Select between two values based on a condition."""
    condition: Value = attr.ib()
    true_value: Value = attr.ib()
    false_value: Value = attr.ib()

    def __attrs_post_init__(self):
        """Initialize the instruction."""
        self.add_operand(self.condition)
        self.add_operand(self.true_value)
        self.add_operand(self.false_value)
