from pathlib import Path
from datetime import datetime
from typing import Set

class Settings:
    # デフォルト設定
    DEFAULT_OUTPUT_DIR = Path("output")
    TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
    
    # デフォルトのスキャン対象拡張子
    DEFAULT_EXTENSIONS = {
        # プログラミング言語
        '.py',    # Python
        '.js',    # JavaScript
        '.ts',    # TypeScript
        '.java',  # Java
        '.cpp',   # C++
        '.hpp',   # C++ Header
        '.c',     # C
        '.h',     # C Header
        '.go',    # Go
        '.rs',    # Rust
        
        # 設定ファイル
        '.json',  # JSON
        '.yml',   # YAML
        '.yaml',  # YAML
        '.toml',  # TOML
        
        # ドキュメント
        '.md',    # Markdown
        '.txt',   # Text
    }
    
    @classmethod
    def get_timestamp(cls) -> str:
        return datetime.now().strftime(cls.TIMESTAMP_FORMAT)
    
    @classmethod
    def get_clone_dir(cls, timestamp: str) -> Path:
        return cls.DEFAULT_OUTPUT_DIR / f"repo_clone_{timestamp}"
    
    @classmethod
    def get_output_file(cls, timestamp: str) -> Path:
        return cls.DEFAULT_OUTPUT_DIR / f"scan_result_{timestamp}.md"
