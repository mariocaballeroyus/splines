#pragma once

#include "basis.hpp"

#include <cstddef>
#include <vector>
#include <Eigen/Dense>

namespace splinekernel 
{

using MatXd = Eigen::MatrixXd;
using VecXd = Eigen::VectorXd;

class BSplineCurve
{
private:
    std::vector<double> knots_;
    size_t degree_;
    size_t n_bases_;
    VecXd eval_points_;
    MatXd basis_matrix_;
    
public:
    BSplineCurve(const std::vector<double>& knots, 
                 size_t degree, 
                 const VecXd& eval_points)
    : knots_(knots), 
      degree_(degree), 
      n_bases_(knots_.size() - degree - 1), 
      eval_points_(eval_points), 
      basis_matrix_(compute_bases(degree_, n_bases_, knots_, eval_points_))
    {}

    MatXd evaluate_curve(const MatXd& control_points) const
    {
        return basis_matrix_ * control_points;
    }

    // Getter functions
    std::vector<double> get_knot_vector() const { return knots_; }
    size_t get_degree() const { return degree_; }
    size_t get_n_bases() const { return n_bases_; }
    VecXd get_eval_points() const { return eval_points_; }
    MatXd get_basis() const { return basis_matrix_; }
};

} // namespace splinekernel