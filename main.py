import copy
import shapes_creator
import sys
import time
import os
import random

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

def check_clue_is_valid(clue_cell, addition=0):
    cur_sum = sum_adj_cells(clue_cell[0], clue_cell[1])
    target = clues[clue_cell]
    if cur_sum + addition > target:
        return False
    return True

def get_cells(shape_index):
    return shapes['shapes'][shape_index]

def fill_shape(_, available_cells, num, nums_left, available_shape_indices):
    if nums_left > len(available_cells):
        # Not possilbe if there are less cells then number we have to fill.
        return False
    
    elif nums_left == 0 and num == 1:
        # We finished filling the shape. Check for validitiy.
        # 1. all one block
        # 2. at least one empty in 2x2 squares
        # TODO: Check here
        matrix_hash = get_hash_matrix(matrix)
        if matrix_hash not in solutions:
            # TODO: do final validations:
            # 1. All on shape
            # 2. Check that clues line up
            all_clues_valid, num_valid = check_all_clues_valid()
            
            if num_valid > (.75 * len(clues)):
                print_matrix(matrix)
                output_matrix_to_file(matrix, not_valid=True)

            if not all_clues_valid:
                return 
        
            # Set hash so we don't processs it again
            solutions.add(matrix_hash)

            print_matrix(matrix)
            output_matrix_to_file(matrix)
            
            counter["count"] += 1
            log(f'COUNT: {counter["count"]}')

        return True

    elif nums_left == 0:

        # we filled all the shapes for this block and need to move on.
        for i, shape_index in enumerate(available_shape_indices):
            new_num = num - 1
            new_avail_cells = get_cells(shape_index)

            new_avail_shape_indices = available_shape_indices[:i] + available_shape_indices[i+1:]

            fill_shape(_, new_avail_cells, new_num, new_num, new_avail_shape_indices)

    else:
        for i, cell in enumerate(available_cells):
            row = cell[0]
            col = cell[1]

            # TODO: CHeck if this breaks a clue. Meaning by placing the cell it would result in a larger than possible clue
            clue_cells = find_adj_clues(row, col)
            all_clues_valid = True
            for clue_cell in clue_cells:
                if not check_clue_is_valid(clue_cell, num):
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
            # time.sleep(1)

            # remove cell from available_ceels
            new_avail_cells = available_cells[i+1:]
            
            fill_shape(_, new_avail_cells, num, nums_left - 1, available_shape_indices)

            # Add it back after recursive call
            matrix[row][col] = 0
    
    return False


def get_start_shapes_indices(cur_shapes, num):

    if num == 9:
        points = [
            (1,7),
            (3,7),
            (2,8),
            (2,6),
        ]
    else:
        points = [
            (2,2),
            (4,2),
            (3,1),
            (3,3)
        ]

    all_indices = []
    start_indices = []
    for index, list_points in enumerate(cur_shapes):
        all_indices.append(index)
        for point in points:
            if point in list_points:
                start_indices.append(index)

    assert len(start_indices) == 4

    return all_indices, start_indices

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
    random.shuffle(slice_shapes)

    print("TOTAL: ", len(slice_shapes))
    print(f"Start: {start} Stop: {stop}")
    
    for i, item in enumerate(slice_shapes):
        print('FORM: ', i + start)
        
        m, cur_shapes = item

        shapes['shapes'] = cur_shapes

        # print_matrix(m)
        
        all_shape_indices, start_shape_indices = get_start_shapes_indices(cur_shapes, LENGTH)

        for shape_index in start_shape_indices:
            available_cells = get_cells(shape_index)
            num = LENGTH  # Example number to fill
            nums_left = num  # Example number of shapes left to fill
            new_avail_shape_indices = all_shape_indices[:shape_index] + all_shape_indices[shape_index+1:]
            
            fill_shape(shape_index, available_cells, num, nums_left, new_avail_shape_indices)


if __name__ == "__main__":
    main()