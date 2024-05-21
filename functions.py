import string
from tkinter import filedialog

import whisper

model_whisper = whisper.load_model("base")
model_vosk = "vosk-model-small-tr-0.3"
from df.enhance import enhance, init_df, load_audio, save_audio
import subprocess
from tkinter import END


def normalize_text(text):
    # Convert all capital letters to lowercase
    normalized_text = text.lower()

    # Remove punctuation using translation and str.maketrans
    translator = str.maketrans("", "", string.punctuation)
    normalized_text = normalized_text.translate(translator)

    return normalized_text


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
            textbox.configure(state="disabled")
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
        normalized_text = normalize_text(result["text"])
        # Display the transcription in the specified textbox
        textbox.configure(state="disabled")
        textbox.delete("1.0", END)  # Clear any previous content
        textbox.insert("1.0", normalized_text)  # Insert the transcription text
        textbox.configure(state="disabled")  # Disable editing of the textbox
    else:
        print("No file selected")


def Enhance(entry_file_path, enhanced_file_path):
    filename = entry_file_path.get()
    if filename:
        print(f"Enhancing audio: {filename}")

        # Initialize DeepFilter model and state
        model, df_state, _ = init_df()

        # Load the audio file
        audio, _ = load_audio(filename, sr=df_state.sr())

        # Enhance the audio using DeepFilter
        enhanced_audio = enhance(model, df_state, audio)

        # Save the enhanced audio to a new file
        output_filename = "enhanced_audio.wav"
        save_audio(output_filename, enhanced_audio, df_state.sr())

        enhanced_file_path.configure(state="normal")
        enhanced_file_path.delete(0, END)
        enhanced_file_path.insert(0, output_filename)
        enhanced_file_path.configure(state="readonly")

        print("Audio enhancement completed.")
    else:
        print("No file selected")


def UploadAction(entry_file_path, event=None):
    filename = filedialog.askopenfilename(
        filetypes=[("MP3 files", "*.mp3"), ("M4A files", "*.m4a"), ("WAV files", "*.wav")])
    entry_file_path.configure(state="normal")
    entry_file_path.delete(0, END)
    entry_file_path.insert(0, filename)
    entry_file_path.configure(state="readonly")

    print(f'Selected: {filename}')


def ResetPath(entry_file_path, enhanced_file_path, reset_type):
    if reset_type == "entry":
        entry_file_path.configure(state="normal")
        entry_file_path.delete(0, END)
        entry_file_path.configure(state="readonly")
    elif reset_type == "enhanced":
        enhanced_file_path.configure(state="normal")
        enhanced_file_path.delete(0, END)
        enhanced_file_path.configure(state="readonly")
    else:
        print("Invalid target specified for reset")
