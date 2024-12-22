import os
from dotenv import load_dotenv

class LLMSettings:
    def __init__(self):
        load_dotenv()
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.default_llm = "claude"
        
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
    
    def get_available_models(self):
        return ["claude"]