# Analysis of Algorithms — Project 1

This repository contains the source code, benchmarking suites, experimental data, and LaTeX report sources for **Project 1** in *Analysis of Algorithms*.

The project addresses two major algorithmic paradigms:
1. **Greedy Algorithm (50 pts):** Optimal Interval Scheduling for Satellite Observation & Cloud Resources.
2. **Divide-and-Conquer Algorithm (50 pts):** 2D Closest-Pair Computation for Air Traffic & Autonomous Drone Collision Avoidance.

---

## Quick Links

- **[Master Project Plan & Specification](PROJECT_PLAN.md)**: Full rubric mapping, problem abstractions, proof designs, and timeline.
- **[Source Code Directory](src/)**: Implementations of both algorithms and benchmarking scripts.
- **[LaTeX Report Directory](report/)**: Ready-to-sync files for Overleaf (IEEE Conference format).
- **[LLM Prompt Logs](logs/prompt_history.md)**: Audit trail of AI assistance for the required appendix.

---

## Repository Structure

```
.
├── PROJECT_PLAN.md          # Complete project specification and execution plan
├── README.md                # Repository overview and quick start guide
├── logs/                    # Audit logs for mandatory LLM appendix
│   └── prompt_history.md
├── report/                  # LaTeX publication manuscript (IEEEtran)
│   ├── figures/             # Generated empirical runtime plots
│   ├── sections/            # Modular LaTeX content chapters
│   ├── main.tex             # Main Overleaf entrypoint
│   └── references.bib       # BibTeX citations
└── src/                     # Algorithms and benchmarking harnesses
    ├── divide_and_conquer/  # 2D Closest Pair implementation and benchmarks
    ├── greedy/              # Interval Scheduling implementation and benchmarks
    └── utils/               # Plotting and curve-fitting utilities
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Recommended packages:
  ```bash
  pip install numpy scipy matplotlib
  ```

### Running the Benchmarks

```bash
# Run greedy scheduler benchmark & generate plots
python src/greedy/benchmark.py

# Run divide & conquer closest pair benchmark & generate plots
python src/divide_and_conquer/benchmark.py
```
