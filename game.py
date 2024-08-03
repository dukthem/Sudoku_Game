import pygame
import os

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (400, 700)

surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Sudoku")

running = True

while running:
    
    #check for input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        surface.fill((0,0,0))
        
        pygame.display.flip()