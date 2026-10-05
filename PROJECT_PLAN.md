# Project 1: Algorithmic Problem Solving & Empirical Analysis

## Analysis of Algorithms (AOA) — Project Master Plan & Specification

---

## 1. Project Overview & Rubric Breakdown

This project requires solving two real-world problems using specific algorithmic paradigms, providing formal mathematical abstractions, theoretical analysis, proofs of correctness, problem-domain explanations, empirical validation, and a publication-quality LaTeX report conforming to ACM/IEEE standards.

### Grading Distribution (100 Points Total)

| Component | Points | Deliverable Requirements |
| :--- | :--- | :--- |
| **Problem 1: Greedy Algorithm** | **50 pts** | |
| 1.1 Real-World Problem Identification | 10 pts | Non-algorithms domain (e.g., Cloud Computing, Networks, Aerospace). Clear motivation and constraints. |
| 1.2 Mathematical Abstraction | 5 pts | Formal modeling using sets, graphs, trees, or metric spaces. |
| 1.3 Algorithmic Solution | 10 pts | Complete pseudocode / formal algorithm specification. |
| 1.4 Running Time Analysis | 5 pts | Formal asymptotic complexity derivation. |
| 1.5 Proof of Correctness | 10 pts | Rigorous mathematical proof (exchange argument or greedy-stays-ahead induction). |
| 1.6 Problem Domain Translation | 5 pts | Mapping algorithmic steps back to real-world domain operations. |
| 1.7 Empirical Verification | 5 pts | Benchmarking against theoretical bounds with experimental plots. |
| **Problem 2: Divide and Conquer** | **50 pts** | |
| 2.1 Real-World Problem Identification | 10 pts | Non-algorithms domain (e.g., Air Traffic Control, Robotics, Computational Geometry). |
| 2.2 Mathematical Abstraction | 5 pts | Formal modeling using coordinate spaces, metric sets, or partitions. |
| 2.3 Algorithmic Solution | 10 pts | Complete pseudocode / formal algorithm specification. |
| 2.4 Running Time Analysis | 5 pts | Recurrence relations solved via Master Theorem / recursion tree. |
| 2.5 Proof of Correctness | 10 pts | Mathematical induction proving correctness over all subproblems and merge steps. |
| 2.6 Problem Domain Translation | 5 pts | Mapping algorithmic steps back to real-world domain operations. |
| 2.7 Empirical Verification | 5 pts | Benchmarking against theoretical bounds with experimental plots. |
| **Report & Compliance Standards** | — | Typeset in LaTeX (Overleaf, IEEE/ACM template). Includes mandatory appendices: LLM prompt logs and reproducible source code. |

---

## 2. Selected Problems & Architectural Design

### Problem 1 (Greedy): Cloud / Satellite Resource Interval Scheduling
* **Domain:** Cloud Computing / Earth Observation Satellite Operations.
* **Operational Problem:** A low Earth orbit (LEO) satellite payload or a single high-performance cloud compute resource receives $n$ competing observation/task requests over an observation window. Each task $j$ has a designated request window $[s_j, f_j)$. The satellite cannot service two tasks simultaneously. The objective is to maximize total completed tasks (throughput).
* **Mathematical Abstraction:**
  * Given a finite ground set of open/half-open intervals $\mathcal{I} = \{I_1, I_2, \dots, I_n\}$, where $I_j = [s_j, f_j) \subset \mathbb{R}$ with $s_j < f_j$.
  * Two intervals $I_j, I_k$ are compatible if $I_j \cap I_k = \emptyset$ (i.e., $f_j \le s_k$ or $f_k \le s_j$).
  * **Objective:** Find an independent subset $S^* \subseteq \mathcal{I}$ of maximum cardinality $|S^*|$.
* **Algorithm:** Earliest Finish Time First (EFT).
* **Complexity:** $O(n \log n)$ time due to initial sorting; $O(n)$ selection pass. Space complexity: $O(n)$.
* **Proof of Correctness:** Exchange argument / "Greedy stays ahead" induction showing that at every step $k$, the greedy schedule finishes no later than any hypothetical optimal schedule $O$.

---

