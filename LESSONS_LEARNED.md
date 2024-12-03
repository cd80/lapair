# Lessons Learned

## Issue: Implementing Python Bindings with `pybind11`

### Description

While integrating Python bindings into the project, several challenges and insights were encountered. The goal was to expose the core IR classes (`Node` and `Edge`) to Python using `pybind11`, enabling scripting and interoperability.

### Challenges and Resolutions

#### Missing `pybind11` Headers

- **Problem**: Compilation errors indicated that the compiler could not find the `pybind11` header files.
- **Resolution**:
  - Added `pybind11` to the project using CMake's `FetchContent` module in `CMakeLists.txt`.
  - Corrected include directories and linked targets in `bindings/CMakeLists.txt`.

#### Syntax Errors Due to HTML Entities

- **Problem**: Encountered errors like `use of undeclared identifier 'amp'` caused by the use of `&amp;` instead of `&`.
- **Resolution**:
  - Replaced all instances of `&amp;` with the actual `&` symbol in `bindings/pybind_module.cpp`.

#### Undefined Methods in IR Classes

- **Problem**: Compilation errors due to `setProperty` and `getProperty` methods not being defined in the `Node` class.
- **Resolution**:
  - Added `setProperty` and `getProperty` methods to `IRNode.h` and implemented them in `IRNode.cpp`.
  - Ensured consistency with the `Edge` class, which already had these methods.

#### Module Not Found Error When Testing Bindings

- **Problem**: Python could not locate the `ir_bindings` module when running the test script.
- **Resolution**:
  - Updated the `PYTHONPATH` environment variable to include the directory where `ir_bindings` was built (`build/bindings`).
  - Confirmed successful import and execution of `tests/test_bindings.py`.

### Insights Gained

- **Build System Integration**:
  - Recognized the importance of correctly configuring CMake when adding new dependencies and targets.
  - Using `FetchContent` to manage third-party libraries simplifies dependency management.

- **Consistency Across Codebase**:
  - Ensured that class interfaces are consistent to prevent errors when extending functionality (e.g., property management in both `Node` and `Edge`).

- **Testing and Verification**:
  - Emphasized writing test scripts in both C++ and Python to validate functionality and catch issues early.
  - Proper setup of environment variables is essential for testing modules not installed system-wide.

### Future Considerations

- **Enhanced Documentation**:
  - Plan to document the process of building and using the Python bindings for future contributors.
  - Provide guidelines on extending the bindings to new classes and functionalities.

- **Error Handling**:
  - Implement more robust error handling in both the C++ and Python code to provide clearer messages for debugging.

- **Community Engagement**:
  - Encourage contributions from the community to expand the bindings and improve the system.

## Issue: 'stdarg.h' File Not Found When Running the C++ Parser

*(Previously documented; ongoing investigation. See above for details.)*

### Further Actions

- **Consult Clang Tooling Documentation**: Investigate nuances in Clang Tooling on macOS.
- **Community Assistance**: Reach out for insights or known issues.
