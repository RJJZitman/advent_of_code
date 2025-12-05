import math

from input import puzzle_raw


def prep_input(raw_input: str) -> list[str]:
    return raw_input.split("\n")

def main1():
    puzzle = prep_input(raw_input=puzzle_raw)
    zero_counter = 0

    curr_idx = 50
    for click in puzzle:
        steps = int(click[1:])
        if click[0] == "L":
            steps = steps*-1

        curr_idx = (curr_idx + steps) % 100
        if curr_idx == 0:
            zero_counter += 1

    print(f"result: {zero_counter}")

def main2():
    puzzle = prep_input(raw_input=puzzle_raw)
    zero_counter = 0

    curr_idx = 50
    for click in puzzle:
        # determine arithmetic for click instruction
        steps = int(click[1:])
        if click[0] == "L":
            steps = steps*-1

        # compute full rotations and remaining steps
        full_rotation  = math.floor(abs(steps / 100))
        zero_counter += full_rotation
        leftover_steps = steps - 100*full_rotation if steps>0 else steps + 100*full_rotation

        # compute new position after following the instruction
        new_idx = (curr_idx + leftover_steps) % 100

        # evaluate if 0 has been passed
        if (new_idx != curr_idx + leftover_steps and curr_idx != 0) or new_idx == 0:
            zero_counter += 1
        
        # setp the new position as current for next instruction
        curr_idx = new_idx

    print(f"result: {zero_counter}")

if __name__ == "__main__":
    main1()
    print(80*"-")
    main2()
