"""
Symbol table implementation for the LaPair framework.

This module provides symbol management and scoping functionality for the IR,
allowing efficient symbol lookup and scope handling across different contexts.
"""

from __future__ import annotations

from typing import Dict, Optional, Set, List
import attr

from lapair.core.types import Type

@attr.s(auto_attribs=True)
class Symbol:
    """Represents a symbol in the IR."""
    name: str
    type: Type
    is_global: bool = False
    is_constant: bool = False
    is_defined: bool = False
    scope: Optional[Scope] = None

    def __attrs_post_init__(self) -> None:
        """Register this symbol with its scope if one is provided."""
        if self.scope is not None:
            self.scope.add_symbol(self)

@attr.s(auto_attribs=True)
class Scope:
    """Represents a scope in the IR."""
    name: str
    parent: Optional[Scope] = None
    children: List[Scope] = attr.Factory(list)
    symbols: Dict[str, Symbol] = attr.Factory(dict)

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to this scope."""
        self.symbols[symbol.name] = symbol
        symbol.scope = self

    def lookup_symbol(self, name: str, recursive: bool = True) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: The name of the symbol to look up
            recursive: If True, search parent scopes if not found in current scope
        
        Returns:
            The symbol if found, None otherwise
        """
        symbol = self.symbols.get(name)
        if symbol is not None or not recursive or self.parent is None:
            return symbol
        return self.parent.lookup_symbol(name, recursive=True)

    def add_child_scope(self, name: str) -> Scope:
        """Create and add a new child scope."""
        child = Scope(name=name, parent=self)
        self.children.append(child)
        return child

class SymbolTable:
    """Manages symbols and their scopes in the IR."""

    def __init__(self) -> None:
        """Initialize the symbol table with a global scope."""
        self.global_scope = Scope(name="global")
        self.current_scope = self.global_scope

    def enter_scope(self, name: str) -> None:
        """Enter a new scope."""
        self.current_scope = self.current_scope.add_child_scope(name)

    def exit_scope(self) -> None:
        """Exit the current scope."""
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    def add_symbol(self, name: str, type_: Type, is_global: bool = False,
                  is_constant: bool = False, is_defined: bool = False) -> Symbol:
        """Add a symbol to the current scope."""
        symbol = Symbol(
            name=name,
            type=type_,
            is_global=is_global,
            is_constant=is_constant,
            is_defined=is_defined,
            scope=self.current_scope
        )
        return symbol

    def lookup_symbol(self, name: str, current_scope_only: bool = False) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: The name of the symbol to look up
            current_scope_only: If True, only search the current scope
        
        Returns:
            The symbol if found, None otherwise
        """
        return self.current_scope.lookup_symbol(name, recursive=not current_scope_only)

    def get_scope_symbols(self, include_parent_scopes: bool = False) -> Dict[str, Symbol]:
        """
        Get all symbols in the current scope.
        
        Args:
            include_parent_scopes: If True, include symbols from parent scopes
        
        Returns:
            Dictionary mapping symbol names to Symbol objects
        """
        if not include_parent_scopes:
            return dict(self.current_scope.symbols)
        
        symbols = {}
        scope = self.current_scope
        while scope is not None:
            for name, symbol in scope.symbols.items():
                if name not in symbols:
                    symbols[name] = symbol
            scope = scope.parent
        return symbols

    def get_global_symbols(self) -> Dict[str, Symbol]:
        """Get all global symbols."""
        return {name: symbol for name, symbol in self.global_scope.symbols.items()
                if symbol.is_global}

    def clear_scope(self) -> None:
        """Clear all symbols from the current scope."""
        self.current_scope.symbols.clear()

    def reset(self) -> None:
        """Reset the symbol table to initial state."""
        self.global_scope = Scope(name="global")
        self.current_scope = self.global_scope
