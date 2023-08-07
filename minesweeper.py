#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:00:49 2022

@author: hbasnight01
"""

import random
import time


class Point:
    def __init__(self, row, col, character, bomb, flag, mined, neighbors):
        self.row = row
        self.col = col
        self.character = character
        self.bomb = bomb
        self.flag = flag
        self.mined = mined
        self.neighbors = neighbors
        self.original_char = character
    
    def mine(self, g):
        self.mined = True
        if self.flag:
            return True
        if self.character == 'x':
            return False
        elif self.character == '.':
            for i in self.neighbors:
                if not g.grid[i[0]][i[1]].mined and not g.grid[i[0]][i[1]].flag:
                    g.grid[i[0]][i[1]].mine(g)
        return True
        
    def set_bomb(self):
        self.bomb = True
        self.character = 'x'
        return
        
    def is_bomb(self):
        return self.bomb
    
    def set_num(self, count):
        self.character = count
        return
    
    def toggle_flag(self, num_flags):
        if self.flag:
            self.flag = False
            temp = self.character
            self.character = self.original_char
            self.original_char = temp
            #self.mined = False
            num_flags -= 1
        else:
            self.flag = True
            self.original_char = self.character
            self.character = '!'
            num_flags += 1
        return num_flags
            

    def __repr__(self):
        return self.character


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = create_grid(rows, cols)
    
    def __repr__(self):
        return print_grid(self)


def print_grid(g):
    print()
    print('     ', end='')
    for i in range(g.cols):
        print(f'{i:2}', end=' ')
    print()
    
    print('   +', end='')
    for i in range(g.cols):
        print('---', end='')
    print('--+')
    
    for i in range(g.rows):
        print(f'{i:2} |', end=' ')
        for j in range(g.cols):
            if g.grid[i][j].flag: print(' !', end=' ')
            elif g.grid[i][j].mined: print('', g.grid[i][j].character, end=' ')
            else: print(' -', end=' ')
        print(' |')
    
    print('   +', end='')
    for i in range(g.cols):
        print('---', end='')
    print('--+')
    print()
    return


def final_print(g):
    print()
    print('     ', end='')
    for i in range(g.cols):
        print(f'{i:2}', end=' ')
    print()
    
    print('   +', end='')
    for i in range(g.cols):
        print('---', end='')
    print('--+')
    
    for i in range(len(g.grid)):
        print(f'{i:2} |', end=' ')
        for j in range(len(g.grid[i])):
            if g.grid[i][j].flag: 
                g.grid[i][j].toggle_flag(0)
                print('', g.grid[i][j].character, end=' ')
                g.grid[i][j].toggle_flag(0)
            else:
                print('', g.grid[i][j].character, end=' ')
        print(' |')
    
    print('   +', end='')
    for i in range(len(g.grid)):
        print('---', end='')
    print('--+')
    print()
    return


def check_grid(g):
    for i in range(len(g.grid)):
        for j in range(len(g.grid[i])):
            if not g.grid[i][j].is_bomb() and not g.grid[i][j].mined:
                return False
    return True


def create_grid(rows, cols):
    g = []
    for i in range(rows):
        temp = []
        for j in range(cols):
            temp.append(Point(i, j, '.', False, False, False, get_neighbors(i, j, rows, cols)))
        g.append(temp)
    return g


def populate_mines(g, difficulty, choice_x = -1, choice_y = -1):
    total = 0
    for i in range(len(g.grid)):
        for j in range(len(g.grid[i])):
            if i == choice_x and j == choice_y:
                continue
            chance = random.randint(1, difficulty)
            if chance == 1:
                g.grid[i][j].set_bomb()
                total += 1
    return total


def get_neighbors(x, y, max_x, max_y):
    n = []
    if x-1 >= 0 and y-1 >= 0: n.append((x-1, y-1))
    if y-1 >= 0: n.append((x, y-1))
    if x+1 < max_x and y-1 >= 0: n.append((x+1, y-1))
    if x-1 >= 0: n.append((x-1, y))
    if x+1 < max_x: n.append((x+1, y))
    if x-1 >= 0 and y+1 < max_y: n.append((x-1, y+1))
    if y+1 < max_y: n.append((x, y+1))
    if x+1 < max_x and y+1 < max_y: n.append((x+1, y+1))
    return n


def populate_nums(g):
    for i in range(len(g.grid)):
        for j in range(len(g.grid[i])):
            neighbors = get_neighbors(i, j, len(g.grid), len(g.grid[i]))
            count = 0
            for k in neighbors:
                if k[0] >= 0 and k[0] < len(g.grid) and k[1] >= 0 and k[1] < len(g.grid[i]):
                    if g.grid[k[0]][k[1]].is_bomb():
                        count += 1
            if count > 0 and not g.grid[i][j].is_bomb():
                g.grid[i][j].set_num(count)
    return
                     

num_rows = int(input('Enter the number of rows (height) for the map: ').strip())
while num_rows <= 0:
    print('There must be at least one row.')
    num_rows = int(input('Enter the number of rows (height) for the map: ').strip())

num_cols = int(input('Enter the number of columns (width) for the map: ').strip())
while num_cols <= 0:
    print('There must be at least one column.')
    num_cols = int(input('Enter the number of columns (width) for the map: ').strip())

while num_rows * num_cols > 2000 or num_rows > 100 or num_cols > 100:
    print('Map is too big. Please limit to 2000 tiles and a maximum dimension of 100.')
    num_rows = int(input('Enter the number of rows (height) for the map: ').strip())
    num_cols = int(input('Enter the number of columns (width) for the map: ').strip())

difficulty = int(input('Enter difficulty: \'0\' for easy, \'1\' for medium, and \'2\' for hard: '))
while difficulty != 0 and difficulty != 1 and difficulty != 2:
    difficulty = int(input('Invalid input. Enter difficulty: \'0\' for easy, \'1\' for medium, and \'2\' for hard: '))

if difficulty == 0:
    difficulty = 16
elif difficulty == 1:
    difficulty = 10
else:
    difficulty = 5

g = Grid(num_rows, num_cols)

num_flags = 0
print_grid(g)

while True:
    choice_x = input('Enter the row of a tile to mine: ')
    while int(choice_x) < 0 or int(choice_x) >= g.rows:
        choice_x = input('Out of bounds. Enter the row of a tile to mine: ')
    choice_y = input('Enter the column of a tile to mine (or \'c\' to cancel): ')
    if choice_y == 'c':
        continue
    while int(choice_y) < 0 or int(choice_y) >= g.cols:
        choice_y = input('Out of bounds. Enter the column of a tile to mine (or \'c\' to cancel): ')
        if choice_y == 'c':
            continue
    break

choice_x = int(choice_x)
choice_y = int(choice_y)
alive = True

total = populate_mines(g, difficulty, choice_x, choice_y)
populate_nums(g)
g.grid[choice_x][choice_y].mine(g)

print_grid(g)
print(total - num_flags, 'bombs remaining.')
start = time.time()

while True:
    choice_x = input('Enter the row of a tile to mine: ')
    while int(choice_x) < 0 or int(choice_x) >= g.rows:
        choice_x = input('Out of bounds. Enter the row of a tile to mine: ')
    choice_y = input('Enter the column of a tile to mine (or \'c\' to cancel): ')
    if choice_y == 'c':
        continue
    while int(choice_y) < 0 or int(choice_y) >= g.cols:
        choice_y = input('Out of bounds. Enter the column of a tile to mine (or \'c\' to cancel): ')
        if choice_y == 'c':
            continue
    flag = input('Toggle flag? (\'y\' or \'n\'): ').lower()
    while flag != 'y' and flag != 'n':
        flag = input('Invalid input. Toggle flag? (\'y\' or \'n\'): ').lower()
    
    choice_x = int(choice_x)
    choice_y = int(choice_y)
    alive = True
    
    if flag == 'y':
        num_flags = g.grid[choice_x][choice_y].toggle_flag(num_flags)    
    else:
        alive = g.grid[choice_x][choice_y].mine(g)
    
    if check_grid(g) or not alive:
        end = time.time()
        final_print(g)
        if not alive:
            print('Game over.')
        else:
            print('You win.')
        mins = int(end - start) // 60
        secs = int(end - start) % 60
        print('Time elapsed:', mins, 'minute', end='')
        if mins != 1:
            print('s', end=' ')
        print(secs, 'second', end='')
        if secs != 1:
            print('s')
        else:
            print()

        # calculate bombs flagged correctly, number of incorrect flags, and bombs left unflagged
        
        total_flags = 0
        correct_flags = 0
        incorrect_flags = 0
        unflagged_mines = 0
        
        for i in g.grid:
            for j in i:
                if j.flag:
                    total_flags += 1
                    if j.is_bomb():
                        correct_flags += 1
                    else:
                        incorrect_flags += 1
                elif j.is_bomb():
                    unflagged_mines += 1
        
        print('Total mines:', total)
        print('Flags used:', total_flags)
        print('Correct flags:', correct_flags)
        print('Incorrect flags:', incorrect_flags)
        print('Unflagged mines:', unflagged_mines)
        break
    
    else:
        print_grid(g)
        print(total - num_flags, 'bombs remaining.')
        
        
        
        
        
        
        
        
        