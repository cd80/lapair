"""Tests for Available Expressions Analysis."""

import pytest
from lapair.core.ir import (
    Function, BasicBlock, Instruction, Constant,
    AddInstruction, MulInstruction, AssignInstruction
)
from lapair.core.types import TypeSystem
from lapair.analysis.control_flow import ControlFlowGraph
from lapair.analysis.data_flow import AvailableExpressionsAnalysis, Expression


def test_available_expressions_analysis():
    """Test the available expressions analysis."""
    # Create a simple type system
    type_system = TypeSystem()
    i32 = type_system.get_type("i32")

    # Create constants and variables
    const_1 = Constant(type=i32, value=1)
    const_2 = Constant(type=i32, value=2)

    # Create instructions for expressions
    # x = 1
    inst_x = AssignInstruction(type=i32, name="x", operands=[const_1])
    # y = 2
    inst_y = AssignInstruction(type=i32, name="y", operands=[const_2])
    # a = x + y
    inst_a = AddInstruction(type=i32, name="a", operands=[inst_x, inst_y])
    # b = x * y
    inst_b = MulInstruction(type=i32, name="b", operands=[inst_x, inst_y])
    # x = 2 (kills expressions using x)
    inst_x2 = AssignInstruction(type=i32, name="x", operands=[const_2])
    # c = x + y (recomputes x+y with new x value)
    inst_c = AddInstruction(type=i32, name="c", operands=[inst_x2, inst_y])

    # Create basic blocks
    entry = BasicBlock(name="entry", instructions=[inst_x, inst_y])
    block1 = BasicBlock(name="block1", instructions=[inst_a, inst_b])
    block2 = BasicBlock(name="block2", instructions=[inst_x2, inst_c])
    exit_block = BasicBlock(name="exit", instructions=[])

    # Set up control flow
    entry.successors.update({block1, block2})
    block1.predecessors.add(entry)
    block2.predecessors.add(entry)

    block1.successors.add(exit_block)
    block2.successors.add(exit_block)
    exit_block.predecessors.update({block1, block2})

    # Create function
    function = Function(
        name="test_function",
        return_type=i32,
        parameters=[],
        blocks=[entry, block1, block2, exit_block]
    )

    # Build CFG and run analysis
    cfg = ControlFlowGraph(function=function)
    analysis = AvailableExpressionsAnalysis(function=function, cfg=cfg)
    analysis.analyze()

    # Get nodes
    entry_node = cfg.nodes[entry]
    block1_node = cfg.nodes[block1]
    block2_node = cfg.nodes[block2]
    exit_node = cfg.nodes[exit_block]

    # Create expected expressions
    add_expr = Expression(operator="add", operands=("x", "y"))
    mul_expr = Expression(operator="multiply", operands=("x", "y"))
    new_add_expr = Expression(operator="add", operands=("x", "y"))  # Same structure but after x is redefined

    # Expected available expressions at each point
    expected_in_entry = set()
    expected_out_entry = set()  # No expressions computed yet

    expected_in_block1 = set()
    expected_out_block1 = {add_expr, mul_expr}  # Both expressions computed and available

    expected_in_block2 = set()
    expected_out_block2 = {new_add_expr}  # Only new x+y available after x is redefined

    # At exit, expressions are only available if they reach from all predecessors
    # Since x was redefined in block2, no expressions are available at exit
    expected_in_exit = set()
    expected_out_exit = set()

    # Get actual results
    in_entry = analysis.in_sets[entry_node]
    out_entry = analysis.out_sets[entry_node]

    in_block1 = analysis.in_sets[block1_node]
    out_block1 = analysis.out_sets[block1_node]

    in_block2 = analysis.in_sets[block2_node]
    out_block2 = analysis.out_sets[block2_node]

    in_exit = analysis.in_sets[exit_node]
    out_exit = analysis.out_sets[exit_node]

    # Assertions
    assert in_entry == expected_in_entry, f"Entry IN mismatch: got {in_entry}, expected {expected_in_entry}"
    assert out_entry == expected_out_entry, f"Entry OUT mismatch: got {out_entry}, expected {expected_out_entry}"

    assert in_block1 == expected_in_block1, f"Block1 IN mismatch: got {in_block1}, expected {expected_in_block1}"
    assert out_block1 == expected_out_block1, f"Block1 OUT mismatch: got {out_block1}, expected {expected_out_block1}"

    assert in_block2 == expected_in_block2, f"Block2 IN mismatch: got {in_block2}, expected {expected_in_block2}"
    assert out_block2 == expected_out_block2, f"Block2 OUT mismatch: got {out_block2}, expected {expected_out_block2}"

    assert in_exit == expected_in_exit, f"Exit IN mismatch: got {in_exit}, expected {expected_in_exit}"
    assert out_exit == expected_out_exit, f"Exit OUT mismatch: got {out_exit}, expected {expected_out_exit}"
