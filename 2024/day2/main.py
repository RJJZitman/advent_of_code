import csv

def get_input(input_path: str = "./input.csv") -> list[list[int]]:
    with open(input_path, "r") as file:
        csv_reader = csv.reader(file, delimiter=" ")

        data = []
        for line in csv_reader:
            data.append([int(item) for item in line])
    return data

def safety_check(report: list[int]) -> bool:
    if len(report) < 2:
        return True  # A report with fewer than two levels is always safe.

    # Determine direction: ascending or descending
    ascending = report[0] < report[1]

    for i in range(1, len(report)):
        prev_level = report[i - 1]
        current_level = report[i]

        # Check for equal consecutive elements
        if current_level == prev_level:
            return False

        # Check for absolute difference exceeding 3
        if abs(current_level - prev_level) > 3:
            return False

        # Check for consistent direction
        if ascending and current_level < prev_level:
            return False
        if not ascending and current_level > prev_level:
            return False

    return True

def dampened_safety_check(reports: list[list[int]]) -> int:
    safe_count = 0

    for report in reports:
        if safety_check(report):
            safe_count += 1
        else:
            # Check if removing one level makes the report safe
            for i in range(len(report)):
                modified_report = report[:i] + report[i+1:]
                if safety_check(modified_report):
                    safe_count += 1
                    break  # No need to test further; one removal worked.

    return safe_count

def main() -> tuple[int, int]:
    # Get input data
    reports = get_input()

    # Calculate the number of safe reports
    nb_safe_reports = sum(safety_check(report) for report in reports)
    nb_safe_reports_damp = dampened_safety_check(reports)

    return nb_safe_reports, nb_safe_reports_damp


if __name__ == "__main__":
    output_1, output_2 = main()
    print(f"First puzzle output: {output_1}\nSecond puzzle output: {output_2}")
