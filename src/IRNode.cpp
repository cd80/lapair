// Implementation of Node class methods

#include "IRNode.h"

namespace ir {

Node::Node(const std::string& id)
    : id_(id) {
}

Node::~Node() { }

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

// Implement setProperty method
void Node::setProperty(const std::string& key, const std::string& value) {
    properties_[key] = value;
}

// Implement getProperty method
std::string Node::getProperty(const std::string& key) const {
    auto it = properties_.find(key);
    if (it != properties_.end()) {
        return it->second;
    } else {
        return "";
    }
}

} // namespace ir
