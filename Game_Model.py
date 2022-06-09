#!/usr/bin/python

# This is student project at VUT university at Brno
# Made by Adam Fabo (xfaboa00)
# Licence: none - you are free to shace this code as you please

import tkinter as tk
from Game_View import *
import Game_backend
from os import listdir
from os.path import isfile, join

class Model:
    def __init__(self,view):

        self.view = view
        self.cursor1 = [0,0]
        self.cursor2 = [0,0]
        self.starting_pos1 = [0, 0]
        self.starting_pos2 = [0, 0]
        self.w = 48
        self.h = 34
        self.curren_map_name = ""




        f = open("Settings/Settings.txt")
        self.name1 = tk.StringVar()
        self.name2 = tk.StringVar()

        line = f.readline()
        self.name1.set('{}'.format(line).strip())

        line = f.readline()
        self.col1 = str(line).strip()

        line = f.readline()
        self.name2.set('{}'.format(line).strip())

        line = f.readline()
        self.col2 = str(line).strip()

        f.close()

    def draw_maze(self,view):

        for i in range(self.h):
            for j in range(self.w):
                if(self.mapa[i][j] == 1):
                    view.draw_pos([j+1,i+1],'black')
                if (self.mapa[i][j] == 0):
                    view.draw_pos([j + 1, i + 1], 'white')
                if (self.mapa[i][j] == 4):
                    view.draw_pos([j + 1, i + 1], 'white')
                    view.draw_rec2([j + 1, i + 1],view.canvas,'red',20,3,3)
                if (self.mapa[i][j] == 5):
                    view.draw_pos([j + 1, i + 1], 'white')
                    view.draw_rec2([j + 1, i + 1], view.canvas, 'yellow', 20, 3, 3)
                if (self.mapa[i][j] == 7):
                    view.draw_pos([j + 1, i + 1], 'white')
                    view.draw_elip([j + 1, i + 1], 'yellow')
                if (self.mapa[i][j] == 6):
                    view.draw_pos([j + 1, i + 1], 'white')
                    view.draw_elip([j + 1, i + 1], 'orange')


    def add_cur_to_map(self,n):

        if(n == 1):
            self.mapa[self.cursor1[1]-1][self.cursor1[0]-1] = 8
        if (n == 2):
            self.mapa[self.cursor2[1]-1][self.cursor2[0]-1] = 9

    def change_cursor(self,x,y,n):
        if(n == 1):
            self.cursor1 = [x,y]
        elif (n == 2):
            self.cursor1 = [x, y]

    def get_cursor(self,n):

        if (n == 1):
            return self.cursor1
        elif (n == 2):
            return self.cursor2

    def get_name(self,n):

        if (n == 1):
            return self.name2
        elif (n == 2):
            return self.name1

    def add_to_cursor(self, x, y,n):

        #osetrit podmienku ci to neni mimo hranic
        if (n == 1):
            if (Game_backend.check_validity_of_cursor( [self.cursor1[0] + x, self.cursor1[1] +y],self.mapa )):
                self.cursor1[0] = self.cursor1[0] + x
                self.cursor1[1] = self.cursor1[1] + y
            else:
                #print("cursor 1 narazil")
                self.reset_player(1)
                return False
        elif (n == 2):
            if (Game_backend.check_validity_of_cursor([self.cursor2[0] + x, self.cursor2[1] + y],self.mapa)):
                self.cursor2[0] = self.cursor2[0] + x
                self.cursor2[1] = self.cursor2[1] + y
            else:
               # print("cursor 2 narazil")
                self.reset_player(2)
                return False


        return True

    def reset_player(self,id):
        #print(self.cursor1, self.cursor2)
        #print(self.starting_pos1, self.starting_pos2)

        if(id ==1):
            self.cursor1[0] = self.starting_pos1[0]
            self.cursor1[1] = self.starting_pos1[1]

            for i in range(self.h):
                for j in range(self.w):
                    if (self.mapa[i][j] == 8):
                        self.mapa[i][j] = self.map_zaloha[i][j]
                        if (self.mapa[i][j] == 0):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                        if (self.mapa[i][j] == 4):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_rec2([j + 1, i + 1], self.view.canvas, 'red', 20, 3, 3)
                        if (self.mapa[i][j] == 7):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_elip([j + 1, i + 1], 'yellow')
                        if (self.mapa[i][j] == 6):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_elip([j + 1, i + 1], 'orange')

            self.view.draw_pos(self.get_cursor(1), self.col2)
        elif (id == 2):
            self.cursor2[0] = self.starting_pos2[0]
            self.cursor2[1] = self.starting_pos2[1]

            for i in range(self.h):
                for j in range(self.w):
                    if (self.mapa[i][j] == 9):
                        self.mapa[i][j] = self.map_zaloha[i][j]
                        if (self.mapa[i][j] == 0):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                        if (self.mapa[i][j] == 5):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_rec2([j + 1, i + 1], self.view.canvas, 'yellow', 20, 3, 3)
                        if (self.mapa[i][j] == 7):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_elip([j + 1, i + 1], 'yellow')
                        if (self.mapa[i][j] == 6):
                            self.view.draw_pos([j + 1, i + 1], 'white')
                            self.view.draw_elip([j + 1, i + 1], 'orange')

            self.view.draw_pos(self.get_cursor(2), self.col1)



    def map_contains(self,num):
        for i in range(self.h):
            for j in range(self.w):
                if(self.mapa[i][j] == num):
                    return True

        return False

    def seek_files(self):
        onlyfiles = [f for f in listdir('Maps') if isfile(join('Maps', f))]
        map_names = []                     #nacitanie listu map

        for file in onlyfiles:
            with open(join('Maps', file), 'r') as f:
                first_line = f.readline()
                if (first_line.rstrip() == "ffff"):
                    map_names.append(file)

        return map_names


    def load_map(self,name):
        with open(name) as f:
            #self.w, self.h = [int(x) for x in next(f).split()]
            self.fheader = next(f)
            #self.cursor1[0], self.cursor1[1],self.cursor2[0],self.cursor2[1] = [int(x) for x in next(f).split()]
            self.mapa = []
            for i in range(self.h):
                line = next(f)
                self.mapa.append([int(x) for x in line.split()])
           # self.mapa = [[int(x) for x in line.split()] for line in f]

            self.highscore = []


            for i in range(self.w):
                for j in range(self.h):
                    if(self.mapa[j][i] == 3):
                        self.cursor2[0] = i+1
                        self.cursor2[1] = j+1

                        self.starting_pos2[0] = int(self.cursor2[0])
                        self.starting_pos2[1] = int(self.cursor2[1])

                    if(self.mapa[j][i] == 2):
                        self.cursor1[0] = i+1
                        self.cursor1[1] = j+1
                        self.starting_pos1[0] = int(self.cursor1[0])
                        self.starting_pos1[1] = int(self.cursor1[1])

            for line in f:
                self.highscore.append(line.strip())
            #print(self.highscore)
        self.map_zaloha = list(map(list,self.mapa))
        f.close()