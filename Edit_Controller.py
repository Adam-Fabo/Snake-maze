#!/usr/bin/python
#
# Project: GUI application (for subject ITU on BUT)
# Brief: Code for the controller part of the Editor app (MVC)
# Author: Stanislav Gabriš (xgabri18)

from Edit_View import *
from Edit_Model import *


class EController:
    def __init__(self, app):

        self.elremoved = 0  # if set dont paint / undo happened
        self.cmpf = 0  # value to compare with flag
        self.view = EView(app)
        self.model = EModel(app)

        self.view.canvas.bind("<Button-1>", self.lmb)
        self.view.clear.bind("<Button-1>", self.clearmem)
        self.view.importbtn.bind("<Button-1>", self.importing)
        self.view.save.bind("<Button-1>", self.saving)

    def lmb(self, event):
        if self.view.v2 == 6:
            self.model.obst2_count += 1

        if self.view.v2 == 0:  # when nothing is selected
            self.model.obst2_count = 0
            self.model.erasing_obst2 = 0

        self.elremoved = 0
        self.model.cursor_pos(event)
        if self.model.flag != 1 and self.view.v2 != 0:
            self.view.editflag = 1
            if self.model.obst2_count != 2:
                for i in range(len(self.model.memory)):  # check what is painted on the coordinates
                    if i % 3 == 0:  # 1 element comprises of 3 values
                        if self.model.mousex == self.model.memory[i] and self.model.mousey == self.model.memory[i + 1]:
                            self.check_mem(i, self.view.v2)
                            if self.elremoved == 1:
                                return
                            break

            if self.view.v2 == 1:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_p1(self.model.mousex, self.model.mousey)
                self.double_check(self.model.mousex, self.model.mousey, self.view.v2)
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 2:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_p2(self.model.mousex, self.model.mousey)
                self.double_check(self.model.mousex, self.model.mousey, self.view.v2)
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 3:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_point(self.model.mousex, self.model.mousey, 'yellow')
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 4:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_wall(self.model.mousex, self.model.mousey)
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 5:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_endpoint(self.model.mousex, self.model.mousey, 'green')
                self.double_check(self.model.mousex, self.model.mousey, self.view.v2)
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 6:
                if self.model.obst2_count == 1:  # first point
                    self.model.store(self.model.mousex, self.model.mousey, 4)  # 4 because its still just a wall
                    self.view.paint_wall(self.model.mousex, self.model.mousey)
                else:  # second point
                    self.handle_mode6(self.model.mousex, self.model.mousey, self.model.prev_mousex,
                                      self.model.prev_mousey)
                    self.model.obst2_count = 0
                    self.model.erasing_obst2 = 0

            elif self.view.v2 == 7:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_point(self.model.mousex, self.model.mousey, 'orange')
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0
            elif self.view.v2 == 8:
                self.model.store(self.model.mousex, self.model.mousey, self.view.v2)
                self.view.paint_endpoint(self.model.mousex, self.model.mousey, 'red')
                self.double_check(self.model.mousex, self.model.mousey, self.view.v2)
                self.model.obst2_count = 0
                self.model.erasing_obst2 = 0

        return

    def clearmem(self, event):
        self.view.editflag = 0
        if len(self.model.memory) == 0:
            return
        self.view.clear.configure(relief='sunken')
        self.model.memory = []
        self.view.clear_and_repaint()

        self.view.clear.configure(relief='raised')

    def importing(self, event):
        self.view.importbtn.configure(relief='sunken')
        self.model.filepath = self.view.import_window(self.model.path)
        self.view.importbtn.configure(relief='raised')
        if self.model.filepath == '':
            return "break"
        self.model.txt_to_memory()
        if self.model.memory[0] == 42:
            self.view.error_window("Wrong map format!")
            self.model.memory = []
            return "break"
        self.view.clear_and_repaint()
        self.view.paint_from_imported(self.model.memory)
        self.view.importbtn.configure(relief='raised')
        self.view.editflag = 0
        return "break"  # to not proceed further (if break wasn't returned the button would remain sunken)

    def saving(self, event):
        i = self.model.data_correctness()
        if i == 0:
            self.view.error_window("Missing vital elements!\n(P1/P2 start or endpoint)")
            return

        sv, entr, text, button = self.view.save_window()
        button.configure(command=lambda: self.final_save(sv, entr, text, button))


    def final_save(self, sv, entry, text, button):
        tmp = entry.get()
        if tmp == "":
            text.configure(text="Filename missing!", fg="red")
            return

        if self.view.save_text.get() == "Confirm":
            if tmp + ".txt" == self.model.filename:
                i = 0
                self.model.store_map(i)
                self.view.editflag = 0
                sv.destroy()
                return
        text.configure(text="Enter filename:", fg="black")
        self.view.save_text.set("Save")
        self.model.filename = entry.get()
        i = self.model.name_check()
        self.model.filename = self.model.filename + ".txt"
        if i == 0:
            text.configure(text="Use only numbers and letters in filename!", fg="red")
            return

        i = self.model.path_check()
        if i == 0:
            text.configure(text="File already exists, overwrite?", fg="black")
            self.view.save_text.set("Confirm")
            return

        self.model.store_map(i)
        self.view.editflag = 0
        sv.destroy()


    ##################################################################

    def check_mem(self, i, cur):  # cur(current mode)
        if self.model.memory[i+2] == 1:
            if cur == 1:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 2:
            if cur == 2:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 3:
            if cur == 3:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 4:
            if cur == 4 or cur == 6:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
                if cur == 6:
                    self.model.erasing_obst2 = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 5:
            if cur == 5:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 7:
            if cur == 7:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
        elif self.model.memory[i+2] == 8:
            if cur == 8:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)
                self.elremoved = 1
            else:
                self.view.paint_blank(self.model.mousex, self.model.mousey)
                self.model.rm_element(i)




    def double_check(self, x, y, cur):  # makes sure there is only one starting point/endpoint for each player
        for j in range(len(self.model.memory)):
            if j % 3 == 0 and (self.model.memory[j] != x or self.model.memory[j+1] != y):
                if (self.model.memory[j+2] == 1 and cur == 1) or (self.model.memory[j+2] == 2 and cur == 2) or\
                        (self.model.memory[j+2] == 5 and cur == 5) or (self.model.memory[j+2] == 8 and cur == 8):
                    self.view.paint_blank(self.model.memory[j], self.model.memory[j+1])
                    self.model.rm_element(j)
                    return

    def handle_mode6(self, x, y, px, py):
        if x < px:
            tmp = px
            px = x
            x = tmp
        if y < py:
            tmp = py
            py = y
            y = tmp
        
        curx = px
        cury = py
        const = 20
        inmem = 0

        while cury != y + const:
            while curx != x + const:
                inmem = 0
                for i in range(len(self.model.memory)):  # check what is painted on the coordinates
                    if i % 3 == 0:  # 1 element comprises of 3 values
                        if curx == self.model.memory[i] and cury == self.model.memory[i+1]:
                            inmem = 1
                            if self.model.erasing_obst2 == 1:  # if we are erasing
                                self.view.paint_blank(curx, cury)
                                self.model.rm_element(i)
                                break
                            if self.model.memory[i+2] != 4:  # something else than wall
                                self.view.paint_blank(curx, cury)
                                self.view.paint_wall(curx, cury)
                                self.model.memory[i+2] = 4
                                break
                            else:
                                break
                if inmem == 0 and self.model.erasing_obst2 == 0:
                    self.view.paint_wall(curx, cury)
                    self.model.store(curx, cury, 4)
                curx += const

            curx = px
            cury += const



