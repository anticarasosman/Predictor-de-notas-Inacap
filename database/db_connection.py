import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class DatabaseConnection:
    
    def __init__(self, host: str = None, user: str = None, 
                 password: str = None, database: str = None, port: int = None):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.database = database or os.getenv('DB_NAME', 'inacap_db')
        self.port = port or int(os.getenv('DB_PORT', 3306))
        self.connection = None
    
    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
                use_unicode=True
            )
            try:
                self.connection.set_charset_collation("utf8mb4", "utf8mb4_unicode_ci")
            except Error:
                pass
            print(f"✓ Conectado a: {self.user}@{self.host}:{self.port}/{self.database}")
            return True
        except Error as e:
            print(f"✗ Error de conexión: {str(e)}")
            return False
    
    def cursor(self, **kwargs):
        if self.connection:
            return self.connection.cursor(**kwargs)
        else:
            raise Error("No hay conexión activa a la base de datos")
    
    def disconnect(self) -> bool:
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("✓ Desconectado de base de datos")
                return True
        except Error as e:
            print(f"✗ Error al desconectar: {str(e)}")
        return False
    
    def get_connection(self):
        if self.connection and self.connection.is_connected():
            return self.connection
        else:
            print("✗ No hay conexión activa con la base de datos")
            return None
    
    def is_connected(self) -> bool:
        return self.connection is not None and self.connection.is_connected()
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
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
