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

    # --- VOICE SPECIFIC LOGIC ---
    if 'Madhur' in voice:
        pitch_base = 12
        rate_base = 2
    else:
        pitch_base = 2
        rate_base = 0

    # --- MOOD LOGIC (Using your exact speed/rate values) ---
    if mood == 'caring':
        r, p = rate_base + 6, pitch_base
    elif mood == 'excited':
        r, p = rate_base + 14, pitch_base + 5
    elif mood == 'sad':
        r, p = rate_base + 3, pitch_base - 5
    elif mood == 'motivational':
        r, p = rate_base + 11, pitch_base + 3
    elif mood == 'apologetic':
        r, p = rate_base - 5, pitch_base - 1
    else:  # friendly / professional
        r, p = rate_base, pitch_base

    # --- STRICT SIGN CONTROL (+/- Logic) ---
    # Isse '+2%' ya '-5%' jaisa format fix ho jayega
    rate_str = f"{r:+}%"
    pitch_str = f"{p:+}Hz"

    output_file = "output.mp3"
    
    async def generate():
        # Using formatted rate and pitch strings
        communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
        await asyncio.wait_for(communicate.save(output_file), timeout=15)

    try:
        if os.path.exists(output_file):
            os.remove(output_file)
            
        asyncio.run(generate())
        return send_file(output_file, mimetype="audio/mpeg")
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
        
