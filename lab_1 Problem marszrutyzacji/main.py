from vrp import VRP

if __name__ == '__main__':
    vrp = VRP("data/PL.csv")
    vrp.calculate_best_base_location()
