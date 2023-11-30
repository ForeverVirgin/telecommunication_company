import random
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

radius = 5
tower_cost = 200

class Tower:
    def __init__(self, x, y, r):
        self.x = x
        self.radius = r
        self.y = y


class CityGrid:
    towers = []

    def __init__(self, length, width, coverage):
        self.length = length
        self.width = width
        self.obstructed_coverage = coverage
        self.matrix = self.generate_points(length, width, coverage)

    def generate_points(self, length, width, coverage):
        matrix = [1 for i in range(math.ceil(length * width * coverage))]
        amount_of_zeros = length * width - len(matrix)
        for i in range(amount_of_zeros):
            matrix.insert(random.randint(0, len(matrix)), 0)
        new_matrix = [matrix[i * width:(i + 1) * width] for i in range(length)]
        return new_matrix

    def placeable(matrix, x, y):
        if x < len(matrix) and y < len(matrix[0]):
            return matrix[x][y] == 0 or matrix[x][y] == 2
        else:
            return False

    def place_tower(matr, x, y, r):
        if CityGrid.placeable(matr, x, y):
            for i in range(max(x - r, 0), min(x + r, len(matr) - 1) + 1):
                for j in range(max(y - r, 0), min(y + r, len(matr[0]) - 1) + 1):
                    if matr[i][j] == 0:
                        matr[i][j] += 2
            matr[x][y] = 4
        return matr

    def covered(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    return False
        return True

    def zero_indexes(self, matrix):
        list_of_zeros = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    list_of_zeros.append([i, j])
        return list_of_zeros

    def new_combination(current_list, n_max):
        n = len(current_list) - 1
        current_list[n] += 1
        while current_list[n] > n_max - (len(current_list) - n):
            current_list[n] = 0
            n -= 1
            if n == -1:
                raise Exception("Final combination")
            current_list[n] += 1
        for i in range(1, len(current_list)):
            if current_list[i] <= current_list[i - 1] and current_list[i] == 0:
                current_list[i] = current_list[i - 1] + 1
        return current_list

    def find_min_towers_map(self):
        k_towers = 1
        list_of_zeros = self.zero_indexes(self.matrix)
        while k_towers <= len(list_of_zeros):
            temp_matrix = []
            for i in self.matrix:
                temp_matrix.append(i.copy())
            self.towers = []
            current_list = [i for i in range(k_towers)]
            for i in current_list:
                temp_matrix = CityGrid.place_tower(temp_matrix, list_of_zeros[i][0], list_of_zeros[i][1], radius)
                self.towers.append(Tower(list_of_zeros[i][0], list_of_zeros[i][1], radius))
            while not (CityGrid.covered(temp_matrix) and CityGrid.connected(self.towers)):
                temp_matrix = []
                for i in self.matrix:
                    temp_matrix.append(i.copy())
                self.towers = []
                try:
                    current_list = CityGrid.new_combination(current_list, len(list_of_zeros))
                except:
                    break
                for i in current_list:
                    temp_matrix = CityGrid.place_tower(temp_matrix, list_of_zeros[i][0], list_of_zeros[i][1], radius)
                    self.towers.append(Tower(list_of_zeros[i][0], list_of_zeros[i][1], radius))
            if CityGrid.covered(temp_matrix) and CityGrid.connected(self.towers):
                return
            else:
                k_towers += 1
        raise Exception("Minimal map does not exist")

    def connected(towers):
        list_of_connected = []
        list_of_connected_new = [towers[0]]
        while list_of_connected_new != list_of_connected:
            list_of_connected = list_of_connected_new
            for tower in list_of_connected:
                for i in towers:
                    if tower.x - tower.radius <= i.x <= tower.x + tower.radius and tower.y - tower.radius <= i.y <= tower.y + tower.radius and i not in list_of_connected_new:
                        list_of_connected_new.append(i)
        return len(list_of_connected_new) == len(towers)

    def get_list_of_towers(self, tower):
        list_of_towers = []
        for i in self.towers:
            if tower.x - radius <= i.x <= tower.x + radius and tower.y - radius <= i.y <= tower.y + radius and not (
                    i.x == tower.x and i.y == tower.y):
                list_of_towers.append(i)
        return list_of_towers

    def find_reliable_path(self, tower1, tower2):
        visited_towers = [tower1]
        routes = []
        while tower2 not in visited_towers:
            for i in visited_towers:
                neighbours = self.get_list_of_towers(i)
                for j in neighbours:
                    if j not in visited_towers:
                        visited_towers.append(j)
                        routes.append([i, j])
                        if j == tower2:
                            break
        tmp = tower2
        for_str = "tower " + str(self.towers.index(tmp))
        while tmp != tower1:
            for i in range(len(routes) - 1, -1, -1):
                if routes[i][1] == tmp:
                    for_str = "tower " + str(self.towers.index(routes[i][0])) + " -> " + for_str
                    tmp = routes[i][0]
        return for_str

    def show_graphics_map(self):
        coverage = []
        for i in range(len(self.matrix)):
            a = [False for j in range(len(self.matrix[0]))]
            coverage.append(a)

        for tower in self.towers:
            for i in range(max(0, tower.x - tower.radius), min(tower.x + tower.radius, len(self.matrix) - 1) + 1):
                for j in range(max(0, tower.y - tower.radius),
                               min(tower.y + tower.radius, len(self.matrix[0]) - 1) + 1):
                    coverage[i][j] = True
        for tower in self.towers:
            coverage[tower.x][tower.y] = False
        CityGrid.draw_map(self, coverage)

    def draw_map(self, coverage):
        fig, ax = plt.subplots()
        ax.plot([0, len(self.matrix)], [0, len(self.matrix[0])])
        for i in range(len(self.matrix[0]) - 1, -1, -1):
            for j in range(len(self.matrix) - 1, -1, -1):
                ax.add_patch(Rectangle((j, i), 1, 1,
                                       facecolor="c" if self.matrix[j][i] == 0 and coverage[j][i] else "b" if self.matrix[j][
                                                                                                               i] == 1 and
                                                                                                           coverage[
                                                                                                               j][
                                                                                                               i] else "y" if
                                       self.matrix[j][i] == 0 and not coverage[j][i] else "g" if self.matrix[j][i] == 1 and not
                                       coverage[j][i] else "m", fill=True))
        for tower in self.towers:
            ax.add_patch(Rectangle((tower.x, tower.y), 1, 1, facecolor="m"))
        plt.show()

    def find_best_coverage(self, budget):
        k_towers = int(budget / tower_cost)
        list_of_zeros = self.zero_indexes(self.matrix)
        temp_matrix = []
        for i in self.matrix:
            temp_matrix.append(i.copy())
        self.towers = []
        current_list = [i for i in range(k_towers)]
        for i in current_list:
            temp_matrix = CityGrid.place_tower(temp_matrix, list_of_zeros[i][0], list_of_zeros[i][1], radius)
            self.towers.append(Tower(list_of_zeros[i][0], list_of_zeros[i][1], radius))
        covers = 0
        for i in list_of_zeros:
            if temp_matrix[i[0]][i[1]] == 0:
                covers += 1
        if CityGrid.connected(self.towers):
            best_matrix = []
            for i in temp_matrix:
                best_matrix.append(i.copy())
            best_cover = len(list_of_zeros) - covers
            best_towers = self.towers.copy()
        else:
            best_cover = -1
        while not (CityGrid.covered(temp_matrix) and CityGrid.connected(self.towers)):
            temp_matrix = []
            for i in self.matrix:
                temp_matrix.append(i.copy())
            self.towers = []
            try:
                current_list = CityGrid.new_combination(current_list, len(list_of_zeros))
            except:
                self.towers = best_towers
                return best_matrix
            for i in current_list:
                temp_matrix = CityGrid.place_tower(temp_matrix, list_of_zeros[i][0], list_of_zeros[i][1], radius)
                self.towers.append(Tower(list_of_zeros[i][0], list_of_zeros[i][1], radius))
            covers = 0
            for i in list_of_zeros:
                if temp_matrix[i[0]][i[1]] == 0:
                    covers += 1
            if len(list_of_zeros) - covers > best_cover and CityGrid.connected(self.towers):
                best_cover = len(list_of_zeros) - covers
                best_matrix = []
                for i in temp_matrix:
                    best_matrix.append(i.copy())
                best_towers = self.towers.copy()
        self.towers = best_towers
        return best_matrix
