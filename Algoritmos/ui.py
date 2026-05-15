import tkinter as tk
from tkinter import messagebox
from utils import Utils
from controller import Controller
from visuals.barras import Barras
from visuals.arbol import Arbol
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
CURRENT_INDEX = 0


def app():
    from visuals.arbol import Arbol as ArbolClass
    ArbolClass.accent = ACCENT_MERGE

    pausado = False
    ventana = tk.Tk()
    apply_window_style(ventana, "AlgoSort — Merge Sort", 980, 800)

    # ── NAVEGACIÓN ─────────────────────────────────────────────────────────────
    def on_switch(idx):
        ventana.destroy()
        if idx == 0:
            app()
        elif idx == 1:
            from ui_shell import app as shell_app
            shell_app()
        elif idx == 2:
            from ui_radix import app as radix_app
            radix_app()

    make_navbar(ventana, ALGORITHMS, CURRENT_INDEX, on_switch)

    # ── CUERPO ─────────────────────────────────────────────────────────────────
    body = tk.Frame(ventana, bg=BG_DARK)
    body.pack(fill="both", expand=True)

    # Panel izquierdo: controles
    left = tk.Frame(body, bg=BG_DARK, width=260)
    left.pack(side="left", fill="y", padx=(0, 0))
    left.pack_propagate(False)

    tk.Frame(left, bg=BORDER, width=1).pack(side="right", fill="y")

    # Título del algoritmo
    tk.Label(
        left,
        text="MERGE SORT",
        font=("Consolas", 18, "bold"),
        fg=ACCENT_MERGE,
        bg=BG_DARK,
        anchor="w",
        padx=16,
        pady=16,
    ).pack(fill="x")

    tk.Label(
        left,
        text="Divide y vencerás · O(n log n)",
        font=FONT_SMALL,
        fg=TEXT_MUTED,
        bg=BG_DARK,
        anchor="w",
        padx=16,
    ).pack(fill="x")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=10)

    # Entrada de datos
    make_section_label(left, "DATOS DE ENTRADA", ACCENT_MERGE)

    frame_entrada, entrada = make_input_row(left, "Array", entry_width=22, accent=ACCENT_MERGE)
    frame_entrada.pack(fill="x", padx=16, pady=4)

    frame_n, entry_n = make_input_row(left, "N", entry_width=8, accent=ACCENT_MERGE)
    frame_n.pack(padx=16, pady=2)
    entry_n.insert(0, "10")

    btn_gen = make_pill_button(left, "⟳  Generar", lambda: generar(), ACCENT_MERGE, width=18)
    btn_gen.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    # Controles de animación
    make_section_label(left, "ANIMACIÓN", ACCENT_MERGE)

    btn_frame = tk.Frame(left, bg=BG_DARK)
    btn_frame.pack(padx=16, pady=4, fill="x")

    btn_ordenar = make_pill_button(btn_frame, "▶  Ordenar", lambda: ordenar(), ACCENT_MERGE, width=14)
    btn_ordenar.pack(side="left", padx=(0, 6))

    btn_pausa = make_ghost_button(btn_frame, "⏸  Pausa", lambda: toggle_pause(), ACCENT_MERGE)
    btn_pausa.pack(side="left")

    velocidad = tk.IntVar(value=500)
    frame_vel = make_speed_control(left, velocidad, ACCENT_MERGE)
    frame_vel.pack(padx=16, pady=8, anchor="w")

    tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

    # Info
    make_section_label(left, "INFORMACIÓN", ACCENT_MERGE)

    info_text = (
        "Divide el arreglo en mitades\n"
        "recursivamente, luego combina\n"
        "los subarreglos ordenados.\n\n"
        "Visualización:\n"
        "🌳 Árbol de división\n"
        "📊 Barras de combinación"
    )
    tk.Label(
        left,
        text=info_text,
        font=FONT_SMALL,
        fg=TEXT_SECONDARY,
        bg=BG_DARK,
        justify="left",
        padx=16,
        pady=4,
        wraplength=220,
    ).pack(fill="x")

    # ── Panel derecho: visualización ───────────────────────────────────────────
    right = tk.Frame(body, bg=BG_DARK)
    right.pack(side="left", fill="both", expand=True)

    # Etiqueta de estado
    estado_var = tk.StringVar(value="Esperando datos…")
    estado_frame = tk.Frame(right, bg=BG_PANEL, height=36)
    estado_frame.pack(fill="x")
    estado_frame.pack_propagate(False)

    tk.Frame(estado_frame, bg=BORDER, height=1).pack(fill="x", side="bottom")

    estado_label = tk.Label(
        estado_frame,
        textvariable=estado_var,
        font=FONT_BODY,
        fg=ACCENT_MERGE,
        bg=BG_PANEL,
        anchor="w",
        padx=16,
    )
    estado_label.pack(side="left", fill="y")

    # Canvas árbol
    tk.Label(
        right, text="ÁRBOL DE DIVISIÓN",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16, pady=(8, 2),
    ).pack(fill="x")

    canvas_arbol = make_canvas_card(right, 680, 220, accent=ACCENT_MERGE)

    # Canvas barras
    tk.Label(
        right, text="BARRAS DE COMBINACIÓN",
        font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK,
        anchor="w", padx=16, pady=(8, 2),
    ).pack(fill="x")

    canvas_barras = make_canvas_card(right, 680, 240, accent=ACCENT_MERGE)

    # Drag-to-scroll en barras
    def mover_inicio(e):
        canvas_barras.scan_mark(e.x, e.y)

    def mover(e):
        canvas_barras.scan_dragto(e.x, e.y, gain=1)

    def zoom(e):
        factor = 1.1 if e.delta > 0 else 0.9
        canvas_barras.scale("all", e.x, e.y, factor, factor)

    canvas_barras.bind("<ButtonPress-1>", mover_inicio)
    canvas_barras.bind("<B1-Motion>", mover)
    canvas_barras.bind("<MouseWheel>", zoom)

    # ── Barra de estado inferior ───────────────────────────────────────────────
    status_bar, status_label = make_status_bar(ventana, ACCENT_MERGE)

    # ── LÓGICA ─────────────────────────────────────────────────────────────────

    def ingresar_datos():
        try:
            datos = entrada.get().split()
            resultado = []
            for d in datos:
                try:
                    resultado.append(float(d))
                except Exception:
                    resultado.append(d)
            return resultado
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

    def animar(pasos, i=0):
        if pausado:
            ventana.after(200, lambda: animar(pasos, i))
            return

        if i >= len(pasos):
            estado_var.set("✔  Ordenamiento completado")
            status_label.config(text=f"Finalizado — {len(pasos)} pasos")
            Barras.color_primario = Barras.color_ok
            return

        tipo, data = pasos[i]

        if tipo == "nodo":
            estado_var.set("🌳  Dividiendo…")
            Arbol.dibujar(canvas_arbol, data)

        else:
            if tipo == "merge":
                estado_var.set("🔄  Combinando subarreglos…")
                Barras.color_primario = ACCENT_MERGE
            elif tipo == "comparar":
                estado_var.set("⚖️  Comparando elementos…")
                Barras.color_primario = "#f0c060"
            elif tipo == "resultado":
                estado_var.set("✅  Resultado parcial")
                Barras.color_primario = ACCENT_SHELL

            Barras.dibujar(canvas_barras, data)
            canvas_barras.xview_moveto(0)
            canvas_barras.yview_moveto(0)

        status_label.config(text=f"Paso {i+1} / {len(pasos)}")
        ventana.after(velocidad.get(), lambda: animar(pasos, i + 1))

    def ordenar():
        datos = ingresar_datos()
        if not datos:
            return

        if Utils.esta_ordenado(datos):
            messagebox.showinfo("Info", "El arreglo ya está ordenado")
            return

        Arbol.reset()
        Barras.color_primario = ACCENT_MERGE
        canvas_arbol.delete("all")
        canvas_barras.delete("all")

        pasos = Controller.obtener_pasos(datos)
        estado_var.set("▶  Iniciando…")
        status_label.config(text=f"Procesando {len(datos)} elementos…")
        animar(pasos)

    ventana.mainloop()
