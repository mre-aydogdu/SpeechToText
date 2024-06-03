import threading

from customtkinter import *
from customtkinter import CTkEntry
from PIL import Image
from functions import VoskTranscribe, WhisperTranscribe, UploadAction, ResetPath, Enhance, \
    UploadAction_Text, play_normal, read_text_file

entry_file_path = None
original_text = None

def create_ui(app):
    # Add a text box to show the file name and path
    global entry_file_path
    global original_text_path
    global original_text

    custom_font = CTkFont(family="Montserrat", size=14, weight="bold")
    cross_image = CTkImage(Image.open("Icons/close.png").resize((20, 20), Image.Resampling.LANCZOS))
    play_image = CTkImage(Image.open("Icons/play_image.png").resize((20, 20), Image.Resampling.LANCZOS))

    def update_original_text():
        global original_text
        file_path = original_text_path.get()  # Get the file path from the entry widget

        # Read the content of the selected text file
        original_text = read_text_file(file_path)

        # Debug print to verify that original_text is properly updated
        print("Original Text:", original_text)

    play_button = CTkButton(master=app, image=play_image, text="", command=lambda: play_normal(entry_file_path.get()))
    play_button.place(relx=0.285, rely=0.1, anchor=CENTER, relwidth=0.02)

    play_button2 = CTkButton(master=app, image=play_image, text="", command=lambda: play_normal(enhanced_file_path.get()))
    play_button2.place(relx=0.285, rely=0.13, anchor=CENTER, relwidth=0.02)

    original_text_path = CTkEntry(master=app, width=400, fg_color="#111111", border_width=0, text_color="white",
                                  font=("default", 10), state="normal")
    original_text_path.place(relx=0.5, rely=0.05, anchor=CENTER)

    button_open_origin = CTkButton(master=app, text='Load Text', command=lambda: [UploadAction_Text(original_text_path), update_original_text()],
                                   font=custom_font)
    button_open_origin.place(relx=0.69, rely=0.05, anchor=CENTER, relwidth=0.09)

    reset_button_original = CTkButton(master=app, image=cross_image, text='', fg_color="#1E201F",
                                      command=lambda: ResetPath(entry_file_path, enhanced_file_path, original_text_path,
                                                                "original_path"))
    reset_button_original.place(relx=0.635, rely=0.05, anchor=CENTER, relwidth=0.02)

    entry_file_path = CTkEntry(master=app, fg_color="#111111", border_width=0, text_color="white",
                               font=("default", 10), state="normal")
    entry_file_path.place(relx=0.5, rely=0.1, anchor=CENTER, relwidth=0.4)
    entry_file_path.configure(state="readonly")

    enhanced_file_path = CTkEntry(master=app, fg_color="#111111", border_width=0, text_color="white",
                                  font=("default", 10), state="normal")
    enhanced_file_path.place(relx=0.5, rely=0.13, anchor=CENTER, relwidth=0.4)
    enhanced_file_path.configure(state="readonly")

    # Define the custom font

    button_open = CTkButton(master=app, text='Load', command=lambda: UploadAction(entry_file_path),
                            font=custom_font)
    button_open.place(relx=0.69, rely=0.1, anchor=CENTER, relwidth=0.09)

    whisper_button_enhance = CTkButton(master=app, text='Transcribe Enhanced File with Whisper', fg_color="purple",
                                       command=lambda: WhisperTranscribe(enhanced_file_path, whisper_textbox_enhanced,
                                                                         whisper_similarity_label_enhanced,
                                                                         original_text), font=custom_font)
    whisper_button_enhance.place(relx=0.25, rely=0.69, anchor=CENTER, relwidth=0.4)

    # Use CTkButton instead of tkinter Button
    button_whisper = CTkButton(master=app, text="Transcribe with Whisper", hover_color="red",
                               command=lambda: WhisperTranscribe(entry_file_path, whisper_textbox,
                                                                 whisper_similarity_label, original_text),
                               font=custom_font)
    button_whisper.place(relx=0.25, rely=0.3, anchor=CENTER, relwidth=0.4)

    vosk_button_enhance = CTkButton(master=app, text='Transcribe Enhanced File with Vosk', fg_color="purple",
                                    command=lambda: VoskTranscribe(enhanced_file_path, vosk_textbox_enhanced,
                                                                   vosk_similarity_label_enhanced, original_text),
                                    font=custom_font)
    vosk_button_enhance.place(relx=0.75, rely=0.69, anchor=CENTER, relwidth=0.4)

    button_vosk = CTkButton(master=app, text="Transcribe with Vosk", hover_color="orange",
                            command=lambda: VoskTranscribe(entry_file_path, vosk_textbox,
                                                           vosk_similarity_label, original_text),
                            font=custom_font)
    button_vosk.place(relx=0.75, rely=0.3, anchor=CENTER, relwidth=0.4)

    # Add a Reset button to clear the selected file and path
    reset_button = CTkButton(master=app, image=cross_image, text='', fg_color="#1E201F",
                             command=lambda: ResetPath(entry_file_path, enhanced_file_path, original_text_path,
                                                       "entry"))
    reset_button.place(relx=0.635, rely=0.1, anchor=CENTER, relwidth=0.02)
    reset_button_2 = CTkButton(master=app, image=cross_image, text='', fg_color="#1E201F",
                               command=lambda: ResetPath(entry_file_path, enhanced_file_path, original_text_path,
                                                         "enhanced"))
    reset_button_2.place(relx=0.635, rely=0.13, anchor=CENTER, relwidth=0.02)
    button_enhance = CTkButton(master=app, text='Enhance', fg_color="purple",
                               command=lambda: Enhance(entry_file_path, enhanced_file_path), font=custom_font)
    button_enhance.place(relx=0.69, rely=0.13, anchor=CENTER, relwidth=0.092)

    vosk_textbox = CTkTextbox(master=app, fg_color="#111111", border_width=0,
                              text_color="white", font=("default", 20), state="normal")
    vosk_textbox.place(relx=0.75, rely=0.46, anchor=CENTER, relwidth=0.4, relheight=0.25)
    vosk_textbox.configure(state="disabled")

    whisper_textbox = CTkTextbox(master=app, fg_color="#111111", border_width=0,
                                 text_color="white", font=("default", 20), state="normal")
    whisper_textbox.place(relx=0.25, rely=0.46, anchor=CENTER, relwidth=0.4, relheight=0.25)
    whisper_textbox.configure(state="disabled")

    whisper_textbox_enhanced = CTkTextbox(master=app, fg_color="#111111", border_width=0,
                                          text_color="white", font=("default", 20), state="normal")
    whisper_textbox_enhanced.place(relx=0.25, rely=0.85, anchor=CENTER, relwidth=0.4, relheight=0.25)
    whisper_textbox_enhanced.configure(state="disabled")

    vosk_textbox_enhanced = CTkTextbox(master=app, fg_color="#111111", border_width=0,
                                       text_color="white", font=("default", 20), state="normal")
    vosk_textbox_enhanced.place(relx=0.75, rely=0.85, anchor=CENTER, relwidth=0.4, relheight=0.25)
    vosk_textbox_enhanced.configure(state="disabled")

    # Add labels to display similarity percentages
    whisper_similarity_label = CTkLabel(master=app, text="Whisper Similarity: N/A", font=custom_font)
    whisper_similarity_label.place(relx=0.25, rely=0.55, anchor=CENTER)

    vosk_similarity_label = CTkLabel(master=app, text="Vosk Similarity: N/A", font=custom_font)
    vosk_similarity_label.place(relx=0.75, rely=0.55, anchor=CENTER)

    whisper_similarity_label_enhanced = CTkLabel(master=app, text="Whisper Similarity (Enhanced): N/A",
                                                 font=custom_font)
    whisper_similarity_label_enhanced.place(relx=0.25, rely=0.95, anchor=CENTER)

    vosk_similarity_label_enhanced = CTkLabel(master=app, text="Vosk Similarity (Enhanced): N/A", font=custom_font)
    vosk_similarity_label_enhanced.place(relx=0.75, rely=0.95, anchor=CENTER)

    return entry_file_path, vosk_textbox, whisper_textbox, enhanced_file_path

