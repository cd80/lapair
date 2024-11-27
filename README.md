# LaPair - Language-agnostic Program Analysis IR Framework

LaPair is a robust and extensible Intermediate Representation (IR) framework designed to serve as a unified foundation for program analysis and vulnerability detection across multiple programming languages.

## Overview

LaPair provides a sophisticated IR system that can represent source code from various programming languages in a unified format, enabling powerful cross-language analysis capabilities. The framework is designed to be language-agnostic, providing clean interfaces for language frontend developers to integrate their parsers.

## Features

### Core IR System

- **Rich Instruction Set**: Comprehensive set of IR instructions supporting various programming constructs
- **Advanced Type System**: Sophisticated type representation with support for complex type relationships
- **Robust Symbol Management**: Efficient symbol handling with proper scoping and resolution
- **Control Flow Representation**: Detailed control flow tracking and analysis capabilities

### Integration Support

- **Clean Frontend Interfaces**: Well-documented APIs for language frontend integration
- **Flexible AST Mapping**: Support for converting various AST structures to IR
- **Error Handling**: Robust error reporting and diagnostic capabilities
- **Source Tracking**: Detailed source location preservation

### Analysis Capabilities

- **Control Flow Analysis**: Framework for analyzing program control flow
- **Data Flow Analysis**: Infrastructure for tracking data flow and dependencies
- **Type Analysis**: Tools for type checking and inference
- **Symbol Resolution**: Advanced symbol lookup and resolution

## Project Status

Currently focusing on core IR system enhancement. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress and [ROADMAP.md](ROADMAP.md) for planned features.

## Installation

```bash
pip install lapair
```

## Usage

Documentation for frontend developers will be available as the project matures. The framework will provide:

- IR system documentation
- Integration guides
- API reference
- Example implementations

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
