

import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

from pylab import plot, title, show , legend, grid, xlabel, ylabel

listaConsolidada = [
	{'region': 'Sul', 'university': 3.0, 'bank': 25.0, 'occupied_private_housing': 48927.0, 'lng': -976.2406893536584, 'shopping': 1.0, 'ubs': 8.0, 'delegacy': 2.0, 'hospital': 1.0, 'lat': -486.01751130731725, 'upa': 3.0, 'market': 13.0, 'qtd': 21, 'residents': 163862.0, 'school': 29.0, 'residents_per_household': 70.29999999999998, 'price_by_meter': 3730.5917276622044} ,
	{'region': 'Oeste', 'university': 2.0, 'bank': 9.0, 'occupied_private_housing': 11813.0, 'lng': -232.43825936991865, 'shopping': 0.0, 'ubs': 1.0, 'delegacy': 1.0, 'hospital': 0.0, 'lat': -115.71845507317073, 'upa': 0.0, 'market': 4.0, 'qtd': 5, 'residents': 35326.0, 'school': 11.0, 'residents_per_household': 15.100000000000001, 'price_by_meter': 5324.674376240277} ,
	{'region': 'Leste', 'university': 0.0, 'bank': 5.0, 'occupied_private_housing': 36229.0, 'lng': -1115.7036449756094, 'shopping': 0.0, 'ubs': 13.0, 'delegacy': 1.0, 'hospital': 1.0, 'lat': -555.4485843512197, 'upa': 2.0, 'market': 15.0, 'qtd': 24, 'residents': 125809.0, 'school': 19.0, 'residents_per_household': 82.90000000000002, 'price_by_meter': 3244.0327032589935} ,
	{'region': 'Sudeste', 'university': 0.0, 'bank': 1.0, 'occupied_private_housing': 8592.0, 'lng': -418.3888668658536, 'shopping': 0.0, 'ubs': 2.0, 'delegacy': 0.0, 'hospital': 0.0, 'lat': -208.29321913170736, 'upa': 0.0, 'market': 4.0, 'qtd': 9, 'residents': 30464.0, 'school': 4.0, 'residents_per_household': 31.7, 'price_by_meter': 2833.4061504412543} ,
	{'region': 'Norte', 'university': 1.0, 'bank': 5.0, 'occupied_private_housing': 14743.0, 'lng': -650.8271262357722, 'shopping': 0.0, 'ubs': 4.0, 'delegacy': 1.0, 'hospital': 1.0, 'lat': -324.01167420487815, 'upa': 1.0, 'market': 5.0, 'qtd': 14, 'residents': 50073.0, 'school': 8.0, 'residents_per_household': 46.900000000000006, 'price_by_meter': 3066.7589758047243} ,
	{'region': 'Centro', 'university': 4.0, 'bank': 26.0, 'occupied_private_housing': 16687.0, 'lng': -790.2900818577234, 'shopping': 1.0, 'ubs': 3.0, 'delegacy': 5.0, 'hospital': 1.0, 'lat': -393.4427472487806, 'upa': 0.0, 'market': 8.0, 'qtd': 17, 'residents': 49643.0, 'school': 20.0, 'residents_per_household': 50.5, 'price_by_meter': 4604.609680237176}
]

l = []
for i in listaConsolidada:
	l.append(i['occupied_private_housing'])

# x = np.arange(min, 120, 0.4)

# print()

x = l

y = scipy.stats.norm.pdf(x, 2,1)
plot(x, y, 'r.')

plt.show()