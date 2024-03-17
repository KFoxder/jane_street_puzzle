import os

from l_shape_generator import LShapeGenerator


class PuzzleSolver:
    LENGTH = LShapeGenerator.LENGTH
    CLUES: dict[tuple[int, int], int] = LShapeGenerator.CLUES
    SQUARE_DIRECTIONS: list[list[tuple[int, int]]] = [
        [
            # upper left square
            (-1, -1),  # top left
            (-1, 0),  # top
            (0, -1),  # left
        ],
        [
            # upper right square
            (-1, 1),  # top right
            (-1, 0),  # top
            (0, 1),  # right
        ],
        [
            # bottom right square
            (1, 1),  # bottom right
            (1, 0),  # bottom
            (0, 1),  # right
        ],
        [
            # bottom left square
            (1, -1),  # bottom left
            (1, 0),  # bottom
            (0, -1),  # left
        ],
    ]

    def __init__(self, l_shapes: list[list[list[tuple[int, int]]]]) -> None:
        self.l_shapes = l_shapes
        # Create empty matrix
        self.matrix: list[list[int]] = []
        for _ in range(self.LENGTH):
            new_row = []
            for _ in range(self.LENGTH):
                new_row.append(0)
            self.matrix.append(new_row)

    def solve(self) -> None:
        # Always start with the smalles L-Shape which is 1 and work your way up to the larger L-Shapes
        available_cells = self._get_cells(shape_index=0)
        avail_nums = list(range(2, self.LENGTH + 1))
        self._fill_l_shape(
            l_shape_index=0,
            available_cells=available_cells,
            num=1,
            nums_left=1,
            avail_nums=avail_nums,
        )

    def _output_matrix_to_file(self, matrix: list[list[int]]) -> None:
        file_name = os.path.join(os.path.dirname(__file__), "matrix.txt")
        with open(file_name, "a") as file:
            for row in matrix:
                file.write(" ".join(str(cell) for cell in row) + "\n")
            file.write("---------\n")

    def _is_valid_cell(self, x, y, matrix) -> bool:
        return 0 <= x < self.LENGTH and 0 <= y < self.LENGTH and matrix[x][y] != 0

    def _dfs(self, x, y, matrix, visited):
        if not self._is_valid_cell(x, y, matrix) or visited[x][y]:
            return
        visited[x][y] = True  # Mark the cell as visited
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            self._dfs(new_x, new_y, matrix, visited)

    def _are_all_cells_contiguously_connected(self, matrix):
        visited = [[False for _ in range(self.LENGTH)] for _ in range(self.LENGTH)]
        start_found = False

        for i in range(9):
            for j in range(9):
                if matrix[i][j] != 0:
                    start_x, start_y = i, j
                    start_found = True
                    break
            if start_found:
                break

        if not start_found:
            return False

        self._dfs(start_x, start_y, matrix, visited)

        # Check if there's any filled cell that was not visited
        for i in range(self.LENGTH):
            for j in range(self.LENGTH):
                if matrix[i][j] != 0 and not visited[i][j]:
                    return False  # Found an unvisited filled cell

        return True  # All filled cells are contiguously connected

    def _are_clues_valid(self) -> bool:
        for clue_, target in self.CLUES.items():
            r, c = clue_
            clue_sum = self._sum_adj_cells(r, c)
            if clue_sum != target:
                return False
        return True

    def _has_valid_squares(self, row: int, col: int) -> bool:
        all_squares_valid = True
        for square_directions in self.SQUARE_DIRECTIONS:
            num_empty = 0
            full_square = True
            for direction in square_directions:
                r = row + direction[0]
                c = col + direction[1]
                if r < 0 or r >= self.LENGTH or c < 0 or c >= self.LENGTH:
                    full_square = False
                    break
                if self.matrix[r][c] == 0:
                    num_empty += 1
                    break

            if full_square and num_empty < 1:
                all_squares_valid = False
                break

        return all_squares_valid

    def _get_valid_adj_cells(self, row, col, clues_only=False):
        cells = []
        directions = [
            (-1, 0),  # above
            (1, 0),  # below
            (0, -1),  # left
            (0, 1),  # right
        ]
        for direction in directions:
            r = row + direction[0]
            c = col + direction[1]
            if r < 0 or r >= self.LENGTH or c < 0 or c >= self.LENGTH:
                continue

            if clues_only:
                if (r, c) in self.CLUES:
                    cells.append((r, c))
            else:
                cells.append((r, c))

        return cells

    def _sum_adj_cells(self, row, col):
        sum = 0
        adj_cells = self._get_valid_adj_cells(row, col)
        for r, c in adj_cells:
            sum += self.matrix[r][c]

        return sum

    def _find_adj_clues(self, row, col):
        adj_clue_cells = self._get_valid_adj_cells(row, col, clues_only=True)
        return adj_clue_cells

    def _clues_is_valid(self, clue_cell, addition) -> bool:
        sum = 0
        num_empty_cells = 0
        adj_cells = self._get_valid_adj_cells(clue_cell[0], clue_cell[1])
        for r, c in adj_cells:
            sum += self.matrix[r][c]
            if self.matrix[r][c] == 0:
                num_empty_cells += 1

        target = self.CLUES[clue_cell]
        new_sum = sum + addition
        if new_sum > target:
            return False
        elif num_empty_cells == 1 and new_sum != target:
            return False
        return True

    def _get_cells(self, shape_index: int) -> list[list[tuple[int, int]]]:
        return self.l_shapes[shape_index]

    def _fill_l_shape(
        self,
        l_shape_index: int,
        available_cells: list[tuple[int, int]],
        num: int,
        nums_left: int,
        avail_nums: list[int],
    ) -> None:
        if nums_left > len(available_cells):
            # Not possilbe if there are less cells then number we have to fill.
            return

        elif nums_left == 0 and l_shape_index == self.LENGTH - 1:
            # We finished filling all the shapes of the matrix.
            # Now we need to validate the matrix with a few checks.
            # 1. Are all the clues valid?
            # 2. Are all the cells connected?

            # Check if clues are satisfied.
            all_clues_valid = self._are_clues_valid()
            if not all_clues_valid:
                return

            # check if all values are connected
            all_cells_connected = self._are_all_cells_contiguously_connected(self.matrix)
            if not all_cells_connected:
                return

            # Sucess: If we have gotten here we now found the solution. Output it to a file.
            self._output_matrix_to_file(self.matrix)
            exit(0)  # Stop processing once we find solution

        elif nums_left == 0:
            # We filled all the cells for this L-Shape so move on to the next L-Shape.
            new_shape_index = l_shape_index + 1
            new_avail_cells = self._get_cells(new_shape_index)
            for i, new_num in enumerate(avail_nums):
                new_avail_nums = avail_nums[:i] + avail_nums[i + 1 :]
                self._fill_l_shape(
                    new_shape_index, new_avail_cells, new_num, new_num, new_avail_nums
                )

        else:
            for i, cell in enumerate(available_cells):
                row = cell[0]
                col = cell[1]

                # CHECK 1: Check if placing the cell has broken
                #          the constraints of the clue.
                clue_cells = self._find_adj_clues(row, col)
                all_clues_valid = True
                for clue_cell in clue_cells:
                    if not self._clues_is_valid(clue_cell, num):
                        all_clues_valid = False
                        break

                if not all_clues_valid:
                    continue

                # CHECK 2: Check if placing the cell has broken the constraints
                #          of at least 1 empty cell in a 2x2 square
                valid_squares = self._has_valid_squares(row, col)
                if not valid_squares:
                    continue

                # Place the num in the matrix if it doesn't break those constraints.
                self.matrix[row][col] = num

                # Remove the cell from the available cells left in the current L-Shape.
                new_avail_cells = available_cells[i + 1 :]
                # Continue placing nums in the current L-Shape
                self._fill_l_shape(
                    l_shape_index, new_avail_cells, num, nums_left - 1, avail_nums
                )

                # After recursion we need to un-place the cell for backtracking.
                self.matrix[row][col] = 0

        return
