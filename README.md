# Multilingual Intermediate Representation (IR) System

Welcome to the Multilingual IR System project. This project aims to develop a robust, scalable Intermediate Representation (IR) system that supports multiple programming languages and advanced program analysis features.

## Objectives

- **Support Multiple Languages**: C, C++, Java, Swift, Kotlin, Rust, Objective-C, JavaScript, TypeScript.
- **Advanced Program Analysis Features**:
  - Taint Propagation Analysis
  - Symbolic/Concolic Execution
  - Program Slicing
- **Concurrency Support**: Accurate representation of concurrency constructs.
- **Comprehensive Analysis**: Inter-repository, inter-file, inter-procedural, and inter-language analysis.
- **Efficient Parsing**: Avoid full compilation by employing source-level parsing and partial compilation techniques.
- **Graceful Duplicate Symbol Resolution**: Strategies to handle duplicate symbols effectively.

## Programming Languages Used

- **C++**: Used for the core framework due to its performance and control over system resources.
- **Python**: Utilized for scripting, tooling, and interoperability through bindings.

## Rationale for Language Selection

- **C++**: Provides high performance and system-level capabilities essential for the core framework.
- **Python**: Offers rapid prototyping and ease of scripting, enhancing interoperability via bindings.

## Prerequisites for Contributors

- Proficiency in C++ and Python programming.
- Understanding of compiler design and program analysis concepts.
- Familiarity with Git and version control workflows.
- Required tools and software:
  - C++ compiler (supporting C++17 or later).
  - Python 3.7 or later.
  - CMake for build management.
  - Git for version control.

## Development Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/cd80/lapair.git
   ```
2. **Install Dependencies**
   - Ensure a C++ compiler (e.g., GCC or Clang) is installed.
   - Install Python 3.7 or later.
   - Install CMake.
3. **Build the Project**
   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```
4. **Run Tests**
   ```bash
   make test
   ```

## Contributing to the Project

We welcome contributions from the community. Please adhere to the following guidelines:

- **Coding Standards**: Follow the coding standards outlined in `CONTRIBUTING.md`.
- **Code Quality**: Utilize pre-commit hooks to enforce coding standards and run linters.
- **Branching Strategy**: Use the GitFlow branching model for version control.
- **Pull Requests**: Submit pull requests with clear descriptions and ensure all CI checks pass.

## Code Quality Practices

- **Pre-commit Hooks**: Set up using tools like `pre-commit` or custom scripts to enforce code quality.
- **Linters**:
  - **C++**: `clang-format`, `clang-tidy`
  - **Python**: `pylint`, `flake8`
- **Unit Tests**: Implement unit tests for all new features in the `tests/` directory.
