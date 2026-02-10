from tkinter import ttk

def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TButton",
        font=("Segoe UI", 10),
        padding=8
    )

    style.configure(
        "TLabel",
        font=("Segoe UI", 10)
    )

    style.configure(
        "Header.TLabel",
        font=("Segoe UI", 16, "bold")
    )
