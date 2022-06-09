#!/usr/bin/python

# This is student project at VUT university at Brno
# Made by Adam Fabo (xfaboa00)
# Licence: none - you are free to shace this code as you please

import tkinter as tk


def check_winning_condition(map,map_zaloha,num,tmp_cur):
    if (map_zaloha[tmp_cur[1] - 1][tmp_cur[0] - 1] == 4 or map_zaloha[tmp_cur[1] - 1][tmp_cur[0] - 1] == 5):
        # sedmicka su kruzky prveho hraca
        if map_contains_backend(num + 5,map) == False:
            return True

    return False

def map_contains_backend(num,mapa):
    for i in range(34):
        for j in range(48):
            if (mapa[i][j] == num):
                return True

    return False

def check_validity_of_cursor(cursor,mapa):
    if cursor[0] <= 0 or cursor[0] > 48  or cursor[1] <= 0 or cursor[1] > 34:
        return False
    elif mapa[cursor[1] - 1][cursor[0] - 1] != 0 and mapa[cursor[1] - 1][cursor[0] - 1] != 7 and mapa[cursor[1] - 1][cursor[0] - 1] != 6  and mapa[cursor[1] - 1][cursor[0] - 1] != 4  and mapa[cursor[1] - 1][cursor[0] - 1] !=5:
        return False

    return True