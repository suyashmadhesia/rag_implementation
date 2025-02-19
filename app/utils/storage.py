import uuid
from app.schemas.models import *
from .crypto import generate_unique_id

class LocalStorage:
    _instance = None
    _max_file_store = 25 * 1024 * 1024  # Max 25MB file size

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            sessions : dict[str, SessionStorage] = {}
            files : dict[str, FileStorage] = {}
            cls._instance._sessions = sessions
            cls._instance._files = files
        return cls._instance

    def create_session(self):
        """Creates a new session and returns the session ID."""
        session_id = str(uuid.uuid4())
        session = SessionStorage(session_id=session_id, storage_usage=0)
        self._sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> SessionStorage | None:
        """Retrieves a session by session ID."""
        return self._sessions.get(session_id)

    def store_file(self, session_id: str, file_id: str, file_size: int, file_name: str):
        """Stores a file under a given session, enforcing storage limits."""
        if session_id not in self._sessions:
            raise ValueError("Session not found")
        if self._sessions[session_id].storage_usage + file_size > self._max_file_store:
            raise ValueError("File size exceeds maximum allowed storage")

        file_storage_id = generate_unique_id(session_id, file_id)
        file = FileStorage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            file_id=file_id,
            file_size=file_size,
            file_name=file_name
        )

        self._files[file_storage_id] = file
        self._sessions[session_id].storage_usage += file_size
        return file_storage_id

    def delete_file(self, session_id: str, file_id: str):
        """Deletes a file from a session and updates storage usage."""
        file_storage_id = generate_unique_id(session_id, file_id)

        if file_storage_id not in self._files:
            raise ValueError("File not found")

        file = self._files.pop(file_storage_id)

        # Update session storage usage
        if session_id in self._sessions:
            self._sessions[session_id].storage_usage -= file.file_size

        return True

    def delete_session(self, session_id: str):
        """Deletes a session and all associated files."""
        if session_id not in self._sessions:
            raise ValueError("Session not found")

        # Remove all files related to this session and update storage usage
        files_to_delete = [
            file_id for file_id, file in self._files.items() if file.session_id == session_id
        ]

        total_freed_space = sum(self._files[file_id].file_size for file_id in files_to_delete)

        for file_id in files_to_delete:
            del self._files[file_id]

        # Remove session
        del self._sessions[session_id]

        return True
    

    def get_session_file(self, session_id):
        files = []
        for key, value in self._files.items():
            if value.session_id == session_id:
                files.append(value.to_json())
        return files
        
