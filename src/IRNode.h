#ifndef IR_NODE_H
#define IR_NODE_H

#include <string>
#include <vector>
#include <memory>

namespace ir {

class Edge; // Forward declaration

class Node {
public:
    explicit Node(const std::string& id);
    virtual ~Node();

    const std::string& getId() const;

    void addIncomingEdge(const std::shared_ptr<Edge>& edge);
    void addOutgoingEdge(const std::shared_ptr<Edge>& edge);

    const std::vector<std::shared_ptr<Edge>>& getIncomingEdges() const;
    const std::vector<std::shared_ptr<Edge>>& getOutgoingEdges() const;

private:
    std::string id_;
    std::vector<std::shared_ptr<Edge>> incomingEdges_;
    std::vector<std::shared_ptr<Edge>> outgoingEdges_;
};

} // namespace ir

#endif // IR_NODE_H
