import asyncio
import edge_tts
from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/speak')
def speak():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'hi-IN-SwaraNeural')
    # Humne ye mood parameter add kiya hai
    mood = request.args.get('mood', 'friendly').lower()

    # Mood Tuning Logic
    # Rate: - matlab slow, + matlab fast
    # Pitch: + matlab sweet/high, - matlab deep/low
        if mood == 'caring':
        rate, pitch = '+0%', '+2Hz'   # Pehle -15% tha, ab fast lagega
    elif mood == 'excited':
        rate, pitch = '+15%', '+5Hz'  # Thoda aur energetic
    elif mood == 'sad':
        rate, pitch = '-5%', '-3Hz'  # Zyada slow nahi kiya
    elif mood == 'motivational':
        rate, pitch = '+8%', '+3Hz'
    elif mood == 'professional':
        rate, pitch = '+0%', '+0Hz'
    elif mood == 'apologetic':
        rate, pitch = '-3%', '-1Hz'
    else:  # Default 'friendly'
        rate, pitch = '+0%', '+1Hz'   # Normal speed


    output_file = "output.mp3"
    
    # edge-tts ko instructions dena
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    asyncio.run(communicate.save(output_file))
    
    return send_file(output_file, mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
