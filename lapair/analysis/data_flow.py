"""
Data Flow Analysis module for the LaPair framework.

This module provides classes and functions to perform data flow analyses
on the IR using the control flow graph.
"""

from __future__ import annotations

from typing import Dict, Set, Any, List, Optional, Tuple, FrozenSet
import attr

from lapair.core.ir import (
    Function, Instruction, Constant, Value,
    AddInstruction, MulInstruction, AssignInstruction
)
from lapair.analysis.control_flow import ControlFlowGraph, CFGNode


@attr.s(frozen=True, eq=True)
class Expression:
    """Represents an expression in the program."""
    operator: str = attr.ib()
    operands: Tuple[str, ...] = attr.ib()

    # Map instruction types to operator names
    OPERATOR_MAP = {
        AddInstruction: 'add',
        MulInstruction: 'multiply',
        AssignInstruction: 'assign',
    }

    @classmethod
    def from_instruction(cls, instruction: Instruction) -> Optional[Expression]:
        """Create an Expression from an Instruction if possible."""
        # Only create expressions for operations with multiple operands
        if len(instruction.operands) <= 1:
            return None

        # Get the operator from the instruction type
        operator = cls.OPERATOR_MAP.get(instruction.__class__)
        if operator is None:
            return None  # Skip unsupported instruction types

        # Get operand names
        operand_names = []
        for operand in instruction.operands:
            if isinstance(operand, Instruction) and operand.name:
                operand_names.append(operand.name)
            elif isinstance(operand, Constant):
                # Include constants in the expression
                operand_names.append(f"const_{operand.value}")
            else:
                return None  # Skip expressions with unsupported operands

        if not operand_names:
            return None

        return cls(operator=operator, operands=tuple(sorted(operand_names)))


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
class AvailableExpressionsAnalysis(DataFlowAnalysis):
    """Implementation of Available Expressions Analysis."""
    var_versions: Dict[str, Dict[CFGNode, int]] = attr.Factory(dict)
    killed_vars: Dict[CFGNode, Set[str]] = attr.Factory(dict)

    def initialize(self):
        """Initialize analysis data structures."""
        super().initialize()
        self.var_versions = {}  # Reset version tracking
        self.killed_vars = {}  # Reset killed variables tracking

    def is_forward(self) -> bool:
        """Indicate that this is a forward analysis."""
        return True

    def initial_data(self) -> Set[Expression]:
        """Initial data is an empty set of expressions."""
        return set()

    def get_var_version(self, var: str, node: CFGNode) -> int:
        """Get the version of a variable at a specific node."""
        if var not in self.var_versions:
            self.var_versions[var] = {}
        return self.var_versions[var].get(node, 0)

    def increment_var_version(self, var: str, node: CFGNode):
        """Increment the version of a variable at a specific node."""
        if var not in self.var_versions:
            self.var_versions[var] = {}
        current_version = self.var_versions[var].get(node, 0)
        self.var_versions[var][node] = current_version + 1

    def flow_function(self, node: CFGNode, in_set: Set[Expression]) -> Set[Expression]:
        """Compute the out set for available expressions."""
        # Start with expressions from input
        out_set = in_set.copy()
        killed_vars = set()  # Variables that are modified in this block

        # First pass: collect killed variables
        for instruction in node.block.instructions:
            if instruction.name:
                killed_vars.add(instruction.name)

        # Store killed variables for this node
        self.killed_vars[node] = killed_vars

        # Remove expressions that use killed variables
        out_set = {expr for expr in out_set 
                  if not any(var in killed_vars for var in expr.operands)}

        # Second pass: add new expressions
        for instruction in node.block.instructions:
            # Try to create an expression from the instruction
            expr = Expression.from_instruction(instruction)
            if expr is not None:
                # Add the expression regardless of variable versions
                # The meet operator will handle version mismatches
                out_set.add(expr)

        return out_set

    def meet_operator(self, sets: List[Set[Expression]]) -> Set[Expression]:
        """Meet operator using intersection for available expressions."""
        if not sets:
            return set()
        if len(sets) == 1:
            return sets[0].copy()

        # Get all killed variables from all paths
        all_killed_vars = set()
        for node in self.cfg.get_nodes():
            if node in self.killed_vars:
                all_killed_vars.update(self.killed_vars[node])

        # For multiple predecessors, an expression is only available if:
        # 1. It's available from all predecessors
        # 2. None of its variables have been killed along any path
        result = sets[0].copy()
        for s in sets[1:]:
            # Only keep expressions that appear in all sets
            result = {expr for expr in result if expr in s}

        # Remove expressions that use any killed variables
        result = {expr for expr in result 
                 if not any(var in all_killed_vars for var in expr.operands)}

        return result


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
