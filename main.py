import os
import gradio as gr
import yt_dlp
from gtts import gTTS
from gemini_guide import TourGuide

def download_video(url):
    """Faz o download do vídeo do YouTube usando yt-dlp e retorna o caminho."""
    if not url:
        return None, "Por favor, insira uma URL válida do YouTube."
    
    # Opções do yt-dlp para baixar em qualidade boa sem demorar exageradamente
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'tour_video.%(ext)s',
        'quiet': False,
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, f"Sucesso! Vídeo '{info.get('title')}' carregado. Onde estamos?"
    except Exception as e:
        return None, f"Erro ao baixar o vídeo: {str(e)}"

def generate_audio(text):
    """Gera o arquivo de áudio usando gTTS baseado no texto do Gemini."""
    if not text:
        return None
    try:
        tts = gTTS(text=text, lang='pt', tld='com.br')
        audio_path = "resposta_guia.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None

def chat_interface(user_message, history, guide_instance):
    """Gerencia o envio da mensagem, histórico contínuo e geração de áudio."""
    
    # Cria a instância do Guia na primeira vez que o usuário fala
    if not guide_instance:
        try:
            guide_instance = TourGuide()
        except Exception as e:
            history.append((user_message, f"Erro de Inicialização: {str(e)}"))
            return history, guide_instance, None

    # Pega a resposta de texto do Gemini através da classe TourGuide
    response_text = guide_instance.send_message(user_message)
    
    # Gera o áudio narrado pelo guia
    audio_path = generate_audio(response_text)
    
    # Atualiza o histórico visual da interface Gradio
    history.append((user_message, response_text))
    
    return history, guide_instance, audio_path

# --- Configuração da Interface Gráfica com Gradio ---
with gr.Blocks(title="Tourverse Gemini", theme=gr.themes.Soft(primary_hue="teal")) as demo:
    gr.Markdown(
        """
        # 🌍 Tourverse Gemini
        ### O seu Guia Virtual Imersivo com IA
        Cole a URL de um Walk 4K ou Drive Tour do YouTube, inicie o vídeo e converse com seu guia!
        """
    )
    
    # Estado oculto para manter a classe TourGuide viva (mantém a sessão do chat e memória)
    guide_state = gr.State(None)
    
    with gr.Row():
        # Coluna Esquerda: Player de Vídeo
        with gr.Column(scale=3):
            gr.Markdown("### 1. Carregue o Tour")
            video_url = gr.Textbox(
                label="URL do Vídeo (YouTube)", 
                placeholder="Ex: https://www.youtube.com/watch?v=..."
            )
            download_btn = gr.Button("Baixar e Iniciar Vídeo", variant="primary")
            status_text = gr.Textbox(label="Status do Vídeo", interactive=False)
            video_player = gr.Video(label="Tela do Tour Virtual", autoplay=True)
            
        # Coluna Direita: Chat e Voz
        with gr.Column(scale=2):
            gr.Markdown("### 2. Converse com o Guia")
            chatbot = gr.Chatbot(label="Chat Contínuo", height=400)
            audio_output = gr.Audio(label="Voz do Guia (Auto-play)", autoplay=True, visible=True)
            
            msg_input = gr.Textbox(
                label="Diga algo ao guia...", 
                placeholder="Ex: Que lugar lindo, onde estamos exatamente?"
            )
            clear_btn = gr.ClearButton([msg_input, chatbot, audio_output])

    # --- Eventos de Clique / Submit ---
    
    download_btn.click(
        fn=download_video, 
        inputs=[video_url], 
        outputs=[video_player, status_text]
    )
    
    msg_input.submit(
        fn=chat_interface,
        inputs=[msg_input, chatbot, guide_state],
        outputs=[chatbot, guide_state, audio_output]
    ).then(
        # Reseta o campo de input de texto após o envio
        fn=lambda: "", 
        inputs=None, 
        outputs=msg_input
    )

if __name__ == "__main__":
    print("Iniciando interface do Tourverse Gemini...")
    print("Dica: Certifique-se de que a variável GEMINI_API_KEY está configurada no seu sistema.")
    # Inicia a aplicação web local
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
