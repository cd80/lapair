// Header file for TaintAnalysis module

#ifndef TAINT_ANALYSIS_H
#define TAINT_ANALYSIS_H

#include "IRNode.h"
#include "IREdge.h"
#include <unordered_set>
#include <memory>

namespace analysis {

class TaintAnalysis {
public:
    TaintAnalysis();
    virtual ~TaintAnalysis();

    void analyze(const std::shared_ptr<ir::Node>& entryNode);

private:
    void propagateTaint(const std::shared_ptr<ir::Node>& node);

    std::unordered_set<std::string> taintedVariables_;
};

} // namespace analysis

#endif // TAINT_ANALYSIS_H
