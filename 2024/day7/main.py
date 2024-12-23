from functools import reduce
from itertools import product


equation_type = tuple[int, list[int]]


OPERATORS = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "||": lambda x, y: int(''.join([str(x), str(y)])),
}

def get_input(input_path: str = "./input.txt") -> list[equation_type]:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    with open(input_path, "r") as file:
        equations = [line.strip("\n").split(": ") for line in file]

    return [tuple([int(result), [int(val) for val in vals.split(" ")]]) for result, vals in equations]

def test_equation(equation: tuple, operands: list[str] = ["+", "*"]) -> bool:
    # Convert operator strings to callable functions
    operand_funcs = [OPERATORS[op] for op in operands if op in operands]

    # Target result and list of numbers
    target, values = equation

    # Generate all possible operand combinations
    operand_permutations = list(product(operand_funcs, repeat=len(values) - 1))

    # Test each combination
    for ops in operand_permutations:
        # Evaluate expression left-to-right with a foldl
        result = reduce(lambda acc, pair: pair[0](acc, pair[1]), zip(ops, values[1:]), values[0])
        if target == result:
            return True    
    return False


def main():
    equations = get_input()
    valid_equations = [equation[0] for equation in equations if test_equation(equation=equation)]
    valid_equations_with_pipe = [equation[0] for equation in equations if test_equation(equation=equation, operands=["+", "*", "||"])]
    
    return sum(valid_equations), sum(valid_equations_with_pipe)

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
