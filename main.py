import asyncio
import edge_tts
from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/speak')
def speak():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'hi-IN-SwaraNeural')
    mood = request.args.get('mood', 'friendly').lower()

    # Mood Tuning Logic - Speed and Pitch balance
    if mood == 'caring':
        rate, pitch = '-5%', '+2Hz'
    elif mood == 'excited':
        rate, pitch = '+15%', '+5Hz'
    elif mood == 'sad':
        rate, pitch = '-10%', '-3Hz'
    elif mood == 'motivational':
        rate, pitch = '+8%', '+3Hz'
    elif mood == 'professional':
        rate, pitch = '+0%', '+0Hz'
    elif mood == 'apologetic':
        rate, pitch = '-5%', '-1Hz'
    else:  # Default 'friendly'
        rate, pitch = '+0%', '+1Hz'

    output_file = "output.mp3"
    
    async def generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(output_file)

    try:
        asyncio.run(generate())
        return send_file(output_file, mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
