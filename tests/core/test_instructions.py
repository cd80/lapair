"""Tests for IR instructions."""

import pytest
from lapair.core.ir import IR, Value, BasicBlock, Function, Module
from lapair.core.types import TypeSystem, IntegerType, PointerType
from lapair.core.instructions import (
    InstructionKind,
    ComparisonKind,
    BinaryInstruction,
    CompareInstruction,
    AllocaInstruction,
    LoadInstruction,
    StoreInstruction,
    GetElementPtrInstruction,
    BranchInstruction,
    ReturnInstruction,
    CallInstruction,
    PhiInstruction,
    SelectInstruction,
)

@pytest.fixture
def type_system():
    """Fixture providing a type system for tests."""
    return TypeSystem()

@pytest.fixture
def i32(type_system):
    """Fixture providing an i32 type for tests."""
    return type_system.get_type("i32")

@pytest.fixture
def i64(type_system):
    """Fixture providing an i64 type for tests."""
    return type_system.get_type("i64")

@pytest.fixture
def basic_block():
    """Fixture providing a basic block for tests."""
    return BasicBlock(name="test_block")

def test_binary_instruction(i32):
    """Test binary instruction creation and properties."""
    left = Value(type=i32, name="left")
    right = Value(type=i32, name="right")
    
    inst = BinaryInstruction(
        type=i32,
        name="add",
        kind=InstructionKind.ADD,
        left=left,
        right=right
    )
    
    assert inst.kind == InstructionKind.ADD
    assert inst.type == i32
    assert len(inst.operands) == 2
    assert inst.operands[0] == left
    assert inst.operands[1] == right

def test_compare_instruction(i32):
    """Test compare instruction creation and properties."""
    left = Value(type=i32, name="left")
    right = Value(type=i32, name="right")
    
    inst = CompareInstruction(
        type=i32,
        name="cmp",
        kind=InstructionKind.ICMP,
        comparison=ComparisonKind.EQ,
        left=left,
        right=right
    )
    
    assert inst.kind == InstructionKind.ICMP
    assert inst.comparison == ComparisonKind.EQ
    assert len(inst.operands) == 2
    assert inst.operands[0] == left
    assert inst.operands[1] == right

def test_alloca_instruction(i32):
    """Test alloca instruction creation and properties."""
    size = Value(type=i32, name="size")
    ptr_type = PointerType(pointee_type=i32)
    
    # Test without array size
    inst = AllocaInstruction(
        type=ptr_type,
        name="alloc",
        allocated_type=i32
    )
    assert inst.allocated_type == i32
    assert inst.array_size is None
    assert len(inst.operands) == 0
    
    # Test with array size
    inst = AllocaInstruction(
        type=ptr_type,
        name="alloc_array",
        allocated_type=i32,
        array_size=size
    )
    assert inst.allocated_type == i32
    assert inst.array_size == size
    assert len(inst.operands) == 1
    assert inst.operands[0] == size

def test_load_instruction(i32):
    """Test load instruction creation and properties."""
    ptr = Value(type=PointerType(pointee_type=i32), name="ptr")
    
    inst = LoadInstruction(
        type=i32,
        name="load",
        pointer=ptr
    )
    
    assert inst.pointer == ptr
    assert len(inst.operands) == 1
    assert inst.operands[0] == ptr

def test_store_instruction(i32):
    """Test store instruction creation and properties."""
    value = Value(type=i32, name="value")
    ptr = Value(type=PointerType(pointee_type=i32), name="ptr")
    
    inst = StoreInstruction(
        type=i32,
        name="store",
        value=value,
        pointer=ptr
    )
    
    assert inst.value == value
    assert inst.pointer == ptr
    assert len(inst.operands) == 2
    assert inst.operands[0] == value
    assert inst.operands[1] == ptr

