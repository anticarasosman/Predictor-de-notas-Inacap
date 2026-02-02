import tkinter as tk
from tkinter import messagebox
from database.db_connection import DatabaseConnection
from frontend.file_loader_gui import FileLoaderGUI
import os
from dotenv import load_dotenv
import signal
import sys

from frontend.main_menu_gui import MainMenu

load_dotenv()

def cleanup(db_connection, root):
    """Cierra conexión y limpia recursos"""
    try:
        if db_connection and db_connection.connection:
            db_connection.connection.close()
            print("✓ Conexión cerrada")
    except Exception as e:
        print(f"Error al cerrar conexión: {e}")
    finally:
        root.quit()
        sys.exit(0)

if __name__ == "__main__":
    # Crear conexión a la base de datos
    try:
        db_connection = DatabaseConnection()
        if db_connection.connect():
            # Crear la ventana principal
            root = tk.Tk()
            root.title("Predictor de Notas INACAP")
            root.geometry("600x600")  # Tamaño visible para el menú
            root.resizable(False, False)
            
            # Manejador para Ctrl+C
            def on_closing():
                cleanup(db_connection, root)
            
            def signal_handler(sig, frame):
                cleanup(db_connection, root)
            
            signal.signal(signal.SIGINT, signal_handler)
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            # Crear GUI del cargador de archivos
            menu = MainMenu(root, db_connection)
            
            root.mainloop()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
    except KeyboardInterrupt:
        print("\n✓ Aplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar: {str(e)}")


