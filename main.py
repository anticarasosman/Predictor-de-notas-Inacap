# Configurar Tcl/Tk ANTES de cualquier import de tkinter
import setup_tkinter

import tkinter as tk
from tkinter import messagebox
from database.db_connection import DatabaseConnection
from frontend.file_loader_gui import FileLoaderGUI
import os
import config_loader
import signal
import sys

from frontend.main_menu_gui import MainMenu

# Cargar configuración desde .env.encrypted
config_loader.load_config()

def cleanup(db_connection, root):
    """Cierra conexión y limpia recursos"""
    try:
        if db_connection and db_connection.is_connected():
            db_connection.disconnect()
            print("✓ Conexión cerrada")
    except Exception as e:
        print(f"Error al cerrar conexión: {e}")
    finally:
        root.quit()
        sys.exit(0)

if __name__ == "__main__":
    # Crear conexión a la base de datos
    try:
        print(f"[MAIN] Python ejecutándose desde: {sys.executable}")
        print(f"[MAIN] Directorio de trabajo: {os.getcwd()}")
        
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
            # Mensaje detallado de error
            error_msg = f"No se pudo conectar a la base de datos\n\n"
            error_msg += f"Host: {db_connection.host}\n"
            error_msg += f"User: {db_connection.user}\n"
            error_msg += f"Database: {db_connection.database}\n"
            error_msg += f"Port: {db_connection.port}\n\n"
            error_msg += f"Verifica:\n"
            error_msg += f"1. El archivo .env existe en la misma carpeta que el .exe\n"
            error_msg += f"2. Las credenciales son correctas\n"
            error_msg += f"3. El servidor está accesible desde este PC\n\n"
            error_msg += f"Revisa la consola para más detalles."
            messagebox.showerror("Error de Conexión", error_msg)
            input("\nPresiona ENTER para cerrar...")
    except KeyboardInterrupt:
        print("\n✓ Aplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar: {str(e)}")


