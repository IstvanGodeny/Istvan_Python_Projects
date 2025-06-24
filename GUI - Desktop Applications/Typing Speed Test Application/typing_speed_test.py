"""
Application: Typing Speed Test
Author: Istvan Godeny
Date: 24/06/2025
Licence: MIT Licence
"""

import time
from tkinter import Tk, Label, Frame, Button, filedialog, Text
from refernce_texts import texts
from random import randint

# Variables
test_in_progress = False
typing_started = False
start_typing = None

def start_test():
    number = randint(0, len(texts)-1)
    test_text = texts[number]
    userText.delete("1.0", "end")
    referenceText.configure(state="normal")
    referenceText.delete("1.0", "end")
    referenceText.insert("1.0", test_text)
    referenceText.configure(state="disabled", font=["Courier", 15])
    userText.focus()
    global  start_typing
    start_typing = time.time()


def reset():
    referenceText.configure(state="normal")
    referenceText.delete("1.0", "end")
    referenceText.configure(state="disabled")
    userText.delete("1.0", "end")
    resultLabel.configure(text="")
    startButton.configure(state="normal")
    global test_in_progress
    test_in_progress = False
    global typing_started
    typing_started = False
    global start_typing
    start_typing = None


def on_typing(event):
    global typing_started, test_in_progress

    if not typing_started:
        typing_started = True
        startButton.configure(state="disabled")
        test_in_progress = True

    typed = userText.get("1.0", "end-1c")
    reference = referenceText.get("1.0", "end-1c")

    if typed == reference:
        end_time = time.time()
        elapsed = end_time - start_typing
        wpm = round(len(typed.split()) / (elapsed / 60))

        resultLabel.configure(text=f"Done! WPM: {wpm}", font=["Arial black", 20])
        test_in_progress = False



# The window setup
root = Tk()
root.title("Typing Speed Application")
w, h = (640, 480)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_position_x = int(((screen_width/2)-(w/2)))
window_position_y = int(((screen_height/2)-(h/2)))
root.geometry(f"{w}x{h}+{window_position_x}+{window_position_y}")


# UI setup

mainFrame = Frame(master=root)
mainFrame.configure()
mainFrame.pack(padx=10, pady=10, fill="both", expand=True)

# Frame for the reference text and the text input
textFame = Frame(master=mainFrame)

Label(master=textFame, text="Reference Text: ", font=["Courier", 15]).pack(pady=2)
referenceText = Text(master=textFame, height=6)
referenceText.configure(state="disabled")
referenceText.pack(padx=2, pady=2, fill="both", expand=True)

Label(master=textFame, text="Type here: ", font=["Courier", 15]).pack(pady=2)
userText = Text(master=textFame, height=8)
userText.configure(font=["Courier", 15])
userText.pack(padx=2, pady=2, fill="both", expand=True)

textFame.pack(padx=5, pady=5, fill="both", expand=True)

# Frame for the button(s)
buttonFrame = Frame(master=mainFrame)

startButton = Button(master=buttonFrame, height=2, foreground="blue")
startButton.configure(text="Start", command=start_test)
startButton.pack(padx=2, pady=2, side="left")

resetButton = Button(master=buttonFrame, height=2, foreground="blue")
resetButton.configure(text="Reset", command=reset)
resetButton.pack(padx=2, pady=2, side="left")

buttonFrame.pack(padx=5, pady=5)

# Frame for the actual result

resultFrame = Frame(master=mainFrame)

Label(master=resultFrame, text="Your typing speed result: ", font=["Courier", 15]).pack(pady=2)
resultLabel = Label(master=resultFrame)
resultLabel.pack(padx=2, pady=2, fill="both", expand=True)

resultFrame.pack(padx=5, pady=5, fill="both", expand=True)


# Bindings
userText.bind("<KeyRelease>", on_typing)
referenceText.bind("<Control-s>", lambda e: "break")




# Start the application
if __name__ == "__main__":
    root.mainloop()
