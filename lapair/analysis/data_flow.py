"""
Data Flow Analysis module for the LaPair framework.

This module provides classes and functions to perform data flow analyses
on the IR using the control flow graph.
"""

from __future__ import annotations

from typing import Dict, Set, Any, List, Tuple
import attr

from lapair.core.ir import Function, Instruction
from lapair.analysis.control_flow import ControlFlowGraph, CFGNode


@attr.s(auto_attribs=True)
class DataFlowAnalysis:
    """Base class for data flow analyses."""
    function: Function
    cfg: ControlFlowGraph = attr.ib()
    in_sets: Dict[CFGNode, Set[Any]] = attr.Factory(dict)
    out_sets: Dict[CFGNode, Set[Any]] = attr.Factory(dict)

    def initialize(self):
        """Initialize in and out sets for each node."""
        for node in self.cfg.get_nodes():
            self.in_sets[node] = set()
            self.out_sets[node] = set()

    def flow_function(self, node: CFGNode, in_set: Set[Any]) -> Set[Any]:
        """Data flow function for the analysis. Should be overridden by subclasses."""
        raise NotImplementedError

    def meet_operator(self, out_sets: List[Set[Any]]) -> Set[Any]:
        """Meet operator for the analysis (e.g., union, intersection). Should be overridden."""
        raise NotImplementedError

    def analyze(self):
        """Perform the data flow analysis using a worklist algorithm."""
        self.initialize()
        worklist = set(self.cfg.get_nodes())

        while worklist:
            node = worklist.pop()

            # Compute the in set using the meet operator over predecessors' out sets
            predecessor_out_sets = [self.out_sets[pred] for pred in node.predecessors]
            in_set = self.meet_operator(predecessor_out_sets)
            self.in_sets[node] = in_set

            # Compute the out set using the flow function
            old_out_set = self.out_sets[node]
            new_out_set = self.flow_function(node, in_set)
            self.out_sets[node] = new_out_set

            if new_out_set != old_out_set:
                # If out set has changed, add successors to the worklist
                worklist.update(node.successors)


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

    def meet_operator(self, out_sets: List[Set[Tuple[str, Instruction]]]) -> Set[Tuple[str, Instruction]]:
        """Meet operator using union for reaching definitions."""
        result = set()
        for out_set in out_sets:
            result.update(out_set)
        return result


@attr.s(auto_attribs=True)
class ExampleDataFlowAnalysis(DataFlowAnalysis):
    """Example implementation of a data flow analysis."""

    def flow_function(self, node: CFGNode, in_set: Set[Any]) -> Set[Any]:
        """Example flow function that simply copies the in_set to out_set."""
        # In a real analysis, this function would modify the in_set based on the instructions in the node
        return in_set.copy()

    def meet_operator(self, out_sets: List[Set[Any]]) -> Set[Any]:
        """Example meet operator using union."""
        result = set()
        for out_set in out_sets:
            result.update(out_set)
        return result
