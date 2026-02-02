#include "basis.hpp"


namespace splinekernel 
{

double evaluate_bspline_basis(double t,
                              size_t i, 
                              size_t p,
                              const std::vector<double>& knots)
{
    double tolerance = 1e-12;
    
    if (p == 0) 
    {
        return (knots[i] <= t && t < knots[i + 1]) || 
               (std::abs(t - knots.back()) < tolerance &&
                std::abs(t - knots[i + 1]) < tolerance);
    }

    double result = 0.0;

    double n1 = t - knots[i];
    double d1 = knots[i + p] - knots[i];
    if (std::abs(d1) > tolerance) 
    {
        result += n1 / d1 * evaluate_bspline_basis(t, i, p - 1, knots);
    }

    double n2 = knots[i + p + 1] - t;
    double d2 = knots[i + p + 1] - knots[i + 1];
    if (std::abs(d2) > tolerance) 
    {
        result += n2 / d2 * evaluate_bspline_basis(t, i + 1, p - 1, knots);
    }

    return result;
}


MatXd compute_bases(size_t degree,
                    size_t n_bases,
                    const std::vector<double>& knots,
                    const VecXd& eval_points
                    ) 
{
    size_t n_points = eval_points.size();
    MatXd basis_matrix(n_points, n_bases);

    for (size_t j = 0; j < n_points; ++j) 
    {
        for (size_t i = 0; i < n_bases; ++i) 
        {
            basis_matrix(j, i) = evaluate_bspline_basis(eval_points(j), i, degree, knots);
        }
    }

    return basis_matrix;
}


} // namespace splinekernel