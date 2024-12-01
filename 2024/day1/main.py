import csv


def get_input(input_path: str = "./input.csv") -> tuple[list, list]:
    """ Simple function to read the puzzle input data and ensure corrext types"""
    with open(input_path, "r") as file:
        csv_reader = csv.reader(file, delimiter=" ")

        list1, list2 = [], []
        for line in csv_reader:
            # Note that the first and list index contain out data
            # This is caused by the csv being delimited by multiple spaces
            list1.append(int(line[0]))
            list2.append(int(line[-1]))
    return list1, list2

def calc_diffs(l1: list[int], l2: list[int], abs: bool = True) -> int:
    """
    Calculates the euclidian distance between entries of two lists of equal length.
    
    :param l1: first list used in calculation.
    :param l2: second list used in calculation.
    :param abs: calulate absolute difference between list entries. Defaults to True.

    :return: sum of calculated differences.
    """
    if abs:
        return sum([a-b if a-b >= 0 else b-a for a,b in zip(l1,l2)])
    else:
        return sum([a-b for a,b in zip(l1,l2)])


def calc_sim_score(l1: list[int], l2: list[int]) -> int:
    """
    Calculates a similarity score for entries of two lists of equal length. The score is calculated 
    by "adding up each number in the left list after multiplying it by the number of times that 
    number appears in the right list".

    Value counts are computed to reduce the number of lookups of l1 values in list 2. It also allows 
    for a single calculation per unique value in 1.

    :param l1: first list used in calculation.
    :param l2: second list used in calculation.
    :return: similarity score 
    """
    # Compute value counts
    value_counts_l1 = {x:l1.count(x) for x in l1}
    value_counts_l2 = {x:l2.count(x) for x in l2}

    # Calculate the sim score
    return sum([loc_id * value_counts_l2[loc_id] * nb_occ
                    if loc_id in value_counts_l2 
                    else 0 
                for loc_id, nb_occ in value_counts_l1.items()]
                )


def main() -> tuple[int, int]:
    # Get input data
    left_list, right_list = get_input()

    # Sort lists
    left_list.sort()
    right_list.sort()

    # Calc output for the first puzzle
    diffs = calc_diffs(l1=left_list, l2=right_list)

    # Calc output for the second puzzle
    sim_score = calc_sim_score(l1=left_list, l2=right_list)

    return diffs, sim_score

if __name__ == "__main__":
    output_p1, output_p2 = main()
    print(f"First puzzle output: {output_p1}\nSecond puzzle output: {output_p2}")
