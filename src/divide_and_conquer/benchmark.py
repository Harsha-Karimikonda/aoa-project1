"""
Benchmark harness for 2D Closest Pair Divide and Conquer Algorithm.
Evaluates empirical execution time across varying point sets, fits theoretical O(n log n),
and compares scaling against O(n^2) brute-force.
"""

import sys
import os
import time
import random
import gc
from typing import List, Tuple
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.divide_and_conquer.closest_pair import Point, closest_pair_dnc, brute_force_closest_pair
from src.utils.plotter import fit_and_plot_benchmark
import matplotlib.pyplot as plt

def generate_random_points(n: int, bounds: float = 10000.0) -> List[Point]:
    """Generates n points uniformly distributed in 2D Euclidean plane."""
    return [(random.uniform(0, bounds), random.uniform(0, bounds)) for _ in range(n)]

def run_benchmark():
    n_values_dnc = [100, 500, 1000, 2500, 5000, 10000, 25000, 50000]
    n_values_bf = [100, 300, 600, 1000, 2000, 3000]
    trials = 5

    mean_dnc = []
    std_dnc = []

    print("=" * 60)
    print("Executing 2D Closest Pair Divide-and-Conquer Benchmark")
    print("=" * 60)

    for n in n_values_dnc:
        durations = []
        for _ in range(trials):
            pts = generate_random_points(n)
            gc.disable()
            t0 = time.perf_counter()
            _ = closest_pair_dnc(pts)
            t1 = time.perf_counter()
            gc.enable()
            durations.append(t1 - t0)

        mean_t = float(np.mean(durations))
        std_t = float(np.std(durations))
        mean_dnc.append(mean_t)
        std_dnc.append(std_t)
        print(f"[D&C] n = {n:6d} | Mean: {mean_t:.6f}s | Std: {std_t:.6f}s")

    # Fit & plot D&C scaling curve
    fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../report/figures'))
    os.makedirs(fig_dir, exist_ok=True)
    dnc_prefix = os.path.join(fig_dir, 'divide_conquer_runtime')

    fit_and_plot_benchmark(
        n_values=n_values_dnc,
        empirical_times=mean_dnc,
        std_devs=std_dnc,
        title="2D Closest Pair D&C: Empirical vs. $\\mathcal{O}(n \\log n)$ Fit",
        output_prefix=dnc_prefix
    )

    # Brute Force Comparison Benchmark
    print("\nExecuting Brute-Force vs. D&C Comparative Benchmark")
    mean_bf = []
    dnc_comparison_times = []

    for n in n_values_bf:
        bf_runs = []
        dnc_runs = []
        for _ in range(trials):
            pts = generate_random_points(n)
            
            # Brute force timing
            gc.disable()
            t0 = time.perf_counter()
            _ = brute_force_closest_pair(pts)
            t1 = time.perf_counter()
            bf_runs.append(t1 - t0)

            # D&C timing
            t0 = time.perf_counter()
            _ = closest_pair_dnc(pts)
            t1 = time.perf_counter()
            gc.enable()
            dnc_runs.append(t1 - t0)

        m_bf = float(np.mean(bf_runs))
        m_dnc = float(np.mean(dnc_runs))
        mean_bf.append(m_bf)
        dnc_comparison_times.append(m_dnc)
        print(f"[Comparison] n = {n:5d} | Brute-force: {m_bf:.6f}s | D&C: {m_dnc:.6f}s | Speedup: {m_bf/m_dnc:.1f}x")

    # Generate comparative plot
    comp_fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=300)
    ax.plot(n_values_bf, mean_bf, 's-', color='#d62728', label='Brute-Force $\\mathcal{O}(n^2)$')
    ax.plot(n_values_bf, dnc_comparison_times, 'o-', color='#1f77b4', label='Divide-and-Conquer $\\mathcal{O}(n \\log n)$')
    ax.set_title("Runtime Comparison: D&C vs. Brute-Force Baseline", pad=10)
    ax.set_xlabel("Input Size ($n$)")
    ax.set_ylabel("Execution Time (seconds)")
    ax.grid(True, linestyle=':')
    ax.legend(frameon=True, loc='best')
    plt.tight_layout()

    comp_pdf = os.path.join(fig_dir, 'dnc_comparison.pdf')
    comp_png = os.path.join(fig_dir, 'dnc_comparison.png')
    plt.savefig(comp_pdf, bbox_inches='tight')
    plt.savefig(comp_png, bbox_inches='tight')
    plt.close()
    print(f"Comparison plot saved to:\n  - {comp_pdf}\n  - {comp_png}")

if __name__ == '__main__':
    run_benchmark()