### Problem 2 (Divide & Conquer): Air Traffic Control & Autonomous Drone Collision Avoidance
* **Domain:** Avionics / Unmanned Aerial Vehicle (UAV) Fleet Coordination.
* **Operational Problem:** In high-density airspace or autonomous drone swarms, collision warning systems (TCAS) must monitor all $n$ aircraft in real time and compute the minimum spatial separation $\min_{i \neq j} d(p_i, p_j)$ to trigger proximity avoidance maneuvers before any pair breaches safe separation limits.
* **Mathematical Abstraction:**
  * Given a set of $n$ points in Euclidean space $P = \{p_1, p_2, \dots, p_n\} \subset \mathbb{R}^2$, where $p_i = (x_i, y_i)$.
  * Distance metric: Euclidean distance $d(p_i, p_j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$.
  * **Objective:** Identify pair $(p^*, q^*) \in P \times P$ such that $d(p^*, q^*) = \min_{p \neq q} d(p, q)$.
* **Algorithm:** 2D Closest Pair Divide-and-Conquer algorithm (Bentley–Shamos).
* **Complexity Analysis:**
  * Recurrence relation: $T(n) = 2T(n/2) + O(n)$.
  * By Master Theorem (Case 2: $a=2, b=2, d=1$), $T(n) = \Theta(n \log n)$.
* **Proof of Correctness:**
  * Base case ($n \le 3$): solved by exhaustive inspection.
  * Inductive step: Assumes left and right subproblems correctly identify $\delta_L, \delta_R$. The merge step tests points within the vertical strip of width $2\delta$ centered at dividing line $x = x_{mid}$ ($\delta = \min(\delta_L, \delta_R)$).
  * Sparsity Lemma: Any $\delta \times 2\delta$ rectangle in the strip can contain at most 6 (or 8) points with mutual distance $\ge \delta$, bounding strip comparisons to at most $7n = O(n)$.

---

## 3. Repository Directory Structure

```
aoa-project1/
├── README.md                           # Quickstart & overview
├── PROJECT_PLAN.md                     # This master document
├── report/                             # LaTeX paper files for Overleaf
│   ├── main.tex                        # Master document (IEEEtran conference format)
│   ├── references.bib                  # BibTeX bibliography
│   ├── figures/                        # High-resolution benchmark plots (PDF/PNG)
│   │   ├── greedy_runtime.pdf
│   │   ├── divide_conquer_runtime.pdf
│   │   └── dnc_comparison.pdf
│   └── sections/
│       ├── 01_introduction.tex
│       ├── 02_greedy.tex               # Sections 1.1 - 1.7
│       ├── 03_divide_conquer.tex       # Sections 2.1 - 2.7
│       ├── 04_conclusion.tex
│       ├── appendix_code.tex           # Source code listings
│       └── appendix_llm.tex            # LLM prompt and tool usage disclosures
├── src/                                # Reproducible Python code
│   ├── greedy/
│   │   ├── __init__.py
│   │   ├── scheduler.py                # Algorithm implementation
│   │   └── benchmark.py                # Timing harness & data generator
│   ├── divide_and_conquer/
│   │   ├── __init__.py
│   │   ├── closest_pair.py             # D&C + Brute force baseline
│   │   └── benchmark.py                # Timing harness & data generator
│   └── utils/
│       ├── __init__.py
│       └── plotter.py                  # Matplotlib formatting & theoretical curve fitting
└── logs/
    └── prompt_history.md               # Continuous audit log of AI interactions
```

---

## 4. Empirical Benchmarking Methodology

To fulfill the experimental validation requirement (5 pts per problem):

1. **Input Size Scaling:**
   - **Greedy:** $n \in [10^2, 10^3, 5\times10^3, 10^4, 5\times10^4, 10^5, 5\times10^5, 10^6]$.
   - **Divide & Conquer:** $n \in [10^2, 5\times10^2, 10^3, 5\times10^3, 10^4, 5\times10^4, 10^5]$. (Also benchmark brute-force $O(n^2)$ up to $n=10^4$ to empirically illustrate the algorithmic crossover).
2. **Measurement Protocol:**
   - High-resolution wall-clock timing using `time.perf_counter()`.
   - Perform 5 to 10 independent trials per input size to calculate the mean runtime and 95% confidence intervals / standard deviations.
   - Garbage collection disabled (`gc.disable()`) during timed loops to eliminate GC jitter.
3. **Curve Fitting:**
   - Fit measured empirical runtimes $t(n)$ to theoretical model $f(n) = c \cdot n \log_2 n$ using non-linear least squares (`scipy.optimize.curve_fit`).
   - Plot both empirical data points (with error bars) and the fitted theoretical curve on linear and log-log scales to verify asymptotic scaling.

---

## 5. LaTeX & Publication Guidelines

* **Template:** IEEE Conference format (`\documentclass[conference]{IEEEtran}`) or ACM SIGCONF (`\documentclass[sigconf]{acmart}`).
* **Tools:** Overleaf for collaborative authoring and compilation.
* **Appendices Required by Project Rules:**
  1. **Appendix A: Source Code:** Direct verbatim source listings with syntax highlighting using `listings`.
  2. **Appendix B: LLM Tool Usage Disclosure:** Complete audit table containing:
     - Tool/Model name (e.g., Claude 3.5 Sonnet, Gemini Pro, ChatGPT-4o).
     - Full verbatim prompt text.
     - Summary of intermediate output received.
     - Verification, critique, or bug corrections performed by the authors.

---

## 6. Execution Milestones & Task Breakdown (2-Person Group)

| Phase | Milestone | Primary Deliverable | Target Date |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Formulation & Architecture** | Complete problem specifications, mathematical models, pseudocode, repo scaffolding | Days 1–3 |
| **Phase 2** | **Core Implementation & Verification** | Python modules for both algorithms, unit tests verifying exact output against brute-force | Days 4–6 |
| **Phase 3** | **Empirical Benchmarking & Figures** | Scalability benchmarks, statistical curve fits, PDF plots for paper | Days 7–9 |
| **Phase 4** | **Proofs & Theoretical Exposition** | Complete inductive proofs, Master theorem derivation, domain translations | Days 10–11 |
| **Phase 5** | **LaTeX Report Drafting & Overleaf Sync** | Overleaf integration, conference layout, citations, code & LLM appendices | Days 12–14 |

