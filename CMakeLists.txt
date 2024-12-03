cmake_minimum_required(VERSION 3.10)

project(MultilingualIRSystem LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set LLVM_DIR and Clang_DIR to find LLVM and Clang
set(LLVM_DIR "/opt/homebrew/opt/llvm/lib/cmake/llvm")
set(Clang_DIR "/opt/homebrew/opt/llvm/lib/cmake/clang")

# Find LLVM and Clang libraries
find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

# Include LLVM and Clang headers
include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${CLANG_INCLUDE_DIRS})

# Define the LLVM components we need
llvm_map_components_to_libnames(LLVM_LIBS support core irreader)

# Enable testing
enable_testing()

# Include FetchContent module
include(FetchContent)

# Download and make pybind11 available
FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/heads/master.zip
)

FetchContent_MakeAvailable(pybind11)

# Add the core library
add_library(MultilingualIRLib STATIC
    src/IRNode.cpp
    src/IREdge.cpp
    src/IRGenerator.cpp
    src/analysis/TaintAnalysis.cpp
    src/analysis/SymbolicExecution.cpp
    src/analysis/ProgramSlicing.cpp
)

# Include directories for the library
target_include_directories(MultilingualIRLib PUBLIC
    src
    ${LLVM_INCLUDE_DIRS}
    ${CLANG_INCLUDE_DIRS}
)

# Link LLVM and Clang libraries to the static library
target_link_libraries(MultilingualIRLib
    ${LLVM_LIBS}
    clangTooling
    clangBasic
    clangASTMatchers
)

# Set properties for the library
set_target_properties(MultilingualIRLib PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# Add LLVM definitions
target_compile_definitions(MultilingualIRLib PUBLIC ${LLVM_DEFINITIONS})

# Add subdirectories
add_subdirectory(src)
add_subdirectory(tests)
add_subdirectory(bindings)
