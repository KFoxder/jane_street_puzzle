from collections import deque

WILDCARD = "*"

DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]

class TrieNode():

    def __init__(self, char, state_id):
        self.char = char
        self.state_ids = {state_id} # CA,TX, etc
        self.children = {} # key: letter, value: TrieNode
        self.is_end = False
        self.end_states = set() # CA, TX, etc

    def has_child(self, char):
        return char in self.children
    
    def add_child(self, node):
        self.children[node.char] = node

    def get_child(self, char):
        return self.children[char]
    
    def set_end(self, state_id):
        self.is_end = True
        self.end_states = self.end_states.union({state_id})
    

class Trie():
    def __init__(self):
        self.root = TrieNode(None, None)

    def _add_state(self, state_id, state_name):
        current_node = self.root
        for char in state_name:
            if not current_node.has_child(char):
                new_node = TrieNode(char, state_id)
                current_node.add_child(new_node)
                current_node = new_node
            else:
                current_node = current_node.get_child(char)
                current_node.state_ids = current_node.state_ids.union({state_id})

        current_node.set_end(state_id)

    def add_transformations(self, state_id, state_name):
        self._add_state(state_id, state_name)
        for i in range(len(state_name)):
            altered_name = state_name[:i] + '*' + state_name[i+1:]
            self._add_state(state_id, altered_name)

    def find_states(self, matrix, ignored_state_ids, print_paths=False):
        import main
        found = set()

        queue = deque()
        # Add all the possible starting points
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                queue.append((row, col, self.root, []))

        while queue:
            row, col, node, path = queue.popleft()
            if node.is_end:
                for state_id in node.end_states:
                    if state_id not in found and state_id not in ignored_state_ids:
                        if print_paths:
                            print(f'{main.state_id_to_name[state_id]} -> {"".join([char for _, _, char in path])}')
                            # print('FOUND: ', main.state_id_to_name[state_id])
                            # print('NAME: ', ''.join([char for _, _, char in path]))
                            # print('PATH: ', path)
                        found.add(state_id)

            for dx, dy in DIRECTIONS:
                new_row = row + dx
                new_col = col + dy
                if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):

                    # Always look for wildcard
                    if node.has_child(WILDCARD):
                        wildcard_node = node.get_child(WILDCARD)
                        # Check we ignore letters if they are already found or in the ignore list.
                        if len(wildcard_node.state_ids.difference(ignored_state_ids.union(found))) > 0:
                            char = matrix[new_row][new_col] if matrix[new_row][new_col] is not None else WILDCARD
                            queue.append((new_row, new_col, wildcard_node, path + [(new_row, new_col, char)]))


                    if matrix[new_row][new_col] is not None:
                        cell_char = matrix[new_row][new_col]

                        if node.has_child(cell_char):
                            new_node = node.get_child(cell_char)
                            # Check we ignore letters if they are already found or in the ignore list.
                            if len(new_node.state_ids.difference(ignored_state_ids.union(found))) > 0:
                                queue.append((new_row, new_col, new_node, path + [(new_row, new_col, cell_char)]))
        return found

