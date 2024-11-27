"""Tests for the symbol table implementation."""

import pytest
from lapair.core.symbol import Symbol, Scope, SymbolTable
from lapair.core.types import TypeSystem, IntegerType, VoidType

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

def test_symbol_creation(i32):
    """Test symbol creation and properties."""
    symbol = Symbol(name="x", type=i32)
    assert symbol.name == "x"
    assert symbol.type == i32
    assert not symbol.is_global
    assert not symbol.is_constant
    assert not symbol.is_defined
    assert symbol.scope is None

def test_scope_creation():
    """Test scope creation and properties."""
    scope = Scope(name="test_scope")
    assert scope.name == "test_scope"
    assert scope.parent is None
    assert len(scope.children) == 0
    assert len(scope.symbols) == 0

def test_scope_symbol_management(i32):
    """Test adding and looking up symbols in a scope."""
    scope = Scope(name="test_scope")
    symbol = Symbol(name="x", type=i32, scope=scope)

    assert scope.symbols["x"] == symbol
    assert scope.lookup_symbol("x") == symbol
    assert scope.lookup_symbol("nonexistent") is None

def test_scope_hierarchy(i32):
    """Test scope hierarchy and symbol lookup."""
    parent_scope = Scope(name="parent")
    child_scope = Scope(name="child", parent=parent_scope)
    parent_scope.children.append(child_scope)

    # Add symbols to both scopes
    parent_symbol = Symbol(name="parent_var", type=i32, scope=parent_scope)
    child_symbol = Symbol(name="child_var", type=i32, scope=child_scope)

    # Test lookup from child scope
    assert child_scope.lookup_symbol("child_var") == child_symbol
    assert child_scope.lookup_symbol("parent_var") == parent_symbol
    assert child_scope.lookup_symbol("parent_var", recursive=False) is None

    # Test lookup from parent scope
    assert parent_scope.lookup_symbol("parent_var") == parent_symbol
    assert parent_scope.lookup_symbol("child_var") is None

def test_symbol_table_basic(i32):
    """Test basic symbol table functionality."""
    symtab = SymbolTable()
    
    # Add symbol to global scope
    symbol = symtab.add_symbol("x", i32)
    assert symtab.lookup_symbol("x") == symbol
    assert symbol.scope == symtab.global_scope

def test_symbol_table_scoping(i32):
    """Test symbol table scoping functionality."""
    symtab = SymbolTable()
    
    # Add symbol to global scope
    global_symbol = symtab.add_symbol("x", i32, is_global=True)
    
    # Enter new scope
    symtab.enter_scope("function")
    local_symbol = symtab.add_symbol("x", i32)  # Shadows global x
    
    # Test lookup in current scope
    assert symtab.lookup_symbol("x") == local_symbol
    assert symtab.lookup_symbol("x", current_scope_only=True) == local_symbol
    
    # Exit scope
    symtab.exit_scope()
    assert symtab.lookup_symbol("x") == global_symbol

def test_symbol_table_nested_scopes(i32):
    """Test nested scoping in symbol table."""
    symtab = SymbolTable()
    
    # Global scope
    global_x = symtab.add_symbol("x", i32, is_global=True)
    
    # Function scope
    symtab.enter_scope("function")
    func_x = symtab.add_symbol("x", i32)
    func_y = symtab.add_symbol("y", i32)
    
    # Block scope
    symtab.enter_scope("block")
    block_x = symtab.add_symbol("x", i32)
    block_z = symtab.add_symbol("z", i32)
    
    # Test lookup from block scope
    assert symtab.lookup_symbol("x") == block_x
    assert symtab.lookup_symbol("y") == func_y
    assert symtab.lookup_symbol("z") == block_z
    
    # Exit block scope
    symtab.exit_scope()
    assert symtab.lookup_symbol("x") == func_x
    assert symtab.lookup_symbol("y") == func_y
    assert symtab.lookup_symbol("z") is None
    
    # Exit function scope
    symtab.exit_scope()
    assert symtab.lookup_symbol("x") == global_x
    assert symtab.lookup_symbol("y") is None

def test_symbol_table_get_scope_symbols(i32):
    """Test getting all symbols in current scope."""
    symtab = SymbolTable()
    
    # Global scope symbols
    global_x = symtab.add_symbol("x", i32, is_global=True)
    global_y = symtab.add_symbol("y", i32, is_global=True)
    
    # Function scope
    symtab.enter_scope("function")
    func_z = symtab.add_symbol("z", i32)
    
    # Test getting symbols
    current_scope_symbols = symtab.get_scope_symbols()
    assert len(current_scope_symbols) == 1
    assert current_scope_symbols["z"] == func_z
    
    # Test getting symbols including parent scopes
    all_symbols = symtab.get_scope_symbols(include_parent_scopes=True)
    assert len(all_symbols) == 3
    assert all_symbols["x"] == global_x
    assert all_symbols["y"] == global_y
    assert all_symbols["z"] == func_z

def test_symbol_table_get_global_symbols(i32):
    """Test getting global symbols."""
    symtab = SymbolTable()
    
    # Add global and non-global symbols
    global_x = symtab.add_symbol("x", i32, is_global=True)
    global_y = symtab.add_symbol("y", i32, is_global=True)
    non_global = symtab.add_symbol("z", i32, is_global=False)
    
    globals = symtab.get_global_symbols()
    assert len(globals) == 2
    assert globals["x"] == global_x
    assert globals["y"] == global_y
    assert "z" not in globals

def test_symbol_table_clear_and_reset(i32):
    """Test clearing and resetting symbol table."""
    symtab = SymbolTable()
    
    # Add some symbols
    symtab.add_symbol("x", i32)
    symtab.enter_scope("function")
    symtab.add_symbol("y", i32)
    
    # Clear current scope
    symtab.clear_scope()
    assert symtab.lookup_symbol("y", current_scope_only=True) is None
    assert symtab.lookup_symbol("x") is not None
    
    # Reset entire table
    symtab.reset()
    assert symtab.lookup_symbol("x") is None
    assert symtab.current_scope == symtab.global_scope
