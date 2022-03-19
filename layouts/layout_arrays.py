"""
- 0 is not a space
- 1 is black (player 1)
- 2 is white (player 2)
- 3 is empty
"""
DEFAULT_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                 [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0],
                 [0, 0, 0, 3, 3, 2, 2, 2, 3, 3, 0],
                 [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                 [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                 [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                 [0, 3, 3, 1, 1, 1, 3, 3, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

BELGIAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 2, 3, 1, 1, 0],
                       [0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 0],
                       [0, 0, 0, 3, 2, 2, 3, 1, 1, 3, 0],
                       [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                       [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                       [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                       [0, 3, 1, 1, 3, 2, 2, 3, 0, 0, 0],
                       [0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
                       [0, 1, 1, 3, 2, 2, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

GERMAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 3, 2, 2, 0],
                      [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 0],
                      [0, 0, 0, 3, 1, 1, 3, 2, 2, 3, 0],
                      [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                      [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                      [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                      [0, 3, 2, 2, 3, 1, 1, 3, 0, 0, 0],
                      [0, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
                      [0, 2, 2, 3, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

STARTING_LAYOUT = {1: DEFAULT_START, 2: BELGIAN_DAISY_START, 3: GERMAN_DAISY_START}

VALID_NODES = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Change matrix for no changes
NO_CHANGE_MATRIX = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Boards for testing
PUSHABLE_TEST_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0],
                       [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0],
                       [0, 0, 0, 3, 3, 2, 2, 2, 3, 3, 0],
                       [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                       [0, 3, 3, 3, 2, 3, 3, 3, 3, 3, 0],
                       [0, 3, 3, 3, 2, 3, 3, 3, 3, 0, 0],
                       [0, 2, 3, 1, 1, 1, 2, 2, 0, 0, 0],
                       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
