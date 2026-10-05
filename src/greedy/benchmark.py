"""
Benchmark harness for Greedy Interval Scheduling.
Evaluates empirical execution time across varying workload scales and fits theoretical O(n log n).
"""

import sys
import os
import time
import random
import gc
from typing import List

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.greedy.scheduler import Interval, greedy_interval_scheduling
from src.utils.plotter import fit_and_plot_benchmark

def generate_random_intervals(n: int, max_time: float = 100000.0) -> List[Interval]:
    """Generates n random intervals with uniform duration distribution."""
    intervals = []
    for i in range(n):
        start = random.uniform(0, max_time)
        duration = random.exponential(50.0) if hasattr(random, 'exponential') else random.uniform(1, 100)
        finish = start + duration
        intervals.append(Interval(start=start, finish=finish, request_id=f"req_{i}"))
    return intervals

def run_benchmark():
    n_values = [100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000]
    trials_per_n = 5

    mean_times = []
    std_devs = []

    print("=" * 60)
    print("Executing Greedy Interval Scheduling Benchmark")
    print("=" * 60)

    for n in n_values:
        trial_durations = []
        for trial in range(trials_per_n):
            data = generate_random_intervals(n)
            gc.disable()
            t_start = time.perf_counter()
            _ = greedy_interval_scheduling(data)
            t_end = time.perf_counter()
            gc.enable()
            trial_durations.append(t_end - t_start)

        import numpy as np
        mean_t = float(np.mean(trial_durations))
        std_t = float(np.std(trial_durations))
        mean_times.append(mean_t)
        std_devs.append(std_t)
        print(f"n = {n:7d} | Mean: {mean_t:.6f}s | Std: {std_t:.6f}s")

    output_prefix = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../report/figures/greedy_runtime'))
    fit_and_plot_benchmark(
        n_values=n_values,
        empirical_times=mean_times,
        std_devs=std_devs,
        title="Greedy Interval Scheduling: Empirical vs. $\\mathcal{O}(n \\log n)$ Fit",
        output_prefix=output_prefix
    )

if __name__ == '__main__':
    run_benchmark()

