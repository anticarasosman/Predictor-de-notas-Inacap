import tkinter as tk
from tkinter import ttk
import time

class MainMenu:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection
        self.create_menu()

    def create_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear título, botones, etc...
        # Boton "Subir Archivos" debe llamar a self.open_file_loader