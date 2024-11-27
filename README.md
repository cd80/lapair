# LaPair - Language-agnostic Program Analysis IR Framework

LaPair is a robust and extensible Intermediate Representation (IR) framework designed for comprehensive program analysis and vulnerability detection across multiple programming languages.

## Overview

LaPair provides a unified IR that serves as a foundation for analyzing source code from various programming languages including:

- C/C++
- Objective-C
- Swift
- Java
- Kotlin
- Rust
- JavaScript/TypeScript
- Python

The framework is designed with modularity and extensibility in mind, allowing easy integration of new language frontends and analysis tools.

## Features

- **Language-agnostic IR Design**: Represents syntactic and semantic structures of supported languages in a unified way
- **Comprehensive Analysis Support**:
  - Inter-file analysis
  - Inter-procedural analysis
  - Intra-procedural analysis
- **Sophisticated Type System**:
  - Unified type representation
  - Cross-language type mapping
  - Type inference capabilities
- **Symbol Management**:
  - Global symbol table
  - Scope-aware symbol resolution
  - Cross-module symbol handling
- **Control Flow Analysis**:
  - Comprehensive call graph generation
  - Control flow graph construction
  - Path analysis
- **Extensible Architecture**:
  - Modular language frontend design
  - Custom parser integration support
  - Analysis framework plugins
- **Performance Optimizations**:
  - Parallel processing support
  - Efficient data structures
  - Memory optimization
- **Developer-Friendly**:
  - Clean, well-documented APIs
  - Comprehensive test coverage
  - Detailed documentation

## Project Status

Currently in initial development. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress and [ROADMAP.md](ROADMAP.md) for planned features.

## Installation

```bash
pip install lapair
```

## Usage

Documentation for language frontend development and IR manipulation will be available soon.

## Development

To set up the development environment:

```bash
git clone https://github.com/cd80/lapair.git
cd lapair
pip install -e ".[dev]"
```

Run tests:

```bash
pytest -v
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or inquiries, please open an issue on GitHub.
