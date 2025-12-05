import copy

from typing import TypeAlias


ComplexGridType: TypeAlias = dict[complex, str]


def get_input() -> ComplexGridType:
    # parse input to complex plane Q4
    grid_dict = {}
    with open("2025/day4/input.txt", "r") as f:
        for y, line in enumerate(f):
            line = line.rstrip("\n")
            for x, char in enumerate(line):
                grid_dict[complex(x, -y)] = char
    return grid_dict


def check_liftable_from(grid: ComplexGridType):
    """
    Closure that encapsulates the paper roll grid and provides functionality
    to check if the max number of surrounding paper rolls surpasses the
    lifitng threshold
    """
    # Define grid bounds
    xs = [int(z.real) for z in grid.keys()]
    ys = [int(z.imag) for z in grid.keys()]
    
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    def surrounding_coords(x: int, y: int) -> complex:
        """
        Find all surrounding coordinates
        """
        x = int(x)
        y = int(y)
        neighbors = []
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                if delta_x == 0 and delta_y == 0:
                    continue
                neighbor_x, neighbor_y = x + delta_x, y + delta_y
                if x_min <= neighbor_x <= x_max and y_min <= neighbor_y <= y_max:
                    neighbors.append(complex(neighbor_x, neighbor_y))
        return neighbors
        

    def check_liftable(coord: complex, on_grid: ComplexGridType) -> bool:
        if on_grid[coord] != "@":
            # Only compute for paper rolls denoted by a "@"
            return False
        # Check if the number of surrounding rolls is less than 4
        surrounding = surrounding_coords(x=coord.real, y=coord.imag)
        surrounding_rolls = [x for x in surrounding if on_grid[x]=="@"]
        return True if len(surrounding_rolls) < 4 else False
    
    def check_liftable_recursive() -> int:
        def iterate(on_grid, alread_lifted=0):
            """Function that recursively computes the number of lifted records by checking each new grid layout"""
            liftable_coords = [k for k in on_grid.keys() if check_liftable(k, on_grid)]
            
            # Exit clause; no liftable entries on the grid
            if (nb_liftable := len(liftable_coords)) == 0:
                return alread_lifted
           
           # Update number already lifted rolls 
            alread_lifted += nb_liftable

            # Compute the new grid and continue
            new_grid = copy.copy(on_grid)
            for key in liftable_coords:
                new_grid[key] = "."
            return iterate(new_grid, alread_lifted)
        
        # Start iterating over the grid by recursively removing liftable paper rolls
        return iterate(on_grid=grid)

    def closure(): ...
    closure.check_liftable = check_liftable
    closure.check_liftable_recursive = check_liftable_recursive
    return closure

def main1():
    grid = get_input()
    checker = check_liftable_from(grid)

    liftable_coords = [k for k in grid.keys() if checker.check_liftable(k)]
    print(len(liftable_coords))

def main2():
    grid = get_input()
    checker = check_liftable_from(grid)

    total_liftable = checker.check_liftable_recursive()
    print(total_liftable)

if __name__ == "__main__":
    main1()
    print(80*"-")
    main2()
