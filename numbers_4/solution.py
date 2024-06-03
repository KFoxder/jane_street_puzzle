import copy
from collections import deque
from functools import cache
import time
import utils

from validation_functions import (
    is_square,
    is_fibonacci_num,
    is_prime_raised_to_a_prime,
    is_sum_digits_7,
    is_multiple_of_37,
    is_palindrome_multiple_of_23,
    is_product_ends_in_1,
    is_multiple_of_88,
    is_1_more_than_palindrome,
    is_1_less_than_palindrome,
)

SHADED_VAL = utils.SHADED_VAL
SIZE = 11
LEFT = (0, -1)
RIGHT = (0, 1)

REGION_1 = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
REGION_2 = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1)]
REGION_3 = [
    (0, 3),
    (0, 4),
    (0, 5),
    (1, 4),
    (1, 5),
    (2, 3),
    (2, 4),
    (2, 5),
    (3, 3),
    (3, 4),
    (4, 2),
    (4, 3),
]
REGION_4 = [(0, 6), (0, 7), (1, 6), (2, 6)]
REGION_5 = [(3, 5), (3, 6), (4, 6)]
REGION_6 = [(1, 10), (2, 10), (3, 8), (3, 9), (3, 10), (4, 8), (4, 10)]
REGION_7 = [(5, 10)]
REGION_8 = [(4, 9), (5, 8), (5, 9), (6, 8), (6, 9), (6, 10), (7, 9)]
REGION_9 = [(9, 10), (10, 10)]
REGION_10 = [
    (6, 5),
    (6, 6),
    (7, 5),
    (7, 6),
    (8, 5),
    (8, 6),
    (9, 6),
    (10, 5),
    (10, 6),
    (10, 7),
]
REGION_11 = [(7, 2), (7, 4), (8, 2), (8, 3), (8, 4), (9, 1), (9, 2)]
REGION_12 = [
    (6, 0),
    (7, 0),
    (7, 1),
    (8, 0),
    (8, 1),
    (9, 0),
    (9, 3),
    (9, 4),
    (9, 5),
    (10, 0),
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 4),
]
REGION_13 = [
    (0, 8),
    (0, 9),
    (0, 10),
    (1, 7),
    (1, 8),
    (1, 9),
    (2, 7),
    (2, 8),
    (2, 9),
    (3, 7),
    (4, 4),
    (4, 5),
    (4, 7),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (5, 6),
    (5, 7),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 7),
    (7, 3),
    (7, 7),
    (7, 8),
    (7, 10),
    (8, 7),
    (8, 8),
    (8, 9),
    (8, 10),
    (9, 7),
    (9, 8),
    (9, 9),
    (10, 8),
    (10, 9),
]

GROUPS = [
    REGION_1,
    REGION_2,
    REGION_3,
    REGION_4,
    REGION_5,
    REGION_6,
    REGION_7,
    REGION_8,
    REGION_9,
    REGION_10,
    REGION_11,
    REGION_12,
    REGION_13,
]

VAL_FUNCTIONS = {
    0: is_square,
    1: is_1_more_than_palindrome,
    2: is_prime_raised_to_a_prime,
    3: is_sum_digits_7,
    4: is_fibonacci_num,
    5: is_square,
    6: is_multiple_of_37,
    7: is_palindrome_multiple_of_23,
    8: is_product_ends_in_1,
    9: is_multiple_of_88,
    10: is_1_less_than_palindrome,
}


@cache
def cell_to_group_id(row, col):
    for i, group in enumerate(GROUPS):
        if (row, col) in group:
            return i


def fill_group_in_row(matrix, row, col, group_id, val):
    """
    Fill all cells in the same row and group with the same value.
    """
    directions = [LEFT, RIGHT]
    queue = deque([(row, col)])
    seen = set()

    if matrix[row][col] == SHADED_VAL:
        return

    while queue:
        row, col = queue.popleft()
        matrix[row][col] = val
        seen.add((row, col))
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            # If we are out of bounds, skip.
            if (
                new_row < 0
                or new_row >= len(matrix)
                or new_col < 0
                or new_col >= len(matrix[0])
            ):
                continue
            # If we have already seen this cell, skip.
            if (new_row, new_col) in seen:
                continue
            # If the cell is shaded, skip.
            if matrix[new_row][new_col] == SHADED_VAL:
                continue
            # If the cell is not part of the group, skip.
            if cell_to_group_id(new_row, new_col) != group_id:
                continue
            # Otherwise we have found a cell in our group and should fill it.
            queue.append((new_row, new_col))


