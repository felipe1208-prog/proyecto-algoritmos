import threading
import time
from typing import Optional
from structures.queue import Queue
from models.analysis_request import AnalysisRequest
from services.gemini_service import GeminiService


class RequestWorker(threading.Thread):

    def __init__(self, request_queue: Queue, ai_service: GeminiService, poll_interval: float = 0.5) -> None:
        super().__init__(daemon=True)
        self.request_queue: Queue = request_queue
        self.ai_service: GeminiService = ai_service
        self.poll_interval: float = poll_interval
        self._is_running: bool = False
        self._lock: threading.Lock = threading.Lock()

    def run(self) -> None:
        self._is_running = True

        while self._is_running:
            item_to_process: Optional[AnalysisRequest] = None

            with self._lock:
                if not self.request_queue.is_empty():
                    item_to_process = self.request_queue.dequeue()

            if item_to_process:
                self._process_request(item_to_process)
            else:
                time.sleep(self.poll_interval)

    def _process_request(self, request: AnalysisRequest) -> None:
        request.mark_processing()
        try:
            ai_result = self.ai_service.analyze_code(
                code_content=request.code_content,
                file_name=request.file_name
            )
            request.mark_completed(ai_result)
        except Exception as ex:
            request.mark_failed(str(ex))

    def stop(self) -> None:
        self._is_running = False