# src/CMakeLists.txt

# Create the executable and link it against the static library
add_executable(MultilingualIR
    CPPParser.cpp
)

target_link_libraries(MultilingualIR
    MultilingualIRLib
)

# Include directories for the executable
target_include_directories(MultilingualIR PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${LLVM_INCLUDE_DIRS}
    ${CLANG_INCLUDE_DIRS}
)

# Set properties for the executable
set_target_properties(MultilingualIR PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# Add LLVM definitions
target_compile_definitions(MultilingualIR PUBLIC ${LLVM_DEFINITIONS})

# Removed modifications to MultilingualIRLib to resolve CMake errors
