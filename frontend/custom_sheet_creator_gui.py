import tkinter as tk
from tkinter import messagebox
from utils.db_schema_reader import get_all_tables, get_table_columns
from utils.custom_sheet_manager import save_custom_sheet_data
from factories.frontend_factories.checkbox_factory import CheckboxFactory

class CustomSheetCreatorGUI:


    def __init__(self, root, db_connection):
        self.parent = root
        self.db_connection = db_connection
        
        # Crear ventana independiente
        self.window = tk.Toplevel(root)
        self.window.title("Crear Hoja Personalizada")
        self.window.geometry("600x700")
        self.window.resizable(True, True)
        
        self.create_sheet_config()

    def create_sheet_config(self) -> dict:
        #Titulo
        title_label = tk.Label(
            self.window,
            text="CREAR HOJA PERSONALIZADA",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        #Subtitulo
        subtitle_label = tk.Label(
            self.window,
            text="Configura los parámetros de la hoja personalizada",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)

        #Frame para el input del nombre de la hoja
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=20)

        # Label del input
        name_label = tk.Label(
            input_frame,
            text="Nombre de la hoja:",
            font=("Arial", 11)
        )
        name_label.pack(side=tk.LEFT, padx=10)

        # Entry (campo de texto)
        name_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            width=20
        )
        name_entry.pack(side=tk.LEFT, padx=10)
        name_entry.focus()  # Poner el foco en el Entry

        self.show_variables()

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        # Botón Crear Hoja
        create_btn = tk.Button(
            button_frame,
            text="Guardar Hoja Personalizada",
            font=("Arial", 12),
            height=2,
            bg="#4CAF50",
            fg="white",
            command=lambda: self.create_custom_sheet(name_entry.get())
        )
        create_btn.pack()

    def show_variables(self):
        #Frame contenedor con scroll
        container_frame = tk.LabelFrame(
            self.window,
            text="Selecciona las variables para incluir en la hoja",
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        container_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Canvas para el scroll
        canvas = tk.Canvas(container_frame, height=300)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(container_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno donde irán los checkboxes
        vars_frame = tk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=vars_frame, anchor=tk.NW)

        # Crear diccionario de tablas
        self.tables = get_all_tables(self.db_connection)
        self.variables = {}

        # Crear checkboxes para cada variable
        for table, columns in self.tables.items():
            table_label = tk.Label(
                vars_frame,
                text=table,
                font=("Arial", 11, "bold"),
                pady=5
            )
            table_label.pack(anchor=tk.W)

            for column in columns:
                var = tk.BooleanVar(value=False)
                checkbox = CheckboxFactory.create_checkbox(vars_frame, column, var)
                checkbox.pack(anchor=tk.W, padx=20)
                self.variables[f"{table}.{column}"] = var

        # Actualizar scroll region cuando cambie el tamaño
        vars_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Ajustar ancho del frame interno al canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)

    def create_custom_sheet(self, sheet_name: str):
        """Crea la hoja personalizada con las variables seleccionadas"""
        
        # Validar nombre
        if not sheet_name.strip():
            messagebox.showerror("Error", "El nombre de la hoja no puede estar vacío.")
            return
        
        # Recopilar columnas checkeadas agrupadas por tabla
        selected_columns = {}
        
        for full_key, var in self.variables.items():
            if var.get():  # Si la checkbox está checkeada
                table, column = full_key.split(".")
                
                # Agregar columna a la tabla
                if table not in selected_columns:
                    selected_columns[table] = []
                selected_columns[table].append(column)
        
        # Validar que se seleccionó al menos 1 columna
        if not selected_columns:
            messagebox.showerror("Error", "Debe seleccionar al menos una variable.")
            return
        
        # Crear estructura JSON para guardar
        config = {
            "name": sheet_name,
            "tables": [
                {"table": table, "columns": columns}
                for table, columns in selected_columns.items()
            ]
        }
        
        try:
            # Guardar la configuración
            save_custom_sheet_data(sheet_name, config)
            
            # Mostrar éxito
            messagebox.showinfo(
                "Éxito",
                f"✓ Hoja personalizada '{sheet_name}' guardada correctamente.\n\n"
                f"Se guardaron {sum(len(cols) for cols in selected_columns.values())} columnas de {len(selected_columns)} tabla(s)."
            )
            
            # Cerrar ventana después de guardar exitosamente
            self.window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la hoja personalizada:\n{str(e)}")