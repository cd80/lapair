// Unit tests for the ProgramSlicing class

#include "analysis/ProgramSlicing.h"
#include "IRNode.h"
#include "IREdge.h"
#include <gtest/gtest.h>
#include <memory>
#include <unordered_set>

using namespace analysis;
using namespace ir;

TEST(ProgramSlicingTest, BackwardSliceTest) {
    // Create nodes
    auto nodeA = std::make_shared<Node>("A");
    auto nodeB = std::make_shared<Node>("B");
    auto nodeC = std::make_shared<Node>("C");
    auto nodeD = std::make_shared<Node>("D");

    // Create edges
    auto edgeAB = std::make_shared<Edge>("edgeAB", nodeA, nodeB);
    auto edgeBC = std::make_shared<Edge>("edgeBC", nodeB, nodeC);
    auto edgeCD = std::make_shared<Edge>("edgeCD", nodeC, nodeD);

    // Add edges to nodes
    nodeA->addOutgoingEdge(edgeAB);
    nodeB->addIncomingEdge(edgeAB);
    nodeB->addOutgoingEdge(edgeBC);
    nodeC->addIncomingEdge(edgeBC);
    nodeC->addOutgoingEdge(edgeCD);
    nodeD->addIncomingEdge(edgeCD);

    // Initialize ProgramSlicing
    ProgramSlicing slicer;

    // Compute backward slice from node D
    auto slice = slicer.computeSlice(nodeD);

    // Verify the slice contains nodes A, B, C, D
    EXPECT_EQ(slice.size(), 4);
    EXPECT_TRUE(slice.find(nodeA) != slice.end());
    EXPECT_TRUE(slice.find(nodeB) != slice.end());
    EXPECT_TRUE(slice.find(nodeC) != slice.end());
    EXPECT_TRUE(slice.find(nodeD) != slice.end());
}

TEST(ProgramSlicingTest, ForwardSliceTest) {
    // Create nodes
    auto nodeA = std::make_shared<Node>("A");
    auto nodeB = std::make_shared<Node>("B");
    auto nodeC = std::make_shared<Node>("C");
    auto nodeD = std::make_shared<Node>("D");

    // Create edges
    auto edgeAB = std::make_shared<Edge>("edgeAB", nodeA, nodeB);
    auto edgeAC = std::make_shared<Edge>("edgeAC", nodeA, nodeC);
    auto edgeCD = std::make_shared<Edge>("edgeCD", nodeC, nodeD);

    // Add edges to nodes
    nodeA->addOutgoingEdge(edgeAB);
    nodeA->addOutgoingEdge(edgeAC);
    nodeB->addIncomingEdge(edgeAB);
    nodeC->addIncomingEdge(edgeAC);
    nodeC->addOutgoingEdge(edgeCD);
    nodeD->addIncomingEdge(edgeCD);

    // Initialize ProgramSlicing
    ProgramSlicing slicer;

    // Compute forward slice from node A
    std::unordered_set<std::shared_ptr<Node>> slice;
    slicer.computeForwardSlice(nodeA, slice);

    // Verify the slice contains nodes A, B, C, D
    EXPECT_EQ(slice.size(), 4);
    EXPECT_TRUE(slice.find(nodeA) != slice.end());
    EXPECT_TRUE(slice.find(nodeB) != slice.end());
    EXPECT_TRUE(slice.find(nodeC) != slice.end());
    EXPECT_TRUE(slice.find(nodeD) != slice.end());
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
