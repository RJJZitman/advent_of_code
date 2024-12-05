import copy


coord = tuple[int, int]
sequence_coords = tuple[coord, coord, coord, coord]


class XmasPuzzle:
    literal = "XMAS"
    valid_mas = {"MAS", "SAM"}

    def __init__(self, input_file_path: str) -> None:
        with open(input_file_path, 'r') as file:
            self._grid = [list(line) if line[-1].isalpha() else list(line[:-1]) for line in file]
    
    @property
    def grid(self) -> list[str]:
        return copy.deepcopy(self._grid)


class XmasPuzzleSolver:
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1), 
        (-1, -1), 
        (1, -1),
        (-1, 1)
    ]

    def __init__(self, puzzle: XmasPuzzle) -> None:
        self.puzzle = puzzle
        self.grid = self.puzzle.grid

        self.__literal_matches: list[sequence_coords] | None = None
        self.__pattern_matches: list[sequence_coords] | None = None

    def solve_literals(self) -> None:
        rows, cols = len(self.grid), len(self.grid[0])
        word_len = len(self.puzzle.literal)
        self.__literal_matches = []

        # Brute force the puzzle
        for row in range(rows):
            for col in range(cols):
                # Check each direction
                for step_row, step_col in self.directions:
                    positions = []
                    for k in range(word_len):
                        # Check range for safe traversing over grid elements
                        r = row + k * step_row
                        c = col + k * step_col
                        if 0 <= r < rows and 0 <= c < cols and self.grid[r][c] == self.puzzle.literal[k]:
                            positions.append((r, c))
                        else:
                            break
                    if len(positions) == word_len:
                        self.__literal_matches.append(positions)

    def solve_patterns(self) -> None:
        rows, cols = len(self.grid), len(self.grid[0])
        self.__pattern_matches = []

        # Start at index 1 and go to the second last to check each 3x3 block
        for row in range(1, rows - 1): 
            for col in range(1, cols - 1):
                # Check if the center is 'A'
                if self.grid[row][col] != "A":
                    continue

                # Compute diagonals
                main_diag = self.grid[row - 1][col - 1] + self.grid[row][col] + self.grid[row + 1][col + 1]
                anti_diag = self.grid[row - 1][col + 1] + self.grid[row][col] + self.grid[row + 1][col - 1]

                # Check if both diagonals are "MAS" or "SAM"
                if main_diag in self.puzzle.valid_mas and anti_diag in self.puzzle.valid_mas:
                    # Get coordinates
                    match_coords = [
                        (row - 1, col - 1), (row + 1, col + 1), # Main diagonal
                        (row - 1, col + 1), (row + 1, col - 1), # Anti-diagonal
                        (row, col) # Center
                    ]
                    self.__pattern_matches.append(tuple(match_coords))
            
    @property
    def literal_matches(self) -> list[sequence_coords]:
        return copy.deepcopy(self.__literal_matches)
            
    @property
    def pattern_matches(self) -> list[sequence_coords]:
        return copy.deepcopy(self.__pattern_matches)


def main() -> tuple[int, any]:

    xmas_puzzle = XmasPuzzle(input_file_path="input.txt")
    solver = XmasPuzzleSolver(puzzle=xmas_puzzle)

    solver.solve_literals()
    solver.solve_patterns()

    return len(solver.literal_matches), len(solver.pattern_matches)


if __name__ == "__main__":
    output_1, output_2 = main()
    print(output_1, output_2)
