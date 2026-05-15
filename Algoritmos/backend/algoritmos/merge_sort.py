def merge_sort(arr):
    pasos = []

    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m

        L = arr[l:m+1]
        R = arr[m+1:r+1]

        i = j = 0
        k = l

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            pasos.append(arr.copy())

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            pasos.append(arr.copy())

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            pasos.append(arr.copy())

    def sort(l, r):
        if l < r:
            m = (l + r) // 2
            sort(l, m)
            sort(m + 1, r)
            merge(arr, l, m, r)

    sort(0, len(arr) - 1)
    return pasos