"""Core interfaces for language frontends."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, TypeVar, Generic, Protocol

from lapair.core.ir import IR, Module, Value, Location
from lapair.core.types import Type, TypeSystem

@dataclass
class SourceLocation:
    """Represents a location in source code."""
    file: str
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    
    def to_ir_location(self) -> Location:
        """Convert to IR Location."""
        return Location(
            file=self.file,
            line=self.start_line,
            column=self.start_column,
            end_line=self.end_line,
            end_column=self.end_column
        )

class AST(Protocol):
    """Protocol for AST nodes."""
    @property
    def location(self) -> Optional[SourceLocation]:
        """Get the source location of this node."""
        ...

    @property
    def children(self) -> List[AST]:
        """Get child nodes."""
        ...

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor."""
        ...

T = TypeVar('T', bound=AST)

class ASTVisitor(abc.ABC, Generic[T]):
    """Base class for AST visitors."""
    
    def __init__(self, ir: IR) -> None:
        """Initialize the visitor with an IR instance."""
        self.ir = ir
        self.current_module: Optional[Module] = None
        self.type_system = ir.type_system
        self.errors: List[str] = []
        self.warnings: List[str] = []

    @abc.abstractmethod
    def visit(self, node: T) -> Any:
        """Visit an AST node."""
        raise NotImplementedError

    def add_error(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add an error message."""
        if location:
            self.errors.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.errors.append(message)

    def add_warning(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add a warning message."""
        if location:
            self.warnings.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.warnings.append(message)

class Parser(abc.ABC):
    """Base class for language parsers."""
    
    def __init__(self) -> None:
        """Initialize the parser."""
        self.errors: List[str] = []
        self.warnings: List[str] = []

    @abc.abstractmethod
    def parse_file(self, file_path: str) -> Optional[AST]:
        """Parse a source file into an AST."""
        raise NotImplementedError

    @abc.abstractmethod
    def parse_string(self, content: str, file_path: str = "<string>") -> Optional[AST]:
        """Parse a string into an AST."""
        raise NotImplementedError

    def add_error(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add an error message."""
        if location:
            self.errors.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.errors.append(message)

    def add_warning(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add a warning message."""
        if location:
            self.warnings.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.warnings.append(message)

class Frontend(abc.ABC):
    """Base class for language frontends."""
    
    def __init__(self, ir: IR) -> None:
        """Initialize the frontend with an IR instance."""
        self.ir = ir
        self.parser = self.create_parser()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    @abc.abstractmethod
    def create_parser(self) -> Parser:
        """Create a parser for this frontend."""
        raise NotImplementedError

    @abc.abstractmethod
    def create_module(self, name: str) -> Module:
        """Create a new IR module."""
        raise NotImplementedError

    @abc.abstractmethod
    def process_file(self, file_path: str) -> Optional[Module]:
        """Process a source file and convert it to IR."""
        raise NotImplementedError

    @abc.abstractmethod
    def process_string(self, content: str, file_path: str = "<string>") -> Optional[Module]:
        """Process a string and convert it to IR."""
        raise NotImplementedError

    def add_error(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add an error message."""
        if location:
            self.errors.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.errors.append(message)

    def add_warning(self, message: str, location: Optional[SourceLocation] = None) -> None:
        """Add a warning message."""
        if location:
            self.warnings.append(f"{location.file}:{location.start_line}:{location.start_column}: {message}")
        else:
            self.warnings.append(message)

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0 or len(self.parser.errors) > 0

    def get_all_errors(self) -> List[str]:
        """Get all errors from both frontend and parser."""
        return self.errors + self.parser.errors

    def get_all_warnings(self) -> List[str]:
        """Get all warnings from both frontend and parser."""
        return self.warnings + self.parser.warnings
