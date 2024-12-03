// Implementation of Edge class methods

#include "IREdge.h"
#include "IRNode.h"

namespace ir {

Edge::Edge(const std::string& id, const std::shared_ptr<Node>& source, const std::shared_ptr<Node>& target)
    : id_(id), source_(source), target_(target) {
}

Edge::~Edge() { }

const std::string& Edge::getId() const {
    return id_;
}

std::shared_ptr<Node> Edge::getSource() const {
    return source_;
}

std::shared_ptr<Node> Edge::getTarget() const {
    return target_;
}

// Implement setProperty method
void Edge::setProperty(const std::string& key, const std::string& value) {
    properties_[key] = value;
}

// Implement getProperty method
std::string Edge::getProperty(const std::string& key) const {
    auto it = properties_.find(key);
    if (it != properties_.end()) {
        return it->second;
    } else {
        return "";
    }
}

} // namespace ir
