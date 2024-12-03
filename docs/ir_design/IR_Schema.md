# Intermediate Representation (IR) Schema

## Introduction

This document outlines the design of the Intermediate Representation (IR) for the Multilingual IR System. The IR is structured into two levels:

- **High-Level IR (HIR)**: Captures language-specific constructs, closely resembling the source code.
- **Low-Level IR (LIR)**: Provides a language-agnostic representation optimized for analysis and transformations.

## High-Level IR (HIR)

The HIR preserves rich information from the source code, including syntactic sugar and high-level constructs. It enables accurate mapping back to the original code, assisting in tasks like debugging and reverse engineering.

### Core Components

#### Abstract Syntax Trees (ASTs)

- **Nodes**: Represent syntactic constructs such as expressions, statements, and declarations.
- **Edges**: Define the hierarchical structure (parent-child relationships) of the syntax.
- **Metadata**: Includes source code locations and annotations.

#### Symbol Tables

- Store information about identifiers, types, scopes, and bindings.
- Enable name resolution and type checking.
- Support for namespaces and modules.

### HIR Elements

#### Nodes

- **Expression Nodes**: Literals, binary operations, function calls, etc.
- **Statement Nodes**: If statements, loops, return statements, etc.
- **Declaration Nodes**: Variable declarations, function prototypes, class definitions.

#### Edges

- **Syntax Edges**: Reflect the syntactic structure (e.g., a function node connected to its parameter nodes).
- **Reference Edges**: Link usage of symbols to their declarations.

#### Metadata

- **Source Locations**: File names, line numbers, and column numbers.
- **Annotations**: Compiler hints, optimization notes, or pragmas.

## Low-Level IR (LIR)

The LIR abstracts away language-specific details to provide a uniform platform for analysis. It is designed for performance and ease of analysis by simplifying complex constructs into fundamental operations.

### Core Components

#### Control Flow Graphs (CFGs)

- **Nodes**: Basic blocks containing sequences of instructions without branching.
- **Edges**: Represent possible flow of control between blocks (e.g., jumps, branches).
- **Entry and Exit Points**: Define the start and end of the program or function.

#### Program Dependency Graphs (PDGs)

- Combine both data and control dependencies.
- Used for advanced analyses like program slicing and impact analysis.
- **Data Dependencies**: Show how data values are related.
- **Control Dependencies**: Show how the execution of statements depends on control structures.

#### Symbol Tables (Optimized for LIR)

- Simplified for faster lookups during analysis.
- May include alias analysis information.

### LIR Elements

#### Nodes

- **Operation Nodes**: Represent low-level operations (e.g., arithmetic operations, memory accesses).
- **Variable Nodes**: Represent registers or memory locations.
- **Control Nodes**: Represent control operations (e.g., jumps, branches).

#### Edges

- **Control Flow Edges**: Indicate the possible execution paths.
- **Data Flow Edges**: Indicate the flow of data between operations.
- **Dependence Edges**: For parallelism and concurrency analysis.

#### Metadata

- **Optimizations Flags**: Indicate whether certain optimizations have been applied.
- **Runtime Information**: Profiling data such as execution counts.

## Mapping Between HIR and LIR

- **Transformation Process**:
  - The HIR is lowered to the LIR through a series of transformations.
  - Language-specific constructs are translated into universal representations.
- **Preservation of Semantics**:
  - Ensures that the behavior of the program remains unchanged.
  - Critical for correctness in analyses and optimizations.

## IR Design Considerations

- **Language Agnosticism**:
  - The IR must support features from multiple languages.
  - Extensible to accommodate new languages in the future.
- **Modularity**:
  - Different components (parsers, analyzers) interact through well-defined interfaces.
- **Performance**:
  - Optimized for static analysis tasks.
  - Efficient memory usage and processing speed.

## Diagrams and Examples

### Abstract Syntax Tree (AST)

```plaintext
FunctionDeclaration: foo
├── ParameterList
│   ├── Parameter: int x
│   └── Parameter: int y
└── Body
    └── ReturnStatement
        └── BinaryExpression: +
            ├── Identifier: x
            └── Identifier: y
```

### Control Flow Graph (CFG)

```plaintext
[Start] --> [Block 1] --> [Decision] --yes--> [Block 2] --> [End]
                               |
                              no
                               |
                            [Block 3] 
                               |
                               v
                            [End]
```

### Program Dependency Graph (PDG)

- Nodes represent statements and expressions.
- Edges represent control and data dependencies.

## Conclusion

The IR schema provides a robust foundation for advanced program analysis across multiple languages. By structuring the IR into HIR and LIR, we balance the need for language-specific details with the efficiency required for large-scale analysis.

## Future Work

- **Extend IR to Support Concurrency Constructs**:
  - Model threads, locks, and synchronization primitives.
- **Incorporate Intermediate Levels**:
  - Introduce Mid-Level IRs for specific analysis needs.
- **Enhance Metadata Annotations**:
  - Include security-related information for vulnerability analysis.
