# components.py — Widgets reutilizables con el nuevo diseño

import tkinter as tk
from theme import *


def apply_window_style(ventana, title, width=960, height=760):
    """Configura ventana principal con el diseño dark."""
    ventana.title(title)
    ventana.geometry(f"{width}x{height}")
    ventana.configure(bg=BG_DARK)
    ventana.resizable(True, True)
    # Centrar en pantalla
    ventana.update_idletasks()
    sw = ventana.winfo_screenwidth()
    sh = ventana.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    ventana.geometry(f"{width}x{height}+{x}+{y}")


def make_navbar(parent, algorithms, current_index, on_switch):
    """
    Barra de navegación superior con tabs por algoritmo.
    algorithms: lista de dicts {label, accent}
    on_switch: callback(index)
    """
    nav = tk.Frame(parent, bg=BG_PANEL, height=50)
    nav.pack(fill="x", side="top")
    nav.pack_propagate(False)

    # Logo
    tk.Label(
        nav,
        text="AlgoSort",
        font=("Consolas", 14, "bold"),
        fg=TEXT_PRIMARY,
        bg=BG_PANEL,
        padx=16,
    ).pack(side="left")

    # Separador vertical
    tk.Frame(nav, bg=BORDER, width=1).pack(side="left", fill="y", pady=8)

    # Tabs
    for i, algo in enumerate(algorithms):
        is_active = i == current_index
        accent = algo["accent"]

        btn = tk.Button(
            nav,
            text=algo["label"],
            font=FONT_LABEL,
            fg=accent if is_active else TEXT_SECONDARY,
            bg=BG_PANEL,
            activebackground=BG_PANEL,
            activeforeground=accent,
            relief="flat",
            bd=0,
            padx=18,
            pady=0,
            cursor="hand2",
            command=lambda idx=i: on_switch(idx),
        )
        btn.pack(side="left", fill="y")

        if is_active:
            # Underline indicator
            indicator = tk.Frame(nav, bg=accent, height=2)
            indicator.place(in_=btn, relx=0, rely=1.0, relwidth=1, y=-2)

    # Espaciador + badge algoritmo activo
    tk.Label(
        nav,
        text=algorithms[current_index]["label"].upper(),
        font=("Consolas", 9, "bold"),
        fg=TEXT_MUTED,
        bg=BG_PANEL,
        padx=16,
    ).pack(side="right")

    # Línea divisoria inferior
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

    return nav


def make_section_label(parent, text, accent=ACCENT_MERGE):
    """Etiqueta de sección con decoración."""
    frame = tk.Frame(parent, bg=BG_DARK)
    frame.pack(fill="x", padx=16, pady=(12, 4))

    tk.Frame(frame, bg=accent, width=3, height=14).pack(side="left")
    tk.Label(
        frame,
        text=f"  {text}",
        font=FONT_HEADING,
        fg=TEXT_SECONDARY,
        bg=BG_DARK,
    ).pack(side="left")

    return frame


def make_pill_button(parent, text, command, accent, width=14):
    """Botón con estilo de píldora / chip."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BODY,
        fg=BG_DARK,
        bg=accent,
        activebackground=accent,
        activeforeground=BG_DARK,
        relief="flat",
        bd=0,
        padx=16,
        pady=6,
        cursor="hand2",
        width=width,
    )
    return btn


def make_ghost_button(parent, text, command, accent=TEXT_SECONDARY):
    """Botón outline / ghost."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BODY,
        fg=accent,
        bg=BG_CARD,
        activebackground=BG_INPUT,
        activeforeground=accent,
        relief="flat",
        bd=1,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=14,
        pady=5,
        cursor="hand2",
    )
    return btn


