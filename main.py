from tkinter import *
from tkinter import PhotoImage
import random
import pandas as pd

# Switch Card Function
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    word_to_learn = current_card[LANGUAGE_TO_LEARN]
    canvas.itemconfig(card_word,text=word_to_learn,fill="black")
    canvas.itemconfig(card_title,text=LANGUAGE_TO_LEARN,fill="black")
    canvas.itemconfig(card_side,image=card_front_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_title,text=TRANSLATED_LANGUAGE,fill="white")
    canvas.itemconfig(card_side,image=card_back_img)
    canvas.itemconfig(card_word,fill="white",text=current_card[TRANSLATED_LANGUAGE])

def remove_item():
    to_learn.remove(current_card)
    next_card()
    new_df = pd.DataFrame(to_learn)
    new_df.to_csv("./data/words_to_learn.csv",index=False)

# Constants
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_TO_LEARN = "Spanish"
TRANSLATED_LANGUAGE = "English"
current_card = {}
words_to_learn = []

# Open and read words file and create dictionary with each record a nested dictionary
try:
    df = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("./data/spanish_words.csv")
to_learn = df.to_dict(orient="records")

# UI
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR,padx=50,pady=50)
flip_timer = window.after(3000, flip_card)

# Create Canvas
canvas = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
# Images
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
# Add Canvas Objects
card_side = canvas.create_image(400,263,image=card_front_img)
card_title = canvas.create_text(400,150,text="",font=("Ariel",40,"italic"))
card_word = canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))
canvas.grid(column=0,row=0,columnspan=2)

# Create Buttons
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")
check_button = Button(image=right,highlightthickness=0,command=remove_item)
check_button.grid(column=1,row=1)
x_button = Button(image=wrong,highlightthickness=0,command=next_card)
x_button.grid(column=0,row=1)


next_card()

window.mainloop()
