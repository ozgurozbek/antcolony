import numpy as np

from algorithm import AntColony

"""
Args:
    distances (2D numpy.array): Mesafelerin kare matrisi. Köşegenler np.inf olarak kabul ediliyor.
    n_ants (int): Her iterasyon başına var olan karınca sayısı
    n_best (int): Feromon salgılayabilen karınca sayısı
    n_iteration (int): İterasyon sayısı
    decay (float): Feromonun kaybolma oranı. Bu değer decay ile çarpılıyor, bir nevi feromonun korunma oranı da denebilir. Ne kadar yüksek, o kadar çok feromon.
    alpha (int or float): Feromonun üssü, Ne kadar yüksekse o kadar güçlü feromon. Standart=1
    beta (int or float): Mesafenin üssü, Ne kadar yüksekse o kadar zorlu mesafe. Standart=1

Test:
    ant_colony = AntColony(distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
"""

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])
ant_colony = AntColony(distances, 1, 1, 100, 0.95, alpha=1, beta=1) #mesafeler, karınca sayısı, feromon veren sayısı, kaç defa çalışacağı, feromonun korunma oranı, feromonun üssü, mesafenin üssü

#ozgur_dist = np.array([[np.inf, 6, 5, 12, 22],
#                      [6, np.inf, 8, 9, 2],
#                      [5, 8, np.inf, 5, 3],
#                      [12, 9, 5, np.inf, 21],
#                      [22, 2, 3, 21, np.inf]])
#ant_colony = AntColony(ozgur_dist, 100, 20, 2000, 0.95, alpha=1, beta=2)

shortest_path = ant_colony.run()
print ("En kısa yol: {}".format(shortest_path))