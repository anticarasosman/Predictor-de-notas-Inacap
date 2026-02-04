import tkinter as tk
from tkinter import messagebox
from utils.custom_sheet_manager import list_custom_sheets, delete_custom_sheet

class CustomSheetDeleterGUI:
    
    def __init__(self, refresh_callback):
        self.refresh_callback = refresh_callback
        
        # Crear ventana independiente
        self.window = tk.Toplevel()
        self.window.title("Eliminar Hoja Personalizada")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        self.create_deletion_interface()

    def create_deletion_interface(self):
        # Título
        title_label = tk.Label(
            self.window,
            text="BORRAR HOJAS PERSONALIZADAS",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()

        # Subtítulo
        subtitle_label = tk.Label(
            self.window,
            text="Selecciona las hojas personalizadas que deseas eliminar",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)

        # Frame contenedor con scroll
        container_frame = tk.LabelFrame(
            self.window,
            text="Hojas Personalizadas Disponibles",
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
        sheets_frame = tk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=sheets_frame, anchor=tk.NW)

        # Cargar hojas personalizadas
        self.sheet_vars = {}
        custom_sheets_list = list_custom_sheets()

        if custom_sheets_list:
            # Crear checkboxes para cada sheet
            for sheet_name in custom_sheets_list:
                var = tk.BooleanVar(value=False)
                tk.Checkbutton(
                    sheets_frame,
                    text=sheet_name,
                    variable=var,
                    font=("Arial", 10)
                ).pack(anchor=tk.W, padx=10, pady=2)
                self.sheet_vars[sheet_name] = var
        else:
            # Mostrar mensaje si no hay sheets
            tk.Label(
                sheets_frame,
                text="No hay hojas personalizadas para borrar",
                font=("Arial", 10),
                fg="gray"
            ).pack(anchor=tk.W, padx=10)

        # Actualizar scroll region
        sheets_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Ajustar ancho del frame interno al canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Frame para botones
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        # Botón Cancelar
        cancel_button = tk.Button(
            button_frame,
            text="Cancelar",
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            width=15,
            command=self.window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Botón Borrar
        delete_button = tk.Button(
            button_frame,
            text="Borrar",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=15,
            command=self.confirm_deletion,
            state=tk.NORMAL if custom_sheets_list else tk.DISABLED
        )
        delete_button.pack(side=tk.LEFT, padx=10)

    def confirm_deletion(self):
        """Confirma la eliminación de las hojas seleccionadas"""
        # Recopilar hojas seleccionadas
        selected_sheets = [name for name, var in self.sheet_vars.items() if var.get()]
        
        # Validar que se seleccionó al menos una
        if not selected_sheets:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar al menos una hoja para eliminar."
            )
            return
        
        # Construir mensaje de confirmación
        sheets_list = "\n".join([f"- {name}" for name in selected_sheets])
        confirm_message = (
            f"Está a punto de eliminar las siguientes tablas:\n\n"
            f"{sheets_list}\n\n"
            f"Esta operación no se puede revertir ¿está seguro?"
        )
        
        # Mostrar diálogo de confirmación
        confirmed = messagebox.askyesno(
            "Confirmar Eliminación",
            confirm_message,
            icon="warning"
        )
        
        if confirmed:
            self.delete_sheets(selected_sheets)
    
    def delete_sheets(self, sheet_names):
        """Elimina las hojas seleccionadas"""
        deleted_count = 0
        failed_sheets = []
        
        for sheet_name in sheet_names:
            try:
                delete_custom_sheet(sheet_name)
                deleted_count += 1
            except Exception as e:
                failed_sheets.append(f"{sheet_name}: {str(e)}")
        
        # Mostrar resultado
        if deleted_count > 0:
            success_message = f"✓ Se eliminaron {deleted_count} hoja(s) correctamente."
            if failed_sheets:
                success_message += f"\n\nErrores:\n" + "\n".join(failed_sheets)
            
            messagebox.showinfo("Éxito", success_message)
            
            # Refrescar lista en exporter
            if self.refresh_callback:
                self.refresh_callback()
            
            # Cerrar ventana
            self.window.destroy()
        else:
            error_message = "No se pudo eliminar ninguna hoja.\n\n" + "\n".join(failed_sheets)
            messagebox.showerror("Error", error_message)