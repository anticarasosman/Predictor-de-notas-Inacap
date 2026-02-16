import tkinter as tk
from tkinter import ttk, messagebox
from frontend.file_loader_gui import FileLoaderGUI
from frontend.excel_exporter_gui import FileExporterGUI
from frontend.semester_exporter_gui import SemesterExporterGUI


class MainMenu:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection
        self.create_menu()

    def create_menu(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título principal
        title_label = tk.Label(
            self.root,
            text="PREDICTOR DE NOTAS INACAP",
            font=("Arial", 18, "bold"),
            pady=30
        )
        title_label.pack()

        # Subtítulo
        subtitle_label = tk.Label(
            self.root,
            text="Menú Principal",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack()

        # Frame para botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=40, padx=50, fill=tk.BOTH, expand=True)

        # Botón: Subir Archivos
        upload_btn = tk.Button(
            button_frame,
            text="📁 Subir Archivos a la Base de Datos",
            font=("Arial", 12),
            height=3,
            bg="#4CAF50",
            fg="white",
            command=self.open_file_loader
        )
        upload_btn.pack(pady=10, fill=tk.X)

        #Boton: Exportar a Excel
        export_btn = tk.Button(
            button_frame,
            text="📊 Exportar Datos de alumno a Excel",
            font=("Arial", 12),
            height=3,
            bg="#FF9800",
            fg="white",
            command=self.open_exporter
        )
        export_btn.pack(pady=10, fill=tk.X)

        # Botón: Exportar por Semestre
        semester_export_btn = tk.Button(
            button_frame,
            text="📚 Exportar Datos por Semestre",
            font=("Arial", 12),
            height=3,
            bg="#2196F3",
            fg="white",
            command=self.open_semester_exporter
        )
        semester_export_btn.pack(pady=10, fill=tk.X)

        # Botón: Salir
        exit_btn = tk.Button(
            button_frame,
            text="Salir",
            font=("Arial", 11),
            height=2,
            bg="#f44336",
            fg="white",
            command=self.root.quit
        )
        exit_btn.pack(pady=10, fill=tk.X)

    def open_file_loader(self):
        # Instanciar FileLoaderGUI y mostrar selección de archivos
        file_loader = FileLoaderGUI(self.root, self.db_connection, main_menu=self)
        file_loader.show_type_selection()

    def open_exporter(self):
        # Instanciar FileExporterGUI y mostrar pantalla de ingreso de RUT
        exporter = FileExporterGUI(self.root, self.db_connection, main_menu=self)
        exporter.ask_user_for_rut()

    def open_semester_exporter(self):
        # Instanciar SemesterExporterGUI y mostrar selector de semestres
        semester_exporter = SemesterExporterGUI(self.root, self.db_connection, main_menu=self)
        semester_exporter.show_semester_selector()