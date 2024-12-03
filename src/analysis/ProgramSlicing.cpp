// Implementation of ProgramSlicing module

#include "ProgramSlicing.h"

namespace analysis {

ProgramSlicing::ProgramSlicing() {
}

ProgramSlicing::~ProgramSlicing() {
}

std::unordered_set<std::shared_ptr<ir::Node>> ProgramSlicing::computeSlice(const std::shared_ptr<ir::Node>& criterionNode) {
    std::unordered_set<std::shared_ptr<ir::Node>> slice;
    computeBackwardSlice(criterionNode, slice);
    return slice;
}

void ProgramSlicing::computeBackwardSlice(const std::shared_ptr<ir::Node>& node, std::unordered_set<std::shared_ptr<ir::Node>>& slice) {
    if (!node || slice.find(node) != slice.end()) {
        return;
    }
    slice.insert(node);
    for (const auto& edge : node->getIncomingEdges()) {
        auto sourceNode = edge->getSource();
        computeBackwardSlice(sourceNode, slice);
    }
}

void ProgramSlicing::computeForwardSlice(const std::shared_ptr<ir::Node>& node, std::unordered_set<std::shared_ptr<ir::Node>>& slice) {
    if (!node || slice.find(node) != slice.end()) {
        return;
    }
    slice.insert(node);
    for (const auto& edge : node->getOutgoingEdges()) {
        auto targetNode = edge->getTarget();
        computeForwardSlice(targetNode, slice);
    }
}

} // namespace analysis
