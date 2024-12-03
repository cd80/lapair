# CMake configuration for tests

# Enable testing
enable_testing()

# Include FetchContent module
include(FetchContent)

# Download and make GoogleTest available
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/heads/main.zip
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Download and add GoogleTest to the build
FetchContent_MakeAvailable(googletest)

# Include directories for headers
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/src/analysis
)

# Add test executable for IRNodeTest
add_executable(IRNodeTest IRNodeTest.cpp)
target_link_libraries(IRNodeTest gtest gtest_main MultilingualIRLib)
add_test(NAME IRNodeTest COMMAND IRNodeTest)

# Add test executable for IREdgeTest
add_executable(IREdgeTest IREdgeTest.cpp)
target_link_libraries(IREdgeTest gtest gtest_main MultilingualIRLib)
add_test(NAME IREdgeTest COMMAND IREdgeTest)

# Add test executable for TaintAnalysisTest
add_executable(TaintAnalysisTest TaintAnalysisTest.cpp)
target_link_libraries(TaintAnalysisTest gtest gtest_main MultilingualIRLib)
add_test(NAME TaintAnalysisTest COMMAND TaintAnalysisTest)

# Add test executable for SymbolicExecutionTest
add_executable(SymbolicExecutionTest SymbolicExecutionTest.cpp)
target_link_libraries(SymbolicExecutionTest gtest gtest_main MultilingualIRLib)
add_test(NAME SymbolicExecutionTest COMMAND SymbolicExecutionTest)

# Add test executable for ProgramSlicingTest
add_executable(ProgramSlicingTest ProgramSlicingTest.cpp)
target_link_libraries(ProgramSlicingTest gtest gtest_main MultilingualIRLib)
add_test(NAME ProgramSlicingTest COMMAND ProgramSlicingTest)
