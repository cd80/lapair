# Multilingual Intermediate Representation (IR) System

## Overview

The Multilingual IR System is designed to support multiple programming languages and provide advanced program analysis features. It aims to facilitate inter-repository, inter-file, inter-procedural, and inter-language analysis without the need for full compilation, while gracefully resolving duplicate symbols.

## Objectives

- **Language Support**: C, C++, Java, Swift, Kotlin, Rust, Objective-C, JavaScript, TypeScript.
- **Advanced Analysis Features**:
  - Taint propagation analysis.
  - Symbolic/concolic execution.
  - Program slicing.
- **Concurrency Support**: Model concurrency constructs and enable analysis like deadlock detection.
- **Interoperability**: Support inter-language interactions through a unified symbol table and interoperability constructs.
- **Performance**: Optimize for scalability and efficiency, avoiding full compilation when possible.

## Programming Languages Used

- **C++**: Chosen for the core framework due to its performance and control over system resources.
- **Python**: Utilized for scripting, tooling, and interoperability through Python bindings.

## Rationale for Language Selection

- **C++**:
  - High performance and low-level system access.
  - Extensive libraries and tools for system programming.
  - Strong support for concurrent and parallel programming.
- **Python**:
  - Rapid prototyping capability.
  - Ease of integration with other systems.
  - Large ecosystem of libraries for scripting and automation.

## Prerequisites for Contributors

- **C++ Knowledge**: Proficiency in modern C++ (C++17 or later).
- **Python Knowledge**: Familiarity with Python 3.x and relevant libraries.
- **Build Tools**: Experience with CMake for building C++ projects.
- **Version Control**: Understanding of Git workflows.
- **Development Environment**:
  - **Compiler**: LLVM/Clang toolchain.
  - **Operating System**: Development primarily on macOS and Linux.

## Setting Up the Development Environment

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/cd80/lapair.git
   ```

2. **Install Dependencies**:

   - **LLVM/Clang**:
     - macOS: Install via Homebrew.
       ```bash
       brew install llvm
       ```
     - Linux: Install via package manager or build from source.
   - **Python Packages**: Install required Python packages using `pip`.
     ```bash
     pip install -r requirements.txt
     ```

3. **Build the Project**:

   ```bash
   mkdir build
   cd build
   cmake ..
   make
   ```

4. **Run Tests**:

   ```bash
   ctest --output-on-failure
   ```

## Using the Python Bindings

The project now includes Python bindings for the core IR classes, allowing you to interact with the IR system using Python.

### Running Python Examples

1. **Set `PYTHONPATH`**:

   Ensure that Python can locate the `ir_bindings` module by adding the `build/bindings` directory to `PYTHONPATH`.

   ```bash
   export PYTHONPATH=build/bindings:$PYTHONPATH
   ```

2. **Run the Test Script**:

   Navigate to the project root directory and run the test script to verify the bindings.

   ```bash
   python3 tests/test_bindings.py
   ```

   **Expected Output**:

   ```
   Node A ID: A, Color: red
   Node B ID: B, Color: blue
   Edge ID: edge1, Weight: 5
   Edge from A to B
   ```

### Integrating Python Bindings in Your Scripts

You can now import the `ir_bindings` module in your Python scripts to create and manipulate IR nodes and edges.

```python
import ir_bindings

# Create nodes
node_a = ir_bindings.Node("A")
node_b = ir_bindings.Node("B")

# Set properties
node_a.setProperty("type", "function")
node_b.setProperty("type", "variable")

# Create edge
edge = ir_bindings.Edge("edge1", node_a, node_b)

# Manipulate the IR as needed
```

## Contributing to the Project

- **Coding Standards**: Follow the guidelines outlined in `CONTRIBUTING.md`.
- **Pre-commit Hooks**: Ensure pre-commit hooks are set up and functional.
- **Testing**: Write unit tests for new features and ensure all tests pass before committing.
- **Documentation**: Update relevant documentation for any changes or new features.
- **Pull Requests**: Submit pull requests with clear descriptions and await code review.

## Code Quality Practices

- **Linters and Formatters**:
  - **C++**: `clang-format`, `clang-tidy`.
  - **Python**: `pylint`, `flake8`.
- **Pre-commit Hooks**: Automated checks to enforce coding standards.
- **Continuous Integration**: Builds and tests run automatically via GitHub Actions.

## Project Status

See `ROADMAP.md` for milestones and progress.

## Licensing and Legal Considerations

- This project is licensed under the MIT License (see `LICENSE` for details).

## Security Reporting

- Please see `SECURITY.md` for information on how to report security vulnerabilities.

## Contact and Communication

- For questions, please open an issue on GitHub or reach out to the maintainers.
