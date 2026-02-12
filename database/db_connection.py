import os
import sys
from dotenv import load_dotenv
from aws.api_client import APIClient, APIClientError

# Cargar .env desde el directorio del ejecutable (importante para PyInstaller)
if not os.getenv('API_URL'):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    env_path = os.path.join(application_path, '.env')
    load_dotenv(env_path)


class DatabaseConnection:
    """
    Conexión a base de datos a través de API Gateway + Lambda.
    Usa APIClient para comunicarse con el API en lugar de mysql.connector directo.
    """
    
    def __init__(self, api_url: str = None, api_timeout: int = None):
        self.api_url = api_url or os.getenv('API_URL')
        self.api_timeout = api_timeout or int(os.getenv('API_TIMEOUT', 30))
        self.client = None
        self.connected = False
    
    def connect(self) -> bool:
        try:
            print(f"[DB] Intentando conectar a API Gateway...")
            print(f"[DB] URL: {self.api_url}")
            print(f"[DB] Timeout: {self.api_timeout}s")
            
            if not self.api_url:
                print(f"✗ Error: API_URL no configurada en .env")
                return False
            
            self.client = APIClient(self.api_url, timeout=self.api_timeout)
            
            # Verificar conexión con un ping
            response = self.client._request('verificar_conexion')
            self.connected = response.get('success', False)
            
            if self.connected:
                print(f"✓ Conectado a API Gateway exitosamente")
                return True
            else:
                print(f"✗ Error de conexión API: {response.get('error', 'Unknown')}")
                return False
                
        except APIClientError as e:
            print(f"✗ Error de conexión API:")
            print(f"   {str(e)}")
            self.connected = False
            return False
        except Exception as e:
            print(f"✗ Error inesperado:")
            print(f"   {str(e)}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        try:
            self.connected = False
            self.client = None
            print("✓ Desconectado de API Gateway")
            return True
        except Exception as e:
            print(f"✗ Error al desconectar: {str(e)}")
        return False
    
    def is_connected(self) -> bool:
        return self.connected and self.client is not None
    
    def get_connection(self):
        """Retorna el cliente API. Compatibilidad con código legacy."""
        if self.is_connected():
            return self.client
        else:
            print("✗ No hay conexión activa con la API")
            return None
    
    def cursor(self, **kwargs):
        """
        API Gateway no retorna cursores tradicionales.
        Este método está deprecado.
        """
        raise NotImplementedError(
            "cursor() no está disponible con API Gateway. "
            "Usa los métodos específicos de APIClient (listar_estudiantes, buscar_estudiante, etc.)"
        )
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Ejecutar query SQL directo no está soportado con API Gateway.
        Este método está deprecado.
        """
        raise NotImplementedError(
            "execute_query() no está disponible con API Gateway. "
            "Usa los métodos específicos de APIClient."
        )
    
    def fetch_query(self, query: str, params: tuple = None):
        """
        Fetch query no está soportado con API Gateway.
        Este método está deprecado.
        """
        raise NotImplementedError(
            "fetch_query() no está disponible con API Gateway. "
            "Usa los métodos específicos de APIClient."
        )
