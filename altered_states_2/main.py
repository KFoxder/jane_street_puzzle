import random
import state_trie

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
MIN_SCORE = 165_379_860
MIN_AWARDS_TO_PRINT = 0


def create_matrix(n):
    matrix = []
    for i in range(n):
        matrix.append([None] * n)
    return matrix


def print_solution(matrix):
    ans = ""
    for row in matrix:
        for cell in row:
            if cell is None:
                ans += "_"
            else:
                ans += cell
    print(ans)
    TRIE.find_states(matrix, set(), print_paths=True)


def print_matrix(matrix):
    for row in matrix:
        print(row)


state_id_to_score = {
    # Remove California to get award (NOCAL)
    "CA": 39_538_223,
    "TX": 29_145_505,
    "FL": 21_538_187,
    "NY": 20_201_249,
    "PA": 13_002_700,
    "IL": 12_812_508,
    "OH": 11_799_448,
    "GA": 10_711_908,
    "NC": 10_439_388,
    "MI": 10_077_331,
    "NJ": 9_288_994,
    "VA": 8_631_393,
    "WA": 7_705_281,
    "AZ": 7_151_502,
    "MA": 7_029_917,
    "TN": 6_910_840,
    "IN": 6_785_528,
    "MD": 6_177_224,
    "MO": 6_154_913,
    "WI": 5_893_718,
    "CO": 5_773_714,
    "MN": 5_706_494,
    "SC": 5_118_425,
    "AL": 5_024_279,
    "LA": 4_657_757,
    "KY": 4_505_836,
    "OR": 4_237_256,
    "OK": 3_959_353,
    "CT": 3_605_944,
    "UT": 3_271_616,
    "IA": 3_190_369,
    "NV": 3_104_614,
    "AR": 3_011_524,
    "MS": 2_961_279,
    "KS": 2_937_880,
    "NM": 2_117_522,
    "NE": 1_961_504,
    "ID": 1_839_106,
    "WV": 1_793_716,
    "HI": 1_455_271,
    "NH": 1_377_529,
    "ME": 1_362_359,
    "RI": 1_097_379,
    "MT": 1_084_225,
    "DE": 989_948,
    "SD": 886_667,
    "ND": 779_094,
    "AK": 733_391,
    "VT": 643_077,
    "WY": 576_851,
}

state_id_to_name = {
    "AL": "alabama",
    "AK": "alaska",
    "AZ": "arizona",
    "AR": "arkansas",
    # Remove California to get award (NOCAL)
    "CA": "california",
    "CO": "colorado",
    "CT": "connecticut",
    "DE": "delaware",
    "FL": "florida",
    "GA": "georgia",
    "HI": "hawaii",
    "ID": "idaho",
    "IL": "illinois",
    "IN": "indiana",
    "IA": "iowa",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "ME": "maine",
    "MD": "maryland",
    "MA": "massachusetts",
    "MI": "michigan",
    "MN": "minnesota",
    "MS": "mississippi",
    "MO": "missouri",
    "MT": "montana",
    "NE": "nebraska",
    "NV": "nevada",
    "NH": "newhampshire",
    "NJ": "newjersey",
    "NM": "newmexico",
    "NY": "newyork",
    "NC": "northcarolina",
    "ND": "northdakota",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "RI": "rhodeisland",
    "SC": "southcarolina",
    "SD": "southdakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VT": "vermont",
    "VA": "virginia",
    "WA": "washington",
    "WV": "westvirginia",
    "WI": "wisconsin",
    "WY": "wyoming",
}

ordered_states = sorted(
    list(state_id_to_score.keys()), key=lambda x: state_id_to_score[x], reverse=True
)

TRIE = state_trie.Trie()
for state_id, state_name in state_id_to_name.items():
    TRIE.add_transformations(state_id, state_name)


def get_available_start_cells(matrix, letter):
    same_letter_cells = []
    empty_cells = []
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] is None:
                empty_cells.append((row, col))
            elif matrix[row][col] == letter:
                same_letter_cells.append((row, col))
    return same_letter_cells + empty_cells


def get_available_cells(matrix, letter, row, col):
    same_letter_cells = []
    empty_cells = []

    for dx, dy in DIRECTIONS:
        new_row = row + dx
        new_col = col + dy
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            new_cell = matrix[new_row][new_col]
            if new_cell == letter:
                same_letter_cells.append((new_row, new_col))
            elif new_cell is None:
                empty_cells.append((new_row, new_col))

    random.shuffle(empty_cells)
    return same_letter_cells + empty_cells


