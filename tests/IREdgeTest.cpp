// Unit test for IREdge class

#include "IREdge.h"
#include "IRNode.h"
#include <gtest/gtest.h>
#include <memory>

using namespace ir;

TEST(IREdgeTest, ConstructorTest) {
    auto sourceNode = std::make_shared<Node>("source");
    auto targetNode = std::make_shared<Node>("target");
    Edge edge("edge1", sourceNode, targetNode);

    EXPECT_EQ(edge.getId(), "edge1");
    EXPECT_EQ(edge.getSource(), sourceNode);
    EXPECT_EQ(edge.getTarget(), targetNode);
}

TEST(IREdgeTest, SetAndGetPropertiesTest) {
    auto sourceNode = std::make_shared<Node>("source");
    auto targetNode = std::make_shared<Node>("target");
    Edge edge("edge2", sourceNode, targetNode);

    edge.setProperty("weight", "10");
    EXPECT_EQ(edge.getProperty("weight"), "10");

    edge.setProperty("label", "edge_label");
    EXPECT_EQ(edge.getProperty("label"), "edge_label");
}

TEST(IREdgeTest, NullNodesTest) {
    std::shared_ptr<Node> sourceNode = nullptr;
    std::shared_ptr<Node> targetNode = nullptr;
    Edge edge("edge3", sourceNode, targetNode);

    EXPECT_EQ(edge.getSource(), nullptr);
    EXPECT_EQ(edge.getTarget(), nullptr);
}

TEST(IREdgeTest, ConnectionTest) {
    auto sourceNode = std::make_shared<Node>("source");
    auto targetNode = std::make_shared<Node>("target");
    auto edge = std::make_shared<Edge>("edge4", sourceNode, targetNode);

    sourceNode->addOutgoingEdge(edge);
    targetNode->addIncomingEdge(edge);

    EXPECT_EQ(sourceNode->getOutgoingEdges().size(), 1);
    EXPECT_EQ(targetNode->getIncomingEdges().size(), 1);
    EXPECT_EQ(sourceNode->getOutgoingEdges()[0], edge);
    EXPECT_EQ(targetNode->getIncomingEdges()[0], edge);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
