"""Tests for common frontend interfaces."""

import pytest
from typing import List, Optional, Any

from lapair.core.ir import IR, Module, Location
from lapair.frontends.common.frontend import (
    SourceLocation,
    AST,
    ASTVisitor,
    Parser,
    Frontend,
)

class MockAST:
    """Mock AST implementation for testing."""
    def __init__(self, location: Optional[SourceLocation] = None, children: List['MockAST'] = None):
        self._location = location
        self._children = children or []

    @property
    def location(self) -> Optional[SourceLocation]:
        return self._location

    @property
    def children(self) -> List['MockAST']:
        return self._children

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit(self)

class MockVisitor(ASTVisitor[MockAST]):
    """Mock visitor implementation for testing."""
    def visit(self, node: MockAST) -> Any:
        return "visited"

class MockParser(Parser):
    """Mock parser implementation for testing."""
    def parse_file(self, file_path: str) -> Optional[AST]:
        return MockAST()

    def parse_string(self, content: str, file_path: str = "<string>") -> Optional[AST]:
        return MockAST()

class MockFrontend(Frontend):
    """Mock frontend implementation for testing."""
    def create_parser(self) -> Parser:
        return MockParser()

    def create_module(self, name: str) -> Module:
        return self.ir.create_module(name)

    def process_file(self, file_path: str) -> Optional[Module]:
        ast = self.parser.parse_file(file_path)
        if ast:
            module = self.create_module(file_path)
            return module
        return None

    def process_string(self, content: str, file_path: str = "<string>") -> Optional[Module]:
        ast = self.parser.parse_string(content, file_path)
        if ast:
            module = self.create_module(file_path)
            return module
        return None

def test_source_location():
    """Test SourceLocation creation and conversion."""
    loc = SourceLocation(
        file="test.py",
        start_line=1,
        start_column=0,
        end_line=1,
        end_column=10
    )
    
    assert loc.file == "test.py"
    assert loc.start_line == 1
    assert loc.start_column == 0
    assert loc.end_line == 1
    assert loc.end_column == 10
    
    ir_loc = loc.to_ir_location()
    assert isinstance(ir_loc, Location)
    assert ir_loc.file == loc.file
    assert ir_loc.line == loc.start_line
    assert ir_loc.column == loc.start_column
    assert ir_loc.end_line == loc.end_line
    assert ir_loc.end_column == loc.end_column

def test_ast_visitor():
    """Test ASTVisitor functionality."""
    ir = IR()
    visitor = MockVisitor(ir)
    
    # Test basic visitor functionality
    ast = MockAST()
    result = ast.accept(visitor)
    assert result == "visited"
    
    # Test error and warning handling
    loc = SourceLocation("test.py", 1, 0, 1, 10)
    visitor.add_error("Test error", loc)
    visitor.add_warning("Test warning", loc)
    
    assert len(visitor.errors) == 1
    assert len(visitor.warnings) == 1
    assert "test.py:1:0" in visitor.errors[0]
    assert "test.py:1:0" in visitor.warnings[0]

def test_parser():
    """Test Parser functionality."""
    parser = MockParser()
    
    # Test parsing
    ast = parser.parse_file("test.py")
    assert isinstance(ast, MockAST)
    
    ast = parser.parse_string("test code")
    assert isinstance(ast, MockAST)
    
    # Test error and warning handling
    loc = SourceLocation("test.py", 1, 0, 1, 10)
    parser.add_error("Test error", loc)
    parser.add_warning("Test warning", loc)
    
    assert len(parser.errors) == 1
    assert len(parser.warnings) == 1
    assert "test.py:1:0" in parser.errors[0]
    assert "test.py:1:0" in parser.warnings[0]

def test_frontend():
    """Test Frontend functionality."""
    ir = IR()
    frontend = MockFrontend(ir)
    
    # Test module creation
    module = frontend.process_file("test.py")
    assert isinstance(module, Module)
    assert module.name == "test.py"
    
    module = frontend.process_string("test code")
    assert isinstance(module, Module)
    assert module.name == "<string>"
    
    # Test error and warning handling
    loc = SourceLocation("test.py", 1, 0, 1, 10)
    frontend.add_error("Test error", loc)
    frontend.add_warning("Test warning", loc)
    
    assert len(frontend.errors) == 1
    assert len(frontend.warnings) == 1
    assert "test.py:1:0" in frontend.errors[0]
    assert "test.py:1:0" in frontend.warnings[0]
    
    # Test error aggregation
    frontend.parser.add_error("Parser error")
    assert len(frontend.get_all_errors()) == 2
    assert frontend.has_errors()
    
    frontend.parser.add_warning("Parser warning")
    assert len(frontend.get_all_warnings()) == 2
