from dataclasses import asdict, dataclass

import json
import time


@dataclass
class SessionStorage:
    session_id: str
    storage_usage: int= 0
    created_at: int = int(time.time())

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass
class FileStorage:
    id: str
    session_id: str
    file_id: str
    file_name: str
    file_size: int
    created_at: int = int(time.time())

    def to_json(self):
        return json.dumps(asdict(self))
    