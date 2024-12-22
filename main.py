import sys
from pathlib import Path
import tempfile
import git
from datetime import datetime
from config.settings import Settings
from core.git_manager import GitManager
from core.file_scanner import FileScanner, FileInfo
from typing import Tuple, List, List, Set, Optional

class DirectoryStructureScanner:
    def __init__(self, root_path: Path):
        self.root_path = root_path
    
    def generate_tree(self, path: Path = None, prefix: str = "", is_last: bool = True) -> str:
        if path is None:
            path = self.root_path
        
        output = prefix + ("└── " if is_last else "├── ") + (path.name or str(path)) + "\n"
        
        entries = list(path.iterdir())
        dirs = sorted([d for d in entries if d.is_dir()])
        files = sorted([f for f in entries if f.is_file()])
        
        dirs = [d for d in dirs if not d.name.startswith('.') and d.name != '__pycache__']
        files = [f for f in files if not f.name.startswith('.')]
        
        next_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, dir_path in enumerate(dirs):
            is_last_entry = (i == len(dirs) - 1) and not files
            output += self.generate_tree(dir_path, next_prefix, is_last_entry)
        
        for i, file_path in enumerate(files):
            is_last_file = i == len(files) - 1
            output += next_prefix + ("└── " if is_last_file else "├── ") + file_path.name + "\n"
        
        return output

class MarkdownGenerator:
    def __init__(self, target_path: str, target_extensions: Set[str] = None):
        self.target_path = target_path
        self.timestamp = Settings.get_timestamp()
        self.temp_dir = None
        self.is_github = target_path.startswith(('http://', 'https://')) and 'github.com' in target_path
        # Settings.pyのデフォルト拡張子を使用
        self.target_extensions = target_extensions or Settings.DEFAULT_EXTENSIONS
    
    def generate_markdowns(self) -> Tuple[str, str, List[FileInfo]]:
        """リポジトリの内容とディレクトリ構造のMarkdownを生成"""
        try:
            if self.is_github:
                self.temp_dir = Path(tempfile.mkdtemp())
                git.Repo.clone_from(self.target_path, self.temp_dir)
                work_dir = self.temp_dir
            else:
                work_dir = Path(self.target_path)
                if not work_dir.exists():
                    raise ValueError(f"Directory not found: {work_dir}")
            
            # ディレクトリ構造のスキャン
            dir_scanner = DirectoryStructureScanner(work_dir)
            tree_structure = dir_scanner.generate_tree()
            
            # ファイル内容のスキャン
            file_scanner = FileScanner(work_dir, self.target_extensions)
            files = file_scanner.scan_files()
            
            # Markdown生成
            structure_md = self._create_structure_markdown(tree_structure)
            content_md = self._create_content_markdown(files)
            
            return content_md, structure_md, files
            
        finally:
            if self.is_github and self.temp_dir and Path(self.temp_dir).exists():
                import shutil
                shutil.rmtree(self.temp_dir)
    
    def _create_structure_markdown(self, tree_structure: str) -> str:
        name = self._get_name()
        content = f"# {name} - ディレクトリ構造\n\n"
        content += f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "```\n"
        content += tree_structure
        content += "```\n"
        return content
    
    def _create_content_markdown(self, files: List[FileInfo]) -> str:
        content = ""
        for file in files:
            content += f"## {file.path}\n"
            content += "------------\n"
            if file.content is not None:
                content += file.content
            else:
                content += "# Failed to read content"
            content += "\n\n"
        return content
    
    def _get_name(self) -> str:
        if self.is_github:
            return self.target_path.split('/')[-1].replace('.git', '')
        else:
            return Path(self.target_path).name

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <github_url or directory_path>")
        return 1
    
    target_path = sys.argv[1]
    
    try:
        print(f"Processing: {target_path}")
        
        generator = MarkdownGenerator(target_path)
        content_md, structure_md, _ = generator.generate_markdowns()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = generator._get_name()
        
        content_file = f"{name}_content_{timestamp}.md"
        structure_file = f"{name}_structure_{timestamp}.md"
        
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(content_md)
        
        with open(structure_file, 'w', encoding='utf-8') as f:
            f.write(structure_md)
        
        print(f"生成完了:")
        print(f"- ファイル内容: {content_file}")
        print(f"- ディレクトリ構造: {structure_file}")
        
        return 0
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())