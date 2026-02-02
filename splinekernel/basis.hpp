#pragma once

#include <cstddef>
#include <vector>
#include <cmath>
#include <Eigen/Dense>


namespace splinekernel 
{

using MatXd = Eigen::MatrixXd;
using VecXd = Eigen::VectorXd;


/// @brief Recursive Cox-de Boor evaluation of B-spline basis function
/// @param t Parameter value
/// @param i Basis function index
/// @param p Polynomial degree of the B-spline
/// @param knots Knot vector
/// @return Value of the B-spline basis function at t
double evaluate_bspline_basis(double t,
                             size_t i, 
                             size_t p,
                             const std::vector<double>& knot_vector);

MatXd compute_bases(size_t degree,
                    size_t n_bases,
                    const std::vector<double>& knots,
                    const VecXd& eval_points
                    );


} // namespace splinekernel