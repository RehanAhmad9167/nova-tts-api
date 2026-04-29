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
    # Madhur (Male) ko young banane ke liye high pitch boost chahiye
    if 'Madhur' in voice:
        pitch_base = 12  # Young male sound
        rate_base = 2    # Slightly faster to avoid "old" tone
    # Swara (Female) ke liye normal settings
    else:
        pitch_base = 2   # Natural female sound
        rate_base = 0    # Normal speed

    # --- MOOD LOGIC (Tuning) ---
    if mood == 'caring':
        rate, pitch = f'{rate_base+6}%', f'+{pitch_base}Hz'
    elif mood == 'excited':
        rate, pitch = f'{rate_base+14}%', f'+{pitch_base+5}Hz'
    elif mood == 'sad':
        rate, pitch = f'{rate_base+3}%', f'+{pitch_base-5}Hz'
    elif mood == 'motivational':
        rate, pitch = f'{rate_base+11}%', f'+{pitch_base+3}Hz'
    elif mood == 'professional':
        rate, pitch = f'{rate_base}%', f'+{pitch_base}Hz'
    elif mood == 'apologetic':
        rate, pitch = f'{rate_base-5}%', f'+{pitch_base-1}Hz'
    else:  # Default 'friendly'
        rate, pitch = f'{rate_base}%', f'+{pitch_base}Hz'

    output_file = "output.mp3"
    
    async def generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await asyncio.wait_for(communicate.save(output_file), timeout=15)

    try:
        # Puraani file delete karna taaki fresh audio bane
        if os.path.exists(output_file):
            os.remove(output_file)
            
        asyncio.run(generate())
        return send_file(output_file, mimetype="audio/mpeg")
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
                         
