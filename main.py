import asyncio
import edge_tts
from flask import Flask, request, send_file
import os

app = Flask(__name__)

async def generate_speech(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.route('/speak')
def speak():
    # Android se 'text' aur 'voice' parameters aayenge
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'hi-IN-SwaraNeural')
    
    if not text:
        return "No text provided", 400
        
    output_file = "output.mp3"
    # Audio generate karke temporary file mein save karega
    asyncio.run(generate_speech(text, voice, output_file))
    
    # Wo MP3 file wapas Android app ko bhej dega
    return send_file(output_file, mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
