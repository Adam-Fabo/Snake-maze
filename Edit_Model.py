#!/usr/bin/python
#
# Project: GUI application (for subject ITU on BUT)
# Brief: Code for the model part of the Editor app (MVC)
# Author: Stanislav Gabriš (xgabri18)

import os


class EModel:
    def __init__(self, app):
        self.memory = []
        self.flag = 0  # if flag set mouse didnt click on canvas
        self.mousex = 0  # x of topleft corner in rectangle
        self.mousey = 0  # y of topleft corner in rectangle
        self.prev_mousex = 0
        self.prev_mousey = 0
        self.obst2_count = 0  # if 1 - one click in mode 6 , if 2 - two clicks
        self.erasing_obst2 = 0  # are we erasing in mode 6?

        self.path = os.path.dirname(os.path.abspath(__file__))  # directory where the running .py file is
        self.filepath = os.path.dirname(os.path.abspath(__file__))  # will hold the info about the file with map
        self.filename = "\\init.txt"



    def cursor_pos(self, event):
        self.flag = 0
        self.prev_mousex = self.mousex
        self.prev_mousey = self.mousey
        self.mousex = 0
        self.mousey = 0
        const = 20
        zx = 20  # maze parameters: width 960 (window 1000),height 680 (window 720)
        zy = 20  # 20,20 is 0,0 in maze
        kx = 40
        ky = 40
        for i in range(48):
            if zx + const*i <= event.x < kx + const*i:
                self.mousex = zx+const*i
                break
        for i in range(34):
            if zy + const*i <= event.y < ky + const*i:
                self.mousey = zy+const*i
                break
        if self.mousex == 0 or self.mousey == 0:
            self.obst2_count = 0
            self.flag = 1  # flag set dont change anything

    def txt_to_memory(self):
        tmpmem = []
        with open(self.filepath, 'r') as filehandle:  # with statement closes the file on its own (close() not needed)
            text = list(filehandle)
            text = [line.replace(' ', '') for line in text]  # replace space with nothing

            if text[0] != "ffff\n":
                tmpmem.append(42)
                self.memory = tmpmem
                return

            for y in range(1, 35):
                for x in range(1, 49):
                    if text[y][x-1] == '0':  # nothing
                        continue
                    elif text[y][x-1] == '1':  # wall
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(4)
                    elif text[y][x-1] == '2':  # Starting point2
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(2)
                    elif text[y][x-1] == '3':  # Starting point1
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(1)
                    elif text[y][x-1] == '4':  # Endpoint2
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(8)
                    elif text[y][x-1] == '5':  # Endpoint1
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(5)
                    elif text[y][x-1] == '6':  # Point2
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(7)
                    elif text[y][x-1] == '7':  # Point1
                        tmpmem.append(x*20)
                        tmpmem.append(y*20)
                        tmpmem.append(3)
        self.memory = tmpmem

    def memory_to_list(self, memory):
        tolist = ["ffff\n"]
        added = 0

        for y in range(1, 35):
            listy = y * 20
            tolist.append('')
            for x in range(1, 49):
                listx = x * 20
                for i in range(len(memory)):
                    if i % 3 == 0:
                        if memory[i] == listx and memory[i+1] == listy:
                            if memory[i+2] == 1:
                                tolist[y] = tolist[y] + "3 "
                                added = 1
                                break
                            elif memory[i+2] == 2:
                                tolist[y] = tolist[y] + "2 "
                                added = 1
                                break
                            elif memory[i+2] == 5:
                                tolist[y] = tolist[y] + "5 "
                                added = 1
                                break
                            elif memory[i+2] == 8:
                                tolist[y] = tolist[y] + "4 "
                                added = 1
                                break
                            elif memory[i+2] == 4:
                                tolist[y] = tolist[y] + "1 "
                                added = 1
                                break
                            elif memory[i+2] == 7:
                                tolist[y] = tolist[y] + "6 "
                                added = 1
                                break
                            elif memory[i + 2] == 3:
                                tolist[y] = tolist[y] + "7 "
                                added = 1
                                break

                if added == 0:
                    tolist[y] = tolist[y] + "0 "
                added = 0

            tolist[y] = tolist[y] + "\n"
        return tolist




    def data_correctness(self):
        memory = self.memory
        end1 = 0    # 5
        end2 = 0    # 8
        start1 = 0  # 1
        start2 = 0  # 2

        for j in range(len(memory)):
            if j % 3 == 0:
                if memory[j+2] == 1:
                    start1 = 1
                elif memory[j+2] == 2:
                    start2 = 1
                elif memory[j+2] == 5:
                    end1 = 1
                elif memory[j+2] == 8:
                    end2 = 1

        if start1 == 1 and start2 == 1 and end1 == 1 and end2 == 1:
            return 1

        return 0

    def name_check(self):
        if "." in self.filename or '\\' in self.filename:
            return 0
        return 1

    def path_check(self):
        if not os.path.isdir(self.path + '/maps'):
            try:
                os.mkdir(self.path + '/maps')
            except OSError:
                print("Creation of the directory failed")
                return 0
        if os.path.isfile(self.path + '/maps/' + self.filename):
            return 0
        return 1


    def store_map(self,exists):
        memory = self.memory
        tolist = self.memory_to_list(memory)
        if exists == 0:
            try:
                os.remove(self.path + '/maps/' + self.filename)
            except OSError:
                print("Deleting of file failed")
                return 0

        with open(self.path + '/maps/' + self.filename, 'w') as filehandle:
            for item in tolist:
                filehandle.write("%s" % item)


    def store(self, x, y, mode):
        self.memory.append(x)  # array [x,y,mode,x,y,mode,...] where (x,y,mode) is an element
        self.memory.append(y)
        self.memory.append(mode)

    def rm_element(self, element):  # removes element from array
        for i in range(3):
            self.memory.pop(element)
