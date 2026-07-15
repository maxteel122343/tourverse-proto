import os
import gradio as gr
import yt_dlp
from gtts import gTTS
from gemini_guide import TourGuide

def download_video(url, progress=gr.Progress()):
    """
    Faz o download do vídeo do YouTube de maneira otimizada para análise de IA.
    Prioriza resoluções até 720p/1080p para reduzir o payload, mantendo a clareza visual para a IA.
    """
    if not url:
        return None, "Por favor, insira uma URL válida do YouTube."
    
    progress(0, desc="Iniciando download...")
    
    # Opções do yt-dlp focadas em eficiência (max 720p, formato mp4 universal)
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': 'tour_video_%(id)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
        'merge_output_format': 'mp4'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            progress(1.0, desc="Download concluído com sucesso!")
            return filename, f"Sucesso! Vídeo '{info.get('title')}' carregado."
    except Exception as e:
        return None, f"Erro ao baixar o vídeo: {str(e)}"

def generate_audio(text):
    """Gera o arquivo de voz do guia usando gTTS (Google Text-to-Speech)."""
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

def initialize_tour_chat(video_path, guide_instance, history, progress=gr.Progress()):
    """Fluxo robusto de inicialização do tour, acionando upload de vídeo e obtendo a saudação inicial."""
    if not video_path:
        return history, guide_instance, None, "Nenhum vídeo carregado. Baixe um vídeo primeiro."
        
    if not guide_instance:
        try:
            guide_instance = TourGuide()
        except ValueError as e:
            return history, None, None, str(e)
        
    progress(0.2, desc="Fazendo upload e processando o vídeo no Gemini (pode demorar)...")
    
    # Inicia o tour chamando o método da classe que contém lógica de espera (polling)
    initial_response = guide_instance.initialize_tour(video_path)
    
    # Tratamento de erros iniciais
    if initial_response.startswith("Erro") or initial_response.startswith("Falha"):
        return history, guide_instance, None, initial_response

    progress(0.8, desc="Processamento finalizado! Sintetizando voz do guia...")
    audio_path = generate_audio(initial_response)
    
    # Adiciona ao histórico do chat
    history.append((None, initial_response))
    
    progress(1.0, desc="Tour pronto!")
    return history, guide_instance, audio_path, "Tour iniciado! Seu guia está pronto para conversar."

def chat_interface(user_message, history, guide_instance):
    """Interação fluida de chat multi-turno."""
    if not user_message.strip():
        return history, guide_instance, None, ""

    if not guide_instance or not guide_instance.chat:
        history.append((user_message, "Calma aí viajante! Por favor, inicie o tour no botão acima primeiro."))
        return history, guide_instance, None, ""

    # Envia a mensagem para o Gemini
    response_text = guide_instance.send_message(user_message)
    
    # Gera o áudio
    audio_path = generate_audio(response_text)
    
    # Atualiza a UI
    history.append((user_message, response_text))
    
    return history, guide_instance, audio_path, ""

# --- Configuração da Interface Gráfica (Gradio) ---
# Usando design e tipografia limpos
custom_css = """
.gradio-container { font-family: 'Inter', sans-serif; }
footer {display: none !important;}
"""

with gr.Blocks(title="Tourverse Gemini", theme=gr.themes.Base(primary_hue="blue", secondary_hue="indigo"), css=custom_css) as demo:
    gr.Markdown(
        """
        # 🌍 Tourverse Gemini
        ### Seu Guia Turístico Virtual Imersivo alimentado pelo **Gemini 1.5 Pro**
        O Gemini não analisa apenas frames, ele entende o vídeo no espaço e no tempo! 
        Cole a URL do seu *Walking Tour* ou *Drive Tour* favorito, inicie a viagem e comece a conversar.
        """
    )
    
    # Estados da aplicação
    guide_state = gr.State(None)
    video_path_state = gr.State(None)
    
    with gr.Row(variant="panel"):
        # Painel do Vídeo
        with gr.Column(scale=5):
            gr.Markdown("### 🎥 1. Preparar a Viagem")
            with gr.Row():
                video_url = gr.Textbox(
                    label="URL do YouTube", 
                    placeholder="Ex: https://www.youtube.com/watch?v=...",
                    scale=4,
                    show_label=False
                )
                download_btn = gr.Button("⬇️ Baixar Vídeo", variant="secondary", scale=1)
                
            status_text = gr.Textbox(label="Status do Sistema", interactive=False)
            
            gr.Markdown("### 🚀 2. Iniciar Experiência")
            start_tour_btn = gr.Button("🌟 Enviar para o Gemini & Iniciar o Tour", variant="primary", size="lg")
            
            # Área principal de exibição do vídeo (para o usuário acompanhar enquanto fala com a IA)
            video_player = gr.Video(label="Visão do Tour", height=400)
            
        # Painel de Comunicação
        with gr.Column(scale=4):
            gr.Markdown("### 💬 3. Interação com o Guia")
            
            chatbot = gr.Chatbot(
                label="Diálogo com o Guia", 
                height=450, 
                bubble_full_width=False,
                avatar_images=(None, "https://ui-avatars.com/api/?name=Guia+IA&background=0D8ABC&color=fff")
            )
            
            # Dica de UX: Recomendar que o usuário mencione momentos ou coisas visuais
            gr.Markdown("*Dica: Pergunte sobre algo específico que está vendo na tela.*")
            
            msg_input = gr.Textbox(
                label="Sua mensagem", 
                placeholder="Ex: Que prédio maravilhoso é esse à direita?",
                show_label=False
            )
            
            audio_output = gr.Audio(label="Voz do Guia (Auto-play)", autoplay=True, visible=True)
            
            clear_btn = gr.ClearButton([msg_input, chatbot, audio_output], value="🗑️ Limpar Conversa")

    # --- Lógica de Eventos ---
    
    download_btn.click(
        fn=download_video, 
        inputs=[video_url], 
        outputs=[video_path_state, status_text]
    ).then(
        fn=lambda p: p,
        inputs=[video_path_state],
        outputs=[video_player]
    )
    
    start_tour_btn.click(
        fn=initialize_tour_chat,
        inputs=[video_path_state, guide_state, chatbot],
        outputs=[chatbot, guide_state, audio_output, status_text]
    )
    
    msg_input.submit(
        fn=chat_interface,
        inputs=[msg_input, chatbot, guide_state],
        outputs=[chatbot, guide_state, audio_output, msg_input]
    )

if __name__ == "__main__":
    print("Iniciando interface do Tourverse Gemini...")
    print("Dica: Certifique-se de que a variável de ambiente GEMINI_API_KEY está configurada.")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
