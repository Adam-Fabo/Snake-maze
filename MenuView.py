#!/usr/bin/python
#
# Project: GUI application (for subject ITU on BUT)
# Brief: Code for the view part of the main menu
# Author: Stanislav Gabriš (xgabri18)

import tkinter as tk
from PIL import ImageTk, Image


class MenuView:
    def __init__(self, app):
        self.w = 980
        self.h = 620
        self.ws = app.winfo_screenwidth()  # width of the screen
        self.hs = app.winfo_screenheight()  # height of the screen
        self.x = (self.ws / 2) - (self.w / 2)
        self.y = (self.hs / 2) - (self.h / 2)
        self.save_text = tk.StringVar()

        app.iconbitmap(app,'images/icona.ico')
        app.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        app.title("SnakeMaze")
        app.resizable(width=False, height=False)
        app.configure(bg="light cyan")

        load = Image.open("./Images/SnakeMazeLogo.png")
        load = load.resize((500, 350))
        render = ImageTk.PhotoImage(load)
        self.img = tk.Label(app, image=render, bg="light cyan")
        self.img.image = render
        self.img.pack()

        self.EButton = tk.Button(app, text="Editor", font=("Helvetica", "20", "bold"), width=15, height=3,
                                 bg="pale green")
        self.EButton.place(x=70, y=400)
        self.GButton = tk.Button(app, text="Game", font=("Helvetica", "20", "bold"), width=15, height=3,
                                 bg="pale green")
        self.GButton.place(x=650, y=400)

        self.info = tk.Button(app, text="i", font=("Helvetica", "20", "bold"), height=1, command=self.info, bg="gold")
        self.info.place(x=470, y=430)


    def info(self):
        new = tk.Toplevel()
        new.iconbitmap('images/icona.ico')
        new.title("Information")
        new.geometry('%dx%d+%d+%d' % (self.w-300, self.h-350, self.x+170, self.y+170))
        basicinfo = "Editor - edit or create your own maps, let your imagination flow. Use created maps to play.\n\n" \
                    "Game - play a game of snake on your own map versus your friend. "
        text = tk.Message(new, text=basicinfo, font=("Helvetica", "16", "bold"), width=500)
        text.pack(pady=60)
