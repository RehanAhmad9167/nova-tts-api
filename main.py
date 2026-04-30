import asyncio
import edge_tts
from flask import Flask, request, Response, stream_with_context
import io

app = Flask(__name__)

@app.route('/speak')
def speak():
    text  = request.args.get('text', '')
    voice = request.args.get('voice', 'hi-IN-SwaraNeural')
    mood  = request.args.get('mood', 'friendly').lower()

    if not text.strip():
        return "No text provided", 400

    # --- VOICE SPECIFIC BASE VALUES ---
    if 'Madhur' in voice:
        pitch_base = 18
        rate_base  = 2
    else:
        pitch_base = 7
        rate_base  = 0

    # --- MOOD → RATE + PITCH ---
    mood_map = {
        'caring':       (rate_base + 14, pitch_base),
        'excited':      (rate_base + 16, pitch_base + 5),
        'sad':          (rate_base + 13, pitch_base - 5),
        'motivational': (rate_base + 15, pitch_base + 3),
        'apologetic':   (rate_base + 13, pitch_base - 1),
        'question':     (rate_base + 13, pitch_base + 4),
        'command':      (rate_base + 16, pitch_base + 1),
        'professional': (rate_base + 13, pitch_base),
    }
    r, p = mood_map.get(mood, (rate_base + 15, pitch_base))  # default = friendly

    rate_str  = f"{r:+}%"
    pitch_str = f"{p:+}Hz"

    # ✅ STREAMING — file save nahi hogi, directly chunks bhejenge
    def generate_audio():
        async def _stream():
            communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]

        # asyncio event loop run karo aur chunks yield karo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            async_gen = _stream()
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    return Response(
        stream_with_context(generate_audio()),
        mimetype="audio/mpeg",
        headers={
            "Transfer-Encoding": "chunked",
            "Cache-Control": "no-cache"
        }
    )

@app.route('/health')
def health():
    return {"status": "ok", "service": "Nova TTS API"}, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
