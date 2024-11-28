"""Tests for Data Flow Analysis."""

import pytest
from lapair.core.ir import Function, BasicBlock, Instruction
from lapair.core.types import TypeSystem
from lapair.analysis.control_flow import ControlFlowGraph
from lapair.analysis.data_flow import ReachingDefinitionsAnalysis


def test_reaching_definitions_analysis():
    """Test the reaching definitions analysis."""
    # Create a simple type system
    type_system = TypeSystem()
    i32 = type_system.get_type("i32")

    # Create instructions (simulating variable definitions)
    inst_a1 = Instruction(type=i32, name="a")
    inst_b = Instruction(type=i32, name="b")
    inst_a2 = Instruction(type=i32, name="a")

    # Create basic blocks
    entry = BasicBlock(name="entry", instructions=[inst_a1])
    block1 = BasicBlock(name="block1", instructions=[inst_b])
    block2 = BasicBlock(name="block2", instructions=[inst_a2])
    exit_block = BasicBlock(name="exit", instructions=[])

    # Simulate control flow by setting successors and predecessors
    entry.successors.update({block1, block2})
    block1.predecessors.add(entry)
    block2.predecessors.add(entry)

    block1.successors.add(exit_block)
    block2.successors.add(exit_block)
    exit_block.predecessors.update({block1, block2})

    # Create a function and add blocks
    function = Function(
        name="test_function",
        return_type=i32,
        parameters=[],
        blocks=[entry, block1, block2, exit_block]
    )

    # Build the control flow graph
    cfg = ControlFlowGraph(function=function)

    # Perform reaching definitions analysis
    analysis = ReachingDefinitionsAnalysis(function=function, cfg=cfg)
    analysis.analyze()

    # Helper to extract variable names from definitions
    def defs_to_names(defs):
        return {(var_name, instr) for var_name, instr in defs}

    # Get the CFG nodes
    entry_node = cfg.nodes[entry]
    block1_node = cfg.nodes[block1]
    block2_node = cfg.nodes[block2]
    exit_node = cfg.nodes[exit_block]

    # Expected definitions at each node
    expected_in_entry = set()
    expected_out_entry = {("a", inst_a1)}

    expected_in_block1 = {("a", inst_a1)}
    expected_out_block1 = {("a", inst_a1), ("b", inst_b)}

    expected_in_block2 = {("a", inst_a1)}
    expected_out_block2 = {("a", inst_a2)}

    # At the exit block, both definitions of 'a' reach due to merging paths
    expected_in_exit = {("a", inst_a1), ("a", inst_a2), ("b", inst_b)}
    expected_out_exit = expected_in_exit.copy()

    # Actual definitions
    in_entry = defs_to_names(analysis.in_sets[entry_node])
    out_entry = defs_to_names(analysis.out_sets[entry_node])

    in_block1 = defs_to_names(analysis.in_sets[block1_node])
    out_block1 = defs_to_names(analysis.out_sets[block1_node])

    in_block2 = defs_to_names(analysis.in_sets[block2_node])
    out_block2 = defs_to_names(analysis.out_sets[block2_node])

    in_exit = defs_to_names(analysis.in_sets[exit_node])
    out_exit = defs_to_names(analysis.out_sets[exit_node])

    # Assertions
    assert in_entry == expected_in_entry, f"Entry IN set mismatch: got {in_entry}, expected {expected_in_entry}"
    assert out_entry == expected_out_entry, f"Entry OUT set mismatch: got {out_entry}, expected {expected_out_entry}"

    assert in_block1 == expected_in_block1, f"Block1 IN set mismatch: got {in_block1}, expected {expected_in_block1}"
    assert out_block1 == expected_out_block1, f"Block1 OUT set mismatch: got {out_block1}, expected {expected_out_block1}"

    assert in_block2 == expected_in_block2, f"Block2 IN set mismatch: got {in_block2}, expected {expected_in_block2}"
    assert out_block2 == expected_out_block2, f"Block2 OUT set mismatch: got {out_block2}, expected {expected_out_block2}"

    assert in_exit == expected_in_exit, f"Exit IN set mismatch: got {in_exit}, expected {expected_in_exit}"
    assert out_exit == expected_out_exit, f"Exit OUT set mismatch: got {out_exit}, expected {expected_out_exit}"
