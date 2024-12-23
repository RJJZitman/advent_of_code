from collections import Counter


def get_input(input_path: str = "./input.txt") -> list[int]:
    """Simple function to read the puzzle input data and ensure correct types."""
    with open(input_path, "r") as file:
        return list(map(int, next(file).split()))

def apply_rules_to(stone: int) -> list[int]:
    """Applies rules to a single stone."""
    if stone == 0:
        return [1]
    s = str(stone)
    if len(s) % 2 == 0:
        mid = len(s) // 2
        return [int(s[:mid]), int(s[mid:])]
    return [stone * 2024]

def blinking_counts(stone_counts: Counter, iters: int) -> Counter:
    for _ in range(iters):
        new_counts = Counter()
        for stone, count in stone_counts.items():
            new_stones = apply_rules_to(stone)
            for new_stone in new_stones:
                new_counts[new_stone] += count
        stone_counts = new_counts
    return stone_counts

def main():
    stones = Counter(get_input())
    blinked_25 = blinking_counts(stones, iters=25)
    blinked_75 = blinking_counts(blinked_25, iters=50)
    return sum(blinked_25.values()), sum(blinked_75.values())

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
