// Python bindings for IRNode and IREdge classes using pybind11

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "IRNode.h"
#include "IREdge.h"

namespace py = pybind11;
using namespace ir;

PYBIND11_MODULE(ir_bindings, m) {
    py::class_<Node, std::shared_ptr<Node>>(m, "Node")
        .def(py::init<const std::string&>())
        .def("getId", &Node::getId)
        .def("addIncomingEdge", &Node::addIncomingEdge)
        .def("addOutgoingEdge", &Node::addOutgoingEdge)
        .def("getIncomingEdges", &Node::getIncomingEdges)
        .def("getOutgoingEdges", &Node::getOutgoingEdges)
        .def("setProperty", &Node::setProperty)
        .def("getProperty", &Node::getProperty);

    py::class_<Edge, std::shared_ptr<Edge>>(m, "Edge")
        .def(py::init<const std::string&, const std::shared_ptr<Node>&, const std::shared_ptr<Node>&>())
        .def("getId", &Edge::getId)
        .def("getSource", &Edge::getSource)
        .def("getTarget", &Edge::getTarget)
        .def("setProperty", &Edge::setProperty)
        .def("getProperty", &Edge::getProperty);
}
