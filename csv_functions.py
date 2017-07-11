import csv
import numpy as np


def get_data(filename):
    # Return the data from the specified file as an ndarray.
    result = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row)

    ndarray_result = np.array(result)

    return ndarray_result


def append_row(filename, row):
    # append one row to the specified csv file.
    for x in range(len(row)):
        if isinstance(row[x], list):
            raise Exception("This function accepts only a single row as input.")

    csv_ndarray = get_data(filename)
    if len(csv_ndarray[0]) != len(row):
        raise Exception("This row does not have the same number of entries as there are columns!")

    with open(filename, "a", newline="\n") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row)


def clear_data(filename):
    # delete all data in the specified file.
    f = open(filename, "w+")
    length = len(f.readline())
    f.close()
    if length == 0:
        success = True
    else:
        success = False
    return success

def save_data(filename, ndarray):
    # delete all data in the specified file and then save the given ndarray in the file.
    with open(filename, "w", newline="\n") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        clear_data(filename)

        columns = len(ndarray[0])
        for row in ndarray:
            length = len(row)
            if length != columns:
                raise Exception("These rows do not all have the same number of entries as there are columns!")
            writer.writerow(row)

