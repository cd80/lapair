# CMake configuration for Python bindings

# Create the Python module using pybind11
pybind11_add_module(ir_bindings pybind_module.cpp)

# Link the module against MultilingualIRLib and pybind11
target_link_libraries(ir_bindings PRIVATE MultilingualIRLib pybind11::pybind11)

# Include directories for LLVM and Clang
target_include_directories(ir_bindings PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${LLVM_INCLUDE_DIRS}
    ${CLANG_INCLUDE_DIRS}
)

# Set properties for the Python module
set_target_properties(ir_bindings PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# Add LLVM definitions
target_compile_definitions(ir_bindings PRIVATE ${LLVM_DEFINITIONS})
