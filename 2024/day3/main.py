import re

from input import instructions_text as INSTRUCTION_TEXT


INSTRUCTION_PATTERN = r"mul\(\d{1,3},\d{1,3}\)"
CONTROL_PATTERN = r"(don't\(\)|do\(\))"

def multiply_instruction(instruction: str) -> int:
    # Extract numbers from the mul instruction
    l, r = instruction.split(",")
    l = l[4:] 
    r = r[:-1]
    return int(l) * int(r)

def compute_mults(instructions_text: str) -> list[int]:
    # Find instructions and perform multiplication
    instructions = re.findall(INSTRUCTION_PATTERN, instructions_text)
    return [multiply_instruction(instruction=instruction) for instruction in instructions]

def compute_controled_mults(instructions_text: str) -> list[int]:
    # By default, mul instructions are enabled
    mul_enabled = True
    enabled_multiplications = []

    for section in re.split(CONTROL_PATTERN, instructions_text):
        # Split intstructions_text into control commands and the remaining text sections
        if section == "don't()":
            mul_enabled = False
        elif section == "do()":
            mul_enabled = True
        else:
            # Process mul instructions in this section if they are enabled
            if mul_enabled:
                instructions = re.findall(INSTRUCTION_PATTERN, section)
                enabled_multiplications.extend(
                    multiply_instruction(instruction) for instruction in instructions
                )
    return enabled_multiplications

def main():
    simple_mults = sum(compute_mults(instructions_text=INSTRUCTION_TEXT))
    controled_mults = sum(compute_controled_mults(instructions_text=INSTRUCTION_TEXT))

    return simple_mults, controled_mults

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
