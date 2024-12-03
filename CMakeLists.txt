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

# Include subdirectories
add_subdirectory(src)
add_subdirectory(tests)
