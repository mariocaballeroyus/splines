#pragma once

#include <cstddef>
#include <vector>
#include <Eigen/Dense>


namespace splinekernel 
{


class SplineSurface
{
private:
    std::vector<double> knots_u_;
    std::vector<double> knots_v_;
    size_t degree_u_;
    size_t degree_v_;
    size_t n_bases_u_;
    size_t n_bases_v_;
public:

};


} // namespace splinekernel