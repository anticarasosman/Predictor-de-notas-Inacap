import requests
import time
from typing import Dict

class JobMonitor:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_status(self, job_id: str) -> Dict:
        response = requests.post(
            self.api_url,
            json={
                'accion': 'obtener_estado_job',
                'job_id': job_id
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['datos']
    
    def wait_for_completion(self, job_id: str, callback=None, interval=5):
        while True:
            status = self.get_status(job_id)

            if callback:
                callback(status)
            
            if status['status'] in ['completed', 'failed']:
                return status
            time.sleep(interval)