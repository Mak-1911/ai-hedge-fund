from openai import OpenAI
import os
from typing import Dict, Any, Optional, List

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialising the OpenAIService class.
        Args:
            api_key (Optional[str]): The API key for the OpenAI service.
            base_url (Optional[str]): The base URL for the OpenAI service.
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = OpenAI(
            base_url = base_url or "https://openrouter.ai/api/v1",
            api_key = api_key
        )
    
    def call_llm(self, model:str, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict[str, Any]:

        """
        Calls the OpenAI API with the specified model and messages.
        Args:
            model: The model identifier ( eg. "gpt-4", "gpt-3.5-turbo")
            messages: List of message dictionaries with role and content.
            temperature: Sampling temperature(0.0 - 1.0)
            max_tokens: Maximum number of tokens to generate.
        Returns:
            Dictionary containing the response from the model
                  
        """

        try:
            response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature,
                max_tokens = max_tokens
            )
            return response.model_dump()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {}

    
    def get_completion(self, model:str, prompt:str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
        """
        Get a simple text completion from the model.
        Args:
            model: The model identifier ( eg. "gpt-4", "gpt-3.5-turbo")
            prompt: The prompt to generate a completion for.
            temperature: Sampling temperature(0.0 - 1.0)
            max_tokens: Maximum number of tokens to generate.
        Returns:
            The completion text as a string.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.call_llm(model, messages, temperature, max_tokens)
        return response["choices"][0]["message"]["content"]


def get_openai_service(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAIService:
    """
    Get an instance of the OpenAIService class.
    Returns:
        An instance of the OpenAIService class.
    """
    return OpenAIService(api_key, base_url)
