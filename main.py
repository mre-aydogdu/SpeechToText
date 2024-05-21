from customtkinter import CTk, set_appearance_mode, set_default_color_theme
from ui import create_ui

if __name__ == "__main__":
    set_appearance_mode("dark")  # Modes: system (default), light, dark
    set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app = CTk()  # create CTk window like you do with the Tk window
    app.geometry("1620x980")
    create_ui(app)

    app.mainloop()
