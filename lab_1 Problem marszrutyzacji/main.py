from vrp import VRP
from cvrp import CVRP

filename = 'PL'


if __name__ == '__main__':
    print("\nVRP: ")
    vrp = VRP(filename)
    vrp.calculate_best_base_location()
    print("\nCVRP: ")
    cvrp = CVRP(filename)
    cvrp.calculate_best_base_location()

