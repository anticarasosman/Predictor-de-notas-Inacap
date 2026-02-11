import requests
import json
from typing import Dict, List, Any, Optional


class APIClientError(Exception):
    pass


class APIClient:
    
    def __init__(self, api_url: str, timeout: int = 30):
        self.api_url = api_url
        self.timeout = timeout
    
    def _request(self, accion: str, parametros: Optional[Dict] = None) -> Dict:
        body = {"accion": accion}
        if parametros:
            body.update(parametros)
        
        try:
            response = requests.post(
                self.api_url,
                json=body,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success', False):
                error_info = data.get('error', {})
                raise APIClientError(
                    f"Error de API: {error_info.get('tipo', 'Unknown')} - "
                    f"{error_info.get('mensaje', 'Error desconocido')}"
                )
            
            return data
        
        except requests.ConnectionError:
            raise APIClientError("No se pudo conectar a la API. Verifica tu conexión a internet.")
        
        except requests.Timeout:
            raise APIClientError(f"La API no respondió en {self.timeout} segundos. Intenta de nuevo.")
        
        except requests.HTTPError as e:
            raise APIClientError(f"Error HTTP {e.response.status_code}: {str(e)}")
        
        except json.JSONDecodeError:
            raise APIClientError("La API devolvió una respuesta inválida (no es JSON).")
        
        except Exception as e:
            raise APIClientError(f"Error inesperado: {str(e)}")
    
    def listar_estudiantes(self, 
                          filtros: Optional[Dict] = None, 
                          pagina: int = 1, 
                          limite: int = 100) -> tuple[List[Dict], Dict]:
        parametros = {
            "filtros": filtros or {},
            "pagina": pagina,
            "limite": limite
        }
        
        response = self._request("listar_estudiantes", parametros)
        return response.get("datos", []), response.get("metadatos", {})
    
    def buscar_estudiante(self, rut: str) -> Optional[Dict]:
        parametros = {"rut": rut}
        
        try:
            response = self._request("buscar_estudiante", parametros)
            return response.get("datos")
        except APIClientError as e:
            # Si el error es NotFoundError, devolver None
            if "NotFoundError" in str(e):
                return None
            raise
    
    def consulta_personalizada(self,
                              tabla: str,
                              columnas: Optional[List[str]] = None,
                              filtros: Optional[Dict] = None,
                              pagina: int = 1,
                              limite: int = 100) -> tuple[List[Dict], Dict]:
        parametros = {
            "tabla": tabla,
            "columnas": columnas,
            "filtros": filtros or {},
            "pagina": pagina,
            "limite": limite
        }
        
        response = self._request("consulta_personalizada", parametros)
        return response.get("datos", []), response.get("metadatos", {})
    
    def insertar_estudiante(self, datos: Dict) -> Dict:
        parametros = {"datos": datos}
        response = self._request("insertar_estudiante", parametros)
        return response.get("datos", {})
    
    def insertar_generico(self, tabla: str, datos: Dict) -> Dict:
        parametros = {
            "tabla": tabla,
            "datos": datos
        }
        
        # Lambda usa acción genérica para insert en otras tablas
        response = self._request("insertar_estudiante", parametros)
        return response.get("datos", {})
    
    def actualizar_estudiante(self, rut: str, datos: Dict) -> Dict:
        parametros = {
            "rut": rut,
            "datos": datos
        }
        
        response = self._request("actualizar_estudiante", parametros)
        return response.get("datos", {})
    
    def actualizar_generico(self, 
                           tabla: str, 
                           id_campo: str, 
                           id_valor: Any, 
                           datos: Dict) -> Dict:
        parametros = {
            "tabla": tabla,
            "id_campo": id_campo,
            "id_valor": id_valor,
            "datos": datos
        }
        
        response = self._request("actualizar_generico", parametros)
        return response.get("datos", {})
    
    def eliminar_estudiante(self, rut: str) -> Dict:
        parametros = {"rut": rut}
        response = self._request("eliminar_estudiante", parametros)
        return response.get("datos", {})
    
    def eliminar_generico(self, tabla: str, id_campo: str, id_valor: Any) -> Dict:
        parametros = {
            "tabla": tabla,
            "id_campo": id_campo,
            "id_valor": id_valor
        }
        
        response = self._request("eliminar_generico", parametros)
        return response.get("datos", {})
    
    def verificar_conexion(self) -> bool:
        try:
            response = self._request("verificar_conexion")
            datos = response.get("datos", {})
            return datos.get("conectado", False)
        except APIClientError:
            return False