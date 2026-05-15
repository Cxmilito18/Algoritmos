import copy


def bucket_sort(arr):
    pasos = []
    if not arr:
        return pasos

    max_val = max(arr)
    size = max_val / len(arr)
    buckets = [[] for _ in range(len(arr))]

    # Distribuir cada número en su cubeta
    for num in arr:
        index = int(num / size)
        if index != len(arr):
            buckets[index].append(num)
        else:
            buckets[len(arr) - 1].append(num)

    # Paso 1: snapshot de cubetas recién distribuidas
    # deepcopy es OBLIGATORIO — sin él ambos pasos apuntan al mismo objeto
    # y cuando ordenas abajo, el paso 1 también queda ordenado
    pasos.append(copy.deepcopy(buckets))

    # Ordenar cada cubeta individualmente
    for bucket in buckets:
        bucket.sort()

    # Paso 2: cubetas ya ordenadas internamente
    pasos.append(copy.deepcopy(buckets))

    return pasos