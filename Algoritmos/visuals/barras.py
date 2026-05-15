from theme import (
    BG_DARK, ACCENT_MERGE, ACCENT_SHELL, ACCENT_RADIX,
    TEXT_PRIMARY, TEXT_MUTED, BORDER
)


class Barras:

    color_primario = ACCENT_MERGE
    color_comparar = "#f0c060"
    color_ok       = "#22d3a0"

    @staticmethod
    def dibujar(canvas, arr, highlight_indices=None, color_override=None):
        canvas.delete("all")

        if not arr:
            return

        alto = int(canvas["height"])
        ancho = max(860, len(arr) * 36)

        n = len(arr)
        ancho_barra = ancho / n
        padding_h = 4

        altura_max = alto * 0.72
        altura_min = 12

        nums = [v for v in arr if isinstance(v, (int, float))]
        letras = [v for v in arr if not isinstance(v, (int, float))]

        max_num = max(nums) if nums else 1
        min_num = min(nums) if nums else 0
        rango_num = max_num - min_num if max_num != min_num else 1

        letras_ascii = [ord(str(v)[0]) for v in letras] if letras else [1]
        max_let = max(letras_ascii) if letras_ascii else 1
        min_let = min(letras_ascii) if letras_ascii else 0
        rango_let = max_let - min_let if max_let != min_let else 1

        accent = color_override or Barras.color_primario

        for i, val in enumerate(arr):
            x0 = i * ancho_barra + padding_h
            x1 = (i + 1) * ancho_barra - padding_h

            if isinstance(val, (int, float)):
                escala = (val - min_num) / rango_num
                color = accent
            else:
                ascii_val = ord(str(val)[0])
                escala = (ascii_val - min_let) / rango_let
                color = ACCENT_RADIX

            if highlight_indices and i in highlight_indices:
                color = Barras.color_comparar

            altura = altura_min + (escala * (altura_max - altura_min))
            y0 = alto - altura
            y1 = alto - 2

            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="", width=0)

            highlight_h = max(4, altura * 0.15)
            canvas.create_rectangle(
                x0, y0, x1, y0 + highlight_h,
                fill=_lighten(color), outline="", width=0
            )

            canvas.create_text(
                x0 + (x1 - x0) / 2, y0 - 7,
                text=str(val), font=("Consolas", 8), fill=TEXT_PRIMARY,
            )

            canvas.create_text(
                x0 + (x1 - x0) / 2, alto - 10,
                text=str(i), font=("Consolas", 7), fill=TEXT_MUTED,
            )

        canvas.config(scrollregion=canvas.bbox("all") or (0, 0, ancho, alto))


def _lighten(hex_color):
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = min(255, r + 40)
        g = min(255, g + 40)
        b = min(255, b + 40)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color
