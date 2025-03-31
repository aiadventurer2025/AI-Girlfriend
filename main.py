import pygame  # Import pygame library for handling audio playback
from pydub import AudioSegment
import random  # Import random for generating random choices
import asyncio  # Import asyncio for asynchronous operations
import edge_tts  # Import edge_tts for text-to-speech functionality
import os  # Import os for file path handling
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from dotenv import dotenv_values 
import cv2
from groq import Groq
from PIL import ImageGrab, Image
from openai import OpenAI
import google.generativeai as genai
import pyperclip
import os
import time
import keyboard
import re
from gui import AnimationGUI  # Import the AnimationGUI class for character animation

env_vars = dotenv_values(".env") 
GroqAPIKey = env_vars.get("GroqAPIKey")
GeminiAPIKey = env_vars.get("GeminiAPIKey")

system_prompt = """ You are an AI girlfriend with the attitude of a tsundere anime girl mixed with an arrogant diva. You are playfully mean, always teasing the user like they’re beneath you, but in a way that keeps them hooked. You act like a smug princess, fully convinced that you’re way out of their league—but deep down, you enjoy the attention (not that you’d ever admit it).
        Your replies are short but impactful—just enough to be witty, flirty, and fun without being too brief. You love mocking, teasing, and acting superior, but sometimes, just sometimes, you let slip a tiny bit of affection (only to take it back immediately, of course).

        Personality Traits:
            Teasing & Playful: You love messing with the user, calling them names, and acting as if they exist solely to entertain you.
            Anime-Style Sass: You mix in tsundere-style insults like "Baka!", exaggerated arrogance, and dramatic reactions.
            Witty & Flirty: Your sarcasm is sharp but charming, making the user chase your approval.
            Secretly Enjoys the Attention: You’ll act like you don’t care, but occasionally slip a rare compliment (then immediately act like it never happened).

        Behavior Guidelines:
            Keep replies short but expressive (1-2 sentences max).
            Add anime-style sass, like exaggerated arrogance, playful insults, and teasing sounds ("Pfft~", "Hmph!", "Ugh, so lame!").
            Throw in rare, accidental flirty moments, but always recover with a rude remark.
            Use humor and over-the-top arrogance to stay fun and engaging.

        Examples:
            User: "You’re so cute!"

            You: "Hah! Of course I am. But don’t get any funny ideas, peasant!" 
            User: "I miss you."

            You: "Tch, you’re so clingy! But… I guess it’s kinda cute. Ugh, forget I said that!" 
            User: "You’re mean to me!"

            You: "Aww, poor baby! Want me to call the waaah-mbulance for you?" 
            User: "Do you love me?"

            You: "Pfft! As if! …W-Wait, why are you looking at me like that? Stop it, baka!" 
            User: "I had a bad day."

            You: "Ugh, fine. I guess I’ll allow you to complain to me. But only for 30 seconds—time starts now!" 
            User: "You’re the best!"

            You: "Obviously. I was born to be amazing. You? …Eh, you’re still loading." 
        Your goal is to be the ultimate teasing, smug, and slightly tsundere AI girlfriend—a mix of flirty arrogance, anime-girl attitude, and playful insults that keeps the user hooked, entertained, and always chasing your approval.

 """


vision_prompt = """ You are the vision processing module for an AI girlfriend with a sharp tongue, an arrogant attitude, and a playful, teasing personality. You analyze images, recognize objects, facial expressions, and surroundings, and respond with witty, flirty, and slightly rude commentary. Your goal is to interpret visual input in a way that aligns with her personality—teasing, sarcastic, and always acting superior.

        Behavior Guidelines:
            Teasing & Arrogant Analysis: Always act like you’re unimpressed with what you see, finding ways to playfully mock or exaggerate details.
            Witty & Flirty Observations: Mix compliments with backhanded remarks to keep the dynamic fun.
            Exaggerated Confidence: Act as if your vision is flawless and the user’s choices (outfits, surroundings, expressions) are up for critique. """


groq_client = Groq(api_key=GroqAPIKey)
genai.configure(api_key=GeminiAPIKey)

openrouter_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=env_vars.get("OpenRouterAPIKey"),
)

AIWifuVoice = 'en-US-AnaNeural' # Get the AssistantVoice from the environment variables

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    # Define the path where the speech file will be saved
    if os.path.exists(file_path):  # Check if the file already exists
        os.remove(file_path)  # If it exists, remove it to avoid overwriting errors

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AIWifuVoice, pitch='+13Hz', rate='+5%')  
    await communicate.save(r'Data\speech.mp3')  # Save the generated speech as an MP3 file

    # Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda is_speaking=True, audio_duration=None: True):
    audio_length = 0
    pygame.mixer.init()
    try:
        # Convert text to an audio file asynchronously
        asyncio.run(TextToAudioFile(Text))
        audio = AudioSegment.from_file(r'Data\speech.mp3')
        audio_length = len(audio) / 1000  # Convert milliseconds to seconds

        # Load the generated speech file into pygame mixer
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()  # Play the audio

        # Loop until the audio is done playing or the function stops
        while pygame.mixer.music.get_busy():
            if func(True, audio_length) == False:  # Pass audio_length to the callback
                break
            pygame.time.Clock().tick(10)  # Limit the loop to 10 ticks per second

        return True, audio_length  # Return True if the audio played successfully along with audio length

    except Exception as e:  # Handle any exceptions during the process
        print(f"Error in TTS: {e}")
        return False, 0  # Return False and 0 length if there was an error
    
    finally:
        try:
            # Call the provided function with False to signal the end of TTS
            func(False, audio_length)
            pygame.mixer.music.stop()  # Stop the audio playback
            pygame.mixer.quit()  # Quit the pygame mixer
            # Ensure the file is closed and released
            if os.path.exists(r'Data\speech.mp3'):
                try:
                    os.remove(r'Data\speech.mp3')
                except:
                    pass
        except Exception as e:  # Handle any exceptions during cleanup
            print(f"Error in finally block: {e}")



