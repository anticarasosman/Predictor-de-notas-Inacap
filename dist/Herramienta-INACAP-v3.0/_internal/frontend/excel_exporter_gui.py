import tkinter as tk
from tkinter import messagebox
from classes.export.exporter import Exporter
from frontend.custom_sheet_creator_gui import CustomSheetCreatorGUI
from frontend.custom_sheet_deleter_gui import CustomSheetDeleterGUI
from frontend.user_selects_output import select_output_directory
from frontend.buttons import create_back_button, create_exit_button
from utils.custom_sheet_manager import list_custom_sheets

class FileExporterGUI:

    def __init__(self, root, db_connection, main_menu=None):
        self.root = root
        self.db_connection = db_connection
        self.main_menu = main_menu

    def ask_user_for_rut(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.root,
            text="EXPORTAR DATOS A EXCEL",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        subtitle_label = tk.Label(
            self.root,
            text="Ingrese el RUT del estudiante a exportar (sin puntos y con guion):",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        rut_label = tk.Label(
            input_frame,
            text="RUT:",
            font=("Arial", 11)
        )
        rut_label.pack(side=tk.LEFT, padx=10)

        rut_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            width=20
        )
        rut_entry.pack(side=tk.LEFT, padx=10)
        rut_entry.focus()  # Poner el foco en el Entry

        sheets_frame = tk.LabelFrame(
            self.root,
            text="Selecciona hojas para incluir en el Excel",
            font=("Arial", 10),
            padx=20,
            pady=10
        )
        sheets_frame.pack(padx=20, pady=10)

        # UNA VES IMPLEMENTAMOS LA FACTORY DE CHECKBOXES, DEBEMOS USARLA AQUI PARA CREAR LOS CHECKBOXES DEFAULT

        self.sheet_general = tk.BooleanVar(value=True)
        self.sheet_academic = tk.BooleanVar(value=True)
        self.sheet_financial = tk.BooleanVar(value=True)
        self.sheet_notas_media = tk.BooleanVar(value=True)

        tk.Checkbutton(
            sheets_frame,
            text="Información General",
            variable=self.sheet_general,
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        tk.Checkbutton(
            sheets_frame,
            text="Semestres y Asignaturas",
            variable=self.sheet_academic,
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        tk.Checkbutton(
            sheets_frame,
            text="Información Financiera",
            variable=self.sheet_financial,
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        tk.Checkbutton(
            sheets_frame,
            text="Notas Media",
            variable=self.sheet_notas_media,
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        self.personalized_sheets_frame = tk.LabelFrame(
            self.root,
            text="Hojas Personalizadas",
            font=("Arial", 10),
            padx=20,
            pady=10
        )
        self.personalized_sheets_frame.pack(padx=20, pady=10, anchor=tk.W, fill=tk.X)
        
        self.custom_sheet_vars = {}
        
        self.load_custom_sheets()

        action_button_frame = tk.Frame(self.root)
        action_button_frame.pack(pady=10)

        export_btn = tk.Button(
            action_button_frame,
            text="📊 Exportar a Excel",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=20,
            command=lambda: self.export_student(
                rut_entry.get().strip(), 
                {
                    'general': self.sheet_general.get(),
                    'academic': self.sheet_academic.get(),
                    'financial': self.sheet_financial.get(),
                    'notas_media': self.sheet_notas_media.get()
                },
                {sheet_name: var.get() for sheet_name, var in self.custom_sheet_vars.items()}
            )
        )
        export_btn.pack(side=tk.LEFT, padx=10)

        personalize_btn = tk.Button(
            action_button_frame,
            text="➕ Crear Hoja Personalizada",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            width=22,
            command=lambda: self.create_personalized_sheet()
        )
        personalize_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = tk.Button(
            action_button_frame,
            text="🗑 Borrar Hojas Personalizadas",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            width=24,
            command=lambda: self.delete_personalized_sheets()
        )
        delete_btn.pack(side=tk.LEFT, padx=10)

        navigation_button_frame = tk.Frame(self.root)
        navigation_button_frame.pack(pady=10)

        if self.main_menu:
            create_back_button(navigation_button_frame, self.return_to_menu, side=tk.LEFT, padx=10)

        create_exit_button(navigation_button_frame, self.root.quit, side=tk.LEFT, padx=10)

    def export_student(self, rut: str, sheets_selection, custom_sheet_selection=None) -> None:
        
        if custom_sheet_selection is None:
            custom_sheet_selection = {}
        
        if not rut:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un RUT")
            return
        
        try:
            output_dir = select_output_directory(
                title="Selecciona la carpeta donde guardar el archivo Excel"
            )
            
            exporter = Exporter(self.db_connection, sheets_selection, custom_sheet_selection)
            
            file_path = exporter.export_student_by_rut(rut, output_dir)
            
            messagebox.showinfo(
                "Éxito",
                f"✓ Archivo exportado exitosamente\n\n{file_path}"
            )
            
            self.show_export_success(rut, file_path)
            
        except ValueError as e:
            messagebox.showerror("Error", f"✗ {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"✗ Error al exportar: {str(e)}")

    def show_export_success(self, rut: str, file_path: str) -> None:
        
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.root,
            text="EXPORTACIÓN COMPLETADA",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

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

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

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

        if self.main_menu:
            create_back_button(button_frame, self.return_to_menu, side=tk.LEFT, padx=10)

        create_exit_button(button_frame, self.root.quit, side=tk.LEFT, padx=10)

    def return_to_menu(self) -> None:
        if self.main_menu:
            self.main_menu.create_menu()

    def load_custom_sheets(self) -> None:
        for widget in self.personalized_sheets_frame.winfo_children():
            widget.destroy()
        
        self.custom_sheet_vars.clear()
        
        custom_sheets_list = list_custom_sheets()
        
        if custom_sheets_list:
            for sheet_name in custom_sheets_list:
                var = tk.BooleanVar(value=False)
                tk.Checkbutton(
                    self.personalized_sheets_frame,
                    text=sheet_name,
                    variable=var,
                    font=("Arial", 10)
                ).pack(anchor=tk.W)
                self.custom_sheet_vars[sheet_name] = var
        else:
            tk.Label(
                self.personalized_sheets_frame,
                text="No hay hojas personalizadas creadas",
                font=("Arial", 9),
                fg="gray"
            ).pack(anchor=tk.W)
    
    def create_personalized_sheet(self) -> None:
        sheet_creator = CustomSheetCreatorGUI(
            self.root, 
            self.db_connection,
            refresh_callback=self.load_custom_sheets
        )
    
    def delete_personalized_sheets(self) -> None:
        sheet_deleter = CustomSheetDeleterGUI(
            refresh_callback=self.load_custom_sheets
        )