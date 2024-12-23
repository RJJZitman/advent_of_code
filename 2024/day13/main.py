from sympy import symbols, Eq, solve
from sympy.core.numbers import Integer

A, B = symbols('a b')


def get_input(input_path: str = "./input.txt") -> list[list[str]]:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    input = []
    with open(input_path, "r") as file:
        machine = []
        for line in file:
            if line == "\n":
                input.append(machine)
                machine = []
                continue
            machine.append(line.strip("\n"))
        
        input.append(machine)

    return input

def make_equations(machine: list[str], out_offset: int = 0) -> list[Eq]:
    
    def get_equation_inputs(equations_parts: tuple[str, str]) -> tuple[str, str]:
        return int(equations_parts[0].split("X+")[1].strip("")), int(equations_parts[1].split("Y+")[1].strip(""))

    for line in machine:
        eq = line.split(": ")[1].split(", ")
        if line.startswith("Button A: "):
            a1, b1 = get_equation_inputs(equations_parts=eq)
        elif line.startswith("Button B: "):
            a2, b2 = get_equation_inputs(equations_parts=eq)
        elif line.startswith("Prize: "):
            out1 = int(eq[0].split("=")[1]) + out_offset
            out2 = int(eq[1].split("=")[1]) + out_offset
    return [Eq(a1 * A + a2 * B, out1), Eq(b1 * A + b2 * B, out2)]

def compute_combinations(machines: list[list[str]], out_offset: int = 0) -> tuple[list[int], list[int]]:
    a, b = [], []
    for machine in machines:
        eqs = make_equations(machine=machine, out_offset=out_offset)
        solutions = solve(eqs, (A, B))
        if all([isinstance(v, Integer) for _, v in solutions.items()]):
            a.append(int(solutions[A]))
            b.append(int(solutions[B]))
    return a, b


def main():
    machines = get_input()
    a1, b1 = compute_combinations(machines=machines)
    tokens_1 = sum([3*nb_a + nb_b for nb_a, nb_b in zip(a1, b1)])

    a2, b2 = compute_combinations(machines=machines, out_offset=10000000000000)
    tokens_2 = sum([3*nb_a + nb_b for nb_a, nb_b in zip(a2, b2)])
    return tokens_1, tokens_2

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