def test_gep_instruction(i32):
    """Test GEP instruction creation and properties."""
    ptr = Value(type=PointerType(pointee_type=i32), name="ptr")
    index1 = Value(type=i32, name="index1")
    index2 = Value(type=i32, name="index2")
    
    inst = GetElementPtrInstruction(
        type=PointerType(pointee_type=i32),
        name="gep",
        pointer=ptr,
        indices=[index1, index2]
    )
    
    assert inst.pointer == ptr
    assert len(inst.indices) == 2
    assert inst.indices[0] == index1
    assert inst.indices[1] == index2
    assert len(inst.operands) == 3
    assert inst.operands[0] == ptr
    assert inst.operands[1] == index1
    assert inst.operands[2] == index2

def test_branch_instruction(i32, basic_block):
    """Test branch instruction creation and properties."""
    cond = Value(type=i32, name="cond")
    true_block = BasicBlock(name="true")
    false_block = BasicBlock(name="false")
    
    # Test conditional branch
    inst = BranchInstruction(
        type=i32,
        name="br",
        condition=cond,
        true_block=true_block,
        false_block=false_block
    )
    
    assert inst.condition == cond
    assert inst.true_block == true_block
    assert inst.false_block == false_block
    assert len(inst.operands) == 1
    assert inst.operands[0] == cond
    
    # Test unconditional branch
    inst = BranchInstruction(
        type=i32,
        name="br",
        true_block=true_block
    )
    
    assert inst.condition is None
    assert inst.true_block == true_block
    assert inst.false_block is None
    assert len(inst.operands) == 0

def test_return_instruction(i32):
    """Test return instruction creation and properties."""
    value = Value(type=i32, name="value")
    
    # Test return with value
    inst = ReturnInstruction(
        type=i32,
        name="ret",
        value=value
    )
    
    assert inst.value == value
    assert len(inst.operands) == 1
    assert inst.operands[0] == value
    
    # Test void return
    inst = ReturnInstruction(
        type=i32,
        name="ret"
    )
    
    assert inst.value is None
    assert len(inst.operands) == 0

def test_call_instruction(i32):
    """Test call instruction creation and properties."""
    func = Value(type=i32, name="func")
    arg1 = Value(type=i32, name="arg1")
    arg2 = Value(type=i32, name="arg2")
    
    inst = CallInstruction(
        type=i32,
        name="call",
        function=func,
        arguments=[arg1, arg2]
    )
    
    assert inst.function == func
    assert len(inst.arguments) == 2
    assert inst.arguments[0] == arg1
    assert inst.arguments[1] == arg2
    assert len(inst.operands) == 3
    assert inst.operands[0] == func
    assert inst.operands[1] == arg1
    assert inst.operands[2] == arg2

def test_phi_instruction(i32):
    """Test phi instruction creation and properties."""
    block1 = BasicBlock(name="block1")
    block2 = BasicBlock(name="block2")
    value1 = Value(type=i32, name="value1")
    value2 = Value(type=i32, name="value2")
    
    # Create dictionary with proper syntax
    incoming_values = {
        block1: value1,
        block2: value2
    }
    
    inst = PhiInstruction(
        type=i32,
        name="phi",
        incoming_values=incoming_values
    )
    
    # Print debug information
    print(f"\nIncoming values: {list(incoming_values.items())}")
    print(f"Instruction incoming values: {list(inst.incoming_values.items())}")
    print(f"Instruction operands: {inst.operands}")
    print(f"len(inst.incoming_values): {len(inst.incoming_values)}")
    print(f"len(inst.operands): {len(inst.operands)}")
    
    assert len(inst.incoming_values) == 2
    assert inst.incoming_values[block1] == value1
    assert inst.incoming_values[block2] == value2
    assert len(inst.operands) == 2
    assert value1 in inst.operands
    assert value2 in inst.operands

def test_select_instruction(i32):
    """Test select instruction creation and properties."""
    cond = Value(type=i32, name="cond")
    true_val = Value(type=i32, name="true_val")
    false_val = Value(type=i32, name="false_val")
    
    inst = SelectInstruction(
        type=i32,
        name="select",
        condition=cond,
        true_value=true_val,
        false_value=false_val
    )
    
    assert inst.condition == cond
    assert inst.true_value == true_val
    assert inst.false_value == false_val
    assert len(inst.operands) == 3
    assert inst.operands[0] == cond
    assert inst.operands[1] == true_val
    assert inst.operands[2] == false_val
