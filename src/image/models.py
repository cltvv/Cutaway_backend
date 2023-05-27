from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Image():
    def __init__(self, 
                 id: str,
                 file_path: str):
        self.id = id 
        self.file_path = file_path