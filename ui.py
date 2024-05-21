from customtkinter import *
from customtkinter import CTkEntry
from PIL import Image

from functions import VoskTranscribe, WhisperTranscribe, UploadAction, ResetPath, Enhance

entry_file_path = None


def create_ui(app):
    # Add a text box to show the file name and path
    global entry_file_path
    cross_image = CTkImage(Image.open("Icons/close.png").resize((20, 20), Image.Resampling.LANCZOS))

    entry_file_path = CTkEntry(master=app, width=400, fg_color="#111111", border_width=0, text_color="white",
                               font=("default", 10), state="normal")
    entry_file_path.place(relx=0.5, rely=0.1, anchor=CENTER)
    entry_file_path.configure(state="readonly")

    enhanced_file_path = CTkEntry(master=app, width=400, fg_color="#111111", border_width=0, text_color="white",
                                  font=("default", 10), state="normal")
    enhanced_file_path.place(relx=0.5, rely=0.13, anchor=CENTER)
    enhanced_file_path.configure(state="readonly")

    # Define the custom font
    custom_font = CTkFont(family="Montserrat", size=14, weight="bold")
    button_open = CTkButton(master=app, text='Load', command=lambda: UploadAction(entry_file_path),
                            font=custom_font)
    button_open.place(relx=0.69, rely=0.1, anchor=CENTER)

    # Use CTkButton instead of tkinter Button
    button_whisper = CTkButton(master=app, text="Transcribe with Whisper", width=200, hover_color="red",
                               command=lambda: WhisperTranscribe(entry_file_path, whisper_textbox), font=custom_font)
    button_whisper.place(relx=0.25, rely=0.3, anchor=CENTER)

    button_vosk = CTkButton(master=app, text="Transcribe with Vosk", width=200, hover_color="orange",
                            command=lambda: VoskTranscribe(entry_file_path, vosk_textbox), font=custom_font)
    button_vosk.place(relx=0.75, rely=0.3, anchor=CENTER)

    # Add a Reset button to clear the selected file and path
    reset_button = CTkButton(master=app, image=cross_image, text='', width=30, fg_color="#1E201F",
                             command=lambda: ResetPath(entry_file_path, enhanced_file_path, "entry"))
    reset_button.place(relx=0.635, rely=0.1, anchor=CENTER)

    reset_button_2 = CTkButton(master=app, image=cross_image, text='', width=30, fg_color="#1E201F",
                               command=lambda: ResetPath(entry_file_path, enhanced_file_path, "enhanced"))
    reset_button_2.place(relx=0.635, rely=0.13, anchor=CENTER)

    button_enhance = CTkButton(master=app, text='Enhance', fg_color="purple",
                               command=lambda: Enhance(entry_file_path, enhanced_file_path), font=custom_font)
    button_enhance.place(relx=0.69, rely=0.13, anchor=CENTER)

    vosk_textbox = CTkTextbox(master=app, width=400, height=300, fg_color="#111111", border_width=0,
                              text_color="white", font=("default", 20), state="normal")
    vosk_textbox.place(relx=0.75, rely=0.5, anchor=CENTER)
    vosk_textbox.configure(state="disabled")
    whisper_textbox = CTkTextbox(master=app, width=400, height=300, fg_color="#111111", border_width=0,
                                 text_color="white", font=("default", 20), state="normal")
    whisper_textbox.place(relx=0.25, rely=0.5, anchor=CENTER)
    whisper_textbox.configure(state="disabled")
    return entry_file_path, vosk_textbox, whisper_textbox
