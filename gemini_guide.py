import os
import time
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT

class TourGuide:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "A variável de ambiente GEMINI_API_KEY não está configurada. "
                "Por favor, defina-a antes de iniciar."
            )
        
        # Inicializa o client do novo SDK google-genai
        self.client = genai.Client(api_key=self.api_key)
        self.chat = None
        self.video_file = None

    def initialize_tour(self, video_path: str) -> str:
        """Faz o upload do vídeo de forma eficiente, aguarda processamento e inicia a sessão de chat."""
        try:
            print(f"Fazendo upload do vídeo para o Gemini: {video_path}")
            # Upload usando a API de arquivos (essencial para vídeos e suporte a long context)
            self.video_file = self.client.files.upload(file=video_path)
            
            # Aguarda o processamento do vídeo (Active Processing loop)
            print(f"Vídeo {self.video_file.name} enviado. Aguardando processamento da API...")
            while self.video_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(3) # Aguarda 3 segundos antes de checar novamente para evitar rate limits
                self.video_file = self.client.files.get(name=self.video_file.name)
            print("\nProcessamento concluído!")
            
            if self.video_file.state.name == "FAILED":
                return "Falha ao processar o vídeo na API do Gemini. O arquivo pode estar corrompido ou ser inválido."
            
            # Configuração avançada do modelo
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                top_p=0.9,
                top_k=40,
            )

            # Inicia o chat contínuo com o modelo gemini-1.5-pro, que tem janela de contexto gigante para vídeos
            self.chat = self.client.chats.create(
                model="gemini-1.5-pro",
                config=config
            )
            
            # Primeira interação: envia a referência do arquivo de vídeo processado e pede uma introdução.
            # Essa abordagem com 'chat.send_message' injeta o vídeo no histórico da conversa!
            print("Iniciando a conversa com o guia...")
            response = self.chat.send_message(
                [self.video_file, "O tour virtual acaba de começar! Analise profundamente o vídeo que estamos 'vivendo'. Faça uma saudação calorosa e imersiva ao usuário, introduzindo o clima e o local onde estamos (se conseguir identificar)."]
            )
            return response.text
        
        except Exception as e:
            return f"Erro crítico ao iniciar o tour: {str(e)}"

    def send_message(self, message: str) -> str:
        """Envia a mensagem de texto do usuário para o chat, mantendo o contexto longo do vídeo."""
        if not self.chat:
            return "O chat ainda não foi inicializado com um vídeo."
            
        try:
            # O Gemini 1.5 Pro manterá o vídeo no contexto graças à sessão de chat gerenciada
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Desculpe, a conexão com a matriz caiu rapidamente: {str(e)}"
