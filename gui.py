import pygame
import os
import time
import threading
import math  # Import math module for animation effects
import sys  # Import sys for exit handling
import win32gui  # Import win32gui for setting window always on top
import win32con  # Import win32con for window constants

class AnimationGUI:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Set window size and title
        self.width, self.height = 300, 433
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Roya")
        
        # Set window to always stay on top
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        # Load idle animation frames (displayed when not speaking)
        self.idle_animation_folder = os.path.join('AIwifu', 'StandingFrames')
        self.idle_frames = []
        self.load_idle_frames()
        
        # Load speaking animation frames (displayed when speaking)
        self.speaking_animation_folder = os.path.join('AIwifu', 'TalkingFrames')
        self.speaking_frames = []
        self.load_speaking_frames()
        
        # Animation state
        self.is_speaking = False
        self.current_idle_frame = 0
        self.current_speaking_frame = 0
        self.animation_speed = 0.2 # seconds per frame (slowed down for better visibility)
        self.last_frame_time = 0
        
        # Start animation thread
        self.running = True
        self.animation_thread = threading.Thread(target=self.animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def load_idle_frames(self):
        """Load all idle animation frames from the normal folder"""
        try:
            # Get all jpg files in the idle animation folder
            frame_files = sorted([f for f in os.listdir(self.idle_animation_folder) if f.endswith('.jpg')])
            
            # Load each frame
            for frame_file in frame_files:
                frame_path = os.path.join(self.idle_animation_folder, frame_file)
                frame = pygame.image.load(frame_path)
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.idle_frames.append(frame)
                
            print(f"Loaded {len(self.idle_frames)} idle animation frames")
        except Exception as e:
            print(f"Error loading idle animation frames: {e}")
    
    def load_speaking_frames(self):
        """Load all speaking animation frames from the Talking folder"""
        try:
            # Get all jpg files in the speaking animation folder
            frame_files = sorted([f for f in os.listdir(self.speaking_animation_folder) if f.endswith('.jpg')])
            
            # Load each frame
            for frame_file in frame_files:
                frame_path = os.path.join(self.speaking_animation_folder, frame_file)
                frame = pygame.image.load(frame_path)
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.speaking_frames.append(frame)
             
        except Exception as e:
            print(f"Error loading speaking animation frames: {e}")
    
    def animation_loop(self):
        """Main animation loop that runs in a separate thread"""
        while self.running:
            try:
                # Handle pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                
                # Draw the appropriate animation based on speaking state
                current_time = time.time()
                if current_time - self.last_frame_time > self.animation_speed:
                    self.last_frame_time = current_time
                    
                    if self.is_speaking and self.speaking_frames:
                        # Update speaking animation frame
                        self.current_speaking_frame = (self.current_speaking_frame + 1) % len(self.speaking_frames)
                        # Display the current speaking animation frame
                        self.screen.blit(self.speaking_frames[self.current_speaking_frame], (0, 0))
                    elif self.idle_frames:
                        # Update idle animation frame
                        self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_frames)
                        # Display the current idle animation frame
                        self.screen.blit(self.idle_frames[self.current_idle_frame], (0, 0))
                
                # Update the display
                pygame.display.flip()
                
                # Control the frame rate
                pygame.time.Clock().tick(30)
            except Exception as e:
                print(f"Error in animation loop: {e}")
                time.sleep(0.1)  # Prevent CPU overload in case of error
    
    def set_speaking(self, is_speaking, audio_duration=None):
        """Set the speaking state to control animation
        
        Args:
            is_speaking (bool): Whether the character is currently speaking
            audio_duration (float, optional): Duration of the audio in seconds
        
        Returns:
            bool: Always returns True to continue TTS playback
        """
        self.is_speaking = is_speaking
        return True
    
    def close(self):
        """Clean up resources and close the GUI"""
        self.running = False
        pygame.quit()