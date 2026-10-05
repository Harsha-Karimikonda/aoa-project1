"""
Optimal Interval Scheduling Algorithm (Greedy EFT)
Applied Domain: Earth-Observing Satellite Mission Scheduling / Cloud VM Scheduling
"""

from typing import List, Tuple, NamedTuple

class Interval(NamedTuple):
    start: float
    finish: float
    request_id: str

def greedy_interval_scheduling(intervals: List[Interval]) -> List[Interval]:
    """
    Selects a maximum-cardinality mutually compatible subset of intervals using
    the Earliest Finish Time First (EFT) greedy strategy.

    Time Complexity:
        Sorting: O(n log n)
        Greedy Scan: O(n)
        Total: O(n log n)
    Space Complexity:
        O(n) auxiliary space for sorted list and result set.

    :param intervals: List of Interval objects
    :return: List of chosen non-overlapping intervals
    """
    if not intervals:
        return []

    # Sort intervals by finish time in non-decreasing order
    sorted_intervals = sorted(intervals, key=lambda x: x.finish)

    selected: List[Interval] = [sorted_intervals[0]]
    last_finish = sorted_intervals[0].finish

    for current in sorted_intervals[1:]:
        if current.start >= last_finish:
            selected.append(current)
            last_finish = current.finish

    return selected

