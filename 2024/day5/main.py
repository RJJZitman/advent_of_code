import csv
import copy


def get_input(input_path: str = "./input.csv", delim: str = ",") -> list[list[int]]:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    with open(input_path, "r") as file:
        csv_reader = csv.reader(file, delimiter=delim)

        return [line for line in csv_reader]

def validate_updates(updates: list[list[int]], rules: list[tuple[int, int]]) -> tuple[list[list[int]], list[list[int]]]:
    def validate_update(update: list[int], page_id: int = 0) -> bool:
        """Traverses over the update and continues while the update adheres to the rules."""
        if page_id == len(update)-1:
            # Return True if the entire list adheres
            return True
        
        corresponding_rules = [rule[1] for rule in rules if update[page_id] == rule[0]]
        if update[page_id+1] in corresponding_rules:
            # Continue with the next page in the update if it matches a corresponding rule
            return validate_update(update=update, page_id=page_id+1)
        
        # The update does not adhere to the rules, invalid update return False
        return False
    
    valids, invalids = [], []
    for update in updates:
        if validate_update(update=update):
            valids.append(update)
        else:
            invalids.append(update)
    return valids, invalids

def correct_updates(updates: list[list[int]], rules: list[tuple[int, int]]) -> list[list[int]]:
    
    def correct_update(update: list[int], page_id: int = 0, corrected: list[int] = []) -> list[int]:
        """Traverses over the update and swaps elements untill it adheres to the rules."""
        # Note that this function applies a recursive algorithm tht assumes a correct update 
        # can be computed with the given update list.

        if page_id == len(update)-1:
            # Return True if the entire list adheres
            return update
        
        corresponding_rules = [rule[1] for rule in rules if update[page_id] == rule[0]]
        if update[page_id+1] in corresponding_rules:
            # Its a match!
            # Continue with the next page in the update if it matches a corresponding rule
            return correct_update(update=update, page_id=page_id+1)
        
        # It's not a match, split the part thats corrected so far from the remainder
        if page_id == 0:
            corrected = [copy.deepcopy(update[0])]
            other_pages = copy.deepcopy(update[1:])
        else:
            corrected = copy.deepcopy(update[:page_id+1])
            other_pages = copy.deepcopy(update[page_id+1:])

        for page in other_pages:
            # Check if our page from other_pages, is in corresponding_rules
            if page in corresponding_rules:
                # Yes it is! swap the matching page with the first element in other pages
                index_at_others = other_pages.index(page)
                other_pages[0], other_pages[index_at_others] = other_pages[index_at_others], other_pages[0]
                # Join the part that's corrected so far with the remainder that now has a corrected first element
                corrected.extend(other_pages)
                return correct_update(update=corrected, page_id=page_id+1)
        else:
            # No match, move latest element to be first and try again
            other_pages.extend(corrected)
            return correct_update(update=other_pages)

    return [correct_update(update=update) for update in updates]


def main():
    rules = get_input(input_path="input_rules.csv", delim="|")
    puzzle = get_input(input_path="input_puzzle.csv", delim=",")

    valid_updates, invalid_updates = validate_updates(updates=puzzle, rules=rules)
    corrected_invalids = correct_updates(updates=invalid_updates, rules=rules)

    return (sum([int(v[len(v)//2]) for v in valid_updates]),
            sum([int(v[len(v)//2]) for v in corrected_invalids])
            )

if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
