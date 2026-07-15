# 🌍 Tourverse Gemini - Protótipo Python

Este é o protótipo em Python do **Tourverse Gemini**, um guia virtual interativo construído com `Gradio`, `yt-dlp`, `gTTS` e a API do `Gemini 1.5 Pro`.

## Pré-requisitos
- Ter o **Python 3.9 a 3.12** instalado na sua máquina.
- Ter o **FFmpeg** instalado no seu sistema (recomendado para o `yt-dlp` combinar faixas de áudio e vídeo corretamente).

## 1. Instalação das Dependências

Abra seu terminal na pasta onde estes arquivos (`main.py`, etc.) foram baixados/extraídos e execute:

```bash
pip install -r requirements.txt
```

## 2. Configurar a Chave da API (Gemini)

Você precisa de uma chave de API para o Google Gemini. (Pode ser obtida no [Google AI Studio](https://aistudio.google.com/)).

Antes de rodar o código, configure a chave no seu terminal:

**No Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=sua_chave_aqui
```

**No Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="sua_chave_aqui"
```

**No Linux / macOS (Terminal):**
```bash
export GEMINI_API_KEY="sua_chave_aqui"
```

## 3. Rodar o Protótipo

Após configurar a chave, execute o aplicativo:
```bash
python main.py
```

Uma URL local (como `http://127.0.0.1:7860`) aparecerá no terminal. Basta abrir o link no seu navegador, colar a URL de um tour do YouTube e começar a conversar com seu guia!
