import os
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT

class TourGuide:
    def __init__(self):
        # Obtém a chave da variável de ambiente
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "A variável de ambiente GEMINI_API_KEY não está configurada. "
                "Por favor, defina-a antes de iniciar."
            )
        
        # Inicializa o client do novo SDK google-genai
        self.client = genai.Client(api_key=self.api_key)
        
        # Inicia o chat contínuo com o modelo gemini-1.5-pro e o system prompt
        self.chat = self.client.chats.create(
            model="gemini-1.5-pro",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            )
        )

    def send_message(self, message: str) -> str:
        """Envia a mensagem do usuário para o Gemini e retorna a resposta em texto."""
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Desculpe, tive um problema de conexão: {str(e)}"
