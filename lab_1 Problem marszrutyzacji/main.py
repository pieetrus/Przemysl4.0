import csv

MAX_VALUE = 999999
MIN_VALUE = -1

fileName = 'data/PL.csv'
n = 0
unit = ""
km_data = []
cities_data = []


def read_file(name):
    global n, unit, km_data, cities_data
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


def convert_matrix_values_from_string_to_float(array):
    row_index = 0
    column_index = 0
    for row_values in array:
        row_index = row_index + 1
        for value in row_values:
            column_index = column_index + 1
            array[row_index - 1][column_index - 1] = float(value.replace(',', '.'))
        column_index = 0


def greedy(base_city, cities):
    available_cities = list.copy(cities)
    permutation = []
    lorry_number = 1  # numer ciężarówki
    courses_amount = 10  # (n/K) zgodnie z założeniem stała liczba kursów dla pojazdu
    while available_cities:
        limit = True
        permutation.append(base_city)
        j = find_max(available_cities, base_city)  # znajdź miasto najbardziej oddalone od miasta bazowego
        permutation.append(j)
        available_cities.remove(j)
        amount_of_order_handle_by_k_vehicle = 1  # liczba zleceń obsłużonych przez pojazd k
        while limit:
            l = find_min(available_cities, j)  # znajdź miasto najbliższe miasta j
            if amount_of_order_handle_by_k_vehicle + 1 < courses_amount:
                permutation.append(l)
                available_cities.remove(l)
                amount_of_order_handle_by_k_vehicle = amount_of_order_handle_by_k_vehicle + 1
                if not available_cities:
                    limit = False
            else:
                limit = False
        lorry_number = lorry_number + 1
    return permutation


def find_max(list_of_available_cities, base):
    if not list_of_available_cities:
        raise Exception("Empty list of available cities")
    distance_from_base_to_other_cities = list.copy(km_data[base])
    while distance_from_base_to_other_cities:
        max_value = max(distance_from_base_to_other_cities)
        index = distance_from_base_to_other_cities.index(max_value)
        if index in list_of_available_cities:
            return index
        else:
            distance_from_base_to_other_cities[index] = MIN_VALUE


def find_min(list_of_available_cities, base):
    if not list_of_available_cities:
        raise Exception("Empty list of available cities")
    distance_from_base_to_other_cities = list.copy(km_data[base])
    while True:
        min_value = min(distance_from_base_to_other_cities)
        index = distance_from_base_to_other_cities.index(min_value)
        if index in list_of_available_cities:
            return index
        else:
            distance_from_base_to_other_cities[index] = MAX_VALUE


def calculate_length_of_road(permutation):
    distance_sum = 0
    for origin, target in zip(permutation, permutation[1:]):
        distance_sum += km_data[origin][target]
    return distance_sum


if __name__ == '__main__':
    read_file(fileName)
    nodes = list(range(n))
    best_result = MAX_VALUE
    best_result_base = 0
    best_result_perm = []
    for node in nodes:
        perm_result = greedy(node, nodes)
        length_of_road = calculate_length_of_road(perm_result)
        if length_of_road < best_result:
            best_result = length_of_road
            best_result_base = node
            best_result_perm = list.copy(perm_result)
    print("Best base location: " + str(cities_data[best_result_base][1]))
    print("Distance to take: " + str(best_result))
    print("Permutation: " + str(best_result_perm))

