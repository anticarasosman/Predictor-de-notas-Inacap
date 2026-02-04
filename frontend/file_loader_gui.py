import tkinter as tk
from tkinter import filedialog, messagebox
from factories.readers_factory import ReadersFactory
from frontend.progress_window import ProgressWindow
from frontend.buttons import create_back_button, create_exit_button, create_upload_button
from mysql.connector import Error
import os
import subprocess


class FileLoaderGUI:
    """GUI para cargar archivos a la base de datos"""
    
    def __init__(self, root, db_connection, main_menu=None):
        self.root = root
        self.db_connection = db_connection
        self.main_menu = main_menu
        self.file_types = ReadersFactory.get_file_types()
    
    def show_type_selection(self):
        """Muestra la selección de tipo de archivo en la ventana principal"""
        # Limpiar la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(
            self.root,
            text="SUBIR ARCHIVOS A LA BASE DE DATOS",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(
            self.root,
            text="¿Qué tipo de archivo deseas subir?",
            font=("Arial", 12),
            fg="gray"
        )
        subtitle_label.pack(pady=10)
        
        # Frame para botones de tipos de archivo
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20, padx=50, fill=tk.X)
        
        # Crear botones para cada tipo
        for file_type, info in self.file_types.items():
            btn = tk.Button(
                button_frame,
                text=info['name'],
                font=("Arial", 11),
                height=2,
                bg="#2196F3",
                fg="white",
                command=lambda ft=file_type: self.select_files(ft)
            )
            btn.pack(pady=8, fill=tk.X)
        
        # Frame para botones inferiores
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=20)
        
        # Botón Volver al Menú
        if self.main_menu:
            create_back_button(bottom_frame, self.return_to_menu, side=tk.LEFT, padx=10)
        
        # Botón Cerrar Programa
        create_exit_button(bottom_frame, self.root.quit, side=tk.LEFT, padx=10)
    
    def return_to_menu(self):
        """Vuelve al menú principal"""
        if self.main_menu:
            self.main_menu.create_menu()

    
    def select_files(self, file_type):
        """Abre explorador de archivos para seleccionar archivos"""
        file_info = self.file_types[file_type]
        
        files = filedialog.askopenfilenames(
            title=f"Selecciona archivos de {file_info['name']}",
            filetypes=file_info['extensions'] + [("Todos los archivos", "*.*")],
            initialdir=os.path.join(os.getcwd(), "data")
        )
        
        if files:
            self.process_files(file_type, files)
        else:
            messagebox.showwarning("Cancelado", "No se seleccionaron archivos")
    
    def process_files(self, file_type, files):
        """Procesa los archivos seleccionados"""
        if not files:
            return
        
        total_files = len(files)
        success_count = 0
        error_messages = []
        
        for idx, file_path in enumerate(files, 1):
            progress_window = None
            try:
                # Crear reader usando la factory
                reader = ReadersFactory.create_reader(file_type, file_path, self.db_connection)
                
                # Obtener total de filas usando el método polimórfico
                total_rows = reader.get_total_rows()
                
                # Crear ventana de progreso
                progress_window = ProgressWindow(self.root, total_rows, os.path.basename(file_path))
                
                # Callback para actualizar progreso
                def update_progress(current_row):
                    progress_window.update(current_row)
                
                # Ejecutar UPSERT con progreso
                reader._process_and_upsert(progress_callback=update_progress)
                
                # Confirmar cambios
                self.db_connection.connection.commit()
                
                success_count += 1
                print(f"✓ Archivo {idx}/{total_files} cargado exitosamente")
            
            except FileNotFoundError:
                error_msg = f"Archivo no encontrado: {os.path.basename(file_path)}"
                error_messages.append(error_msg)
                print(f"✗ {error_msg}")
                # Deshacer cambios si hay error
                try:
                    self.db_connection.connection.rollback()
                except:
                    pass
                
            except Exception as e:
                # Capturar excepciones generales incluyendo errores críticos de BD
                error_str = str(e)
                if "ERROR CRÍTICO" in error_str or "doesn't exist" in error_str:
                    error_msg = f"{os.path.basename(file_path)}: {error_str}"
                    error_messages.append(error_msg)
                    print(f"✗ {error_msg}")
                    # Deshacer cambios
                    try:
                        self.db_connection.connection.rollback()
                    except:
                        pass
                    # Interrumpir el procesamiento
                    break
                else:
                    error_msg = f"{os.path.basename(file_path)}: {error_str}"
                    error_messages.append(error_msg)
                    print(f"✗ {error_msg}")
                    try:
                        self.db_connection.connection.rollback()
                    except:
                        pass
                
            except Error as e:
                error_msg = f"{os.path.basename(file_path)}: Error en BD - {str(e)}"
                error_messages.append(error_msg)
                print(f"✗ {error_msg}")
                # Deshacer cambios
                try:
                    self.db_connection.connection.rollback()
                except:
                    pass
                
            finally:
                # Cerrar ventana de progreso
                if progress_window:
                    progress_window.close()
        
        # Mostrar resumen
        self.show_result_summary(success_count, total_files, error_messages)
    
    def show_result_summary(self, success_count, total_files, error_messages):
        """Muestra resumen de resultados en la ventana principal"""
        # Limpiar la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(
            self.root,
            text="RESUMEN DE CARGA",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Información de resultado
        info_text = f"""Archivos procesados: {total_files}
Archivos exitosos: {success_count}
Archivos con error: {len(error_messages)}"""
        
        info_label = tk.Label(
            self.root,
            text=info_text,
            font=("Courier", 11),
            justify=tk.LEFT,
            pady=10
        )
        info_label.pack()
        
        # Area de texto para errores
        if error_messages:
            errors_label = tk.Label(
                self.root,
                text="ERRORES:",
                font=("Arial", 10, "bold")
            )
            errors_label.pack(pady=5, anchor=tk.W, padx=50)
            
            text_frame = tk.Frame(self.root)
            text_frame.pack(pady=5, padx=50, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(
                text_frame,
                height=8,
                yscrollcommand=scrollbar.set,
                font=("Courier", 9),
                wrap=tk.WORD
            )
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_widget.yview)
            
            for error in error_messages:
                text_widget.insert(tk.END, f"• {error}\n")
            text_widget.config(state=tk.DISABLED)
        
        # Frame para botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Botón Subir otro archivo
        create_upload_button(button_frame, self.show_type_selection, side=tk.LEFT, padx=10)
        
        # Botón Volver al Menú Principal
        if self.main_menu:
            create_back_button(button_frame, self.return_to_menu, side=tk.LEFT, padx=10)
        
        # Botón Cerrar Programa
        create_exit_button(button_frame, self.root.quit, side=tk.LEFT, padx=10)