import os
import string
from tkinter import filedialog
import ffmpeg
import whisper
from df.enhance import enhance, init_df, load_audio, save_audio
import subprocess
from tkinter import END

model_whisper = whisper.load_model("base")
model_vosk = "vosk-model-small-tr-0.3"


def read_text_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().lower()  # Convert text to lowercase
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None


def calculate_similarity(text1, text2):
    if text1 is None or text2 is None:
        return -1
    else:
        words1 = set(text1.split())
        words2 = set(text2.split())

        print(f'Text1 words: {words1}')  # Debug print
        print(f'Text2 words: {words2}')  # Debug print

        common_words = words1 & words2
        similarity = (len(common_words) / max(len(words1), len(words2))) * 100
        return similarity



def normalize_text(text):
    # Convert all capital letters to lowercase
    normalized_text = text.lower()

    # Remove punctuation using translation and str.maketrans
    return text.lower().translate(str.maketrans("", "", string.punctuation))


def VoskTranscribe(entry_file_path, textbox, similarity_label, original_text, language='tr'):
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

            print("Before similarity calculation")  # Debug print
            similarity_percentage = calculate_similarity(original_text,
                                                         vosk_text)  # Ensure correct variables are passed
            print(f'Similarity Percentage: {similarity_percentage:.2f}%')
            print("After similarity calculation")  # Debug print

            similarity_label.configure(text=f"Vosk Similarity: {similarity_percentage:.2f}%")

    except Exception as e:
        print(f"An error occurred while reading the transcription file: {e}")


def WhisperTranscribe(entry_file_path, textbox, similarity_label, original_text):
    filename = entry_file_path.get()

    if not filename:
        print("No file selected")
        return

    # Convert the input file to WAV using ffmpeg
    converted_filename = './cache/converted_audio.wav'
    try:
        (
            ffmpeg
            .input(filename)
            .output(converted_filename)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e}")
        return

    if not os.path.isfile(converted_filename):
        print(f"Converted file does not exist: {converted_filename}")
        return

    print(f"Transcribing with Whisper: {filename}")

    try:
        result = model_whisper.transcribe(converted_filename)
        normalized_text = normalize_text(result["text"])

        # Display the transcription in the specified textbox
        textbox.configure(state="normal")
        textbox.delete("1.0", END)  # Clear any previous content
        textbox.insert("1.0", normalized_text)  # Insert the transcription text
        textbox.configure(state="disabled")  # Disable editing of the textbox

        similarity = calculate_similarity(normalized_text, original_text)
        similarity_label.configure(text=f"Whisper Similarity: {similarity:.2f}%")

        print("Whisper Transcription Result:", normalized_text)
    except Exception as e:
        print(f"An error occurred during Whisper transcription: {e}")


def Enhance(entry_file_path, enhanced_file_path):
    filename = entry_file_path.get()

    # Ensure the cache directory exists
    cache_dir = './cache/'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Convert the audio file to WAV format using ffmpeg
    converted_filename = os.path.join(cache_dir, 'converted_audio.wav')
    ffmpeg_command = ['ffmpeg', '-y', '-i', filename, converted_filename]
    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg conversion: {e}")
        return

    filename = converted_filename
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


def UploadAction_Text(entry_file_path, event=None):

    filename = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    entry_file_path.configure(state="normal")
    entry_file_path.delete(0, END)
    entry_file_path.insert(0, filename)
    entry_file_path.configure(state="readonly")

    print(f'Selected: {filename}')

    # Read the text file and store its content
    original_text = read_text_file(filename)
    if original_text:
        print(f'Original text loaded: {original_text[:100]}...')  # Display the first 100 characters as a preview
    else:
        print('Failed to load the original text.')


def ResetPath(entry_file_path, enhanced_file_path, original_text_path, reset_type):
    if reset_type == "entry":
        entry_file_path.configure(state="normal")
        entry_file_path.delete(0, END)
        entry_file_path.configure(state="readonly")
    elif reset_type == "enhanced":
        enhanced_file_path.configure(state="normal")
        enhanced_file_path.delete(0, END)
        enhanced_file_path.configure(state="readonly")
    elif reset_type == "original_path":
        original_text_path.configure(state="normal")
        original_text_path.delete(0, END)
        original_text_path.configure(state="readonly")
    else:
        print("Invalid target specified for reset")
