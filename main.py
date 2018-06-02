import model
import view
import pygame

"""
This is controler.
"""

game_engine = model.GameEngine()
graphical_view = view.GraphicalView(game_engine)

while game_engine.running:
    
    #pass event to model and view 
    for event in pygame.event.get():
        graphical_view.notify(event)
        game_engine.notify(event)

    game_engine.update()
    graphical_view.update()
    
            
