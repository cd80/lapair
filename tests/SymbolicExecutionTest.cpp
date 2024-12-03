// Unit tests for the SymbolicExecution class

#include "analysis/SymbolicExecution.h"
#include "IRNode.h"
#include "IREdge.h"
#include <gtest/gtest.h>
#include <memory>

using namespace analysis;
using namespace ir;

TEST(SymbolicExecutionTest, BasicExecutionTest) {
    // Create nodes representing a simple control flow
    auto nodeA = std::make_shared<Node>("A");
    auto nodeB = std::make_shared<Node>("B");
    auto nodeC = std::make_shared<Node>("C");

    // Set up properties to simulate symbolic variables and operations
    nodeA->setProperty("instruction", "input");
    nodeB->setProperty("instruction", "add");
    nodeC->setProperty("instruction", "multiply");

    // Create edges to represent control flow
    auto edgeAB = std::make_shared<Edge>("edgeAB", nodeA, nodeB);
    auto edgeBC = std::make_shared<Edge>("edgeBC", nodeB, nodeC);

    // Add edges to nodes
    nodeA->addOutgoingEdge(edgeAB);
    nodeB->addIncomingEdge(edgeAB);
    nodeB->addOutgoingEdge(edgeBC);
    nodeC->addIncomingEdge(edgeBC);

    // Initialize symbolic execution
    SymbolicExecution symExec;
    symExec.execute(nodeA);

    // Verify that symbolic states have been processed
    EXPECT_EQ(nodeA->getProperty("symbolic_state"), "processed");
    EXPECT_EQ(nodeB->getProperty("symbolic_state"), "processed");
    EXPECT_EQ(nodeC->getProperty("symbolic_state"), "processed");
}

TEST(SymbolicExecutionTest, BranchExecutionTest) {
    // Create nodes representing branching control flow
    auto nodeStart = std::make_shared<Node>("Start");
    auto nodeIfTrue = std::make_shared<Node>("IfTrue");
    auto nodeIfFalse = std::make_shared<Node>("IfFalse");
    auto nodeEnd = std::make_shared<Node>("End");

    // Set up properties
    nodeStart->setProperty("instruction", "input");
    nodeIfTrue->setProperty("instruction", "add");
    nodeIfFalse->setProperty("instruction", "subtract");
    nodeEnd->setProperty("instruction", "output");

    // Create edges to represent control flow with a branch
    auto edgeStartTrue = std::make_shared<Edge>("edgeStartTrue", nodeStart, nodeIfTrue);
    auto edgeStartFalse = std::make_shared<Edge>("edgeStartFalse", nodeStart, nodeIfFalse);
    auto edgeTrueEnd = std::make_shared<Edge>("edgeTrueEnd", nodeIfTrue, nodeEnd);
    auto edgeFalseEnd = std::make_shared<Edge>("edgeFalseEnd", nodeIfFalse, nodeEnd);

    // Add edges to nodes
    nodeStart->addOutgoingEdge(edgeStartTrue);
    nodeStart->addOutgoingEdge(edgeStartFalse);
    nodeIfTrue->addIncomingEdge(edgeStartTrue);
    nodeIfTrue->addOutgoingEdge(edgeTrueEnd);
    nodeIfFalse->addIncomingEdge(edgeStartFalse);
    nodeIfFalse->addOutgoingEdge(edgeFalseEnd);
    nodeEnd->addIncomingEdge(edgeTrueEnd);
    nodeEnd->addIncomingEdge(edgeFalseEnd);

    // Initialize symbolic execution
    SymbolicExecution symExec;
    symExec.execute(nodeStart);

    // Verify that symbolic states have been processed
    EXPECT_EQ(nodeStart->getProperty("symbolic_state"), "processed");
    EXPECT_EQ(nodeIfTrue->getProperty("symbolic_state"), "processed");
    EXPECT_EQ(nodeIfFalse->getProperty("symbolic_state"), "processed");
    EXPECT_EQ(nodeEnd->getProperty("symbolic_state"), "processed");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
