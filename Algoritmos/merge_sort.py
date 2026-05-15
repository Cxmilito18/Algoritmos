class MergeSort:

    @staticmethod
    def ordenar(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr)//2
        left = MergeSort.ordenar(arr[:mid])
        right = MergeSort.ordenar(arr[mid:])

        return MergeSort.merge(left, right)

    @staticmethod
    def clave(x):
        if isinstance(x, (int, float)):
            return (0, x)  # números primero
        else:
            return (1, str(x))  # luego strings

    @staticmethod
    def merge(l, r):
        result = []
        i = j = 0

        while i < len(l) and j < len(r):
            if MergeSort.clave(l[i]) < MergeSort.clave(r[j]):
                result.append(l[i])
                i += 1
            else:
                result.append(r[j])
                j += 1

        result += l[i:]
        result += r[j:]

        return result