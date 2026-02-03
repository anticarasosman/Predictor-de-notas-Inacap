import tkinter as tk
from tkinter import filedialog, messagebox
from export.student_exporter import StudentExporter
from frontend.user_selects_output import select_output_directory
from frontend.buttons import create_back_button, create_exit_button
from frontend.progress_window import ProgressWindow
from pathlib import Path
import os

class FileExporterGUI:
    """GUI para exportar datos de estudiantes a Excel"""

    def __init__(self, root, db_connection, main_menu=None):
        self.root = root
        self.db_connection = db_connection
        self.main_menu = main_menu

    def ask_user_for_rut(self):
        """Pregunta al usuario por el RUT del estudiante a exportar"""
        
        # Limpiamos la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(
            self.root,
            text="EXPORTAR DATOS A EXCEL",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        # Subtítulo
        subtitle_label = tk.Label(
            self.root,
            text="Ingrese el RUT del estudiante a exportar (sin puntos y con guion):",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)

        # Frame para el input del RUT
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        # Label del input
        rut_label = tk.Label(
            input_frame,
            text="RUT:",
            font=("Arial", 11)
        )
        rut_label.pack(side=tk.LEFT, padx=10)

        # Entry (campo de texto)
        rut_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            width=20
        )
        rut_entry.pack(side=tk.LEFT, padx=10)
        rut_entry.focus()  # Poner el foco en el Entry

        # Frame para botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Botón Exportar
        export_btn = tk.Button(
            button_frame,
            text="📊 Exportar a Excel",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=20,
            command=lambda: self.export_student(rut_entry.get().strip())
        )
        export_btn.pack(side=tk.LEFT, padx=10)

        # Botón Volver
        if self.main_menu:
            create_back_button(button_frame, self.return_to_menu, side=tk.LEFT, padx=10)

        # Botón Cerrar Programa
        create_exit_button(button_frame, self.root.quit, side=tk.LEFT, padx=10)

    def export_student(self, rut: str) -> None:
        """
        Exporta los datos del estudiante con el RUT proporcionado
        
        Args:
            rut: RUT del estudiante
        """
        
        # Validar que el RUT no esté vacío
        if not rut:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un RUT")
            return
        
        try:
            # Solicitar al usuario que seleccione la carpeta de exportación
            output_dir = select_output_directory(
                title="Selecciona la carpeta donde guardar el archivo Excel"
            )
            
            # Crear exportador
            exporter = StudentExporter(self.db_connection)
            
            # Mostrar ventana de progreso mientras se exporta
            # (Para esta operación es rápida, pero lo dejamos por consistencia)
            
            # Exportar estudiante
            file_path = exporter.export_student_by_rut(rut, output_dir)
            
            # Mostrar éxito
            messagebox.showinfo(
                "Éxito",
                f"✓ Archivo exportado exitosamente\n\n{file_path}"
            )
            
            # Mostrar pantalla de resultado
            self.show_export_success(rut, file_path)
            
        except ValueError as e:
            messagebox.showerror("Error", f"✗ {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"✗ Error al exportar: {str(e)}")

    def show_export_success(self, rut: str, file_path: str) -> None:
        """Muestra pantalla de éxito después de la exportación"""
        
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(
            self.root,
            text="EXPORTACIÓN COMPLETADA",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        # Información
        info_text = f"""RUT Exportado: {rut}
Archivo guardado en:
{file_path}"""
        
        info_label = tk.Label(
            self.root,
            text=info_text,
            font=("Courier", 10),
            justify=tk.LEFT,
            pady=20
        )
        info_label.pack()

        # Frame para botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Botón Exportar otro
        export_btn = tk.Button(
            button_frame,
            text="📊 Exportar otro estudiante",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=25,
            command=self.ask_user_for_rut
        )
        export_btn.pack(side=tk.LEFT, padx=10)

        # Botón Volver
        if self.main_menu:
            create_back_button(button_frame, self.return_to_menu, side=tk.LEFT, padx=10)

        # Botón Cerrar Programa
        create_exit_button(button_frame, self.root.quit, side=tk.LEFT, padx=10)

    def return_to_menu(self) -> None:
        """Vuelve al menú principal"""
        if self.main_menu:
            self.main_menu.create_menu()