// Implementation of TaintAnalysis module

#include "TaintAnalysis.h"
#include <queue>

namespace analysis {

TaintAnalysis::TaintAnalysis() {
}

TaintAnalysis::~TaintAnalysis() {
}

void TaintAnalysis::analyze(const std::shared_ptr<ir::Node>& entryNode) {
    // Clear previous tainted variables
    taintedVariables_.clear();

    // Start taint propagation from the entry node
    propagateTaint(entryNode);
}

void TaintAnalysis::propagateTaint(const std::shared_ptr<ir::Node>& node) {
    if (!node) {
        return;
    }

    std::queue<std::shared_ptr<ir::Node>> worklist;
    std::unordered_set<std::string> visited;

    worklist.push(node);

    while (!worklist.empty()) {
        auto currentNode = worklist.front();
        worklist.pop();

        if (visited.find(currentNode->getId()) != visited.end()) {
            continue;
        }
        visited.insert(currentNode->getId());

        // Check if the current node introduces a taint
        if (currentNode->getProperty("tainted") == "true") {
            taintedVariables_.insert(currentNode->getId());
        }

        // Propagate taint to connected nodes
        for (const auto& edge : currentNode->getOutgoingEdges()) {
            auto targetNode = edge->getTarget();
            if (targetNode) {
                // If current node is tainted, taint the target node
                if (taintedVariables_.find(currentNode->getId()) != taintedVariables_.end()) {
                    targetNode->setProperty("tainted", "true");
                }
                worklist.push(targetNode);
            }
        }
    }
}

} // namespace analysis
