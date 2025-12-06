from typing import Iterator


def get_input():
    with open("2025/day5/input.txt", "r") as f:
        fresh_ranges = []
        ingredients = []

        for line in f:
            if line == "\n":
                break
            bounds = line.split("-")
            fresh_ranges.append((int(bounds[0]), int(bounds[1])))
        else:
            print("no ingredients requested")
        
        # Iterate over the remainder of the file for the requested ingredients
        for line in f:
            ingredients.append(int(line))

    return fresh_ranges, set(ingredients)

def main1():
    # Get input data
    fresh_ranges, ingredients = get_input()

    # Compute global bounds 
    smallest = min([bounds[0] for bounds in fresh_ranges])
    biggest = max([bounds[1] for bounds in fresh_ranges])

    fresh_ingredients = []
    for ingredient in ingredients:
        if ingredient < smallest or ingredient > biggest:
            # Prune ingredients outside of the global bounds
            continue

        for fresh_range in fresh_ranges:
            # Check per fresh range if the ingredient is fresh
            if ingredient < fresh_range[0] or ingredient > fresh_range[1]:
                continue
            # Add the fresh ingredient to the list
            fresh_ingredients.append(ingredient)
            # Break to prevent duplicate counts of a single ingredient
            break
    print(len(fresh_ingredients))


def check_overlapping_ranges(x: tuple[int, int], y: tuple[int, int]) -> bool:
    return max(x[0], y[0]) < min(x[1], y[1])

def range_merger(ranges: set[tuple[int, int]]) -> set[tuple[int, int]]:
    print(len(ranges))
    def merge(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        return (min(x[0], y[0]), max(x[1], y[1]))
    
    def iterate(on_ranges: Iterator[tuple[int, int]]):
        # print(f"new iteration with ranges: {on_ranges}")
        merged = []
        skip_next = False
        nb_ranges = len(on_ranges)
        for idx in range(0, nb_ranges, 1):
            if skip_next:
                skip_next = False
                continue
            # print(idx)
            if idx >= nb_ranges-1:
                # print("final with", on_ranges[idx])
                merged.append(on_ranges[idx])
                continue

            if not check_overlapping_ranges(on_ranges[idx], on_ranges[idx+1]):
                merged.append(on_ranges[idx])
                # print(f"no overlap with {idx} and {idx+1}")
                continue
            # print("overlap with ", on_ranges[idx], on_ranges[idx+1])
            merged.append(merge(on_ranges[idx], on_ranges[idx+1]))
            skip_next = True
            # print(merged)
        
        if len(merged) == len(on_ranges):
            return merged
        return iterate(merged)
    
    return iterate(ranges)


def main2(): # 338693411431475 is too high;338693411431459
    # Get input data
    fresh_ranges, _ = get_input()
    # print(fresh_ranges)
    sorted_ranges = sorted(fresh_ranges, key=lambda r: r[0])
    # print(sorted_ranges)
    merged_ranges = range_merger(ranges=sorted_ranges)
    # print(merged_ranges)
    lens = [x[1]+1 - x[0] if x[0] != x[1] else 0 for x in merged_ranges]
    print(lens, len(lens), sum(lens))


if __name__ == "__main__":
    # main1()
    print(80*"-")
    main2() # wrong answer, idk
