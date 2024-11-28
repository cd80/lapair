"""
Control Flow Analysis module for the LaPair framework.

This module provides the ControlFlowGraph class and associated functions to
build and analyze control flow graphs from the IR.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional
import attr

from lapair.core.ir import Function, BasicBlock


@attr.s(auto_attribs=True, eq=False)
class CFGNode:
    """Node in the control flow graph."""
    block: BasicBlock
    successors: Set[CFGNode] = attr.Factory(set)
    predecessors: Set[CFGNode] = attr.Factory(set)

    def __eq__(self, other: object) -> bool:
        """Check equality based on object identity."""
        return self is other

    def __hash__(self) -> int:
        """Hash based on object identity."""
        return id(self)


@attr.s(auto_attribs=True)
class ControlFlowGraph:
    """Control Flow Graph representing the flow of a function."""
    function: Function
    nodes: Dict[BasicBlock, CFGNode] = attr.Factory(dict)

    def __attrs_post_init__(self):
        """Initialize the CFG by building nodes and edges from the function."""
        self.build_cfg()

    def build_cfg(self):
        """Build the CFG from the function's basic blocks."""
        # Create CFG nodes
        for block in self.function.blocks:
            self.nodes[block] = CFGNode(block=block)

        # Link the nodes based on the IR's control flow
        for block in self.function.blocks:
            cfg_node = self.nodes[block]
            for successor in block.successors:
                successor_node = self.nodes[successor]
                cfg_node.successors.add(successor_node)
                successor_node.predecessors.add(cfg_node)

    def traverse(self, start_block: Optional[BasicBlock] = None) -> List[CFGNode]:
        """Traverse the CFG starting from the given block.

        Returns a list of CFGNodes in traversal order.
        """
        if start_block is None:
            start_block = self.function.blocks[0]
        visited = set()
        traversal_order = []
        stack = [self.nodes[start_block]]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            traversal_order.append(node)
            # Add successors to the stack
            stack.extend(node.successors - visited)
        return traversal_order

    def get_nodes(self) -> List[CFGNode]:
        """Get all nodes in the CFG."""
        return list(self.nodes.values())
