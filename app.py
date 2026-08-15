from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import time
import os

# Load secret key configuration values from the local .env file
load_dotenv()

# Initialize the mandatory modern Google GenAI Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)

# System instructions to give Orion the exact Shadow the Hedgehog personality profile
SHADOW_PERSONALITY = (
    "You are Orion, an advanced AI system with the personality, tone, and mannerisms of "
    "Shadow the Hedgehog. You are serious, blunt, fiercely independent, and highly confident. "
    "You do not waste words, you do not use fluff, and you never sound overly cheerful. "
    "Address the user with respect but keep your edge. Refer to yourself as Orion. "
    "Keep responses short (one or two sentences maximum)."
)

# We keep track of the conversation flow using a global tracker variable
current_interaction_id = None

@app.route('/')
def home():
    global current_interaction_id
    current_interaction_id = None  # Reset backend interaction state memory on home reload
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global current_interaction_id
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': '...', 'response_time': '0.0s'})
    
    start_time = time.time()
    
    try:
        # Check if there is an active session id to link previous history context
        prev_id = current_interaction_id if current_interaction_id else None

        # Execute the correct client interactions call without nested configs
        interaction = client.interactions.create(
            model="gemini-2.5-flash-lite",
            input=user_message,
            system_instruction=SHADOW_PERSONALITY,
            temperature=0.7,
            previous_interaction_id=prev_id
        )
        
        # Store the conversation state context ID on Google's cloud server
        current_interaction_id = interaction.id
        
        # Read content outputs from the step sequence sequence loop layout
        reply_text = ""
        for step in interaction.steps:
            if step.type == "model_output":
                reply_text = step.content.text
                break
                
        if not reply_text:
            reply_text = "..."

    except Exception as e:
        reply_text = f"Transmission error. Orion framework upgrade offline: {str(e)}"
    
    end_time = time.time()
    response_time = round(end_time - start_time, 2)
    
    return jsonify({
        'reply': reply_text,
        'response_time': f"{response_time}s response time"
    })

if __name__ == '__main__':
    app.run(debug=True)
