from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
import chardet

@dataclass
class FileInfo:
    path: Path
    size: int
    extension: str
    content: Optional[str] = None
    encoding: Optional[str] = None
    
    @property
    def formatted_size(self) -> str:
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size/1024:.1f} KB"
        else:
            return f"{self.size/(1024*1024):.1f} MB"

class FileScanner:
    EXCLUDED_DIRS = {
        '.git', '__pycache__', 'node_modules', 'venv', 
        '.env', 'build', 'dist', 'target', 'bin', 'obj'
    }
    
    def __init__(self, base_dir: Path, target_extensions: Set[str]):
        self.base_dir = base_dir
        self.target_extensions = target_extensions
    
    def _should_scan_file(self, path: Path) -> bool:
        if any(excluded in path.parts for excluded in self.EXCLUDED_DIRS):
            return False
        return path.suffix.lower() in self.target_extensions
    
    def _read_file_content(self, file_path: Path) -> tuple[Optional[str], Optional[str]]:
        try:
            with file_path.open('rb') as f:
                raw_data = f.read(4096)
                result = chardet.detect(raw_data)
                encoding = result['encoding'] if result['confidence'] > 0.7 else 'utf-8'
            try:
                with file_path.open('r', encoding=encoding) as f:
                    return f.read(), encoding
            except UnicodeDecodeError:
                try:
                    with file_path.open('r', encoding='cp932') as f:
                        return f.read(), 'cp932'
                except UnicodeDecodeError:
                    return None, None
        except (OSError, ValueError):
            return None, None
    
    def scan_files(self) -> List[FileInfo]:
        if not self.base_dir.exists():
            raise FileNotFoundError(f"ディレクトリが見つかりません: {self.base_dir}")
        
        files = []
        for entry in self.base_dir.glob("**/*"):
            if entry.is_file() and self._should_scan_file(entry):
                content, encoding = self._read_file_content(entry)
                if content is not None:
                    files.append(FileInfo(
                        path=entry.absolute(),
                        size=entry.stat().st_size,
                        extension=entry.suffix.lower(),
                        content=content,
                        encoding=encoding
                    ))
        return sorted(files, key=lambda x: str(x.path))
