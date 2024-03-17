import copy

class LShapeGenerator:
    """
    This class is in charge of generating the different L-Shape permuations for a matrix.
    """
    LENGTH = 9
    CLUES: dict[tuple[int, int], int] = {
        (0, 1): 18,
        (0, 6): 7,
        (1, 4): 12,
        (2, 2): 9,
        (2, 7): 31,
        (4, 1): 5,
        (4, 3): 11,
        (4, 5): 22,
        (4, 7): 22,
        (6, 1): 9,
        (6, 6): 19,
        (7, 4): 14,
        (8, 2): 22,
        (8, 7): 15,
    }
    DIRECTIONS: list[tuple[int, int]] = [
        (-1, 0),  # down
        (0, 1),  # right
        (1, 0),  # up
        (0, -1),  # left
    ]

    def __init__(self) -> None:
        self.valid_shapes: list[list[tuple[int, int]]] = []
        self.valid_matrices: list[list[list[int]]] = []

        # Create empty matrix
        self.matrix: list[list[int]] = []
        for _ in range(self.LENGTH):
            new_row = []
            for _ in range(self.LENGTH):
                new_row.append(0)
            self.matrix.append(new_row)

    def get_all_matrices(self) -> list[list[list[int]]]:
        start_positions = self._get_start_positions(self.matrix)

        size = (self.LENGTH * 2) - 1

        for row, col in start_positions:
            direction = self._get_start_direction(row, col)
            self._fill_shapes(row, col, size, self.LENGTH, direction)
            
        # This should be equal to 4 ^ (LENGTH -1)
        assert len(self.valid_matrices) == (4 ** (self.LENGTH - 1))

        return self.valid_matrices
    
    def get_all_shapes(self) -> list[list[list[tuple[int, int]]]]:
        start_positions = self._get_start_positions(self.matrix)

        size = (self.LENGTH * 2) - 1

        for row, col in start_positions:
            direction = self._get_start_direction(row, col)
            self._fill_shapes(row, col, size, self.LENGTH, direction)

        # This should be equal to 4 ^ (LENGTH -1)
        assert len(self.valid_shapes) == (4 ** (self.LENGTH - 1))

        return self.valid_shapes

    def _matrix_to_list_of_lists(self, matrix) -> list[list[tuple[int, int]]]:
        # These lists need to be in order of smallest to largerst L-Shape
        l_shapes = [[] for _ in range(self.LENGTH)]
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                coord = (i, j)
                # do not add a clue cell to the L-shape coordinates
                if coord in self.CLUES:
                    continue
                
                l_shapes[value - 1].append(
                    coord
                ) 
                
        return l_shapes

    def _is_open_cell(self, row: int, col: int):
        if (
            row < 0
            or row >= len(self.matrix)
            or col < 0
            or col >= len(self.matrix[row])
        ):
            return False
        if self.matrix[row][col] == 0:
            return True
        return False

    def _get_next_direction(
        self, cur_row: int, cur_col: int, cur_dir: tuple[int, int]
    ) -> tuple[int, int]:
        index = self.DIRECTIONS.index(cur_dir)
        if index == 3:
            next_dir = self.DIRECTIONS[0]
        else:
            next_dir = self.DIRECTIONS[index + 1]

        next_row, next_col = cur_row + next_dir[0], cur_col + next_dir[1]

        if self._is_open_cell(next_row, next_col):
            return next_dir

        return self._get_next_direction(cur_row, cur_col, next_dir)

    def _get_start_direction(self, row: int, col: int) -> tuple[int, int]:
        # If left is valid. Start by going right
        # otherwise start by going down.
        # both are clockwise.
        left_row, left_col = row, col - 1
        if (
            left_col >= 0
            and left_col < len(self.matrix[left_row])
            and self.matrix[left_row][left_col] == 0
        ):
            return self.DIRECTIONS[1]
        return self.DIRECTIONS[0]

    def _get_start_positions(self, matrix: list[list[int]]) -> list[tuple[int, int]]:
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
            (first_found[0] + dist, first_found[1]),
            (second_found[0] + dist, second_found[1]),
        ]

        return pos

    def _fill_shapes(
        self, row: int, col: int, num_left: int, num: int, direction: tuple[int, int]
    ) -> None:
        if num == 1:
            # If we have reached the last L-shape then we have completed this matrix.

            new_row, new_col = self._get_start_positions(self.matrix)[0]
            self.matrix[new_row][new_col] = num
            self.valid_matrices.append(copy.deepcopy(self.matrix))
            self.valid_shapes.append(self._matrix_to_list_of_lists(self.matrix))

            self.matrix[new_row][new_col] = 0
            return

        elif num_left == 0:
            # we finished filling the l shape for this num. Need to go lower.
            start_positions = self._get_start_positions(self.matrix)
            new_num = num - 1
            new_num_left = (new_num * 2) - 1
            for new_row, new_col in start_positions:
                new_direction = self._get_start_direction(new_row, new_col)
                self._fill_shapes(
                    new_row, new_col, new_num_left, new_num, new_direction
                )
        else:
            # mark cell since we know it is valid
            self.matrix[row][col] = num

            next_row = row + direction[0]
            next_col = col + direction[1]
            if self._is_open_cell(next_row, next_col):
                self._fill_shapes(next_row, next_col, num_left - 1, num, direction)
            else:
                new_direction = self._get_next_direction(row, col, direction)
                next_row = row + new_direction[0]
                next_col = col + new_direction[1]
                self._fill_shapes(next_row, next_col, num_left - 1, num, new_direction)
            # unmark cell after recursion
            self.matrix[row][col] = 0


def output_shapes_to_file(matrices: list[list[list[tuple[int, int]]]]) -> None:
    with open("all_shapes.txt", "w") as f:
        for matrix in matrices:
            for row in matrix:
                for i, value in enumerate(row):
                    if i == len(row) - 1:
                        f.write(f"{value}")
                    else:
                        f.write(f"{value} ")
                f.write(f"\n")
            f.write("\n")

            
if __name__ == "__main__":
    all_matrices = LShapeGenerator().get_all_matrices()
    output_shapes_to_file(all_matrices)
    