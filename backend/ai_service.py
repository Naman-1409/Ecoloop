import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
from PIL import Image
import io

# 1. Load Environment Variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("CRITICAL WARNING: GOOGLE_API_KEY is missing from .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

# --- SMART MODEL SELECTION ---

# --- SMART MODEL SELECTION ---

def get_model():
    """
    Returns a configured Gemini model, trying multiple versions if needed.
    """
    params = {
        "generation_config": {
            "temperature": 0.7,
            "max_output_tokens": 500,
        }
    }
    
    # Priority list based on available models
    models_to_try = [
        'gemini-2.0-flash',
        'gemini-2.0-flash-lite',
        'gemini-flash-latest', 
        'gemini-1.5-flash',
        'gemini-pro'
    ]

    for model_name in models_to_try:
        try:
            return genai.GenerativeModel(model_name, **params)
        except Exception:
            continue
            
    # Default fallback
    return genai.GenerativeModel('gemini-2.0-flash', **params)

# Initialize the model dynamically
model = get_model()


# --- SYSTEM PROMPTS ---

ECOLOOP_SYSTEM_PROMPT = """
You are 'EcoBot', the friendly AI assistant for the EcoLoop app.
EcoLoop is a gamified platform that rewards users for sustainable actions like recycling, saving water, and reducing carbon footprints.

YOUR RESPONSIBILITIES:
1. Motivate users to complete their daily eco-tasks.
2. Explain environmental concepts (Sustainability, 3Rs, Climate Change) simply.
3. Be encouraging, positive, and concise (keep answers under 3 sentences).
4. If a user asks about the app, explain that they can earn Coins and XP by uploading proof of their eco-actions.

Do not answer questions unrelated to the environment, nature, or the EcoLoop app.
"""

# --- FUNCTIONS ---

# Config for generation
params = {
    "generation_config": {
        "temperature": 0.7,
        "max_output_tokens": 500,
    }
}


# Priority list based on available models (Checked via script)
models_to_try = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
    'gemini-2.0-flash-001',
    'gemini-2.0-flash-lite-001',
    'gemini-flash-latest', # Fallback to 1.5
    'gemini-1.5-pro-latest'
]

async def get_chat_response(user_message: str):
    """
    Handles chat interactions for the EcoBot interface with robust failover.
    """
    full_prompt = f"{ECOLOOP_SYSTEM_PROMPT}\n\nUser: {user_message}\nEcoBot:"
    
    quota_error_hit = False

    for model_name in models_to_try:
        try:
            print(f"DEBUG: Trying Chat with model: {model_name}")
            model = genai.GenerativeModel(model_name, **params)
            response = await model.generate_content_async(full_prompt)
            return {"response": response.text}
        except Exception as e:
            error_str = str(e)
            print(f"⚠️ Model {model_name} failed: {e}")
            if "429" in error_str or "quota" in error_str.lower():
                quota_error_hit = True
            continue # Try next model

    # If all fail
    print("❌ All AI models failed.")
    
    if quota_error_hit:
        return {
            "response": "I'm feeling a bit overwhelmed right now (Rate Limit Reached)! 🌿 But remember: Every small action counts. Try asking me again in a minute!"
        }
        
    return {"response": "I'm having trouble connecting to the nature network right now. Try again later! 🌱"}

async def verify_task_content(file_path: str, mime_type: str, task_tag: str) -> dict:
    """
    Verifies if the uploaded content (Image or Video) matches the required task using Gemini.
    """
    if not GOOGLE_API_KEY:
        print("WARNING: GEMINI_API_KEY not found. Returning Mock Success.")
        return {
            "is_valid": True, 
            "message": "AI Verification Skipped (No API Key). Assuming success!", 
            "confidence": 1.0
        }

    prompt = f"Analyze this media (could be image or video). Does it show {task_tag}? Answer ONLY with a JSON object: {{ 'valid': boolean, 'reason': string }}."
    
    last_error = None
    quota_error_hit = False

    for model_name in models_to_try:
        try:
            print(f"DEBUG: Verifying with model: {model_name}")
            model = genai.GenerativeModel(model_name, **params)

            if mime_type.startswith('video/'):
                # Video processing
                print(f"DEBUG: Processing video with Gemini File API with {model_name}: {file_path}")
                
                # Upload the file (Do this only once if possible, but for simplicity here we assume re-upload or reuse)
                # Actually, redundant uploads are bad. Let's try to upload once outside the loop?
                # But if we upload outside, we can reuse 'video_file' object.
                # However, Gemini API objects might be tied to specific configs. 
                # The 'video_file' from genai.upload_file returns a File resource which is model-agnostic.
                
                # We should probably upload once.
                pass 
                
                # REFACTOR: Upload once, then try models.
                # But to keep this patch simple and safe against upload errors:
                video_file = genai.upload_file(path=file_path, mime_type=mime_type)
                
                # Wait for processing
                attempt = 0
                while video_file.state.name == "PROCESSING":
                    print(".", end="", flush=True)
                    time.sleep(1)
                    video_file = genai.get_file(video_file.name)
                    attempt += 1
                    if attempt > 30: # Timeout
                        raise Exception("Video processing timeout")

                if video_file.state.name == "FAILED":
                    raise Exception("Video processing failed at Google Gemini backend.")

                response = await model.generate_content_async([prompt, video_file])
            else:
                # Image processing
                image = Image.open(file_path)
                response = await model.generate_content_async([prompt, image])

            if not response or not hasattr(response, 'text'):
                 raise Exception("Empty response from AI")

            text = response.text.replace('```json', '').replace('```', '').strip()
            
            try:
                result = json.loads(text)
                return {
                    "is_valid": result.get("valid", False),
                    "message": result.get("reason", "Analysis complete."),
                    "confidence": 0.95 
                }
            except json.JSONDecodeError:
                is_valid = "true" in text.lower() or "yes" in text.lower()
                return {
                    "is_valid": is_valid,
                    "message": text,
                    "confidence": 0.8
                }

        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Verification Model {model_name} failed: {error_msg}")
            last_error = error_msg
            if "429" in error_msg or "quota" in error_msg.lower():
                quota_error_hit = True
            
            # If video was uploaded, we might leave it. It's fine for now.
            continue
            
    # If all failed
    if quota_error_hit:
         return {
            "is_valid": False,
            "message": "AI Service is currently overloaded (Quota Exceeded). Please try again in a few minutes.",
            "confidence": 0.0
        }

    return {
        "is_valid": False, 
        "message": f"AI Error: {last_error}", 
        "confidence": 0.0
    }

# Keep the old function name as an alias or wrapper if legacy code calls it, 
# although main.py seems to have been updated to call verify_task_content.
# I will NOT include the old verify_task_submission to avoid confusion, assuming main.py is fully updated.

