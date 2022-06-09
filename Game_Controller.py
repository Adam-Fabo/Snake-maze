#!/usr/bin/python

# This is student project at VUT university at Brno
# Made by Adam Fabo (xfaboa00)
# Licence: none - you are free to shace this code as you please

import colors
from Game_Model import *
from os import listdir
from os.path import isfile, join
from PIL import ImageTk, Image
import Game_backend



class Controller:
    # konstruktor - zakladna inicializacia
    def __init__(self,app):

        self.app = app
        app.iconbitmap('images/icona.ico')
        app.title("Maze Game")

        app.geometry("1280x720")

        app.resizable(width=False, height=False)
        app.configure(bg="light cyan")
        self.history = []

        self.view = View(app)
        self.model = Model(self.view)


        tmp1 = tk.StringVar()
        tmp1.set("Player 1 name:")

        #vytvaranie prvkov

        self.P1 =  self.view.create_text(1010, 180, tmp1,'black')
        self.P1N = self.view.create_text(1140, 180, self.model.name1,self.model.col1)
        self.B1 =  self.view.create_button(1010, 200, "Change P1 name", lambda : self.change_name_win(self.model.name1,1))
        self.B11 = self.view.create_button(1150, 200, "Change P1 color", lambda : self.change_color_win(1))

        tmp2 = tk.StringVar()
        tmp2.set("Player 2 name:")
        self.P2 =  self.view.create_text(1010, 250, tmp2,'black')
        self.P2N = self.view.create_text(1140, 250, self.model.name2,self.model.col2)
        self.B2 =  self.view.create_button(1010, 270, "Change P2 name", lambda : self.change_name_win(self.model.name2,2) )
        self.B22 = self.view.create_button(1150, 270, "Change P2 color", lambda: self.change_color_win(2))

        #self.R1 = self.view.create_button(1100, 380, "RESET", self.reset)

        self.R2 = self.view.create_button(1150, 670, "QUIT", self.quit)
        self.R2.configure(width = 7, height = 2)

        self.CR1 = self.view.create_button(1045, 630, "Credits",   self.credits_win)
        self.HS1 = self.view.create_button(1100, 630, "Highscore", self.highscore_win)
        self.H2P = self.view.create_button(1170, 630, "How2play",  self.how2play)

        self.R3 = self.view.create_button(1050, 670, "Back to menu", self.b2menu)
        self.R3.configure( height=2)


        self.map_names = self.model.seek_files()                    #nacitanie listu map
        self.selected = tk.StringVar()

        self.selected.set("CHOOSE FILE")

        self.opt =  tk.OptionMenu(app,self.selected, *self.map_names)

        self.opt.configure(width=30,bg="pale green")
        self.opt["activebackground"] = "pale green"
        self.opt["bg"] = "pale green"
        self.opt["highlightthickness"] = 0

        self.opt["menu"]["bg"] = "pale green"
        self.opt["menu"]["activebackground"] = "green"
        self.opt["menu"]["borderwidth"] = 10


        #self.opt.config(selectcolor = "red")
        self.opt.place(x = 1020, y = 100)

        self.optB = self.view.create_button(1100, 140, "Load Map", self.map_load)

        img = Image.open("images/SnakeMazeLogo.png")
        #img = tk.PhotoImage(file="Snake_maze_logo.png")

        img = img.resize((250, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel  = tk.Label(self.app,image = img,bg="light cyan")
        panel.img = img
        #self.view.canvas.create_image(20, 20, image=img)
        panel.configure(width = 250, height = 100)
        panel.place( x = 1010, y = 0)


        app.bind("<KeyPress>", self.keydown)
        app.bind("<KeyRelease>", self.keyup)



    # spracovaie stlacenia na klavesnici
    def keyup(self,event):

        if event.keycode in self.history:
            self.history.pop(self.history.index(event.keycode))

    # spracovaie stlacenia na klavesnici
    def keydown(self,event):
        if not event.keycode in self.history:
            self.history.append(event.keycode)

            #if key pressed  = nejaka key urob nasledovne
            #call keyhandler
            self.key_handler(event.keycode)

    # spracovaie stlacenia na klavesnici
    def key_handler(self,keycode):

        allowed1 = False
        allowed2 = False

        if keycode == 40:       # Down arrow
            allowed1 = self.model.add_to_cursor(0,1,1)

        elif keycode == 39:     # Right arrow
            allowed1 = self.model.add_to_cursor(1,0,1)

        elif keycode == 38:     # Up arrow
            allowed1 = self.model.add_to_cursor(0,-1,1)

        elif keycode == 37:     # Left arrow
            allowed1 = self.model.add_to_cursor(-1,0,1)


        elif keycode == 87:     # Key W
            allowed2 = self.model.add_to_cursor(0, -1,2)

        elif keycode == 65:     # Key A
            allowed2 = self.model.add_to_cursor(-1,0,2)

        elif keycode == 83:     # Key S
            allowed2 = self.model.add_to_cursor(0, 1,2)

        elif keycode == 68:     # Key D
            allowed2 = self.model.add_to_cursor(1, 0,2)

        if allowed1:
            self.game_fun(1,self.model.col2)
        if allowed2:
            self.game_fun(2, self.model.col1)

    # Hlavna funkcia hry
    def game_fun(self, num, col):
        tmp_cur = self.model.get_cursor(num)
        self.view.draw_pos(tmp_cur, col)
        self.model.add_cur_to_map(num)

        if Game_backend.check_winning_condition(self.model.mapa,self.model.map_zaloha,num,tmp_cur) == True:
            self.winning_message(num)
            #print('Player {} won'.format(self.model.get_name(num)))



    def change_name_win(self,txt,index):             #vyskakovacie okno pri zmene mena

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()   # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('250x150+{}+{}'.format(int(ws/2),int(hs/2 - 200)))  #kam sa okno umiestni
        win.wm_title("Name settings")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')

        l = tk.Label(win, text="Set name")
        l.config(font=("Courier", 10),bg="light cyan")
        l.place(x = 50, y = 20)

        e = tk.Entry(win)
        e.place(x=50, y=40)
        e.focus_force()

        b = tk.Button(win, text="Save", command = lambda : self.pop_name_win (win,e,txt,index), bg="pale green",activebackground = "green")
        b.place(x = 50, y = 70)


    def pop_name_win(self,win,e,txt,index):         # pri kliku na Save sa ulozi meno a vymaze okno
        txt.set(e.get())                            # index hovori o tom ktoremu hracovi sa zmeni meno

        if(index == 1):
            self.change_line_in_file("Settings/Settings.txt",0,str(e.get()))
        else:
            self.change_line_in_file("Settings/Settings.txt", 2, str(e.get()))
        win.destroy()



    def change_color_win(self,col):                      #vyskakovacie okno pri zmene farby

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()   # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('750x580+{}+{}'.format(int(ws/2),int(hs/2 - 200)))     #kam sa okno umiestni
        win.wm_title("Color settings")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')

        l = tk.Label(win, text="Choose color by clicking on it")
        l.config(font=("Courier", 10),bg="light cyan")
        l.place(x = 250, y = 20)

        win.bind('<Button-1>', lambda event: self.pop_color_win (win,col))

        cnt = 0

        c = tk.Canvas(win,width = 1000,height = 1000)
        c.place(x= 0,y = 40)

        for i in range(0,25):                   #vykreslenie celej palety pomocou malych stvorcekov
            for j in range(0,18):
                self.view.draw_rec([i,j],c,colors.COLORS[cnt],30)
                cnt = cnt+1



    def pop_color_win(self, win,col):                       # vykona sa po kliku na farbu

        x = win.winfo_pointerx() - win.winfo_rootx()        #treba zistis poziciu kurzora v ramci okna
        y = win.winfo_pointery() - win.winfo_rooty()

        y = y - 40

        x = int(x/30)
        y = int(y/30)
        index = y + x*18                #vypocet indexu farby

        if(col == 1):
            self.model.col1 = colors.COLORS[index]
            self.change_line_in_file("Settings/Settings.txt",1,colors.COLORS[index])
            self.P1N.configure(fg = colors.COLORS[index])

            for i in range(self.model.h):
                for j in range(self.model.w):
                    if (self.model.mapa[i][j] == 3 or self.model.mapa[i][j] == 9 ):
                        self.view.draw_rec([j+1,i+1],self.view.canvas,self.model.col1,20)

        else:
            self.model.col2 = colors.COLORS[index]
            self.change_line_in_file("Settings/Settings.txt", 3, colors.COLORS[index])
            self.P2N.configure(fg=colors.COLORS[index])

            for i in range(self.model.h):
                for j in range(self.model.w):
                    if (self.model.mapa[i][j] == 2 or self.model.mapa[i][j] == 8):
                        self.view.draw_rec([j + 1, i + 1], self.view.canvas, self.model.col2, 20)

        win.destroy()


    def winning_message(self,num):                       #vyskakovacie okno pri vyhre

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()  # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('250x150+{}+{}'.format(int(ws/2),int(hs/2 - 200)))
        win.wm_title("WINNER")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')

        if(num == 1):
            name = str(self.model.name2.get())
            col = self.model.col2
        else:
            name = str(self.model.name1.get())
            col = self.model.col1

        l = tk.Label(win, text=name,fg = col)
        l.config(font=("Courier", 16),bg="light cyan")
        l.place(x=50, y=20)

        l2 = tk.Label(win, text="is Winner")
        l2.config(font=("Courier", 16),bg="light cyan")
        l2.place(x = 50, y = 40)


        b = tk.Button(win, text="NICE",command = lambda : self.pop_win(win), bg="pale green",activebackground = "green")
        b.place(x = 80, y = 80)

    def pop_win(self,win):
        self.reset()
        win.destroy()

    def credits_win(self):                       #vyskakovacie okno pri vyhre

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()  # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('320x100+{}+{}'.format(int(ws/2),int(hs/2 - 200)))
        win.wm_title("Credits")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')


        l = tk.Label(win, text="This game was made as student\n project at Brno university \nby Adam Fabo",fg = 'black',bg="light cyan")


        l.config(font=("Courier", 12))
        l.place(x=10, y=10)

    def how2play(self):                       #vyskakovacie okno pri vyhre

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()  # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('320x100+{}+{}'.format(int(ws/2),int(hs/2 - 200)))
        win.wm_title("How2play")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')


        l = tk.Label(win, text="Player1 - WASD\n  Player2 - arrows",fg = 'black',bg="light cyan")


        l.config(font=("Courier", 12))
        l.place(x=10, y=10)

    def highscore_win(self):                       #vyskakovacie okno pri vyhre

        win = tk.Toplevel()

        ws = win.winfo_screenwidth()  # width of the screen
        hs = win.winfo_screenheight()  # height of the screen

        win.geometry('250x150+{}+{}'.format(int(ws/2),int(hs/2 - 200)))
        win.wm_title("Highscore")
        win.iconbitmap('images/icona.ico')
        win.configure(bg="light cyan")
        win.focus_force()
        win.attributes('-topmost', 'true')

        i = 0
        for line in self.model.highscore:

            if(line != ""):
                l = tk.Label(win, text='{}.  '.format(i+1)+ line,fg = 'black',bg="light cyan")
                l.config(font=("Courier", 12))
                l.place(x=10, y=10 + i*20)
                i = i+1



    def change_line_in_file(self, fname, line, txt):  # zmeni konkretny riadok v kode

        f = open(fname, "r")

        data = f.readlines()

        f.close()

        data[line] = txt + "\n"

        f = open(fname, "w")
        f.writelines(data)

        f.close()

    def map_load(self):
        self.model.curren_map_name = "Maps/"+ self.selected.get()
        self.reset()


    def reset(self):
        self.model.load_map(self.model.curren_map_name)
        self.model.draw_maze(self.view)

        self.model.add_cur_to_map(1)
        self.model.add_cur_to_map(2)

        self.view.draw_pos(self.model.get_cursor(2), self.model.col1)
        self.view.draw_pos(self.model.get_cursor(1), self.model.col2)



    def b2menu(self):
        self.app.destroy()
        self.view.back = 1

    def quit(self):
        self.app.destroy()
        self.view.back = 0



