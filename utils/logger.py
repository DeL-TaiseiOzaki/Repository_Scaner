from pathlib import Path
from typing import List
from datetime import datetime
from core.file_scanner import FileInfo

class ScanLogger:
    def __init__(self, log_file: Path):
        self.log_file = log_file
        
    def write_log(self, repo_url: str, files: List[FileInfo], stats: dict):
        """スキャン結果をログファイルに書き込みます"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with self.log_file.open('w', encoding='utf-8') as f:
            f.write(f"スキャン日時: {datetime.now()}\n")
            f.write(f"リポジトリ: {repo_url}\n")
            f.write(f"ファイル数: {len(files)}\n\n")
            
            f.write("=== ファイル種類の統計 ===\n")
            for ext, count in stats.items():
                f.write(f"{ext}: {count}個\n")
            f.write("\n")
            
            f.write("=== ファイルパス一覧 ===\n")
            for file_info in files:
                f.write(f"{file_info.path} ({file_info.formatted_size})\n")
