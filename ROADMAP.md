# Project Roadmap

## Milestone 1: Project Initialization

- [x] **Initialize Git Repository**
- [x] **Set Up Project Structure**
- [x] **Create Essential Documentation**

## Milestone 2: Build System Setup

- [x] **Initialize Build System with CMake**

## Milestone 3: Pre-Commit Hooks and Code Quality

- [x] **Set Up Pre-Commit Hooks**
- [x] **Configure Unit Test Execution**

## Milestone 4: Initial IR Schema Development

- [x] **Draft the Initial IR Schema**
- [x] **Document IR Design**

## Milestone 5: Core Framework Implementation

- [x] **Set Up Modular Architecture**
- [x] **Develop Core Framework Components**
  - Implemented `Node` and `Edge` classes for IR.
  - Created `IRNode.h`, `IRNode.cpp`, `IREdge.h`, and `IREdge.cpp`.

- [x] **Write Unit Tests for Core Components**
  - Implemented unit tests for the `IRNode` and `IREdge` classes.
  - Configured Google Test framework using CMake's `FetchContent`.
  - Tests are passing and integrated into the build and CI pipeline.

## Milestone 6: Parser Implementation for C++

- [x] **Implement C++ Parser**
  - Began implementation using Clang's LibTooling.
  - Created `CPPParser.cpp` for Clang Tooling setup.
  - Developed `IRGenerator.h` and `IRGenerator.cpp` for AST traversal.
  - Encountered issues with standard header files; ongoing resolution documented in `LESSONS_LEARNED.md`.

- [ ] **Resolve Parsing Issues**
  - Continue investigating the `'stdarg.h' file not found` error.
  - Explore alternative solutions and consult documentation.

- [ ] **Write Parser Unit Tests**
  - To be implemented after resolving parsing issues.

## Milestone 7: Python Bindings Implementation

- [x] **Implement Python Bindings for IR Classes**
  - Utilized `pybind11` to create bindings for `Node` and `Edge` classes.
  - Created `bindings/pybind_module.cpp` and configured build with `bindings/CMakeLists.txt`.
  - Successfully built the Python module `ir_bindings` and tested with `tests/test_bindings.py`.

## Milestone 8: Advanced Program Analysis Features

- [x] **Implement Taint Propagation Analysis**
  - Developed `TaintAnalysis` module.
  - Wrote unit tests in `tests/TaintAnalysisTest.cpp`.
  - Updated documentation accordingly.

- [x] **Integrate Symbolic/Concolic Execution**
  - Developed `SymbolicExecution` module.
  - Wrote unit tests in `tests/SymbolicExecutionTest.cpp`.
  - Updated documentation accordingly.

- [x] **Construct Program Slicing Mechanisms**
  - Developed `ProgramSlicing` module.
  - Wrote unit tests in `tests/ProgramSlicingTest.cpp`.
  - Updated documentation accordingly.

## Milestone 9: Concurrency Support

- [ ] **Model Concurrency Semantics**
  - Plan and begin implementation of concurrency analysis modules.
  - Design models for threads, locks, and synchronization mechanisms.

## Milestone 10: Multi-Language Support and Interoperability

- [ ] **Design Unified Symbol Table**
- [ ] **Implement Interoperability Constructs**
- [ ] **Add Parsers for Additional Languages**

## Milestone 11: Performance Optimization

- [ ] **Profile System Performance**
- [ ] **Optimize for Scalability**

## Milestone 12: Tooling and Visualization

- [ ] **Develop Command-Line Tools**
- [ ] **Implement Visualization Tools**

## Milestone 13: Continuous Integration and Deployment

- [x] **Set Up Continuous Integration Pipelines**
  - Configured GitHub Actions pipeline.
  - Automated building, testing, and code quality checks.

- [ ] **Plan Deployment Strategies**

## Milestone 14: Documentation and Community Engagement

- [x] **Expand Documentation**
  - Updated `DESIGN.md` and `README.md` with recent developments.
  - Documented program slicing and usage instructions.

- [ ] **Establish Community Channels**
- [ ] **Incorporate Feedback Mechanisms**

## Ongoing Tasks and Future Enhancements

- **Code Review and Quality Assurance**
- **Advanced Testing Strategies**
- **Security and Compliance**
- **Backup, Recovery, and Monitoring**
- **Accessibility and Ethical Compliance**
- **Resource Management**
- **Future Enhancements**
  - Deadlock detection in concurrency.
  - Support for additional programming paradigms.
  - Enhanced visualization and user interfaces.
  - Machine learning integration for code analysis.
