import requests
from typing import Tuple

class S3Uploader:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def upload_csv(self, filepath: str, filename: str) -> Tuple[str, str]:
        response = requests.post(
            self.api_url, 
            json= {
                'accion': 'generar_url_subida',
                'filename': filename
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()['datos']

        job_id = data['job_id']
        upload_url = data['upload_url']

        with open(filepath, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f,
                headers={'Content-Type': 'text/csv'},
                timeout=300
            )
            upload_response.raise_for_status()
        return job_id, upload_url