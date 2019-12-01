class Maze:
    """
    Helper class used to display a view of the maze.
    """
    WALL = "#"
    FLOOR = " "
    EXPLORED = "·"
    HIT = "x"

    def __init__(self, grid, start, end):
        self.end = end
        self.start = start
        self.np_grid = grid
        self.height = grid.shape[0]
        self.width = grid.shape[1]
        self.grid = self._grid_to_string(grid)
        self.obstacles = self._obstacles(grid)

    def __str__(self):
        top_line = (",," * self.width) + ",\n"
        line = lambda c, x: "|" + " ".join(i for i in x) + "|"
        lines = [line(c, j) for c, j in enumerate(self.grid)]
        board = "\n".join(i for i in lines)
        bottom_line = "\n" + ("``" * self.width) + "`"
        return top_line + board + bottom_line

    def _grid_to_string(self, np_grid):
        tag = lambda cell: self.WALL if cell == 1. else self.FLOOR
        grid = [[tag(i) for i in row] for row in np_grid]
        return grid

    def _obstacles(self, np_grid):
        coord = lambda y, r : [(x, y) for x, i in enumerate(r) if i == 1.0]
        coord_list = [coord(y, rows) for y, rows in enumerate(np_grid)]
        return [i for sub in coord_list for i in sub]

    def reset(self):
        self.grid = self._grid_to_string(self.np_grid)

    def apply_solution(self, solution):
        for i in solution:
            self.set(i)

    def set(self, position):
        if self.is_valid(position):
            if(position in self.obstacles):
                self.grid[position[1]][position[0]] = self.HIT
            else:
                self.grid[position[1]][position[0]] = self.EXPLORED

    def is_valid(self, position):
        x = 0 <= position[1] <= self.width - 1
        y = 0 <= position[0] <= self.height - 1
        return x and y

    def get(self, position):
        return self.grid[position[1]][position[0]]
