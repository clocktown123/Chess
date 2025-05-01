import pygame
import sys
from map import Map
from pieces import BluePawn, BlackPawn


pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

def main():

    #pieces
    BluePawns = [BluePawn((10,600), (80, 80)), BluePawn((110,600), (80, 80)), BluePawn((210,600), (80, 80)), BluePawn((310,600), (80, 80)), BluePawn((410,600), (80, 80)), BluePawn((510,600), (80, 80)), BluePawn((610,600), (80, 80)), BluePawn((710,600), (80, 80))]
    BlackPawns = [BlackPawn((10,100), (80, 80)), BlackPawn((110,100), (80, 80)), BlackPawn((210,100), (80, 80)), BlackPawn((310,100), (80, 80)), BlackPawn((410,100), (80, 80)), BlackPawn((510,100), (80, 80)), BlackPawn((610,100), (80, 80)), BlackPawn((710,100), (80, 80))]
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


        
        #physics---------------------------------------------------


        #Render section
        
        screen.fill((0, 0, 0))

        Map(screen)

        for i in BluePawns:
            i.draw(screen)
        for i in BlackPawns:
            i.draw(screen)

        pygame.display.flip()

    #end of GAME LOOP##############################################
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
