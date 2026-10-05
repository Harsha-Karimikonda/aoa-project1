"""
Plotting and Curve-Fitting Utilities for Empirical Algorithm Verification.
Formatted for IEEE/ACM publication standards.
"""

import os
from typing import List, Tuple, Callable
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Configure matplotlib for publication styling
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'font.family': 'sans-serif',
    'lines.linewidth': 1.8,
    'grid.alpha': 0.4,
})

def n_log_n_model(n: np.ndarray, c: float) -> np.ndarray:
    """Theoretical O(n log n) scaling model."""
    return c * n * np.log2(n)

def n_squared_model(n: np.ndarray, c: float) -> np.ndarray:
    """Theoretical O(n^2) scaling model."""
    return c * (n ** 2)

def fit_and_plot_benchmark(
    n_values: List[int],
    empirical_times: List[float],
    title: str,
    output_prefix: str,
    theoretical_model: Callable = n_log_n_model,
    model_label: str = r"Fitted $\mathcal{O}(n \log n)$",
    std_devs: List[float] = None
) -> float:
    """
    Fits empirical timing data to theoretical complexity and generates publication-grade plots.

    :param n_values: Array of input sizes
    :param empirical_times: Mean wall-clock runtimes in seconds
    :param title: Plot title
    :param output_prefix: Filepath prefix for saving figures (without extension)
    :param theoretical_model: Theoretical model function for regression
    :param model_label: Label for fitted curve in legend
    :param std_devs: Standard deviations across repeated trials (optional)
    :return: Fitted scaling constant c
    """
    n_arr = np.array(n_values, dtype=float)
    t_arr = np.array(empirical_times, dtype=float)

    # Perform non-linear least squares fit
    popt, _ = curve_fit(theoretical_model, n_arr, t_arr)
    c_fit = popt[0]

    # Generate fine interpolation points for smooth curve
    n_fine = np.linspace(n_arr.min(), n_arr.max(), 300)
    t_fitted = theoretical_model(n_fine, c_fit)

    # Compute R^2 goodness of fit
    residuals = t_arr - theoretical_model(n_arr, c_fit)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((t_arr - np.mean(t_arr))**2)
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

    fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=300)

    # Plot empirical points
    if std_devs is not None and len(std_devs) == len(n_values):
        ax.errorbar(
            n_arr, t_arr, yerr=std_devs, fmt='o', color='#1f77b4',
            ecolor='#6baed6', elinewidth=1.5, capsize=3,
            label='Empirical Mean $\pm 1\sigma$'
        )
    else:
        ax.plot(n_arr, t_arr, 'o', color='#1f77b4', markersize=5, label='Empirical Measurements')

    # Plot fitted curve
    ax.plot(
        n_fine, t_fitted, '--', color='#d62728',
        label=f"{model_label} ($R^2 = {r_squared:.4f}$)"
    )

    ax.set_title(title, pad=10)
    ax.set_xlabel("Input Size ($n$)")
    ax.set_ylabel("Execution Time (seconds)")
    ax.grid(True, linestyle=':')
    ax.legend(frameon=True, loc='best')

    plt.tight_layout()

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_prefix), exist_ok=True)
    pdf_path = f"{output_prefix}.pdf"
    png_path = f"{output_prefix}.png"

    plt.savefig(pdf_path, bbox_inches='tight')
    plt.savefig(png_path, bbox_inches='tight')
    plt.close()

    print(f"Figures saved to:\n  - {pdf_path}\n  - {png_path}\n  (Fit constant c = {c_fit:.3e}, R^2 = {r_squared:.4f})")
    return c_fit

