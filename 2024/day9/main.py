import sys
import copy


def get_input(input_path: str = "./input.txt") -> str:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    with open(input_path, "r") as file:
        map = [line.strip("\n") for line in file]

    return list(map[0])

def compress(map: list[str]) -> list[tuple[str, int | None]]:
    compressed = []
    count = 0
    for idx, val in enumerate(map):
        if idx % 2 == 0:
            compressed.append(tuple([int(val), count]))
            count += 1
        else:
            if val == '0':
                continue
            compressed.append(tuple([int(val), None]))
    return compressed

def swap_leftmost_and_rightmost(compressed: list[tuple[int, int | None]]) -> list[tuple[int, int]]:

    new_compressed = copy.deepcopy(compressed)
    left, right = 0, len(new_compressed) - 1

    while left < right:
        
        # print(f"ITER WITH: {new_compressed}")
        right = len(new_compressed) - 1

        # Find the leftmost `None` block
        while left < len(new_compressed) and new_compressed[left][1] is not None:
            left += 1
        # Find the rightmost indexed value block, ensuring to skip `None` and zero-count blocks
        while right >= 0 and (not new_compressed[right][1] or not new_compressed[right][0]):
            new_compressed.pop(right)
            right -= 1

        if left >= right:  # No more valid swaps
            break

        # Calculate how many elements to swap
        none_count = new_compressed[left][0]
        value_count = new_compressed[right][0]
        to_swap = min(none_count, value_count)

        # Adjust the counts in the blocks
        new_compressed[left] = (none_count - to_swap, None)
        new_compressed[right] = (value_count - to_swap, new_compressed[right][1])

        # Insert the swapped elements into the leftmost position
        new_compressed.insert(left, (to_swap, new_compressed[right][1]))

        # Clean up zero-count blocks
        if not new_compressed[left+1][0]:
            new_compressed.pop(left+1)
            right_idx_add = 0
        else:
            left += 1  # Only move left if the block is not depleted
            right_idx_add = 1

        if not new_compressed[right+right_idx_add][0] or not new_compressed[right+right_idx_add][1]:
            new_compressed.pop(right+right_idx_add)
            right -= right_idx_add  # Adjust right pointer after block removal

    # Final cleanup to remove trailing blocks with `None` or count 0
    if not new_compressed[-1][1]:
        return new_compressed[:-1]
    return new_compressed

def swap_blocks_to_left(compressed: list[tuple[int, int | None]], right_idx: int = -1) -> list[tuple[int, int | None]]:
    c =  compressed[:]#copy.deepcopy(compressed)

    left_idx = 0
    while len(compressed)+right_idx > left_idx:
        if c[right_idx][1] is None:
            right_idx = right_idx-1
        if len(c)+right_idx <= left_idx:
            break

        right = c[right_idx]
        left = c[left_idx]
        if left[1] is None:
            if (diff := left[0] - right[0]) >= 0:
                remains = None
                if diff:
                    remains = tuple([diff, None])
                c[left_idx] = right
                if c[right_idx-1][1] is None:
                    c[right_idx-1] = tuple([c[right_idx-1][0]+right[0], None])
                    c.pop(right_idx)
                else:
                    c[right_idx] = tuple([right[0], None]) 

                if c[right_idx+1][1] is None:
                    c[right_idx+1] = tuple([c[right_idx][0]+c[right_idx+1][0], None])
                    c.pop(right_idx)

                if remains:
                    new = []
                    new.extend(c[:left_idx+1])
                    new.extend([remains])
                    new.extend(c[left_idx+1:])
                    c = new[:]
                    
                left_idx = 0
                continue
        left_idx += 1
    right_idx -= 1
    if len(compressed)+right_idx <= 0:
        return compressed
    return swap_blocks_to_left(compressed=c, right_idx=right_idx)

def decompress(compressed: list[tuple[int, int]]) -> list[int]:
    """
    Decompress the compressed list into the full string format for verification.
    """
    result = []
    for count, value in compressed:
        result.extend([value  for _ in range(count)])
    return result


def main():
    disk_map = get_input()

    compressed_map = compress(map=disk_map)
    sys.setrecursionlimit(len(compressed_map)+1)

    by_el_swapped = swap_leftmost_and_rightmost(compressed=compressed_map)
    by_el_decompressed = decompress(compressed=by_el_swapped)

    swapped = swap_blocks_to_left(compressed=compressed_map)
    test_decomp = decompress(compressed=swapped)

    return sum([idx * val for idx, val in enumerate(by_el_decompressed)]), sum([idx * val if val else 0 for idx, val in enumerate(test_decomp)])

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
