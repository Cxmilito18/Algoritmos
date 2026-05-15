from theme import (
    BG_DARK, ACCENT_MERGE, TEXT_PRIMARY, TEXT_MUTED, BORDER, BG_CARD
)


class Arbol:

    nodos = []
    accent = ACCENT_MERGE

    @staticmethod
    def reset():
        Arbol.nodos = []

    @staticmethod
    def dibujar(canvas, nodo):
        Arbol.nodos.append(nodo)
        canvas.delete("all")

        ancho = int(canvas["width"])

        niveles = {}
        for n in Arbol.nodos:
            lvl = n["nivel"]
            if lvl not in niveles:
                niveles[lvl] = []
            niveles[lvl].append(n)

        posiciones = {}
        for lvl, nodos_nivel in niveles.items():
            cantidad = len(nodos_nivel)
            for i, n in enumerate(nodos_nivel):
                x = (i + 1) * (ancho // (cantidad + 1))
                y = 50 + lvl * 80
                posiciones[id(n)] = (x, y)

        # Conexiones
        for n in Arbol.nodos:
            if n["padre"] and id(n["padre"]) in posiciones and id(n) in posiciones:
                x1, y1 = posiciones[id(n["padre"])]
                x2, y2 = posiciones[id(n)]
                canvas.create_line(x1, y1, x2, y2, fill=BORDER, width=1, dash=(4, 3))

        # Nodos
        accent = Arbol.accent
        for n in Arbol.nodos:
            if id(n) not in posiciones:
                continue
            x, y = posiciones[id(n)]
            r = 24

            # Sombra
            canvas.create_oval(x-r+2, y-r+2, x+r+2, y+r+2, fill="#00000044", outline="")
            # Nodo relleno
            canvas.create_oval(x-r, y-r, x+r, y+r, fill=accent, outline=BG_DARK, width=2)

            texto = str(n["arr"])
            if len(texto) > 10:
                texto = texto[:9] + "…"

            canvas.create_text(
                x, y, text=texto,
                fill=TEXT_PRIMARY,
                font=("Consolas", 7, "bold"),
            )

        canvas.config(scrollregion=canvas.bbox("all") or (0, 0, ancho, 400))
