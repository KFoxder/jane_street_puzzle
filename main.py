import copy
import shapes_creator
import sys
import time
import os
import random
import cProfile

LENGTH = shapes_creator.LENGTH

SMS_COMMAND = """
osascript -e 'tell application "Messages"
    launch
    repeat while (count of windows) is 0
    end repeat
    set a to first account whose service type = SMS and enabled is true
    set p to participant "2158373121" of a
    send "Found Matrix" to p
    -- properties of p
end tell'
"""

matrix = []

for i in range(LENGTH):
    new_row = []
    for x in range(LENGTH):
        new_row.append(0)
    matrix.append(new_row)

shapes = {
    'shapes': []
}

cache = {
    "cache": set()
}

squares = [
        [
            # upper left square
            (-1, -1), # top left
            (-1, 0), # top
            (0, -1) # left
        ],
        [
            # upper right square
            (-1, 1), # top right
            (-1, 0), # top
            (0, 1) # right
        ],
        [
            # bottom right square
            (1, 1), # bottom right
            (1, 0), # bottom
            (0, 1) # right
        ],
        [
            # bottom left square
            (1, -1), # bottom left
            (1, 0), # bottom
            (0, -1) # left
        ],
    ]

clues = shapes_creator.CLUES

solutions = set()

counter = {
    "count": 0
}

logging = True

def log(msg):
    if not logging:
        return
    print(msg)

def output_matrix_to_file(matrix, not_valid=False):
    slice = int(sys.argv[1])
    if not_valid:
        file_name = os.path.join(os.path.dirname(__file__), f'matrix-possible-{slice}.txt')
    else:
        file_name = os.path.join(os.path.dirname(__file__), f'matrix-{slice}.txt')
    with open(file_name, 'a') as file:
        for row in matrix:
            file.write(' '.join(str(cell) for cell in row) + '\n')
        file.write('---------\n')

    if not_valid:
        return
    os.system(SMS_COMMAND)
    


def print_matrix(matrix):
    if not logging:
        return
    print('------')
    for row in matrix:
        print(row)
    print('------')

def get_hash_matrix(matrix):
    hash_matrix = ""
    for row in matrix:
        hash_matrix += "".join(str(cell) for cell in row)
    return hash(hash_matrix)

def check_all_clues_valid():
    count = 0
    for clue_coord, target in clues.items():
        r, c = clue_coord
        clue_sum = sum_adj_cells(r, c)
        if clue_sum != target:
            return False, count
        count += 1

    return True, count

def has_valid_squares(row, col):
    all_squares_valid = True
    for square_directions in squares:
        num_empty = 0
        full_square = True
        for direction in square_directions:
            r = row + direction[0]
            c = col + direction[1]
            if r < 0 or r >= LENGTH or c < 0 or c >= LENGTH:
                full_square = False
                break
            if matrix[r][c] == 0:
                num_empty += 1
                break
        
        if full_square and num_empty < 1:
            all_squares_valid = False
            break

    return all_squares_valid

def get_valid_adj_cells(row, col, clues_only=False):
    cells = []
    directions = [
        (-1, 0), # above
        (1, 0), # below
        (0, -1), # left
        (0, 1), # right
    ]
    for direction in directions:
        r = row + direction[0]
        c = col + direction[1]
        if r < 0 or r >= LENGTH or c < 0 or c >= LENGTH:
            continue
        
        if clues_only:
            if (r,c) in clues:
                cells.append((r,c))
        else:
            cells.append((r,c))

    return cells

def sum_adj_cells(row, col):
    sum = 0
    adj_cells = get_valid_adj_cells(row, col)
    for r, c in adj_cells:
        sum += matrix[r][c]

    return sum

def find_adj_clues(row, col):
    adj_clue_cells = get_valid_adj_cells(row, col, clues_only=True)
    return adj_clue_cells

