import json
import urllib.request
import urllib.error


class GeminiService:

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", timeout: int = 30) -> None:
        self.api_key: str = api_key
        self.model: str = model
        self.timeout: int = timeout

    def analyze_code(self, code_content: str, file_name: str) -> str:
        if not self.api_key or self.api_key.strip() == "":
            raise ValueError("No se ha configurado la API Key de Gemini (apiAI) en el archivo .env")

        endpoint_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

        system_instruction = (
            "Eres un asistente de arquitectura de software y análisis estático integrado en un IDE CLI. "
            "Revisa el código fuente provisto, identifica oportunidades de optimización algorítmica, "
            "posibles errores sintácticos o de memoria, y brinda recomendaciones precisas y profesionales."
        )

        user_prompt = f"Archivo: {file_name}\n\nCódigo fuente:\n```\n{code_content}\n```"

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024
            }
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        req = urllib.request.Request(
            url=endpoint_url,
            data=data_bytes,
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status != 200:
                    raise RuntimeError(f"Respuesta HTTP inesperada de Gemini: {response.status}")

                response_body = response.read().decode("utf-8")
                json_data = json.loads(response_body)

                candidates = json_data.get("candidates", [])
                if not candidates:
                    return "Gemini no devolvió sugerencias para este fragmento."

                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()

                return "Respuesta vacía recibida del modelo."

        except urllib.error.HTTPError as http_err:
            error_body = http_err.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Error HTTP Gemini ({http_err.code}): {error_body}")
        except urllib.error.URLError as url_err:
            raise RuntimeError(f"Fallo de conexión de red hacia Gemini: {url_err.reason}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al conectar con Gemini: {str(e)}")