import tkinter as tk
from tkinter import messagebox
from utils import Utils
from visuals.barras import Barras
from theme import *
from components import (
    apply_window_style, make_navbar, make_section_label,
    make_pill_button, make_ghost_button, make_input_row,
    make_status_bar, make_speed_control, make_canvas_card,
)

ALGORITHMS = [
    {"label": "Merge Sort",  "accent": ACCENT_MERGE},
    {"label": "Shell Sort",  "accent": ACCENT_SHELL},
    {"label": "Radix Sort",  "accent": ACCENT_RADIX},
]
CURRENT_INDEX = 2


def app():
    Barras.color_primario = ACCENT_RADIX

    pausado = False
    pasos = []

    ventana = tk.Tk()
    apply_window_style(ventana, "AlgoSort — Radix Sort", 980, 800)

    # ── NAVEGACIÓN ─────────────────────────────────────────────────────────────
    def on_switch(idx):
        ventana.destroy()
        if idx == 0:
            from ui import app as merge_app
            merge_app()
        elif idx == 1:
            from ui_shell import app as shell_app
            shell_app()
        elif idx == 2:
            app()

    make_navbar(ventana, ALGORITHMS, CURRENT_INDEX, on_switch)

    # ── ALGORITMO ──────────────────────────────────────────────────────────────
    def counting_sort_steps(arr, exp):
        count = [[] for _ in range(10)]
        resultado = []

        for num in arr:
            index = (num // exp) % 10
            count[index].append(num)
            resultado.append(("bucket", exp, [list(b) for b in count]))

        i = 0
        for bucket in count:
            for num in bucket:
                arr[i] = num
                i += 1
                resultado.append(("ordenando", exp, arr.copy()))

        return resultado

    def radix_sort(arr):
        resultado = []
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            resultado += counting_sort_steps(arr, exp)
            exp *= 10
        return resultado

    # ── CUERPO ─────────────────────────────────────────────────────────────────
    body = tk.Frame(ventana, bg=BG_DARK)
    body.pack(fill="both", expand=True)

    # Panel izquierdo
    left = tk.Frame(body, bg=BG_DARK, width=260)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    tk.Frame(left, bg=BORDER, width=1).pack(side="right", fill="y")

    tk.Label(
        left, text="RADIX SORT",
        font=("Consolas", 18, "bold"),
        fg=ACCENT_RADIX, bg=BG_DARK,
        anchor="w", padx=16, pady=16,
    ).pack(fill="x")

    tk.Label(
        left, text="Dígito a dígito · O(nk)",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16,
    ).pack(fill="x")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=10)

    make_section_label(left, "DATOS DE ENTRADA", ACCENT_RADIX)

    frame_entrada, entrada = make_input_row(left, "Array", entry_width=22, accent=ACCENT_RADIX)
    frame_entrada.pack(fill="x", padx=16, pady=4)

    tk.Label(
        left, text="(Solo enteros positivos)",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16,
    ).pack(fill="x")

    frame_n, entry_n = make_input_row(left, "N", entry_width=8, accent=ACCENT_RADIX)
    frame_n.pack(padx=16, pady=4)
    entry_n.insert(0, "10")

    btn_gen = make_pill_button(left, "⟳  Generar", lambda: generar(), ACCENT_RADIX, width=18)
    btn_gen.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    make_section_label(left, "ANIMACIÓN", ACCENT_RADIX)

    btn_frame = tk.Frame(left, bg=BG_DARK)
    btn_frame.pack(padx=16, pady=4, fill="x")

    btn_ordenar = make_pill_button(btn_frame, "▶  Ordenar", lambda: ordenar(), ACCENT_RADIX, width=14)
    btn_ordenar.pack(side="left", padx=(0, 6))

    btn_pausa = make_ghost_button(btn_frame, "⏸  Pausa", lambda: toggle_pause(), ACCENT_RADIX)
    btn_pausa.pack(side="left")

    velocidad = tk.IntVar(value=400)
    frame_vel = make_speed_control(left, velocidad, ACCENT_RADIX)
    frame_vel.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    make_section_label(left, "BUCKETS (0–9)", ACCENT_RADIX)

    buckets_label = tk.Label(
        left,
        text="",
        justify="left",
        font=("Consolas", 9),
        fg=ACCENT_RADIX,
        bg=BG_DARK,
        padx=16,
        pady=4,
    )
    buckets_label.pack(fill="x")

    # Panel derecho
    right = tk.Frame(body, bg=BG_DARK)
    right.pack(side="left", fill="both", expand=True)

    estado_var = tk.StringVar(value="Esperando datos…")
    estado_frame = tk.Frame(right, bg=BG_PANEL, height=36)
    estado_frame.pack(fill="x")
    estado_frame.pack_propagate(False)
    tk.Frame(estado_frame, bg=BORDER, height=1).pack(fill="x", side="bottom")

    tk.Label(
        estado_frame, textvariable=estado_var,
        font=FONT_BODY, fg=ACCENT_RADIX, bg=BG_PANEL,
        anchor="w", padx=16,
    ).pack(side="left", fill="y")

    tk.Label(
        right, text="VISUALIZACIÓN DE BARRAS",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16, pady=(16, 2),
    ).pack(fill="x")

    canvas = make_canvas_card(right, 680, 380, accent=ACCENT_RADIX)

    status_bar, status_label = make_status_bar(ventana, ACCENT_RADIX)

    # ── LÓGICA ─────────────────────────────────────────────────────────────────

    def ingresar_datos():
        try:
            return list(map(int, entrada.get().split()))
        except Exception:
            messagebox.showerror("Error", "Solo enteros positivos")
            return []

    def generar():
        try:
            n = int(entry_n.get())
            datos = Utils.generar_datos(n)
            entrada.delete(0, tk.END)
            entrada.insert(0, " ".join(map(str, datos)))
            status_label.config(text=f"Generados {n} datos aleatorios")
        except Exception:
            messagebox.showerror("Error", "Número inválido")

    def toggle_pause():
        nonlocal pausado
        pausado = not pausado
        if pausado:
            estado_var.set("⏸  Pausado")
            btn_pausa.config(text="▶  Reanudar")
        else:
            estado_var.set("▶  Animando…")
            btn_pausa.config(text="⏸  Pausa")

    def mostrar_buckets(buckets):
        lines = []
        for i, bucket in enumerate(buckets):
            marker = "▶" if bucket else " "
            lines.append(f"{marker} [{i}] {bucket}")
        buckets_label.config(text="\n".join(lines))

    def animar(i=0):
        if pausado:
            ventana.after(200, lambda: animar(i))
            return

        if i >= len(pasos):
            estado_var.set("✔  Ordenamiento completado")
            status_label.config(text=f"Finalizado — {len(pasos)} pasos")
            Barras.color_primario = Barras.color_ok
            return

        paso = pasos[i]
        tipo = paso[0]

        if tipo == "bucket":
            exp = paso[1]
            buckets = paso[2]
            estado_var.set(f"🔢  Distribuyendo — dígito ×{exp}")
            mostrar_buckets(buckets)

        elif tipo == "ordenando":
            exp = paso[1]
            arr = paso[2]
            estado_var.set(f"📦  Reconstruyendo — dígito ×{exp}")
            Barras.color_primario = ACCENT_RADIX
            Barras.dibujar(canvas, arr)

        status_label.config(text=f"Paso {i+1} / {len(pasos)}")
        ventana.after(velocidad.get(), lambda: animar(i + 1))

    def ordenar():
        nonlocal pasos

        datos = ingresar_datos()
        if not datos:
            return

        pasos = radix_sort(datos)
        Barras.color_primario = ACCENT_RADIX
        canvas.delete("all")
        buckets_label.config(text="")
        estado_var.set("▶  Iniciando…")
        status_label.config(text=f"Procesando {len(datos)} elementos…")
        animar()

    ventana.mainloop()
