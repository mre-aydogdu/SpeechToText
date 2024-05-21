import json
import wave
import os
from tkinter import filedialog, END
import whisper
import subprocess
import soundfile as sf
from scipy.signal import resample
from vosk import Model, KaldiRecognizer

model_whisper = whisper.load_model("base")
model_vosk = "vosk-model-small-tr-0.3"

import subprocess
from tkinter import END


def VoskTranscribe(entry_file_path, textbox, language='tr'):
    filename = entry_file_path.get()
    if not filename:
        print("No file selected")
        return

    print(f"Transcribing with Vosk: {filename}")
    output_file = "vosk_transcription.txt"
    command = ['vosk-transcriber', '-l', language, '-i', filename, '-t', 'txt', '-o', output_file]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error during Vosk transcription: {result.stderr}")
            return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    try:
        with open(output_file, "r") as f:
            vosk_text = f.read()
            textbox.configure(state="normal")
            textbox.delete("1.0", END)
            textbox.insert("1.0", vosk_text)
            textbox.configure(state="disabled")
            print("Vosk Transcription Result:", vosk_text)
    except Exception as e:
        print(f"An error occurred while reading the transcription file: {e}")


def WhisperTranscribe(entry_file_path, textbox):
    filename = entry_file_path.get()
    if filename:
        print(f"Transcribing with Whisper: {filename}")
        result = model_whisper.transcribe(filename)
        print("Transcription:", result["text"])

        # Display the transcription in the specified textbox
        textbox.configure(state="normal")
        textbox.delete("1.0", END)  # Clear any previous content
        textbox.insert("1.0", result["text"])  # Insert the transcription text
        textbox.configure(state="disabled")  # Disable editing of the textbox
    else:
        print("No file selected")



def Enhance(entry_file_path):
    filename = entry_file_path.get()
    print(f"Enhancing: {filename}")


def UploadAction(entry_file_path, event=None):
    filename = filedialog.askopenfilename(
        filetypes=[("MP3 files", "*.mp3"), ("M4A files", "*.m4a"), ("WAV files", "*.wav")])
    entry_file_path.delete(0, END)
    entry_file_path.insert(0, filename)
    print(f'Selected: {filename}')


def ResetPath(entry_file_path):
    entry_file_path.delete(0, END)
