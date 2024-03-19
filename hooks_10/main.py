import sys

from puzzle_solver import PuzzleSolver
from l_shape_generator import LShapeGenerator

def get_intervals(lst, num):
    """
    Returns the intervals (start, end) for slicing a list into 4 roughly equal groups.
    These intervals indicate the range of indexes for each group.
    """
    length = len(lst)
    group_size = length // num
    remainder = length % num
    intervals = []
    start = 0

    for i in range(num):
        end = start + group_size + (1 if i < remainder else 0)
        intervals.append((start, end))
        start = end

    return intervals

def main():
    slice = int(sys.argv[1])
    total_slices = int(sys.argv[2])
    gen = LShapeGenerator()
    all_shapes = gen.get_all_shapes()
    all_intervals = get_intervals(all_shapes, total_slices)
    
    interval_start, interval_stop = all_intervals[slice]
    interval_shapes = all_shapes[interval_start:interval_stop]

    print("Total Shapes to process: ", len(interval_shapes))
    
    for i, shapes in enumerate(interval_shapes):
        print(f"Process: {slice} Shape: {i}")
        PuzzleSolver(l_shapes=shapes).solve()


if __name__ == "__main__":
    main()
