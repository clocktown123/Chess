import pygame
import sys
from map import Map
from pieces import pawn

p = []

pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

def main():

    #Mouse variables
    mxpos = 0
    mypos = 0
    mousePos = (mxpos, mypos)
    mouseDown = False

    running = True
    clock.tick(60)
    while running: #GAME LOOP####################################
        #event section------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False

        keys = pygame.key.get_pressed()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     Mshoot = True
        
        #physics---------------------------------------------------


        #Render section
        
        screen.fill((0, 0, 0))



        Map(screen)

        pygame.display.flip()

    #end of GAME LOOP##############################################
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
