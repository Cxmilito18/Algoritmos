def radix_sort(arr):
    pasos = []
    if not arr:
        return pasos

    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        # 10 cubetas vacías (dígitos 0-9)
        buckets = [[] for _ in range(10)]

        # Distribuir según el dígito actual
        for num in arr:
            index = (num // exp) % 10
            buckets[index].append(num)

        # Guardar snapshot de las cubetas en este paso
        # (copia de cada lista para que no muten en la siguiente iteración)
        pasos.append([bucket.copy() for bucket in buckets])

        # Reconstruir el array aplanando las cubetas
        arr = [num for bucket in buckets for num in bucket]

        # Avanzar al siguiente dígito
        exp *= 10

    return pasos