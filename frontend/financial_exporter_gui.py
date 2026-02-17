import tkinter as tk
from tkinter import messagebox
from classes.export.financial_data_exporter import FinancialDataExporter
from frontend.user_selects_output import select_output_directory
from frontend.buttons import create_back_button, create_exit_button
from pathlib import Path
import subprocess


class FinancialExporterGUI:
    """
    Interfaz gráfica para exportar datos financieros (morosidad) de estudiantes.
    """

    def __init__(self, root, db_connection, main_menu=None):
        self.root = root
        self.db_connection = db_connection
        self.main_menu = main_menu
        self.exporter = FinancialDataExporter(db_connection)

    def show_financial_export(self):
        """
        Muestra la interfaz para exportar datos financieros.
        """
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(
            self.root,
            text="EXPORTAR DATOS FINANCIEROS",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        # Subtítulo
        subtitle_label = tk.Label(
            self.root,
            text="Exportar información de morosidad de estudiantes con deuda",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=40, padx=40)

        # Información
        info_label = tk.Label(
            main_frame,
            text="Este reporte incluye todos los estudiantes con deuda vigente,\n"
                 "con detalles de matrículas, colegiaturas y porcentaje de morosidad.",
            font=("Arial", 10),
            fg="gray",
            justify=tk.LEFT,
            wraplength=400
        )
        info_label.pack(pady=20)

        # Botón exportar
        export_button = tk.Button(
            main_frame,
            text="📊 Exportar Datos Financieros",
            font=("Arial", 12, "bold"),
            bg="#C4161C",
            fg="white",
            padx=30,
            pady=10,
            command=self._handle_export
        )
        export_button.pack(pady=20)

        # Botones navegación
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        create_back_button(
            button_frame,
            lambda: self.main_menu.create_menu() if self.main_menu else None,
            side=tk.LEFT,
            padx=10
        )

        create_exit_button(button_frame, self.root.quit, side=tk.RIGHT, padx=10)

    def _handle_export(self):
        """
        Maneja el proceso de exportación de datos financieros.
        """
        # Seleccionar directorio de salida
        output_dir = select_output_directory()

        if not output_dir:
            return  # Usuario canceló

        try:
            # Exportar
            file_path = self.exporter.export_financial_data(Path(output_dir))

            # Mostrar mensaje de éxito
            result = messagebox.askyesno(
                "Exportación Exitosa",
                f"Los datos financieros se han exportado correctamente.\n\n"
                f"Archivo: {Path(file_path).name}\n\n"
                f"¿Desea abrir el archivo?"
            )

            if result:
                subprocess.Popen([file_path], shell=True)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al exportar los datos:\n{str(e)}"
            )
