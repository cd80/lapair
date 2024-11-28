# LaPair

LaPair is a robust and extensible Intermediate Representation (IR) framework designed to facilitate program analysis and vulnerability detection across multiple programming languages. The core IR serves as a solid foundation for future analysis tools and supports comprehensive code representation.

## Key Features

- **Unified IR Framework**

  - Supports multiple programming languages: **C, C++, Objective-C, Swift, Java, Kotlin, Rust, JavaScript, TypeScript, Python**.
  - Provides a language-agnostic representation to enable consistent analysis across different languages.

- **Inter-Procedural and Inter-File Analysis Support**

  - Designed to inherently support inter-procedural representations, allowing analysis across function and method boundaries.
  - Facilitates inter-file analysis, enabling cross-module optimizations and comprehensive program understanding.

- **Modular Architecture**

  - Separates core IR components from language frontends and analysis modules.
  - Promotes a clean, maintainable, and extensible project structure.

- **Advanced Type System**

  - Capable of representing complex types and type relationships found in various languages.
  - Supports language-specific type features while maintaining a unified approach.

- **Symbol Table Management**
  - Implements symbol tables with scope and namespace handling.
  - Supports accurate symbol resolution across different languages and modules.

## Getting Started

### Prerequisites

- **Python 3.7 or higher**
- **pytest** for running tests

### Installation

Clone the repository:

```bash
git clone https://github.com/cd80/lapair.git
cd lapair
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Running Tests

Ensure all tests pass:

```bash
pytest -v
```

## Documentation

Comprehensive documentation is available to help you understand and utilize the LaPair framework effectively. [Link to documentation or explain where to find it.]

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the [MIT License](LICENSE).
