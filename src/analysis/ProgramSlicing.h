// Header file for ProgramSlicing module

#ifndef PROGRAM_SLICING_H
#define PROGRAM_SLICING_H

#include "IRNode.h"
#include "IREdge.h"
#include <memory>
#include <unordered_set>

namespace analysis {

class ProgramSlicing {
public:
    ProgramSlicing();
    virtual ~ProgramSlicing();

    std::unordered_set<std::shared_ptr<ir::Node>> computeSlice(const std::shared_ptr<ir::Node>& criterionNode);

    // Make computeForwardSlice public
    void computeForwardSlice(const std::shared_ptr<ir::Node>& node, std::unordered_set<std::shared_ptr<ir::Node>>& slice);

private:
    void computeBackwardSlice(const std::shared_ptr<ir::Node>& node, std::unordered_set<std::shared_ptr<ir::Node>>& slice);

    // Additional helper methods and data structures for program slicing
};

} // namespace analysis

#endif // PROGRAM_SLICING_H
