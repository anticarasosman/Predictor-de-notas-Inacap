import tkinter as tk

class FramesFactory:
    @staticmethod
    def create_frame(parent, name):
        """Crea un frame con el nombre especificado"""
        frame = tk.Frame(parent)
        return frame