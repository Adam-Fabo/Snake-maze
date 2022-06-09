#!/usr/bin/python

# This is student project at VUT university at Brno
# Made by Adam Fabo (xfaboa00)
# Licence: none - you are free to shace this code as you please


import tkinter as tk


class View():
    def __init__(self,app):

        self.app = app
        self.w = 1000
        self.h = 720
        self.canvas = tk.Canvas(app, bg="white", width=self.w, height=self.h)
        self.canvas.place(x=0, y=0)
        self.back = 0

        self.space = 20

        #vykreslenie gridu
        for i in range(51):
            self.canvas.create_line(i * self.space, 0, (i) * (self.space), self.h)

            #aby zbytocne nevykresloval grid mimo okna
            if i< 36:
                self.canvas.create_line(0, i * self.space,self.w, (i) * (self.space))
        self.draw_borders()


    def draw_borders(self):
        self.canvas.create_rectangle(0, 0, self.w, self.space, fill='black')
        self.canvas.create_rectangle(0, 0, self.space, self.h, fill='black')
        self.canvas.create_rectangle(0, self.h - self.space, self.w, self.h, fill='black')
        self.canvas.create_rectangle(self.w - self.space, 0, self.w, self.h - self.space, fill='black')


    def draw_pos(self,cursor,col):
        self.canvas.create_rectangle ( cursor[0] * self.space,         cursor[1] * self.space,
                                     ( cursor[0] + 1) * (self.space), (cursor[1] + 1) * (self.space),
                                       fill=col)

    def draw_rec(self,cursor,canvas,col,space):
        canvas.create_rectangle ( cursor[0] * space,         cursor[1] * space,
                                     ( cursor[0] + 1) * (space), (cursor[1] + 1) * (space),
                                       fill=col)
    def draw_rec2(self,cursor,canvas,col,space,offset1,offset2):
        canvas.create_rectangle ( cursor[0] * space+offset1,         cursor[1] * space+offset1,
                                     ( cursor[0] + 1) * (space) -offset2, (cursor[1] + 1) * (space) - offset2,
                                       fill=col)

    def draw_elip(self,cursor,col):
        self.canvas.create_oval ( cursor[0] * self.space,         cursor[1] * self.space,
                                     ( cursor[0] + 1) * (self.space), (cursor[1] + 1) * (self.space),
                                       fill=col)

    def create_text(self,x,y,text,col):
        tmp = tk.Label(self.app,textvariable = text, fg = '{}'.format(col))
        tmp.config(font=("Courier", 10),bg="light cyan")
        tmp.place(x = x,y = y)

        return tmp
    def create_entry(self,x,y):
        tmp = tk.Entry(self.app)
        tmp.place(x = x,y = y)

        return tmp

    def create_button(self,x,y,text,cmd):
        tmp = tk.Button(self.app,text = text,command = cmd, bg="pale green",activebackground = "green")
        tmp.place(x = x,y = y)

        return tmp
