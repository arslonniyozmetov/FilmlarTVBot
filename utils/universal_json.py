# utils/universal_json.py

import os
import json

class JSONStorage:
    def __init__(self, file_path, default_data):
        self.file_path = file_path
        self.default_data = default_data
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write(self.default_data)
        else:
            # Fayl bor lekin bo'sh bo'lsa, default data yozish
            try:
                with open(self.file_path, "r") as f:
                    content = f.read()
                    if not content.strip():
                        self._write(self.default_data)
                    else:
                        json.loads(content)  # JSON valid ekanligini tekshiradi
            except Exception:
                self._write(self.default_data)

    def _read(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_data(self):
        return self._read()

    def save_data(self, data):
        self._write(data)

    def append(self, key, item):
        data = self._read()
        data[key].append(item)
        self._write(data)

    def update(self, key, new_list):
        data = self._read()
        data[key] = new_list
        self._write(data)
