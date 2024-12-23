from enum import Enum


coord = tuple[int, int]
map_type =  list[list[int]]


def get_input(input_path: str = "./input.txt") -> map_type:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    with open(input_path, "r") as file:

        return [list(line.strip("\n")) for line in file]

class GuardTrail:
    class Directions(Enum):
        DOWN = lambda x, y, n=1: (x+n, y)
        RIGHT = lambda x, y, n=1: (x, y+n)
        UP = lambda x, y, n=1: (x-n, y)
        LEFT = lambda x, y, n=1: (x, y-n)
    
    def __init__(self, map: map_type, obstacles: list[str] = ["#"], start_indicator: str = "^") -> None:
        self.map = map
        self.obstacles = obstacles
        self.start_indicator = start_indicator

        self._starting_pos = self._find_starting_pos()

    def _find_starting_pos(self) -> coord:
        for row_idx, row in enumerate(self.map):
            for col_idx, col in enumerate(row):
                if col == self.start_indicator:
                    return tuple([row_idx, col_idx])

    def step(self, pos: coord, walk_direction: Directions) -> tuple[coord, callable]:
        # Try walking in given direction
        new_pos = walk_direction(pos[0], pos[1])
        if new_pos[0] < 0 or new_pos[1] < 0:
            # Guard leaves the map
            # If the index is greater than the map range, we'll automatically get an index error
            raise IndexError("out of grid")

        if self.map[new_pos[0]][new_pos[1]] not in self.obstacles:
           # Position is good
            return new_pos, walk_direction
        
        # Position is not good
        # Recursively try next direction. Worst case is to go back in the opposite direction
        if walk_direction == GuardTrail.Directions.UP:
            walk_direction = GuardTrail.Directions.RIGHT
        elif walk_direction == GuardTrail.Directions.RIGHT:
            walk_direction = GuardTrail.Directions.DOWN
        elif walk_direction == GuardTrail.Directions.DOWN:
            walk_direction = GuardTrail.Directions.LEFT
        elif walk_direction == GuardTrail.Directions.LEFT:
            walk_direction = GuardTrail.Directions.UP
        return self.step(pos=pos, walk_direction=walk_direction)
    
    def walk_path(self) -> list[coord]:
        current_pos = self._starting_pos
        passed_coords = [self._starting_pos]
        walk_direction = GuardTrail.Directions.UP

        while True:
            try:
                current_pos, walk_direction = self.step(pos=current_pos, walk_direction=walk_direction)
                if current_pos not in passed_coords:
                    passed_coords.append(current_pos)
            except IndexError:
                # Guard leaves the map
                break

        return passed_coords
    

def main():
    map = get_input()
    trail = GuardTrail(map=map)
    path = trail.walk_path()

    return len(path), ...

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")