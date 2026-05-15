def merge_sort(arr):
    pasos = []

    def dividir(lista):
        if len(lista) <= 1:
            nodo = {"valor": lista}
            pasos.append(nodo.copy())
            return nodo
        mid = len(lista) // 2
        izquierda = dividir(lista[:mid])
        derecha = dividir(lista[mid:])
        nodo = {"valor": lista, "izquierda": izquierda, "derecha": derecha}
        pasos.append(nodo.copy())
        return nodo

    arbol = dividir(arr)
    pasos.append(arbol)
    return pasos
