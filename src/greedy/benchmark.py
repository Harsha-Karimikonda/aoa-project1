"""
Benchmark harness for Greedy Interval Scheduling.
Evaluates empirical execution time across varying workload scales and fits theoretical O(n log n).
Reproducibility: Fixed PRNG seed (42), platform recording, and raw CSV logging.
"""

import sys
import os
import time
import random
import gc
import csv
import platform
from typing import List
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.greedy.scheduler import Interval, greedy_interval_scheduling
from src.utils.plotter import fit_and_plot_benchmark

BENCHMARK_SEED = 42

def generate_random_intervals(n: int, max_time: float = 100000.0, rng: random.Random = None) -> List[Interval]:
    """Generates n random intervals with uniform duration distribution using a deterministic RNG."""
    if rng is None:
        rng = random.Random(BENCHMARK_SEED)
    intervals = []
    for i in range(n):
        start = rng.uniform(0, max_time)
        duration = rng.uniform(1.0, 100.0)
        finish = start + duration
        intervals.append(Interval(start=start, finish=finish, request_id=f"req_{i}"))
    return intervals

def run_benchmark():
    n_values = [100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000]
    trials_per_n = 5

    mean_times = []
    std_devs = []
    raw_records = []

    platform_info = {
        "os": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }

    print("=" * 65)
    print("Executing Greedy Interval Scheduling Benchmark")
    print(f"Platform: {platform_info['os']} ({platform_info['machine']}) | Python: {platform_info['python_version']}")
    print(f"Reproducibility Seed: {BENCHMARK_SEED} | Trials per n: {trials_per_n}")
    print("=" * 65)

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../report/data'))
    os.makedirs(data_dir, exist_ok=True)

    # Initialize deterministic RNG for the entire benchmark sequence
    rng = random.Random(BENCHMARK_SEED)

    for n in n_values:
        trial_durations = []
        for trial in range(trials_per_n):
            data = generate_random_intervals(n, rng=rng)
            gc.disable()
            t_start = time.perf_counter()
            _ = greedy_interval_scheduling(data)
            t_end = time.perf_counter()
            gc.enable()
            elapsed = t_end - t_start
            trial_durations.append(elapsed)
            raw_records.append({"n": n, "trial": trial + 1, "time_seconds": elapsed})

        mean_t = float(np.mean(trial_durations))
        std_t = float(np.std(trial_durations))
        mean_times.append(mean_t)
        std_devs.append(std_t)
        print(f"n = {n:7d} | Mean: {mean_t:.6f}s | Std: {std_t:.6f}s")

    # Save raw trial data to CSV
    raw_csv_path = os.path.join(data_dir, 'greedy_raw_timings.csv')
    with open(raw_csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["n", "trial", "time_seconds"])
        writer.writeheader()
        writer.writerows(raw_records)

    # Save summary data to CSV
    summary_csv_path = os.path.join(data_dir, 'greedy_summary_timings.csv')
    with open(summary_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["n", "mean_time_seconds", "std_dev_seconds"])
        for n, m, s in zip(n_values, mean_times, std_devs):
            writer.writerow([n, m, s])

    print(f"Raw timing results saved to:\n  - {raw_csv_path}\n  - {summary_csv_path}")

    output_prefix = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../report/figures/greedy_runtime'))
    c_fit = fit_and_plot_benchmark(
        n_values=n_values,
        empirical_times=mean_times,
        std_devs=std_devs,
        title="Greedy Interval Scheduling: Empirical vs. $\\mathcal{O}(n \\log n)$ Fit",
        output_prefix=output_prefix
    )

if __name__ == '__main__':
    run_benchmark()
