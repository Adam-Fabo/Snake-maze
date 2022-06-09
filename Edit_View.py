#!/usr/bin/python
#
# Project: GUI application (for subject ITU on BUT)
# Brief: Code for the view part of the Editor app (MVC)
# Author: Stanislav Gabriš (xgabri18)

import tkinter as tk
import os
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename


class EView:
    def __init__(self, app):
        self.return_or_quit = 0  # 0-quit 1-return
        self.back = 0  # 1 means this window was destroyed
        self.myself = app
        self.editflag = 0  # if 1 there are unsaved changes
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.tutorial = tk.Message()
        #self.tutorial.destroy()
        self.C = 0  # clear flag
        self.Im = 0  # import flag
        self.w = 1280
        self.h = 720
        self.ws = app.winfo_screenwidth()  # width of the screen
        self.hs = app.winfo_screenheight()  # height of the screen
        self.x = (self.ws / 2) - (self.w / 2)
        self.y = (self.hs / 2) - (self.h / 2)
        self.save_text = tk.StringVar()

        app.iconbitmap(app, 'images/icona.ico')
        app.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        app.title("SnakeMaze-Editor")
        app.resizable(width=False, height=False)

        load = Image.open("./Images/SnakeMazeLogo.png")
        load = load.resize((170, 100))
        render = ImageTk.PhotoImage(load)
        self.img = tk.Label(app, image=render, bg="light cyan")
        self.img.image = render
        self.img.place(x=1000, y=5)

        self.canvas = tk.Canvas(app, bg="white", width=1000, height=720)
        self.canvas.place(x=0, y=0)

        self.expl = tk.Message(app, text="Editing options", width=250, bg="light cyan", font="Sagoe 12 bold")
        self.expl.place(x=1075, y=10 + 50 + 120)
        app.configure(bg="light cyan")

        self.space = 20
        self.clear_and_repaint()

        # --images for buttons--
        self.saveim = tk.PhotoImage(file=self.path + "/images/save.gif")
        self.importim = tk.PhotoImage(file=self.path + "/images/import.gif")
        self.clearim = tk.PhotoImage(file=self.path + "/images/clear.gif")
        self.btmim = tk.PhotoImage(file=self.path + "/images/btm.gif")
        self.quitim = tk.PhotoImage(file=self.path + "/images/quit.gif")

        # --text for buttons--
        # text = "SAVE"
        # text = "Clear"
        # text = "Import"
        # text = "Back to Menu"
        # text = "Quit"

        self.save = tk.Button(app, image=self.saveim, width=90, pady=10, command=self.clr, bd=0, bg="light cyan")
        self.save.place(x=1180, y=10)

        self.clear = tk.Button(app, image=self.clearim, width=90, command=self.clr, bd=0, bg="light cyan")
        self.clear.place(x=1008, y=10 + 50 + 50)

        self.importbtn = tk.Button(app, image=self.importim, width=90, command=self.clr, bd=0, bg="light cyan")
        self.importbtn.place(x=1180, y=10 + 50)

        self.btm = tk.Button(app, image=self.btmim, width=90, command=self.backing, bd=0, bg="light cyan")
        self.btm.place(x=1050, y=10 + 670)

        self.quit = tk.Button(app, image=self.quitim, width=90, command=self.quiting, bd=0, bg="light cyan")
        self.quit.place(x=1150, y=10 + 670)

        # --images for radiobuttons--
        self.start1im = tk.PhotoImage(file=self.path + "/images/P1_start.gif")
        self.start1im_select = tk.PhotoImage(file=self.path + "/images/select_P1_start.gif")
        self.start2im = tk.PhotoImage(file=self.path + "/images/P2_start.gif")
        self.start2im_select = tk.PhotoImage(file=self.path + "/images/select_P2_start.gif")
        self.start1im = tk.PhotoImage(file=self.path + "/images/P1_start.gif")
        self.start1im_select = tk.PhotoImage(file=self.path + "/images/select_P1_start.gif")
        self.point1im = tk.PhotoImage(file=self.path + "/images/P1_point.gif")
        self.point1im_select = tk.PhotoImage(file=self.path + "/images/select_P1_point.gif")
        self.point2im = tk.PhotoImage(file=self.path + "/images/P2_point.gif")
        self.point2im_select = tk.PhotoImage(file=self.path + "/images/select_P2_point.gif")
        self.end1im = tk.PhotoImage(file=self.path + "/images/P1_end.gif")
        self.end1im_select = tk.PhotoImage(file=self.path + "/images/select_P1_end.gif")
        self.end2im = tk.PhotoImage(file=self.path + "/images/P2_end.gif")
        self.end2im_select = tk.PhotoImage(file=self.path + "/images/select_P2_end.gif")
        self.obstim = tk.PhotoImage(file=self.path + "/images/Obst.gif")
        self.obstim_select = tk.PhotoImage(file=self.path + "/images/select_Obst.gif")
        self.obst2im = tk.PhotoImage(file=self.path + "/images/Obst2.gif")
        self.obst2im_select = tk.PhotoImage(file=self.path + "/images/select_Obst2.gif")

        # --texts for radiobuttons--          --mode--
        # text = "P1 starting position" -1
        # text = "P2 starting position" -2
        # text = "P1 point"             -3
        # text = "P2 point"             -7
        # text = "P1 endpoint"          -5
        # text = "P2 endpoint"          -8
        # text = "Place obstacle"       -4
        # text = "Place obstacle^2"     -6

        self.v = tk.IntVar()
        self.v2 = 0  # kontroluje stlacenie

        self.mode1 = tk.Radiobutton(app, image=self.start1im, variable=self.v, value=1, indicatoron=0,
                                    command=self.start_posp1, width=125, bd=0, bg="light cyan",
                                    selectimage=self.start1im_select, selectcolor='light cyan')
        self.mode1.place(x=1005, y=10 + 50 + 150)

        self.mode2 = tk.Radiobutton(app, image=self.start2im, variable=self.v, value=2, indicatoron=0,
                                    command=self.start_posp2, width=125, bd=0, bg="light cyan",
                                    selectimage=self.start2im_select, selectcolor='light cyan')
        self.mode2.place(x=1145, y=10 + 50 + 150)

        self.mode3 = tk.Radiobutton(app, image=self.point1im, variable=self.v, value=3, indicatoron=0,
                                    command=self.point, width=125, bd=0, bg="light cyan",
                                    selectimage=self.point1im_select, selectcolor='light cyan')
        self.mode3.place(x=1005, y=10 + 50 + 190)

        self.mode4 = tk.Radiobutton(app, image=self.obstim, variable=self.v, value=4, indicatoron=0,
                                    command=self.obstacle, width=125, bd=0, bg="light cyan",
                                    selectimage=self.obstim_select, selectcolor='light cyan')
        self.mode4.place(x=1005, y=10 + 50 + 300)

        self.mode5 = tk.Radiobutton(app, image=self.end1im, variable=self.v, value=5, indicatoron=0,
                                    command=self.victory, width=125, bd=0, bg="light cyan",
                                    selectimage=self.end1im_select, selectcolor='light cyan')
        self.mode5.place(x=1005, y=10 + 50 + 230)

        self.mode6 = tk.Radiobutton(app, image=self.obst2im, variable=self.v, value=6, indicatoron=0,
                                    command=self.obstacle2, width=125, bd=0, bg="light cyan",
                                    selectimage=self.obst2im_select, selectcolor='light cyan')
        self.mode6.place(x=1145, y=10 + 50 + 300)

        self.mode7 = tk.Radiobutton(app, image=self.point2im, variable=self.v, value=7, indicatoron=0,
                                    command=self.point2, width=125, bd=0, bg="light cyan",
                                    selectimage=self.point2im_select, selectcolor='light cyan')
        self.mode7.place(x=1145, y=10 + 50 + 190)

        self.mode8 = tk.Radiobutton(app, image=self.end2im, variable=self.v, value=8, indicatoron=0,
                                    command=self.victory2, width=125, bd=0, bg="light cyan",
                                    selectimage=self.end2im_select, selectcolor='light cyan')
        self.mode8.place(x=1145, y=10 + 50 + 230)

        ####################################################################################

    def clr(self):
        tmp = self.v2
        if tmp == 1:
            self.start_posp1()
        elif tmp == 2:
            self.start_posp2()
        elif tmp == 3:
            self.point()
        elif tmp == 4:
            self.obstacle()
        elif tmp == 5:
            self.victory()
        elif tmp == 6:
            self.obstacle2()
        elif tmp == 7:
            self.point2()
        elif tmp == 8:
            self.victory2()


    def start_posp1(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode1.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode1.select()
        self.tutorial_w(self.v2, "show")

    def start_posp2(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode2.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode2.select()
        self.tutorial_w(self.v2, "show")

    def point(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode3.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode3.select()
        self.tutorial_w(self.v2, "show")

    def obstacle(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode4.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode4.select()
        self.tutorial_w(self.v2, "show")

    def victory(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode5.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode5.select()
        self.tutorial_w(self.v2, "show")

    def obstacle2(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode6.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode6.select()
        self.tutorial_w(self.v2, "show")

    def point2(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode7.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode7.select()
        self.tutorial_w(self.v2, "show")

    def victory2(self):
        if self.v2 != 0:
            self.tutorial_w(0, "rem")
        if self.v2 == self.v.get():
            self.mode8.deselect()
            self.v2 = 0
            return
        self.v2 = self.v.get()
        self.mode8.select()
        self.tutorial_w(self.v2, "show")

    def backing(self):
        self.clr()
        if self.editflag == 1:
            self.unsaved_window()
            if self.return_or_quit == 1:
                return
        self.back = 1
        self.myself.destroy()

    def quiting(self):
        self.clr()
        if self.editflag == 1:
            self.unsaved_window()
            if self.return_or_quit == 1:
                return
        self.back = 0
        self.myself.destroy()


    ########################################################################################

    def draw_borders(self):
        self.canvas.create_rectangle(0, 0, 1000, self.space, fill='black')
        self.canvas.create_rectangle(0, 0, self.space, 720, fill='black')
        self.canvas.create_rectangle(0, 720 - self.space, 1000, 720, fill='black')
        self.canvas.create_rectangle(1000 - self.space, 0, 1000, 720 - self.space, fill='black')

    def paint_wall(self, x, y):
        self.canvas.create_rectangle(x, y, x+20, y+20, fill='black')

    def paint_blank(self, x, y):
        self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='white')

    def paint_point(self, x, y, color):
        self.canvas.create_oval(x, y, x + 20, y + 20, fill=color)

    def paint_endpoint(self, x, y, color):
        self.canvas.create_rectangle(x+3, y+3, x + 17, y + 17, fill=color)

    def paint_p1(self, x, y):
        self.canvas.create_oval(x+5, y+5, x + 15, y + 15, width=5, outline='green')

    def paint_p2(self, x, y):
        self.canvas.create_oval(x+5, y+5, x + 15, y + 15, width=5, outline='red')

    def paint_from_imported(self, memory):
        for i in range(len(memory)):
            if i % 3 == 0:
                if memory[i+2] == 4:
                    self.paint_wall(memory[i], memory[i+1])
                elif memory[i+2] == 1:
                    self.paint_p1(memory[i], memory[i+1])
                elif memory[i+2] == 2:
                    self.paint_p2(memory[i], memory[i+1])
                elif memory[i+2] == 3:
                    self.paint_point(memory[i], memory[i+1], 'yellow')
                elif memory[i + 2] == 5:
                    self.paint_endpoint(memory[i], memory[i + 1], 'green')
                elif memory[i+2] == 7:
                    self.paint_point(memory[i], memory[i+1], 'orange')
                elif memory[i + 2] == 8:
                    self.paint_endpoint(memory[i], memory[i + 1], 'red')

    ##################################################################################

    def import_window(self, path):
        filename = askopenfilename(initialdir=path, title="Select a map")
        return filename

    def error_window(self, errmsg):
        w = 300
        h = 125
        err = tk.Toplevel(height=h, width=w)
        err.iconbitmap(err, 'images/icona.ico')
        err.title("Error")
        err.resizable(width=False, height=False)
        x = (self.ws / 2) - (w / 2)
        y = (self.hs / 2) - (h / 2)
        err.geometry('%dx%d+%d+%d' % (w, h, x, y))

        text = tk.Message(err, text=errmsg, width=250, font=("Helvetica", "16", "bold"))
        text.pack(pady=15)

        button = tk.Button(err, text="Dismiss", command=err.destroy, width=15)
        button.place(x=90, y=90)

    def tutorial_w(self, mode, state):
        txt = ""
        if mode == 1:
            txt = "Place/Remove the starting point of Player1 (only one can exist)"
        elif mode == 2:
            txt = "Place/Remove the starting point of Player2 (only one can exist)"
        elif mode == 3:
            txt = "Place/Remove points for Player1 to collect"
        elif mode == 4:
            txt = "Place/Remove obstacles players won't be able to pass(one at a time)"
        elif mode == 5:
            txt = "Place/Remove the \"victory\" point of Player1 (only one can exist)"
        elif mode == 6:
            txt = "Place/Remove obstacles players won't be able to pass in a rectangular shape\n(choose the top-left " \
                  "point with first click on mouse and the bottom-right with the next one)"
        elif mode == 7:
            txt = "Place/Remove points for Player2 to collect"
        elif mode == 8:
            txt = "Place/Remove the \"victory\" point of Player2 (only one can exist)"

        if state == "show":
            self.tutorial = tk.Message(self.myself, text="Hint:\n"+txt, font="Courier", width=250, background="gold")
            self.tutorial.place(x=1010, y=10 + 50 + 300 + 100)
        else:
            self.tutorial.configure(text="")
            self.tutorial.destroy()



    def save_window(self):
        w = 300
        h = 125
        sv = tk.Toplevel(height=h, width=w)
        sv.iconbitmap(sv, 'images/icona.ico')
        sv.title("Save")
        sv.resizable(width=False, height=False)
        x = (self.ws / 2) - (w / 2)
        y = (self.hs / 2) - (h / 2)
        sv.geometry('%dx%d+%d+%d' % (w, h, x, y))

        text = tk.Message(sv, text="Enter filename:", width=250)
        text.pack()

        entr = tk.Entry(sv)
        entr.pack()
        self.save_text.set("Save")
        button = tk.Button(sv, textvariable=self.save_text, width=15)
        button.place(x=90, y=90)
        return sv, entr, text, button

    def clear_and_repaint(self):
        self.canvas.delete("all")
        for i in range(51):
            self.canvas.create_line(i * self.space, 0, i * self.space, 720)

            # aby zbytocne nevykresloval grid mimo okna
            if i < 36:
                self.canvas.create_line(0, i * self.space, 1000, i * self.space)
        self.draw_borders()


    def unsaved_window(self):
        self.return_or_quit = 1
        w = 300
        h = 125
        pop = tk.Toplevel(height=h, width=w)
        pop.iconbitmap(pop, 'images/icona.ico')
        pop.title("Beware")
        pop.resizable(width=False, height=False)
        x = (self.ws / 2) - (w / 2)
        y = (self.hs / 2) - (h / 2)
        pop.geometry('%dx%d+%d+%d' % (w, h, x, y))

        text = tk.Message(pop, text="Unsaved changes!", width=250, font=("Helvetica", "16", "bold"))
        text.pack(pady=15)

        button1 = tk.Button(pop, text="Quit/Menu", command=lambda: self.quit_press(pop), width=10)
        button1.place(x=50, y=90)

        button2 = tk.Button(pop, text="Return", command=lambda: self.return_press(pop), width=10)
        button2.place(x=170, y=90)
        self.myself.wait_window(pop)

    def quit_press(self, top):
        self.return_or_quit = 0
        top.destroy()

    def return_press(self, top):
        self.return_or_quit = 1
        top.destroy()




