#ifndef IR_EDGE_H
#define IR_EDGE_H

#include <string>
#include <memory>

namespace ir {

class Node; // Forward declaration

class Edge {
public:
    Edge(const std::string& id, const std::shared_ptr<Node>& source, const std::shared_ptr<Node>& target);
    virtual ~Edge();

    const std::string& getId() const;

    std::shared_ptr<Node> getSource() const;
    std::shared_ptr<Node> getTarget() const;

private:
    std::string id_;
    std::shared_ptr<Node> source_;
    std::shared_ptr<Node> target_;
};

} // namespace ir

#endif // IR_EDGE_H
