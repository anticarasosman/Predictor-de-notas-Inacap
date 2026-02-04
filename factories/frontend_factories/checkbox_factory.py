import tkinter as tk

class CheckboxFactory:
    @staticmethod
    def create_checkbox(parent, text, var):
        """Crea un checkbox en el contenedor padre con el texto y variable dados"""
        checkbox = tk.Checkbutton(parent, text=text, variable=var)
        return checkbox