def get_possible_vals_for_cell(matrix, row, col):
    """
    Find all possible values for this cell.
    """
    directions = [LEFT, RIGHT]
    vals = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    group_id = cell_to_group_id(row, col)
    queue = deque([(row, col)])
    seen = set()

    while queue:
        row, col = queue.popleft()

        seen.add((row, col))
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            # If we have processed this cell, skip it.
            if (new_row, new_col) in seen:
                continue

            # If the cell has a left border that is the matrix edge
            # then remove the zero since we can't lead by zero.
            if new_col < 0:
                vals.discard(0)
                continue

            # If the cell is out of bounds, skip it.
            if new_row < 0 or new_row >= len(matrix) or new_col >= len(matrix[0]):
                continue

            # If the cell has a left border that is shaded
            # then remove the zero since we can't lead by zero.
            if matrix[new_row][new_col] == SHADED_VAL and (drow, dcol) == LEFT:
                vals.discard(0)
                continue

            # If we see a cell that has a value that is not part of our group,
            # remove it from the possible values.
            if (
                matrix[new_row][new_col] is not None
                and cell_to_group_id(new_row, new_col) != group_id
            ):
                vals.discard(matrix[new_row][new_col])
                continue

            # If we see a cell that is part of our group and is not shaded
            # add it to our queue to explore and find the edge of the group.
            if (
                matrix[new_row][new_col] != SHADED_VAL
                and cell_to_group_id(new_row, new_col) == group_id
            ):
                queue.append((new_row, new_col))
                continue

    return list(vals)


def can_shade_cell(matrix, row, col):
    """
    Checks whether we can shade this cell based on the surrounding cells.
    """
    # Check if there is a shaded cell above that is shaded.
    if row > 0 and matrix[row - 1][col] == SHADED_VAL:
        return False

    # Check if there is a shaded cell below that is shaded.
    if row < len(matrix) - 1 and matrix[row + 1][col] == SHADED_VAL:
        return False

    # If its the first cell from the left border
    # or last cell from the right border
    # we can shade it.
    if (
        col == 0
        and matrix[row][col + 1] != SHADED_VAL
        and matrix[row][col + 2] != SHADED_VAL
    ):
        return True

    if (
        col == len(matrix[0]) - 1
        and matrix[row][col - 1] != SHADED_VAL
        and matrix[row][col - 2] != SHADED_VAL
    ):
        return True

    # The col cannot be 1 or len(matrix) - 2 because it would create a single digit number.
    if col == 1 or col == len(matrix[0]) - 2:
        return False

    # Count number of empty spaces to the left. If there are more than 2, we can shade it.
    if (
        matrix[row][col - 1] == SHADED_VAL
        or matrix[row][col - 2] == SHADED_VAL
        or matrix[row][col + 1] == SHADED_VAL
        or matrix[row][col + 2] == SHADED_VAL
    ):
        return False

    return True


