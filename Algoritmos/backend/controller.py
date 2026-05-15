from algoritmos.merge_sort import merge_sort
from algoritmos.radix_sort import radix_sort
from algoritmos.bucket_sort import bucket_sort


def ordenar_algoritmo(valores, algoritmo):
    if algoritmo == "merge":
        return merge_sort(valores.copy())
    elif algoritmo == "radix":
        return radix_sort(valores.copy())
    elif algoritmo == "bucket":
        return bucket_sort(valores.copy())
    else:
        return []