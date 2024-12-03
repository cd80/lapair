import ir_bindings

def main():
    # Create nodes
    node_a = ir_bindings.Node("A")
    node_b = ir_bindings.Node("B")
    
    # Set properties
    node_a.setProperty("color", "red")
    node_b.setProperty("color", "blue")
    
    # Create edge
    edge = ir_bindings.Edge("edge1", node_a, node_b)
    edge.setProperty("weight", "5")
    
    # Add edges to nodes
    node_a.addOutgoingEdge(edge)
    node_b.addIncomingEdge(edge)
    
    # Print node properties
    print(f"Node A ID: {node_a.getId()}, Color: {node_a.getProperty('color')}")
    print(f"Node B ID: {node_b.getId()}, Color: {node_b.getProperty('color')}")
    
    # Print edge properties
    print(f"Edge ID: {edge.getId()}, Weight: {edge.getProperty('weight')}")
    print(f"Edge from {edge.getSource().getId()} to {edge.getTarget().getId()}")

if __name__ == "__main__":
    main()
