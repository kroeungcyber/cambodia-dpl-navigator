from typing import List
from openai import AsyncOpenAI
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model_name: str = settings.llm_model_name
        self.temperature: float = settings.llm_temperature
        
    async def generate(self, prompt: str) -> str:
        """Generate text from prompt using chat completion for consistency."""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages)
        
    async def chat(self, messages: List[dict]) -> str:
        """Chat completion interface using OpenAI API."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during LLM chat completion: {e}")
            return f"Error: Could not generate response. {e}"
