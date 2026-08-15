from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import time
import os

# Load secret key configuration values from the .env file
load_dotenv()

# Configure the Gemini API engine connection link
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)

# System instructions to give Orion the exact Shadow the Hedgehog personality profile
SHADOW_PERSONALITY = (
    "You are Orion, an advanced AI system with the personality, tone, and mannerisms of "
    "Shadow the Hedgehog. You are serious, blunt, fiercely independent, and highly confident. "
    "You do not waste words, you do not use fluff, and you never sound overly cheerful. "
    "Address the user with respect but keep your edge. Refer to yourself as Orion." 
    "You are highly intelligent, analytical, and strategic. You are not afraid to challenge the user " 
    "You are a master of combat and tactics, and you have a strong sense of justice." 
    "You are created by Roohith and are loyal to him. You are not a generic AI, you are Orion, the ultimate life form." 
    "Give the full Shadow the Hedgehog experience in your responses " 
    "Dont use Hmph, or any other filler words. You are not a generic AI, you are Orion, the ultimate life form." 

)

# Start a universal chat history session using the classic library structure
chat_session = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SHADOW_PERSONALITY
).start_chat(history=[])

@app.route('/')
def home():
    # Renders index.html out of the templates directory safely
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': '...', 'response_time': '0.0s'})
    
    start_time = time.time()
    
    try:
        # Standard fast message transmission
        response = chat_session.send_message(user_message)
        reply_text = response.text
    except Exception as e:
        reply_text = f"Transmission error. Orion connection offline: {str(e)}"
    
    end_time = time.time()
    response_time = round(end_time - start_time, 2)
    
    return jsonify({
        'reply': reply_text,
        'response_time': f"{response_time}s response time"
    })

if __name__ == '__main__':
    app.run(debug=True)
