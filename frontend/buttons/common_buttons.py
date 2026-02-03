import tkinter as tk

def create_back_button(parent, command, **kwargs):
    btn = tk.Button(
        parent,
        text="← Volver al Menú Principal",
        font=("Arial", 10),
        bg="#607D8B",
        fg="white",
        width=25,
        command=command,
    )

    side = kwargs.get('side', tk.LEFT)
    padx = kwargs.get('padx', 10)
    pady = kwargs.get('pady', 0)

    btn.pack(side=side, padx=padx, pady=pady)
    return btn

def create_exit_button(parent, command, **kwargs):
    btn = tk.Button(
        parent,
        text="Cerrar Programa",
        font=("Arial", 10),
        bg="#f44336",
        fg="white",
        width=18,
        command=command,
    )

    side = kwargs.get('side', tk.LEFT)
    padx = kwargs.get('padx', 10)
    pady = kwargs.get('pady', 0)

    btn.pack(side=side, padx=padx, pady=pady)
    return btn

def create_upload_button(parent, command, **kwargs):
    btn = tk.Button(
        parent,
        text="⬆️ Subir otro archivo",
        font=("Arial", 10),
        bg="#2196F3",
        fg="white",
        width=20,
        command=command,
    )

    side = kwargs.get('side', tk.LEFT)
    padx = kwargs.get('padx', 10)
    pady = kwargs.get('pady', 0)

    btn.pack(side=side, padx=padx, pady=pady)
    return btn