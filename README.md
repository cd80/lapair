# LaPair

LaPair is a comprehensive Intermediate Representation (IR) framework designed specifically for program analysis. Rather than implementing programs directly, LaPair provides the foundational infrastructure needed to analyze programs written in various programming languages.

## Purpose

The primary goal of LaPair is to provide a robust IR framework that enables:

- Program analysis tools to work with a unified representation of code
- Static analysis implementations to focus on analysis logic rather than IR handling
- Research and development of new program analysis techniques

LaPair is **not** a programming language or a compiler - it is a framework that provides the intermediate representation and analysis infrastructure needed to build program analysis tools.

## Key Features

### Core IR Framework

- Language-agnostic intermediate representation
- Comprehensive type system supporting multiple programming language features
- Symbol table management with scope handling
- Support for inter-procedural and inter-file analysis

### Analysis Infrastructure

- Control Flow Graph (CFG) construction and manipulation
- Data Flow Analysis framework supporting both forward and backward analyses
- Built-in analyses including:
  - Reaching Definitions Analysis
  - Live Variable Analysis
  - Constant Propagation Analysis
  - Available Expressions Analysis

### Extensibility

- Well-defined interfaces for implementing new analyses
- Support for custom data flow lattices
- Modular design allowing easy addition of new features

## Framework Components

### IR Core (`lapair/core/`)

- Basic blocks and instructions
- Functions and modules
- Type system
- Symbol management
- Specialized instruction types for operations

### Analysis Framework (`lapair/analysis/`)

- Control flow analysis
- Data flow analysis infrastructure
- Common analysis implementations
- Variable version tracking

### Frontend Interface (`lapair/frontends/`)

- Common interface for language frontends
- Language-specific type mapping
- Abstract syntax tree conversion

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pytest for running tests

### Installation

```bash
git clone https://github.com/cd80/lapair.git
cd lapair
pip install -r requirements.txt
```

### Running Tests

```bash
pytest -v
```

## Using LaPair

### Implementing a New Analysis

```python
from lapair.analysis.data_flow import DataFlowAnalysis

class MyAnalysis(DataFlowAnalysis):
    def flow_function(self, node, in_set):
        # Implement your analysis logic here
        pass

    def meet_operator(self, sets):
        # Implement your meet operator here
        pass
```

### Working with Available Expressions Analysis

```python
from lapair.core.ir import Function, BasicBlock, AddInstruction, MulInstruction
from lapair.analysis.control_flow import ControlFlowGraph
from lapair.analysis.data_flow import AvailableExpressionsAnalysis

# Create IR structures
function = Function(name="example", return_type=void_type, parameters=[])
block = BasicBlock(name="entry")

# Add instructions
x_plus_y = AddInstruction(type=int_type, name="a", operands=[x, y])
x_times_y = MulInstruction(type=int_type, name="b", operands=[x, y])
block.add_instruction(x_plus_y)
block.add_instruction(x_times_y)

function.add_block(block)

# Perform analysis
cfg = ControlFlowGraph(function)
analysis = AvailableExpressionsAnalysis(function=function, cfg=cfg)
analysis.analyze()

# Get results
available_expressions = analysis.out_sets[cfg.nodes[block]]
```

### Working with the IR

```python
from lapair.core.ir import Function, BasicBlock, Instruction

# Create IR structures
function = Function(name="example", return_type=void_type, parameters=[])
block = BasicBlock(name="entry")
function.add_block(block)

# Perform analysis
cfg = ControlFlowGraph(function)
analysis = MyAnalysis(function=function, cfg=cfg)
analysis.analyze()
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [IR Framework Guide](docs/ir_framework.md)
- [Analysis Framework Guide](docs/analysis_framework.md)
- [Frontend Interface Guide](docs/frontend_interface.md)

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- How to implement new analyses
- How to add support for new language features
- How to report and fix bugs

## License

This project is licensed under the [MIT License](LICENSE).

## Recent Updates

- Added Available Expressions Analysis with proper handling of expressions and variable versions
- Implemented specific instruction types for better operation tracking
- Enhanced control flow handling with improved variable version tracking
- Added comprehensive test coverage for all analyses
