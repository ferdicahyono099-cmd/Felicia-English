"""
Felicia — MVP chatbot belajar Bahasa Inggris.
Platform: Render.com (Web Service)
LLM: Groq gpt-oss-20b
Tanpa RAG, tanpa chunk. Semua dari prompt + LLM.
"""

import os
import gradio as gr
from groq import Groq

from prompts import SYSTEM_PROMPT

# ==============================
# SETUP
# ==============================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"

MAX_HISTORY = 6
MAX_TOKENS = 500

# ==============================
# LOGIKA CHAT
# ==============================
def respond(message: str, history: list) -> str:
    """Kirim pesan ke Groq, balikin jawaban Felicia."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    recent = history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history
    for user_msg, bot_msg in recent:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=MAX_TOKENS,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Aduh, Felicia lagi error nih: {str(e)[:100]}. Coba lagi ya!"

# ==============================
# UI GRADIO
# ==============================
demo = gr.ChatInterface(
    fn=respond,
    title="🎓 Felicia — Belajar Bahasa Inggris",
    description=(
        "Hai! Aku Felicia, teman belajar Bahasa Inggris kamu. "
        "Tanya apa aja soal grammar, vocabulary, atau ngobrol santai — aku siap bantu! 🇬🇧"
    ),
    examples=[
        "Jelaskan simple present tense dong",
        "Apa bedanya 'make' dan 'do'?",
        "Coba koreksi: I am go to school yesterday",
        "Hi Felicia, how are you today?",
    ],
    theme="soft",
)

# ==============================
# LAUNCH (disesuaikan untuk Render)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