def make_input_row(parent, label_text, entry_width=40, accent=ACCENT_MERGE):
    """Fila con label + entrada estilizada."""
    frame = tk.Frame(parent, bg=BG_DARK)

    tk.Label(
        frame,
        text=label_text,
        font=FONT_LABEL,
        fg=TEXT_SECONDARY,
        bg=BG_DARK,
        anchor="w",
    ).pack(side="left", padx=(0, 8))

    entry = tk.Entry(
        frame,
        width=entry_width,
        font=FONT_BODY,
        bg=BG_INPUT,
        fg=TEXT_PRIMARY,
        insertbackground=accent,
        relief="flat",
        bd=0,
        highlightbackground=BORDER,
        highlightthickness=1,
        highlightcolor=accent,
    )
    entry.pack(side="left", ipady=5, padx=2)

    return frame, entry


def make_status_bar(parent, accent=ACCENT_MERGE):
    """Barra de estado inferior."""
    bar = tk.Frame(parent, bg=BG_PANEL, height=32)
    bar.pack(fill="x", side="bottom")
    bar.pack_propagate(False)

    tk.Frame(bar, bg=BORDER, height=1).pack(fill="x", side="top")

    label = tk.Label(
        bar,
        text="Listo",
        font=FONT_SMALL,
        fg=TEXT_MUTED,
        bg=BG_PANEL,
        anchor="w",
        padx=16,
    )
    label.pack(side="left", fill="y")

    return bar, label


def make_speed_control(parent, variable, accent=ACCENT_MERGE):
    """Control de velocidad con label."""
    frame = tk.Frame(parent, bg=BG_DARK)

    tk.Label(
        frame,
        text="Velocidad",
        font=FONT_LABEL,
        fg=TEXT_SECONDARY,
        bg=BG_DARK,
    ).pack(side="left", padx=(0, 8))

    scale = tk.Scale(
        frame,
        from_=100,
        to=1500,
        orient="horizontal",
        variable=variable,
        bg=BG_DARK,
        fg=TEXT_PRIMARY,
        troughcolor=BG_INPUT,
        activebackground=accent,
        highlightthickness=0,
        bd=0,
        length=160,
        showvalue=False,
    )
    scale.pack(side="left")

    val_label = tk.Label(
        frame,
        textvariable=variable,
        font=FONT_SMALL,
        fg=TEXT_MUTED,
        bg=BG_DARK,
        width=5,
    )
    val_label.pack(side="left")

    tk.Label(frame, text="ms", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK).pack(side="left")

    return frame


def make_canvas_card(parent, width, height, label="", accent=ACCENT_MERGE):
    """Canvas dentro de un card con borde."""
    outer = tk.Frame(parent, bg=BG_CARD, bd=0, highlightbackground=BORDER, highlightthickness=1)
    outer.pack(fill="x", padx=16, pady=6)

    if label:
        header = tk.Frame(outer, bg=BG_CARD)
        header.pack(fill="x")
        tk.Frame(header, bg=accent, width=3).pack(side="left", fill="y", padx=(0, 8))
        tk.Label(
            header,
            text=label,
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=BG_CARD,
            pady=6,
            padx=8,
        ).pack(side="left")
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")

    inner = tk.Frame(outer, bg=BG_CARD)
    inner.pack(fill="both", expand=True)

    scroll_x = tk.Scrollbar(inner, orient="horizontal", bg=BG_PANEL, troughcolor=BG_DARK)
    scroll_x.pack(side="bottom", fill="x")

    scroll_y = tk.Scrollbar(inner, orient="vertical", bg=BG_PANEL, troughcolor=BG_DARK)
    scroll_y.pack(side="right", fill="y")

    canvas = tk.Canvas(
        inner,
        width=width,
        height=height,
        bg=BG_DARK,
        bd=0,
        highlightthickness=0,
        xscrollcommand=scroll_x.set,
        yscrollcommand=scroll_y.set,
    )
    canvas.pack(side="left", fill="both", expand=True)

    scroll_x.config(command=canvas.xview)
    scroll_y.config(command=canvas.yview)

    return canvas
