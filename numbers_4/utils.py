SHADED_VAL = 'X'

def print_matrix(matrix):
    for row in matrix:
        for val in row:
            if val is None:
                print('-', end=' ')
                continue
            print(val, end=' ')
        print()
    print()

def create_matrix(n):
    matrix = []
    for i in range(n):
        matrix.append([None] * n)
    return matrix

def get_last_num(matrix, row, col, move_left=False):
    if move_left:
        while col >= 0 and matrix[row][col] == SHADED_VAL:
            col -= 1
    num = ""
    while col >= 0 and matrix[row][col] != SHADED_VAL:
        num = str(matrix[row][col]) + num
        col -= 1

    return int(num)

def get_row_nums(matrix, row):
    nums = []
    num = ""
    for val in matrix[row]:
        if val == SHADED_VAL and num != "":
            nums.append(int(num))
            num = ""
        elif val == SHADED_VAL:
            continue
        else:
            num += str(val)
    
    if num != "":
        nums.append(int(num))
        
    return nums

def get_answer(matrix):
    ans = 0
    for row_index in range(len(matrix)):
        row_nums = get_row_nums(matrix, row_index)
        for row_num in row_nums:
            ans += row_num
    return ans