"""Python wrapper for BSpline C++ implementation."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from . import pysplinekernel  # type: ignore


class BSplineCurve:
    """Python wrapper for B-spline basis functions and curve evaluation."""

    def __init__(self, knots: list | np.ndarray, degree: int) -> None:
        """Initialize a B-spline with the knot vector and polynomial degree.
        
        Args:
            knots: Knot vector defining the spline
            degree: Polynomial degree of the B-spline
        """
        self._knot_vector: list[float] = knots if isinstance(knots, list) else knots.tolist()
        self._degree: int = degree
        self._n_bases: int = len(self._knot_vector) - degree - 1
    
    @property
    def knot_vector(self) -> list[float]: return self._knot_vector
    
    @property
    def degree(self) -> int: return self._degree
    
    @property
    def n_bases(self) -> int: return self._n_bases
    
    def compute_bases(self, eval_points: np.ndarray | list) -> np.ndarray:
        """Compute all basis functions at multiple evaluation points.
        
        Args:
            eval_points: Array of parameter values where to evaluate
            
        Returns:
            Basis matrix of shape (n_points, n_bases)
        """
        eval_points_array = np.asarray(eval_points)
        return pysplinekernel.compute_bases(
            self._degree, 
            self._n_bases, 
            self._knot_vector, 
            eval_points_array
        )
    
    def evaluate_curve(
        self, 
        control_points: np.ndarray, 
        eval_points: np.ndarray | list | None = None
    ) -> np.ndarray:
        """Evaluate the B-spline curve at given points.
        
        Args:
            control_points: Array of shape (n_bases, dim) containing control points
            eval_points: Parameter values where to evaluate. 
                If None, uses default linspace.
            
        Returns:
            Array of shape (n_points, dim) with curve points
        """
        if control_points.shape[0] != self._n_bases:
            raise ValueError(
                f"The number of control points ({control_points.shape[0]}) "
                f"must match number of basis functions ({self._n_bases})."
            )
        
        if eval_points is None:  # default linspace if not provided
            eval_points = np.linspace(self._knot_vector[self._degree], 
                                     self._knot_vector[-self._degree-1], 100)
        
        # Compute basis functions and multiply with control points
        basis_matrix = self.compute_bases(eval_points)
        return basis_matrix @ control_points


def create_bspline_curve(knots: list | np.ndarray, degree: int) -> BSplineCurve:
    """Create a B-spline curve with the given knot vector and degree.
    
    Args:
        knots: Knot vector defining the spline
        degree: Polynomial degree of the B-spline
    
    Returns:
        `BSplineCurve` object
    """
    return BSplineCurve(knots, degree)