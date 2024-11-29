"""
Data Flow Analysis module for the LaPair framework.

This module provides classes and functions to perform data flow analyses
on the IR using the control flow graph.
"""

from __future__ import annotations

from typing import Dict, Set, Any, List, Optional, Tuple
import attr

from lapair.core.ir import Function, Instruction, Constant, Value
from lapair.analysis.control_flow import ControlFlowGraph, CFGNode


@attr.s(auto_attribs=True)
class DataFlowAnalysis:
    """Base class for data flow analyses."""
    function: Function
    cfg: ControlFlowGraph = attr.ib()
    in_sets: Dict[CFGNode, Any] = attr.Factory(dict)
    out_sets: Dict[CFGNode, Any] = attr.Factory(dict)

    def is_forward(self) -> bool:
        """Indicate whether the analysis is forward or backward."""
        return True  # Default to forward analysis

    def initialize(self):
        """Initialize in and out sets for each node."""
        for node in self.cfg.get_nodes():
            self.in_sets[node] = self.initial_data()
            self.out_sets[node] = self.initial_data()

    def initial_data(self) -> Any:
        """Provide the initial data set for analysis."""
        return {}

    def flow_function(self, node: CFGNode, data_set: Any) -> Any:
        """Data flow function for the analysis. Should be overridden by subclasses."""
        raise NotImplementedError

    def meet_operator(self, sets: List[Any]) -> Any:
        """Meet operator for the analysis (e.g., union, intersection). Should be overridden."""
        raise NotImplementedError

    def analyze(self):
        """Perform the data flow analysis using a worklist algorithm."""
        self.initialize()
        worklist = set(self.cfg.get_nodes())

        while worklist:
            node = worklist.pop()

            # For forward analysis, use predecessors; for backward, use successors
            if self.is_forward():
                neighbors = node.predecessors
            else:
                neighbors = node.successors

            # Compute the data set based on the neighbors
            if self.is_forward():
                neighbor_sets = [self.out_sets[pred] for pred in neighbors] if neighbors else [self.initial_data()]
                meet_result = self.meet_operator(neighbor_sets)
                self.in_sets[node] = meet_result
                old_out_set = self.out_sets[node]
                new_out_set = self.flow_function(node, meet_result)
                self.out_sets[node] = new_out_set
                if new_out_set != old_out_set:
                    worklist.update(node.successors)
            else:
                neighbor_sets = [self.in_sets[succ] for succ in neighbors] if neighbors else [self.initial_data()]
                meet_result = self.meet_operator(neighbor_sets)
                self.out_sets[node] = meet_result
                old_in_set = self.in_sets[node]
                new_in_set = self.flow_function(node, meet_result)
                self.in_sets[node] = new_in_set
                if new_in_set != old_in_set:
                    worklist.update(node.predecessors)


@attr.s(auto_attribs=True)
class ReachingDefinitionsAnalysis(DataFlowAnalysis):
    """Implementation of Reaching Definitions Analysis."""

    def flow_function(self, node: CFGNode, in_set: Set[Tuple[str, Instruction]]) -> Set[Tuple[str, Instruction]]:
        """Compute the out set for reaching definitions."""

        out_set = in_set.copy()

        # KILL set: definitions that are redefined in this node
        kill_set: Set[Tuple[str, Instruction]] = set()

        # GEN set: definitions generated in this node
        gen_set: Set[Tuple[str, Instruction]] = set()

        for instruction in node.block.instructions:
            if instruction.name:
                # Assuming instruction.name is the variable being defined
                var_name = instruction.name

                # Remove previous definitions of var_name from out_set (KILL)
                kill_set.update({d for d in out_set if d[0] == var_name})

                # Add the new definition to GEN set
                gen_set.add((var_name, instruction))

        # Apply KILL and GEN sets
        out_set.difference_update(kill_set)
        out_set.update(gen_set)

        return out_set

    def meet_operator(self, sets: List[Set[Tuple[str, Instruction]]]) -> Set[Tuple[str, Instruction]]:
        """Meet operator using union for reaching definitions."""
        result = set()
        for data_set in sets:
            result.update(data_set)
        return result


