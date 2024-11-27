"""Tests for the core IR components."""

import pytest
from lapair.core.ir import (
    Location,
    Value,
    Instruction,
    BasicBlock,
    Function,
    Module,
    IR,
)
from lapair.core.types import TypeSystem, IntegerType, VoidType
from lapair.core.symbol import SymbolTable

@pytest.fixture
def type_system():
    """Fixture providing a type system for tests."""
    return TypeSystem()

@pytest.fixture
def i32(type_system):
    """Fixture providing an i32 type for tests."""
    return type_system.get_type("i32")

@pytest.fixture
def void(type_system):
    """Fixture providing a void type for tests."""
    return type_system.get_type("void")

def test_location():
    """Test location creation and properties."""
    loc = Location(file="test.c", line=1, column=1, end_line=1, end_column=10)
    assert loc.file == "test.c"
    assert loc.line == 1
    assert loc.column == 1
    assert loc.end_line == 1
    assert loc.end_column == 10

def test_value(i32):
    """Test value creation and properties."""
    value = Value(type=i32, name="x")
    assert value.type == i32
    assert value.name == "x"
    assert value.location is None

def test_instruction(i32):
    """Test instruction creation and manipulation."""
    inst1 = Instruction(type=i32, name="result")
    inst2 = Instruction(type=i32, name="operand")
    
    # Test adding operand
    inst1.add_operand(inst2)
    assert inst2 in inst1.operands
    assert inst1 in inst2.users
    
    # Test removing operand
    inst1.remove_operand(inst2)
    assert inst2 not in inst1.operands
    assert inst1 not in inst2.users

def test_basic_block():
    """Test basic block creation and manipulation."""
    block = BasicBlock(name="entry")
    assert block.name == "entry"
    assert len(block.instructions) == 0
    assert len(block.predecessors) == 0
    assert len(block.successors) == 0

def test_basic_block_instruction_management(i32):
    """Test instruction management in basic blocks."""
    block = BasicBlock(name="entry")
    inst = Instruction(type=i32, name="x")
    
    # Test adding instruction
    block.add_instruction(inst)
    assert inst in block.instructions
    assert inst.parent == block
    
    # Test instruction order
    inst2 = Instruction(type=i32, name="y")
    block.add_instruction(inst2)
    assert block.instructions == [inst, inst2]

def test_basic_block_control_flow():
    """Test control flow between basic blocks."""
    block1 = BasicBlock(name="entry")
    block2 = BasicBlock(name="exit")
    
    # Test adding predecessor/successor
    block2.add_predecessor(block1)
    assert block1 in block2.predecessors
    assert block2 in block1.successors
    
    # Test removing predecessor/successor
    block2.remove_predecessor(block1)
    assert block1 not in block2.predecessors
    assert block2 not in block1.successors

def test_function(i32, void):
    """Test function creation and manipulation."""
    func = Function(
        name="test_func",
        return_type=void,
        parameters=[Value(type=i32, name="param1")]
    )
    
    assert func.name == "test_func"
    assert func.return_type == void
    assert len(func.parameters) == 1
    assert len(func.blocks) == 0

def test_function_block_management(i32, void):
    """Test basic block management in functions."""
    func = Function(
        name="test_func",
        return_type=void,
        parameters=[Value(type=i32, name="param1")]
    )
    
    block = BasicBlock(name="entry")
    func.add_block(block)
    
    assert block in func.blocks
    assert block.parent == func

def test_module():
    """Test module creation and manipulation."""
    module = Module(name="test_module")
    assert module.name == "test_module"
    assert len(module.functions) == 0
    assert module.symbol_table is not None
    assert module.type_system is not None

def test_module_function_management(i32, void):
    """Test function management in modules."""
    module = Module(name="test_module")
    func = Function(
        name="test_func",
        return_type=void,
        parameters=[Value(type=i32, name="param1")]
    )
    
    module.add_function(func)
    assert func.name in module.functions
    assert module.functions[func.name] == func
    assert func.parent == module

def test_ir():
    """Test IR creation and manipulation."""
    ir = IR()
    assert len(ir.modules) == 0
    assert ir.global_symbol_table is not None
    assert ir.type_system is not None

def test_ir_module_management():
    """Test module management in IR."""
    ir = IR()
    
    # Test creating module
    module = ir.create_module("test_module")
    assert module.name == "test_module"
    assert module in ir.modules.values()
    
    # Test getting module
    assert ir.get_module("test_module") == module
    assert ir.get_module("nonexistent") is None

def test_ir_integration(i32, void):
    """Test integration of all IR components."""
    ir = IR()
    
    # Create module
    module = ir.create_module("test_module")
    
    # Create function
    func = Function(
        name="test_func",
        return_type=void,
        parameters=[Value(type=i32, name="param1")]
    )
    module.add_function(func)
    
    # Create basic blocks
    entry_block = BasicBlock(name="entry")
    exit_block = BasicBlock(name="exit")
    func.add_block(entry_block)
    func.add_block(exit_block)
    
    # Create instructions
    inst1 = Instruction(type=i32, name="x")
    inst2 = Instruction(type=i32, name="y")
    entry_block.add_instruction(inst1)
    entry_block.add_instruction(inst2)
    
    # Set up control flow
    exit_block.add_predecessor(entry_block)
    
    # Verify structure
    assert module in ir.modules.values()
    assert func in module.functions.values()
    assert entry_block in func.blocks
    assert exit_block in func.blocks
    assert inst1 in entry_block.instructions
    assert inst2 in entry_block.instructions
    assert entry_block in exit_block.predecessors
    assert exit_block in entry_block.successors
