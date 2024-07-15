from tkinter import messagebox

def update_progress():
    try:
        global progress_bar
        progress_bar.step(1)
    except:
        pass

def show_error(message):
    messagebox.showerror("Error", message)
