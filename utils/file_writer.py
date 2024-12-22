from pathlib import Path
from typing import List
from core.file_scanner import FileInfo

class FileWriter:
    def __init__(self, output_file: Path):
        self.output_file = output_file
    
    def write_contents(self, files: List[FileInfo]) -> None:
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with self.output_file.open('w', encoding='utf-8') as f:
            for file_info in files:
                # ファイルパスのセクション
                f.write("## ")
                f.write(str(file_info.path))
                f.write("\n------------\n")
                
                # ファイル内容
                if file_info.content is not None:
                    f.write(file_info.content)
                else:
                    f.write("# Failed to read content")
                f.write("\n\n")