# System Design Document

## Overview

The Multilingual Intermediate Representation (IR) System is designed to support multiple programming languages and advanced program analysis features. The system aims for extensibility, modularity, and scalability.

## Architecture

### Modular Design

- **Core Framework**: Implemented in C++ for performance-critical components.
- **Python Bindings**: Provide scripting, tooling, and interoperability.
- **Independent Modules**:
  - **Parsers**: Language-specific parsing modules.
  - **Analyzers**: Perform various static and dynamic analyses.
  - **IR Generators**: Build the IR from parsed code.
  - **Visualization Tools**: Represent IR components graphically.

### Data Flow

1. **Parsing Phase**:
   - Source code is input into language-specific parsers.
   - Parsers generate Abstract Syntax Trees (ASTs).
2. **IR Construction Phase**:
   - ASTs are converted into the High-Level IR (HIR).
   - HIR is transformed into the Low-Level IR (LIR) for optimization.
3. **Analysis Phase**:
   - Conduct analyses such as taint propagation, symbolic execution, and program slicing.
   - Results are used for optimization, security auditing, and performance enhancements.

## Recent Developments

### Python Bindings Implementation

- **Purpose**: Enable scripting, tooling, and interoperability through Python.
- **Implementation**:
  - Utilized `pybind11` to create bindings for the core IR classes (`Node` and `Edge`).
  - Created `bindings/pybind_module.cpp` to expose C++ classes to Python.
  - Configured the build system with `bindings/CMakeLists.txt` and updated the root `CMakeLists.txt` to include `pybind11` using CMake's `FetchContent`.
- **Features**:
  - Exposed methods for property management, edge connections, and more.
  - Enabled rapid prototyping and integration with Python scripts.
- **Testing**:
  - Developed `tests/test_bindings.py` to validate the Python bindings.
  - Successfully executed the test script, confirming the functionality of the bindings.

### Taint Propagation Analysis Implementation

- **Purpose**: Implemented as part of advanced program analysis features to detect potential security vulnerabilities arising from untrusted data flows.
- **Implementation**:
  - Developed the `TaintAnalysis` class in `src/analysis/TaintAnalysis.h` and `src/analysis/TaintAnalysis.cpp`.
  - Utilizes a worklist algorithm to propagate taint through the IR graph starting from specified entry points.
  - Analyzes the IR to identify nodes (variables, functions) that are influenced by tainted data.
- **Design Considerations**:
  - The module is designed to be extensible for future enhancements, such as supporting multiple taint sources and sinks.
  - Integrates seamlessly with existing IR structures (`Node` and `Edge` classes).
  - Employs efficient traversal methods to handle large graphs.
- **Testing**:
  - Created `tests/TaintAnalysisTest.cpp` with comprehensive unit tests.
  - Tests cover scenarios including successful taint propagation and cases where taint should not propagate.
  - All tests are passing, confirming the correctness and reliability of the module.

### Symbolic Execution Module Implementation

- **Purpose**: The Symbolic Execution module enhances the system's analysis capabilities by allowing symbolic exploration of program execution paths, essential for detecting potential bugs, vulnerabilities, and unintended behaviors.

- **Implementation**:
  - Developed the `SymbolicExecution` class in `src/analysis/SymbolicExecution.h` and `src/analysis/SymbolicExecution.cpp`.
  - Implemented a basic symbolic execution engine that processes IR nodes symbolically.
  - Capable of traversing the IR graph, handling branching, and maintaining symbolic state across nodes.

- **Design Considerations**:
  - Designed for extensibility, allowing future integration with constraint solvers like Z3 for path feasibility analysis.
  - Optimized for efficient traversal to handle large and complex codebases.

- **Testing**:
  - Created `tests/SymbolicExecutionTest.cpp` with unit tests covering basic execution and branching scenarios.
  - Updated `tests/CMakeLists.txt` to include the new test executable.
  - All tests are passing, confirming the correct functioning of the module.

### Adjustments to IR Classes

- **Property Management in `Node` and `Edge` Classes**:
  - Added `setProperty` and `getProperty` methods to `IRNode.h` and `IRNode.cpp`.
  - Ensured consistency across IR classes for property handling.
  - Facilitates annotation of IR elements with metadata required for analyses.

## Concurrency Support

- Models threads, locks, and synchronization mechanisms.
- Accurately represents concurrency constructs in the IR.
- Facilitates analyses like race condition detection and deadlock prevention.

## Avoiding Full Compilation

- Utilizes source-level parsing to minimize overhead.
- Employs partial compilation techniques where necessary.
- Handles duplicate symbol resolution gracefully to manage multiple definitions.

## Future Enhancements

- **Scalability Improvements**:
  - Optimize for large codebases and repositories.
- **Additional Language Support**:
  - Plan to add parsers for Swift, Kotlin, Rust, and more.
- **Advanced Analyses**:
  - Implement program slicing mechanisms.
  - Develop modules for deadlock detection and energy consumption analysis.
- **Community Feedback Integration**:
  - Establish channels for user input and collaboration.
  - Encourage contributions to expand capabilities and improve the system.

## Tools and Frameworks

- **Build System**: CMake for cross-platform compatibility.
- **Bindings**: `pybind11` utilized for Python interoperability.
- **Testing**:
  - **C++**: Google Test for unit testing.
  - **Python**: Python scripts and unit tests for bindings.
- **Inter-Module Communication**: Consider gRPC or ZeroMQ if needed.
- **Profiling and Performance**: Use `gprof` or Valgrind.

## Security Considerations

- Implement secure coding practices.
- Utilize input validation to prevent injection attacks.
- Ensure memory safety and efficient resource management.

## Deployment and Continuous Integration

- **CI Pipeline**: Configured with GitHub Actions.
- **Testing**: Automated unit tests for C++ and Python components.
- **Packaging**: Plans for distribution and deployment are underway.
