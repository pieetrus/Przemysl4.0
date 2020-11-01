import csv
import matplotlib.pyplot as plt
import pandas as pd

MAX_VALUE = 999999
MIN_VALUE = -1
maxWeight = {
    'Truck': 8000,
    'Lorry': 24000
}
maxSize = {
    'Truck': 7.8,
    'Lorry': 16.6
}


class CVRP:
    def __init__(self, file_name):
        with open("data/" + file_name + ".csv", 'r') as file:
            reader = csv.reader(file, delimiter=";", skipinitialspace=True)
            data = list(reader)
        self.n = int(data[0][0])
        self.unit = data[1][0]
        self.km_data = data[2:self.n + 2]
        self.__convert_matrix_values_from_string_to_float(self.km_data)
        self.cities_data = []
        self.load_size_data = []
        self.load_weight_data = []
        self.nodes = list(range(self.n))
        for line in data[self.n + 2:]:
            self.cities_data.append([line[0], line[1], line[2], line[3]])
        with open("data/" + file_name + "data.csv", 'r') as file:
            reader = csv.reader(file, delimiter=";", skipinitialspace=True)
            for line in reader:
                if line[1] != '':
                    self.load_size_data.append(float(line[1].replace(',', '.')))
                if line[2] != '':
                    self.load_weight_data.append(float(line[2].replace(',', '.')))
        self.data_for_plot = pd.read_csv("data/" + file_name + ".csv", sep=";", skiprows=self.n + 1, nrows=self.n * 2, decimal=",")

    def plot_map(self, perm):
        fig, ax = plt.subplots()
        x_axis = [self.data_for_plot.iat[x, 3] for x in perm]
        y_axis = [self.data_for_plot.iat[x, 2] for x in perm]
        plt.plot(x_axis, y_axis, "ro-")
        i = 0
        for xy in zip(x_axis, y_axis):  # <--
            ax.annotate(str(self.cities_data[perm[i]][1]), xy=xy, textcoords='data')  # <--
            i += 1
        plt.show()

    def calculate_best_base_location(self):
        best_result = MAX_VALUE
        best_result_base = 0
        best_result_perm = []
        for node in self.nodes:
            perm_result = self.greedy(node, self.nodes)
            length_of_road = self.calculate_length_of_road(perm_result)
            if length_of_road < best_result:
                best_result = length_of_road
                best_result_base = node
                best_result_perm = list.copy(perm_result)
        print("Best base location: " + str(self.cities_data[best_result_base][1]))
        print("Distance to take: " + str(best_result))
        print("Permutation: " + str(best_result_perm))
        self.plot_map(best_result_perm)

    def greedy(self, base_city, cities):
        available_cities = list.copy(cities)
        permutation = []
        lorry_number = 1  # numer ciężarówki
        while available_cities:
            limit = True
            permutation.append(base_city)
            j = self.find_max(available_cities, base_city)  # znajdź miasto najbardziej oddalone od miasta bazowego
            permutation.append(j)
            available_cities.remove(j)
            weight_k = self.load_weight_data[j]
            size_k = self.load_size_data[j]
            while limit:
                if not available_cities:
                    break
                l = self.find_min(available_cities, j)  # znajdź miasto najbliższe miasta j
                j = l
                weight_l = self.load_weight_data[l]
                size_l = self.load_size_data[l]
                if weight_k + weight_l < maxWeight['Truck'] and size_k + size_l < maxSize['Truck']:
                    permutation.append(l)
                    available_cities.remove(l)
                    weight_k += weight_l
                    size_k += size_l
                else:
                    limit = False
            lorry_number += 1
        permutation.append(base_city)
        return permutation

    def find_max(self, list_of_available_cities, base):
        if not list_of_available_cities:
            raise Exception("Empty list of available cities")
        distance_from_base_to_other_cities = list.copy(self.km_data[base])
        while distance_from_base_to_other_cities:
            max_value = max(distance_from_base_to_other_cities)
            index = distance_from_base_to_other_cities.index(max_value)
            if index in list_of_available_cities:
                return index
            else:
                distance_from_base_to_other_cities[index] = MIN_VALUE

    def find_min(self, list_of_available_cities, base):
        if not list_of_available_cities:
            raise Exception("Empty list of available cities")
        distance_from_base_to_other_cities = list.copy(self.km_data[base])
        while True:
            min_value = min(distance_from_base_to_other_cities)
            index = distance_from_base_to_other_cities.index(min_value)
            if index in list_of_available_cities:
                return index
            else:
                distance_from_base_to_other_cities[index] = MAX_VALUE

    def calculate_length_of_road(self, permutation):
        distance_sum = 0
        for origin, target in zip(permutation, permutation[1:]):
            distance_sum += self.km_data[origin][target]
        return distance_sum

    def __convert_matrix_values_from_string_to_float(self, array):
        row_index = 0
        column_index = 0
        for row_values in array:
            row_index = row_index + 1
            for value in row_values:
                column_index = column_index + 1
                array[row_index - 1][column_index - 1] = float(value.replace(',', '.'))
            column_index = 0
