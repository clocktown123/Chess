import pygame
import sys
from map import Map
from pieces import Pawn




pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()


def main():


    #pieces
    BluePawns = [Pawn((10,600), (80, 80)), Pawn((110,600), (80, 80)), Pawn((210,600), (80, 80)), Pawn((310,600), (80, 80)), Pawn((410,600), (80, 80)), Pawn((510,600), (80, 80)), Pawn((610,600), (80, 80)), Pawn((710,600), (80, 80))]
    BlackPawns = [Pawn((10,100), (80, 80)), Pawn((110,100), (80, 80)), Pawn((210,100), (80, 80)), Pawn((310,100), (80, 80)), Pawn((410,100), (80, 80)), Pawn((510,100), (80, 80)), Pawn((610,100), (80, 80)), Pawn((710,100), (80, 80))]
    #Mouse variables
    mxpos = 0
    mypos = 0
    mousePos = (mxpos, mypos)
    mouseDown = False


    #Turn
    turn = "Blue"


    running = True
    clock.tick(60)
    while running: #GAME LOOP####################################
        #event section------------------------------------
        for event in pygame.event.get():
            mouseX, mouseY = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
           


       


        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False


        keys = pygame.key.get_pressed()




        print(BluePawns[0].PawnBox)
        #physics---------------------------------------------------
        if turn == "Blue":
            for i in BluePawns:
                i.BlueMove(mouseX, mouseY, mouseDown)
                if i.BlueMove(mouseX, mouseY, mouseDown):
                    turn = "Black"
        if turn == "Black":
            for i in BlackPawns:
                i.BlackMove(mouseX, mouseY, mouseDown)
                if i.BlackMove(mouseX, mouseY, mouseDown):
                    turn = "Blue"
        #Render section
       
        screen.fill((0, 0, 0))


        Map(screen)
       
        for i in BluePawns:
            i.BlueDraw(screen)
        for i in BlackPawns:
            i.Blackdraw(screen)


        pygame.display.flip()


    #end of GAME LOOP##############################################
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