def check_clue_is_valid(clue_cell, addition, new_row, new_col):
    sum = 0
    num_empty_cells = 0
    adj_cells = get_valid_adj_cells(clue_cell[0], clue_cell[1])
    for r, c in adj_cells:
        sum += matrix[r][c]
        if matrix[r][c] == 0:
            num_empty_cells += 1

    target = clues[clue_cell]
    new_sum = (sum + addition)
    if new_sum > target:
        return False
    elif num_empty_cells == 1 and new_sum != target:
        return False
    return True

def get_cells(shape_index):
    return shapes['shapes'][shape_index]

def fill_shape(shape_index, available_cells, num, nums_left, avail_nums):
    if nums_left > len(available_cells):
        # Not possilbe if there are less cells then number we have to fill.
        return False
    
    elif nums_left == 0 and shape_index == LENGTH - 1:
        # We finished filling the shape. Check for validitiy.
        # 1. all one block
        # 2. at least one empty in 2x2 squares
        # TODO: Check here

        # TODO: do final validations:
        # 1. All on shape
        # 2. Check that clues line up
        all_clues_valid, num_valid = check_all_clues_valid()
        
        if num_valid > (.75 * len(clues)):
            print_matrix(matrix)
            output_matrix_to_file(matrix, not_valid=True)

        if not all_clues_valid:
            return

        print_matrix(matrix)
        output_matrix_to_file(matrix)
        
        counter["count"] += 1
        log(f'COUNT: {counter["count"]}')

        return True

    elif nums_left == 0:
        # TODO: Once we have finished a block, check if we have finished for the tree
        # and then check that everything is still connected. 

        # we filled all the shapes for this block and need to move on.
        new_shape_index = shape_index + 1
        new_avail_cells = get_cells(new_shape_index)
        for i, new_num in enumerate(avail_nums):
            new_avail_nums = avail_nums[:i] + avail_nums[i+1:]
            fill_shape(new_shape_index, new_avail_cells, new_num, new_num, new_avail_nums)

    else:
        for i, cell in enumerate(available_cells):
            row = cell[0]
            col = cell[1]

            # TODO: CHeck if this breaks a clue. Meaning by placing the cell it would result in a larger than possible clue
            clue_cells = find_adj_clues(row, col)
            all_clues_valid = True
            for clue_cell in clue_cells:
                if not check_clue_is_valid(clue_cell, num, row, col):
                    #log(f'Cannot fill. Breaks clue cell: {clue_cell[0]} : {clue_cell[1]}')
                    all_clues_valid = False
                    break
            
            if not all_clues_valid:
                continue
                    
            # TODO: Check if this breaks 2x2 square rule
            valid_squares = has_valid_squares(row, col)
            if not valid_squares:
                continue

            # Place num in cell
            matrix[row][col] = num

            # print_matrix(matrix)
            # time.sleep(0.3)

            # remove cell from available_ceels
            new_avail_cells = available_cells[i+1:]
            fill_shape(shape_index, new_avail_cells, num, nums_left - 1, avail_nums)

            # Add it back after recursive call
            matrix[row][col] = 0
    
    return False


def main():
    def cutoff_intervals_for_four_groups(lst, num):
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

    slice = int(sys.argv[1])
    total_slices = int(sys.argv[2])
    all_shapes = shapes_creator.main()
    start, stop = cutoff_intervals_for_four_groups(all_shapes, total_slices)[slice]
    slice_shapes = all_shapes[start:stop]

    print("TOTAL: ", len(slice_shapes))
    print(f"Start: {start} Stop: {stop}")
    for i, item in enumerate(slice_shapes):
        print(f'SlICE: {slice} FORM: {i}' )
        
        m, cur_shapes = item

        shapes['shapes'] = cur_shapes
        
        shape_index = 0
        available_cells = get_cells(shape_index=shape_index)

        num = 1
        nums_left = 1
        avail_nums = list(range(2,LENGTH + 1))

        fill_shape(shape_index, available_cells, num, nums_left, avail_nums)


if __name__ == "__main__":
    main()
    # pypy3 main.py 0 1  0.22s user 0.04s system 63% cpu 0.407 total
    # pypy3 main.py 0 1  0.18s user 0.03s system 65% cpu 0.320 total