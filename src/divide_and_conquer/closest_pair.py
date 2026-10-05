"""
2D Closest Pair Algorithm (Divide and Conquer - Bentley-Shamos)
Applied Domain: Air Traffic Control (TCAS) and Autonomous Drone Fleet Collision Avoidance
"""

import math
from typing import List, Tuple, Optional

Point = Tuple[float, float]
ClosestPairResult = Tuple[float, Optional[Tuple[Point, Point]]]

def euclidean_dist(p1: Point, p2: Point) -> float:
    """Computes standard Euclidean distance in R^2."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def brute_force_closest_pair(points: List[Point]) -> ClosestPairResult:
    """
    Exhaustive O(n^2) closest pair search for base cases and baseline comparisons.
    """
    n = len(points)
    if n < 2:
        return float('inf'), None

    min_dist = float('inf')
    best_pair = None

    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_dist(points[i], points[j])
            if d < min_dist:
                min_dist = d
                best_pair = (points[i], points[j])

    return min_dist, best_pair

def closest_pair_dnc(points: List[Point]) -> ClosestPairResult:
    """
    Computes closest pair of points in O(n log n) using Divide and Conquer.
    Pre-sorts once by x and y coordinates to achieve T(n) = 2T(n/2) + O(n).
    """
    if len(points) < 2:
        return float('inf'), None

    # Pre-sort points
    px = sorted(points, key=lambda p: (p[0], p[1]))
    py = sorted(points, key=lambda p: (p[1], p[0]))

    return _closest_pair_rec(px, py)

def _closest_pair_rec(px: List[Point], py: List[Point]) -> ClosestPairResult:
    n = len(px)
    if n <= 3:
        return brute_force_closest_pair(px)

    mid = n // 2
    mid_point = px[mid]
    mid_x = mid_point[0]

    # Divide step
    qx = px[:mid]
    rx = px[mid:]

    # Partition py in O(n) preserving y-order
    # Use set membership on left partition coordinates
    left_set = set(qx)
    qy = [p for p in py if p in left_set]
    ry = [p for p in py if p not in left_set]

    # Conquer step
    dist_l, pair_l = _closest_pair_rec(qx, qy)
    dist_r, pair_r = _closest_pair_rec(rx, ry)

    if dist_l <= dist_r:
        delta, best_pair = dist_l, pair_l
    else:
        delta, best_pair = dist_r, pair_r

    # Combine step: vertical strip of width 2*delta
    strip = [p for p in py if abs(p[0] - mid_x) < delta]
    num_strip = len(strip)

    for i in range(num_strip):
        # By the Sparsity Lemma, check at most 7 subsequent points in y-order
        for j in range(i + 1, min(i + 8, num_strip)):
            if strip[j][1] - strip[i][1] >= delta:
                break
            d = euclidean_dist(strip[i], strip[j])
            if d < delta:
                delta = d
                best_pair = (strip[i], strip[j])

    return delta, best_pair

