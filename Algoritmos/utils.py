import random

class Utils:

    @staticmethod
    def ingresar_datos():
        datos = input("Ingrese números separados por espacios: ")
        return list(map(int, datos.split()))

    @staticmethod
    def generar_datos(n):
        return [random.randint(1, 10000) for _ in range(n)]

    @staticmethod
    def esta_ordenado(arr):
        return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))