import sounddevice as sd
from scipy.io import wavfile
import numpy as np

# ================= 1. AUDIO SETTINGS =================
# Optimized for Microcontrollers (STM32 / 8051)
SAMPLE_RATE = 8000  # 8000 samples per second saves RAM
DURATION = 1.0      # 1 second is enough for a single command
CHANNELS = 1        # Mono recording

# ================= 2. RECORDING FUNCTION =================
def record_command(filename, command_name):
    print(f"\n>>> PREPARING TO RECORD: [{command_name}] <<<")
    
    # Wait for the user to be ready
    input("Press [ENTER] when you are ready to speak...")
    
    print("🔴 RECORDING (1 second)... Speak loudly and clearly!")
    
    # Start recording from the microphone
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), 
                        samplerate=SAMPLE_RATE, 
                        channels=CHANNELS, 
                        dtype='int16') # int16 is standard for 16-bit audio
    
    # Block execution until recording is finished
    sd.wait() 
    
    print("✅ RECORDING COMPLETE!")
    
    # Save the array to a .wav file
    wavfile.write(filename, SAMPLE_RATE, audio_data)
    print(f"File saved successfully: {filename}")

# ================= 3. MAIN EXECUTION =================
if __name__ == "__main__":
    print("========== VOICE TEMPLATE GENERATOR ==========")
    
    # Record the "TURN ON" command
    record_command("template_ON.wav", "TURN ON (BAT)")
    
    # Record the "TURN OFF" command
    record_command("template_OFF.wav", "TURN OFF (TAT)")
    
    print("\n🎉 All done! Please check your project directory for the .wav files.")
