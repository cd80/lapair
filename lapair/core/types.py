"""
Type system implementation for the LaPair framework.

This module provides a unified type system that can represent types from various
source languages in a consistent way within the IR.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, TypeVar, Generic
import attr

@attr.s(auto_attribs=True, frozen=True)
class Type:
    """Base class for all types in the IR."""
    name: str
    size: Optional[int] = None  # Size in bits, if applicable

    def is_compatible_with(self, other: Type) -> bool:
        """Check if this type is compatible with another type."""
        return self == other

@attr.s(auto_attribs=True, frozen=True)
class VoidType(Type):
    """Represents the void type."""
    name: str = "void"
    size: Optional[int] = None

@attr.s(auto_attribs=True, frozen=True)
class IntegerType(Type):
    """Represents integer types."""
    signed: bool = True

    @classmethod
    def create(cls, size: int, signed: bool = True) -> IntegerType:
        """Create an integer type with the specified size and signedness."""
        name = f"{'i' if signed else 'u'}{size}"
        return cls(name=name, size=size, signed=signed)

@attr.s(auto_attribs=True, frozen=True)
class FloatType(Type):
    """Represents floating-point types."""
    
    @classmethod
    def create(cls, size: int) -> FloatType:
        """Create a float type with the specified size."""
        name = f"f{size}"
        return cls(name=name, size=size)

@attr.s(auto_attribs=True, frozen=True)
class PointerType(Type):
    """Represents pointer types."""
    pointee_type: Type
    name: str = attr.ib(init=False)
    size: int = 64  # Assuming 64-bit architecture by default

    def __attrs_post_init__(self) -> None:
        """Initialize the name based on the pointee type."""
        object.__setattr__(self, 'name', f"{self.pointee_type.name}*")

@attr.s(auto_attribs=True, frozen=True)
class ArrayType(Type):
    """Represents array types."""
    element_type: Type
    length: Optional[int] = None  # None for variable-length arrays
    name: str = attr.ib(init=False)
    size: Optional[int] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize name and size based on element type and length."""
        name = f"{self.element_type.name}[{self.length if self.length is not None else ''}]"
        size = (self.element_type.size * self.length) if (self.element_type.size is not None and self.length is not None) else None
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'size', size)

@attr.s(auto_attribs=True, frozen=True)
class StructType(Type):
    """Represents structure types."""
    fields: Dict[str, Type]
    name: str
    size: Optional[int] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        """Calculate the total size of the structure."""
        total_size = 0
        for field_type in self.fields.values():
            if field_type.size is None:
                total_size = None
                break
            total_size += field_type.size
        object.__setattr__(self, 'size', total_size)

@attr.s(auto_attribs=True, frozen=True)
class FunctionType(Type):
    """Represents function types."""
    return_type: Type
    parameter_types: List[Type]
    name: str = attr.ib(init=False)
    size: Optional[int] = None

    def __attrs_post_init__(self) -> None:
        """Initialize the name based on return and parameter types."""
        params_str = ", ".join(t.name for t in self.parameter_types)
        name = f"{self.return_type.name} ({params_str})"
        object.__setattr__(self, 'name', name)

class TypeSystem:
    """Manages types and their relationships in the IR."""
    
    def __init__(self) -> None:
        """Initialize the type system with built-in types."""
        self.types: Dict[str, Type] = {}
        self._initialize_builtin_types()

    def _initialize_builtin_types(self) -> None:
        """Initialize built-in types."""
        # Void type
        self.register_type(VoidType())

        # Integer types
        for size in [8, 16, 32, 64]:
            self.register_type(IntegerType.create(size, signed=True))
            self.register_type(IntegerType.create(size, signed=False))

        # Float types
        for size in [32, 64]:
            self.register_type(FloatType.create(size))

    def register_type(self, type_: Type) -> None:
        """Register a new type in the type system."""
        self.types[type_.name] = type_

    def get_type(self, name: str) -> Optional[Type]:
        """Get a type by name."""
        return self.types.get(name)

    def create_pointer_type(self, pointee_type: Type) -> PointerType:
        """Create a pointer type."""
        ptr_type = PointerType(pointee_type=pointee_type)
        self.register_type(ptr_type)
        return ptr_type

    def create_array_type(self, element_type: Type, length: Optional[int] = None) -> ArrayType:
        """Create an array type."""
        array_type = ArrayType(element_type=element_type, length=length)
        self.register_type(array_type)
        return array_type

    def create_struct_type(self, name: str, fields: Dict[str, Type]) -> StructType:
        """Create a structure type."""
        struct_type = StructType(name=name, fields=fields)
        self.register_type(struct_type)
        return struct_type

    def create_function_type(self, return_type: Type, parameter_types: List[Type]) -> FunctionType:
        """Create a function type."""
        func_type = FunctionType(return_type=return_type, parameter_types=parameter_types)
        self.register_type(func_type)
        return func_type
