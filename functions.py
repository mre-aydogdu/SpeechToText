import json
import wave
import os
from tkinter import filedialog, END
import whisper
import soundfile as sf
from scipy.signal import resample
from vosk import Model, KaldiRecognizer

model_whisper = whisper.load_model("base")
model_vosk = "vosk-model-small-tr-0.3"


def VoskTranscribe(entry_file_path):
    print("VoskTranscribe")


def WhisperTranscribe(entry_file_path):
    filename = entry_file_path.get()
    if filename:
        print(f"Transcribing with Whisper: {filename}")
        result = model_whisper.transcribe(filename)
        print("Transcription:", result["text"])
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
