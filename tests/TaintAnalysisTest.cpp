// Unit test for TaintAnalysis class

#include "analysis/TaintAnalysis.h"
#include "IRNode.h"
#include "IREdge.h"
#include <gtest/gtest.h>
#include <memory>

using namespace analysis;
using namespace ir;

TEST(TaintAnalysisTest, BasicPropagationTest) {
    // Create nodes
    auto nodeA = std::make_shared<Node>("A");
    auto nodeB = std::make_shared<Node>("B");
    auto nodeC = std::make_shared<Node>("C");

    // Create edges
    auto edgeAB = std::make_shared<Edge>("edgeAB", nodeA, nodeB);
    auto edgeBC = std::make_shared<Edge>("edgeBC", nodeB, nodeC);

    // Add edges to nodes
    nodeA->addOutgoingEdge(edgeAB);
    nodeB->addIncomingEdge(edgeAB);
    nodeB->addOutgoingEdge(edgeBC);
    nodeC->addIncomingEdge(edgeBC);

    // Taint starting node
    nodeA->setProperty("tainted", "true");

    // Perform taint analysis
    TaintAnalysis taintAnalysis;
    taintAnalysis.analyze(nodeA);

    // Verify that taint has propagated
    EXPECT_EQ(nodeA->getProperty("tainted"), "true");
    EXPECT_EQ(nodeB->getProperty("tainted"), "true");
    EXPECT_EQ(nodeC->getProperty("tainted"), "true");
}

TEST(TaintAnalysisTest, NoPropagationTest) {
    // Create nodes
    auto nodeA = std::make_shared<Node>("A");
    auto nodeB = std::make_shared<Node>("B");

    // Create edge
    auto edgeAB = std::make_shared<Edge>("edgeAB", nodeA, nodeB);

    // Add edges to nodes
    nodeA->addOutgoingEdge(edgeAB);
    nodeB->addIncomingEdge(edgeAB);

    // No taint on starting node
    nodeA->setProperty("tainted", "false");

    // Perform taint analysis
    TaintAnalysis taintAnalysis;
    taintAnalysis.analyze(nodeA);

    // Verify that taint has not propagated
    EXPECT_EQ(nodeA->getProperty("tainted"), "false");
    EXPECT_EQ(nodeB->getProperty("tainted"), "");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
