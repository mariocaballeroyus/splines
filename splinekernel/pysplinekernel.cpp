#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

#include "basis.hpp"
#include "curve.hpp"
//#include "surface.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pysplinekernel, m) {    

    // Expose basis computation functions directly
    m.def("compute_bases", &splinekernel::compute_bases,
          "Compute B-spline basis functions at evaluation points");
    
    m.def("evaluate_bspline_basis", &splinekernel::evaluate_bspline_basis,
          "Evaluate a single B-spline basis function");

    py::class_<splinekernel::BSplineCurve>(m, "BSplineCurve")
        .def(py::init<const std::vector<double>&, size_t, const splinekernel::VecXd&>())
        .def("evaluate_curve", &splinekernel::BSplineCurve::evaluate_curve)
        .def("get_eval_points", &splinekernel::BSplineCurve::get_eval_points)
        .def("get_knot_vector", &splinekernel::BSplineCurve::get_knot_vector)
        .def("get_degree", &splinekernel::BSplineCurve::get_degree)
        .def("get_n_bases", &splinekernel::BSplineCurve::get_n_bases)
        .def("get_basis", &splinekernel::BSplineCurve::get_basis);
    
}