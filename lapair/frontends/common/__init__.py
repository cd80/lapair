"""Common interfaces and utilities for language frontends."""

from lapair.frontends.common.frontend import (
    Frontend,
    Parser,
    AST,
    ASTVisitor,
    SourceLocation,
)

__all__ = [
    'Frontend',
    'Parser',
    'AST',
    'ASTVisitor',
    'SourceLocation',
]
