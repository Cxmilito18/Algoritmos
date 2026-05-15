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
CURRENT_INDEX = 1


def app():
    Barras.color_primario = ACCENT_SHELL

    pausado = False
    pasos = []

    ventana = tk.Tk()
    apply_window_style(ventana, "AlgoSort — Shell Sort", 980, 800)

    # ── NAVEGACIÓN ─────────────────────────────────────────────────────────────
    def on_switch(idx):
        ventana.destroy()
        if idx == 0:
            from ui import app as merge_app
            merge_app()
        elif idx == 1:
            app()
        elif idx == 2:
            from ui_radix import app as radix_app
            radix_app()

    make_navbar(ventana, ALGORITHMS, CURRENT_INDEX, on_switch)

    # ── ALGORITMO ──────────────────────────────────────────────────────────────
    def shell_sort(arr):
        resultado = []
        n = len(arr)
        gap = n // 2

        while gap > 0:
            resultado.append(("gap", gap, arr.copy()))

            for i in range(gap, n):
                temp = arr[i]
                j = i

                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    resultado.append(("comparar", gap, arr.copy(), j, j - gap))
                    j -= gap

                arr[j] = temp
                resultado.append(("insertar", gap, arr.copy(), j))

            gap //= 2

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
        left, text="SHELL SORT",
        font=("Consolas", 18, "bold"),
        fg=ACCENT_SHELL, bg=BG_DARK,
        anchor="w", padx=16, pady=16,
    ).pack(fill="x")

    tk.Label(
        left, text="Gaps decrecientes · O(n log² n)",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16,
    ).pack(fill="x")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=10)

    make_section_label(left, "DATOS DE ENTRADA", ACCENT_SHELL)

    frame_entrada, entrada = make_input_row(left, "Array", entry_width=22, accent=ACCENT_SHELL)
    frame_entrada.pack(fill="x", padx=16, pady=4)

    frame_n, entry_n = make_input_row(left, "N", entry_width=8, accent=ACCENT_SHELL)
    frame_n.pack(padx=16, pady=2)
    entry_n.insert(0, "10")

    btn_gen = make_pill_button(left, "⟳  Generar", lambda: generar(), ACCENT_SHELL, width=18)
    btn_gen.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    make_section_label(left, "ANIMACIÓN", ACCENT_SHELL)

    btn_frame = tk.Frame(left, bg=BG_DARK)
    btn_frame.pack(padx=16, pady=4, fill="x")

    btn_ordenar = make_pill_button(btn_frame, "▶  Ordenar", lambda: ordenar(), ACCENT_SHELL, width=14)
    btn_ordenar.pack(side="left", padx=(0, 6))

    btn_pausa = make_ghost_button(btn_frame, "⏸  Pausa", lambda: toggle_pause(), ACCENT_SHELL)
    btn_pausa.pack(side="left")

    velocidad = tk.IntVar(value=500)
    frame_vel = make_speed_control(left, velocidad, ACCENT_SHELL)
    frame_vel.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    make_section_label(left, "GAP ACTUAL", ACCENT_SHELL)

    gap_label = tk.Label(
        left, text="—",
        font=("Consolas", 28, "bold"),
        fg=ACCENT_SHELL, bg=BG_DARK,
        anchor="w", padx=24,
    )
    gap_label.pack(fill="x")

    tk.Label(
        left, text="distancia entre comparaciones",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=24,
    ).pack(fill="x")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=10)

    info_text = (
        "Compara elementos separados\n"
        "por un gap que se reduce a\n"
        "la mitad cada iteración.\n\n"
        "Eficiente en arrays casi\n"
        "ordenados."
    )
    tk.Label(
        left, text=info_text,
        font=FONT_SMALL, fg=TEXT_SECONDARY, bg=BG_DARK,
        justify="left", padx=16, pady=4, wraplength=220,
    ).pack(fill="x")

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
        font=FONT_BODY, fg=ACCENT_SHELL, bg=BG_PANEL,
        anchor="w", padx=16,
    ).pack(side="left", fill="y")

    tk.Label(
        right, text="VISUALIZACIÓN DE BARRAS",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16, pady=(16, 2),
    ).pack(fill="x")

    canvas = make_canvas_card(right, 680, 400, accent=ACCENT_SHELL)

    status_bar, status_label = make_status_bar(ventana, ACCENT_SHELL)

    # ── LÓGICA ─────────────────────────────────────────────────────────────────

    def ingresar_datos():
        try:
            return list(map(float, entrada.get().split()))
        except Exception:
            messagebox.showerror("Error", "Entrada inválida")
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

    def animar(i=0):
        if pausado:
            ventana.after(200, lambda: animar(i))
            return

        if i >= len(pasos):
            estado_var.set("✔  Ordenamiento completado")
            status_label.config(text=f"Finalizado — {len(pasos)} pasos")
            Barras.color_primario = Barras.color_ok
            Barras.dibujar(canvas, pasos[-1][2] if pasos else [])
            return

        paso = pasos[i]
        tipo = paso[0]

        if tipo == "gap":
            gap_val = paso[1]
            arr = paso[2]
            gap_label.config(text=str(gap_val))
            estado_var.set(f"⚡  Gap = {gap_val}")
            Barras.color_primario = ACCENT_SHELL
            Barras.dibujar(canvas, arr)

        elif tipo == "comparar":
            gap_val, arr, a, b = paso[1:]
            estado_var.set(f"🔍  Comparando [{a}] ↔ [{b}]")
            Barras.dibujar(canvas, arr, highlight_indices={a, b}, color_override=ACCENT_SHELL)

        elif tipo == "insertar":
            gap_val, arr, pos = paso[1:]
            estado_var.set(f"📥  Insertando en [{pos}]")
            Barras.dibujar(canvas, arr, highlight_indices={pos}, color_override="#f0c060")

        status_label.config(text=f"Paso {i+1} / {len(pasos)}")
        ventana.after(velocidad.get(), lambda: animar(i + 1))

    def ordenar():
        nonlocal pasos

        datos = ingresar_datos()
        if not datos:
            return

        pasos = shell_sort(datos)
        Barras.color_primario = ACCENT_SHELL
        canvas.delete("all")
        gap_label.config(text="—")
        estado_var.set("▶  Iniciando…")
        status_label.config(text=f"Procesando {len(datos)} elementos…")
        animar()

    ventana.mainloop()