def check_row(matrix, row, cur_col):
    if cur_col == len(matrix[0]):
        completed_num = utils.get_last_num(matrix, row, cur_col - 1, move_left=True)
        row_validation_func = VAL_FUNCTIONS[row]
        if row_validation_func(completed_num):
            # If the last value is valid then we have found a solution for the row
            # and we return it.
            return [copy.copy(matrix[row])]
        # If the last value is not valid, we have not found a solution and return an empty list.
        return []
    else:
        # each column you can fill it with a number or shade it.
        # 1: See if it has already been filled. If it has just continue to the next column.
        # 2: If it has not been filled, get the possible values it can be filled with and fill via BFS.
        if matrix[row][cur_col] == SHADED_VAL:
            if cur_col != 0:
                # If we hit a shaded cell that isn't the first shaded cell that,
                # means we have completed either a number (and possibly a row)
                # so lets check to see if the number is correct before we procceed.
                completed_num = utils.get_last_num(matrix, row, cur_col - 1)
                row_validation_func = VAL_FUNCTIONS[row]
                if not row_validation_func(completed_num):
                    return []
                else:
                    return check_row(matrix, row, cur_col + 1)
            else:
                return check_row(matrix, row, cur_col + 1)
        elif matrix[row][cur_col] is not None:
            return check_row(matrix, row, cur_col + 1)
        else:
            solutions = []
            possible_vals = get_possible_vals_for_cell(matrix, row, cur_col)
            for val in possible_vals:
                group_id = cell_to_group_id(row, cur_col)
                fill_group_in_row(matrix, row, cur_col, group_id, val)
                solutions = solutions + check_row(matrix, row, cur_col + 1)

            fill_group_in_row(matrix, row, cur_col, group_id, None)
            return solutions


def get_solutions_for_row(matrix, row, col):
    if col == len(matrix[0]):
        # Check that it is possible to fill the row
        # with a valid solution before continuing to shade.
        solutions = check_row(matrix, row, 0)
        return solutions

    # Do not shade the cell and move on.
    solutions = get_solutions_for_row(matrix, row, col + 1)

    # Check if you can shade this cell.
    # if you can, shade it and call shade_cell on the next col.
    if can_shade_cell(matrix, row, col):
        matrix[row][col] = SHADED_VAL
        solutions = solutions + get_solutions_for_row(matrix, row, col + 1)
        matrix[row][col] = None

    return solutions


def find_solution(rows_to_solutions, matrix, row):
    # If we have gotten to this point we have succesfully found
    # a solution that satisifies all rows so we return it.
    if row == SIZE:
        return matrix

    solutions = rows_to_solutions[row]
    for solution in solutions:
        matrix[row] = solution
        if matrix_is_valid(matrix, row):
            solution = find_solution(rows_to_solutions, matrix, row + 1)
            # If we find a solution, break early and return it.
            if solution is not None:
                return solution

    return None


def matrix_is_valid(matrix, row_num):
    """
    Checks to see if the matrix is valid.

    1. Check that shaded sells are not adjacent to each other.
    2. Check that if a cell is filled, if the cell above it is not shaded and the same group that it is the same value.
    3. Check that if a cell is filled, if the cell above it is filled and the same group that it is not the same value.
    """
    if row_num == 0:
        return True

    for col in range(SIZE):
        cell_above_val = matrix[row_num - 1][col]
        cell_above_group_id = cell_to_group_id(row_num - 1, col)
        cell_val = matrix[row_num][col]

        if matrix[row_num][col] == SHADED_VAL:
            # If the cell above is shaded, return False since they can't touch.
            if cell_above_val == SHADED_VAL:
                return False
        elif cell_above_val == SHADED_VAL:
            continue
        else:
            group_id = cell_to_group_id(row_num, col)
            if cell_above_group_id == group_id and cell_above_val != cell_val:
                return False
            if cell_above_group_id != group_id and cell_above_val == cell_val:
                return False

    return True


if __name__ == "__main__":
    blank_matrix = utils.create_matrix(SIZE)

    # Mapping of row number to list of possible solutions for that row.
    rows_to_solutions = {}

    for row in range(SIZE):
        start_time = time.time()
        sols = get_solutions_for_row(blank_matrix, row, 0)
        rows_to_solutions[row] = sols
        print(f"Row: {row} | Num Solutions: {len(rows_to_solutions[row])}")
        end_time = time.time()
        print(f"Time to solve in seconds: {end_time-start_time}")
        print(f"Time to solve in minutes: {(end_time-start_time) / 60}")

    start_time = time.time()
    # Once we have all the possible solutions for each row we can iterate
    # over them and find the combination that is valid.
    matrix = find_solution(rows_to_solutions, blank_matrix, 0)
    ans = utils.get_answer(matrix)
    print(f"Answer: {ans}")
    utils.print_matrix(matrix)

    end_time = time.time()
    print(f"Time to solve in seconds: {end_time-start_time}")
    print(f"Time to solve in minutes: {(end_time-start_time) / 60}")