@attr.s(auto_attribs=True)
class LiveVariableAnalysis(DataFlowAnalysis):
    """Implementation of Live Variable Analysis."""

    def is_forward(self) -> bool:
        """Indicate that this is a backward analysis."""
        return False

    def flow_function(self, node: CFGNode, out_set: Set[str]) -> Set[str]:
        """Compute the in set for live variables."""
        in_set = out_set.copy()

        for instruction in reversed(node.block.instructions):
            # KILL: variables defined in this instruction
            if instruction.name:
                var_def = instruction.name
                in_set.discard(var_def)

            # GEN: variables used in this instruction
            used_vars = self.get_used_variables(instruction)
            in_set.update(used_vars)

        return in_set

    def meet_operator(self, sets: List[Set[str]]) -> Set[str]:
        """Meet operator using union for live variables."""
        result = set()
        for data_set in sets:
            result.update(data_set)
        return result

    @staticmethod
    def get_used_variables(instruction: Instruction) -> Set[str]:
        """Extract variables used by the instruction."""
        used_vars = set()
        for operand in instruction.operands:
            if isinstance(operand, Value) and operand.name:
                used_vars.add(operand.name)
        return used_vars


@attr.s(auto_attribs=True)
class ConstantPropagationAnalysis(DataFlowAnalysis):
    """Implementation of Constant Propagation Analysis."""

    TOP = 'TOP'
    CONST = 'CONST'

    def is_forward(self) -> bool:
        """Indicate that this is a forward analysis."""
        return True

    def initial_data(self) -> Dict[str, str]:
        """Initial data for each variable is TOP (unknown)."""
        return {}

    def flow_function(self, node: CFGNode, in_set: Dict[str, str]) -> Dict[str, str]:
        """Compute the out set for constant propagation analysis."""
        out_set = in_set.copy()

        # Track variables defined in this block
        defined_vars = set()

        for instruction in node.block.instructions:
            if instruction.name:
                defined_vars.add(instruction.name)
                # For simple assignments (single operand)
                if len(instruction.operands) == 1:
                    operand = instruction.operands[0]
                    if isinstance(operand, Constant):
                        out_set[instruction.name] = self.CONST
                    elif isinstance(operand, Instruction) and operand.name:
                        # Copy the constant status from the operand
                        operand_status = out_set.get(operand.name, in_set.get(operand.name, self.TOP))
                        out_set[instruction.name] = operand_status
                # For operations with multiple operands
                elif len(instruction.operands) > 1:
                    # Check if all operands are constant
                    all_const = True
                    for operand in instruction.operands:
                        if isinstance(operand, Constant):
                            continue
                        elif isinstance(operand, Instruction) and operand.name:
                            operand_status = out_set.get(operand.name, in_set.get(operand.name, self.TOP))
                            if operand_status != self.CONST:
                                all_const = False
                                break
                        else:
                            all_const = False
                            break
                    out_set[instruction.name] = self.CONST if all_const else self.TOP
                else:
                    # No operands means unknown value
                    out_set[instruction.name] = self.TOP

        # Preserve values from in_set for variables not defined in this block
        for var, value in in_set.items():
            if var not in defined_vars:
                out_set[var] = value

        return out_set

    def meet_operator(self, sets: List[Dict[str, str]]) -> Dict[str, str]:
        """Meet operator using intersection for constant propagation."""
        if not sets:
            return {}

        all_keys = set().union(*[s.keys() for s in sets])
        result = {}

        for key in all_keys:
            values = [s.get(key, self.TOP) for s in sets]
            first_value = values[0]
            if all(value == first_value for value in values):
                result[key] = first_value
            else:
                result[key] = self.TOP

        return result


@attr.s(auto_attribs=True)
class ExampleDataFlowAnalysis(DataFlowAnalysis):
    """Example implementation of a data flow analysis."""

    def flow_function(self, node: CFGNode, data_set: Set[Any]) -> Set[Any]:
        """Example flow function that simply copies the data_set."""
        # In a real analysis, this function would modify the data_set based on the instructions in the node
        return data_set.copy()

    def meet_operator(self, sets: List[Set[Any]]) -> Set[Any]:
        """Example meet operator using union."""
        result = set()
        for data_set in sets:
            result.update(data_set)
        return result
