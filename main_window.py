#!/usr/bin/python
#
# Project: GUI application (for subject ITU on BUT)
# Brief: Code for the controller part of the main menu
# Author: Stanislav Gabriš (xgabri18)

from MenuView import *
from Edit_Controller import *
from Game_Controller import *


class MainWindow:
    def __init__(self, app):
        self.root = app
        self.top = app
        self.actual = EController
        self.view = MenuView(app)

        self.view.EButton.bind("<Button-1>", self.top_editor)
        self.view.GButton.bind("<Button-1>", self.top_game)


    def top_editor(self,event):
        self.root.withdraw()
        self.top = tk.Toplevel()
        self.actual = EController(self.top)
        self.root.wait_window(self.top)
        if self.actual.view.back == 1:
            self.root.deiconify()
            return "break"
        self.root.destroy()
        exit(1)

    def top_game(self,event):
        self.root.withdraw()
        self.top = tk.Toplevel()
        self.actual = Controller(self.top)

        self.root.wait_window(self.top)
        if self.actual.view.back == 1:
            self.root.deiconify()
            return "break"
        self.root.destroy()
        exit(0)