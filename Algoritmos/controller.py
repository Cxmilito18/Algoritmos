class Controller:

    @staticmethod
    def obtener_pasos(arr):
        pasos = []

        def ordenar(a, nivel=0, pos=0, padre=None):

            nodo = {
                "arr": a,
                "nivel": nivel,
                "pos": pos,
                "padre": padre
            }

            pasos.append(("nodo", nodo))

            if len(a) <= 1:
                return a

            mid = len(a)//2

            left = ordenar(a[:mid], nivel+1, pos-1, nodo)
            right = ordenar(a[mid:], nivel+1, pos+1, nodo)

            return merge(left, right)

        # 🔥 COMPARADOR PRO (BIEN INDENTADO)
        def clave(x):
            if isinstance(x, (int, float)):
                return (0, x)
            else:
                return (1, str(x))

        # 🔥 MERGE USANDO CLAVE
        def merge(l, r):
            result = []
            i = j = 0

            pasos.append(("merge", l + r))

            while i < len(l) and j < len(r):
                if clave(l[i]) < clave(r[j]):
                    result.append(l[i])
                    i += 1
                else:
                    result.append(r[j])
                    j += 1

                pasos.append(("comparar", result + l[i:] + r[j:]))

            result += l[i:]
            result += r[j:]

            pasos.append(("resultado", result))

            return result

        ordenar(arr.copy())
        return pasos