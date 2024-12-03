add_executable(MultilingualIR
    CPPParser.cpp
    IRNode.cpp
    IREdge.cpp
    IRGenerator.cpp
)

# Include directories
target_include_directories(MultilingualIR PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${LLVM_INCLUDE_DIRS}
    ${CLANG_INCLUDE_DIRS}
)

# Link against LLVM and Clang libraries
target_link_libraries(MultilingualIR
    ${LLVM_LIBS}
    clangTooling
    clangBasic
    clangASTMatchers
)

# Set C++ standard and other properties
set_target_properties(MultilingualIR PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# Add LLVM definitions
target_compile_definitions(MultilingualIR PUBLIC ${LLVM_DEFINITIONS})
