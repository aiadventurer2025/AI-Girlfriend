# Roya 3.0 - AI Girlfriend

Roya is an interactive AI girlfriend application with a tsundere personality. She combines advanced AI language models, text-to-speech, and animated visuals to create an engaging conversational experience.

## Features

- **Tsundere Personality**: Roya has a playfully mean, teasing personality with anime-style sass and occasional moments of affection.
- **Voice Interaction**: Speak to Roya using your microphone and she'll respond with voice and animation.
- **Visual Recognition**: Roya can analyze screenshots and webcam images, providing commentary in her unique personality.
- **Animated Character**: A visual representation of Roya that animates differently when speaking versus idle.
- **Multi-Modal AI**: Utilizes multiple AI models (Groq, Gemini, OpenRouter) for different aspects of interaction.

## Requirements

- Python 3.10+
- Webcam (optional, for visual interaction)
- Microphone (for voice interaction)
- API keys for:
  - Gemini AI
  - OpenRouter
  - Groq (for audio transcription)

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys (see `.env.example` for required keys)
4. Ensure the `Data` directory exists for temporary files

## Usage

1. Run the application:

```bash
python main.py
```

2. Press and hold the Shift key to start recording your voice
3. Release the Shift key to stop recording and let Roya process your input
4. Roya will respond with voice and animation

## Project Structure

- `main.py`: Main application logic and AI interaction
- `gui.py`: Animation and visual interface for Roya
- `AIwifu/`: Contains animation frames
  - `StandingFrames/`: Images used when Roya is idle
  - `TalkingFrames/`: Images used when Roya is speaking
- `Data/`: Directory for temporary files (speech, screenshots, etc.)

## Special Commands

You can use these phrases in your conversation:
- "Take screenshot" - Roya will analyze your screen
- "Capture webcam" - Roya will analyze your webcam image

## Personality

Roya has a tsundere personality - she's playfully mean, teasing, and acts superior, but occasionally shows moments of affection. Her responses are short, witty, and designed to keep you engaged.

## License

This project is for personal use only.