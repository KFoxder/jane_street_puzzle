import copy 

def print_matrix(matrix):
    print('------')
    for row in matrix:
        print(row)
    print('------')

counter = {
    "count": 0
}

solutions = []

LENGTH = 5

DIRECTIONS = [
    (-1, 0), # down
    (0, 1), # right
    (1, 0), # up
    (0, -1), # left
]

matrix = []


for i in range(LENGTH):
    new_row = []
    for x in range(LENGTH):
        new_row.append(0)
    matrix.append(new_row)


def matrix_to_list_of_lists(matrix):
    max_value = max(max(row) for row in matrix)
    value_lists = [[] for _ in range(max_value)]  # Adjusted to not include an index for 0
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            value_lists[value-1].append((i, j))  # Adjusted index to match value starting from 1
    return value_lists

def is_open_cell(row:int, col:int):
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[row]):
        return False
    if matrix[row][col] == 0:
        return True
    return False

def get_next_direction(cur_row:int, cur_col:int, cur_dir: tuple[int,int]) -> tuple[int, int]:
    index = DIRECTIONS.index(cur_dir)
    if index == 3:
        next_dir = DIRECTIONS[0]
    else:
        next_dir = DIRECTIONS[index+1]
    
    next_row, next_col = cur_row + next_dir[0], cur_col + next_dir[1]

    if is_open_cell(next_row, next_col):
        return next_dir
    
    return get_next_direction(cur_row, cur_col, next_dir)

def get_start_direction(row:int, col:int) -> tuple[int, int]:
    # If left is valid. Start by going right
    # otherwise start by going down. 
    # both are clockwise. 
    left_row, left_col = row, col - 1
    if left_col >= 0 and left_col < len(matrix[left_row]) and matrix[left_row][left_col] == 0:
        return DIRECTIONS[1]
    return DIRECTIONS[0]

def get_start_positions(matrix: list[list[int]]) -> list[tuple[int, int]]:
    # go line by line starting from the top
    # when you find the first open cell
    # you have found a corner. Keeping going
    # until you find the last valid cell
    # then calc distance and go down distance 
    # from each position so far. 
    first_found = None
    second_found = None

    for row in range(len(matrix)):
        found = False
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:
                found = True
                first_found = (row, col)
                second_found = (row, col)
                while col < len(matrix[row]) and matrix[row][col] == 0:
                    second_found = (row, col)
                    col += 1
                break
        if found:
            break


    # If first and second are the same then we found the last square possible. 
    if first_found[0] == second_found[0] and first_found[1] == second_found[1]:
        return [first_found]
    
    dist = second_found[1] - first_found[1]

    pos = [
        first_found,
        second_found,
        (first_found[0]+dist, first_found[1]),
        (second_found[0]+dist, second_found[1]),
    ]

    return pos


def fill_shapes(row, col, num_left, num, direction):
    if num == 1:
        new_row, new_col = get_start_positions(matrix)[0]
        matrix[new_row][new_col] = num
        counter["count"] += 1
        #print_matrix(matrix)
        m = copy.deepcopy(matrix)
        solutions.append((m, matrix_to_list_of_lists(m)))
        matrix[new_row][new_col] = 0
        return

    elif num_left == 0:
        # we finished filling the l shape for this num. Need to go lower. 
        start_positions = get_start_positions(matrix)
        new_num = num - 1
        new_num_left = (new_num * 2) - 1
        for new_row, new_col in start_positions:
            new_direction = get_start_direction(new_row, new_col)
            fill_shapes(new_row, new_col, new_num_left, new_num, new_direction)
    else:
        # mark cell since we know it is valid
        matrix[row][col] = num

        next_row = row + direction[0]
        next_col = col + direction[1]
        if is_open_cell(next_row, next_col):
            fill_shapes(next_row, next_col, num_left - 1, num, direction)
        else:

            new_direction = get_next_direction(row, col, direction)
            next_row = row + new_direction[0]
            next_col = col + new_direction[1]
            fill_shapes(next_row, next_col, num_left - 1, num, new_direction)
        # unmark cell after recursion
        matrix[row][col] = 0
    

def main():
    start_positions = get_start_positions(matrix)

    size = (LENGTH * 2) - 1 

    for row, col in start_positions:
        direction = get_start_direction(row, col)
        fill_shapes(row, col, size, LENGTH, direction)

    # This should be equal to 4 ^ (LENGTH -1)
    assert counter["count"] == (4 ** (LENGTH -1))
    assert len(solutions) == (4 ** (LENGTH -1))
    print(counter)
    return solutions


    

if __name__ == "__main__":
    main()