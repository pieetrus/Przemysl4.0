import csv

fileName = 'data/US.csv'


def readFile(name):
    with open(fileName, 'r') as file:
        reader = csv.reader(file, delimiter=";", skipinitialspace=True)
        data = list(reader)
    n = int(data[0][0])
    unit = data[1][0]
    km_data = data[2:n + 2]
    convert_matrix_values_from_string_to_float(km_data)
    cities_data = []
    for line in data[n + 2:]:
        cities_data.append([line[0], line[1], line[2], line[3]])
    return n, unit, km_data, cities_data


def convert_matrix_values_from_string_to_float(array):
    row_index = 0
    column_index = 0
    for row_values in array:
        row_index = row_index + 1
        for value in row_values:
            column_index = column_index + 1
            array[row_index - 1][column_index - 1] = float(value.replace(',', '.'))
        column_index = 0


if __name__ == '__main__':
    n, unit, km_data, cities_data = readFile(fileName)
