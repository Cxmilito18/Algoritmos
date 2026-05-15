def radix_sort(arr):
    pasos = []
    if not arr:
        return pasos

    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        # Crear 10 cubetas vacías
        buckets = [[] for _ in range(10)]

        # Colocar cada número en la cubeta según el dígito actual
        for num in arr:
            index = (num // exp) % 10
            buckets[index].append(num)

        # Guardar snapshot de las cubetas en este paso
        pasos.append([bucket.copy() for bucket in buckets])

        # Reconstruir el arreglo concatenando las cubetas
        arr = [num for bucket in buckets for num in bucket]

        # Guardar snapshot del arreglo reconstruido (para las barras)
        pasos.append(arr.copy())

        # Pasar al siguiente dígito
        exp *= 10

    return pasos
