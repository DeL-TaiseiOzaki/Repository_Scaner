import subprocess
from pathlib import Path

class GitManager:
    def __init__(self, repo_url: str, target_dir: Path):
        self.repo_url = repo_url
        self.target_dir = target_dir
    
    def clone_repository(self) -> bool:
        try:
            if self.target_dir.exists():
                raise FileExistsError(f"Directory already exists: {self.target_dir}")
            
            self.target_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", self.repo_url, str(self.target_dir)],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Clone error: {e.stderr}")
    
    def cleanup(self):
        if self.target_dir.exists():
            subprocess.run(
                ["rm", "-rf", str(self.target_dir)],
                check=True,
                capture_output=True,
                text=True
            )