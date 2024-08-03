import pygame
import os 
from grid import Grid

# set the window position relative to the screen upper left corner
os.environ["SOL_VIDEO_WINDOW_POS"] = "%d,%d" % (400, 100)

# create the window surface and set the window caption
surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("SUDOKU")


pygame.font.init()
game_font = pygame.font.SysFont(name= 'Comfortaa', size= 55)
game_font2 = pygame.font.SysFont(name= 'Comfortaa', size= 35)

#the game loop
grid = Grid(pygame, game_font)
running = True

while running:

    # check for input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()


    
    #clear the window surface to black
    surface.fill((0, 0, 0))

    #draw the grid here
    grid.draw_all(pygame, surface)
    
    if grid.win:
        won_surface = game_font.render("YOU WON", False,  (0, 255, 0))
        surface.blit(won_surface, dest=(950, 650))

        press_space_surf = game_font2.render("Press Space to restart!", False, (0, 255, 200))
        surface.blit(press_space_surf, dest=(920,750))
    #update the window surface
    pygame.display.flip()