"""6.009 Lab 3 -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!


class MinesGame:
    """
    Class to represent a game of Mines.
    """

    def __init__(self, num_rows, num_cols, bombs):
        """Start a new game.

        Initializes a new instance of `MinesGame` to have the following
        attributes:
           * `dimensions`
           * `state`
           * `board`
           * `mask`

        Each of these should be as described in the handout.

        Parameters:
           num_rows (int): Number of rows
           num_cols (int): Number of columns
           bombs (list/tuple): List of bombs, given in (row, column) pairs,
                               which can be either tuples or lists
        """
        self.dimensions = [num_rows, num_cols]
        self.state = "ongoing"
        self.mask = [[False] * num_cols] * num_rows
        self.board = [[0] * num_cols] * num_rows
        for x in range(num_rows):
            for y in range(num_cols):
                if [x,y] in bombs or (x,y) in bombs:
                    self.board[x][y] = '.'
        for r in range(num_rows):
            for c in range(num_cols):
                if self.board[r][c] == 0:
                    neighbor_bombs = 0
                    if 0 <= r-1 < num_rows:
                        if 0 <= c-1 < num_cols:
                            if self.board[r-1][c-1] == '.':
                                neighbor_bombs += 1
                    if 0 <= r < num_rows:
                        if 0 <= c-1 < num_cols:
                            if self.board[r][c-1] == '.':
                                neighbor_bombs += 1
                    if 0 <= r+1 < num_rows:
                        if 0 <= c-1 < num_cols:
                            if self.board[r+1][c-1] == '.':
                                neighbor_bombs += 1
                    if 0 <= r-1 < num_rows:
                        if 0 <= c < num_cols:
                            if self.board[r-1][c] == '.':
                                neighbor_bombs += 1
                    if 0 <= r < num_rows:
                        if 0 <= c < num_cols:
                            if self.board[r][c] == '.':
                                neighbor_bombs += 1
                    if 0 <= r+1 < num_rows:
                        if 0 <= c < num_cols:
                            if self.board[r+1][c] == '.':
                                neighbor_bombs += 1
                    if 0 <= r-1 < num_rows:
                        if 0 <= c+1 < num_cols:
                            if self.board[r-1][c+1] == '.':
                                neighbor_bombs += 1
                    if 0 <= r < num_rows:
                        if 0 <= c+1 < num_cols:
                            if self.board[r][c+1] == '.':
                                neighbor_bombs += 1
                    if 0 <= r+1 < num_rows:
                        if 0 <= c+1 < num_cols:
                            if self.board[r+1][c+1] == '.':
                                neighbor_bombs += 1
                    self.board[r][c] = neighbor_bombs


    def dump(self):
        """Print a human-readable representation of this game.

        >>> g = MinesGame(1, 2, [(0, 0)])
        >>> g.dump()
        dimensions: [1, 2]
        board: ['.', 1]
        mask:  [False, False]
        state: ongoing
        """
        lines = ["dimensions: {}".format(self.dimensions),
                 "board: {}".format("\n       ".join(map(str, self.board))),
                 "mask:  {}".format("\n       ".join(map(str, self.mask))),
                 "state: {}".format(self.state),
                 ]
        print("\n".join(lines))


    def dig(self, row, col):
        """Recursively dig up (row, col) and neighboring squares.

        Update self.mask to reveal (row, col); then recursively reveal (dig up)
        its neighbors, as long as (row, col) does not contain and is not adjacent
        to a bomb.  Return an integer indicating how many new squares were
        revealed.

        The state of the game should be changed to "defeat" when at least one bomb
        is visible on the board after digging, "victory" when all safe squares
        (squares that do not contain a bomb) and no bombs are visible, and
        "ongoing" otherwise.

        Parameters:
           row (int): Where to start digging (row)
           col (int): Where to start digging (col)

        Returns:
           int: the number of new squares revealed

        >>> game = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.dig(0, 3)
        4
        >>> game.dump()
        dimensions: [2, 4]
        board: ['.', 3, 1, 0]
               ['.', '.', 1, 0]
        mask:  [False, True, True, True]
               [False, False, True, True]
        state: victory

        >>> game = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.dig(0, 0)
        1
        >>> game.dump()
        dimensions: [2, 4]
        board: ['.', 3, 1, 0]
               ['.', '.', 1, 0]
        mask:  [True, True, False, False]
               [False, False, False, False]
        state: defeat
        """
        state = self.state
        if state == "defeat" or state == "victory":
            self.state = state
            return 0

        if self.board[row][col] == '.':
            self.mask[row][col] = True
            self.state = "defeat"
            return 1

        coord1 = [row - 1, col - 1]
        coord2 = [row - 1, col]
        coord3 = [row - 1, col + 1]

        coord4 = [row, col - 1]
        coord5 = [row, col + 1]

        coord6 = [row + 1, col - 1]
        coord7 = [row + 1, col]
        coord8 = [row + 1, col + 1]

        count = 0
        for coord in [coord1, coord2, coord3, coord4,
                      coord5, coord6, coord7, coord8]:
            if coord[0] >= 0:
                if coord[0] < self.height:
                    if cooef[1] >= 0:
                        if coord[1] < self.width:
                            count += 1
                            self.mask[coord[0], coord[1]] = True

        self.mask[row][col] = True

        bombs = 0
        covered_squares = 0
        for r in range(self.dimensions[0]):
            for c in range(self.dimensions[1]):
                if self.board[r][c] == ".":
                    if  self.mask[r][c] == True:
                        bombs += 1
                elif self.mask[r][c] == False:
                    covered_squares += 1
        if bombs != 0:
            self.state = "defeat"
            return 0
        elif covered_squares == 0:
            self.state = "victory"
            return 0
        else:
            return count


    def render(self, xray=False):
        """Prepare a game for display.

        Returns a two-dimensional array (list of lists) of "_" (hidden
        squares), "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  game.mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Parameters:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           A 2D array (list of lists) representing the rendered board

        >>> g = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "state": "ongoing",
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask":  [[False, True, True, False],
        ...                   [False, False, True, False]]})
        >>> g.render(False)
        [['_', '3', '1', '_'], ['_', '_', '1', '_']]

        >>> g.render()
        [['_', '3', '1', '_'], ['_', '_', '1', '_']]

        >>> g.render(True)
        [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
        """
        raise NotImplementedError


    def render_ascii(self, xray=False):
        """Render a game as ASCII art.

        Returns a string-based representation of the game.  Each tile of
        the game board should be rendered as in the `render` method.

        Parameters:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           A string-based representation of game

        >>> g = MinesGame.from_dict({"dimensions": [2, 4],
        ...                     "state": "ongoing",
        ...                     "board": [[".", 3, 1, 0],
        ...                               [".", ".", 1, 0]],
        ...                     "mask":  [[True, True, True, False],
        ...                               [False, False, True, False]]})
        >>> print(g.render_ascii())
        .31_
        __1_
        """
        raise NotImplementedError


    @classmethod
    def from_dict(cls, d):
        """
        Create an instance of `MinesGame` from a dictionary representation of
        the game.

        Parameters:
          d (dict): a dictionary with keys 'board', 'state', 'mask', and
                    'dimensions'.

        Returns:
          An instance of `MinesGame` with parameters as specified in the
          dictionary.
        """
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    doctest.testmod()
