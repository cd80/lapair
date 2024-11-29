"""Tests for Live Variable Analysis."""

import pytest
from lapair.core.ir import Function, BasicBlock, Instruction
from lapair.core.types import TypeSystem
from lapair.analysis.control_flow import ControlFlowGraph
from lapair.analysis.data_flow import LiveVariableAnalysis


def test_live_variable_analysis():
    """Test the live variable analysis."""
    # Create a simple type system
    type_system = TypeSystem()
    i32 = type_system.get_type("i32")

    # Create instructions (simulating variable usage and definitions)
    # Instruction format: Instruction(type=i32, name="variable_name", operands=[])
    inst1 = Instruction(type=i32, name="a")  # Define 'a'
    inst2 = Instruction(type=i32, operands=[], name=None)  # Use 'a'
    inst2.operands.append(inst1)  # 'a' is used here
    inst3 = Instruction(type=i32, name="b")  # Define 'b'
    inst4 = Instruction(type=i32, operands=[inst3], name=None)  # Use 'b'
    inst5 = Instruction(type=i32, operands=[inst1], name=None)  # Use 'a' again

    # Create basic blocks
    entry = BasicBlock(name="entry", instructions=[inst1, inst2])
    block1 = BasicBlock(name="block1", instructions=[inst3, inst4])
    block2 = BasicBlock(name="block2", instructions=[inst5])
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

    # Perform live variable analysis
    analysis = LiveVariableAnalysis(function=function, cfg=cfg)
    analysis.analyze()

    # Helper to extract variable names from live variable sets
    def vars_to_names(var_set):
        return set(var_set)

    # Get the CFG nodes
    entry_node = cfg.nodes[entry]
    block1_node = cfg.nodes[block1]
    block2_node = cfg.nodes[block2]
    exit_node = cfg.nodes[exit_block]

    # Expected live variables at each node (IN and OUT sets)
    # Since live variable analysis is backward, we focus on IN sets
    expected_in_exit = set()
    expected_in_block1 = set()
    expected_in_block2 = {"a"}
    expected_in_entry = set()  # Corrected to set() since 'a' is defined before use

    # Actual IN sets from the analysis
    in_exit = vars_to_names(analysis.in_sets[exit_node])
    in_block1 = vars_to_names(analysis.in_sets[block1_node])
    in_block2 = vars_to_names(analysis.in_sets[block2_node])
    in_entry = vars_to_names(analysis.in_sets[entry_node])

    # Assertions
    assert in_exit == expected_in_exit, f"Exit IN set mismatch: got {in_exit}, expected {expected_in_exit}"
    assert in_block1 == expected_in_block1, f"Block1 IN set mismatch: got {in_block1}, expected {expected_in_block1}"
    assert in_block2 == expected_in_block2, f"Block2 IN set mismatch: got {in_block2}, expected {expected_in_block2}"
    assert in_entry == expected_in_entry, f"Entry IN set mismatch: got {in_entry}, expected {expected_in_entry}"
