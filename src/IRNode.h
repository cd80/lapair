#ifndef IR_NODE_H
#define IR_NODE_H

#include <string>
#include <vector>
#include <memory>
#include <unordered_map>

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

    // Methods for properties
    void setProperty(const std::string& key, const std::string& value);
    std::string getProperty(const std::string& key) const;

private:
    std::string id_;
    std::vector<std::shared_ptr<Edge>> incomingEdges_;
    std::vector<std::shared_ptr<Edge>> outgoingEdges_;

    std::unordered_map<std::string, std::string> properties_;
};

} // namespace ir

#endif // IR_NODE_H
