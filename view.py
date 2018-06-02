import pygame
from random import randint

class Label():
    """Class to manage labels"""
    
    def __init__(self, text='', x=0, y=0):
        """Initiation of object label"""
        
        #Some defaults
        self.text = text
        self.text_color = (255, 255, 255)
        self.text_size = 36
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, self.text_size)
        self.text_img = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.left = self.x
        self.text_rect.top = self.y
        
    def render(self):
        self.text_img = self.font.render(self.text, True, self.text_color)
            

class GraphicalView:
    """
    This class is responsible for drawing game
    """
    
    def __init__(self, model):
        result = pygame.init()
        self.isInitialized = True
        self.model = model
        self.current_level = self.model.level
            
        self.screen_height = 700
        self.screen_width = 700
        
        self.level = Label('Level: ' + str(self.model.level))
        self.text_height =  self.level.text_rect.height
        self.points = Label('Points: ' + str(self.model.points))
        self.moves = Label('Moves: ' + str(self.model.moves))
                
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height + self.text_height))
        self.clock = pygame.time.Clock()
        self.init_view()

    def init_view(self):   
        self.points.text_rect.centerx = int(self.screen_width/2)
        self.moves.text_rect.right = self.screen_width
        
        self.block_width = self.screen_width/self.model.grid_x 
        self.block_height = self.screen_height/self.model.grid_y
        self.block_rect = pygame.Rect(0, 0, self.block_width-5, self.block_height-5)
        self.colors = []
        for x in range(self.model.number_of_colors):
            self.colors.append(self.getRandomColor()) 
    
    def getRandomColor(self):
        return (randint(0,255), randint(0,255), randint(0,255)) 
    
        
    def notify(self, event):
        if event.type == pygame.QUIT:
            self.isInitialized = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and self.model.moves > 0:
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                x = int(position[0] / self.block_width) 
                y =  int((position[1] - self.text_height) / self.block_height) 
                if self.model.grid[(x,y)] != None:
                    self.model.remove_blocks(x, y)
                        
                
    def update(self):
        if self.isInitialized:
            if self.current_level != self.model.level:
               self.current_level = self.model.level
               self.init_view()
                
            self.screen.fill((0,0,0))
            self.level.text = 'Level: ' + str(self.model.level)
            self.points.text = 'Points: ' + str(self.model.points)
            self.moves.text = 'Moves: ' + str(self.model.moves)
            self.level.render()
            self.points.render()
            self.moves.render()
            
            self.screen.blit(self.level.text_img, self.level.text_rect)
            self.screen.blit(self.points.text_img, self.points.text_rect)
            self.screen.blit(self.moves.text_img, self.moves.text_rect)


            for x in range(self.model.grid_x):
                for y in range(self.model.grid_y):
                    if self.model.grid[(x,y)] != None:
                        col = self.model.grid[(x,y)].color
                        selected = self.model.grid[(x,y)].selected
                        if selected:
                            self.block_rect.width = self.block_width-1
                            self.block_rect.height = self.block_height-1
                        else:
                            self.block_rect.width = self.block_width-5
                            self.block_rect.height = self.block_height-5
                            
                        self.block_rect.centerx = x * self.block_width + int(self.block_width/2)
                        self.block_rect.centery = y * self.block_height + int(self.block_height/2) + self.text_height
                        pygame.draw.rect(self.screen, self.colors[col], self.block_rect)
            
            pygame.display.flip()  
            self.clock.tick(30)
        
