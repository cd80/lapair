#include "IREdge.h"
#include "IRNode.h"

using namespace ir;

Edge::Edge(const std::string& id, const std::shared_ptr<Node>& source, const std::shared_ptr<Node>& target)
    : id_(id), source_(source), target_(target) {}

Edge::~Edge() = default;

const std::string& Edge::getId() const {
    return id_;
}

std::shared_ptr<Node> Edge::getSource() const {
    return source_;
}

std::shared_ptr<Node> Edge::getTarget() const {
    return target_;
}
