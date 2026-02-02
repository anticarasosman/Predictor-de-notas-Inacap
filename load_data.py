import mysql.connector
from mysql.connector import Error
from classes.readers.asignaturas_criticas_reader import AsignaturaCriticasReader


class DatabaseConnection:
    """Maneja la conexión a la base de datos MySQL"""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Conectado a base de datos: {self.database}")
            return self.connection
        except Error as e:
            print(f"✗ Error al conectar: {str(e)}")
            return None
    
    def disconnect(self):
        """Cierra la conexión"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Desconectado de base de datos")
    
    def get_connection(self):
        """Retorna la conexión actual"""
        return self.connection


def main():
    """
    Ejemplo de cómo usar los readers
    """
    
    # 1. CREAR CONEXIÓN A LA BASE DE DATOS
    db = DatabaseConnection(
        host='localhost',
        user='root',
        password='tu_contraseña',  # Cambiar por tu contraseña
        database='predictor_notas'
    )
    
    connection = db.connect()
    if not connection:
        print("No se pudo establecer conexión a la base de datos")
        return
    
    try:
        # 2. USAR EL READER DE ASIGNATURAS CRÍTICAS
        print("\n--- Procesando Asignaturas Críticas ---")
        reader_asignaturas = AsignaturaCriticasReader(
            file_path=r'data/Asignaturas Críticas.csv',
            db_connection=connection
        )
        reader_asignaturas.read()
        
        # 3. PUEDES USAR OTROS READERS DE LA MISMA FORMA
        # Por ejemplo, cuando implementes los demás readers:
        # reader_morosidad = ReporteMorosidadReader(
        #     file_path=r'data/REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv',
        #     db_connection=connection
        # )
        # reader_morosidad.read()
        
    finally:
        # 4. CERRAR CONEXIÓN
        db.disconnect()


if __name__ == "__main__":
    main()
