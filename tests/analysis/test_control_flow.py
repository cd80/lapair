"""Tests for Control Flow Graph analysis."""

import pytest
from lapair.core.ir import Function, BasicBlock
from lapair.core.types import TypeSystem
from lapair.analysis.control_flow import ControlFlowGraph

def test_control_flow_graph():
    """Test building and traversing a control flow graph."""
    # Create a simple type system
    type_system = TypeSystem()
    i32 = type_system.get_type("i32")

    # Create basic blocks
    entry = BasicBlock(name="entry")
    if_true = BasicBlock(name="if_true")
    if_false = BasicBlock(name="if_false")
    exit_block = BasicBlock(name="exit")

    # Simulate control flow by setting successors and predecessors
    entry.successors.update({if_true, if_false})
    if_true.predecessors.add(entry)
    if_false.predecessors.add(entry)

    if_true.successors.add(exit_block)
    if_false.successors.add(exit_block)
    exit_block.predecessors.update({if_true, if_false})

    # Create a function and add blocks
    function = Function(
        name="test_function",
        return_type=i32,
        parameters=[],
        blocks=[entry, if_true, if_false, exit_block]
    )

    # Build the control flow graph
    cfg = ControlFlowGraph(function=function)

    # Get all CFG nodes
    nodes = cfg.get_nodes()

    # Assert that all basic blocks are represented in the CFG
    assert len(nodes) == 4
    block_names = {node.block.name for node in nodes}
    assert block_names == {"entry", "if_true", "if_false", "exit"}

    # Test traversal order
    traversal = cfg.traverse()
    traversal_names = [node.block.name for node in traversal]
    assert set(traversal_names) == {"entry", "if_true", "if_false", "exit"}

    # Check successors and predecessors
    entry_node = cfg.nodes[entry]
    assert len(entry_node.successors) == 2
    assert {node.block.name for node in entry_node.successors} == {"if_true", "if_false"}

    exit_node = cfg.nodes[exit_block]
    assert len(exit_node.predecessors) == 2
    assert {node.block.name for node in exit_node.predecessors} == {"if_true", "if_false"}
