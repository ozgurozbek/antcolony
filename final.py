import numpy
from numpy.random import choice as numpy_rand
import matplotlib.pyplot as mpl

class Ant_Colony(object):

    def __init__(self, distances, number_of_ants, number_of_best, number_of_iterations, preserve, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Mesafelerin kare matrisi. Köşegenler numpy.inf olarak kabul ediliyor.
            number_of_ants (int): Her iterasyon başına var olan karınca sayısı
            number_of_best (int): Feromon salgılayabilen karınca sayısı
            number_of_iteration (int): İterasyon sayısı
            preserve (float): Feromonun korunma oranı. Bu değer feromon ile çarpılıyor. Ne kadar yüksek, o kadar çok feromon.
            alpha (int or float): Feromonun üssü, Ne kadar yüksekse o kadar güçlü feromon. Standart=1
            beta (int or float): Mesafenin üssü, Ne kadar yüksekse o kadar zorlu mesafe. Standart=1

        Ignore:
            Unused variable.

        Self:
            Class itself.
        """

        # INITIALIZATION
        self.distances = distances
        self.pheromone = numpy.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.number_of_ants = number_of_ants
        self.number_of_best = number_of_best
        self.number_of_iterations = number_of_iterations
        self.preserve = preserve
        self.alpha = alpha
        self.beta = beta

    def spread_pheronome(self, all_paths, number_of_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, ignore in sorted_paths[:number_of_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def generate_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def generate_all_paths(self):
        all_paths = []
        for ignore in range(self.number_of_ants):
            path = self.generate_path(0)
            all_paths.append((path, self.generate_path_dist(path)))
        return all_paths

    def generate_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for ignore in range(len(self.distances) - 1):
            move = self.pick_move(
                self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        # Başa dön
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = numpy.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = numpy_rand(self.all_inds, 1, p=norm_row)[0]
        return move

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("ignore", numpy.inf)
        for i in range(self.number_of_iterations):
            all_paths = self.generate_all_paths()
            self.spread_pheronome(
                all_paths, self.number_of_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print(f"Run: {i}, Shortest Path: {shortest_path}")
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone * self.preserve
        return all_time_shortest_path

def make_distances_graph(ozgur_dist):
    mpl.bar([0,10,20,30,40],ozgur_dist[0],label="Kaynak 1")
    mpl.bar([12,22,32,42,2],ozgur_dist[1],label="Kaynak 2")
    mpl.bar([34,34,44,4,14],ozgur_dist[2],label="Kaynak 3")
    mpl.bar([36,46,6,16,26],ozgur_dist[3],label="Kaynak 4")
    mpl.bar([48,8,18,28,38],ozgur_dist[4],label="Kaynak 5")

    mpl.xlabel("Kaynaklar")
    mpl.ylabel("Mesafeler")
    mpl.title("KKA Mesafeler Tablosu")
    mpl.legend()

    mpl.show()

def make_graph(shortest_path,ozgur_dist):
    a = list(map(int, (str(shortest_path[0]).replace("[","").replace("(","").replace(")","").replace("]","").replace(",","")).split()))
    plot_path = []
    for i in range(len(a)):
        if i%2!=0:
            plot_path.append(a[i]*10)

    mpl.plot(plot_path,[0,2,4,6,8],label="Optimize Edilmiş Yol",linewidth="2",color="k")

    mpl.bar([0,10,20,30,40],ozgur_dist[0],label="Kaynak 1")
    mpl.bar([12,22,32,42,2],ozgur_dist[1],label="Kaynak 2")
    mpl.bar([34,34,44,4,14],ozgur_dist[2],label="Kaynak 3")
    mpl.bar([36,46,6,16,26],ozgur_dist[3],label="Kaynak 4")
    mpl.bar([48,8,18,28,38],ozgur_dist[4],label="Kaynak 5")

    mpl.xlabel("Kaynaklar")
    mpl.ylabel("Mesafeler")
    mpl.title("KKA Tablosu")
    mpl.legend()

    mpl.show()


def cases():
    case = int(input("Hangi örnek? "))
    if case == 1:
        distances = numpy.array([[numpy.inf, 2, 2, 5, 7],
                                 [2, numpy.inf, 4, 8, 2],
                                 [2, 4, numpy.inf, 1, 3],
                                 [5, 8, 1, numpy.inf, 2],
                                 [7, 2, 3, 2, numpy.inf]])
        # Mesafeler, karınca sayısı, feromon veren sayısı, kaç defa çalışacağı, feromonun korunma oranı, feromonun üssü, mesafenin üssü
        ant_colony = Ant_Colony(distances, 1, 1, 100, 0.95, alpha=1, beta=1)

        #Distances
        make_distances_graph(distances)

        shortest_path = ant_colony.run()
        print("En kısa yol: {}".format(shortest_path))
        # Run: N -> Shortest Path -> ([(0, 2), (2, 3), (3, 1), (1, 4), (4, 0)], 20.0) ; 2 + 1 + 8 + 2 + 7 = 20

        #Optimized With Distances
        make_graph(shortest_path,distances)

    elif case == 2:
        ozgur_dist = numpy.array([[numpy.inf, 6, 5, 12, 22],
                                  [6, numpy.inf, 8, 9, 2],
                                  [5, 8, numpy.inf, 5, 3],
                                  [12, 9, 5, numpy.inf, 21],
                                  [22, 2, 3, 21, numpy.inf]])
        ant_colony = Ant_Colony(ozgur_dist, 2, 2, 200, 0.95, alpha=1, beta=2)

        #Distances
        make_distances_graph(ozgur_dist)

        shortest_path = ant_colony.run()
        print("En kısa yol: {}".format(shortest_path))

        #Optimized With Distances
        make_graph(shortest_path,ozgur_dist)
        
    elif case == 3:
        long_case = numpy.array([[numpy.inf, 6, 5, 12, 22,  12, 18, 17, 6],
                                  [6,  numpy.inf,8, 9,  2,   6,  8,  19, 9],
                                  [5,  8, numpy.inf,5,  3,   8,  6,  3,  2],
                                  [12, 9,  5, numpy.inf,21,  19, 12, 22, 14],
                                  [22, 2,  3,  21, numpy.inf,33, 7,  1,  22],
                                  [12, 6,  8,  19, 33, numpy.inf,21, 12, 6],
                                  [18, 8,  6,  12, 7,  21, numpy.inf,21, 21],
                                  [17, 19, 3,  22, 1,  12, 21, numpy.inf, 21],
                                  [6,  9,  2,  14, 22, 6,  21, 21, numpy.inf]])
        ant_colony = Ant_Colony(long_case, 100, 60, 200, 0.45, alpha=1, beta=1)
        # Optimum cevap 54.

        shortest_path = ant_colony.run()
        print("En kısa yol: {}".format(shortest_path))

    else:
        print("Yanlış girdi.")
        cases()


while True:
    cases()
