def bucket_sort(arr):
    pasos = []
    if not arr:
        return pasos

    max_val = max(arr)
    size = max_val / len(arr)
    buckets = [[] for _ in range(len(arr))]

    for num in arr:
        index = int(num / size)
        if index != len(arr):
            buckets[index].append(num)
        else:
            buckets[len(arr) - 1].append(num)
    pasos.append(buckets)

    for bucket in buckets:
        bucket.sort()
    pasos.append(buckets)

    return pasos
