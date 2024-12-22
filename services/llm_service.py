import anthropic
from dataclasses import dataclass
from typing import List, Optional, Dict
from core.file_scanner import FileInfo

@dataclass
class Message:
    role: str
    content: str

class LLMService:
    MAX_TURNS = 5
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history: List[Message] = []
    
    def create_prompt(self, content: str, query: str) -> str:
        return f"""以下はGitHubリポジトリのコード解析結果です。このコードについて質問に答えてください。

コード解析結果:
{content}

質問: {query}

できるだけ具体的に、コードの内容を参照しながら回答してください。"""
    
    def _add_to_history(self, role: str, content: str):
        self.conversation_history.append(Message(role=role, content=content))
        if len(self.conversation_history) > self.MAX_TURNS * 2:
            self.conversation_history = self.conversation_history[-self.MAX_TURNS * 2:]
    
    def get_response(self, content: str, query: str) -> tuple[Optional[str], Optional[str]]:
        try:
            prompt = self.create_prompt(content, query)
            self._add_to_history("user", prompt)
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                messages=[{"role": msg.role, "content": msg.content} 
                         for msg in self.conversation_history],
                max_tokens=1024
            )
            
            answer = response.content[0].text
            self._add_to_history("assistant", answer)
            return answer, None
            
        except Exception as e:
            return None, f"エラーが発生しました: {str(e)}"
    
    def clear_history(self):
        self.conversation_history = []
    
    @staticmethod
    def format_code_content(files: List[FileInfo]) -> str:
        formatted_content = []
        for file_info in files:
            formatted_content.append(
                f"#ファイルパス\n{file_info.path}\n------------\n{file_info.content}\n"
            )
        return "\n".join(formatted_content)