def check_matrix_score(matrix):
    found_state_ids = TRIE.find_states(matrix, set())
    score = sum([state_id_to_score[state_id] for state_id in found_state_ids])
    if score >= MIN_SCORE:
        # Check Special Awards
        awards = ""
        num_awards = 0
        if len(found_state_ids) >= 20:
            awards += "(20S)"
            num_awards += 1
        if score >= 200_000_000:
            awards += "(200M)"
            num_awards += 1
        if {"UT", "CO", "NM", "AZ"}.issubset(found_state_ids):
            awards += "(4C)"
            num_awards += 1
        if {"ME", "MA", "MD", "MT", "MI", "MN", "MS", "MO"}.issubset(found_state_ids):
            awards += "(M8)"
            num_awards += 1
        if "CA" not in found_state_ids:
            awards += "(NOCAL)"
            num_awards += 1
        if "PA" in found_state_ids:
            awards += "(PA)"
            num_awards += 1

        if num_awards >= MIN_AWARDS_TO_PRINT:
            print("AWARDS: ", awards)
            print("SCORE: ", score)
            print("STATES: ", found_state_ids)
            print_matrix(matrix)
            print_solution(matrix)
    return found_state_ids, score


def fill_matrix(
    matrix,
    cur_score,
    state_index,
    letter_index,
    last_row,
    last_col,
    filled_cells,
    filled_states,
):
    # If we got to the end of the ordered states
    # without reaching the minimum score, we failed.
    if state_index == len(ordered_states):
        return

    state_id = ordered_states[state_index]
    state_name = state_id_to_name[state_id]

    # Check that we haven't already filled the matrix with this state.
    state_id = ordered_states[state_index]
    if state_id in filled_states:
        fill_matrix(
            matrix, cur_score, state_index + 1, 0, None, None, [], filled_states
        )
        return

    # If we reached the end of the state name,
    # move on to the next state and increase the score
    if letter_index == len(state_name):
        state_score = state_id_to_score[state_id]
        new_score = cur_score + state_score
        new_filled_states = filled_states.union({state_id})

        # Add blank in each cell of the letters
        for row, col in filled_cells:
            temp = matrix[row][col]
            matrix[row][col] = None

            # If we just finished filling a state, lets take the time to check
            # if any others have gotten filled in the process.
            found_states = TRIE.find_states(matrix, new_filled_states)
            for found_state in found_states:
                found_state_score = state_id_to_score[found_state]
                new_score += found_state_score
                new_filled_states = new_filled_states.union({found_state})

            if new_score >= MIN_SCORE:
                check_matrix_score(matrix)

            fill_matrix(
                matrix, new_score, state_index + 1, 0, None, None, [], new_filled_states
            )
            matrix[row][col] = temp
        return

    state_letter = state_name[letter_index]

    if letter_index == 0:
        available_cells = get_available_start_cells(matrix, state_letter)
    else:
        available_cells = get_available_cells(matrix, state_letter, last_row, last_col)

    for row, col in available_cells:
        if matrix[row][col] is None:
            matrix[row][col] = state_letter
            new_filled_cells = filled_cells + [(row, col)]
            next_letter_index = letter_index + 1
            fill_matrix(
                matrix,
                cur_score,
                state_index,
                next_letter_index,
                row,
                col,
                new_filled_cells,
                filled_states,
            )
            matrix[row][col] = None
        else:
            # If we are re-using a letter from a different state we don't
            # want to add it to filled_cells because it will be used to blank it.
            next_letter_index = letter_index + 1
            new_filled_cells = filled_cells.copy()
            # Remove this from filled_cells
            try:
                new_filled_cells.remove((row, col))
            except ValueError:
                pass
            fill_matrix(
                matrix,
                cur_score,
                state_index,
                next_letter_index,
                row,
                col,
                new_filled_cells,
                filled_states,
            )

    # If we reached this point, it means we couldn't find a valid cell to place the letter
    # so we need to backtrack.
    if letter_index == 0:
        fill_matrix(
            matrix, cur_score, state_index + 1, 0, None, None, [], filled_states
        )
    return


def main():
    n = 5
    matrix = create_matrix(n)
    fill_matrix(matrix, 0, 0, 0, None, None, [], set())


if __name__ == "__main__":
    main()
