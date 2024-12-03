#include "IRNode.h"
#include "IREdge.h"

using namespace ir;

Node::Node(const std::string& id) : id_(id) {}

Node::~Node() = default;

const std::string& Node::getId() const {
    return id_;
}

void Node::addIncomingEdge(const std::shared_ptr<Edge>& edge) {
    incomingEdges_.push_back(edge);
}

void Node::addOutgoingEdge(const std::shared_ptr<Edge>& edge) {
    outgoingEdges_.push_back(edge);
}

const std::vector<std::shared_ptr<Edge>>& Node::getIncomingEdges() const {
    return incomingEdges_;
}

const std::vector<std::shared_ptr<Edge>>& Node::getOutgoingEdges() const {
    return outgoingEdges_;
}
