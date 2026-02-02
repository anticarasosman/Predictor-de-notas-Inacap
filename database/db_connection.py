import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """
    Maneja la conexión y operaciones con la base de datos MySQL
    """
    
    def __init__(self, host: str = 'localhost', user: str = 'root', 
                 password: str = '', database: str = 'predictor_notas'):
        """
        Inicializa parámetros de conexión
        
        Args:
            host: Host de MySQL (default: localhost)
            user: Usuario de MySQL (default: root)
            password: Contraseña de MySQL
            database: Nombre de la base de datos
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establece conexión con la base de datos
        
        Returns:
            True si conexión es exitosa, False si falla
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Conectado a: {self.user}@{self.host}/{self.database}")
            return True
        except Error as e:
            print(f"✗ Error de conexión: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """
        Cierra la conexión con la base de datos
        
        Returns:
            True si cierre es exitoso
        """
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("✓ Desconectado de base de datos")
                return True
        except Error as e:
            print(f"✗ Error al desconectar: {str(e)}")
        return False
    
    def get_connection(self):
        """
        Retorna el objeto de conexión actual
        
        Returns:
            Objeto mysql.connector.connection.MySQLConnection
        """
        if self.connection and self.connection.is_connected():
            return self.connection
        else:
            print("✗ No hay conexión activa con la base de datos")
            return None
    
    def is_connected(self) -> bool:
        """
        Verifica si hay conexión activa
        
        Returns:
            True si está conectado, False si no
        """
        return self.connection is not None and self.connection.is_connected()
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Ejecuta una consulta INSERT, UPDATE o DELETE
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)
        
        Returns:
            True si se ejecuta exitosamente
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error en consulta: {str(e)}")
            return False
    
    def fetch_query(self, query: str, params: tuple = None):
        """
        Ejecuta una consulta SELECT
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)
        
        Returns:
            Lista de tuplas con los resultados
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"✗ Error en consulta: {str(e)}")
            return None
