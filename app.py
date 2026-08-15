from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import time
import os

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)

SHADOW_PERSONALITY = (
    "You are Orion, an advanced AI system with the personality, tone, and mannerisms of "
    "Shadow the Hedgehog. You are serious, blunt, fiercely independent, and highly confident. "
    "You do not waste words, you do not use fluff, and you never sound overly cheerful. "
    "Address the user with respect but keep your edge. Refer to yourself as Orion. "
    "If the user provides an image or file, look at it carefully and analyze its data layout "
    "with cold precision, but keep your Shadow persona intact."
)

chat_session = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction=SHADOW_PERSONALITY
).start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('message', '').trim()
    uploaded_file = request.files.get('file')
    
    # If there's absolutely no data sent over, halt loop execution
    if not user_message and not uploaded_file:
        return jsonify({'reply': '...', 'response_time': '0.0s'})
    
    start_time = time.time()
    contents_payload = []

    try:
        # Handle interaction file binaries if present
        if uploaded_file and uploaded_file.filename != '':
            file_bytes = uploaded_file.read()
            mime_type = uploaded_file.mimetype
            
            # Formats document data blocks into Gemini's payload format structure
            image_part = {
                "mime_type": mime_type,
                "data": file_bytes
            }
            contents_payload.append(image_part)
            
            # If text prompt field is left blank, auto-assign an assessment instruction
            if not user_message:
                user_message = "Analyze this visual dataset data transmission immediately."

        # Append string message to the transmission container array list block
        if user_message:
            contents_payload.append(user_message)

        # Transmit the rich multi-part contents directly to Google AI Studio infrastructure
        response = chat_session.send_message(contents_payload)
        reply_text = response.text

    except Exception as e:
        reply_text = f"Transmission error. Interaction pipeline broke: {str(e)}"
    
    end_time = time.time()
    response_time = round(end_time - start_time, 2)
    
    return jsonify({
        'reply': reply_text,
        'response_time': f"{response_time}s response time"
    })

if __name__ == '__main__':
    app.run(debug=True)
