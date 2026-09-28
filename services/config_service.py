import json
import os
from typing import Any, Dict, Optional


class ConfigService:

    DEFAULT_CONFIG: Dict[str, Any] = {
        "groq_api_key": "",
        "groq_model": "llama-3.3-70b-versatile",
        "api_url": "https://api.groq.com/openai/v1/chat/completions",
        "timeout_seconds": 30,
        "backup_directory": "./backups",
        "max_line_length": 80
    }

    def __init__(self, config_path: str = "config.json", env_path: str = ".env") -> None:
        self.config_path: str = config_path
        self.env_path: str = env_path
        self._config_data: Dict[str, Any] = {}
        self.load_config()
        self._load_env()

    def _load_env(self) -> None:
        if os.path.exists(self.env_path):
            try:
                with open(self.env_path, "r", encoding="utf-8") as env_file:
                    for line in env_file:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip().strip("'\"")
                            if key == "apiAI" and val:
                                self._config_data["groq_api_key"] = val
                                os.environ["apiAI"] = val
            except OSError:
                pass


        if not self._config_data.get("groq_api_key"):
            env_val = os.environ.get("apiAI")
            if env_val:
                self._config_data["groq_api_key"] = env_val

    def load_config(self) -> None:
        if not os.path.exists(self.config_path):
            self._config_data = self.DEFAULT_CONFIG.copy()
            self.save_config()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                loaded = json.load(file)
                self._config_data = self.DEFAULT_CONFIG.copy()
                self._config_data.update(loaded)
        except (json.JSONDecodeError, OSError):
            self._config_data = self.DEFAULT_CONFIG.copy()

    def save_config(self) -> bool:
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                json.dump(self._config_data, file, indent=4)
            return True
        except OSError:
            return False

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        self._config_data[key] = value
        return self.save_config()

    def get_all(self) -> Dict[str, Any]:
        return self._config_data.copy()