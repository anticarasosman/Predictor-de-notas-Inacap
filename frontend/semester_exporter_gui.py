import tkinter as tk
from tkinter import ttk, messagebox
from classes.export.semester_range_exporter import SemesterRangeExporter
from frontend.user_selects_output import select_output_directory
from frontend.buttons import create_back_button, create_exit_button
from pathlib import Path
import subprocess


class SemesterExporterGUI:
    """
    Interfaz gráfica para exportar datos de estudiantes por rango de semestres.
    """

    def __init__(self, root, db_connection, main_menu=None):
        self.root = root
        self.db_connection = db_connection
        self.main_menu = main_menu
        self.exporter = SemesterRangeExporter(db_connection)
        
    def show_semester_selector(self):
        """
        Muestra la interfaz para seleccionar rango de semestres.
        """
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(
            self.root,
            text="EXPORTAR DATOS POR SEMESTRE",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(
            self.root,
            text="Seleccione el rango de semestres a exportar",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20, padx=40)
        
        # Obtener semestres disponibles
        semestres = self._get_available_semestres()
        
        if not semestres:
            messagebox.showerror(
                "Error",
                "No hay semestres disponibles en la base de datos"
            )
            if self.main_menu:
                self.main_menu.create_menu()
            return
        
        # Periodo inicio
        inicio_frame = tk.Frame(main_frame)
        inicio_frame.pack(pady=10, fill=tk.X)
        
        inicio_label = tk.Label(
            inicio_frame,
            text="Periodo Inicio:",
            font=("Arial", 11),
            width=15,
            anchor='w'
        )
        inicio_label.pack(side=tk.LEFT, padx=10)
        
        self.inicio_combo = ttk.Combobox(
            inicio_frame,
            values=semestres,
            state='readonly',
            font=("Arial", 11),
            width=20
        )
        self.inicio_combo.pack(side=tk.LEFT, padx=10)
        if semestres:
            self.inicio_combo.current(0)  # Seleccionar primer semestre
        
        # Periodo fin
        fin_frame = tk.Frame(main_frame)
        fin_frame.pack(pady=10, fill=tk.X)
        
        fin_label = tk.Label(
            fin_frame,
            text="Periodo Fin:",
            font=("Arial", 11),
            width=15,
            anchor='w'
        )
        fin_label.pack(side=tk.LEFT, padx=10)
        
        self.fin_combo = ttk.Combobox(
            fin_frame,
            values=semestres,
            state='readonly',
            font=("Arial", 11),
            width=20
        )
        self.fin_combo.pack(side=tk.LEFT, padx=10)
        if semestres:
            self.fin_combo.current(len(semestres) - 1)  # Seleccionar último semestre
        
        # Nota informativa
        info_label = tk.Label(
            main_frame,
            text="El reporte incluirá todos los semestres en el rango seleccionado.\n"
                 "Cada semestre será una hoja separada en el archivo Excel.",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT,
            wraplength=400
        )
        info_label.pack(pady=20)
        
        # Botón exportar
        export_button = tk.Button(
            main_frame,
            text="📊 Exportar",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
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

    def _get_available_semestres(self) -> list:
        """
        Obtiene la lista de semestres disponibles en la base de datos.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        
        try:
            query = """
                SELECT DISTINCT periodo 
                FROM Semestre
                ORDER BY periodo
            """
            cursor.execute(query)
            return [row['periodo'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo semestres: {e}")
            return []
        finally:
            cursor.close()

    def _handle_export(self):
        """
        Maneja el proceso de exportación.
        """
        periodo_inicio = self.inicio_combo.get()
        periodo_fin = self.fin_combo.get()
        
        if not periodo_inicio or not periodo_fin:
            messagebox.showerror(
                "Error",
                "Debe seleccionar ambos periodos (inicio y fin)"
            )
            return
        
        # Seleccionar directorio de salida
        output_dir = select_output_directory()
        
        if not output_dir:
            return  # Usuario canceló
        
        try:
            # Exportar
            file_path = self.exporter.export_by_semester_range(
                periodo_inicio,
                periodo_fin,
                Path(output_dir)
            )
            
            # Mostrar mensaje de éxito
            result = messagebox.askyesno(
                "Exportación Exitosa",
                f"Los datos se han exportado correctamente.\n\n"
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
