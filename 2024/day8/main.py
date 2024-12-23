from typing import List, Dict, Set, Union

map_type = Dict[Union[str, int], Set[complex]]


def get_input(input_path: str = "./input.txt") -> List[str]:
    """Simple function to read the puzzle input data and ensure correct types."""
    with open(input_path, "r") as file:
        return [line.strip("\n") for line in file]


def parse_map(input_map: List[str]) -> map_type:
    """Parse the input map into a dictionary with characters and their complex coordinates."""
    return {
        char: {
            col + -row * 1j  # Use j for the complex number notation
            for row, line in enumerate(input_map)
            for col, char_in_line in enumerate(line)
            if char_in_line == char
        }
        for char in set(char for line in input_map for char in line if char.isalnum())
    }


def is_within_bounds(point: complex, grid_width: int, grid_height: int) -> bool:
    """Check if the point lies within the grid's boundaries."""
    x, y = int(point.real), int(-point.imag)
    return 0 <= x < grid_width and 0 <= y < grid_height


def extend_line(char_coords: Set[complex], grid_width: int, grid_height: int) -> Set[complex]:
    """
    For each pair of points, calculate the vector and determine the extended points.
    """
    additional_points = set()
    coords = list(char_coords)
    
    # Iterate over all pairs of coordinates
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            p1, p2 = coords[i], coords[j]
            vector = p2 - p1
            
            # Calculate extended points
            extended_p1 = p1 - vector
            extended_p2 = p2 + vector
            
            # Add only the new points within bounds
            if is_within_bounds(extended_p1, grid_width, grid_height):
                additional_points.add(extended_p1)
            if is_within_bounds(point=extended_p2, grid_width=grid_width, grid_height=grid_height):
                additional_points.add(extended_p2)
    
    # Remove points that are already in the original set
    additional_points -= char_coords
    return additional_points


def compute_additional_points(parsed_map: map_type, grid_width: int, grid_height: int) -> map_type:
    """
    Compute the unique additional points for each character based on their extended lines,
    restricted to within the grid bounds.
    """
    return {
        char: extend_line(char_coords=coords, grid_width=grid_width, grid_height=grid_height)
        for char, coords in parsed_map.items()
    }

def compute_line_points(
    p1: complex, p2: complex, grid_width: int, grid_height: int, original_points: Set[complex]
) -> Set[complex]:
    """
    Compute all points on the line between p1 and p2 within the grid bounds.
    Stops when points go out of bounds.
    """
    vector = p2 - p1
    line_points = set()

    # Extend in the positive direction
    current = p2 + vector
    while is_within_bounds(current, grid_width, grid_height):
        if current not in original_points:
            line_points.add(current)
        current += vector

    # Extend in the negative direction
    current = p1 - vector
    while is_within_bounds(current, grid_width, grid_height):
        if current not in original_points:
            line_points.add(current)
        current -= vector

    return line_points


def compute_additional_points_on_lines(parsed_map: map_type, grid_width: int, grid_height: int) -> map_type:
    """
    Compute all new antennas on lines extended between every pair of points for each character.
    """
    additional_points = {}

    for char, coords in parsed_map.items():
        char_points = set()
        coords = list(coords)

        # Iterate over all pairs of points
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                p1, p2 = coords[i], coords[j]

                # Compute all points on the line within bounds
                line_points = compute_line_points(p1, p2, grid_width, grid_height, set(coords))
                char_points.update(line_points)

        additional_points[char] = char_points

    return additional_points



def main():
    map_data = get_input()
    grid_height = len(map_data)  # Number of rows
    grid_width = len(map_data[0])  # Number of columns (assume all rows are the same length)

    parsed_map = parse_map(input_map=map_data)
    
    extra_points = compute_additional_points(parsed_map=parsed_map, grid_width=grid_width, grid_height=grid_height)
    total_unique_points = len(set().union(*extra_points.values()))


    return total_unique_points, ...

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\n")
    print(f"Second puzzle output: {output_2}")
