import tkinter as tk
from tkinter import ttk
import time


class ProgressWindow:
    """Ventana de progreso para mostrar el avance de la carga"""
    
    def __init__(self, parent, total_rows, filename):
        self.window = tk.Toplevel(parent)
        self.window.title("Procesando archivo...")
        self.window.geometry("500x200")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.total_rows = total_rows
        self.current_row = 0
        self.start_time = time.time()
        
        # Nombre del archivo
        tk.Label(
            self.window,
            text=f"Procesando: {filename}",
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self.window,
            length=450,
            mode='determinate',
            maximum=total_rows
        )
        self.progress_bar.pack(pady=10)
        
        # Texto de progreso
        self.progress_label = tk.Label(
            self.window,
            text=f"0 / {total_rows} filas procesadas",
            font=("Arial", 10)
        )
        self.progress_label.pack(pady=5)
        
        # Tiempo estimado
        self.time_label = tk.Label(
            self.window,
            text="Estimando tiempo...",
            font=("Arial", 9),
            fg="gray"
        )
        self.time_label.pack(pady=5)
        
        # Porcentaje
        self.percent_label = tk.Label(
            self.window,
            text="0%",
            font=("Arial", 12, "bold")
        )
        self.percent_label.pack(pady=10)
    
    def update(self, current_row):
        """Actualiza el progreso"""
        self.current_row = current_row
        self.progress_bar['value'] = current_row
        
        # Actualizar texto
        percent = (current_row / self.total_rows) * 100 if self.total_rows > 0 else 0
        self.progress_label.config(text=f"{current_row} / {self.total_rows} filas procesadas")
        self.percent_label.config(text=f"{percent:.1f}%")
        
        # Calcular tiempo estimado
        if current_row > 0:
            elapsed = time.time() - self.start_time
            avg_time_per_row = elapsed / current_row
            remaining_rows = self.total_rows - current_row
            estimated_remaining = avg_time_per_row * remaining_rows
            
            if estimated_remaining < 60:
                time_text = f"Tiempo estimado restante: {int(estimated_remaining)} segundos"
            else:
                minutes = int(estimated_remaining / 60)
                seconds = int(estimated_remaining % 60)
                time_text = f"Tiempo estimado restante: {minutes}m {seconds}s"
            
            self.time_label.config(text=time_text)
        
        self.window.update()
    
    def close(self):
        """Cierra la ventana"""
        self.window.destroy()
