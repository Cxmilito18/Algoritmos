import time
import matplotlib.pyplot as plt
from merge_sort import MergeSort
from utils import Utils

class Graficas:

    @staticmethod
    def graficar():
        tamanos = [10, 100, 300, 500, 1000]
        tiempos = []

        for n in tamanos:
            datos = Utils.generar_datos(n)

            inicio = time.time()
            MergeSort.ordenar(datos.copy())
            fin = time.time()

            tiempos.append(fin - inicio)

        plt.plot(tamanos, tiempos)
        plt.xlabel("Tamaño de datos (n)")
        plt.ylabel("Tiempo (s)")
        plt.title("Rendimiento Merge Sort")
        plt.show()