def tests():
    ########## Test 1 ##########
    trie = Trie()
    trie.add_transformations("WY", "wyoming")

    matrix = [
        ['k', 'r', None, 'i', 'm'],
        ['o', 'a', 'n', 'a', 'e'],
        ['y', 'm', 'l', 'x', 's'],
        ['w', 'i', 'n', 'l', 'r'],
        [None, 'o', 'a', 'd', 'i']
    ]

    found = trie.find_states(matrix, set())
    assert found == {"WY"}

    ########## Test 2 ##########
    trie = Trie()
    trie.add_transformations("WY", "wyoming")

    matrix = [
        ['k', 'r', None, 'i', 'm'],
        ['o', 'a', 'n', 'a', 'e'],
        ['y', 'g', 'l', 'x', 's'],
        ['w', 'i', 'n', 'l', 'r'],
        [None, 'o', 'a', 'd', 'i']
    ]

    found = trie.find_states(matrix, set())
    assert found == {"WY"}

    ########## Test 3 ##########
    trie = Trie()
    trie.add_transformations("WY", "wyoming")

    matrix = [
        ['k', 'r', None, 'i', 'm'],
        ['o', 'a', 'n', 'a', 'e'],
        ['y', 'f', 'l', 'x', 's'],
        ['w', 'i', 'n', 'g', 'r'],
        [None, 'o', 'a', 'd', 'i']
    ]

    found = trie.find_states(matrix, set())
    assert found == {"WY"}

    ########## Test 4 ##########
    # Find Idaho (ifaho) in matrix
    trie = Trie()
    trie.add_transformations("ID", "idaho")
    trie.add_transformations("OH", "ohio")
    trie.add_transformations("TX", "texas")

    matrix = [
        [None, None, 'i', 'n', None],
        ['a', 'd', 'a', 'r', 'e'],
        ['l', 'i', 'f', 'o', 'x'],
        ['n', None, 'o', 's', 'a'],
        ['w', 'e', 'r', 'k', None],
    ]

    found = trie.find_states(matrix, {"OH", "TX"})
    assert found == {"ID"}

    ########## Test 5 ##########
    # Ignore all of them.
    trie = Trie()
    trie.add_transformations("ID", "idaho")
    trie.add_transformations("OH", "ohio")
    trie.add_transformations("TX", "texas")

    matrix = [
        [None, None, 'i', 'n', None],
        ['a', 'd', 'a', 'r', 'e'],
        ['l', 'i', 'f', 'o', 'x'],
        ['n', None, 'o', 's', 'a'],
        ['w', 'e', 'r', 'k', None],
    ]

    found = trie.find_states(matrix, {"OH", "TX", "ID"})
    assert len(found) == 0

    ########## Test 6 ##########
    # Test that we can re-use letters (ie. Ohio)
    trie = Trie()
    trie.add_transformations("ID", "idaho")
    trie.add_transformations("OH", "ohio")
    trie.add_transformations("TX", "texas")

    matrix = [
        ['o', None, None, None, None],
        ['i', None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]

    found = trie.find_states(matrix, set())
    assert found == {"OH"}

    ########## Test 7 ##########
    # Test that we continue when a path has a state we are interested in and a stat we are not (ie. New York, New Jersey)
    trie = Trie()
    trie.add_transformations("NJ", "newjersey")
    trie.add_transformations("NY", "newyork")

    matrix = [
        ['n', 'w', None, None, None],
        ['e', None, 'o', None, None],
        [None, None, None, 'r', None],
        [None, None, None, None, 'k'],
        [None, None, None, None, None],
    ]

    found = trie.find_states(matrix, {"NJ"})
    assert found == {"NY"}

    ########## Test 8 ##########
    # Test two states that end in the same letter (ie. OH, ID)
    trie = Trie()
    trie.add_transformations("OH", "ohio")
    trie.add_transformations("ID", "idaho")

    matrix = [
        ['i', 'o', None, None, None],
        [None, 'd', 'h', None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]

    found = trie.find_states(matrix, set())
    assert found == {"OH", "ID"}

    ########## Test 9 ##########
    # Find all states in the matrix
    import main
    trie = Trie()
    for state_id, state_name in main.state_id_to_name.items():
        if state_id == 'CA':
            continue
        trie.add_transformations(state_id, state_name)

    matrix = [
        ['k', 'r', None, 'i', 'm'],
        ['o', 'a', 'n', 'a', 'e'],
        ['y', 'f', 'l', 'x', 's'],
        ['w', 'i', 'n', 'l', 'r'],
        [None, 'o', 'a', 'd', 'i'],
    ]

    found = trie.find_states(matrix, set())
    assert found == {'OH', 'IA', 'TX', 'ME', 'ID', 'AK', 'KS', 'AL', 'NY', 'IN', 'FL', 'AR', 'IL'}

    ########## Test 10 ##########
    # Find all states in the matrix and check score
    trie = Trie()
    for state_id, state_name in main.state_id_to_name.items():
        if state_id == 'CA':
            continue
        trie.add_transformations(state_id, state_name)

    matrix = [
        ['a', 'x', 'w', 'i', 'n'],
        ['a', 'e', 'y', 'r', 'a'],
        ['s', 'l', 'o', 's', 'k'],
        ['i', 'f', 'i', 'n', 'p'],
        ['n', 'a', 'e', 'n', 'e'],
    ]

    found = trie.find_states(matrix, set())
    score = 0
    for state_id in found:
        score += main.state_id_to_score[state_id]
    
    assert score == 131_178_405
    assert found == {'AK', 'AR', 'FL', 'IA', 'IL', 'IN', 'KS', 'LA', 'ME', 'NY', 'OH', 'PA', 'TX'}


def validate():
    """
    AWARDS:  (20S)(NOCAL)(PA)
    SCORE:  168725432
    STATES:  {'OH', 'IA', 'TX', 'ME', 'ID', 'KS', 'AK', 'NV', 'FL', 'NY', 'MT', 'IN', 'AL', 'AZ', 'GA', 'IL', 'AR', 'VA', 'LA', 'PA'}
    ['p', 'e', 'w', 'v', 'l']
    ['x', 'l', 'm', 'y', 'a']
    ['i', 'a', 'o', 'n', 's']
    ['n', 's', 'r', 'i', 'v']
    ['a', 'k', 'g', 'd', 'a']
    pewvlxlmyaiaonsnsrivakgda
    ohio -> onio
    iowa -> iona
    texas -> xexas
    maine -> mains
    idaho -> idaio
    kansas -> xansas
    alaska -> alasva
    nevada -> nsvada
    florida -> elorida
    newyork -> xewyork
    montana -> monsana
    indiana -> insiana
    alabama -> alaoama
    arizona -> arirona
    georgia -> grorgia
    illinois -> iloinois
    arkansas -> arsansas
    virginia -> oirginia
    louisiana -> loaisiana
    pennsylvania -> pemnsylvania
    """
    import main
    trie = Trie()
    for state_id, state_name in main.state_id_to_name.items():
        trie.add_transformations(state_id, state_name)

    matrix = [
        ['p', 'e', 'w', 'v', 'l'],
        ['x', 'l', 'm', 'y', 'a'],
        ['i', 'a', 'o', 'n', 's'],
        ['n', 's', 'r', 'i', 'v'],
        ['a', 'k', 'g', 'd', 'a'],
    ]
    main.print_solution(matrix)

    found = trie.find_states(matrix, set())
    score = 0
    for state_id in found:
        score += main.state_id_to_score[state_id]
    
    expected_state_ids = {'OH', 'IA', 'TX', 'ME', 'ID', 'KS', 'AK', 'NV', 'FL', 'NY', 'MT', 'IN', 'AL', 'AZ', 'GA', 'IL', 'AR', 'VA', 'LA', 'PA'}
    expected_score = 168725432

    print('SCORE: ', score)
    print('MISSING: ', expected_state_ids.difference(found))
    assert score == expected_score
    assert len(expected_state_ids.difference(found)) == 0

if __name__ == "__main__":
    print("Running validations")
    validate()

    print("Running tests")
    tests()
    print("All tests passed")
