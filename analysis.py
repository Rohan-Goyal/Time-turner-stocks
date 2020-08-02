from csv import reader
from pathlib import Path


def find_csvs(directory):
    return [i for i in directory.iterdir() if i.suffix == ".csv" and "clean" in i.name]


def csv_to_matrix(filename):
    with open(filename, newline="") as csvfile:
        return [row for row in reader(csvfile)]


def mean(arr):
    return sum(arr) / len(arr)


pwd = Path(".").resolve()
max_dict = {}
open_dict = {}

for i in find_csvs(pwd):
    name = str(i)
    matrix = csv_to_matrix(name)[1:]
   max_diffs = [
        (float(row[-2]) - float(row[-1])) * 100 / float(row[-2]) for row in matrix
    ]  # Percentage changes in stock price, from lowest for a day to highest for that same day
    avg_maxdiff = mean([abs(i) for i in max_diffs])

    open_diffs = [
        (float(row[1]) - float(row[3])) * 100 / float(row[3])
        for row in matrix
        if float(row[1]) > float(row[3])
    ]
    # Percentage change from open to close, only on days when the close price is larger than the opening price
    avg_opendiff = mean([abs(i) for i in open_diffs])

    max_dict.update(
        {i.name.replace("-max-clean.csv", ""): avg_maxdiff}
    )  # At the end, we have each companies average max-min fluctuation over that period
    open_dict.update({i.name.replace("-max-clean.csv", ""): avg_opendiff})

# Sorted for convenience, should you desire to print them
max_dict = {k: v for k, v in sorted(max_dict.items(), key=lambda item: item[1])}
open_dict = {k: v for k, v in sorted(open_dict.items(), key=lambda item: item[1])}

avg_max = mean([i[1] for i in max_dict.items()])
avg_open = mean([i[1] for i in open_dict.items()])


def interest(
    principal, contribution, rate, years
):
    # A utility to figure out the returns given that you're withdrawing or adding a certain amount annually.
    # We assume the rate is daily, and the contribution is annual
    end = principal * (1 + rate / 100) ** 250
    if years == 1:
        return end
    else:
        return interest(end + contribution, contribution, rate, years - 1)
