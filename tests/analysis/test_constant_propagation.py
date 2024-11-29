"""Tests for Constant Propagation Analysis."""

import pytest
from lapair.core.ir import Function, BasicBlock, Instruction, Constant
from lapair.core.types import TypeSystem
from lapair.analysis.control_flow import ControlFlowGraph
from lapair.analysis.data_flow import ConstantPropagationAnalysis


def test_constant_propagation_analysis():
    """Test the constant propagation analysis."""
    # Create a simple type system
    type_system = TypeSystem()
    i32 = type_system.get_type("i32")

    # Create constants
    const_1 = Constant(type=i32, value=1)
    const_2 = Constant(type=i32, value=2)

    # Create instructions simulating variable assignments and uses
    inst_a = Instruction(type=i32, name="a", operands=[const_1])  # a = 1
    inst_b = Instruction(type=i32, name="b", operands=[inst_a])    # b = a
    inst_c = Instruction(type=i32, name="c", operands=[const_2])  # c = 2
    inst_d = Instruction(type=i32, name="d", operands=[inst_b, inst_c])  # d = b + c (assuming an addition operation)
    inst_e = Instruction(type=i32, name="e")  # e = some unknown value

    # Create basic blocks
    entry = BasicBlock(name="entry", instructions=[inst_a, inst_b])
    block1 = BasicBlock(name="block1", instructions=[inst_c, inst_d])
    block2 = BasicBlock(name="block2", instructions=[inst_e])
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

    # Perform constant propagation analysis
    analysis = ConstantPropagationAnalysis(function=function, cfg=cfg)
    analysis.analyze()

    # Get the CFG nodes
    entry_node = cfg.nodes[entry]
    block1_node = cfg.nodes[block1]
    block2_node = cfg.nodes[block2]
    exit_node = cfg.nodes[exit_block]

    # Expected constants at each node
    expected_in_entry = {}
    expected_out_entry = {"a": "CONST", "b": "CONST"}

    expected_in_block1 = {"a": "CONST", "b": "CONST"}
    expected_out_block1 = {"a": "CONST", "b": "CONST", "c": "CONST", "d": "CONST"}

    expected_in_block2 = {"a": "CONST", "b": "CONST"}
    expected_out_block2 = {"a": "CONST", "b": "CONST", "e": "TOP"}  # 'e' is unknown

    # The meet operator for constant propagation is intersection, so at exit block,
    # variables that have different values along different paths become 'TOP' (unknown)
    expected_in_exit = {
        "a": "CONST",
        "b": "CONST",
        "c": "TOP",  # 'c' is only defined in block1
        "d": "TOP",  # 'd' is only defined in block1
        "e": "TOP",  # 'e' is only defined in block2
    }

    # Actual data from the analysis
    in_entry = analysis.in_sets[entry_node]
    out_entry = analysis.out_sets[entry_node]

    in_block1 = analysis.in_sets[block1_node]
    out_block1 = analysis.out_sets[block1_node]

    in_block2 = analysis.in_sets[block2_node]
    out_block2 = analysis.out_sets[block2_node]

    in_exit = analysis.in_sets[exit_node]
    out_exit = analysis.out_sets[exit_node]

    # Assertions
    assert out_entry == expected_out_entry, f"Entry OUT mismatch: got {out_entry}, expected {expected_out_entry}"
    assert in_block1 == expected_in_block1, f"Block1 IN mismatch: got {in_block1}, expected {expected_in_block1}"
    assert out_block1 == expected_out_block1, f"Block1 OUT mismatch: got {out_block1}, expected {expected_out_block1}"
    assert in_block2 == expected_in_block2, f"Block2 IN mismatch: got {in_block2}, expected {expected_in_block2}"
    assert out_block2 == expected_out_block2, f"Block2 OUT mismatch: got {out_block2}, expected {expected_out_block2}"
    assert in_exit == expected_in_exit, f"Exit IN mismatch: got {in_exit}, expected {expected_in_exit}"
