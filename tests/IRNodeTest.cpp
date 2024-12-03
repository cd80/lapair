// Unit test for IRNode class

#include "IRNode.h"
#include "IREdge.h"
#include <gtest/gtest.h>
#include <memory>

using namespace ir;

TEST(IRNodeTest, ConstructorTest) {
    Node node("test_node");
    EXPECT_EQ(node.getId(), "test_node");
    EXPECT_TRUE(node.getIncomingEdges().empty());
    EXPECT_TRUE(node.getOutgoingEdges().empty());
}

TEST(IRNodeTest, AddIncomingEdgeTest) {
    auto node = std::make_shared<Node>("node");
    auto sourceNode = std::make_shared<Node>("source");
    auto edge = std::make_shared<Edge>("edge1", sourceNode, node);
    node->addIncomingEdge(edge);

    auto incomingEdges = node->getIncomingEdges();
    EXPECT_EQ(incomingEdges.size(), 1);
    EXPECT_EQ(incomingEdges[0]->getId(), "edge1");
    EXPECT_EQ(incomingEdges[0]->getSource(), sourceNode);
    EXPECT_EQ(incomingEdges[0]->getTarget(), node);
}

TEST(IRNodeTest, AddOutgoingEdgeTest) {
    auto node = std::make_shared<Node>("node");
    auto targetNode = std::make_shared<Node>("target");
    auto edge = std::make_shared<Edge>("edge2", node, targetNode);
    node->addOutgoingEdge(edge);

    auto outgoingEdges = node->getOutgoingEdges();
    EXPECT_EQ(outgoingEdges.size(), 1);
    EXPECT_EQ(outgoingEdges[0]->getId(), "edge2");
    EXPECT_EQ(outgoingEdges[0]->getSource(), node);
    EXPECT_EQ(outgoingEdges[0]->getTarget(), targetNode);
}

TEST(IRNodeTest, MultipleEdgesTest) {
    auto node = std::make_shared<Node>("node");
    auto nodeA = std::make_shared<Node>("nodeA");
    auto nodeB = std::make_shared<Node>("nodeB");

    auto edge1 = std::make_shared<Edge>("edge1", nodeA, node);
    auto edge2 = std::make_shared<Edge>("edge2", node, nodeB);

    node->addIncomingEdge(edge1);
    node->addOutgoingEdge(edge2);

    EXPECT_EQ(node->getIncomingEdges().size(), 1);
    EXPECT_EQ(node->getOutgoingEdges().size(), 1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
