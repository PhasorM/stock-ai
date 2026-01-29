from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import main  # Make sure this import works
import ai    # Make sure this import works

# -------------------------------------------
# THIS IS THE MISSING LINE causing your error
app = FastAPI() 
# -------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/run-agent")
async def run_agent():
    print("\n⚡ API CALL: Processing Voice Request...")
    
    # 1. Record
    # Make sure 'record_manual_api' exists in main.py
    audio_data = main.record_manual_api(duration=5)
    
    if len(audio_data) == 0:
        return {"bot_text": "I didn't hear anything."}

    # 2. Transcribe
    user_text = main.transcribe(audio_data)
    print(f"👤 User: {user_text}")

    # 3. Brain
    bot_text = ai.process_user_input(user_text)
    
    # 4. Speak
    await main.speak(bot_text)
    
    return {"user_text": user_text, "bot_text": bot_text}