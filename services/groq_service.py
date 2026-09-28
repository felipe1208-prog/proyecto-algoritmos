import json
import urllib.request
import urllib.error
from typing import Optional


class GroqService:

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", timeout: int = 30) -> None:
        self.api_key: str = api_key
        self.model: str = model
        self.timeout: int = timeout
        self.endpoint_url: str = "https://api.groq.com/openai/v1/chat/completions"

    def analyze_code(self, code_content: str, file_name: str) -> str:
        if not self.api_key or self.api_key.strip() == "":
            raise ValueError("No se ha configurado la API Key de Groq en config.json.")

        system_prompt = (
            "Eres un asistente de arquitectura de software y análisis estático integrado en un IDE CLI. "
            "Revisa el código fuente provisto, identifica oportunidades de optimización algorítmica, "
            "posibles fugas de memoria o errores lógicos, y brinda recomendaciones precisas y profesionales."
        )

        user_content = f"Archivo: {file_name}\n\nCódigo fuente:\n```\n{code_content}\n```"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2,
            "max_tokens": 1024
        }

        data_bytes = json.dumps(payload).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "SynthetixStudio/1.0"
        }

        req = urllib.request.Request(
            url=self.endpoint_url,
            data=data_bytes,
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status != 200:
                    raise RuntimeError(f"Respuesta inesperada del servidor Groq: HTTP {response.status}")

                response_body = response.read().decode("utf-8")
                json_response = json.loads(response_body)
                return json_response["choices"][0]["message"]["content"].strip()

        except urllib.error.HTTPError as http_err:
            error_body = http_err.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Error HTTP Groq ({http_err.code}): {error_body}")
        except urllib.error.URLError as url_err:
            raise RuntimeError(f"Fallo de conexión de red hacia Groq: {url_err.reason}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al conectar con Groq: {str(e)}")