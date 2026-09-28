import time
from typing import Optional


class AnalysisRequest:

    def __init__(self, request_id: int, file_name: str, code_content: str) -> None:
        self.request_id: int = request_id
        self.file_name: str = file_name
        self.code_content: str = code_content
        self.status: str = "PENDING"
        self.response: Optional[str] = None
        self.created_at: float = time.time()
        self.completed_at: Optional[float] = None
        self.error_message: Optional[str] = None

    def mark_processing(self) -> None:
        self.status = "PROCESSING"

    def mark_completed(self, ai_response: str) -> None:
        self.status = "COMPLETED"
        self.response = ai_response
        self.completed_at = time.time()

    def mark_failed(self, error: str) -> None:
        self.status = "FAILED"
        self.error_message = error
        self.completed_at = time.time()

    def summary(self) -> str:
        timestamp = time.strftime("%H:%M:%S", time.localtime(self.created_at))
        status_detail = f"[{self.status}]"
        if self.status == "FAILED" and self.error_message:
            status_detail += f" ({self.error_message})"
        return f"Ticket #{self.request_id} | Archivo: {self.file_name} | Hora: {timestamp} | Estado: {status_detail}"

    def __repr__(self) -> str:
        return f"AnalysisRequest(id={self.request_id}, file='{self.file_name}', status='{self.status}')"