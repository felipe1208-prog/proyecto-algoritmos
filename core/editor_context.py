from typing import Optional, List
from structures.linked_list import LinkedList
from structures.queue import Queue
from models.code_file import CodeFile
from models.analysis_request import AnalysisRequest
from models.diagnostic import Diagnostic
from services.config_service import ConfigService
from services.static_analyzer import StaticAnalyzer
from services.groq_service import GroqService
from services.request_worker import RequestWorker


class EditorContext:

    def __init__(self, config_path: str = "config.json", env_path: str = ".env") -> None:
        self.config_service: ConfigService = ConfigService(config_path=config_path, env_path=env_path)
        
        max_len = int(self.config_service.get("max_line_length", 80))
        self.static_analyzer: StaticAnalyzer = StaticAnalyzer(max_line_length=max_len)

        api_key = str(self.config_service.get("groq_api_key", ""))
        model_name = str(self.config_service.get("groq_model", "llama-3.3-70b-versatile"))
        timeout = int(self.config_service.get("timeout_seconds", 30))

        self.groq_service: GroqService = GroqService(api_key=api_key, model=model_name, timeout=timeout)
        self.request_queue: Queue = Queue()

        self.requests_history: LinkedList = LinkedList()
        self._request_counter: int = 0

        self.worker: RequestWorker = RequestWorker(
            request_queue=self.request_queue,
            groq_service=self.groq_service
        )
        self.worker.start()

        self.open_files: LinkedList = LinkedList()
        self.active_file: Optional[CodeFile] = None

        self.last_diagnostics: List[Diagnostic] = []

    def create_file(self, file_name: str, content: str = "") -> Optional[CodeFile]:
        existing = self.find_file(file_name)
        if existing is not None:
            return None

        new_file = CodeFile(name=file_name, initial_content=content)
        self.open_files.append(new_file)
        self.active_file = new_file
        return new_file

    def find_file(self, file_name: str) -> Optional[CodeFile]:
        return self.open_files.find_by_predicate(lambda f: f.name == file_name)

    def switch_file(self, file_name: str) -> bool:
        target = self.find_file(file_name)
        if target is not None:
            self.active_file = target
            return True
        return False

    def delete_file(self, file_name: str) -> bool:
        removed = self.open_files.delete_by_predicate(lambda f: f.name == file_name)
        if removed is None:
            return False

        if self.active_file is not None and self.active_file.name == file_name:
            self.active_file = self.open_files.get_at(0)

        return True

    def enqueue_analysis(self, file_to_analyze: CodeFile) -> AnalysisRequest:
        self._request_counter += 1
        ticket = AnalysisRequest(
            request_id=self._request_counter,
            file_name=file_to_analyze.name,
            code_content=file_to_analyze.content
        )
        self.requests_history.append(ticket)
        self.request_queue.enqueue(ticket)
        return ticket

    def update_diagnostics(self, diagnostics: List[Diagnostic]) -> None:
        self.last_diagnostics = [d for d in diagnostics]

    def shutdown(self) -> None:
        if self.worker.is_alive():
            self.worker.stop()