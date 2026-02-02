"""Module for plotting B-spline curves and basis functions."""

from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from .bspline import BSplineCurve


def plot_basis(
    spline: BSplineCurve,
    eval_points: np.ndarray | None = None,
    ax=None
):
    """Plot all B-spline basis functions.
    
    Args:
        spline: BSplineCurve object to plot basis functions for
        eval_points: Points where to evaluate. If None, uses default linspace.
        ax: Matplotlib axes to plot on. If None, creates new figure.
        
    Returns:
        Matplotlib axes object
    """
    if eval_points is None:
        eval_points = np.linspace(
            spline.knot_vector[spline.degree], 
            spline.knot_vector[-spline.degree-1],
            100
        )
    
    if ax is None:
        fig, ax = plt.subplots()
    
    basis_matrix = spline.compute_bases(eval_points)
    
    for i in range(spline.n_bases):
        ax.plot(eval_points, basis_matrix[:, i], label=f'N_{i},{spline.degree}')
    
    # Plot knots as vertical lines
    for knot in spline.knot_vector:
        ax.axvline(x=knot, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    
    ax.set_xlabel('Parameter t')
    ax.set_ylabel('Basis value')
    ax.set_title(f'B-spline Basis Functions (degree {spline.degree})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def plot_curve_2d(
    spline: BSplineCurve,
    control_points: np.ndarray, 
    eval_points: np.ndarray | None = None,
    ax=None
):
    """Plot a 2D B-spline curve with its control polygon.
    
    Args:
        spline: BSplineCurve object to plot
        control_points: Array of shape (n_bases, 2) containing 2D control points
        eval_points: Points where to evaluate. If None, uses default linspace.
        ax: Matplotlib axes to plot on. If None, creates new figure.
        
    Returns:
        Matplotlib axes object
    """
    curve_points = spline.evaluate_curve(control_points, eval_points)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot the B-spline curve
    ax.plot(curve_points[:, 0], curve_points[:, 1], 'b-', linewidth=2, label='B-spline curve')
    
    # Plot the control polygon
    ax.plot(control_points[:, 0], control_points[:, 1], 'ro--', linewidth=1, 
             markersize=8, label='Control polygon')
    
    # Label control points
    for i, (x, y) in enumerate(control_points):
        ax.text(x, y, f'  P{i}', fontsize=10, ha='left')
    
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'B-spline Curve (degree {spline.degree})')
    
    return ax