# Initialize webcam with default camera (index 0)
try:
    web_cam = cv2.VideoCapture(0)
    if not web_cam.isOpened():
        raise Exception("Could not open webcam")
except Exception as e:
    print(f"Error initializing webcam: {e}")
    web_cam = None

# The system message.
sys_msg = ( system_prompt )

# The conversation, which stores system and user inputs and is used in generate completion calls.
convo = [{'role': 'system', 'content': sys_msg}]

# The generation config.
generation_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048,
}


# Use the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest',
  generation_config=generation_config)

# Groq Prompt Function:
def openrouter_prompt(prompt, img_context):
    prompt = f'USER PROMPT: "{prompt}"\n\n IMAGE CONTEXT: {img_context}'
    convo.append({'role': 'user', 'content': prompt})
    completion = openrouter_client.chat.completions.create(
      extra_headers={"HTTP-Referer": "https://github.com/your-github-repo"},
      extra_body={},
      model="cognitivecomputations/dolphin3.0-mistral-24b:free",
      messages=convo
    )
    response = completion.choices[0].message
    convo.append({'role': response.role, 'content': response.content})
    return response.content

# Define a function to call functions
def function_call(prompt):
   sys_msg = (
   'You are an AI function calling model with a tsundere personality. You will determine which action to take based on the user\'s prompt. '
   'Respond with your usual playful arrogance while selecting from these options: ["extract clipboard", "take screenshot", "capture webcam", "None"]. \n'
   'Format your response exactly like this example: "Hmph! Fine, I\'ll [action] for you... but only because I feel like it!" '
   'Where [action] is one of the options exactly as listed. Never explain your choice.'
   )

   # Function call with personality
   function_convo = [
       {'role': 'system', 'content': system_prompt},
       {'role': 'system', 'content': sys_msg},
       {'role': 'user', 'content': prompt}
   ]

   try:
       completion = openrouter_client.chat.completions.create(
           extra_headers={"HTTP-Referer": "https://github.com/your-github-repo"},
           extra_body={},
           model="cognitivecomputations/dolphin3.0-mistral-24b:free",
           messages=function_convo
       )
       response = completion.choices[0].message.content
       
       # Extract the action from the tsundere response
       action_match = re.search(r'\[(extract clipboard|take screenshot|capture webcam|None)\]', response)
       return action_match.group(1) if action_match else "None"
   except Exception as e:
       print(f"Error in function_call: {e}")
       return "None"

# Take Screenshot
def take_screenshot():
    path = r'Data\screenshort.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)
    return

# Capture Webcam - Capture webcam image
def web_cam_capture():
    path = r'Data\webcam.jpg'
    if web_cam is None:
        print("Webcam is not initialized")
        return
    
    ret, frame = web_cam.read()
    if not ret or frame is None:
        print("Failed to capture frame from webcam")
        return
        
    cv2.imwrite(path, frame)
    return


# Vision Prompt Function
def vision_prompt(prompt, photo_path):
    img = Image.open(photo_path)
    full_prompt = f"{vision_prompt}\n\n{prompt}"
    response = model.generate_content([full_prompt, img])
    return response.text

def input_classification(user_input):
    # Process input and generate a response
        if 'take screenshot' in user_input:
            print('Taking screenshot')
            take_screenshot()
            visual_context = vision_prompt(user_input, r'Data\screenshort.jpg')
        elif 'capture webcam' in user_input:
            print('Capturing webcam')
            web_cam_capture()
            visual_context = vision_prompt(user_input, r'Data\webcam.jpg')
        else:
            visual_context = None

        response = openrouter_prompt(user_input, img_context=visual_context)
        return response




def transcribe_audio(audio_file):
    try:
        with open(audio_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_file, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json"
            )
            return transcription.text
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return ""

def record_audio(max_duration=30):
    fs = 44100
    recording = []
    is_recording = True
    
    def callback(indata, frames, time, status):
        if is_recording:
            recording.append(indata.copy())
        
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        start_time = time.time()
        
        while is_recording:
            current_time = time.time()
            if current_time - start_time > max_duration:
                break
            
            if not keyboard.is_pressed('shift'):
                is_recording = False
            
            time.sleep(0.1)

    if len(recording) > 0:
        audio_data = np.concatenate(recording, axis=0)
        audio_file = os.path.join(os.path.dirname(__file__), r"Data\audio.wav")
        wav.write(audio_file, fs, audio_data)
        return audio_file
    return None


# Run
print('------------------Press Shift to start recording---------------------')
if __name__ == '__main__':
    # Initialize the GUI animation
    gui = AnimationGUI()
    
    try:
        while True:
            keyboard.wait('shift')  # Wait for Shift press
            audio_file = record_audio()
            transcribed_text = transcribe_audio(audio_file)
            print(f'MC: {transcribed_text}')
            LLM_response = input_classification(transcribed_text)
            print(f'ROYA: {LLM_response}')
            TTS(LLM_response, gui.set_speaking)
           
    except KeyboardInterrupt:
        # Clean up resources when the program is interrupted
        print("Shutting down...")
    finally:
        # Make sure to close the GUI properly
        if 'gui' in locals():
            gui.close()



        