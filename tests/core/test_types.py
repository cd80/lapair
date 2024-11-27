"""Tests for the type system implementation."""

import pytest
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

def test_void_type():
    """Test void type creation and properties."""
    void_type = VoidType()
    assert void_type.name == "void"
    assert void_type.size is None

def test_integer_type():
    """Test integer type creation and properties."""
    # Test signed integers
    i32 = IntegerType.create(32, signed=True)
    assert i32.name == "i32"
    assert i32.size == 32
    assert i32.signed is True

    # Test unsigned integers
    u64 = IntegerType.create(64, signed=False)
    assert u64.name == "u64"
    assert u64.size == 64
    assert u64.signed is False

def test_float_type():
    """Test float type creation and properties."""
    f32 = FloatType.create(32)
    assert f32.name == "f32"
    assert f32.size == 32

    f64 = FloatType.create(64)
    assert f64.name == "f64"
    assert f64.size == 64

def test_pointer_type():
    """Test pointer type creation and properties."""
    i32 = IntegerType.create(32, signed=True)
    ptr = PointerType(pointee_type=i32)
    assert ptr.name == "i32*"
    assert ptr.size == 64  # Assuming 64-bit architecture
    assert ptr.pointee_type == i32

def test_array_type():
    """Test array type creation and properties."""
    i32 = IntegerType.create(32, signed=True)
    
    # Fixed-length array
    fixed_array = ArrayType(element_type=i32, length=10)
    assert fixed_array.name == "i32[10]"
    assert fixed_array.size == 320  # 10 * 32 bits
    assert fixed_array.element_type == i32
    assert fixed_array.length == 10

    # Variable-length array
    var_array = ArrayType(element_type=i32)
    assert var_array.name == "i32[]"
    assert var_array.size is None
    assert var_array.element_type == i32
    assert var_array.length is None

def test_struct_type():
    """Test struct type creation and properties."""
    i32 = IntegerType.create(32, signed=True)
    f64 = FloatType.create(64)
    
    fields = {
        "x": i32,
        "y": f64,
    }
    
    struct = StructType(name="Point", fields=fields)
    assert struct.name == "Point"
    assert struct.size == 96  # 32 + 64 bits
    assert struct.fields == fields

def test_function_type():
    """Test function type creation and properties."""
    i32 = IntegerType.create(32, signed=True)
    void = VoidType()
    
    # Function with parameters
    func = FunctionType(return_type=i32, parameter_types=[i32, i32])
    assert func.name == "i32 (i32, i32)"
    assert func.return_type == i32
    assert func.parameter_types == [i32, i32]

    # Function without parameters
    void_func = FunctionType(return_type=void, parameter_types=[])
    assert void_func.name == "void ()"
    assert void_func.return_type == void
    assert void_func.parameter_types == []

def test_type_system():
    """Test type system functionality."""
    ts = TypeSystem()

    # Test built-in types
    assert ts.get_type("void") is not None
    assert ts.get_type("i32") is not None
    assert ts.get_type("u64") is not None
    assert ts.get_type("f64") is not None

    # Test pointer type creation
    i32 = ts.get_type("i32")
    assert i32 is not None
    ptr = ts.create_pointer_type(i32)
    assert ts.get_type("i32*") == ptr

    # Test array type creation
    arr = ts.create_array_type(i32, 10)
    assert ts.get_type("i32[10]") == arr

    # Test struct type creation
    fields = {"x": i32, "y": ts.get_type("f32")}
    struct = ts.create_struct_type("Point", fields)
    assert ts.get_type("Point") == struct

    # Test function type creation
    func = ts.create_function_type(i32, [i32, i32])
    assert ts.get_type("i32 (i32, i32)") == func

def test_type_compatibility():
    """Test type compatibility checking."""
    ts = TypeSystem()
    i32 = ts.get_type("i32")
    assert i32 is not None

    # Same types should be compatible
    assert i32.is_compatible_with(i32)

    # Different types should not be compatible
    i64 = ts.get_type("i64")
    assert i64 is not None
    assert not i32.is_compatible_with(i64)

    # Pointers to same type should be compatible
    ptr1 = ts.create_pointer_type(i32)
    ptr2 = ts.create_pointer_type(i32)
    assert ptr1.is_compatible_with(ptr2)

    # Pointers to different types should not be compatible
    ptr3 = ts.create_pointer_type(i64)
    assert not ptr1.is_compatible_with(ptr3)
