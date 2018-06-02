import pygame
from random import randint

class Block:
    """
    Class which describes one block 
    """
    def __init__(self, number_of_colors):
        self.color = randint(0, number_of_colors-1)
        self.selected = False

class GameEngine:
    """
    This class contains methods which controls all game elements
    """
    
    def __init__(self):
        self.running = True
        self.level = 1
        self.points = 0
        self.level_init(self.points)
        
    def level_init(self, p):
        self.grid_x = self.level + 4
        self.grid_y = self.level + 4
        self.moves = self.grid_x + self.grid_y + p
        self.number_of_colors = int(self.level * 0.2) + 4
        self.grid = {}
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.grid[(x,y)] = Block(self.number_of_colors-1)    
        self.number_of_blocks = self.grid_x * self.grid_y        
        
    def notify(self, event):
        if event.type == pygame.QUIT:
            self.running = False
    
    def update(self):
        pass


    def remove_selection(self):
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.grid[(x,y)] != None:
                    self.grid[(x,y)].selected = False


    def select_block(self, x, y, current_color=None):
        if 0 <= x < self.grid_x and 0 <= y < self.grid_y:
            if self.grid[(x,y)] != None:
                if current_color == None:
                    current_color = self.grid[(x,y)].color
                if current_color == self.grid[(x,y)].color:
                    if self.grid[(x,y)].selected == False:
                        self.grid[(x,y)].selected = True
                        self.select_block(x+1, y, current_color)
                        self.select_block(x-1, y, current_color)
                        self.select_block(x, y+1, current_color)
                        self.select_block(x, y-1, current_color)


    def select_blocks(self, x, y):
        self.remove_selection()
        self.select_block(x, y)
        

    def remove_block(self, x, y, current_color=None):
        if 0 <= x < self.grid_x and 0 <= y < self.grid_y:
            if self.grid[(x,y)] != None:
                if current_color == None:
                    current_color = self.grid[(x,y)].color
                if current_color == self.grid[(x,y)].color:
                    self.grid[(x, y)] = None
                    self.number_of_blocks -= 1
                    self.remove_block(x+1, y, current_color)
                    self.remove_block(x-1, y, current_color)
                    self.remove_block(x, y+1, current_color)
                    self.remove_block(x, y-1, current_color)
                    
    
    def move_column_down(self, x):
        y = self.grid_y - 1
        destination = None
        while y >= 0:
            if self.grid[(x,y)] == None: 
                if destination == None:
                    destination = y
            else:
                if destination != None:
                    self.grid[(x,destination)] = self.grid[(x,y)]
                    self.grid[(x,y)] = None
                    destination -= 1
            y -= 1
            

    def move_blocks_down(self):
        for x in range(self.grid_x):
            self.move_column_down(x)
                        
     
    def move_columns_left(self):
        destination = None
        for x in range(self.grid_x):
            y = self.grid_y - 1
            if self.grid[(x,y)] == None:
                if destination == None:
                    destination = x
            else:
                if destination != None:
                    while y >= 0:
                        self.grid[(destination,y)] = self.grid[(x,y)]
                        self.grid[(x,y)] = None
                        y -= 1
                    destination += 1
                        
                
    def remove_blocks(self, x, y):
        if self.grid[(x,y)].selected:
            self.remove_block(x, y)
            self.move_blocks_down()
            self.move_columns_left()
            if self.moves > 0:
                self.moves -= 1
            if self.number_of_blocks <= 0:
                self.level += 1
                self.points += self.moves
                self.level_init(self.moves)
        else:
            self.select_blocks(x,y)
