# config.py
import os
import json

DEFAULT_CONFIG = {
    "file_categories": {
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "video": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"],
        "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
        "spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
        "presentations": [".pptx", ".ppt", ".odp", ".key"]
    }
}

def load_config(path="config.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        with open(path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
